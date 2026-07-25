import unittest
from pathlib import Path
import pytest

from INTERFACES.EXCEL import CreateSchemaExcel,createexcel


class MyTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temppath = Path(tmp_path)

    def setUp(self) -> None:
        self.testfilepath = Path(__file__).parent / "testfiles"
        self.mydebugpath = (Path.home() / "Downloads") if (Path.home() / "Downloads").exists() else self.temppath
        return

    def test_astronomie(self):
        self.astronomietestjsonpath = Path(__file__).parent.parent.parent.parent / \
                                      "IM_STANDARD" /"tests" / "json-test-standard-files" / "astronomie-assets-standard.json"
        CreateSchemaExcel(standardjson=self.astronomietestjsonpath,
                          lang="en").writeexcel(outfilepath=self.mydebugpath / "astronomie-schema.xlsx")
        return

    def test_longnames(self):
        self.astronomietestjsonpath = Path(__file__).parent.parent.parent.parent / \
                                      "IM_STANDARD" /"tests" / "json-test-standard-files" / "astronomie-assets-standard.json"
        excel=CreateSchemaExcel(standardjson=self.astronomietestjsonpath,
                          lang="en")
        excel._standardjson.jsonschemamodel["Entities"][0]["name"]["de"]="VielzulangerNameVielzulangerNameVielzulangerNameVielzulangerName"
        excel._standardjson.jsonschemamodel["Entities"][1]["name"]["de"]="VielzulangerNameVielzulangerNameVielzulangerNameVielzulangerName"
        excel.writeexcel(outfilepath=self.mydebugpath / "astronomie-schema-langname.xlsx")
        return

    def test_IM(self):
        self.imtestjsonpath = Path(__file__).parent.parent.parent.parent / \
                                      "IM_STANDARD" /"tests" / "json-test-standard-files" / "Informationsmodell-modell-standard.json"
        #self.imtestjsonpath = Path("/Users/stb/Library/Mobile Documents/com~apple~CloudDocs/Arbeit/dataspot/access/Sandbox Stefan/exports/Sandbox Stefan-standard.json")
        CreateSchemaExcel(standardjson=self.imtestjsonpath,
                          lang="en").writeexcel(outfilepath=self.mydebugpath / (self.imtestjsonpath.stem+".xlsx"))
        return

    def test_localfile(self):
        inpath  = Path(__file__).parent.parent.parent.parent / "localtestmodels" / "CHEM-X-DMP" / "MVP-DMP-standard.json"

        excel= CreateSchemaExcel(standardjson=inpath,
                          lang="en")
        createexcel(jsonfilepath=inpath,
                                  outfilepath=self.mydebugpath / (inpath.stem+".xlsx")
                                  )


if __name__ == '__main__':
    unittest.main()
