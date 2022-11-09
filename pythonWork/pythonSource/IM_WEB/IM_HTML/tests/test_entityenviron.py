import json
import logging
import unittest
from pathlib import Path

import pytest

from IM_WEB.IM_HTML import entityenviron
from SSOT_db.IM_JSON import JSModel
from SSOT_infra.tests.integration import IntegrationTest, RIDDLE, testmodels_dir, ModelHelper,TESTMODEL2


class MockTranslator:

    def tr(self, value):
        if type(value) == dict and len(value) > 0:
            return list(value.values())[0]
        return ''  # fallback

class test_environment (unittest.TestCase):
    def setUp(self) -> None:
        self.tm2 = ModelHelper(TESTMODEL2)

    def test_recursive(self):
        model = JSModel.readfromfile(pfilename=self.tm2.jsonfile)
        nonrecenti,recenti = None,None
        for entiid,enti in model.getelements("entities").items():
            if enti["name"]['de'].startswith("Rekursive"):
                recenti = entiid
            else:
                nonrecenti = entiid
        env = entityenviron.createentienvironment(pentiid=nonrecenti, pjson=model, pmodellang='de')
        self.assertFalse(env.getcell(pvidx=0,phidx='center').getentirecursive())
        if recenti is not None:
            env = entityenviron.createentienvironment(pentiid=recenti, pjson=model, pmodellang='de')
            self.assertTrue(env.getcell(pvidx=0,phidx='center').getentirecursive())
        return

    def test_indirect(self):
        model = JSModel.readfromfile(pfilename=self.tm2.jsonfile)
        master = None
        for entiid,enti in model.getelements("entities").items():
            if enti["name"]['de'].startswith("Master-Entität2"):
                master = entiid
        env = entityenviron.createentienvironment(pentiid=master, pjson=model, pmodellang='de')
        self.assertEqual(env.getcell(pvidx=1,phidx='center').getentiname(),"Kind-Entität3")
        self.assertTrue (env.getcell(pvidx=1,phidx='center').getassocindirect())
        self.assertEqual(env.getcell(pvidx=-1,phidx='center').getentiname(),"Kind Entität1")
        self.assertFalse(env.getcell(pvidx=-1,phidx='center').getassocindirect())
        return


class EnvironDiagramGeneration(IntegrationTest):
    RIDDLEPATH = testmodels_dir() / RIDDLE / 'DB' / (RIDDLE + '.json')

    @pytest.fixture(autouse=True)
    def init(self, tmp_path):
        self.temp_folder = Path(tmp_path)

    def test_entity_environ_riddle(self):
        ssot_file = self.RIDDLEPATH
        self.render(ssot_file)

    def render(self, ssot_file):
        if not ssot_file.exists():
            logging.warning(f"Skipping integration test due to missing resource {ssot_file.resolve()}")
        with open(ssot_file, 'r') as src:
            model = json.load(src)
        self.assertTrue(len(model['diagrams']) > 0)
        js_model = JSModel(pmodel=model)
        lang = list(model['languages'].keys())[0]
        for entity_key in model['entities'].keys():
            env = entityenviron.createentienvironment(pentiid=entity_key, pjson=js_model, pmodellang=lang)
            content = entityenviron.generate_drawio_content(penviron=env)
            with open(self.temp_folder / f"{entity_key}-env.drawio", 'w') as out:
                out.write(content)

