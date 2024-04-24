
import unittest

import SSOT_infra.tests.integration as testsrc
from LOAD_MODELS.LOAD_ODM.tests.test_fillDB import create_testmodel
from SSOT_db.IM_OBJECTS import *
from SSOT_db.SQL_INFRA import dbConnect,dbDML
from SSOT_db.IM_OBJECTS.checkdatabase import checkdatabase


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.testmodel1 = testsrc.ModelHelper(testsrc.TESTMODEL1)
        self.testcrm = testsrc.ModelHelper(testsrc.CRMTEST)
        create_testmodel(self.testmodel1, new=True)
        create_testmodel(self.testcrm, new=True)
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

    def test_subentity(self):
        dbConnect.openDB(pfilepath=self.testcrm.dbfile)
        enti = Entity.select(pwhere=('enti_name=?', 'Geografische Einheit'))
        subentis = enti[0].getsubentities()
        self.assertEqual('Gebiet',subentis[0][3])
        self.assertEqual('Land',subentis[1][3])
        self.assertEqual('Ländergruppe',subentis[2][3])
        self.assertEqual('PLZ-Gebiet',subentis[3][3])
        self.assertEqual('Administrativgebiet',subentis[4][3])
        subids=enti[0].getsubentityids()
        for se in subentis:
            self.assertIn(se[2],subids)
        dbConnect.closeDB()

    def test_actorrole(self):
        try:
            dbConnect.openDB(pfilepath=self.testmodel1.dbfile)
            actr = Actorrole(srcid='123123',srcname='tests',
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
            self.assertEqual(actrid,Externalref.getmodeid(psrcname='tests',psrcid='123123'))
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

    def test_failing_inserts(self):
        dbConnect.openDB(pfilepath=self.testmodel1.dbfile)
        modes = Modelelement.select(pwhere="mode_type = 'DOCU' and mode_id not in (select docu_id from documents)")
        self.assertEqual(0, len(modes))
        docu = Document(docu_name='dummytest',docu_docu_id=99999)
        with self.assertRaises(Exception):
            docu.insert() #should fail but leaving no tangling modelelement behind
        modes = Modelelement.select(pwhere="mode_type = 'DOCU' and mode_id not in (select docu_id from documents)")
        self.assertEqual(0, len(modes))



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

    def test_checksupertentimap(self):
        dbConnect.openDB(self.testcrm.dbfile)
        conn = dbConnect.connecttodbcopy()
        checks = ColAttrMap.checksuperentitymap()
        self.assertEqual(0,len(checks))
        enti = Entity.getbyuk(enti_name = 'Geografische Einheit')
        entiwrong = Entity.getbyuk(enti_name = 'Haushalt')
        subentiids = enti.getsubentityids()
        for se in subentiids:
            iha = Entity().getbyid(se).getinheritedattrids()
            attridlist = ",".join ([str(i) for i in iha])
            attrs = Attribute.select(pwhere=(f"attr_id in ({attridlist})"))

            if  len(iha)>0:
                cnt = dbDML.exec(f"update colu_attr_map set coam_enti_id =? where coam_attr_id in ({attridlist})",
                                 entiwrong.enti_id)
                self.assertTrue(0<cnt)
                checks = ColAttrMap.checksuperentitymap()
                self.assertTrue(0<len(checks))
                cnt = dbDML.exec(f"update colu_attr_map set coam_enti_id =? where coam_attr_id in ({attridlist})",
                                 Entity.getbyuk(enti_name = 'Gebiet').enti_id)
                checks = ColAttrMap.checksuperentitymap()
                self.assertTrue(0==len(checks))
                cnt = dbDML.exec(f"update colu_attr_map set coam_enti_id =? where coam_attr_id in ({attridlist})",
                                 Entity.getbyuk(enti_name = 'PLZ-Gebiet').enti_id)
                checks = ColAttrMap.checksuperentitymap()
                self.assertTrue(0==len(checks))
                cnt = dbDML.exec(f"update colu_attr_map set coam_enti_id = NULL where coam_attr_id in ({attridlist})")
                checks = ColAttrMap.checksuperentitymap()
                self.assertTrue(0==len(checks))
                break

        conn.close()

    def test_mappings(self):
        dbConnect.openDB(self.testcrm.dbfile)
        conn = dbConnect.connecttodbcopy()
        ColAttrMap.createinheritedmaps()
        for coam in ColAttrMap.select(pwhere="coam_enti_id is not null"):
            attr = Attribute().getbyid(coam.coam_attr_id)
            print (coam.coam_colu_id,Column().getbyid(coam.coam_colu_id).getname(),
                   coam.coam_attr_id,Entity().getbyid(attr.attr_enti_id).getname(),
                   coam.coam_attr_id,attr.getname(),
                   coam.coam_enti_id,Entity().getbyid(coam.coam_enti_id).getname())

        #check that subtype column mappings are correctly delivered
        coaml=[ [coam.coam_attr_id,coam.coam_colu_id,Attribute().getbyid(coam.coam_attr_id).attr_enti_id,coam.coam_enti_id,coam.secondentiids()] for coam in ColAttrMap.select()]#pwhere="coam_enti_id is not null")]

        conn.close()
        return
    def test_new_modetypes(self):

if __name__ == '__main__':
    unittest.main()
