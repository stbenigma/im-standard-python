import unittest
from pathlib import Path

import pytest

from INTERFACES.DATASPOT import Dataspot2SQLdatabase
from IM_STANDARD.SQL.SQL_INFRA import SqliteDb,DbDML
from IM_STANDARD import StandardSqlModel

class Test_dataspot2sql(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temppath = Path(tmp_path)

    def setUp(self) -> None:
        self.mydebugpath = (Path.home() / "Downloads") if (Path.home() / "Downloads").exists() else self.temppath
        return

    def test_createdbastro(self):
        basedb=SqliteDb()
        mydb=DbDML(connection=basedb.connection)
        inpath = Path(__file__).parent / "dataspottestfiles" / "astronomie"

        db=Dataspot2SQLdatabase(indirec=inpath,
                                mydb=mydb)

        self.assertFalse(basedb.dbisempty())
        self.assertEqual(10,len(mydb.gettablelist()))
        self.assertTrue("examples" in  mydb.gettablelist())

        db.filldatabase(modelname=inpath.stem,languages=["de","en"],language="en")
        print (mydb.rowcount("entity_categories"))
        catgs=mydb.select(sql="select * from entity_categories")
        self.assertEqual("Sternsystem",catgs[0].get("enca_name"))
        self.assertEqual(None,catgs[0].get("enca_enca_id"))
        self.assertEqual(catgs[0].get("enca_id"),catgs[1].get("enca_enca_id"))

        basedb.writedbtofile(filepath=self.mydebugpath/"test_sqldb.db")
        return

    def test_createdlocal(self):
        basedb=SqliteDb()
        mydb=DbDML(connection=basedb.connection)
        inpath = Path(__file__).parent.parent.parent.parent.parent /"localtestmodels"/"CHEM-X-DMP"

        db=Dataspot2SQLdatabase(indirec=inpath,
                                mydb=mydb)
        db.filldatabase(modelname=inpath.stem,
                        languages=["de","en"],
                        language="en"
                        )

        basedb.writedbtofile(filepath=self.mydebugpath/"multilang_sqldb.db")
        return


if __name__ == '__main__':
    unittest.main()
