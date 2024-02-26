import unittest
from pathlib import Path

import pytest

import SSOT_infra.tests.integration as testsrc
from SSOT_db.IM_JSON import JSModel
from LOAD_MODELS.LOAD_INFRA import mergedbs


class Load_Infra(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temp_folder = Path(tmp_path)
        self.testmodel1 = testsrc.ModelHelper(testsrc.TESTMODEL1)

    def test_lang_notes(self):
        from LOAD_MODELS.LOAD_INFRA import handleXML
        t1 = """irgendetwas[DE_ENTI_COMMENT[text
]DE_ENTI_COMMENT]
[EN_ENTI_COMMENT[
]EN_ENTI_COMMENT] dann folgen ]]"""
        t1ok = {'de': {'DE_ENTI_COMMENT': 'text'},
                'en': {'EN_ENTI_COMMENT': ''}
                }
        self.assertEqual(t1ok, handleXML.extractlngcomments(ptext=t1))

        t1 = """[DE_ENTI_COMMENT[text]DE_ENTI_COMMENT][EN_ENTI_COMMENT[]EN_ENTI_COMMENT]"""
        t1ok = {'de': {'DE_ENTI_COMMENT': 'text'},
                'en': {'EN_ENTI_COMMENT': ''}
                }
        self.assertEqual(t1ok, handleXML.extractlngcomments(ptext=t1))

        t1 = """[DE_ENTI_COMMENT[text
multilang
3. Zeile]DE_ENTI_COMMENT][EN_ENTI_COMMENT[english]EN_ENTI_COMMENT]"""
        t1ok = {'en': {'EN_ENTI_COMMENT': 'english'},
                'de': {'DE_ENTI_COMMENT': 'text\nmultilang\n3. Zeile'}
                }
        self.assertEqual(t1ok, handleXML.extractlngcomments(ptext=t1))

        t1 = """[DE_ENTI_COMMENT[text
multilang
3. Zeile]DE_ENTI_COMMENT][EN_ENTI_COMMENT[english]EN_ENTI_COMMENT]"""
        t1ok = {'de': {'DE_ENTI_COMMENT': 'text\nmultilang\n3. Zeile'},
                'en': {'EN_ENTI_COMMENT': 'english'}
                }
        self.assertEqual(t1ok, handleXML.extractlngcomments(ptext=t1))

        t1 = """[EN_ENTI_COMMENT[text
        multil]ang
        3. Zeile]EN_ENTI_COMMENT][DE_ENTI_COMMENT[

]DE_ENTI_COMMENT]"""
        t1ok = {'de': {'DE_ENTI_COMMENT': ''},
                'en': {'EN_ENTI_COMMENT': 'text\n        multil]ang\n        3. Zeile'}
                }
        self.assertEqual(t1ok, handleXML.extractlngcomments(ptext=t1))

        t1 = """[EN_ENTI_COMMENT[texte]DE_ENTI_COMMENT]EN_ENTI_COMMENT]"""
        # no german, but gernam ending within english text
        t1ok = {'en': {'EN_ENTI_COMMENT': 'texte]DE_ENTI_COMMENT'}
                }
        self.assertEqual(t1ok, handleXML.extractlngcomments(ptext=t1))
        return

    def test_mergejson(self):
        tm1 = JSModel.readfromfile(self.testmodel1.jsonfile)
        tm1.jsmodel["entities"]["12345678"] = {'name': {'en': 'NEW ENTITY'}, 'shortname': None, 'descr': {
            'en': 'Child entity'}, 'tooltip': {'en': ''},
                                               'category': None, 'exptuple#': None, 'prefix': None,
                                               'supertypeentity': None, 'uc': 'stb',
                                               'dc': '2021-10-05 08:37:45 UTC', 'um': None,
                                               'dm': None, 'minzoomlevel': 0, 'maxzoomlevel': 4,
                                               'publstatus': 'GTOP', 'icon': {'type': None, 'reference': None},
                                               'synonyms': [], 'examples': [], 'sourceref': {
                'TEST': ['12345678', '2023-06-23 17:02:38.593901']},
                                               'referencedby': [], 'userdefprops': {}
                                               }
        diagid=list(tm1.jsmodel["diagrams"].keys())[0]
        tm1.jsmodel["diagrams"][diagid]["elements"]["entity"].append(
            {'element': '12345678', 'index': 0, 'pos_x': 150, 'pos_y': 420, 'uc': None, 'dc': None,
             'um': None, 'dm': None,
             'ui': {'width': 170, 'height': 110, 'opacity': 100, 'color': 'ff89ec', 'marginwidth': 1,
                    'marginopacity': 100, 'margincolor': '0000ff', 'fontsize': 10, 'fontcolor': '0000ff'}}
        )
        arcid=list(tm1.jsmodel["arcs"].keys())[0]
        tm1.jsmodel["relations"][9876543]=\
        {'name': 'Neurelation mit neu ID', 'type': 'ISAS',
         'from-to': {'enti': '12345678', 'arc': None, 'assoc': {'en': 'neu Von'}, 'maptype': '1', 'hist': False,
                     'mandatory': True, 'cardstr+': '1'},
         'to-from': {'enti': 'ENTI42', 'arc': arcid, 'assoc': {'en': 'neu Zu'}, 'maptype': '1', 'hist': False,
                     'mandatory': True, 'cardstr+': '1'}, 'isinkeys+': [],
         'sourceref': {}, 'uc': None, 'dc': None,
         'um': None, 'dm': None, 'minzoomlevel': None, 'maxzoomlevel': None, 'publstatus': None,
         'userdefprops': {}, 'referencedby': []}

        self.assertTrue(mergedbs.checkjsonmodel(pmodel=tm1,pverbose=True))
        mergedbs.mergejs2db(pdbfile=self.testmodel1.dbfile,pmodel=tm1,psrcname="TEST",pverbose=True,pkeepids=True)
        return


if __name__ == '__main__':
    unittest.main()
