#!/usr/bin/python3
import os
from nbconvert import PythonExporter
from traitlets.config import Config
import nbformat as nbf
import logging
import zipfile


script_file = 'generator.ipynb'


def notebook_to_python(source, exporter, destination):
    with open(source, 'r') as src:
        nb = nbf.read(src, nbf.NO_CONVERT)

    source, meta = exporter.from_notebook_node(nb)
    with open(destination, 'w') as dst:
        dst.write(source)

    return source, meta


c = Config()
c.TagRemovePreprocessor.remove_cell_tags = ("test", "visual")
c.TagRemovePreprocessor.enabled = True

c.PythonExporter.preprocessors = ["nbconvert.preprocessors.TagRemovePreprocessor"]

exporter = PythonExporter(config=c)

filename = os.path.basename(script_file)
noext, _ = os.path.splitext(filename)
target = noext + '.py'

logging.info(f"Converting {script_file} to plain python")
notebook_to_python(script_file, exporter, target)
logging.info(f"Generated {target} from {script_file}")




def zipdir(path, ziph, content_root):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            path = os.path.join(root, file)
            ziph.write(path, os.path.relpath(path, content_root))


package_name = 'model2diagram'

archive = os.path.join('.', package_name + '.zip')

with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as zipfile:
    zipfile.write('generator.py')
    zipfile.write('run.bat')
    zipdir('tools', zipfile, '.')

logging.info(f"Compiled archive {archive}")

