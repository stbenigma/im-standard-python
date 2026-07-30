import logging
from pathlib import Path
import unittest
import pytest

import IM_STANDARD.standardmodeljson
from IM_STANDARD.jsonvalidation import ImStandardGithub,validateschema,validate_json_as_schema


class MyTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        caplog.set_level(logging.WARNING)
        self.capsys = capsys
        self.tmp_path=tmp_path
        self.mydebugpath = (Path.home() / "Downloads") if (Path.home() / "Downloads").exists() else self.tmp_path

    def test_pureschema(self):
        jsonschema = {
            "$id": "Attribute-schema.json",
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "description": ""
        }
        validate_json_as_schema(schema=jsonschema)

        # minimum muss eine Zahl sein
        jsonschema = {
            "type": "object",
            "properties": {
                "age": {
                    "type": "integer",
                    "minimum": "0"
                }
            }
        }
        with self.assertRaises(Exception):
            validate_json_as_schema(schema=jsonschema)

    def test_removekey(self):
        removekey = "abc"
        obj = {"key1": {removekey: [0, 1, 2],
                        "def": [{removekey: 99},
                                {"xyz": removekey}]
                        },
               removekey: 1}
        newobj = IM_STANDARD.standardmodeljson.remove_key_from_json(obj, "abc")
        self.assertTrue(removekey not in newobj)
        self.assertTrue(removekey in obj)
        self.assertTrue(removekey in obj["key1"])
        self.assertEqual(removekey, obj["key1"]["def"][1]["xyz"])
        #print(json.dumps(obj, indent=2))
        #print(json.dumps(newobj, indent=2))
        self.assertDictEqual(newobj,
                             {"key1": {"def": [{},
                                               {"xyz": "abc"}
                                               ]
                                       }
                              }
                             )
        newobj = IM_STANDARD.standardmodeljson.remove_key_from_json(obj, "???")
        self.assertDictEqual(newobj,obj)

        return

    def test_githubstandard(self):
        try:
            ImStandardGithub.getimstdschema()
        except AssertionError as exp:
            self.skipTest(f"Github standard-schema-repository not found: {ImStandardGithub.STDSQLBASE}")
        imschema= ImStandardGithub.getimstdschema()
        self.assertIn("$id",imschema)
        self.assertEqual('InformationModel-schema.json',imschema["$id"])
        sqlschema= ImStandardGithub.getsqlschema()
        self.assertIn("entities",sqlschema)

        return

    def test_tarfileread(self):
        tar= ImStandardGithub.getgithubrepoastar()
        with open(self.mydebugpath/"repo_schema"/ "testschema.tar","wb") as outfile:
            outfile.write(tar)

        ImStandardGithub.extracttopath(tar_bytes=tar,outpath=self.mydebugpath/"repo_schema")
        self.assertTrue((self.mydebugpath/"repo_schema"/"Information-model-standard-development"/"Model"/"im-standard-schema" /"InformationModel"/"InformationModel-schema.json").is_file())

        return

    def test_validate_astro(self):
        testfile = Path(__file__).parent / "json-test-standard-files" / "astronomie-assets-standard.json"

        if not testfile.is_file():self.skipTest(f"File not found. {str(testfile)}")

        ImStandardGithub.extracttopath(tar_bytes=ImStandardGithub.getgithubrepoastar(),
                                        outpath=self.tmp_path/"repo")
        errors=validateschema(instance=testfile,schemafile=self.tmp_path/"repo"/"Information-model-standard-development"/"Model"/"im-standard-schema" /"InformationModel"/"InformationModel-schema.json",
                                      schemaonly=True)
        if len(errors)>0:
            print();
            print(errors)
        self.assertEqual(0,len(errors))
        return

if __name__ == '__main__':
    unittest.main()
