import unittest
from pathlib import Path

import json
import pytest

from IM_STANDARD import model2json, jsonvalidation, DMStandardJsonModel
from INTERFACES.EXCEL import StandardExcel, StandardDataExcel, StandardSchemaExcel, CreateDataExcel


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

    def test_standard(self):
        self.astronomietestexcelpath = self.testfilepath / "datafiles" / "Astronomie.xlsx"
        myexcel = StandardExcel(self.astronomietestexcelpath)
        with self.assertRaises(Exception):
            myexcel.analyzeExcel()
        return

    def test_astronomie2standard(self):
        self.astronomietestexcelpath = self.testfilepath / "datafiles" / "Astronomie.xlsx"
        myexcel = StandardDataExcel(self.astronomietestexcelpath)
        myexcel.analyzeExcel(headerline=2)
        return

    def test_dpp1(self):
        self.infilepath = self.testfilepath / "schemafiles" / "Chem-X DMP Model.xlsx"
        myexcel = StandardSchemaExcel(self.infilepath)
        myexcel.analyzeExcel(headerline=1,
                             Description="Comment",
                             Examples="Example")
        purejson = model2json(myexcel.model.jsonschemamodel)
        outfilepath=Path(self.mydebugpath) / (self.infilepath.stem + "-standard.json")
        with open(outfilepath, "w") as outfile:
            json.dump(purejson, outfile, indent=2)
            self.assertEqual(jsonvalidation.validateschema(instance=purejson,
                                                           schemafile=DMStandardJsonModel.DMDEFINITIONFILEPATH,
                                                           schemaonly=False), [])
            print(f'Json written : {outfilepath}')

        dataexcel = CreateDataExcel(standardjson=outfilepath)
        dataexcel.writeemptyexcel(outfilepath=Path(self.mydebugpath) / (self.infilepath.stem + "-data.xlsx"),
                                  withexamples=True)
        print(f'Excelfile written : {Path(self.mydebugpath) / (self.infilepath.stem + "-data.xlsx")}')

        return

    def test_dpp2(self):
        self.infilepath = self.testfilepath / "schemafiles" / "DMP Data Catalog.xlsx"
        myexcel = StandardSchemaExcel(self.infilepath)
        myexcel.analyzeExcel(headerline=1,
                             TechnicalName="Technical name (camelCase)",
                             DataType="ValeDataType",
                             Restriction="Constraint",
                             Examples="Example")
        purejson = model2json(myexcel.model.jsonschemamodel)
        with open(Path(self.mydebugpath) / (self.infilepath.stem + "-standard.json"), "w") as outfile:
            json.dump(purejson, outfile, indent=2)
            jsonvalidation.validateschema(instance=purejson,
                                          schemafile=DMStandardJsonModel.DMDEFINITIONFILEPATH,
                                          schemaonly=False)
            print (f"jsonfile written : {Path(self.mydebugpath) / (self.infilepath.stem + '-standard.json')}")
        return

    def test_write_dataexel(self):
        self.infilepath = self.testfilepath / "schemafiles" / "DMP Data Catalog.xlsx"
        myexcel = StandardSchemaExcel(self.infilepath)
        myexcel.analyzeExcel(headerline=1,
                             TechnicalName="Technical name (camelCase)",
                             DataType="ValeDataType",
                             Restriction="Constraint",
                             Examples="Example")
        purejson = model2json(myexcel.model.jsonschemamodel)
        dataexcel = CreateDataExcel(standardjson=purejson)
        outfilepath=Path(self.mydebugpath) / (self.infilepath.stem + "-data.xlsx")
        dataexcel.writeemptyexcel(outfilepath=outfilepath,
                                  withexamples=True)

        dataexcelread=StandardDataExcel(filespec=outfilepath)
        dataexcelread.analyzeExcel(headerline=1)
        return

    def test_analyze_dataexcel(self):
        self.astronomietestexcelpath = self.testfilepath / "datafiles" / "Astronomie.xlsx"
        #lies mein dataexcel
        print()
        standardexcel=StandardDataExcel(filespec=self.astronomietestexcelpath)
        standardexcel.analyzeExcel(headerline=2)
        purejson = model2json(standardexcel.model.jsonschemamodel)
        outfilepath = Path(self.mydebugpath) / (self.astronomietestexcelpath.stem + "-schema.json")
        print (f"Written schema example excel to  {outfilepath}")
        with open(outfilepath,"w") as outfile:
            json.dump(purejson,outfile,indent=2)
        jsonvalidation.validateschema(instance=purejson,
                                          schemafile=DMStandardJsonModel.DMDEFINITIONFILEPATH,
                                          schemaonly=False)


        dataexcel = CreateDataExcel(standardjson=purejson)
        outfilepath=Path(self.mydebugpath) / (self.astronomietestexcelpath.stem + "-data.xlsx")
        dataexcel.writeemptyexcel(outfilepath=outfilepath,
                                  withexamples=True)
        print (f"Written data example excel to  {outfilepath}")
        return


    def test_write_dataexcel2(self):
        self.astronomietestjsonpath = self.testfilepath / "datafiles" / "Astronomie-schema.json"
        with open(self.astronomietestjsonpath) as infile:
            injson=json.load(infile)
        dataexcel = CreateDataExcel(standardjson=injson)
        outfilepath = Path(self.mydebugpath) / (self.astronomietestjsonpath.stem + "-data.xlsx")
        dataexcel.writeemptyexcel(outfilepath=outfilepath,
                                  withexamples=True)
        print(f"Written data example excel to  {outfilepath}")

        inpath = Path(self.mydebugpath) / "DMP-standard.json"
        if inpath.exists():

            with open(inpath) as infile:
                injson=json.load(infile)
            dataexcel = CreateDataExcel(standardjson=injson)
            outfilepath = Path(self.mydebugpath) / (inpath.stem + "-data.xlsx")
            dataexcel.writeemptyexcel(outfilepath=outfilepath,
                                      withexamples=True)
            print(f"Written data example excel to  {outfilepath}")
        return


if __name__ == '__main__':
    unittest.main()
