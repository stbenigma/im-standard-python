import json
import logging
import unittest

import pytest
from pathlib import Path

from IM_STANDARD import Json2JsonSchema, generatejsonschema


class MyTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = caplog
        self.capsys = caplog
        caplog.set_level(logging.ERROR)
        logging.basicConfig(level=logging.WARNING, force=True)
        if (Path.home() / "Downloads").exists():
            self.downloadpath=Path.home() / "Downloads"
        else:
            self.downloadpath = tmp_path / "Downloads"
        return

    def test_generatefunction_1(self):
        generatejsonschema()
        self.assertTrue("No input given" in self.caplog.text)

        self.caplog.clear()
        jsschema=generatejsonschema(jsonstruct=dict())
        self.assertFalse("No input given" in self.caplog.text)
        self.assertDictEqual(jsschema, Json2JsonSchema.JSONSCHEMATEMPLATE)

        self.caplog.clear()
        testjs = {}
        jsschema=generatejsonschema(jsonstruct={"a": 123, 55: "abc"})
        self.assertFalse("No input given" in self.caplog.text)
        self.assertDictEqual(jsschema, Json2JsonSchema.JSONSCHEMATEMPLATE)
        self.assertTrue("'ModelInfo' not found in structure" in self.caplog.text)
        self.assertEqual(jsschema.get("urn"),"urn:???:????:????#????")

        self.caplog.clear()

        with self.assertRaises(FileNotFoundError) as exp:
            generatejsonschema(jsonfilepath="gag.json")

        return

    def test_generatejson_2(self):
        minimalmodel = {
            "ModelInfo": {
                "modelname": "Testmodel",
                "targetenvironment": "information model Test",
                "modelversion": "0.1",
                "modeltype": "Information model"
            }
        }

        jsschema=generatejsonschema(jsonstruct=minimalmodel,
                                    _schema="https:sbb.ch",
                                    )
        self.assertEqual(jsschema.get("$schema"),"https:sbb.ch")
        self.assertEqual(jsschema.get("urn"),"urn:???:Testmodel:0.1#Testmodel")

    def test_astronomy(self):
        testfile= Path(__file__).parent.parent.parent.parent /\
                  "Information-model-standard" / \
                  "Example models" / \
                  "Astronomie" / \
                  "astronomie-schema-generated.json"
        jsschema=generatejsonschema(jsonfilepath=testfile,
                                    _schema="https:sbb.ch",
                                    )
        self.assertEqual(jsschema.get("$schema"),"https:sbb.ch")
        self.assertEqual(jsschema.get("urn"),"urn:???:Testmodel:0.1#Testmodel")

    def test_localfiles(self):
        testfile= Path(__file__).parent.parent.parent /\
                  "localtestmodels" / \
                  "CHeM-X-DMP"/ \
                  "CHEM-X-DMP-standard.json"
        jsschema=generatejsonschema(jsonfilepath=testfile,
                                    _schema="http://json-schema.org/draft-04/schema",
                                    nid="chem-x",
                                    #collections=["MVP DMP"],
                                    collections=["MaterialDeclaration"],
                                    entities=[],
                                    domains=[]
                                    )
        print ("\n".join([record.message for record in self.caplog.records if record.levelno == logging.WARNING]))
        self.assertEqual("http://json-schema.org/draft-04/schema",jsschema.get("$schema"))
        self.assertEqual("urn:chem-x:materialDeclaration:0.9#materialDeclaration",jsschema.get("urn"),)
        with open(self.downloadpath /(testfile.stem+"-schema.json") ,"w") as outfile:
            json.dump(jsschema,outfile,indent=2)

if __name__ == '__main__':
    unittest.main()
