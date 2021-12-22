import glob
import logging
import os.path
import unittest
from pathlib import Path
import json
from lxml import etree
import pytest

from IM_EA.export.xmiexport import XMIBuilder
from IM_db import JSModel

DEFAULT_SSOT = 'testdata/fyyccim-refmodels/CRM/DB/IM_CRM_FYAYC.json'


class EAExportTest(unittest.TestCase):

    def setUp(self) -> None:
        if not os.path.isfile(DEFAULT_SSOT):
            current = Path(os.path.normpath(__file__))
            dirs = list(current.parts)
            print(dirs)
            base = dirs.index('pythonWork')

            path = list(dirs[0:base])
            self.project_base_path = os.path.join(*path)

            path.extend(os.path.split(DEFAULT_SSOT))
            print(f"SSOT path = {'/'.join(path)}")
            self.crm_ssot = os.path.join('/', *path)
        else:
            self.crm_ssot = DEFAULT_SSOT
            self.project_base_path = os.getcwd()

    def test_blank(self):
        empty_model = EmptyModel()
        exporter = XMIBuilder('en')
        tree = exporter.model_to_basic_xmi(empty_model)
        self.assertIsNotNone(tree)  # add assertion here
        print(f"Resulting XMI: {etree.tostring(tree)}")

    @pytest.mark.integration
    def test_crm(self):
        json_model = self.load_model(self.crm_ssot)
        model = JSModel(pmodel=json_model)
        entities = json_model['entities']

        exporter = XMIBuilder('en')
        tree = exporter.model_to_basic_xmi(model)

        destination = 'crm-2.1.xmi'
        et = etree.ElementTree(tree)
        et.write(destination, pretty_print=True)
        print(f"Wrote {os.path.abspath(destination)}")

        classes = tree.xpath('.//packagedElement[@xmi:type = "uml:Class"]', namespaces=tree.nsmap)
        assert len(entities) == len(classes)

    @pytest.mark.integration
    def test_crm_extended(self):
        json_model = self.load_model(self.crm_ssot)
        model = JSModel(pmodel=json_model)
        entities = json_model['entities']

        exporter = XMIBuilder('en')
        tree = exporter.model_to_basic_xmi(model)
        exporter.model_to_ea_extension(model)

        destination = 'crm-2.1-ea.xmi'
        et = etree.ElementTree(tree)
        et.write(destination, pretty_print=True)
        print(f"Wrote {os.path.abspath(destination)}")

        classes = tree.xpath('.//packagedElement[@xmi:type = "uml:Class"]', namespaces=tree.nsmap)
        assert len(entities) == len(classes)

    def find_ssot_in_folder(self, root_folder: str):
        pattern = os.path.abspath(root_folder) + '/testdata/**/*.json'
        sources = list(glob.glob(pattern, recursive=True))
        print(f"Scanning {len(sources)} models from pattern {pattern}")
        for ssot in list(sources):
            # skip _loaded.json duplicates
            if ssot.endswith('_loaded.json'):
                sources.remove(ssot)
                continue
            try:
                with open(ssot, 'r') as src:
                    model = json.load(src)
                if not verify_ssot(model):
                    sources.remove(ssot)
            except Exception as e:
                logging.info(f"{ssot} is not a valid SSOT", e)
                sources.remove(ssot)
        print(f"Working with {sources}")
        return sources

    @pytest.mark.integration
    def test_all_in_folder(self):
        success = True
        errors = []
        models = self.find_ssot_in_folder(self.project_base_path)
        for ssot in list(models):
            print(f"Processing {ssot}")
            try:
                json_model = self.load_model(ssot)
                model = JSModel(pmodel=json_model)

                exporter = XMIBuilder('de')
                tree = exporter.model_to_basic_xmi(model)
                exporter.model_to_ea_extension(model)

                destination = 'test_all_in_folder.xmi'
                et = etree.ElementTree(tree)
                et.write(destination, pretty_print=True)
                print(f"Wrote {os.path.abspath(destination)}")
                models.remove(ssot)
            except Exception as e:
                success = False
                errors.append({'ssot': ssot, 'error': e})
        self.assertTrue(success, f"{len(models)} failed. Errors: {errors}")

    def load_model(self, model_json_file: str):
        self.assertTrue(os.path.isfile(model_json_file), f"JSON source not found {model_json_file}")
        with open(model_json_file, 'r') as src:
            json_model = json.load(src)
        return json_model


class EmptyModel(JSModel):

    def __init__(self):
        super().__init__()
        for key, value in self._elemtype2label.items():
            self.jsmodel[value] = dict()


def verify_ssot(json: dict) -> bool:
    imprint = json.get('_imprint_')
    if imprint is None:
        return False
    model = json.get('model')
    if model is None:
        return False
    model_version = imprint.get('Modelversion')

    if model_version is not None:
        from packaging import version
        v = version.parse(model_version)
        if v < version.parse('1.5.0'):
            return False

    return True


if __name__ == '__main__':
    unittest.main()
