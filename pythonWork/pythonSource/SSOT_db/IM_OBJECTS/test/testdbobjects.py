
import unittest

import SSOT_infra.tests.integration as testsrc
from LOAD_MODELS.LOAD_ODM.tests.test_fillDB import create_testmodel
from SSOT_db.IM_OBJECTS import Entity,Actorrole,Actorconcern,Attribute,Externalref
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
            self.assertEqual('testrole1',actrs[0].actr_name)
            actcs = actrs[0].getchildren()
            self.assertEqual(attr.attr_id,actcs[0].actc_mode_id)
            self.assertEqual(actrid,actcs[0].actc_actr_id)
            self.assertEqual(actrid,Externalref.getmodeid(psrcname='test',psrcid='123123'))
            self.assertEqual(Attribute , type(actcs[0].getelement()))
            self.assertEqual('R' , actcs[0].getraci())
        finally:
            dbConnect.closeDB()
        return

if __name__ == '__main__':
    unittest.main()
