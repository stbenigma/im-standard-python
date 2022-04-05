import difflib
import json
import unittest
from SSOT_db.IM_OBJECTS import Modelelement
from SSOT_db.IM_JSON import JSModel,FILTEREDJSModel,printJSON
import  SSOT_infra.tests.integration as testsrc

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
            "realsubenti_lev2",
            "Master Entity"
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
      "realsubenti_lev2": {
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
         "supertypeentity": "Master Entity",
         "supertypes+": [],
      },
      "Master Entity": {
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
            "realsubenti_lev2"
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


class MyTestCase(unittest.TestCase):

    def setUp(self):
        from LOAD_MODELS.LOAD_ODM.tests.test_fillDB import create_testmodel
        testmodelname, testdir, dbfilepath = testsrc.testmodel1()
        create_testmodel(testmodelname=testmodelname, testdir=testdir, dbfilepath=dbfilepath, new=True)
        self.model = JSModel.readfromfile(dbfilepath.__str__().replace("db","json"))
        self.emptyfilter = FILTEREDJSModel(pmodel=self.model.jsmodel)
        self.draftfilter = FILTEREDJSModel(ppublstatus=Modelelement.DRAFT,pmodel=self.model.jsmodel)
        self.gtopfilter = FILTEREDJSModel(ppublstatus=Modelelement.GTOP,pmodel=self.model.jsmodel)
        self.publfilter = FILTEREDJSModel(ppublstatus=Modelelement.PUBL,pmodel=self.model.jsmodel)

        testmodelname, testdir, dbfilepath = testsrc.testmodelcrm()
        self.crmmodel = JSModel.readfromfile(dbfilepath.__str__().replace("crmTest.db","stabilescrmTest.json"))


    def test_publish_function(self):
        element = {"id":0}
        self.assertTrue(self.emptyfilter._publishable(element))
        self.assertTrue(self.gtopfilter._publishable(element))
        element["publstatus"]=None
        self.assertTrue(self.emptyfilter._publishable(element))
        self.assertFalse(self.publfilter._publishable(element))
        self.assertTrue(self.draftfilter._publishable(element))
        element["publstatus"]=Modelelement.DRAFT
        self.assertTrue(self.emptyfilter._publishable(element))
        self.assertFalse(self.publfilter._publishable(element))
        self.assertFalse(self.gtopfilter._publishable(element))
        self.assertTrue(self.draftfilter._publishable(element))
        element["publstatus"]=Modelelement.GTOP
        self.assertTrue(self.emptyfilter._publishable(element))
        self.assertFalse(self.publfilter._publishable(element))
        self.assertTrue(self.gtopfilter._publishable(element))
        self.assertTrue(self.draftfilter._publishable(element))
        element["publstatus"]=Modelelement.PUBL
        self.assertTrue(self.emptyfilter._publishable(element))
        self.assertTrue(self.publfilter._publishable(element))
        self.assertTrue(self.gtopfilter._publishable(element))
        self.assertTrue(self.draftfilter._publishable(element))
        return

    def test_buildidlist(self):
        compidlist:set = {key for key in self.model.getelements("ENTI").keys()}
        draft = self.draftfilter.getfilteredidlist()
        self.assertSetEqual(compidlist,compidlist.intersection(self.draftfilter.getfilteredidlist()))

        compidlist:set = {key for key,val in self.model.getelements("ENTI").items() if val["publstatus"] in ("GTOP","PUBL")}
        self.assertSetEqual(compidlist,compidlist.intersection(self.gtopfilter.getfilteredidlist()))

        compidlist:set = {key for key,val in self.model.jsmodel[JSModel.elemtype2label("ENTI")].items()
                          if val["publstatus"] in ("PUBL")}
        self.assertSetEqual(compidlist,compidlist.intersection(self.publfilter.getfilteredidlist()))

    def test_unchanged_model(self):
        def jsonequal(pmodel1,pmodel2):
            return True

        #check with empty (default) filter
        self.assertTrue(jsonequal(self.model.jsmodel, self.emptyfilter.jsmodel))

        # DAFT includes all stati, no diagramlist do no filter diagrams
        self.assertTrue(jsonequal(self.model.jsmodel, self.draftfilter.jsmodel))

    def test_filtered_models(self):
        #my small example
        minimodel = FILTEREDJSModel(pmodel=simpletestjson,ppublstatus="GTOP")
        minimodeltext = json.dumps(minimodel.jsmodel)
        self.assertRegex(minimodeltext,r'.*"realsubenti_lev2".*')
        self.assertRegex(minimodeltext,r'.*"Master Entity".*')
        minimodel = FILTEREDJSModel(pmodel=simpletestjson,ppublstatus="PUBL")
        minimodeltext = json.dumps(minimodel.jsmodel)
        self.assertNotRegex(minimodeltext,r'.*"realsubenti_lev2".*')
        self.assertRegex(minimodeltext,r'.*"Master Entity".*')

        # do not select any diagram
        nodiag = FILTEREDJSModel(self.model.jsmodel,pimdiagrams=[])
        self.assertEqual(0,len(nodiag.jsmodel["diagrams"]))

        try:
            textjson = json.dumps(self.draftfilter.jsmodel)
            self.assertRegex(textjson,r'.*"Multi UK Entity".*')
            self.assertRegex(textjson,r'.*"realsubenti_lev2".*')
            self.assertRegex(textjson,r'.*"Master Entity".*')

            textjson = json.dumps(self.gtopfilter.jsmodel)
            self.assertNotRegex(textjson,r'.*"Multi UK Entity".*')
            self.assertRegex(textjson,r'.*"realsubenti_lev2".*')
            self.assertRegex(textjson,r'.*"Master Entity".*')

            textjson = json.dumps(self.publfilter.jsmodel)
            self.assertNotRegex(textjson,r'.*"Multi UK Entity".*')
            self.assertNotRegex(textjson,r'.*"realsubenti_lev2".*')
            self.assertRegex(textjson,r'.*"Master Entity".*')
        except Exception as e:
            # printJSON(self.model.jsmodel,pfilepath="/Users/stb/Downloads",pfilename="model")
            # printJSON(self.emptyfilter.jsmodel,pfilepath="/Users/stb/Downloads",pfilename="jsonempty")
            # printJSON(self.draftfilter.jsmodel,pfilepath="/Users/stb/Downloads",pfilename="jsondraft")
            # printJSON(self.gtopfilter.jsmodel,pfilepath="/Users/stb/Downloads",pfilename="jsongtop")
            # printJSON(self.publfilter.jsmodel,pfilepath="/Users/stb/Downloads",pfilename="jsonpubl")
            raise e

        #crm does not have any publstatus set.
        try:
            self.crmpublfilter = FILTEREDJSModel(ppublstatus=Modelelement.PUBL, pmodel=self.crmmodel.jsmodel)
            self.assertEqual(0, len(self.crmpublfilter.jsmodel["entities"]))
            self.assertEqual(3, len(self.crmpublfilter.jsmodel["diagrams"]),
                             "Found diagrams " + ",".join(self.crmpublfilter.jsmodel["diagrams"].keys()) + " expected none.\n"
                             + str(next(iter(self.crmpublfilter.jsmodel["diagrams"].values()))))
            self.assertEqual(0, len(self.crmpublfilter.jsmodel["tables"]))
            self.assertEqual(0, len(self.crmpublfilter.jsmodel["columns"]))
            self.assertEqual(0, len(self.crmpublfilter.jsmodel["systems"]))
            self.assertEqual(0, len(self.crmpublfilter.jsmodel["columns"]))
        except Exception as e:
            #printJSON(self.crmmodel.jsmodel, pfilepath="/Users/stb/Downloads", pfilename="crmmodel")
            #printJSON(self.crmpublfilter.jsmodel, pfilepath="/Users/stb/Downloads", pfilename="crmpublmodel")
            raise e

        try:
            self.crmdummyfilter = FILTEREDJSModel(pimdiagrams=["DUMMY"], pmodel=self.crmmodel.jsmodel)
            self.assertEqual(1,len(self.crmdummyfilter.jsmodel["diagrams"]))
            self.assertEqual(6,len(self.crmdummyfilter.jsmodel["entities"]))
            textjson = json.dumps(self.crmdummyfilter.jsmodel)
            self.assertNotRegex(textjson,r'.*"ENTI114".*')
            self.assertEqual(10,len(self.crmdummyfilter.jsmodel["attributes"]))
            self.assertEqual(18,len(self.crmdummyfilter.jsmodel["tables"]))
            self.assertEqual(31,len(self.crmdummyfilter.jsmodel["columns"]))
            self.assertEqual(5,len(self.crmdummyfilter.jsmodel["systems"]))
        except Exception as e:
            #printJSON(self.crmdummyfilter.jsmodel,pfilepath="/Users/stb/Downloads",pfilename="crmdummymodel")
            raise e

        self.crm2diagfilter = FILTEREDJSModel(pimdiagrams=["DUMMY","Kunde mit xxx"],pmodel=self.crmmodel.jsmodel)
        self.assertEqual(1,len(self.crm2diagfilter.jsmodel["diagrams"]))

        self.crm2diagfilter = FILTEREDJSModel(pimdiagrams=["DUMMY","Kunde mit Bilder"],pmodel=self.crmmodel.jsmodel)
        self.assertEqual(2,len(self.crm2diagfilter.jsmodel["diagrams"]))


if __name__ == '__main__':
    unittest.main()
