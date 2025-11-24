import json
import unittest

from IM_STANDARD import jsonvalidation,validateschema,StandardJsonModel


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

    def test_validateschema(self):
        testinstance=StandardJsonModel.SCHEMADEFPATH / "testmodels" / "Attribute" / "valid"/ "maximum.json"
        testinstanceinvalid=StandardJsonModel.SCHEMADEFPATH / "testmodels" / "Attribute" / "invalid"/ "noparent.json"
        attributeschemapath=StandardJsonModel.SCHEMADEFPATH / "Attribute-schema.json"
        self.assertEqual(0,len(validateschema(instance=testinstance,
                                       schemafile=attributeschemapath,
                                       verbose=False,
                                       schemaonly=True))
                        )

        with open(testinstance) as infile:
            schema=json.load(infile)
        self.assertEqual(0,len(validateschema(instance=schema,
                                       schemafile=attributeschemapath,
                                       verbose=False,
                                       schemaonly=True))
                        )

        self.assertNotEqual(0,
                        len(validateschema(instance=testinstanceinvalid,
                                       schemafile=attributeschemapath,
                                       verbose=False,
                                       schemaonly=True))
                        )

        self.assertEqual(0,len(validateschema(instance=testinstance,
                                       schemafile=attributeschemapath,
                                       verbose=False,
                                       schemaonly=False))
                        )
        self.assertNotEqual(0,len(validateschema(instance=testinstanceinvalid,
                                       schemafile=attributeschemapath,
                                       verbose=False,
                                       schemaonly=False))
                        )


if __name__ == '__main__':
    unittest.main()
