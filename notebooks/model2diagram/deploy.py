#!/usr/bin/python3
import os
from nbconvert import PythonExporter
from traitlets.config import Config
import nbformat as nbf
from nbconvert.preprocessors import TagRemovePreprocessor

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
notebook_to_python(script_file, exporter, target)

print(f"Generated {target} from {script_file}")