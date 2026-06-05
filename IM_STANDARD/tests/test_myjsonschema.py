import unittest
from IM_STANDARD import JsonSchema, JsonElement


class MyTestCase(unittest.TestCase):
    def test_additionalprops(self):
        schema = JsonSchema()
        return

    def test_idschema(self):
        schema = JsonSchema(model={"ModelInfo": JsonElement(elemtype="ModelInfo",
                                                            modelname="IM-standard",
                                                            modeltype="Information Model",
                                                            mainlanguage="en",
                                                            modelversion="1.1",
                                                            targetenvironment="Testtarget"),
                                   "Categories":[JsonElement().categoryjson(categorytype="ENTITY",
                                                                            elementid="CATG12",
                                                                            name="mycatg",
                                                                            categoryid="CATG11"),
                                                 JsonElement().categoryjson(categorytype="ENTITY",
                                                                            elementid="CATG11",
                                                                            name="mycatg")
                                                 ],
                                   "Entities":[JsonElement().entityjson(elementid="ENTI12",name="myEntity",
                                                                        categoryid="CATG11")
        ]
                                   # "Domains":
                                   #     [
                                   #         {
                                   #             "elementid": "DOMA65",
                                   #             "name": {
                                   #                 "de": "Document format",
                                   #                 "en": "Document format"
                                   #             },
                                   #             "domaintype": "LOVDomain",
                                   #             "values": [{
                                   #                 "value": "FALSE",
                                   #                 "displayvalue": "unwahr",
                                   #                 "sortorder": 1
                                   #             }
                                   #             ]
                                   #         },
                                   #         {
                                   #             "elementid": "DOMA63",
                                   #             "name": {
                                   #                 "de": "Dockingkposition",
                                   #                 "en": "Dockingkposition"
                                   #             },
                                   #             "domaintype": "GroupDomain",
                                   #             "elements": [
                                   #                 {
                                   #                     "elementid": "ATTR100062",
                                   #                     "name": "edge",
                                   #                     "mandatory": False,
                                   #                     "parentid": "DOMA123",
                                   #                     "description": "edge of rectangualr NESW",
                                   #                     "domainid": "DOMA28"
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
