import logging
import unittest
from pathlib import Path

import pytest

import test_dbDLL
from IM_STANDARD.SQL.SQL_INFRA import SqliteDb, DbDML


class MyTestCase(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        caplog.set_level(logging.WARNING)
        self.capsys = capsys
        self.tmp_path = Path(tmp_path)

    def setUp(self) -> None:
        self.testsqlpath = Path(__file__).parent

        self.conn = SqliteDb().connection

        self.tablename = test_dbDLL.createtable(conn=self.conn,
                                                withfk=False)
        self.dmlconn = DbDML(connection=self.conn)
        return

    def test_statemets(self):
        rowcnt = self.dmlconn.rowcount(tablename=self.tablename)
        self.assertEqual(0, rowcnt)

        inssql = f"""insert into {self.tablename}
                    (mode_col1,mode_col2,mode_col3,mode_col4)
                    VALUES (?,?,?,?)"""
        selsql = f"""select * from {self.tablename}"""

        self.dmlconn.insert(sql=inssql, rec=("abc", None, "def", 1))
        self.assertEqual(1, self.dmlconn.rowcount(tablename=self.tablename))

        cols = self.dmlconn.select(sql=selsql)
        self.assertEqual(1, len(cols))
        self.dmlconn.insert(sql=inssql, rec=[("neu", "DRAFT", "usw", 123),
                                             ("neu2", "PUBL", "usw", 7)]
                            )
        cols = self.dmlconn.select(sql=selsql)
        self.assertEqual(3, len(cols))

        rowcnt = self.dmlconn.execsql(
                                   sql=f"delete from {self.tablename} where mode_col1=:col1",
                      col1="neu"
                                   )
        self.assertEqual(1, rowcnt)
        self.assertEqual(2, self.dmlconn.rowcount(tablename=self.tablename))


        self.dmlconn.execsql(sql=f"delete from {self.tablename}")

        inssql2 = f"""insert into {self.tablename}
                    (mode_id,mode_col1,mode_col2,mode_col3,mode_col4)
                    VALUES (:idx,:col1,:col2,:col3,:intval)"""

        self.dmlconn.insert(sql=inssql2, rec={"idx": 99,
                                             "col1": "abc",
                                             "col2": None,
                                             "intval": 99,
                                             "col3": "def"}
                            )
        cols = self.dmlconn.select(sql=selsql)
        self.assertEqual(99, cols[0].get("mode_id"))
        self.dmlconn.rowinsert(tablename=self.tablename,
                               mode_id= 98,
                               mode_col1= "abc",
                               mode_col2= None,
                               mode_col3= 99,
                               mode_col4= "def"
                               )
        cols = self.dmlconn.select(sql=selsql)
        self.assertEqual(98, cols[0].get("mode_id"))

        self.assertEqual("abc",self.dmlconn.lookupvalue(tablename=self.tablename,
                                                        colname="mode_col1",
                                                        mode_id=98))
        lookrow=self.dmlconn.lookuprow(tablename=self.tablename,
                                                        mode_id=98)
        self.assertDictEqual({"mode_id": 98,
                               "mode_col1": "abc",
                               "mode_col2": None,
                               "mode_col3": '99',
                               "mode_col4": "def"},
                            lookrow)

        return
