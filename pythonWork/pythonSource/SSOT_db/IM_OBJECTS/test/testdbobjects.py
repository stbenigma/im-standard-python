import os
import unittest

import SSOT_infra.tests.integration as testsrc
from LOAD_MODELS.LOAD_ODM.tests.test_fillDB import create_testmodel
from LOAD_MODELS.LOAD_ODM import fillDB
from SSOT_db.IM_OBJECTS import Entity
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
        return


if __name__ == '__main__':
    unittest.main()
