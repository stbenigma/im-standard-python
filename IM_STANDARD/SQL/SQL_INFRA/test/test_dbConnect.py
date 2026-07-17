import unittest
from pathlib import Path
import pytest
import logging

from SQL.SQL_INFRA import SqliteDb,dict_factory


class MyTestCase(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        caplog.set_level(logging.WARNING)
        self.capsys = capsys
        self.tmp_path = Path(tmp_path)

    def setUp(self) -> None:
        self.testsqlpath=Path(__file__).parent
        return

    def test_newdb(self):
        conn=SqliteDb()
        self.assertTrue(conn.dbisempty())

        with self.assertRaises(Exception) as exp:
            conn.writedbtofile() #no filepath ever given

        testdbfilepath=self.tmp_path/"testemptydb.db"
        conn.writedbtofile(filepath=testdbfilepath)
        self.assertTrue(testdbfilepath.is_file())

        conn._readdbfromfile(filepath=testdbfilepath)
        self.assertTrue(conn.dbisempty())

        cursor=conn.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables=cursor.fetchall()
        self.assertTrue(len(tables)==0)

        conn.connection.row_factory = dict_factory
        cursor=conn.connection.cursor()
        cursor.execute("PRAGMA table_info('sqlite_master');")

        tableinfo=cursor.fetchall()
        self.assertTrue(tableinfo[0].get("name")=="type")

        return

    def test_loaddb(self):
        conn=SqliteDb()
        self.assertTrue(conn.dbisempty())

        #create table
        cursor=conn.connection.cursor()
        cursor.execute("""CREATE TABLE modelelement
(
    mode_id  INTEGER  primary key autoincrement,   -- [K4]
    mode_dc  TEXT     NOT NULL,   -- [K5] DATETIME → TEXT (ISO-8601)
    mode_dm  TEXT,                -- [K5]
    mode_uc  TEXT     NOT NULL,   -- [K6]
    mode_um  TEXT
);
""")
        self.assertFalse(conn.dbisempty())

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables=cursor.fetchall()
        self.assertTrue(tables[0][0]=="modelelement")

        testdbfilepath = self.tmp_path / "testemptydb.db"
        conn.writedbtofile(filepath=testdbfilepath)
        self.assertTrue(testdbfilepath.is_file())

        with self.assertRaises(Exception) as e:
            conn._readdbfromfile(filepath=testdbfilepath)


        conn=SqliteDb()
        conn._readdbfromfile(filepath=testdbfilepath)
        self.assertFalse(conn.dbisempty())

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables=cursor.fetchall()
        self.assertTrue(tables[0][0]=="modelelement")

        return
