import os
import unittest

from LOAD_MODELS.LOAD_ODM import fillDB
from SSOT_infra.tests.test_translateprompt import TestTranslation
import SSOT_infra.tests.integration as testsrc


class TESTFILLDB(unittest.TestCase):

    def setUp(self) -> None:
        translation = TestTranslation()
        translation.setUp()

    def test_filldbmain(self):
        assert True

    def test_fillmergedb(self):
        assert True

    def test_filldb(self):
        # create model for testmodel1. no param file
        testmodelname = testsrc.TESTMODEL1
        testpath = testsrc.testmodels_dir() / testmodelname
        dbdirpath = testpath / 'DB'
        dbfilepath = dbdirpath / (testmodelname + '.db')
        if os.path.exists(dbfilepath):
            os.remove(dbfilepath)
        os.chdir(testpath)
        fillDB.filldbmain(pmodelname=testmodelname, pdestination=dbfilepath)
        self.assertTrue(os.path.exists(dbfilepath), f"DB file not created where assumed {dbfilepath}")
        self.assertTrue(os.path.exists(dbdirpath / (testmodelname + '_loaded.json')),
                        f"json file not where assumed {dbdirpath  / (testmodelname + '_loaded.json')}")
        self.assertTrue(os.path.exists(dbdirpath / (testmodelname + '.json')),
                        f"json file not where assumed {dbdirpath / (testmodelname + '.json')}")
        self.assertTrue(os.path.exists(testpath / (testmodelname + '.log')),
                        f"json file not where assumed {testpath / (testmodelname + '.log')}")
        #create db for a second time => merge
        fillDB.filldbmain(pmodelname=testmodelname, pdestination=dbfilepath)

        # create db for testmodel2crmtest with Paramfile
        testmodelname = testsrc.TESTMODEL2
        testpath = testsrc.testmodels_dir() / testmodelname
        dbdirpath = testpath / 'DB'
        dbfilepath = dbdirpath / (testmodelname + '.db')
        logfilepath = testpath / "logfiles" / "speciallog.log"
        paramfile = testpath / ( testmodelname + '.params')
        fillDB.filldbmain(pparamfile=paramfile)

        # create db for crmtest with Paramfile
        testmodelname = testsrc.CRMTEST
        testpath = testsrc.testmodels_dir() / testmodelname
        dbdirpath = testpath / 'DB'
        dbfilepath = dbdirpath / (testmodelname + '.db')
        logfilepath = testpath / ( testmodelname + '.log')
        paramfile = testpath / ( testmodelname + '.params')
        # error for wrong modelname
        with self.assertRaises(Exception):
            fillDB.filldbmain(pparamfile=paramfile, pmodelname='Gugus')

        # should work
        if os.path.exists(dbfilepath):
            os.remove(dbfilepath)
        if os.path.exists(logfilepath):
            os.remove(logfilepath)

        fillDB.filldbmain(pparamfile=paramfile)
        self.assertTrue(os.path.exists(dbfilepath), f"DB file not created where assumed {dbfilepath}")
        self.assertTrue(os.path.exists(dbdirpath / (testmodelname + '_loaded.json')),
                        f"json file not where assumed {dbdirpath / (testmodelname + '_loaded.json')}")
        self.assertTrue(os.path.exists(dbdirpath / ( testmodelname + '.json')),
                        f"json file not where assumed {dbdirpath / ( testmodelname + '.json')}")
        self.assertTrue(os.path.exists(logfilepath),
                        f"json file not where assumed {logfilepath}")

        testmodelname = testsrc.RIDDLE
        testpath = testsrc.testmodels_dir() / testmodelname
        dbdirpath = testpath / 'DB'
        dbfilepath = dbdirpath / (testmodelname + '.db')
        if os.path.exists(dbfilepath):
            os.remove(dbfilepath)
        os.chdir(testpath)
        fillDB.filldbmain(pmodelname=testmodelname, pdestination=dbfilepath)
        self.assertTrue(os.path.exists(dbfilepath), f"DB file not created where assumed {dbfilepath}")
        self.assertTrue(os.path.exists(dbdirpath / (testmodelname + '_loaded.json')),
                        f"json file not where assumed {dbdirpath / ( testmodelname + '_loaded.json')}")
        self.assertTrue(os.path.exists(dbdirpath / ( testmodelname + '.json')),
                        f"json file not where assumed {dbdirpath / ( testmodelname + '.json')}")
        self.assertTrue(os.path.exists((testmodelname + '.log')),
                        f"log file not where assumed {(testmodelname + '.log')}")
        return
