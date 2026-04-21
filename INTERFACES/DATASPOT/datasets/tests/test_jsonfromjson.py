import json
import logging
import unittest
from pathlib import Path

import pytest

from INTERFACES.DATASPOT.datasets.json2datasetjson import Json2Dataset, jsondata2dataset,jsondata2dataset_files


class MyTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temppath = Path(tmp_path)

    def setUp(self) -> None:
        self.mydebugpath = (Path.home() / "Downloads") if (Path.home() / "Downloads").exists() else self.temppath
        return

    def _gen1(self, model, jds):
        outjson = jds.generatedatasetjson(jsonschema=model)
        return outjson

    def test_simpledatajsontojson(self):
        json2ds = Json2Dataset(modelpath="/templ dataset model/jsons",
                               modelname="testmodel",
                               domainmodel="/templ Domain model/Standard Wertebereiche/Basis Wertebereiche"
                               )
        outjson = self._gen1(jds=json2ds, model=[])
        self.assertEqual(2, len(outjson))
        self.assertEqual("MANY", outjson[1].get("card"))

        outjson = self._gen1(jds=json2ds, model={})
        self.assertEqual(2, len(outjson))
        self.assertEqual("ONE", outjson[1].get("card"))

        outjson = self._gen1(jds=json2ds,
                             model={"name": "abcd",
                                    "wert": 123,
                                    "wert2": 123.1,
                                    "boolwert": True,
                                    "leerwert": None
                                    }
                             )
        self.assertEqual(7, len(outjson))
        print(json.dumps(outjson, indent=2))

        # outfilepath = Path(self.mydebugpath) / ("testmodel" + "-dataset.json")
        # with open(outfilepath, "w") as outfile:
        #    json.dump(outjson, outfile, indent=2)
        return

    def test_datajsontojson(self):
        json2ds = Json2Dataset(modelpath="/templ dataset model/jsons",
                               modelname="testmodel",
                               domainmodel="/templ Domain model/Standard Wertebereiche/Basis Wertebereiche"
                               )

        outjson = self._gen1(jds=json2ds,
                             model={"name": {"x": "1",
                                             "y": False}
                                    }
                             )
        self.assertEqual(5, len(outjson))
        self.assertEqual("testmodel", outjson[2].get("subsetOf"))

        outjson = self._gen1(jds=json2ds,
                             model={"name": "Multilevel",
                                    "sub1": {"x": "1",
                                             "y": {"von": 123.123,
                                                   "bis": {"subbis1": "subbis1",
                                                           "subbis2": "subbis2"
                                                           }
                                                   }
                                             },
                                    "sub2": {"element1": 9999}
                                    }
                             )
        self.assertEqual(13, len(outjson))
        self.assertEqual("y", outjson[7].get("subsetOf"))

        self.caplog.set_level(logging.WARNING)
        outjson = self._gen1(jds=json2ds,
                             model={"name": "Multilevel",
                                    "repeated": [1, 2, 3, 4],
                                    "sub1": {"x": "1",
                                             "y": {"von": 123.123,
                                                   "sub1": [{"subbis1": "subbis1",
                                                             "subbis2": ["subbis2", "x", "y"]
                                                             }]
                                                   }
                                             },
                                    "sub2rep": [{"element1": 9999},
                                                {"id": [True, False]}],
                                    "sub2": {"x": None,
                                             "y": {"tag": 1,
                                                   "monat": 2,
                                                   "jahr": 1955
                                                   }
                                             }
                                    }
                             )
        self.assertEqual(21, len(outjson))
        self.assertEqual("Composition", outjson[3].get("_type"))
        self.assertEqual("MANY", outjson[3].get("card"))
        self.assertEqual("ONE", outjson[4].get("card"))

        print('\n'.join(self.caplog.messages))
        print(json.dumps(outjson, indent=2))

        outfilepath = Path(self.mydebugpath) / ("testmodel" + "-dataset.json")
        with open(outfilepath, "w") as outfile:
            json.dump(outjson, outfile, indent=2)

        return

    def test_toplevelproc(self):
        outjson = jsondata2dataset(jsonschema={"name": {"x": "1",
                                                        "y": False}
                                               },
                                   datasetmodelpath="/templ dataset model/jsons",
                                   modelname="testmodel",
                                   domainmodelpath="/templ Domain model/Standard Wertebereiche/Basis Wertebereiche")
        self.assertEqual(5, len(outjson))
        self.assertEqual("testmodel", outjson[2].get("subsetOf"))

        testmodel={"name": {"x": "1",
                                          "y": False}
                                 }
        with open(self.temppath / "testjson.json", 'w') as testjson:
            json.dump(testmodel,testjson)
        jsondata2dataset_files(infilepath=str(self.temppath / "testjson.json"),
                         datasetmodelpath="/templ dataset model/jsons",
                         modelname="testmodel",
                         domainmodelpath="/templ Domain model/Standard Wertebereiche/Basis Wertebereiche")
        with open(self.temppath / "testjson.json", 'r') as testinfile:
            model=json.load(testinfile)
        self.assertDictEqual(testmodel,model)
        return

    def test_localfile(self):
        json2ds = Json2Dataset(modelpath="/templ dataset model/jsons",
                               modelname="localfile",
                               domainmodel="/templ Domain model/Standard Wertebereiche/Basis Wertebereiche"
                               )
        with open(Path(self.mydebugpath) / ("Astronomie-schema.json"), 'r') as infile:
            model = json.load(infile)

        outjson = json2ds.generatedatasetjson(jsonschema=model)
        outfilepath = Path(self.mydebugpath) / ("local" + "-dataset.json")
        with open(outfilepath, "w") as outfile:
            json.dump(outjson, outfile, indent=2)
        return

    def test_localfile2(self):
        json2ds = Json2Dataset(modelpath="/templ dataset model/jsons",
                               modelname="battery",
                               domainmodel="/templ Domain model/Standard Wertebereiche/Basis Wertebereiche"
                               )
        with open(Path(self.mydebugpath) / ("Circularity-sample.json"), 'r') as infile:
            model = json.load(infile)

        outjson = json2ds.generatedatasetjson(jsonschema=model)
        outfilepath = Path(self.mydebugpath) / ("Circularity-sample" + "-dataset.json")
        with open(outfilepath, "w") as outfile:
            json.dump(outjson, outfile, indent=2)
        return


if __name__ == '__main__':
    unittest.main()
