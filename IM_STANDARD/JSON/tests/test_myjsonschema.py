import unittest

from IM_STANDARD import JsonSchema, JsonElement, json2timestamp


class MyTestCase(unittest.TestCase):
    def test_additionalprops(self):
        schema = JsonSchema()
        return

    def test_jsontimestamp(self):
        json_data = {
            "unix_seconds": 1784982600,
            "unix_millis": 1784982600000,
            "string_unix": "1784930400",
            "iso_8601": "2026-07-25T14:30:00Z",
            "readable_str": "July 25, 2026 2:30 PM",
            "short_date": "2026-07-25",
            "rfc_2822": "Sat, 25 Jul 2026 14:30:00 GMT"
        }
        print()
        for name, dv in json_data.items():
            print(name, dv)
            dt = json2timestamp(dv)
            if name == "iso_8601":
                self.assertEqual("2026-07-25T14:30:00+00:00", dt)
            elif name == "readable_str":
                self.assertEqual("2026-07-25T14:30:00", dt)
            elif name in ("short_date", "string_unix"):
                self.assertEqual("2026-07-25T00:00:00", dt)
            elif name == "rfc_2822":
                self.assertEqual("2026-07-25T14:30:00+00:00", dt)
            else:
                self.assertEqual("2026-07-25T14:30:00", dt)
        return

    def test_idschema(self):
        schema = JsonSchema(model={"ModelInfo": JsonElement(elemtype="ModelInfo",
                                                            modelname="IM-standard",
                                                            modeltype="Information model",
                                                            mainlanguage="en",
                                                            modelversion="1.1",
                                                            targetEnvironment="Testtarget"),
                                   "Categories": [JsonElement().categoryjson(categorytype="ENTITY",
                                                                             elementId="CATG12",
                                                                             name="mycatg",
                                                                             categoryId="CATG11"),
                                                  JsonElement().categoryjson(categorytype="ENTITY",
                                                                             elementId="CATG11",
                                                                             name="mycatg")
                                                  ],
                                   "Entities": [JsonElement().entityjson(elementId="ENTI12", name="myEntity",
                                                                         categoryId="CATG11")
                                                ]
                                   # "Domains":
                                   #     [
                                   #         {
                                   #             "elementId": "DOMA65",
                                   #             "name": {
                                   #                 "de": "Document format",
                                   #                 "en": "Document format"
                                   #             },
                                   #             "domainType": "LOVDomain",
                                   #             "values": [{
                                   #                 "value": "FALSE",
                                   #                 "displayValue": "unwahr",
                                   #                 "sortOrder": 1
                                   #             }
                                   #             ]
                                   #         },
                                   #         {
                                   #             "elementId": "DOMA63",
                                   #             "name": {
                                   #                 "de": "Dockingkposition",
                                   #                 "en": "Dockingkposition"
                                   #             },
                                   #             "domainType": "GroupDomain",
                                   #             "elements": [
                                   #                 {
                                   #                     "elementId": "ATTR100062",
                                   #                     "name": "edge",
                                   #                     "mandatory": False,
                                   #                     "parentId": "DOMA123",
                                   #                     "description": "edge of rectangualr NESW",
                                   #                     "domainId": "DOMA28"
                                   #                 }
                                   #             ]
                                   #         }
                                   #     ]
                                   })
        model = schema.getjsonmodel()
        self.assertTrue("$id" in model.get("ModelInfo"))
        self.assertTrue(all(["$id" in e for e in model.get("Entities")]))
        self.assertTrue(all(["$id" in e for e in model.get("Categories")]))

        return


if __name__ == '__main__':
    unittest.main()
