
import unittest

import SSOT_infra.tests.integration as testsrc
from LOAD_MODELS.LOAD_ODM.tests.test_fillDB import create_testmodel
from SSOT_db.IM_OBJECTS import Entity,Actorrole,Actorconcern,Attribute,Externalref,DomaingroupMember,ModelelemDocu
from SSOT_db.SQL_INFRA import dbConnect,dbDML
from SSOT_db.IM_OBJECTS.checkdatabase import checkdatabase


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.testmodel1 = testsrc.Testmodel(testsrc.TESTMODEL1)
        self.testcrm = testsrc.Testmodel(testsrc.CRMTEST)
        create_testmodel(self.testmodel1, new=True)
        return

    def test_entity(self):
        dbConnect.openDB(pfilepath=self.testmodel1.dbfile)
        enti = Entity.select(pwhere=('enti_name=?', 'Child Entity1'))
        attrs = enti[0].getinheritedattrids()
        self.assertEqual(1, len(attrs))
        enti = Entity.select(pwhere=('enti_name=?', 'Multi UK Entity'))
        attrs = enti[0].getinheritedattrids()
        self.assertEqual(2, len(attrs))
        enti = Entity.select(pwhere=('enti_name=?', 'role Entity'))
        attrs = enti[0].getinheritedattrids()
        self.assertEqual(2, len(attrs))
        dbConnect.closeDB()
        return

    def test_actorrole(self):
        try:
            dbConnect.openDB(pfilepath=self.testmodel1.dbfile)
            actr = Actorrole(srcid='123123',srcname='test',
                         actr_name='testrole1',actr_descr='what is it')
            actrid = actr.insert()
            attr=Attribute.select()[0]
            Actorconcern(actc_responsible='TRUE',actc_actr_id=actrid,
                         actc_mode_id = attr.attr_id).insert()
            actrs = Actorrole.select(pwhere=("actr_name = ?",'testrole1'))
            self.assertEqual('testrole1',actrs[0].actr_name)
            actcs = actrs[0].getchildren()
            self.assertTrue(attr.attr_id in (act.actc_mode_id for act in actcs))
            self.assertTrue(actrid in (act.actc_actr_id for act in actcs))
            self.assertEqual(actrid,Externalref.getmodeid(psrcname='test',psrcid='123123'))
            self.assertEqual(Attribute , type(actcs[0].getelement()))
            self.assertEqual('R' , actcs[0].getraci())
        finally:
            dbConnect.closeDB()
        return

    def test_descrfunction(self):
        dbConnect.openDB(pfilepath=self.testmodel1.dbfile)
        elem = [(e.getid(),e.__str__(),e.descrstr()) for e in Entity.select()]
        #print (elem[0][1])
        #print (elem[0][2])
        self.assertTrue('enti_name=' in elem[0][1] and 'enti_id=' in elem[0][1])
        self.assertTrue('enti_name=' in elem[0][2] )
        elem = [(e.getid(),e.__str__(),e.descrstr()) for e in Attribute.select()]
        #print (elem[0][2])
        self.assertTrue('attr_tech_name=' in elem[0][1] and 'attr_displ_name=' in elem[0][1] and 'attr_id=' in elem[0][1])
        self.assertTrue(('attr_tech_name=' in elem[0][2] or 'attr_displ_name=' in elem[0][2]) and 'attr_enti_id=' in elem[0][2] and "Entities" in elem[0][2])

        elem = [(e.getid(),e.__str__(),e.descrstr()) for e in DomaingroupMember.select()]
        #print (dgmrs[0][2])
        self.assertTrue(('dgrm_doma_id_group=' in elem[0][2] or 'dgrm_name=' in elem[0][2]))

        elem = [(e.getid(),e.__str__(),e.descrstr()) for e in ModelelemDocu.select()]
        #print (elem[0][2])
        self.assertTrue(('mode_type=' in elem[0][2] or 'docu_name=' in elem[0][2]))

        dbConnect.closeDB()
        return

    def test_consistency(self):
        def createdberrors():
            """creates 4 UK errors (1 ENTI,1 DOMA, 2 ATTR
             and 2 mismatcherrors"""
            sql = """
            update lang_texts
            set lgtx_text='beidefalsch'
            --select * from lang_texts
            where lgtx_attrname=?
            and lgtx_lang_id=(select lang_id from languages
                            where lang_iso_code2=?)
            and lgtx_mode_id in
                (select enti_id from entities
                where enti_name in (?,?))
            """
            dbDML.exec(sql,'ENTI_NAME','fr','Eigentümer','Händler')

            sql = """
            update lang_texts
            set lgtx_text='allefalsch'
            --select * from lang_texts
            where lgtx_attrname=?
            and lgtx_lang_id=(select lang_id from languages
                            where lang_iso_code2=?)
            and lgtx_mode_id in
                (select doma_id from domains
                where doma_name in (?,?,?))
            """
            dbDML.exec(sql,'DOMA_NAME','en','Anzahl','Artikel ID','Beschreibung')

            sql="""
            update lang_texts
            set lgtx_text='allefalsch'
            --select * from lang_texts
            where lgtx_attrname=?
            and lgtx_lang_id=(select lang_id from languages
                            where lang_iso_code2=?)
            and lgtx_mode_id in
                (select attr_id from attributes
                where attr_displ_name in (?,?,?,?))
            """
            dbDML.exec(sql,'ATTR_NAME','fr','Hausnr','Strassenname','Typ','*Zweck')

            sql="""
            update lang_texts
            set lgtx_text=lgtx_text||'xx'
            where lgtx_attrname=?
            and lgtx_lang_id=(select lang_id from languages
                            where lang_is_base_lang = 'TRUE')
            and lgtx_mode_id in
                (select attr_id from attributes
                where attr_displ_name in (?))
            """
            dbDML.exec(sql,'ATTR_COMMENT','Hausnr')

            sql="""
            update lang_texts
            set lgtx_text=lgtx_text||'xx'
            where lgtx_attrname=?
            and lgtx_lang_id=(select lang_id from languages
                            where lang_is_base_lang = 'TRUE')
            and lgtx_mode_id in
                (select buru_id from business_rules
                where buru_name in (?))
            """
            dbDML.exec(sql,'BURU_DESCR','vonbis')


            return

        #self.testcrm.initDB(True)
        with self.assertRaises(Exception) as exp:
            checkdatabase()
        dbConnect.openDB(self.testcrm.dbfile)
        conn = dbConnect.connecttodbcopy()

        errors = checkdatabase()
        self.assertEqual(0,len(errors))
        createdberrors()
        errors = checkdatabase()
        self.assertEqual(6,len(errors))
        print (errors)

        conn.close()
        return

if __name__ == '__main__':
    unittest.main()
