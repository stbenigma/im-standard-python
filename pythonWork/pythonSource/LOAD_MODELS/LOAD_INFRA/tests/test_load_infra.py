import re
import unittest


class Load_Infra(unittest.TestCase):
    def test_lang_notes(self):
        from LOAD_MODELS.LOAD_INFRA import handleXML
        t1 = """irgendetwas[DE_ENTI_COMMENT[text
]DE_ENTI_COMMENT]
[EN_ENTI_COMMENT[
]EN_ENTI_COMMENT] dann folgen ]]"""
        t1ok= {'de': {'DE_ENTI_COMMENT': 'text'},
               'en': {'EN_ENTI_COMMENT':''}
               }
        self.assertEqual(t1ok,handleXML.extractlngcomments(ptext=t1))

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
        #no german, but gernam ending within english text
        t1ok = {'en': {'EN_ENTI_COMMENT': 'texte]DE_ENTI_COMMENT'}
                }
        self.assertEqual(t1ok, handleXML.extractlngcomments(ptext=t1))
        return


if __name__ == '__main__':
    unittest.main()
