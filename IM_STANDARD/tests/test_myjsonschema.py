import unittest
from IM_STANDARD import JsonSchema, JsonElement


class MyTestCase(unittest.TestCase):
    def test_additionalprops(self):
        schema = JsonSchema()
        return

    def test_idschema(self):
        schema = JsonSchema(model={"ModelInfo": JsonElement(elemtype="ModelInfo",
                                                            modelname="IM-standard",
                                                            modeltype="Information model",
                                                            mainlanguage="en",
                                                            modelversion="1.1",
                                                            targetEnvironment="Testtarget"),
                                   "Categories":[JsonElement().categoryjson(categorytype="ENTITY",
                                                                            elementId="CATG12",
                                                                            name="mycatg",
                                                                            categoryId="CATG11"),
                                                 JsonElement().categoryjson(categorytype="ENTITY",
                                                                            elementId="CATG11",
                                                                            name="mycatg")
                                                 ],
                                   "Entities":[JsonElement().entityjson(elementId="ENTI12",name="myEntity",
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
