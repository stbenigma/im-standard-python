import unittest
from pathlib import Path

import pytest

from IM_STANDARD.SQL.SQL_INFRA import SqliteDb,dbval
from IM_STANDARD.SQL.SQL_STANDARD import StandardModelDb


class Test_standardsqldb(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temppath = Path(tmp_path)

    def setUp(self) -> None:
        self.mydebugpath = (Path.home() / "Downloads") if (Path.home() / "Downloads").exists() else self.temppath
        return

    def _createdb(self):
        mydb=StandardModelDb(sqlitedb=SqliteDb(), withsqlmodel=True)
        return mydb

    def test_emptystandarddb(self):
        mydb = self._createdb()
        mydb.writedbtofile(filepath=self.mydebugpath / "testemptydb.db")
        self.assertEqual(17, len(mydb.gettablelist()))
        self.assertTrue("entities" in mydb.gettablelist())
        return

    def test_sqlconsistency(self):
        mydb = self._createdb()

        modeidattr=mydb.rowinsert(tablename="modelelements",
                                  mode_id=1000, mode_type="ATTR", mode_dc=1, mode_uc=1)
        self.assertEqual('ATTR', mydb.lookupvalue(tablename="modelelements",
                                                  colname="mode_type", mode_id=modeidattr)
                         )

        modeidmodel=mydb.rowinsert(tablename="modelelements",
                       mode_id=1001,mode_type="MODL",mode_dc=1,mode_uc=1)


        modlidtest=mydb.rowinsert(tablename="models",modl_name="test",
                       modl_id=modeidmodel,modl_type="IM")

        modeidenti=mydb.rowinsert(tablename="modelelements",
                       mode_id=1003,mode_type="ENTI",
                        mode_modl_id=modlidtest, mode_dc=1,mode_uc=1)

        #with self.assertRaises(SqliteDb.CHECK_VIOLATED):
        with self.assertRaises(Exception):
            mydb.rowinsert(tablename="modelelements",
                       mode_id=7778,mode_type="BURU",
                           mode_modl_id=None,mode_dc=1,mode_uc=1)

        with self.assertRaises(Exception):
            mydb.rowinsert(tablename="models",modl_name="testfalsch",
                       modl_id=7777,modl_type="IM")
        with self.assertRaises(Exception):
            mydb.rowinsert(tablename="models",modl_name="test",
                       modl_id=modeidmodel,modl_type="IM")
        with self.assertRaises(Exception):
            # check recursive
            mydb.rowinsert(tablename="modelelements",
                           mode_type="MODL",
                           mode_modl_id=1,mode_dc=1,mode_uc=1)

        langid = mydb.rowinsert(tablename="languages",
                                      lang_iso_code2='en')
        mydb.rowinsert(tablename="model_languages",
                                 mola_lang_id=langid,
                                 mola_modl_id=modlidtest,
                                 mola_mainlanguage=dbval('TRUE')
                                 )

        return


if __name__ == '__main__':
    unittest.main()
