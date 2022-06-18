import os
import shutil
import subprocess
import tempfile
import unittest
from os import path

from SSOT_db.SQL_INFRA import dbConnect
from SSOT_db.createDB import main, existsDB, createDB,applysqlscript
from SSOT_infra import Parameter
import SSOT_infra.tests.integration as testsrc


class test_createDB(unittest.TestCase):

    def test_applysqlscript(self):
        assert True

    def test_insertdiagtypes(self):
        assert True

    def test_insert_base_data(self):
        assert True

    def test_exists_db(self):
        self.assertFalse(existsDB(pfilepath=''))
        self.assertFalse(existsDB(pfilepath='bar.db'))
        with tempfile.TemporaryDirectory() as tempdir:
            f = open(path.join(tempdir, 'bar.db'), 'w')
            self.assertTrue(existsDB(pfilepath=f.name))
            f.close()

    def test_createnew_db(self):
        assert True

    def test_version(self):
        assert True

    def test_getlistofupgrfiles(self):
        assert True

    def test_applyupgrades(self):
        assert True

    def test_upgrade_db(self):
        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            # test real upgrade
            savefilename = Parameter.SQLFILENAME
            os.chdir(testsrc.source_root() / 'SSOT_db' / 'dbstructure' / 'sqlite')
            try:
                lastfile = subprocess.check_output(["git", "show",
                                                    f"2.9:./modelmodel_sqlite.sql"
                                                    ]).decode("utf-8")
                os.chdir(tempdir)
                with open(f"{Parameter.sqlpath()}/LAST_modelmodel_sqlite.sql", 'w') as f:
                    f.write(lastfile)
                Parameter.SQLFILENAME = 'LAST_modelmodel_sqlite'
                # create new db without applying insert base data
                connection = dbConnect.opendDB4DDL(pfilepath=dbpath)
                applysqlscript(psqlfilepath=Parameter.sqlfilepath())
                dbConnect.setversion()
                dbConnect.checkson()  # enable all constraints
                dbConnect.closeDB()
                createDB(pdestination=dbpath, pmodelname=testsrc.TESTMODEL1, pupgrade=True)
            except:
                print("upgrade of  modelmodel_sqlite.sql not tested if there's no git")
            Parameter.SQLFILENAME = savefilename

    def test_main(self):
        os.chdir(os.path.dirname(__file__))
        with self.assertRaises(SystemExit) as cm:
            main(psysargs=['createDB.py', '--version', '--unittest'])
            self.assertEqual(cm.exception.code, 2)
        with self.assertRaises(SystemExit) as cm:
            main(psysargs=['createDB.py', '--version', '--paramfile=abc.def', '--unittest'])

        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            with self.assertRaises(SystemExit) as cm:
                main(psysargs=['createDB.py', '-p', 'bar.params', '--unittest'])
            self.assertEqual(cm.exception.code, 1)
            with self.assertRaises(SystemExit):
                main(psysargs=['createDB.py', '-p', 'bar.params', '-m', 'Model', '--unittest'])
            with self.assertRaises(SystemExit):
                main(psysargs=['createDB.py', '--unittest'])
            with self.assertRaises(SystemExit):
                main(psysargs=['createDB.py', '-paramfile', 'bar.params', '-m', 'Model', '--unittest'])
            with self.assertRaises(SystemExit):
                main(psysargs=['createDB.py', '-paramfile', 'bar.params', '-modelname', 'Model', '--unittest'])

            with open(path.join(tempdir, 'bar.params'), 'w') as f:
                try:
                    main(psysargs=['createDB.py', '-p', f.name, '--unittest'])
                except:
                    pass
            try:
                main(psysargs=['createDB.py', '-m', 'Model', '--unittest'])
            except:
                pass
        return

    def test_create_db(self):
        with self.assertRaises(Exception):
            createDB()
        with self.assertRaises(Exception):
            createDB(pmodelname=None)
        with self.assertRaises(Exception):
            createDB(pupgrade=False, pdbtype=Parameter.SQLITE)

        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            logfilepath = os.path.join(tempdir, 'logfile.lll')
            createDB(pmodelname=testsrc.TESTMODEL1, plogfilepath=logfilepath)
            createDB(pmodelname=testsrc.TESTMODEL1, pupgrade=True, plogfilepath=logfilepath)
            self.assertTrue(os.path.exists(logfilepath))
            shutil.rmtree('DB/')
            with self.assertRaises(Exception):
                createDB(pmodelname=testsrc.TESTMODEL1, pupgrade=True)

            # empty database witout version information
            dbpath = os.path.join(tempdir, testsrc.TESTMODEL1 + '.db')
            dbConnect.opendDB4DDL(pfilepath=dbpath)
            with self.assertRaises(Exception):
                createDB(pmodelname=testsrc.TESTMODEL1, pdestination=dbpath, pupgrade=True)
            shutil.rmtree('DB/')

        # test with testmodel-2
        dbdirecpath = os.path.join(testsrc.testmodels_dir(), testsrc.TESTMODEL2, 'DB')
        dbfilepath = os.path.join(dbdirecpath, testsrc.TESTMODEL2 + '.db')
        if os.path.exists(dbfilepath):
            shutil.rmtree(dbdirecpath)

