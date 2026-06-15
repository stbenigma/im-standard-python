import json
import unittest

from IM_STANDARD import jsonvalidation


class MyTestCase(unittest.TestCase):
    def test_pureschema(self):
        jsonschema = {
            "$id": "Attribute-schema.json",
            "$schema": "https://json-schema.org/draft-07/schema",
            "description": ""
        }
        jsonvalidation.validate_json_as_schema(schema=jsonschema)

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
            jsonvalidation.validate_json_as_schema(schema=jsonschema)

    def test_removekey(self):
        removekey = "abc"
        obj = {"key1": {removekey: [0, 1, 2],
                        "def": [{removekey: 99},
                                {"xyz": removekey}]
                        },
               removekey: 1}
        newobj = jsonvalidation.remove_key_from_json(obj, "abc")
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
        newobj = jsonvalidation.remove_key_from_json(obj, "???")
        self.assertDictEqual(newobj,obj)

        return


if __name__ == '__main__':
    unittest.main()
