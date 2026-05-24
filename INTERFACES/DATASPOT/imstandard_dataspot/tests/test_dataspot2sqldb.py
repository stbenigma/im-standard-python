import json
import unittest
from pathlib import Path

import pytest

from INTERFACES.DATASPOT import Dataspot2SQLdatabase,Sql2IMJsonschema
from IM_STANDARD.SQL import SqliteDb,DbDML,StandardSqlModel

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
        mydb=DbDML(basedb=SqliteDb())
        StandardSqlModel.createimstandarddb(db=mydb)
        inpath = Path(__file__).parent / "dataspottestfiles" / "astronomie"
        db=Dataspot2SQLdatabase(indirec=inpath,
                                mydb=mydb)
        db.filldatabase(modelname=inpath.stem,languages=["de","en"],language="en")
        return mydb

    def test_createdbastro(self):
        mydb=self._fillastrodb()

        self.assertEqual(17,len(mydb.gettablelist()))
        self.assertTrue("examples" in  mydb.gettablelist())

        catgs=mydb.select(sql="select * from entity_categories")
        self.assertEqual("Sternsystem",catgs[0].get("enca_name"))
        self.assertEqual(None,catgs[0].get("enca_enca_id"))
        self.assertEqual(catgs[0].get("enca_id"),catgs[1].get("enca_enca_id"))

        mydb.writedbtofile(filepath=self.mydebugpath/"test_sqldb.db")
        return

    def test_createdlocal(self):
        mydb=DbDML(basedb=SqliteDb())
        StandardSqlModel.createimstandarddb(db=mydb)
        inpath = Path(__file__).parent.parent.parent.parent.parent /"localtestmodels"/"CHEM-X-DMP"

        db=Dataspot2SQLdatabase(indirec=inpath,
                                mydb=mydb)
        db.filldatabase(modelname=inpath.stem,
                        languages=["de","en"],
                        language="en"
                        )

        mydb.writedbtofile(filepath=self.mydebugpath/"multilang_sqldb.db")
        return

    def test_sql2json(self):
        mydb=self._fillastrodb()
        sql2json=Sql2IMJsonschema(mydb=mydb)
        bmodel=sql2json.generatejson(status="ALL")
        with open (self.mydebugpath /"testsqljson.json",'w') as outfile:
            json.dump(bmodel,outfile,indent=2)
        return

if __name__ == '__main__':
    unittest.main()
