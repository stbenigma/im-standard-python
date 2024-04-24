import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


from SSOT_db.SQL_INFRA import dbConnect
from SSOT_db.createDB import main, existsDB, createDB,applysqlscript,insertBaseData
from SSOT_infra import Parameter
from SSOT_infra.parameters import expecteddbversion
import SSOT_infra.tests.integration as testsrc
from SSOT_db.IM_OBJECTS import Modelelemtype


class test_createDB(unittest.TestCase):

    def setUp(self) -> None:
        self.sqlitepath=testsrc.source_root() / 'SSOT_db' / 'dbstructure' / 'sqlite'
        self.testddl_1_6 = (Path(__file__).parent) / "TEST1.6_modelmodel_sqlite.sql"
        self.debugpath = Path.home() / "Downloads"  # try local debug path
        if not Path.exists(self.debugpath):
            self.debugpath = None
    def test_exists_db(self):
        self.assertFalse(existsDB(pfilepath=''))
        self.assertFalse(existsDB(pfilepath='bar.db'))
        with tempfile.TemporaryDirectory() as tempdir:
            f = open(os.path.join(tempdir, 'bar.db'), 'w')
            self.assertTrue(existsDB(pfilepath=f.name))
            f.close()

    def test_createandupgradenew_db(self):
        memorydb = ":memory:"
        connection = dbConnect.opendDB4DDL(pfilepath=memorydb)
        applysqlscript(psqlfilepath=self.testddl_1_6)
        dbversion = dbConnect.readversion(connection)
        self.assertTrue(dbversion["version"]=="1.6")

        upgradesql=self.sqlitepath / "modelmodel_sqlite_1.6.1.sql"
        if Path.exists(upgradesql):
            applysqlscript(psqlfilepath=upgradesql)
            dbversion = dbConnect.readversion(connection)
            self.assertEqual("1.6.1",dbversion["version"])

        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            dbfile="TESTDDL.db"
            connection = dbConnect.opendDB4DDL(pfilepath=dbfile)
            applysqlscript(psqlfilepath=self.testddl_1_6)
            insertBaseData()
            dbversion = dbConnect.readversion(connection)
            self.assertTrue(dbversion["version"] == "1.6")
            melts=Modelelemtype.select()
            connection.close()

            createDB(pupgrade=True,pdestination=dbfile)
            connection = dbConnect.openDB(pfilepath=dbfile)
            dbversion = dbConnect.readversion(connection)
            self.assertEqual (expecteddbversion(), dbversion["version"])
            melts=Modelelemtype.select()
            self.assertEqual(20,len(melts)) #Version 2.1 20 Modelelemtypes
            curmeltnames = {
                'ARCS',
                'ATTR',
                'BURU',
                'COLU',
                'DOMA',
                'ENTI',
                'DATM',
                'ORGU',
                'RELA',
                'SYNO',
                'TABL',
                'DATY',
                'KEYS',
                'DOCU',
                'DGRM',
                'DIAG',
                'EXPL',
                'ACTR',
                'SYST',
                'MAPS', }
            self.assertEqual( curmeltnames ,set(m.melt_shortname for m in melts))

            return
        #with

    def test_upgrade_db(self):
        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            # test real upgrade
            savefilename = Parameter.SQLFILENAME
            os.chdir(self.sqlitepath)
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

            with open(os.path.join(tempdir, 'bar.params'), 'w') as f:
                try:
                    main(psysargs=['createDB.py', '-p', f.name, '--unittest'])
                except:
                    pass
            try:
                main(psysargs=['createDB.py', '-m', 'Model', '--unittest'])
            except:
                pass
        return

    def test_create_db_raise(self):
        with self.assertRaises(Exception):
            createDB()
        with self.assertRaises(Exception):
            createDB(pmodelname=None)
        with self.assertRaises(Exception):
            createDB(pupgrade=False, pdbtype=Parameter.SQLITE)

    def test_create_db(self):

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
        dbdirecpath = os.path.join(testsrc.path_to_testmodels(), testsrc.TESTMODEL2, 'DB')
        dbfilepath = os.path.join(dbdirecpath, testsrc.TESTMODEL2 + '.db')
        if os.path.exists(dbfilepath):
            shutil.rmtree(dbdirecpath)

