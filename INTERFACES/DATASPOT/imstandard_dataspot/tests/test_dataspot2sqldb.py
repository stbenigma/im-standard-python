import json
import unittest
import subprocess

from pathlib import Path

import pytest

from INTERFACES.DATASPOT import Dataspot2SQLdatabase,Sql2IMJsonschema,Sql2IMowlschema
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
        db.filldatabase(modelname=inpath.stem,
                        languages=["de","en"],language="de")
        print ("\n".join(self.caplog.messages))
        return mydb

    def test_createdbastro(self):
        mydb=self._fillastrodb()

        self.assertEqual(17,len(mydb.gettablelist()))
        self.assertTrue("examples" in  mydb.gettablelist())

        catgs=mydb.select(sql="select * from entity_categories")
        cat= [cat for cat in catgs if cat.get("enca_name")=="Sternsystem"][0]
        self.assertEqual(None,cat.get("enca_enca_id"))

        mydb.writedbtofile(filepath=self.mydebugpath/"test_sqldb.db")
        print (f'database written {str(self.mydebugpath/"test_sqldb.db")}')
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
        print ("\n".join(self.caplog.messages))

        mydb.writedbtofile(filepath=self.mydebugpath/"multilang_sqldb.db")
        return

    def _validate(self,jsonpath):
        generate = [
            'invoke',
            'validateStandard',
            "--verbose",
            "--injson",
            str(jsonpath)
        ]
        result = subprocess.run(generate, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stderr, result.stdout, result.returncode)
        self.assertEqual(0, result.returncode)
        return

    def test_sql2json(self):
        mydb=self._fillastrodb()
        mydb.writedbtofile(filepath=self.mydebugpath /"testsql.db")
        sql2json=Sql2IMJsonschema(mydb=mydb)
        bmodel=sql2json.generatejson(status="ALL")

        with open (self.mydebugpath /"testsqljson.json",'w') as outfile:
            json.dump(bmodel,outfile,indent=2)
            print (f'{self.mydebugpath / "testsqljson.json"} written')
        self._validate(jsonpath=self.mydebugpath / "testsqljson.json")
        return

    def test_sql2rdf(self):
        mydb = self._fillastrodb()
        mydb.writedbtofile(filepath=self.mydebugpath /"testsql.db")
        print (f'{self.mydebugpath /"testsql.db"} written')

        sql2json = Sql2IMowlschema(mydb=mydb)
        turtle = sql2json.generatejson(status="ALL")
        with open(self.mydebugpath / "testsqlrdf.ttl", 'w') as outfile:
            outfile.write(turtle.serialize(format="turtle"))
            print (f'{self.mydebugpath / "testsqlrdf.ttl"} written')

        return


if __name__ == '__main__':
    unittest.main()
