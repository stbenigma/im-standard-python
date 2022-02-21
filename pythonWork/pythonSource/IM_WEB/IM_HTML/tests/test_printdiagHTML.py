import unittest

from IM_WEB.IM_HTML.printHTML import HTMLExport
from IM_WEB.IM_HTML.printdiagHTML import printelements
from SSOT_db.IM_JSON import JSModel


class MockTranslator:

    def tr(self, value):
        return value


class TestPrintDiagHTML(unittest.TestCase):
    translator = MockTranslator()

    def setUp(self):
        self.test_model = JSModel()

    def test_smoke(self):
        config = HTMLExport()
        config.model = JSModel({'entities': {'ENTI0001': {'subtypellevel+': 0}}})
        diagram = {'name': 'dummy',
                   'elements': {
                       'entity': [],
                       'attribute': [],
                   },
                   'relationships': {},
                   'arcs': {},
                   }
        printelements(config, diagram, 'DIAG001', 'de')

    def test_add_relation_single(self):
        #        diag = deepcopy(self.diagram)
        #        del diag['relationships']['RELA1111']['linesegments'][-1]
        # add_relations(self.diagram, JSModel(self.test_model), self.translator, self.root)
        # print(tostring(self.root))
        pass

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

    segements = [
        {
            "x": 13382,
            "y": 6535,
            "linetype": "DASHED",
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
            "linetype": "SOLID",
            "angle": None,
            "uc": "SNE4FE",
            "dc": "2020-11-16 07:03:01 UTC",
            "um": None,
            "dm": None
        }
    ]

    def test_add_relations_semi(self):
        self.diagram['relationships']['RELA1111']['linesegments'] = self.segements
        self.assertTrue(self.diagram is not None)
        # drawiodiagram.add_relations(self.diagram, JSModel(self.test_model), self.translator, self.root)
        # print(tostring(self.root))
