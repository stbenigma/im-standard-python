import sqlite3
import unittest
from pathlib import Path
import pytest
import logging

from IM_STANDARD.SQL.SQL_INFRA import SqliteDb,DbDDL

def  createtable(conn:sqlite3.Connection,withfk=True):
    """creates a test tabel (also used in test_dbDML"""
    tablename = "modelelement"
    tablename2="newtable"
    crtablesql= f"""CREATE TABLE {tablename} 
                    (mode_id  INTEGER  primary key autoincrement,
                    mode_col1  TEXT     NOT NULL,
                    mode_col2  TEXT,
                    mode_col3  TEXT     NOT NULL ,
                    mode_col4 INTEGER Default 2
                    CONSTRAINT mode2_chk CHECK (mode_col2 IN ('DRAFT','GTOP','PUBL')),
                    constraint mode_UK unique (mode_col1,mode_col3),
                   constraint model2_uk unique (mode_col4)"""
    crtable2=f"""CREATE TABLE {tablename2} 
                    (newt_id  INTEGER  primary key autoincrement,
                    newt_col1  INTEGER     NOT NULL,
                    newt_col2  INTEGER,
                    newt_col3  TEXT     NOT NULL ,
                    newt_col4 INTEGER Default 2,
                    CONSTRAINT fk foreign key (newt_col1) references {tablename} (mode_id)
                    );
                    """
    fks=""",CONSTRAINT model_fk  FOREIGN KEY (mode_col4)
                        REFERENCES modelelement (mode_id) ON DELETE CASCADE,
                CONSTRAINT model_fk2  FOREIGN KEY (mode_col3,mode_col2)
                        REFERENCES modelelement (mode_id,model_col4)                        
                """
    print (crtablesql + (fks if withfk else "")+";")
    ddlconn=DbDDL(connection=conn)
    ddlconn.execscript(sql=crtablesql + (fks if withfk else "")+");")
    ddlconn.execscript(sql=crtable2 )
    return [tablename,tablename2]

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

    def test_functions(self):
        conn=SqliteDb().connection

        tablename=createtable(conn=conn)

        ddlconn=DbDDL(connection=conn)
        tabs=ddlconn.gettablelist()
        self.assertEqual(2,len(tabs))
        self.assertEqual(tablename[0],tabs[0])

        cols=ddlconn.getcolums(tablename=tablename[0])
        self.assertEqual(5,len(cols))
        self.assertTrue("mode_id" in cols)
        self.assertEqual(True,cols["mode_id"].get("inpk"))
        self.assertEqual(True,cols["mode_id"].get("mandatory"))
        self.assertEqual(False,cols["mode_col2"].get("mandatory"))
        self.assertEqual("TEXT",cols["mode_col1"].get("datatype"))
        self.assertEqual("2",cols["mode_col4"].get("default"))
        #print (json.dumps(cols["mode_id"],indent=2))

        uks=ddlconn.getuklist(tablename=tablename[0])
        self.assertEqual(2,len(uks))
        self.assertEqual(1,len(list(uks[0].values())[0]))
        self.assertEqual(2,len(list(uks[1].values())[0]))
        #print(json.dumps(uks[1], indent=2))

        fks=ddlconn.getfklist(tablename=tablename[0])
        self.assertEqual(2,len(fks))
        self.assertEqual(2,len(fks["fk-0"].get("from")))
        self.assertEqual("CASCADE",fks["fk-1"].get("on_delete"))
        #print(json.dumps(fks["fk-0"], indent=2))

        return
