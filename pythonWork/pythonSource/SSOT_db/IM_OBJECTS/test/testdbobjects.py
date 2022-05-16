
import unittest

import SSOT_infra.tests.integration as testsrc
from LOAD_MODELS.LOAD_ODM.tests.test_fillDB import create_testmodel
from SSOT_db.IM_OBJECTS import Entity,Actorrole,Actorconcern,Attribute,Externalref,DomaingroupMember,ModelelemDocu
from SSOT_db.SQL_INFRA import dbConnect


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.testmodel1 = testsrc.Testmodel(testsrc.TESTMODEL1)
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
            actrs = Actorrole.select()
            self.assertEqual('CEO',actrs[0].actr_name)
            actcs = actrs[0].getchildren()
            self.assertEqual(attr.attr_id,actcs[0].actc_mode_id)
            self.assertEqual(actrid,actcs[0].actc_actr_id)
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

if __name__ == '__main__':
    unittest.main()
