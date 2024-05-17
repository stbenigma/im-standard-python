import glob
import logging
import os.path
import unittest
import json

import pytest
from lxml import etree

from LOAD_MODELS.LOAD_EA.export.xmiexport import XMIBuilder
from SSOT_db.IM_JSON import JSModel
from SSOT_infra.tests.integration import IntegrationTest, RIDDLE, path_to_testmodels

MODEL_REPOSITORY = 'testdata/fyyccim-refmodels'


class EAExportTest(unittest.TestCase):

    def test_blank(self):
        empty_model = EmptyModel()
        exporter = XMIBuilder(empty_model, 'en')
        tree = exporter.model_to_basic_xmi()
        self.assertIsNotNone(tree)  # add assertion here
        print(f"Resulting XMI: {etree.tostring(tree)}")


class IntegrationTestXMIExport(IntegrationTest):

    def setUp(self) -> None:
        super().setUp()

    @pytest.mark.integration
    def test_crm_xmi(self):
        json_model, model = self.load_crm_model()
        if json_model is None: return #no referencetestmodel found
        entities = json_model['entities']

        exporter = XMIBuilder(model, 'en')
        tree = exporter.model_to_basic_xmi()

        destination = self.base_path / 'crm-basic-2.1.xmi'
        et = etree.ElementTree(tree)
        et.write(str(destination), pretty_print=True)
        print(f"Wrote {destination.resolve()}")

        classes = tree.xpath('.//packagedElement[@xmi:type = "uml:Class"]',
                             namespaces=tree.nsmap)
        assert len(entities) == len(classes)

    def test_riddle_xmi(self):
        json_model, model = self.load_riddle_model()
        entities = json_model['entities']

        exporter = XMIBuilder(model, 'en')
        tree = exporter.model_to_basic_xmi()
        exporter.model_to_ea_extension()

        destination = self.base_path / f'{RIDDLE}.xmi'
        et = etree.ElementTree(tree)
        et.write(str(destination), pretty_print=True)
        print(f"Wrote {destination.resolve()}")

        classes = tree.xpath('.//packagedElement[@xmi:type = "uml:Class"]',
                             namespaces=tree.nsmap)
        assert len(entities) == len(classes)

    @pytest.mark.integration
    def test_crm_extended(self):
        json_model, model = self.load_crm_model()
        if json_model is None: return #no referencetestmodel found
        entities = json_model['entities']

        exporter = XMIBuilder(model, 'en')
        tree = exporter.model_to_basic_xmi()
        exporter.model_to_ea_extension()

        destination = self.base_path / 'crm.xmi'
        et = etree.ElementTree(tree)
        et.write(str(destination), pretty_print=True)
        print(f"Wrote {destination.resolve()}")

        classes = tree.xpath('.//packagedElement[@xmi:type = "uml:Class"]',
                             namespaces=tree.nsmap)
        assert len(entities) == len(classes)

    def load_crm_model(self) -> (json, JSModel):
        refmodeldir = self.project_root / MODEL_REPOSITORY

        if not refmodeldir.exists():
            logging.warning(f"Skipping integration test due to missing resource {refmodeldir.resolve()}")
            return None,None
        if not os.path.isfile(refmodeldir / 'CRM/DB/IM_CRM_FYAYC.json'):
            logging.warning(f"Skipping integration test due to missing jsonf file {refmodeldir / 'CRM/DB/IM_CRM_FYAYC.json'}")
            return None,None
        json_model = self.load_model(refmodeldir / 'CRM/DB/IM_CRM_FYAYC.json')
        model = JSModel(pmodel=json_model)
        return json_model, model

    def load_riddle_model(self) -> (json, JSModel):
        json_model = self.load_model(path_to_testmodels() / RIDDLE / 'DB' / (RIDDLE + '.json'))
        model = JSModel(pmodel=json_model)
        return json_model, model

    def load_raetsel3lang_model(self) -> (json, JSModel):
        json_model = self.load_model(self.project_root / MODEL_REPOSITORY /
                                     'raetsel3lang/DB/raetsel3lang.json')
        model = JSModel(pmodel=json_model)
        return json_model, model

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
        print(f"Working with:\n{(',' + os.linesep).join(sources)}")
        return sources

    @pytest.mark.integration
    @pytest.mark.nocoverage
    def test_zzz_finally_process_all_models_found_in_testdata_folder(self):
        success = True
        errors = []
        models = self.find_ssot_in_folder(self.project_root)
        for ssot in list(models):
            try:
                json_model = self.load_model(ssot)
                model = JSModel(pmodel=json_model)
                name = json_model['model']['name']
                print(f"Processing '{name}' {ssot}")
                exporter = XMIBuilder(model, 'de')
                tree = exporter.model_to_basic_xmi()
                exporter.model_to_ea_extension()

                destination = self.base_path / (name + '.xmi')
                et = etree.ElementTree(tree)
                et.write(str(destination), pretty_print=True)
                print(f"Wrote {destination.resolve()}")
                models.remove(ssot)
            except Exception as e:
                success = False
                logging.error(f"Model {ssot} failed", exc_info=e)
                errors.append({'ssot': ssot, 'error': e})
        self.assertTrue(success, f"{len(models)} failed. Errors: {errors}")

    def load_model(self, model_json_file):
        self.assertTrue(os.path.isfile(model_json_file),
                        f"JSON source not found {model_json_file}")
        json_model = None
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
