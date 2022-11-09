import json
import logging
import unittest
from pathlib import Path

import pytest
from lxml.etree import Element, tostring

from IM_WEB.IM_HTML.drawiodiagram import create_diagram
from SSOT_db.IM_JSON import JSModel
from IM_WEB.IM_HTML import drawiodiagram

from SSOT_infra.tests.integration import IntegrationTest,RIDDLE,testmodels_dir
from SSOT_infra.tests.test_translateprompt import update_gettext_ressources


class MockTranslator:

    @classmethod
    def tr(cls, value):
        if type(value) == dict and len(value) > 0:
            return list(value.values())[0]
        return ''  # fallback


class TestDrawIoDiagramGeneration(unittest.TestCase):
    translator = MockTranslator()

    def setUp(self):
        self.root = Element('root')
        self.test_model = {
            'relations': {
                'RELA1111': self.diagram,
            }
        }
        update_gettext_ressources()

    def test_add_relations_semi(self):
        segment = {
            "x": 1784,
            "y": 2434,
            "linetype": "SOLID",
            "angle": None,
            "uc": "SNE4FE",
            "dc": "2021-03-10 14:47:16 UTC",
        }
        # noinspection PyTypeChecker
        self.diagram['relationships']['RELA1111']['linesegments'].append(segment)
        drawiodiagram.add_relations(self.diagram,
                                    JSModel(self.test_model,
                                            pwithversioncheck=False), self.translator, self.root)
        print(tostring(self.root))

    def test_add_relation_single(self):
        drawiodiagram.add_relations(self.diagram,
                                    JSModel(self.test_model,
                                            pwithversioncheck=False), self.translator, self.root)
        print(tostring(self.root))

    diagram = {
        'from-to': {
            'mandatory': False,
            'assoc': {'de': None, 'en': None},
        },
        'to-from': {
            'mandatory': True,
            'assoc': {'de': 'zurück', 'en': 'back'},
        },
        'relationships': {
            'RELA1111': {
                "start_connector": "M",
                "end_connector": "1",
                "linesegments": [
                    {
                        "x": 1481,
                        "y": 2434,
                        "linetype": "DASHED",
                        "angle": 0,
                        "uc": "SNE4FE",
                        "dc": "2021-03-10 14:47:16 UTC",
                    },
                    {
                        "x": 1632,
                        "y": 2434,
                        "linetype": "DASHED",
                        "angle": 0,
                        "uc": "SNE4FE",
                        "dc": "2021-03-10 14:47:16 UTC",
                    },
                ]
            }
        }
    }

    segments = [
        {
            "x": 13382,
            "y": 6535,
            "linetype": "SOLID",
            "angle": 3.141592653589793,
            "uc": "SNE4FE",
            "dc": "2020-11-16 07:03:01 UTC",
            "um": None,
            "dm": None
        },
        {
            "x": 13169,
            "y": 6535,
            "linetype": "SOLID",
            "angle": 3.141592653589793,
            "uc": "SNE4FE",
            "dc": "2020-11-16 07:03:01 UTC",
            "um": None,
            "dm": None
        },
        {
            "x": 12956,
            "y": 6535,
            "linetype": "DASHED",
            "angle": None,
            "uc": "SNE4FE",
            "dc": "2020-11-16 07:03:01 UTC",
            "um": None,
            "dm": None
        }
    ]

    def test_relation_dashed_undashed(self):
        # noinspection PyTypedDict
        self.diagram['relationships']['RELA1111']['linesegments'] = self.segments
        drawiodiagram.add_relations(self.diagram, JSModel(self.test_model
                                                          ,pwithversioncheck=False), self.translator, self.root)
        print(tostring(self.root))


class IntegrationTestDrawIoDiagramGeneration(IntegrationTest):

    @pytest.fixture(autouse=True)
    def init(self, tmp_path):
        self.temp_folder = Path(tmp_path)

    def setUp(self) -> None:
        super().setUp()
        update_gettext_ressources()

    def test_riddle_xmi(self):
        ssot_file = testmodels_dir() / RIDDLE / 'DB' / (RIDDLE + '.json')
        if not ssot_file.exists():
            logging.warning(f"Skipping integration test due to missing resource {ssot_file.resolve()}")
        with open(ssot_file, 'r') as src:
            model = json.load(src)
        self.assertTrue(len(model['diagrams']) > 0)
        js_model = JSModel(pmodel=model,pwithversioncheck=False)
        for diagram_key in model['diagrams'].keys():
            xml = create_diagram(diagram_key, js_model, MockTranslator())
            self.assertTrue(len(list(xml.iter())) > 0)
            outfile = self.temp_folder / f"{RIDDLE}-{diagram_key}.drawio"
            xml.write(str(outfile), pretty_print=True)
            print(f"Wrote diagram {diagram_key} to {outfile}")

    @pytest.mark.integration
    def test_CRM_xmi(self):
        ssot_file = self.project_root / 'testdata' / 'fyyccim-refmodels' / 'CRM' / 'DB' / 'IM_CRM_FYAYC.json'
        if not ssot_file.exists():
            logging.warning(f"Skipping integration test due to missing resource {ssot_file.resolve()}")
            return
        with open(ssot_file, 'r') as src:
            model = json.load(src)
        self.assertTrue(len(model['diagrams']) > 0)

        for diagram_key in model['diagrams'].keys():
            js_model = JSModel(pmodel=model,pwithversioncheck=False)
            xml = create_diagram(diagram_key, js_model, MockTranslator())
            self.assertTrue(len(list(xml.iter())) > 0)
