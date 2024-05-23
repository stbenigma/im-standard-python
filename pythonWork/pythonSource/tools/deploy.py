#!/usr/bin/python3
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import argparse
from datetime import datetime

from nbconvert import PythonExporter
from traitlets.config import Config
import nbformat as nbf
import zipfile
import logging

from SSOT_infra import parameters

arguments = argparse.Namespace(verbose=True)

DEFAULT_DIST_FOLDER = './dist'

EXCLUDE_LIST = [
    'pythonWork/pythonSource/IM_WEB/testallwebfillallin1.py',
    'pythonWork/pythonSource/PUBLISH_MODEL/sharepoint/shareplum_sandbox.py',
]


def log(msg):
    """Poor man's logging"""
    global arguments
    if arguments.verbose:
        logging.info(msg)
        print(msg)


def notebook_to_python(source: Path, exporter, destination):
    with open(source, 'r') as src:
        nb = nbf.read(src, nbf.NO_CONVERT)

    source, meta = exporter.from_notebook_node(nb)
    with open(destination, 'w') as dst:
        dst.write(source)
    return source, meta


def hardcode_version(version: str, pattern: str, subject) -> int:
    """
    Replace label
    :param version:
    :param pattern:
    :param subject:
    :return:
    """

    subject = Path(subject)
    assert subject.is_file()

    replaced = 0
    with open(subject, 'r') as source:
        fp = source
        dst, temp_name = tempfile.mkstemp()
        for line in fp.readlines():
            rewrite = re.sub(pattern, version, line)
            if rewrite != line:
                replaced += 1
            os.write(dst, (rewrite + os.linesep).encode())
        os.close(dst)
        if replaced > 0:
            logging.debug(f"Replacing {subject} with updated content in {temp_name}")
            shutil.move(temp_name, subject)
            logging.info(f"Substituted {replaced} locations in {subject}")
    return replaced


def notebook_to_python_script(scripts: [Path], destination_folder: Path, strip_cells_with_tags) -> [Path]:
    c = Config()
    c.TagRemovePreprocessor.remove_cell_tags = strip_cells_with_tags
    c.TagRemovePreprocessor.enabled = True
    c.PythonExporter.preprocessors = ["nbconvert.preprocessors.TagRemovePreprocessor"]

    exporter = PythonExporter(config=c)
    targets = []
    for script in scripts:
        if not os.path.exists(script):
            continue #skip non existing notebooks, as is the case in production environment
        script_file = str(script)
        filename = os.path.basename(script_file)
        noext, _ = os.path.splitext(filename)
        target = destination_folder / (noext + '.py')

        log(f"Converting {script_file} to plain python")
        notebook_to_python(script_file, exporter, target)
        log(f"Wrote {os.path.abspath(target)}. Removed cells with tags {strip_cells_with_tags}")

        target.chmod(0o755)
        targets.append(target)

    return targets


def main(basefolder: Path, argv: []):
    global arguments
    strip_cells_with_tags = ("test", "visual", "debug")

    parser = argparse.ArgumentParser(description="Build generator and deployment package")
    parser.add_argument('--verbose', '-v', action='store_true', dest='verbose')
    parser.add_argument('--output', '-o', dest='output', default=DEFAULT_DIST_FOLDER,
                        help="Output folder for distribution")
    parser.add_argument('notebook', metavar='notebook.ipynb', type=str,
                        default='notebooks/mig/generator.ipynb',
                        nargs='?', help="Source Jupyter Notebook")
    arguments = parser.parse_args(argv)

    destination_folder = Path(arguments.output)
    if not destination_folder.is_absolute():
        destination_folder = basefolder / arguments.output
    destination_folder.mkdir(exist_ok=True)
    logging.info(f"Distribution to {destination_folder.resolve()}")

    if basefolder is None:
        basefolder = Path.cwd()
    pythonsourcefolder= basefolder / 'pythonWork' / 'pythonSource'
    confluencefolder= basefolder / "notebooks" / "confluence-export"

    script_file = Path(basefolder, arguments.notebook)
    renderfile= confluencefolder /"Renderer.ipynb"
    uploadfile = confluencefolder / "Uploader.ipynb"
    targets = notebook_to_python_script([ script_file,renderfile,uploadfile],
                                        destination_folder, strip_cells_with_tags)
    targetgenerator = targets[0]


    version_file = pythonsourcefolder / 'SSOT_infra' / 'versions.json'
    if version_file.is_file():
        with open(version_file, 'r') as src:
            version = json.load(src)
            version_mark = f"{version['TOOLVERSION']} (Schema {version['DBVERSION']})"
    else:
        logging.warning(f"Cannot read version file {version_file.resolve()}")

    hardcode_version("VERSION_TAG = '" + version_mark + "'", r"VERSION_TAG\s*=\s*['\"].+['\"]", targetgenerator)

    git_tag = parameters.toolversion()

    package_name = f"model2diagram-{version['TOOLVERSION']}"
    archive = destination_folder / (package_name + '.zip')

    now = datetime.now()
    stamp = now.strftime("%Y-%m-%d %H:%M:%S")
    version_string = f'{{ "version": "{version["TOOLVERSION"]}", "schema": "{version["DBVERSION"]}", "git": "{git_tag}", timestamp: "{stamp}" }}'

    log("Version " + version_string)

    stamp_file = destination_folder / 'stamp.json'
    with open(stamp_file, 'w') as vfile:
        vfile.write(version_string + '\n')

    windows_runner = basefolder / 'run.bat'
    tasksfile = basefolder / 'tasks.py'
    requirementsfile = basefolder / 'requirements.txt'

    confluencelocale = confluencefolder / "locale"
    confluencejinja = confluencefolder / "templates"


    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as zip:
        for target in targets:
            zip.write(target,  target.relative_to(target.parent.parent))
        zip.write(stamp_file, stamp_file.relative_to(stamp_file.parent))
        zip.write(tasksfile, tasksfile.relative_to(tasksfile.parent))
        zip.write(requirementsfile, requirementsfile.relative_to(requirementsfile.parent))
        zip.write(windows_runner, windows_runner.relative_to(basefolder))
        zipdir(pythonsourcefolder, zip, basefolder)
        zipdir(confluencelocale, zip, basefolder, lambda f: not f.endswith('DS_Store'))
        zipdir(confluencejinja, zip, basefolder, lambda f: not f.endswith('DS_Store'))
        # add resources
        zipdir(basefolder / 'res', zip, basefolder, lambda f: not f.endswith('DS_Store'))

    log(f"Packed up archive {archive}")
    return archive


def generate_translations():
    # prepare translation files
    base = Path(__file__).parent.parent / 'SSOT_infra' / 'locales'
    sources = list(base.rglob('**/*.po'))
    for po_source in sources:
        pre, ext = os.path.splitext(po_source)
        mo_target = pre + '.mo'
        subprocess.check_output(['msgfmt', '-o', mo_target, po_source])
    log(f"Updated {len(sources)} translations {sources}")


def accept(path: str):
    file = os.path.basename(path)
    file_path = Path(path).resolve()

    # exclude
    if '/venv/' in path: return False
    if file is None: return False
    if len(Path(path).parts) < 2: return False  # skip python files in root
    if file_path.match('**/tests/*.py'): return False  # skip unittests
    if file_path.match('**/testenvironment/**/*.*'): return False  # skip testdata
    if "unittest-tmp-dir" in map(lambda part: str(part), file_path.parts): return False

    if str(path) in EXCLUDE_LIST:
        logging.debug(f"Skipping {file} on EXCLUDE_LIST")
        return False

    # include
    if file.endswith('.py'): return True  # source files
    if file.endswith('.mo'): return True  # gettext message catalog
    if file_path.match('**/dbstructure/sqlite/*.*'): return True

    if file_path.match('**/IM_WEB/html-lib/**/*.*'): return True
    if file_path.match('**/IM_WEB/html-lib/images/icons/*.*'): return True
    if file_path.match('**/IM_WEB/html-lib/images/icons/**/*.*'): return True

    if 'modelmodel_sqlite.sql' in file: return True
    if 'versions.json' in file: return True

    # none -> exclude
    return False


def zipdir(path, ziph, content_root, path_filter=accept):
    """
        Add files matching path_filter to zip with path relative to content_root
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            path = os.path.join(root, file)
            relpath=os.path.relpath(path, content_root)
            if path_filter(relpath):
                log(f"Packing {path}")
                ziph.write(path, relpath)


if __name__ == '__main__':
    result = main(Path.cwd(), sys.argv[1:])
    with zipfile.ZipFile(result, 'r') as archive:
        print(f"{len(archive.filelist)} files packed into distribution bundle {result.resolve()}")
