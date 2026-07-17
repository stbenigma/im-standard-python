import json
import logging
import unittest
from pathlib import Path

import pytest

from IM_STANDARD import generatejsonschema


class MyTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.capsys = capsys
        self.caplog = caplog
        logging.basicConfig(level=logging.ERROR, force=True)
        self.caplog.set_level(logging.ERROR)
        if (Path.home() / "Downloads").exists():
            self.downloadpath = Path.home() / "Downloads"
        else:
            self.downloadpath = tmp_path / "Downloads"

        self.standardtestilfespath = Path(__file__).parent / \
                                         "json-test-standard-files"

        return

    def test_generatefunction_1(self):
        generatejsonschema()
        self.assertTrue("No input given" in self.caplog.text)

        self.caplog.clear()
        jsschema,jsexample = generatejsonschema(jsonstruct=dict())
        self.assertFalse("No input given" in self.caplog.text)

        self.caplog.clear()
        testjs = {}
        jsschema,jsexample = generatejsonschema(jsonstruct={"a": 123, 55: "abc"})
        self.assertFalse("No input given" in self.caplog.text)
        self.assertTrue("'ModelInfo' not found in structure" in self.caplog.text)
        self.assertEqual("urn:???:???:0.0#???",jsschema.get("urn"))

        self.caplog.clear()

        with self.assertRaises(FileNotFoundError) as exp:
            generatejsonschema(jsonfilepath="gag.json")

        return

    def test_generatejson_2(self):
        minimalmodel = {
            "ModelInfo": {
                "modelName": "Testmodel",
                "targetEnvironment": "information model Test",
                "modelVersion": "0.1",
                "modelType": "Information Model"
            }
        }

        jsschema,jsexample = generatejsonschema(jsonstruct=minimalmodel,
                                      _schema="https:sbb.ch",
                                      collection="Sternsystem"
                                      )
        self.assertEqual(jsschema.get("$schema"), "https:sbb.ch")
        self.assertEqual(jsschema.get("urn"), "urn:???:Testmodel:0.1#Testmodel")
        with open(self.downloadpath / ("Testmodel" + "-schema.json"), "w") as outfile:
            json.dump(jsschema, outfile, indent=2)

    def test_foryou(self):
        testfile = self.standardtestilfespath / "dataspotforyoumodels-standard.json"

        topelement = "Organisation"
        jsschema,jsexample = generatejsonschema(jsonfilepath=testfile,
                                      _schema="https://json-schema.org/draft/2020-12/schema",
                                      nid="4U",
                                      collection=topelement,
                                      entitiy=None,
                                      domain=None,
                                      outfilepath=self.downloadpath / (topelement + "-schema.json")
                                      )

        self.caplog.clear()
        self.caplog.set_level(logging.WARNING)
        jsschema,jsexample = generatejsonschema(jsonfilepath=testfile,
                                      _schema="https://json-schema.org/draft/2020-12/schema",
                                      nid="4U",
                                      outfilepath=self.downloadpath / ("full4u" + "-schema.json")
                                      )
        print("\n".join(set(self.caplog.messages)))
        return

    def test_imstandard(self):
        testfile = self.standardtestilfespath / "informationsmodell-modell-standard.json"

        topelement = "InformationModel"
        jsschema,jsexample = generatejsonschema(jsonfilepath=testfile,
                                      _schema="https://json-schema.org/draft/2020-12/schema",
                                      nid="InformationModel",
                                      collection=None,
                                      entitie=None,
                                      domain=None,
                                      outfilepath=self.downloadpath / (topelement + "-schema.json")
                                      )
        print("\n".join([record.message for record in self.caplog.records if record.levelno == logging.WARNING]))
        return

    def test_schwipsti(self):
        testfile = self.standardtestilfespath / "Schwipsti-standard.json"

        topelement = "Schwipsti"
        jsschema,jsexample = generatejsonschema(jsonfilepath=testfile,
                                      _schema="https://json-schema.org/draft/2020-12/schema",
                                      nid="Schwipsti",
                                      outfilepath=self.downloadpath / (topelement + "-schema.json")
                                      )
        print("\n".join([record.message for record in self.caplog.records if record.levelno == logging.WARNING]))
        return

    def test_astronomy(self):
        testfile =  self.standardtestilfespath/ "astronomie-assets-standard.json"
        testfile=Path("/Users/stb/Documents/Projekte/IM-Standard/python-Projekt/Information-model-standard/Example models/Astronomie/astronomie-information-model.json")
        jsschema,jsexample = generatejsonschema(jsonfilepath=testfile,
                                      _schema="https:stefanberner.ch",
                                      nid="Astronomy",
                                      #collection="Sternsystem",
                                    examplepath=Path("/Users/stb/Documents/Projekte/IM-Standard/python-Projekt/Information-model-standard/Example models/Astronomie/astronomie-information-model_sample.json")
                                      )

        self.assertEqual("https:stefanberner.ch", jsschema.get("$schema"))
        self.assertEqual("urn:Astronomy:Astronomie Beispiel:0.9#Astronomie Beispiel", jsschema.get("urn"))
        self.caplog.set_level(logging.WARNING)
        print()
        print("\n".join([t for t in self.caplog.messages]))

        return

    def test_astronomy_assets(self):
        testfile =  self.standardtestilfespath/ "astronomie-assets-standard.json"
        jsschema,jsexample = generatejsonschema(jsonfilepath=testfile,
                                      _schema="https:stefanberner.ch",
                                      nid="Astronomy-asset",
                                      entity="Missionsdoku",
                                      outfilepath=self.downloadpath / ("Missionsdoku" + "-schema.json"),
                                      examplepath=self.downloadpath / ("Missionsdoku" + "-sample.json")
                                      )

        jsschema,jsexample = generatejsonschema(jsonfilepath=testfile,
                                      _schema="https:stefanberner.ch",
                                      nid="Astronomy-asset",
                                      entity="Mond Datenblatt",
                                      outfilepath=self.downloadpath / ("Mond_Datenblatt" + "-schema.json"),
                                      examplepath=self.downloadpath / ("Mond_Datenblatt" + "-sample.json")
                                      )
        return

    def test_localfiles(self):
        testfile = Path(__file__).parent.parent.parent / \
                   "localtestmodels" / \
                   "CHEM-X-DMP" / \
                   "CHEM-X-DMP-standard.json"
        if not testfile.exists(): self.skipTest(f"testfile not found")
        topelement = "MaterialDeclaration"
        jsschema,jsexample = generatejsonschema(jsonfilepath=testfile,
                                      _schema="https://json-schema.org/draft/2020-12/schema",
                                      nid="chem-x",
                                      # collections=["MVP DMP"],
                                      collection=topelement,
                                      entity=None,
                                      domain=None
                                      )
        print("\n".join([record.message for record in self.caplog.records if record.levelno == logging.WARNING]))
        self.assertEqual("https://json-schema.org/draft/2020-12/schema", jsschema.get("$schema"))
        self.assertEqual("urn:chem-x:materialDeclaration:0.9#materialDeclaration", jsschema.get("urn"), )
        with open(self.downloadpath / (topelement + "-schema.json"), "w") as outfile:
            json.dump(jsschema, outfile, indent=2)

        topelement = "MVP DMP"
        jsschema,jsexample = generatejsonschema(jsonfilepath=testfile,
                                      _schema="https://json-schema.org/draft/2020-12/schema",
                                      nid="chem-x",
                                      collection=topelement,
                                      entity=None
                                      )
        with open(self.downloadpath / (topelement + "-schema.json"), "w") as outfile:
            json.dump(jsschema, outfile, indent=2)
        with open(self.downloadpath / (topelement + "-sample.json"), "w") as outfile:
            json.dump(jsexample, outfile, indent=2)

        topelement = "MVP-DMP"
        jsschema,jsexample = generatejsonschema(jsonfilepath=testfile,
                                      _schema="https://json-schema.org/draft/2020-12/schema",
                                      nid="chem-x",
                                      entity=topelement,
                                    outfilepath = self.downloadpath / (topelement + "-schema.json"),
                                 examplepath = self.downloadpath / (topelement + "-sample.json")
        )

    def test_localfiles3(self):
        testfile = Path(__file__).parent.parent.parent / \
                   "localtestmodels" / \
                   "CHEM-X-IM" / \
                   "CHEM-X-IM-standard.json"
        if not testfile.exists(): self.skipTest(f"testfile not found")

        topelement = "Chemistry"
        jsschema,jsexample = generatejsonschema(jsonfilepath=testfile,
                                      _schema="https://json-schema.org/draft/2020-12/schema",
                                      nid="chem-x",
                                      # collections=["MVP DMP"],
                                      collection=topelement,
                                      entity=None,
                                      domain=None
                                      )
        print("\n".join([record.message for record in self.caplog.records if record.levelno == logging.WARNING]))
        self.assertEqual("https://json-schema.org/draft/2020-12/schema", jsschema.get("$schema"))
        self.assertEqual("urn:chem-x:Chemistry:0.9#Chemistry", jsschema.get("urn"), )
        with open(self.downloadpath / (topelement + "-schema.json"), "w") as outfile:
            json.dump(jsschema, outfile, indent=2)

        topelement = "Substance"
        jsschema,jsexample = generatejsonschema(jsonfilepath=testfile,
                                      _schema="https://json-schema.org/draft/2020-12/schema",
                                      nid="chem-x",
                                      entity=topelement
                                      )
        print("\n".join([record.message for record in self.caplog.records if record.levelno == logging.WARNING]))
        with open(self.downloadpath / (topelement + "-schema.json"), "w") as outfile:
            json.dump(jsschema, outfile, indent=2)

        topelement = "Substance group"
        topelement = "Mixture substance"
        jsschema,jsexample = generatejsonschema(jsonfilepath=testfile,
                                      _schema="https://json-schema.org/draft/2020-12/schema",
                                      nid="chem-x",
                                      # collections=["MVP DMP"],
                                      collection=None,
                                      entity=topelement,
                                      domain=None
                                      )
        print("\n".join([record.message for record in self.caplog.records if record.levelno == logging.WARNING]))
        with open(self.downloadpath / (topelement + "-schema.json"), "w") as outfile:
            json.dump(jsschema, outfile, indent=2)


if __name__ == '__main__':
    unittest.main()
