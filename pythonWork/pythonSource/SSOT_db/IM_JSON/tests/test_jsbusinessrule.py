import unittest

from IM_ODM import createJSON
from SSOT_db.IM_OBJECTS import BusinessRule, BusinessruleElement, Attribute, Entity, Languagetext, Relation, Language, \
    Table, Column
from SSOT_db.SQL_INFRA import dbConnect
from SSOT_infra.tests.integration import testmodelcrm
from SSOT_db.IM_JSON import jsbusinessrule


class test_businessrules(unittest.TestCase):
    def setUp(self) -> None:
        self.modelname, self.dbdir, self.dbfilepath = testmodelcrm()
        dbConnect.openDB(self.dbfilepath, pversioncheck=False)
        self.buru = BusinessRule.getbyuk(buru_name='Personenrolle.BESCHREIBUNG_CHECK')
        self.bures = self.buru.getchildren()


    def test_buruinelements(self):
        self.assertEqual([],jsbusinessrule.buruinelements())
        self.assertEqual([],jsbusinessrule.buruinelements(-999))
        elements = jsbusinessrule.buruinelements(self.bures[0].bure_mode_id)
        self.assertEqual(1,len(elements))

    def test_buruelements2js(self):
        self.assertEqual(1, len(jsbusinessrule.buruelements2js()))
        self.assertEqual(1, len(jsbusinessrule.buruelements2js()['xxxx0000']))
        jsbure = jsbusinessrule.buruelements2js([self.bures[0]])
        self.assertEqual('R', jsbure['ATTR'+str(self.bures[0].bure_mode_id)]['r/w'])

    def test_businessrules2js(self):
        brjs=jsbusinessrule.businessrules2js(pemptymodel=True)
        self.assertEqual(1, len(brjs))
        self.assertEqual('',brjs['BURU0000']['uc'])
        brjs = jsbusinessrule.businessrules2js(pemptymodel=False)
        self.assertEqual(len(BusinessRule.select()), len(brjs))

    def tearDown(self) -> None:
        dbConnect.closeDB()
