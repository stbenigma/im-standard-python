import json
import os
import unittest
from contextlib import closing
from pathlib import Path

import SSOT_infra.tests.integration as testsrc
from LOAD_MODELS.LOAD_ODM import fillDB
from SSOT_db.SQL_INFRA import dbConnect
from SSOT_db.createDB import createDB
from SSOT_infra import parameters
from SSOT_infra.tests.test_translateprompt import TestTranslation


def create_testmodel(testmodel , new=True):
    # create model for testmodel1 no param file
    if new and os.path.exists(testmodel.dbfile):
        os.remove(testmodel.dbfile)
    os.chdir(testmodel.modeldir)
    db = fillDB.filldbmain(pmodelname=testmodel.modelname, pdestination=testmodel.dbfile)
    assert db.is_file()
    return


class TESTFILLDB(unittest.TestCase):

    def setUp(self) -> None:
        translation = TestTranslation()
        translation.setUp()
        self.testmodel1 = testsrc.Testmodel(testsrc.TESTMODEL1)
        self.testmodel2 = testsrc.Testmodel(testsrc.TESTMODEL2)
        self.testmodelcrm = testsrc.Testmodel(testsrc.CRMTEST)

    def test_filldbmain(self):
        assert True

    def test_fillmergedb(self):
        create_testmodel(self.testmodel1, new=True)
        create_testmodel(self.testmodel1, new=False)

    def test_filldb(self):
        def getbyfield(pmodel, ptype, pname, pfield='name', plang=None):
            retval = []
            for k, v in pmodel[ptype].items():
                if (plang is None and v[pfield] == pname) or \
                        (plang is not None and v[pfield][plang] == pname):
                    retval.append((k, v))
            # raise Exception(f"{ptype} : {pfield} : {pname}({plang}) not found ")
            return retval

        def testuserdefproperties(jmodel):
            entiid, enti = getbyfield(jmodel, "entities", "Multi UK Entity", plang='en')[0]
            self.assertEqual(enti["publstatus"], "DRAFT")
            entiid, enti = getbyfield(jmodel, "entities", "Single Entity", plang='en')[0]
            self.assertEqual(enti["publstatus"], "GTOP")
            attrid, attr = getbyfield(jmodel, "attributes", "Attribute1", plang='en')[0]
            self.assertEqual(attr["publstatus"], "GTOP")
            relaid, rela = getbyfield(jmodel, "relations", "Relation_1")[0]
            self.assertEqual(rela["publstatus"], "GTOP")
            relaid, rela = getbyfield(jmodel, "relations", "Master Entity_subtype_realsubenti_lev1")[0]
            self.assertIsNone(rela["publstatus"])
            return

        def testsubenties(jmodel):
            # subentities and super entities
            masterentityID, masterentity = getbyfield(jmodel, "entities", "Master Entity", plang='en')[0]
            self.assertEqual(masterentity["subtypellevel+"], 0, "Master Entity")
            arcID, arc = getbyfield(jmodel, "arcs", masterentityID, pfield='entity')[0]
            self.assertEqual(len(arc["relations"]), 3, "Master Entity arc has wrong relations")

            masterentity2ID, masterentity2 = getbyfield(jmodel, "entities", "Master Entity2", plang='en')[0]
            self.assertEqual(masterentity2["subtypellevel+"], 0, "Master Entity2")
            arcID, arc = getbyfield(jmodel, "arcs", masterentity2ID, pfield='entity')[0]
            self.assertEqual(len(arc["relations"]), 3, "Master Entity2 arc has wrong relations")

            childentity1ID, childentity1 = getbyfield(jmodel, "entities", "Child Entity1", plang='en')[0]
            self.assertEqual(childentity1["subtypellevel+"], 1, "Child Entity1")

            childentity2ID, childentity2 = getbyfield(jmodel, "entities", "Child Entity2", plang='en')[0]
            self.assertEqual(childentity2["subtypellevel+"], 1, "Child Entity2")

            realsubenti_lev1ID, realsubenti_lev1 = getbyfield(jmodel, "entities", "realsubenti_lev1", plang='en')[0]
            self.assertEqual(realsubenti_lev1["subtypellevel+"], 1, "realsubenti_lev1")
            arcID, arc = getbyfield(jmodel, "arcs", realsubenti_lev1ID, pfield='entity')[0]
            self.assertEqual(len(arc["relations"]), 2, "realsubenti_lev1 arc has wrong relations")

            realsubenti_lev2ID, realsubenti_lev2 = getbyfield(jmodel, "entities", "realsubenti_lev2", plang='en')[0]
            self.assertEqual(realsubenti_lev2["subtypellevel+"], 2, "realsubenti_lev2")
            with self.assertRaises(Exception):
                arcID, arc = getbyfield(jmodel, "arcs", realsubenti_lev2ID, pfield='entity')[0]

            extsubentitylev22ID, extsubentitylev22 = getbyfield(jmodel, "entities", "extsubentitylev2-2", plang='en')[0]
            self.assertEqual(extsubentitylev22["subtypellevel+"], 0, "extsubentitylev2-2")
            self.assertEqual(len(extsubentitylev22["supertypes+"]), 1, "supertentites extsubentitylev2-2")
            arcID, arc = getbyfield(jmodel, "arcs", extsubentitylev22ID, pfield='entity')[0]
            self.assertEqual(len(arc["relations"]), 1, "extsubentitylev2-2 arc has wrong relations")

            realsubenti2lev1ID, realsubenti2lev1 = getbyfield(jmodel, "entities", "realsubenti2-lev1", plang='en')[0]
            self.assertEqual(realsubenti2lev1["subtypellevel+"], 1, "realsubenti2-lev1")
            self.assertEqual(len(realsubenti2lev1["supertypes+"]), 2, "supertentites realsubenti2-lev1")

            subentitynonoverlay2ID, subentitynonoverlay2 = \
                getbyfield(jmodel, "entities", "subentitynonoverlay2", plang='en')[0]
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
            testuserdefproperties(jmodel)

        # create db for testmodel2 with Paramfile
        testmodelname = testsrc.TESTMODEL2
        testpath = testsrc.testmodels_dir() / testmodelname
        dbdirpath = testpath / 'DB'
        dbfilepath = dbdirpath / (testmodelname + '.db')
        jsonfilepath = dbdirpath / (testmodelname + '.json')
        paramfile = testpath / (testmodelname + '.params')
        if os.path.exists(dbfilepath):
            createDB(pupgrade=True, pparamfile=paramfile)
        fillDB.filldbmain(pparamfile=paramfile)
        # check handling of translations
        with open(jsonfilepath) as jsonFile:
            jmodel = json.load(jsonFile)
            checkentityID, checkentity = getbyfield(jmodel, "entities", "Kind Entität1", plang="de")[0]
            self.assertIsNotNone(checkentity, f"Testcase 'Child Entity1' is not present in {testmodelname}")
            synos = list(checkentity["synonyms"])
            self.assertEqual(synos[0]["en"], "DSynonym")
            self.assertEqual(synos[0]["fr"], "DSynonym")
            self.assertEqual(checkentity["descr"]["en"],
                             "Child entity,  Subtype \nDisplayed on all zoom levels (0-2)")
            self.assertEqual(checkentity["descr"]["fr"],
                             "Untergeordnete Entität, Untertyp\nWird auf allen Zoomstufen angezeigt (0-2)")
            attr = jmodel["attributes"][checkentity["attributes+"][0]]
            self.assertEqual(attr["techname"], "ERSTE_ERSCHEINUNG", "wrong testcase attribute")
            self.assertEqual(attr["tooltip"]["en"], "Tooltip Eonly")
            self.assertEqual(attr["tooltip"]["fr"], "Tooltip Eonly")
            jsonFile.close()

        # create db for crmtest with Paramfile
        testmodelcrm = testsrc.Testmodel(testsrc.CRMTEST)
        # error for wrong modelname
        with self.assertRaises(Exception):
            fillDB.filldbmain(pparamfile=testmodelcrm.paramfile, pmodelname='Gugus')

        # should work
        if os.path.exists(testmodelcrm.dbfile):
            os.remove(testmodelcrm.dbfile)
        if os.path.exists(testmodelcrm.logfile):
            os.remove(testmodelcrm.logfile)

        fillDB.filldbmain(pparamfile=testmodelcrm.paramfile)
        self.assertTrue(os.path.exists(testmodelcrm.dbfile), f"DB file not created where assumed {testmodelcrm.dbfile}")
        self.assertTrue(os.path.exists(testmodelcrm.dbdir / (testmodelcrm.modelname + '_loaded.json')),
                        f"json file not where assumed {testmodelcrm.dbdir / (testmodelcrm.modelname + '_loaded.json')}")
        self.assertTrue(os.path.exists(testmodelcrm.jsonfile),
                        f"json file not where assumed {testmodelcrm.jsonfile}")
        self.assertTrue(os.path.exists(testmodelcrm.logfile),
                        f"json file not where assumed {testmodelcrm.logfile}")

        testmodelriddle  = testsrc.Testmodel(testsrc.RIDDLE)
        if os.path.exists(testmodelriddle.dbfile):
            os.remove(testmodelriddle.dbfile)
        os.chdir(testmodelriddle.modeldir)
        fillDB.filldbmain(pmodelname=testmodelriddle.modelname, pdestination=testmodelriddle.dbfile)
        self.assertTrue(os.path.exists(testmodelriddle.dbfile), f"DB file not created where assumed {testmodelriddle.dbfile}")
        self.assertTrue(os.path.exists(testmodelriddle.dbdir/ (testmodelriddle.modelname + '_loaded.json')),
                        f"json file not where assumed {testmodelriddle.dbdir / (testmodelriddle.modelname + '_loaded.json')}")
        self.assertTrue(os.path.exists(testmodelriddle.jsonfile),
                        f"json file not where assumed {testmodelriddle.jsonfile}")
        self.assertTrue(os.path.exists(testmodelriddle.logfile),
                        f"log file not where assumed {testmodelriddle.logfile}")


        return testmodelriddle.dbfile

    def test_revision(self):
        repo_revision = parameters.read_git_description(Path(__file__).parent)
        self.assertTrue('unknown' not in repo_revision)

        db_file = self.test_filldb()
        with closing(dbConnect.openDBbasic(db_file)) as conn:
            ver = dbConnect.read_git_revision(conn)
            self.assertEqual(ver, repo_revision)

