import json
import os
import unittest

import SSOT_infra.tests.integration as testsrc
from LOAD_MODELS.LOAD_ODM import fillDB
from SSOT_infra.tests.test_translateprompt import TestTranslation




class TESTFILLDB(unittest.TestCase):

    def setUp(self) -> None:
        translation = TestTranslation()
        translation.setUp()

    def test_filldbmain(self):
        assert True

    def test_fillmergedb(self):
        assert True

    def test_filldb(self):
        def getbyfield(pmodel, ptype, pname, pfield='name', plang=None):
            for k,v in pmodel[ptype].items():
                if (plang is None and v[pfield] == pname) or \
                        (plang is not None and v[pfield][plang] == pname):
                    return k,v
            raise Exception(f"{ptype} : {pfield} : {pname}({plang}) not found ")

        def testsubenties(jmodel):
            # subentities and super entities
            masterentityID,masterentity = getbyfield(jmodel, "entities", "Master Entity", plang='en')
            self.assertEqual(masterentity["subtypellevel+"], 0, "Master Entity")
            arcID,arc = getbyfield(jmodel,"arcs",masterentityID,pfield='entity')
            self.assertEqual(len(arc["relations"]),3,"Master Entity arc has wrong relations")

            masterentity2ID,masterentity2 = getbyfield(jmodel, "entities", "Master Entity2", plang='en')
            self.assertEqual(masterentity2["subtypellevel+"], 0, "Master Entity2")
            arcID,arc = getbyfield(jmodel,"arcs",masterentity2ID,pfield='entity')
            self.assertEqual(len(arc["relations"]),3,"Master Entity2 arc has wrong relations")

            childentity1ID,childentity1 = getbyfield(jmodel, "entities", "Child Entity1", plang='en')
            self.assertEqual(childentity1["subtypellevel+"], 1, "Child Entity1")

            childentity2ID,childentity2 = getbyfield(jmodel, "entities", "Child Entity2", plang='en')
            self.assertEqual(childentity2["subtypellevel+"], 1, "Child Entity2")

            realsubenti_lev1ID,realsubenti_lev1 = getbyfield(jmodel, "entities", "realsubenti_lev1", plang='en')
            self.assertEqual(realsubenti_lev1["subtypellevel+"], 1, "realsubenti_lev1")
            arcID,arc = getbyfield(jmodel,"arcs",realsubenti_lev1ID,pfield='entity')
            self.assertEqual(len(arc["relations"]),2,"realsubenti_lev1 arc has wrong relations")

            realsubenti_lev2ID,realsubenti_lev2 = getbyfield(jmodel, "entities", "realsubenti_lev2", plang='en')
            self.assertEqual(realsubenti_lev2["subtypellevel+"], 2, "realsubenti_lev2")
            with self.assertRaises(Exception):
                arcID, arc = getbyfield(jmodel, "arcs", realsubenti_lev2ID, pfield='entity')

            extsubentitylev22ID,extsubentitylev22 = getbyfield(jmodel, "entities", "extsubentitylev2-2", plang='en')
            self.assertEqual(extsubentitylev22["subtypellevel+"], 0, "extsubentitylev2-2")
            self.assertEqual(len(extsubentitylev22["supertypes+"]), 1, "supertentites extsubentitylev2-2")
            arcID,arc = getbyfield(jmodel,"arcs",extsubentitylev22ID,pfield='entity')
            self.assertEqual(len(arc["relations"]),1,"extsubentitylev2-2 arc has wrong relations")

            realsubenti2lev1ID,realsubenti2lev1 = getbyfield(jmodel, "entities", "realsubenti2-lev1", plang='en')
            self.assertEqual(realsubenti2lev1["subtypellevel+"], 1, "realsubenti2-lev1")
            self.assertEqual(len(realsubenti2lev1["supertypes+"]), 2, "supertentites realsubenti2-lev1")

            subentitynonoverlay2ID,subentitynonoverlay2 = getbyfield(jmodel, "entities", "subentitynonoverlay2", plang='en')
            self.assertEqual(subentitynonoverlay2["subtypellevel+"], 0, "subentitynonoverlay2")
            return

        # create model for testmodel1. no param file
        testmodelname = testsrc.TESTMODEL1
        testpath = testsrc.testmodels_dir() / testmodelname
        dbdirpath = testpath / 'DB'
        dbfilepath = dbdirpath / (testmodelname + '.db')
        jsonfilepath = dbdirpath / (testmodelname + '.json')
        if os.path.exists(dbfilepath):
            os.remove(dbfilepath)
        os.chdir(testpath)
        fillDB.filldbmain(pmodelname=testmodelname, pdestination=dbfilepath)
        self.assertTrue(os.path.exists(dbfilepath), f"DB file not created where assumed {dbfilepath}")
        self.assertTrue(os.path.exists(dbdirpath / (testmodelname + '_loaded.json')),
                        f"json file not where assumed {dbdirpath / (testmodelname + '_loaded.json')}")
        self.assertTrue(os.path.exists(jsonfilepath),
                        f"json file not where assumed {jsonfilepath}")
        self.assertTrue(os.path.exists(testpath / (testmodelname + '.log')),
                        f"json file not where assumed {testpath / (testmodelname + '.log')}")
        # create db for a second time => merge
        fillDB.filldbmain(pmodelname=testmodelname, pdestination=dbfilepath)
        # check subentitylevels
        with open(jsonfilepath) as jsonFile:
            jmodel = json.load(jsonFile)
            testsubenties(jmodel)

        # create db for testmodel2 with Paramfile
        testmodelname = testsrc.TESTMODEL2
        testpath = testsrc.testmodels_dir() / testmodelname
        dbdirpath = testpath / 'DB'
        dbfilepath = dbdirpath / (testmodelname + '.db')
        jsonfilepath = dbdirpath / (testmodelname + '.json')
        logfilepath = testpath / "logfiles" / "speciallog.log"
        paramfile = testpath / (testmodelname + '.params')
        fillDB.filldbmain(pparamfile=paramfile)
        # check handling of translations
        with open(jsonfilepath) as jsonFile:
            jmodel = json.load(jsonFile)
            checkentityID,checkentity = getbyfield(jmodel, "entities", "Child Entity1", plang="en")
            self.assertIsNotNone(checkentity, f"Testcase 'Child Entity1' is not present in {testmodelname}")
            synos = list(checkentity["synonyms"].values())
            self.assertEqual(synos[0]["de"], "*en* ESynonym")
            self.assertEqual(synos[0]["fr"], "*en* ESynonym")
            self.assertEqual(checkentity["descr"]["de"],
                             "*en* Child entity,  Subtype \nDisplayed on all zoom levels (0-2)")
            self.assertEqual(checkentity["descr"]["fr"],
                             "*en* Child entity,  Subtype \nDisplayed on all zoom levels (0-2)")
            attr = jmodel["attributes"][checkentity["attributes+"][0]]
            self.assertEqual(attr["techname"], "FIRST_APPEARANCE", "wrong testcase attribute")
            self.assertEqual(attr["tooltip"]["de"], "*en* Tooltip Eonly")
            self.assertEqual(attr["tooltip"]["fr"], "*en* Tooltip Eonly")
            jsonFile.close()

        # create db for crmtest with Paramfile
        testmodelname = testsrc.CRMTEST
        testpath = testsrc.testmodels_dir() / testmodelname
        dbdirpath = testpath / 'DB'
        dbfilepath = dbdirpath / (testmodelname + '.db')
        logfilepath = testpath / (testmodelname + '.log')
        paramfile = testpath / (testmodelname + '.params')
        # error for wrong modelname
        with self.assertRaises(Exception):
            fillDB.filldbmain(pparamfile=paramfile, pmodelname='Gugus')

        # should work
        if os.path.exists(dbfilepath):
            os.remove(dbfilepath)
        if os.path.exists(logfilepath):
            os.remove(logfilepath)

        fillDB.filldbmain(pparamfile=paramfile)
        self.assertTrue(os.path.exists(dbfilepath), f"DB file not created where assumed {dbfilepath}")
        self.assertTrue(os.path.exists(dbdirpath / (testmodelname + '_loaded.json')),
                        f"json file not where assumed {dbdirpath / (testmodelname + '_loaded.json')}")
        self.assertTrue(os.path.exists(dbdirpath / (testmodelname + '.json')),
                        f"json file not where assumed {dbdirpath / (testmodelname + '.json')}")
        self.assertTrue(os.path.exists(logfilepath),
                        f"json file not where assumed {logfilepath}")

        testmodelname = testsrc.RIDDLE
        testpath = testsrc.testmodels_dir() / testmodelname
        dbdirpath = testpath / 'DB'
        dbfilepath = dbdirpath / (testmodelname + '.db')
        if os.path.exists(dbfilepath):
            os.remove(dbfilepath)
        os.chdir(testpath)
        fillDB.filldbmain(pmodelname=testmodelname, pdestination=dbfilepath)
        self.assertTrue(os.path.exists(dbfilepath), f"DB file not created where assumed {dbfilepath}")
        self.assertTrue(os.path.exists(dbdirpath / (testmodelname + '_loaded.json')),
                        f"json file not where assumed {dbdirpath / (testmodelname + '_loaded.json')}")
        self.assertTrue(os.path.exists(dbdirpath / (testmodelname + '.json')),
                        f"json file not where assumed {dbdirpath / (testmodelname + '.json')}")
        self.assertTrue(os.path.exists((testmodelname + '.log')),
                        f"log file not where assumed {(testmodelname + '.log')}")
        return
