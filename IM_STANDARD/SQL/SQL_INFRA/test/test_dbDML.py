import logging
import unittest
from pathlib import Path

import pytest

import test_dbDLL
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from dbConnect import SqliteDb
from dbDML import DbDML

class MyTestCase(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        caplog.set_level(logging.WARNING)
        self.capsys = capsys
        self.tmp_path = Path(tmp_path)

    def setUp(self) -> None:
        self.testsqlpath = Path(__file__).parent
        self.sqldb=SqliteDb()
        self.dmldb=DbDML(sqlitedb=self.sqldb)
        self.conn = self.sqldb.connection

        self.tablenames = test_dbDLL.createtable(ddldb=self.dmldb,
                                                 withfk=False)
        return

    def test_statemets(self):
        rowcnt = self.dmldb.rowcount(tablename=self.tablenames[0])
        self.assertEqual(0, rowcnt)

        inssql = f"""insert into {self.tablenames[0]}
                    (mode_col1,mode_col2,mode_col3,mode_col4)
                    VALUES (?,?,?,?)"""
        selsql = f"""select * from {self.tablenames[0]}"""

        self.dmldb.insert(sql=inssql, rec=("abc", None, "def", 1))
        self.assertEqual(1, self.dmldb.rowcount(tablename=self.tablenames[0]))

        cols = self.dmldb.select(sql=selsql,aslist=False)
        self.assertEqual(1, len(cols))
        self.dmldb.insert(sql=inssql, rec=[("neu", "DRAFT", "usw", 123),
                                             ("neu2", "PUBL", "usw", 7)]
                            )
        cols = self.dmldb.select(sql=selsql)
        self.assertEqual(3, len(cols))

        rowcnt = self.dmldb.execsql(
            sql=f"delete from {self.tablenames[0]} where mode_col1=:col1",
            col1="neu"
        )
        self.assertEqual(1, rowcnt)
        self.assertEqual(2, self.dmldb.rowcount(tablename=self.tablenames[0]))

        self.dmldb.execsql(sql=f"delete from {self.tablenames[0]}")

        inssql2 = f"""insert into {self.tablenames[0]}
                    (mode_id,mode_col1,mode_col2,mode_col3,mode_col4)
                    VALUES (:idx,:col1,:col2,:col3,:intval)"""

        self.dmldb.insert(sql=inssql2, rec={"idx": 99,
                                              "col1": "abc",
                                              "col2": None,
                                              "intval": 99,
                                              "col3": "def"}
                            )
        cols = self.dmldb.select(sql=selsql)
        self.assertEqual(99, cols[0].get("mode_id"))
        modeid = self.dmldb.rowinsert(tablename=self.tablenames[0],
                                        mode_id=98,
                                        mode_col1="abc",
                                        mode_col2=None,
                                        mode_col3=99,
                                        mode_col4="def"
                                        )
        cols = self.dmldb.select(sql=selsql)
        self.assertEqual(98, cols[0].get("mode_id"))

        self.assertEqual("abc", self.dmldb.lookupvalue(tablename=self.tablenames[0],
                                                         colname="mode_col1",
                                                         mode_id=98))
        lookrow = self.dmldb.lookuprow(tablename=self.tablenames[0],
                                         mode_id=98)
        self.assertDictEqual({"mode_id": 98,
                              "mode_col1": "abc",
                              "mode_col2": None,
                              "mode_col3": '99',
                              "mode_col4": "def"},
                             lookrow)

        self.dmldb.rowinsert(tablename=self.tablenames[1],
                               newt_id=55,
                               newt_col1=modeid,
                               newt_col2=None,
                               newt_col3=99,
                               newt_col4="defnewt"
                               )

        newsel = f"""SELECt mode_id,mode_col1 as '1.col', newt_col4 as 'defnewt'
                    from {self.tablenames[0]} 
                    join {self.tablenames[1]} on newt_col1=mode_id"""
        newdata = self.dmldb.select(sql=newsel)
        self.assertEqual({'mode_id': 98, '1.col': 'abc', 'defnewt': 'defnewt'},
                         newdata[0])

        return
