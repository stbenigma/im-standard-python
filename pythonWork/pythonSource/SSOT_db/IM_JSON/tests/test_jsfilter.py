import difflib
import json
import unittest
from pathlib import Path
from typing import Dict

import pytest

from SSOT_db.IM_OBJECTS import Modelelement
from SSOT_db.IM_JSON import JSModel, FILTEREDJSModel, printJSON
import SSOT_infra.tests.integration as testsrc

simpletestjson = {
    "_imprint_": {
        "Modelversion": "1.7",
        "comment": "Entries ending with + represent denormalized data and are not checked for consistency while reading back",
        "created": "2022-03-07 17:56:32.475788",
        "database": "/Users/stb/Documents/Projekte/FYAYC_intern/fyyccim-tools/pythonWork/pythonSource/testenvironment/testmodels/testmodel-1/DB/testmodel-1.db",
        "hashvalue": 7484003109600946268
    },
    "documents": {
        "DOCU68": {
            "content": None,
            "format+": "png",
            "formatid": "STFO1",
            "name": "f_icon_377_object_handshake",
            "parent": "",
            "reference": "f_icon_377_object_handshake",
            "referencecnt+": "2",
            "references+": [
                "ENTI100",
                "ENTI105"
            ],
            "sourceref": {
                "ODM": [
                    "311DC210-16D2-5982-489E-052929AB265A",
                    "2022-03-07 17:56:32.191950"
                ]
            }
        }
    },
    "entities": {
        "ENTI100": {
            "publstatus": "GTOP",
            "attributes+": [],
            "category": "CATG9",
            "dc": "2022-01-29 11:16:42 UTC",
            "descr": {
                "en": ""
            },
            "diagrams+": [
                "DIAG145"
            ],
            "dm": "2022-03-07 17:56:32.333902",
            "examples": {},
            "exptuple#": None,
            "icon": {
                "reference": None,
                "type": None
            },
            "inarcs+": [],
            "keys+": [],
            "name": {
                "en": "realsubenti_lev2"
            },
            "referencedby": ["DOCU68"],
            "roles+": [],
            "subtypellevel+": 2,
            "subtypes+": [],
            "supertypeentity": "ENTI105",
            "supertypes+": [],
        },
        "ENTI118": {
            "publstatus": "PUBL",
            "attributes+": [
                "ATTR108"
            ],
            "category": "CATG7",
            "dc": "2021-10-05 08:31:18 UTC",
            "descr": {
                "en": "Master entity with 3 children with attributes and classifications\nDisplayed on all zoom levels (0-4)\nsingle attribute Unique key"
            },
            "diagrams+": [
                "DIAG145"
            ],
            "keys+": [],
            "maxzoomlevel": 4,
            "minzoomlevel": 0,
            "name": {
                "en": "Master Entity"
            },
            "prefix": None,
            "publstatus": "PUBL",
            "referencedby": [
                "DOCU68"
            ],
            "relations+": [
                "RELA140",
                "RELA141",
                "RELA142"
            ],
            "roles+": [],
            "subtypellevel+": 0,
            "subtypes+": [
                "ENTI100"
            ],
            "supertypeentity": None,
            "supertypes+": [],
            "synonyms": [],
            "tablesmapped+": {}
        }
    },
    "languages": {
        "en": {
            "iso3": "eng",
            "modellanguage": True,
            "name": "English",
            "replacementlang": None
        }
    },
    "model": {
        "dc": "2021-10-05 08:01:24 UTC",
        "dm": None,
        "language": "en",
        "name": "testmodel-1",
        "type": "logical",
        "uc": "stb",
        "um": None
    },
    "arcs": {},
    "attributes": {},
    "categories": {},
    "columns": {},
    "datatypes": {},
    "diagrams": {},
    "domains": {},
    "keys": {},
    "orgunits": {},
    "physicalunits": {},
    "relations": {},
    "storageformats": {},
    "systems": {},
    "tables": {},
    "userdefprops": {}
}

# We expect stable entity numbers as for now!
MASTER_ENTITY = ('ENTI118', 'Master Entity')
MULTI_UK_ENTITY = ('ENTI93', 'Multi UK Entity')
REALSUBENTI_LEV2 = ('ENTI100', 'realsubenti_lev2')


class MyTestCase(unittest.TestCase):

    verification_entities = [MASTER_ENTITY, MULTI_UK_ENTITY, REALSUBENTI_LEV2]

    @pytest.fixture(autouse=True)
    def init(self, tmp_path):
        self.temp_folder = Path(tmp_path)

    def setUp(self):
        from LOAD_MODELS.LOAD_ODM.tests.test_fillDB import create_testmodel1
        assert self.temp_folder.is_dir(), f"Missing temporary folder {self.temp_folder.resolve()}"
        testmodelname, testdir, dbfilepath = testsrc.testmodel1()
        db = create_testmodel1(testmodelname=testmodelname, testdir=testdir, dbfilepath=dbfilepath, new=True)
        json_model_file = Path(db.parent, db.name.removesuffix('.db') + '.json')
        print(f"Working with clean slate db {json_model_file.resolve()}")
        self.model = JSModel.readfromfile(str(json_model_file))

        with open(json_model_file, 'r') as src:
            model_string = src.read()
            entity_dict = self.model.jsmodel['entities']
            for element in MyTestCase.verification_entities:
                self.ensure_enti_in_model(element[0], model_string, entity_dict, element[1])

        self.emptyfilter = FILTEREDJSModel(pmodel=self.model.jsmodel)
        self.draftfilter = FILTEREDJSModel(ppublstatus=Modelelement.DRAFT, pmodel=self.model.jsmodel)
        self.gtopfilter = FILTEREDJSModel(ppublstatus=Modelelement.GTOP, pmodel=self.model.jsmodel)
        self.publfilter = FILTEREDJSModel(ppublstatus=Modelelement.PUBL, pmodel=self.model.jsmodel)
        printJSON(self.model.jsmodel, pfilepath=str(self.temp_folder), pfilename="model")
        printJSON(self.emptyfilter.filtered, pfilepath=str(self.temp_folder), pfilename="jsonempty")
        printJSON(self.draftfilter.filtered, pfilepath=str(self.temp_folder), pfilename="jsondraft")
        printJSON(self.gtopfilter.filtered, pfilepath=str(self.temp_folder), pfilename="jsongtop")
        printJSON(self.publfilter.filtered, pfilepath=str(self.temp_folder), pfilename="jsonpubl")

    def test_publish_function(self):
        element = {"id": 0}
        self.assertTrue(self.emptyfilter._publishable(element))
        self.assertTrue(self.gtopfilter._publishable(element))
        element["publstatus"] = None
        self.assertTrue(self.emptyfilter._publishable(element))
        self.assertTrue(self.publfilter._publishable(element))
        self.assertTrue(self.draftfilter._publishable(element))
        element["publstatus"] = Modelelement.DRAFT
        self.assertTrue(self.emptyfilter._publishable(element))
        self.assertFalse(self.publfilter._publishable(element))
        self.assertFalse(self.gtopfilter._publishable(element))
        self.assertTrue(self.draftfilter._publishable(element))
        element["publstatus"] = Modelelement.GTOP
        self.assertTrue(self.emptyfilter._publishable(element))
        self.assertFalse(self.publfilter._publishable(element))
        self.assertTrue(self.gtopfilter._publishable(element))
        self.assertTrue(self.draftfilter._publishable(element))
        element["publstatus"] = Modelelement.PUBL
        self.assertTrue(self.emptyfilter._publishable(element))
        self.assertTrue(self.publfilter._publishable(element))
        self.assertTrue(self.gtopfilter._publishable(element))
        self.assertTrue(self.draftfilter._publishable(element))
        return

    def test_buildidlist(self):
        compidlist: set = {key for key in self.model.getelements("ENTI").keys()}
        draft = self.draftfilter.getfilteredidlist()
        self.assertSetEqual(compidlist, compidlist.intersection(self.draftfilter.getfilteredidlist()))

        compidlist: set = {key for key, val in self.model.getelements("ENTI").items() if
                           val["publstatus"] in ("GTOP", "PUBL")}
        self.assertSetEqual(compidlist, compidlist.intersection(self.gtopfilter.getfilteredidlist()))

        compidlist: set = {key for key, val in self.model.jsmodel[JSModel.elemtype2label("ENTI")].items()
                           if val["publstatus"] in ("PUBL")}
        self.assertSetEqual(compidlist, compidlist.intersection(self.publfilter.getfilteredidlist()))

    def test_unchanged_model(self):
        def jsonequal(pmodel1, pmodel2):
            return True

        # check with empty (default) filter
        self.assertTrue(jsonequal(self.model.jsmodel, self.emptyfilter.jsmodel))

        # DAFT includes all stati, no diagramlist do no filter diagrams
        self.assertTrue(jsonequal(self.model.jsmodel, self.draftfilter.jsmodel))

    def test_filtered_models(self):
        # my small example
        minimodel = FILTEREDJSModel(pmodel=simpletestjson, ppublstatus="GTOP")
        minimodeltext = json.dumps(minimodel.jsmodel)
        self.assertRegex(minimodeltext, r'.*"' + REALSUBENTI_LEV2[0] + r'".*')
        self.assertRegex(minimodeltext, r'.*"' + MASTER_ENTITY[0] + r'".*')
        minimodel = FILTEREDJSModel(pmodel=simpletestjson, ppublstatus="PUBL")
        minimodeltext = json.dumps(minimodel.jsmodel)
        self.assertNotRegex(minimodeltext, r'.*"' + REALSUBENTI_LEV2[0] + r'".*')
        self.assertRegex(minimodeltext, r'.*"' + MASTER_ENTITY[0] + r'".*')

        # do not select any diagram
        nodiag = FILTEREDJSModel(self.model.jsmodel, pimdiagrams=[])
        self.assertEqual(0, len(nodiag.jsmodel["diagrams"]))

        textjson = json.dumps(self.draftfilter.jsmodel)
        self.assertRegex(textjson, r'.*"' + MULTI_UK_ENTITY[0] + r'".*')
        self.assertRegex(textjson, r'.*"' + REALSUBENTI_LEV2[0] + r'".*')
        self.assertRegex(textjson, r'.*"' + MASTER_ENTITY[0] + r'".*')

        textjson = json.dumps(self.gtopfilter.jsmodel)
        self.assertNotRegex(textjson, r'.*"' + MULTI_UK_ENTITY[0] + r'".*')
        self.assertRegex(textjson, r'.*"' + REALSUBENTI_LEV2[0] + r'".*')
        self.assertRegex(textjson, r'.*"' + MASTER_ENTITY[0] + r'".*')

        textjson = json.dumps(self.publfilter.jsmodel)
        self.assertNotRegex(textjson, r'.*"' + MULTI_UK_ENTITY[0] + r'".*')
        self.assertNotRegex(textjson, r'.*"' + REALSUBENTI_LEV2[0] + '".*')
        self.assertRegex(textjson, r'.*"' + MASTER_ENTITY[0] + r'".*')
        return

    def ensure_enti_in_model(self, key: str, model_string: str, entity_dict: Dict, name: str):
        self.assertIsNotNone(entity_dict.get(key),
                             f"Missing entity '{key}' \"{name}\" in entities {entity_dict.keys()}")
        self.assertRegex(model_string, r'.*"' + key + r'":.*')


if __name__ == '__main__':
    unittest.main()
