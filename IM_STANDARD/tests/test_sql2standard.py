import unittest
from pathlib import Path

import pytest

from IM_STANDARD import Sql2IMJsonschema, Sql2IMowlschema, StandardJsonModel, remove_empty_values
from IM_STANDARD.JSON import jsonvalidation
from IM_STANDARD.SQL.SQL_INFRA import SqliteDb, DbDML


class Test_sql2standard(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temppath = Path(tmp_path)

    def setUp(self) -> None:
        self.mydebugpath = (Path.home() / "Downloads") if (Path.home() / "Downloads").exists() else self.temppath
        self.sqltestfilepath = Path(__file__).parent.parent / "SQL" / "SQL_STANDARD"\
                               / "tests" / "sql-test-files"
        return

    def test_sql2jsonastro(self):
        mydb = DbDML(sqlitedb=SqliteDb(filepath=self.sqltestfilepath / "astro_sqldb.db"))
        sql2json = Sql2IMJsonschema(mydb=mydb)
        bmodel = sql2json.generatejson(status="ALL", notnullonly=False)
        smallbmodel = sql2json.generatejson(status="ALL")
        StandardJsonModel.dumpjsonfile(outpath=self.mydebugpath / "astrosqljsonfull.json",
                                       struct=bmodel,
                                       verbose=True)
        smallbmodel = remove_empty_values(bmodel)
        StandardJsonModel.dumpjsonfile(outpath=self.mydebugpath / "astrosqljson.json",
                                       struct=smallbmodel,
                                       verbose=True)

        jsonvalidation.validate_jsonfile_as_schema(self.mydebugpath / "astrosqljson.json")
        return

    def test_sql2jsonIM(self):
        mydb = DbDML(sqlitedb=SqliteDb(filepath=self.sqltestfilepath / "IM-standard.db"))
        sql2json = Sql2IMJsonschema(mydb=mydb)
        bmodel = sql2json.generatejson(status="ALL")

        StandardJsonModel.dumpjsonfile(outpath=self.mydebugpath / "IMsqljson.json",
                                       struct=bmodel,
                                       verbose=True)

        jsonvalidation.validate_jsonfile_as_schema(self.mydebugpath / "IMsqljson.json")
        return

    def test_sql2rdf(self):
        mydb = DbDML(sqlitedb=SqliteDb(filepath=self.sqltestfilepath / "astro_sqldb.db"))
        sql2json = Sql2IMowlschema(mydb=mydb)
        turtle = sql2json.generatejson(status="ALL")
        with open(self.mydebugpath / "testsqlrdf.ttl", 'w') as outfile:
            outfile.write(turtle.serialize(format="turtle"))
            print(f'{self.mydebugpath / "testsqlrdf.ttl"} written')

        return


if __name__ == '__main__':
    unittest.main()
