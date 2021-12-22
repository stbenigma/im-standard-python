import unittest

from .. import existsDB,createDB
import tempfile
from os import path
from SSOT_infra import parameters



class test_createDB(unittest.TestCase):
    testdirectory = path.join(path.dirname(__file__),'..','..' ,'testenvironment', 'odmloadtest',
                                  'testmodels', 'testmodel-1')

    def test_applysqlscript(self):
        assert True

    def test_insertdiagtypes(self):
        assert True

    def test_insert_base_data(self):
        assert True

    def test_exists_db(self):
        self.assertFalse(existsDB(pfilepath=''))
        self.assertFalse(existsDB(pfilepath='bar.db'))
        print (self.testdirectory)
        with tempfile.TemporaryDirectory() as tempdir:
            f = open(path.join(tempdir, 'bar.db'), 'w')
            self.assertTrue( existsDB(pfilepath=f.name))

    def test_createnew_db(self):
        assert True

    def test_version(self):
        assert True

    def test_getlistofupgrfiles(self):
        assert True

    def test_applyupgrades(self):
        assert True

    def test_upgrade_db(self):
        assert True

    def test_create_db(self):
        with self.assertRaises(Exception):
            createDB(par1='something/somewhere', pforcecreate=True, pupgrade=False, pdbtype=parameters.SQLITE)
        createDB(par1=str(self.testdirectory), pforcecreate=True, pupgrade=False, pdbtype=parameters.SQLITE)
        assert existsDB(parameters.dbFilePath())
        with self.assertRaises(Exception):
            createDB(par1=str(self.testdirectory), pforcecreate=False, pupgrade=False, pdbtype=parameters.SQLITE)
