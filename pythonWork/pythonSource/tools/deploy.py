#!/usr/bin/python3
import os
import re

from nbconvert import PythonExporter
from traitlets.config import Config
import nbformat as nbf
import logging
import zipfile


strip_cells_with_tags = ("test", "visual", "debug")

script_file = 'notebooks/mig/generator.ipynb'


def notebook_to_python(source, exporter, destination):
    with open(source, 'r') as src:
        nb = nbf.read(src, nbf.NO_CONVERT)

    source, meta = exporter.from_notebook_node(nb)
    with open(destination, 'w') as dst:
        dst.write(source)
    print(f"Wrote {os.path.abspath(destination)}. Removed cells with tags {strip_cells_with_tags}")
    return source, meta


c = Config()
c.TagRemovePreprocessor.remove_cell_tags = strip_cells_with_tags
c.TagRemovePreprocessor.enabled = True

c.PythonExporter.preprocessors = ["nbconvert.preprocessors.TagRemovePreprocessor"]

exporter = PythonExporter(config=c)

filename = os.path.basename(script_file)
noext, _ = os.path.splitext(filename)
target = noext + '.py'

logging.info(f"Converting {script_file} to plain python")
notebook_to_python(script_file, exporter, target)
logging.info(f"Generated {target} from {script_file}")


def accept(path: str):
    file = os.path.basename(path)
    if '/venv/' in path: return False
    if file is None: return False
    if file.endswith('.py'): return True
    if 'modelmodel_sqlite.sql' in file: return True
    if 'versions.json' in file: return True
    return False

def zipdir(path, ziph, content_root):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            path = os.path.join(root, file)
            if accept(path):
                ziph.write(path, os.path.relpath(path, content_root))

from subprocess import check_output, CalledProcessError
git_tag = 'dev'

try:
    git_tag = check_output(['git', 'describe', '--always']).decode().strip()
except CalledProcessError as e:
    logging.warning(f"Cannot read git status")

version = 'master'

with open(target, 'r') as src:
    expression = re.compile(r'notebook_version\s*=\s*"([^"]+)"')
    for line in src.readlines():
        match = expression.match(line)
        if match:
            version = match.group(1)

package_name = f'model2diagram-{version}'
archive = os.path.join('.', package_name + '.zip')

from datetime import datetime
now = datetime.now()
stamp = now.strftime("%Y-%m-%d %H:%M:%S")

version_file_name = 'version.json'
with open(version_file_name, 'w') as vfile:
    vfile.write(f'{{ "version": "{version}", "git": "{git_tag}", timestamp: "{stamp}" }}\n')

with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as zipfile:
    zipfile.write(target)
    zipfile.write(version_file_name)
    zipfile.write('run.bat')
    zipdir('pythonWork', zipfile, '.')

logging.info(f"Compiled archive {archive}")

