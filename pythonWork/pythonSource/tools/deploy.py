#!/usr/bin/python3
import os
import re
import subprocess
import sys
from pathlib import Path
import argparse
from datetime import datetime
from subprocess import check_output, CalledProcessError
from nbconvert import PythonExporter
from traitlets.config import Config
import nbformat as nbf
import zipfile

arguments = argparse.Namespace(verbose=True)


def log(msg):
    """Poor man's logging"""
    global arguments
    if arguments.verbose:
        print(msg)


def notebook_to_python(source, exporter, destination):
    with open(source, 'r') as src:
        nb = nbf.read(src, nbf.NO_CONVERT)

    source, meta = exporter.from_notebook_node(nb)
    with open(destination, 'w') as dst:
        dst.write(source)
    return source, meta


def main(basefolder: Path, argv: []):
    global arguments
    strip_cells_with_tags = ("test", "visual", "debug")

    parser = argparse.ArgumentParser(description='Build generator and deployment package')
    parser.add_argument('--verbose', '-v', action='store_true', dest='verbose')
    parser.add_argument('notebook', metavar='notebook.ipynb', type=str,
                        default='notebooks/mig/generator.ipynb',
                        nargs='?', help="Source Jupyter Notebook")
    arguments = parser.parse_args(argv)

    script_file = arguments.notebook

    if basefolder is None:
        basefolder = Path.cwd()

    c = Config()
    c.TagRemovePreprocessor.remove_cell_tags = strip_cells_with_tags
    c.TagRemovePreprocessor.enabled = True

    c.PythonExporter.preprocessors = ["nbconvert.preprocessors.TagRemovePreprocessor"]

    exporter = PythonExporter(config=c)

    filename = os.path.basename(script_file)
    noext, _ = os.path.splitext(filename)
    target = basefolder / (noext + '.py')

    log(f"Converting {script_file} to plain python")
    notebook_to_python(script_file, exporter, target)
    log(f"Wrote {os.path.abspath(target)}. Removed cells with tags {strip_cells_with_tags}")

    # prepare translation files
    base = Path(__file__).parent.parent / 'SSOT_infra' / 'locales'
    sources = list(base.rglob('**/*.po'))
    for po_source in sources:
        pre, ext = os.path.splitext(po_source)
        mo_target = pre + '.mo'
        subprocess.check_output(['msgfmt', '-o', mo_target, po_source])
    log(f"Updated {len(sources)} translations {sources}")

    git_tag = 'dev'

    try:
        git_tag = check_output(['git', 'describe', '--always']).decode().strip()
    except CalledProcessError as e:
        print(f"Warning: Cannot read git repository status")

    version = 'master'

    with open(target, 'r') as src:
        expression = re.compile(r'notebook_version\s*=\s*"([^"]+)"')
        for line in src.readlines():
            match = expression.match(line)
            if match:
                version = match.group(1)

    package_name = f'model2diagram-{version}'
    archive = basefolder / (package_name + '.zip')

    now = datetime.now()
    stamp = now.strftime("%Y-%m-%d %H:%M:%S")
    version_string = f'{{ "version": "{version}", "git": "{git_tag}", timestamp: "{stamp}" }}'

    log("Version " + version_string)

    version_file_name = basefolder / 'version.json'
    with open(version_file_name, 'w') as vfile:
        vfile.write(version_string + '\n')

    windows_runner = basefolder / 'run.bat'

    tools = basefolder / 'pythonWork' / 'pythonSource'

    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as zip:
        zip.write(target, target.relative_to(target.parent))
        zip.write(version_file_name, version_file_name.relative_to(basefolder))
        zip.write(windows_runner, windows_runner.relative_to(basefolder))
        zipdir(tools, zip, tools)

    log(f"Packed up archive {archive}")
    return archive


def accept(path: str):
    file = os.path.basename(path)
    file_path = Path(path).resolve()

    if '/venv/' in path: return False
    if file is None: return False
    if len(Path(path).parts) < 2: return False # skip python files in root
    if file_path.match('**/tests/*.py'): return False  # skip unittests
    if file_path.match('**/testenvironment/**/*.*'): return False  # skip testdata

    if file.endswith('.py'): return True  # source files
    if file.endswith('.mo'): return True  # gettext message catalog
    if file_path.match('**/IM_WEB/html-lib/**/*.*'):
        return True
    if 'modelmodel_sqlite.sql' in file: return True
    if 'versions.json' in file: return True

    return False


def zipdir(path, ziph, content_root, path_filter=accept):
    """
        Add files matching path_filter to zip with path relative to content_root
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            path = os.path.join(root, file)
            if path_filter(os.path.relpath(path, content_root)):
                log(f"Packing {path}")
                ziph.write(path, os.path.relpath(path, content_root))


if __name__ == '__main__':
    main(Path.cwd(), sys.argv[1:])
