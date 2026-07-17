import unittest
import pytest
import json
from pathlib import Path

from INTERFACES.EXCEL import StandardDataExcel
from INTERFACES.DATASPOT.datasets import generatedatasetjson



class MyTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temppath = Path(tmp_path)

    def setUp(self) -> None:

        self.exceltestfilepath = Path(__file__).parent.parent.parent.parent \
                              / "EXCEL" / "tests" / "testfiles"

        self.mydebugpath = (Path.home() / "Downloads") if (Path.home() / "Downloads").exists() else self.temppath
        return

    def test_astroexceltojson(self):
        self.astronomietestexcelpath = self.exceltestfilepath / "datafiles" / "Astronomie.xlsx"
        myexcel = StandardDataExcel(self.astronomietestexcelpath)
        myexcel.analyzeExcel(headerline=2)

        outjson=generatedatasetjson(jsonschema=myexcel.model,
                                    domainmodel="/templ Domain model/")
        outfilepath=Path(self.mydebugpath) / (self.astronomietestexcelpath.stem + "-dataset.json")
        with open(outfilepath, "w") as outfile:
            json.dump(outjson, outfile, indent=2)
            print (f"json written to {str(outfilepath)}")
        return

if __name__ == '__main__':
    unittest.main()
