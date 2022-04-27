import datetime
import unittest

from LOAD_MODELS.LOAD_INFRA import mergedbs
from SSOT_db.IM_JSON import JSModel, sql2json, jsbusinessrule,jsguid
from SSOT_db.SQL_INFRA import dbConnect
from SSOT_db.IM_OBJECTS import BusinessRule,Attribute,Entity,Table
import SSOT_infra.tests.integration as testsrc

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.testmodelcrm = testsrc.Testmodel(testsrc.CRMTEST)
        self.testmodel1= testsrc.Testmodel(testsrc.TESTMODEL1)
        return

    def test_merge(self):
        dbConnect.openDB(self.testmodelcrm.dbfile,pversioncheck=False )
        self.newbrname='test-BR10'
        self.crmmodel = JSModel(pmodel=sql2json(pdbname=self.testmodelcrm.modelname))
        try:
            buru = BusinessRule(buru_name=self.newbrname,
                                buru_rule= 'nichts',
                                buru_level= 'ATTR',
                                buru_type= 'CHECK',
                                buru_uc='me',
                                buru_dc= datetime.datetime.now(),
                                srcid='9999',
                                srcname='test_mergejs')
            burujs = jsbusinessrule.businessrule2js(buru,plangs=('de','en','fr'))
            attrid=jsguid('ATTR', Attribute.select()[0].attr_id)
            tablid=jsguid('TABL', Table.select()[0].tabl_id)
            burujs['elements'] = {attrid:{"r/w":"R"},
                                  tablid:{"r/w":"R"}
                                  }
            burujs['sourceref']['test_mergejs'][1] = str(datetime.datetime.now())
            self.crmmodel.jsmodel['businessrules']["BURU9999"] = burujs

            mergedbs.mergejson2db(pmodeljson=self.crmmodel)
            """generate json from merged DB"""
            newjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
            newburuid=newjson.jsmodel['attributes'][attrid]['businessrules+'][0]
            self.assertEqual(newburuid,newjson.jsmodel['tables'][tablid]['businessrules+'][0])

            newburu=newjson.getbyid(newburuid)
            self.assertTrue(newburuid in newjson.jsmodel['businessrules'])
            self.assertTrue(attrid in newburu['elements'])
            self.assertTrue(tablid in newburu['elements'])

            self.assertEqual('9999',newburu['sourceref']['test_mergejs'][0])

            #now test an update
            updjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
            updburu = updjson.getelements('businessrules')[newburuid]
            updburu['errormsg']['en']="new error message"
            updburu['um'] = "meandmyself"
            del updburu['elements'][tablid]
            updburu['sourceref']['test_updatemergejs'] = ['9999-111',str(datetime.datetime.now())]
            mergedbs.mergejson2db(pmodeljson=updjson)
            #now check the merge
            newjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
            newburu=newjson.getbyid(newburuid)
            self.assertEqual('9999-111',newburu['sourceref']['test_updatemergejs'][0])
            self.assertEqual(newburu['errormsg']['en'],"new error message")
            self.assertTrue(attrid in newburu['elements'])
            self.assertFalse(tablid in newburu['elements'])
            #self.assertEqual("meandmyself",newburu['um'])
        finally:
            # remove created elements
            BusinessRule.delete(pwhere=("buru_name = ?", self.newbrname))
            dbConnect.myDbConn.close()

        return

    def mergeactorrole(self):
        dbConnect.openDB(self.testmodel1.dbfile, pversioncheck=False)
        try:
            # neuen Eintrag in json mergen in Datenbank
            actrjs = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
            actrjs.jsmodel['actorroles']['ACTR9999'] = \
                jsactorroles.actorrole2js(
                    Actorrole(srcid='99999', srcname='test',
                              actr_id=99999,
                              actr_name='test2', actr_descr='descr2'))

            # colus = actrjs.getelements('COLU')
            # attrs = actrjs.getelements('ATTR')
            actrjs.jsmodel['actorroles']['ACTR9999']["concerns"] = {'ATTR94': 'RC', 'ENTI93': 'IAC'}
        finally:
            dbConnect.closeDB()


if __name__ == '__main__':
    unittest.main()
