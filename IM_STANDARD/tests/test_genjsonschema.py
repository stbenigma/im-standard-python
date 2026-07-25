import json
import logging
import unittest
from pathlib import Path

import pytest

from IM_STANDARD import generatejsonschema, Json2JsonSchema


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

    def test_internas1(self):
        #(non)null dictionary entries
        self.caplog.set_level(logging.WARNING)
        testdict = {'a': 1,
                    'b': False,
                    'c': 0,
                    'd': "x",
                    'e': {'x': 1},
                    'f': [0],
                    'null0': [],  # vanish
                    'null1': {},  # vanish
                    'null2': None,  # vanish
                    'null3': ""  # vanish
                    }
        notnulltestdict = {'a': 1,
                           'b': False,
                           'c': 0,
                           'd': "x",
                           'e': {'x': 1},
                           'f': [0]}
        self.assertDictEqual(testdict,
                             Json2JsonSchema._conddict(condition=lambda x: True,
                                                       **testdict))
        self.assertDictEqual({},
                             Json2JsonSchema._conddict(condition=lambda x: False,
                                                       **testdict))
        self.assertDictEqual(Json2JsonSchema._fulldict(**testdict),
                             Json2JsonSchema._conddict(**testdict))
        self.assertDictEqual(testdict,
                             Json2JsonSchema._fulldict(**testdict))
        self.assertDictEqual(notnulltestdict,
                             Json2JsonSchema._notnulldict(**testdict))

        #jsonobjectmgt
        testjson= {"ModelInfo":{},
                   "Entities":[]}
        self.caplog.clear()
        struct=Json2JsonSchema(jsonstruct=testjson)
        entiid=struct.getobject(objid="ENTI1")
        self.assertTrue(self.caplog.messages[0].startswith("Object (id=ENTI1) not"))
        entiid=struct.getobject(objid="XXXX1")
        self.assertTrue(self.caplog.messages[1].startswith("Object (id=XXXX1) not"))

        self.caplog.clear()
        testjson["Entities"].append({"elementId":"ENTI1"})
        entiid=struct.getobject(objid="ENTI1")
        self.assertEqual(0,len(self.caplog.messages))
        entiid=struct.getobject(objid="ENTI11")
        self.assertNotEqual(0,len(self.caplog.messages))
        entiid=struct.getobject(objid="RELA1")
        self.assertTrue(self.caplog.messages[-1].startswith("Object (id=RELA1) not"))

        #getmlvalue
        self.caplog.clear()
        testjson["ModelInfo"]["languages"]=["fr","de","en"]
        testjson["ModelInfo"]["mainLanguage"]="de"
        struct=Json2JsonSchema(jsonstruct=testjson)

        self.assertIsNone(struct.getmlvalue(struct={}))
        self.assertIsNone(struct.getmlvalue(struct=None))
        self.assertEqual("abcd",struct.getmlvalue(struct="abcd"))
        self.assertEqual("D",struct.getmlvalue(struct={"de":"D","en":"E","fr":"F"}))
        #simulate different language
        struct.language="fr"
        self.assertEqual("F", struct.getmlvalue(struct={"de": "D", "en": "E", "fr": "F"}))
        struct.language="xx" #fallback to main
        self.assertEqual("D", struct.getmlvalue(struct={"en": "E","de": "D", "fr": "F"}))
        struct.language="xx" #fallback to first entry
        self.assertEqual("E", struct.getmlvalue(struct={"en": "E","ch": "D", "fr": "F"}))
        #print (self.caplog.messages[0])
        self.assertTrue(self.caplog.messages[-1].startswith("Languages 'xx' "))
        return

    def test_internas2(self):
        #additionalprops
        self.caplog.clear()
        self.assertIsNone(Json2JsonSchema.getadditionalprop(struct={},
                                          propname="xx"))
        self.assertIsNone(Json2JsonSchema.getadditionalprop(struct={"abc":1,
                                                                    "additionalProps":{}},
                                          propname="xx"))
        self.assertIsNone(Json2JsonSchema.getadditionalprop(struct={"abc":1,
                                                                    "additionalProps":{'abc':1}},
                                          propname="xx"))
        self.assertEqual(99,Json2JsonSchema.getadditionalprop(struct={"abc":1,
                                                                    "additionalProps":{'abc':1,'xx':99}},
                                          propname="xx"))

        return

    def test_generatefunction_1(self):
        generatejsonschema(entity="x")
        self.assertTrue("No input given" in self.caplog.text)

        self.caplog.clear()
        testjs = {}

        return

    def test_generatejson_2(self):
        minimalmodel = {
            "ModelInfo": {
                "modelName": "Testmodel",
                "targetEnvironment": "information model Test",
                "modelVersion": "0.1",
                "modelType": "Information model"
            }
        }
        self.skipTest(f"minimalmodel not yet for entity not yet implemented")

        jsschemas, jsexamples = generatejsonschema(jsonstruct=minimalmodel,
                                                   _schema="https:sbb.ch",
                                                   entity="Sternsystem"
                                                   )
        self.assertEqual(jsschemas[0][1].get("$schema"), "https:sbb.ch")
        self.assertEqual(jsschemas[0][1].get("urn"), "urn:???:Testmodel:0.1#Testmodel")
        with open(self.downloadpath / ("Testmodel" + "-schema.json"), "w") as outfile:
            json.dump(jsschemas[0][1], outfile, indent=2)

    def test_foryou(self):
        testfile = self.standardtestilfespath / "dataspotforyoumodels-standard.json"
        if not testfile.is_file():
            self.skipTest(f"testfile not found {str(testfile)}")
        self.skipTest(f"collection not yet implemented")

        topelement = "Organisation"
        jsschemas, jsexamples = generatejsonschema(jsonfilepath=testfile,
                                                   _schema="https://json-schema.org/draft/2020-12/schema",
                                                   nid="4U",
                                                   collection=topelement,
                                                   entitiy=None,
                                                   domain=None,
                                                   outfilepath=self.downloadpath
                                                   )

        self.caplog.clear()
        self.caplog.set_level(logging.WARNING)
        jsschemas, jsexamples = generatejsonschema(jsonfilepath=testfile,
                                                   _schema="https://json-schema.org/draft/2020-12/schema",
                                                   nid="4U",
                                                   outfilepath=self.downloadpath
                                                   )
        print("\n".join(set(self.caplog.messages)))
        return

    def test_imstandard(self):
        testfile = self.standardtestilfespath / "informationsmodell-modell-standard.json"
        if not testfile.is_file():
            self.skipTest(f"testfile not found {str(testfile)}")
        self.skipTest(f"full model not yet implemented")

        topelement = "InformationModel"
        jsschemas, jsexamples = generatejsonschema(jsonfilepath=testfile,
                                                   _schema="https://json-schema.org/draft/2020-12/schema",
                                                   nid="InformationModel",
                                                   collection=None,
                                                   entitie=None,
                                                   domain=None,
                                                   outfilepath=self.downloadpath
                                                   )
        print("\n".join([record.message for record in self.caplog.records if record.levelno == logging.WARNING]))
        return

    def test_schwipsti(self):
        testfile = self.standardtestilfespath / "Schwipsti-standard.json"
        if not testfile.is_file():
            self.skipTest(f"testfile not found {str(testfile)}")
        self.skipTest(f"fullmodel not yet implemented")

        topelement = "Schwipsti"
        jsschemas, jsexamples = generatejsonschema(jsonfilepath=testfile,
                                                   _schema="https://json-schema.org/draft/2020-12/schema",
                                                   nid="Schwipsti",
                                                   outfilepath=self.downloadpath
                                                   )
        print("\n".join([record.message for record in self.caplog.records if record.levelno == logging.WARNING]))
        return

    def test_astronomy(self):
        testfile = self.standardtestilfespath / "astronomie-assets-standard.json"
        testfile = Path(
            "/Users/stb/Documents/Projekte/IM-Standard/python-Projekt/Information-model-standard/Example models/Astronomie/astronomie-information-model.json")
        if not testfile.is_file():
            self.skipTest(f"testfile not found {str(testfile)}")
        self.skipTest(f"collection not yet implemented")
        jsschemas, jsexamples = generatejsonschema(jsonfilepath=testfile,
                                                   _schema="https://json-schema.org/draft/2020-12/schema",
                                                   nid="Astronomy",
                                                   outfilepath=self.downloadpath,
                                                   collection="Sternsystem",
                                                   samplespath=self.downloadpath
                                                   )

        self.assertEqual("https://json-schema.org/draft/2020-12/schema", jsschemas[0][1].get("$schema"))
        self.assertEqual("urn:Astronomy:Astronomie Beispiel:0.9#Astronomie Beispiel", jsschemas[0][1].get("urn"))
        self.caplog.set_level(logging.WARNING)
        print()
        print("\n".join([t for t in self.caplog.messages]))

        return

    def test_astronomy_assets(self):
        testfile = self.standardtestilfespath / "astronomie-assets-standard.json"
        jsschemas, jsexamples = generatejsonschema(jsonfilepath=testfile,
                                                   _schema="https://json-schema.org/draft/2020-12/schema",
                                                   nid="Astronomy-asset",
                                                   entity="Missionsdoku",
                                                   singlefile=True,
                                                   outfilepath=self.downloadpath / "astro1",
                                                   samplespath=self.downloadpath / "samples"
                                                   )



        jsschemas, jsexamples = generatejsonschema(jsonfilepath=testfile,
                                                   _schema="https://json-schema.org/draft/2020-12/schema",
                                                   nid="Astronomy-asset",
                                                   entity="Mond Datenblatt",
                                                   singlefile=True,
                                                   outfilepath=self.downloadpath / "astro2",
                                                   samplespath=self.downloadpath/ "samples"
                                                   )
        return

    def test_localfiles(self):
        testfile = Path(__file__).parent.parent.parent / \
                   "localtestmodels" / \
                   "CHEM-X-DMP" / \
                   "DMP-standard.json"
        testfile = Path("/Users/stb/Library/Mobile Documents/com~apple~CloudDocs/Arbeit/dataspot/access/chem-x/ds2json") / "DMP-Model-standard.json"
        if not testfile.exists(): self.skipTest(f"testfile not found")
        topelement = "DMP"  # Header"
        jsschemas, jsexamples = generatejsonschema(jsonfilepath=testfile,
                                                   _schema="https://json-schema.org/draft/2020-12/schema",
                                                   nid="chem-x",
                                                   # collections=["MVP DMP"],
                                                   collection=None,
                                                   entity=topelement,
                                                   singlefile=False,
                                                   outfilepath=self.downloadpath,
                                                   samplespath=self.downloadpath / "samples"
                                                   )
        # print("\n".join([record.message for record in self.caplog.records if record.levelno == logging.WARNING]))
        # self.assertEqual("https://json-schema.org/draft/2020-12/schema", jsschemas[0][1].get("$schema"))
        # self.assertEqual("urn:chem-x:materialDeclaration:0.9#materialDeclaration", jsschemas[0][1].get("urn"), )

        return

    def test_localfiles3(self):
        testfile = Path(__file__).parent.parent.parent / \
                   "localtestmodels" / \
                   "CHEM-X-IM" / \
                   "CHEM-X-IM-standard.json"
        if not testfile.exists(): self.skipTest(f"testfile not found")
        if not testfile.is_file():
            self.skipTest(f"testfile not found {str(testfile)}")
        self.skipTest(f"collection not yet implemented")

        topelement = "Chemistry"
        jsschemas, jsexamples = generatejsonschema(jsonfilepath=testfile,
                                                   _schema="https://json-schema.org/draft/2020-12/schema",
                                                   nid="chem-x",
                                                   # collections=["MVP DMP"],
                                                   collection=topelement,
                                                   entity=None,
                                                   domain=None
                                                   )
        print("\n".join([record.message for record in self.caplog.records if record.levelno == logging.WARNING]))
        self.assertEqual("https://json-schema.org/draft/2020-12/schema", jsschemas[0][1].get("$schema"))
        self.assertEqual("urn:chem-x:Chemistry:0.9#Chemistry", jsschemas[0][1].get("urn"), )
        with open(self.downloadpath / (topelement + "-schema.json"), "w") as outfile:
            json.dump(jsschemas[0][1], outfile, indent=2)

        topelement = "Substance"
        jsschemas, jsexamples = generatejsonschema(jsonfilepath=testfile,
                                                   _schema="https://json-schema.org/draft/2020-12/schema",
                                                   nid="chem-x",
                                                   entity=topelement
                                                   )
        print("\n".join([record.message for record in self.caplog.records if record.levelno == logging.WARNING]))
        with open(self.downloadpath / (topelement + "-schema.json"), "w") as outfile:
            json.dump(jsschemas[0][1], outfile, indent=2)

        topelement = "Substance group"
        topelement = "Mixture substance"
        jsschemas, jsexamples = generatejsonschema(jsonfilepath=testfile,
                                                   _schema="https://json-schema.org/draft/2020-12/schema",
                                                   nid="chem-x",
                                                   # collections=["MVP DMP"],
                                                   collection=None,
                                                   entity=topelement,
                                                   domain=None
                                                   )
        print("\n".join([record.message for record in self.caplog.records if record.levelno == logging.WARNING]))
        with open(self.downloadpath / (topelement + "-schema.json"), "w") as outfile:
            json.dump(jsschemas[0][1], outfile, indent=2)


if __name__ == '__main__':
    unittest.main()
