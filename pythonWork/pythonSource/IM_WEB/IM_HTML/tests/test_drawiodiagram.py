import unittest
from lxml.etree import Element, tostring
from IM_db.IM_JSON import JSModel
from IM_WEB.IM_HTML import drawiodiagram


class MockTranslator:

    def tr(self, value):
        return value


class TestDrawIoDiagramGeneration(unittest.TestCase):
    translator = MockTranslator()

    def setUp(self):
        self.root = Element('root')
        self.test_model = {
            'relations': {
                'RELA1111': self.diagram,
            }
        }

    def test_add_relations_semi(self):
        self.diagram['relationships']['RELA1111']['linesegments'].append(
            {
                "x": 1784,
                "y": 2434,
                "linetype": "SOLID",
                "angle": None,
                "uc": "SNE4FE",
                "dc": "2021-03-10 14:47:16 UTC",
            }
        )
        drawiodiagram.add_relations(self.diagram, JSModel(self.test_model), self.translator, self.root)
        print(tostring(self.root))

    def test_add_relation_single(self):
        #        diag = deepcopy(self.diagram)
        #        del diag['relationships']['RELA1111']['linesegments'][-1]
        drawiodiagram.add_relations(self.diagram, JSModel(self.test_model), self.translator, self.root)
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
