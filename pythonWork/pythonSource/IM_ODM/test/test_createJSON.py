import json
import os
import tempfile
import unittest

from IM_ODM import createJSON
from SSOT_db.IM_OBJECTS import BusinessRule, BusinessruleElement,Attribute,Entity,Languagetext
from SSOT_db.SQL_INFRA import dbConnect
from SSOT_infra.tests.integration import testmodelcrm


class MyTestCase(unittest.TestCase):
    def test_createemptyjson(self):
        filename = "empty_json.json"
        with tempfile.TemporaryDirectory() as tmpdirname:
            createJSON.createemptyJSON(pfilepath=tmpdirname, pfilename=filename)
            fullpath = os.path.join(tmpdirname, filename)
            self.assertTrue(os.path.exists(fullpath))
            jsfile = open(fullpath)
            js = json.load(jsfile)
            self.assertTrue('entities' in js)
            self.assertTrue('businessrules' in js)
        return

    def fillextrabusinessrules(self, pfilepath):
        dbConnect.openDB(pfilepath=pfilepath, pfks='1', pversioncheck=False)
        BusinessRule.delete(pwhere=("buru_name like ?","test_BR%"))
        buru = BusinessRule(buru_name="test-BR1", buru_type=BusinessRule.BURU_TYPE_CHECK,
                            buru_level=BusinessRule.BURU_LEVEL_TUPL, buru_impact='REFUSE',
                            buru_rule="a > b oder c",
                            buru_descr="Rule on 3 Attributes, 2 checked, 1 referenced")
        buruid = buru.insert()
        Languagetext.fillnontranslatedtexts(['BURU'])
        enti = Entity.getbyuk(enti_name="natürliche Person")
        attrs=Attribute.select(pwhere=("attr_enti_id = ?",
                                       enti.enti_id))

        BusinessruleElement(bure_buru_id=buruid,
                                   bure_mode_id=attrs[0].attr_id
                                   ).insert()
        BusinessruleElement(bure_buru_id=buruid,
                                   bure_mode_id=attrs[1].attr_id
                                   ).insert()
        BusinessruleElement(bure_buru_id=buruid,
                                   bure_mode_id=attrs[2].attr_id
                                   ).insert()
        BusinessruleElement(bure_buru_id=buruid,
                                   bure_mode_id=enti.enti_id
                                   ).insert()
        dbConnect.closeDB()
        return

    def test_createJSON(self):
        modelname, modeldir, modeldb = testmodelcrm()
        self.fillextrabusinessrules(pfilepath=modeldb)
        dbConnect.openDB(pfilepath=modeldb, pfks='1', pversioncheck=False)
        buru = BusinessRule.select()
        buruid=BusinessRule.getbyuk(buru_name="test-BR1").getid()
        bures = BusinessruleElement.select(pwhere=("bure_buru_id = ?",buruid))
        buruid="BURU"+str(buruid)
        dbConnect.closeDB()
        with tempfile.TemporaryDirectory() as tmpdirname:
            createJSON.createJSON(pdbfilepath=modeldb, pmodelname=modelname,
                                  pjsfilepath=tmpdirname, pjsfilename=modelname)
            fullpath = os.path.join(tmpdirname, modelname + '.json')
            self.assertTrue(os.path.exists(fullpath))
            jsfile = open(fullpath)
            js = json.load(jsfile)
            self.assertTrue('entities' in js)
            self.assertEqual(len(buru),len(js['businessrules']))
            elems= js['businessrules'][buruid]['elements']
            self.assertEqual(len(bures),len(elems))

        return


if __name__ == '__main__':
    unittest.main()
