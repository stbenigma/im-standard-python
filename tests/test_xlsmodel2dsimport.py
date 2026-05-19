import json
import unittest
from pathlib import Path

import pytest

from IM_STANDARD import model2json
from INTERFACES.DATASPOT import json2dataspot
from INTERFACES.DATASPOT.datasets import generatedatasetjson
from INTERFACES.EXCEL import StandardDataExcel, CreateDataExcel


class MyTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temppath = Path(tmp_path)

    def setUp(self) -> None:
        self.mydebugpath = (Path.home() / "Downloads") if (Path.home() / "Downloads").exists() else self.temppath
        return


    def test_excel2dsjson(self):
        localfile = self.mydebugpath / "zh cust daten.xlsx"
        myexcel = StandardDataExcel(localfile)
        myexcel.analyzeExcel(headerline=1)

        outjson = generatedatasetjson(jsonschema=myexcel.model,
                                      domainmodel="/Wertebereiche/Generische Wertebereiche")
        outfilepath = Path(self.mydebugpath) / (localfile.stem + "-dataset.json")
        with open(outfilepath, "w") as outfile:
            json.dump(outjson, outfile, indent=2)
        print (f"Written file {str(outfilepath)}")

        localfile = self.mydebugpath / "zh cust model.xlsx"
        myexcel = StandardDataExcel(localfile)
        myexcel.analyzeExcel(headerline=3)

        outjson = generatedatasetjson(jsonschema=myexcel.model,
                                      domainmodel="/Wertebereiche/Generische Wertebereiche")
        outfilepath = Path(self.mydebugpath) / (localfile.stem + "-dataset.json")
        with open(outfilepath, "w") as outfile:
            json.dump(outjson, outfile, indent=2)
        print (f"Written file {str(outfilepath)}")


        return

    def test_localfile_DM(self):

        localfile = self.mydebugpath / "zh cust daten.xlsx"
        # localfile = self.mydebugpath / "Astronomie.xlsx"

        if not localfile.is_file():
            self.skipTest(f"file not found {str(localfile)}")

        standardexcel = StandardDataExcel(filespec=localfile)
        standardexcel.analyzeExcel(headerline=2)
        purejson = model2json(standardexcel.model.jsonschemamodel)
        outfilepath = Path(self.mydebugpath) / (localfile.stem + "-dsimport.json")
        print(f"Written schema example excel to  {outfilepath}")
        with open(outfilepath, "w") as outfile:
            json.dump(purejson, outfile, indent=2)

        dataexcel = CreateDataExcel(standardjson=purejson)
        outfilepath = Path(self.mydebugpath) / (localfile.stem + "-data_regenerated.xlsx")
        dataexcel.writeemptyexcel(outfilepath=outfilepath,
                                  withexamples=True)
        print(f"Written data example excel to  {outfilepath}")

        localfile = self.mydebugpath / "zu cust-dsimport.json"
        if not localfile.is_file():
            self.skipTest(f"file not found {str(localfile)}")

        json2dataspot(injson=localfile,
                      outpath=self.mydebugpath,
                      dmname="test zh cust DM",
                      refdomainsname="test zh cust ref model",
                      domainsname="test zh cust domain model",
                      systemsname="test zh cust systems model"
                      )
        return


if __name__ == '__main__':
    unittest.main()
