import unittest
from IM_ODM import fillDB
from os import path, remove

from SSOT_infra.tests.test_translateprompt import TestTranslation


class TestFillDB(unittest.TestCase):

    testdirectory = path.join(path.dirname(__file__), '..', '..', 'testenvironment', 'odmloadtest',
                              'testmodels')

    def setUp(self) -> None:
        translation = TestTranslation()
        translation.setUp()

    def test_filldbmain(self):
        assert True

    def test_fillmergedb(self):
        assert True

    def test_main(self):
        testpath = path.join(self.testdirectory, 'testmodel-1')
        dbfilepath = path.join(testpath, 'DB', 'testmodel-1.db')
        try:
            remove(dbfilepath)
        except FileNotFoundError:
            print(f"dbfile not found: {dbfilepath}")

        try:
            fillDB.main(p_param1=str(testpath), create_base_folder=True)
        except:
            self.fail(f"FAILED 1. load {testpath}")

        try:
            fillDB.main(p_param1=str(testpath))
        except:
            self.fail(f"FAILED 2. load {testpath}")

        testpath = path.join(self.testdirectory, 'crmTest')
        dbfilepath = path.join(testpath, 'DB', 'crmTest.db')
        try:
            remove(dbfilepath)
        except FileNotFoundError:
            print(f"dbfile not found: {dbfilepath}")

        try:
            fillDB.main(p_param1=str(testpath), create_base_folder=True)
        except:
            self.fail(f"FAILED 1. load {testpath}")

        try:
            fillDB.main(p_param1=str(testpath))
        except:
            self.fail(f"FAILED 2. load {testpath}")
