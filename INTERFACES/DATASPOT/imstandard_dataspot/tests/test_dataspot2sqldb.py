import unittest
from pathlib import Path

import pytest

from IM_STANDARD.SQL import SqliteDb, StandardModelDb
from INTERFACES.DATASPOT import Dataspot2SQLdatabase
from IM_STANDARD import Sql2IMJsonschema, Sql2IMowlschema


class Test_dataspot2sql(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temppath = Path(tmp_path)

    def setUp(self) -> None:
        self.mydebugpath = (Path.home() / "Downloads") if (Path.home() / "Downloads").exists() else self.temppath
        return

    def _fillastrodb(self):
        mydb = StandardModelDb(sqlitedb=SqliteDb(), withsqlmodel=True)
        inpath = Path(__file__).parent / "dataspottestfiles" / "astronomie"
        db = Dataspot2SQLdatabase(indirec=inpath,
                                  mydb=mydb)
        db.filldatabase(modelname=inpath.stem,
                        languages=["de", "en"], language="de")
        print("\n".join(self.caplog.messages))
        return mydb

    def test_createdbastro(self):
        mydb = self._fillastrodb()

        self.assertEqual(18, len(mydb.gettablelist()))
        self.assertTrue("examples" in mydb.gettablelist())

        catgs = mydb.select(sql="select * from entity_categories")
        cat = [cat for cat in catgs if cat.get("enca_name") == "Sternsystem"][0]
        self.assertEqual(None, cat.get("enca_enca_id"))

        mydb.writedbtofile(filepath=self.mydebugpath / "astro_sqldb.db")
        print(f'database written {str(self.mydebugpath / "astro_sqldb.db")}')
        return

    def test_createdlocal(self):
        mydb = StandardModelDb(sqlitedb=SqliteDb(), withsqlmodel=True)
        inpath = Path(__file__).parent.parent.parent.parent.parent / "localtestmodels" / "CHEM-X-DMP"

        db = Dataspot2SQLdatabase(indirec=inpath,
                                  mydb=mydb)
        db.filldatabase(modelname=inpath.stem,
                        languages=["de", "en"],
                        language="en"
                        )
        print("\n".join(self.caplog.messages))

        mydb.writedbtofile(filepath=self.mydebugpath / "multilang_sqldb.db")
        return

    def test_createdimstandard(self):
        mydb = StandardModelDb(sqlitedb=SqliteDb(), withsqlmodel=True)

        inpath = Path(
            "/Users/stb/Documents/Projekte/IM-Standard/python-Projekt/Information-model-standard/Modelling Tools/dataspot/IM-Stand-2026-06")
        if not inpath.is_dir():
            self.skipTest(f"directory does not exist {inpath}")
        db = Dataspot2SQLdatabase(indirec=inpath,
                                  mydb=mydb)
        db.filldatabase(modelname=inpath.stem,
                        languages=["de", "en"],
                        language="de"
                        )
        print("\n".join(self.caplog.messages))

        mydb.writedbtofile(filepath=self.mydebugpath / "IM-standard.db")
        return




if __name__ == '__main__':
    unittest.main()
