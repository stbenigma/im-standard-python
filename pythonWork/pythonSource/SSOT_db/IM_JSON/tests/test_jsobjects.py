import unittest

from SSOT_db.IM_OBJECTS import BusinessRule,Actorrole,Actorconcern,Attribute,Boolean
from SSOT_db.SQL_INFRA import dbConnect
import SSOT_infra.tests.integration as testsrc
from SSOT_db.IM_JSON import jsbusinessrule,jsactorroles,JSModel,sql2json


class test_jsobjects(unittest.TestCase):
    def setUp(self) -> None:
        self.testmodelcrm= testsrc.Testmodel(testsrc.CRMTEST)
        self.testmodel1= testsrc.Testmodel(testsrc.TESTMODEL1)

    def test_businessrules(self):
        try:
            dbConnect.openDB(self.testmodelcrm.dbfile, pversioncheck=False)
            self.buru = BusinessRule.getbyuk(buru_name='Personenrolle.BESCHREIBUNG_CHECK')
            self.bures = self.buru.getchildren()

            self.assertEqual([],jsbusinessrule.buruinelements())
            self.assertEqual([],jsbusinessrule.buruinelements(-999))
            elements = jsbusinessrule.buruinelements(self.bures[0].bure_mode_id)
            self.assertEqual(1,len(elements))
            self.assertEqual(1, len(jsbusinessrule.buruelements2js()))
            self.assertEqual(1, len(jsbusinessrule.buruelements2js()['xxxx0000']))
            jsbure = jsbusinessrule.buruelements2js([self.bures[0]])
            self.assertEqual('R', jsbure['ATTR'+str(self.bures[0].bure_mode_id)]['r/w'])
            brjs=jsbusinessrule.businessrules2js(pemptymodel=True)
            self.assertEqual(1, len(brjs))
            self.assertEqual('',brjs['BURU0000']['uc'])
            brjs = jsbusinessrule.businessrules2js(pemptymodel=False)
            self.assertEqual(len(BusinessRule.select()), len(brjs))
        finally:
            dbConnect.closeDB()

    def test_actorroles(self):
        def filltestdatatodb():
            self.actrid=Actorrole(srcid='123123',srcname='test',
                      actr_name='test1',actr_descr='descr1').insert()
            attrs=Attribute.select()
            Actorconcern(actc_actr_id=self.actrid,actc_mode_id=attrs[0].attr_id,
                         actc_responsible='TRUE').insert()
            Actorconcern(actc_actr_id=self.actrid,actc_mode_id=attrs[1].attr_id,
                         actc_informed='TRUE',actc_consulted='TRUE').insert()
            return

        try:
            dbConnect.openDB(self.testmodel1.dbfile, pversioncheck=False)

            # js2actc
            actc = jsactorroles.js2actc(pactrid=0, pmodeid=1, praci='R')
            self.assertTrue(Boolean.str2bool(actc.actc_responsible))
            self.assertFalse(Boolean.str2bool(actc.actc_accountable))
            self.assertFalse(Boolean.str2bool(actc.actc_consulted))
            self.assertFalse(Boolean.str2bool(actc.actc_informed))
            self.assertEqual(1, actc.actc_mode_id)
            self.assertEqual(0, actc.actc_actr_id)
            actc = jsactorroles.js2actc(pactrid=3, pmodeid=2, praci='IA')
            self.assertFalse(Boolean.str2bool(actc.actc_responsible))
            self.assertTrue(Boolean.str2bool(actc.actc_accountable))
            self.assertFalse(Boolean.str2bool(actc.actc_consulted))
            self.assertTrue(Boolean.str2bool(actc.actc_informed))
            self.assertEqual(2, actc.actc_mode_id)
            self.assertEqual(3, actc.actc_actr_id)

            emptyactr = jsactorroles.actorroles2js(pemptymodel=True)
            self.assertEqual('',emptyactr['ACTR0000']['name'])
            self.assertEqual('RACI',emptyactr['ACTR0000']['concerns']['xxxx0000'])
            actr = jsactorroles.js2actr(pkey='ACTR0000', pelem=emptyactr['ACTR0000'])
            self.assertEqual(0,actr.actr_id)


            #actors from ODM
            dbactrs = jsactorroles.actorroles2js(pemptymodel=False)
            filltestdatatodb()
            actrs = jsactorroles.actorroles2js(pemptymodel=False)
            self.assertEqual(len(dbactrs)+1,len(actrs))
            for k,v in actrs.items():
                if v['name']=='test1':
                    actrid=k
            newjson = JSModel(pmodel=sql2json(pdbname=self.testmodel1.modelname))

            concerned = list(actrs[actrid]["concerns"].keys())
            mode1 = newjson.getbyid(concerned[0])
            mode2 = newjson.getbyid(concerned[1])
            self.assertEqual('R',mode1['raci+'][actrid])
            self.assertEqual('CI',mode2['raci+'][actrid])

        finally:
            Actorrole.delete(pwhere="actr_name like 'test_'")
            dbConnect.closeDB()
