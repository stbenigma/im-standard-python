import os
import unittest

import SSOT_infra.tests.integration as testsrc
from LOAD_MODELS.LOAD_ODM import fillDB
from SSOT_db.IM_OBJECTS import Entity
from SSOT_db.SQL_INFRA import dbConnect


def create_testmodel(testmodelname, testdir, dbfilepath, new=True):
    # create model for testmodel1 no param file
    if new and os.path.exists(dbfilepath):
        os.remove(dbfilepath)
    os.chdir(testdir)
    fillDB.filldbmain(pmodelname=testmodelname, pdestination=dbfilepath)
    return

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        testmodelname, testdir, dbfilepath = testsrc.testmodel1()
        create_testmodel(testmodelname=testmodelname, testdir=testdir, dbfilepath=dbfilepath, new=True)
        return

    def test_entity(self):
        dbConnect.openDB(pfilepath=testsrc.testmodel1()[2])
        enti = Entity.select(pwhere=('enti_name=?','Child Entity1'))
        attrs=enti[0].getinheritedattrids()
        self.assertEqual(1,len(attrs))
        enti = Entity.select(pwhere=('enti_name=?','Multi UK Entity'))
        attrs=enti[0].getinheritedattrids()
        self.assertEqual(2,len(attrs))
        enti = Entity.select(pwhere=('enti_name=?','role Entity'))
        attrs=enti[0].getinheritedattrids()
        self.assertEqual(2,len(attrs))
        return


if __name__ == '__main__':
    unittest.main()
