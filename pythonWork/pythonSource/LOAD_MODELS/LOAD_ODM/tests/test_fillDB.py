import json
import os
import unittest
from contextlib import closing
from pathlib import Path

import SSOT_infra.tests.integration as testsrc
from SSOT_infra.tests.test_translateprompt import TestTranslation
from SSOT_db.IM_JSON import JSModel
from LOAD_MODELS.LOAD_ODM import fillDB,setodmparams,ODMParameter
from SSOT_db.SQL_INFRA import dbConnect
from SSOT_db.IM_OBJECTS import PhysicalUnit
from SSOT_infra import parameters


def create_testmodel(testmodel, new=True):
    # create model for testmodel1 no param file
    if new and os.path.exists(testmodel.dbfile):
        os.remove(testmodel.dbfile)
    os.chdir(testmodel.modeldir)
    db = fillDB.fillmergedb(pmodelname=testmodel.modelname, pdbfilepath=testmodel.dbfile,
                           plogfilepath=testmodel.logfile,pverbose=True)
    assert db.is_file()
    return


class TestFillDatabase(unittest.TestCase):

    def setUp(self) -> None:
        translation = TestTranslation()
        translation.setUp()
        self.testmodel1 = testsrc.ModelHelper(testsrc.TESTMODEL1)
        self.testmodel2 = testsrc.ModelHelper(testsrc.TESTMODEL2)
        self.testmodelcrm = testsrc.ModelHelper(testsrc.CRMTEST)
        print ("************************* enable test wenn es funktioniert")
        self.testmodel2.initDB(palways=True)

    def test_fillmergedb(self):
        create_testmodel(self.testmodel1, new=True)
        create_testmodel(self.testmodel1, new=False)
        dbConnect.openDB(self.testmodel1.dbfile)
        phyus = PhysicalUnit.select()
        self.assertGreater(len(phyus),0)

    def test_filldb(self):
        def getbyfield(pmodel, ptype, pname, pfield='name', plang=None):
            retval = []
            for k, v in pmodel[ptype].items():
                if (plang is None and v[pfield] == pname) or \
                        (plang is not None and v[pfield][plang] == pname):
                    retval.append((k, v))
            # raise Exception(f"{ptype} : {pfield} : {pvalue}({plang}) not found ")
            return retval

        def testuserdefproperties(jmodel):
            entiid, enti = jmodel.getbyfield(ptype="entities", pvalue="Multi UK Entity", plang='en')[0]
            self.assertEqual(enti["publstatus"], "DRAFT")
            entiid, enti = jmodel.getbyfield(ptype="entities", pvalue="Single Entity", plang='en')[0]
            self.assertEqual(enti["publstatus"], "GTOP")
            attrid, attr = jmodel.getbyfield(ptype="attributes", pvalue="Attribute1", plang='en')[0]
            self.assertEqual(attr["publstatus"], "GTOP")
            relaid, rela = jmodel.getbyfield(ptype="relations", pvalue="Relation_1")[0]
            self.assertEqual(rela["publstatus"], "GTOP")
            relaid, rela = jmodel.getbyfield(ptype="relations", pvalue="Master Entity_subtype_realsubenti_lev1")[0]
            self.assertIsNone(rela["publstatus"])
            return

        def testsubenties(jmodel):
            # subentities and super entities
            masterentityID, masterentity = jmodel.getbyfield(ptype="entities", pvalue="Master Entity", plang='en')[0]
            self.assertEqual(masterentity["subtypellevel+"], 0, "Master Entity")
            arcID, arc = jmodel.getbyfield(ptype="arcs", pvalue=masterentityID, pfield='entity')[0]
            self.assertEqual(len(arc["relations"]), 3, "Master Entity arc has wrong relations")

            masterentity2ID, masterentity2 = jmodel.getbyfield(ptype="entities", pvalue="Master Entity2", plang='en')[0]
            self.assertEqual(masterentity2["subtypellevel+"], 0, "Master Entity2")
            arcID, arc = jmodel.getbyfield(ptype="arcs", pvalue=masterentity2ID, pfield='entity')[0]
            self.assertEqual(len(arc["relations"]), 3, "Master Entity2 arc has wrong relations")

            childentity1ID, childentity1 = jmodel.getbyfield(ptype="entities", pvalue="Child Entity1", plang='en')[0]
            self.assertEqual(childentity1["subtypellevel+"], 1, "Child Entity1")

            childentity2ID, childentity2 = jmodel.getbyfield(ptype="entities", pvalue="Child Entity2", plang='en')[0]
            self.assertEqual(childentity2["subtypellevel+"], 1, "Child Entity2")

            realsubenti_lev1ID, realsubenti_lev1 = jmodel.getbyfield(ptype="entities", pvalue="realsubenti_lev1", plang='en')[0]
            self.assertEqual(realsubenti_lev1["subtypellevel+"], 1, "realsubenti_lev1")
            arcID, arc = jmodel.getbyfield(ptype="arcs", pvalue=realsubenti_lev1ID, pfield='entity')[0]
            self.assertEqual(len(arc["relations"]), 2, "realsubenti_lev1 arc has wrong relations")

            realsubenti_lev2ID, realsubenti_lev2 = jmodel.getbyfield(ptype="entities", pvalue="realsubenti_lev2", plang='en')[0]
            self.assertEqual(realsubenti_lev2["subtypellevel+"], 2, "realsubenti_lev2")
            with self.assertRaises(Exception):
                arcID, arc = jmodel.getbyfield(ptype="arcs", pvalue=realsubenti_lev2ID, pfield='entity')[0]

            extsubentitylev22ID, extsubentitylev22 = jmodel.getbyfield(ptype="entities", pvalue="extsubentitylev2-2", plang='en')[0]
            self.assertEqual(extsubentitylev22["subtypellevel+"], 0, "extsubentitylev2-2")
            self.assertEqual(len(extsubentitylev22["supertypes+"]), 1, "supertentites extsubentitylev2-2")
            arcID, arc = jmodel.getbyfield(ptype="arcs", pvalue=extsubentitylev22ID, pfield='entity')[0]
            self.assertEqual(len(arc["relations"]), 1, "extsubentitylev2-2 arc has wrong relations")

            realsubenti2lev1ID, realsubenti2lev1 = jmodel.getbyfield(ptype="entities", pvalue="realsubenti2-lev1", plang='en')[0]
            self.assertEqual(realsubenti2lev1["subtypellevel+"], 1, "realsubenti2-lev1")
            self.assertEqual(len(realsubenti2lev1["supertypes+"]), 2, "supertentites realsubenti2-lev1")

            subentitynonoverlay2ID, subentitynonoverlay2 = \
                jmodel.getbyfield(ptype="entities", pvalue="subentitynonoverlay2", plang='en')[0]
            self.assertEqual(subentitynonoverlay2["subtypellevel+"], 0, "subentitynonoverlay2")
            return

        # create model for testmodel1. no param file

        tm1 = testsrc.ModelHelper(testsrc.TESTMODEL1)
        tm1.modeldir = testsrc.testmodels_dir() / tm1.modelname
        if os.path.exists(tm1.dbfile):
            os.remove(tm1.dbfile)
        os.chdir(tm1.modeldir)
        fillDB.fillmergedb(pmodelname=tm1.modelname, pdbfilepath=tm1.dbfile, plogfilepath=tm1.logfile)

        self.assertTrue(os.path.exists(tm1.dbfile), f"DB file not created where assumed {tm1.dbfile}")
        self.assertTrue(os.path.exists(tm1.dbdir / (tm1.modelname + '_loaded.json')),
                        f"json file not where assumed {tm1.dbdir / (tm1.modelname + '_loaded.json')}")
        self.assertTrue(os.path.exists(tm1.jsonfile),
                        f"json file not where assumed {tm1.jsonfile}")
        self.assertTrue(os.path.exists(tm1.logfile),
                        f"Log file not where assumed {tm1.logfile}")
        # create db for a second time => merge
        fillDB.fillmergedb(pmodelname=tm1.modelname, pdbfilepath=tm1.dbfile,
                          plogfilepath=tm1.logfile)
        # check subentitylevels
        jmodel = JSModel.readfromfile(tm1.jsonfile)
        testsubenties(jmodel)
        testuserdefproperties(jmodel)

        # create db for testmodel2 with Paramfile
        tm2 = testsrc.ModelHelper(testsrc.TESTMODEL2)
        # if os.path.exists(tm2.dbfile):
        #    createDB(pupgrade=True, pparamfile=paramfile)
        fillDB.fillmergedb(pmodelfilepath=tm2.modelfile, pdbfilepath=tm2.dbfile,
                          plogfilepath=tm2.logfile)
        # check handling of translations
        #print(f"Verifying against {tm2.jsonfile}")
        jmodel = JSModel.readfromfile(tm2.jsonfile)
        checkentityID, checkentity = jmodel.getbyfield(ptype="entities", pvalue="Kind Entität1", plang="de")[0]
        self.assertIsNotNone(checkentity, f"Testcase 'Child Entity1' is not present in {tm2.modelname}")
        synos = list(checkentity["synonyms"])
        self.assertEqual(synos[0]["en"], "*de* DSynonym")
        self.assertEqual(synos[0]["fr"], "*de* DSynonym")
        self.assertEqual(checkentity["descr"]["en"],
                         "Child entity,  Subtype \nDisplayed on all zoom levels (0-2)")
        self.assertEqual(checkentity["descr"]["fr"],
                         "*de* Untergeordnete Entität, Untertyp\nWird auf allen Zoomstufen angezeigt (0-2)")
        attr = jmodel.jsmodel["attributes"][checkentity["attributes+"][0]]
        self.assertEqual(attr["techname"], "ERSTE_ERSCHEINUNG", "wrong testcase attribute")
        self.assertEqual(attr["tooltip"]["en"], "*de* Tooltip Eonly")
        self.assertEqual(attr["tooltip"]["fr"], "*de* Tooltip Eonly")

        imprint = jmodel.jsmodel['_imprint_'].get('git-revision')
        self.assertTrue(len(imprint) > 2)

        # create db for crmtest with Paramfile
        testmodelcrm = testsrc.ModelHelper(testsrc.CRMTEST)
        # error for wrong modelname
        with self.assertRaises(Exception):
            fillDB.fillmergedb(pdbfilepath=testmodelcrm.dbfile, pmodelname='Gugus')

        # should work
        if os.path.exists(testmodelcrm.dbfile):
            os.remove(testmodelcrm.dbfile)
        if os.path.exists(testmodelcrm.logfile):
            os.remove(testmodelcrm.logfile)

        fillDB.fillmergedb(pdbfilepath=testmodelcrm.dbfile,
                          pmodelfilepath=testmodelcrm.modelfile,
                          plogfilepath=testmodelcrm.logfile)
        self.assertTrue(os.path.exists(testmodelcrm.dbfile), f"DB file not created where assumed {testmodelcrm.dbfile}")
        self.assertTrue(os.path.exists(testmodelcrm.dbdir / (testmodelcrm.modelname + '_loaded.json')),
                        f"json file not where assumed {testmodelcrm.dbdir / (testmodelcrm.modelname + '_loaded.json')}")
        self.assertTrue(os.path.exists(testmodelcrm.jsonfile),
                        f"json file not where assumed {testmodelcrm.jsonfile}")
        self.assertTrue(os.path.exists(testmodelcrm.logfile),
                        f"log file not where assumed {testmodelcrm.logfile}")

        testmodelriddle = testsrc.ModelHelper(testsrc.RIDDLE)
        if os.path.exists(testmodelriddle.dbfile):
            os.remove(testmodelriddle.dbfile)
        os.chdir(testmodelriddle.modeldir)
        fillDB.fillmergedb(pmodelname=testmodelriddle.modelname,
                          pdbfilepath=testmodelriddle.dbfile,
                          plogfilepath=testmodelriddle.logfile)
        self.assertTrue(os.path.exists(testmodelriddle.dbfile),
                        f"DB file not created where assumed {testmodelriddle.dbfile}")
        self.assertTrue(os.path.exists(testmodelriddle.dbdir / (testmodelriddle.modelname + '_loaded.json')),
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

    def test_odmfiledefaults(self):
        tm1 = testsrc.ModelHelper(testsrc.TESTMODEL1)
        tm2 = testsrc.ModelHelper(testsrc.TESTMODEL2)

        self.assertEqual(tm1.modeldir / 'IM' / 'Konfiguration',
                         fillDB.configdir(pconfigdir=tm1.modeldir / 'IM' / 'Konfiguration', pmodeldir=None))
        with self.assertRaises(Exception):
            _ = fillDB.configdir(pconfigdir=tm1.modeldir / 'XX' / 'Konfiguguration', pmodeldir=None)
        with self.assertRaises(Exception):
            _ = fillDB.configdir(pconfigdir=tm1.modeldir / 'IM' / 'Konfiguguration', pmodeldir=None)
        self.assertIsNone(fillDB.configdir(pconfigdir=None, pmodeldir=tm1.modeldir))

        self.assertIsNone(fillDB.configdir(pconfigdir=None, pmodeldir=None))
        self.assertIsNone(fillDB.configdir(pmodeldir=tm1.modeldir / 'IM'))
        self.assertEqual(tm1.modeldir / 'IM' / 'Konfiguration', fillDB.configdir(pconfigdir="Konfiguration",pmodeldir=tm1.modeldir / 'IM'))

        self.assertEqual(tm2.modeldir / 'IM' / 'Configuration',
                         fillDB.configdir(pconfigdir=tm2.modeldir / 'IM' / 'Configuration', pmodeldir=None))
        """
        fills default for destination directory

        :param pdestdir:  destination directory or None
        :param pmodeldir:  modelfiledirectory
        :return: pdestdir if it is not None
                pmodeldir/../DB if is None
        assertion failure, if directory does not exist  
        """
        with self.assertRaises(Exception):
            _ = fillDB.destdir(pdestdir=None, pmodeldir=None)
        with self.assertRaises(Exception):
            _ = fillDB.destdir(pdestdir=tm2.modeldir / 'XX')
        self.assertEqual(tm2.modeldir / 'DB', fillDB.destdir(pmodeldir=tm2.modeldir / 'IM'))
        self.assertEqual(tm2.modeldir / 'DB', fillDB.destdir(pdestdir=tm2.modeldir / 'DB'))

        return

    def test_odm2json(self):
        def checksubentimap(attrname,colname):
            #check subentitymapping
            geoinfo = crmjson.getbyfield(ptype="attributes",pfield="techname",pvalue=attrname)
            colu  = crmjson.getbyfield(ptype="columns",pvalue=colname)

            enti2id = None
            c=colu[0][1]
            for am in c["attributesmapped"]:
                if am[0]== geoinfo[0][0]:
                    enti2id = am[1]
                    break
            self.assertIsNotNone(enti2id)
            enti2 = crmjson.getbyid(enti2id)
            self.assertIn(geoinfo[0][0],enti2["inheritedattributes+"])
            self.assertIn(c["table-id"],enti2["tablesmapped+"][c["interface-id+"]])
            #secondary Entity-Id is in table mapping
            self.assertIn(enti2id,crmjson.getbyid(c["table-id"])["entitiesmapped"])
            #primary entityid is also in table mapping
            self.assertIn(geoinfo[0][1]["entity"],crmjson.getbyid(c["table-id"])["entitiesmapped"])
            return

        """
            create an empty memory db
            fill odm info into this db
            Module parameters contains all information about source of ODM files and model

            :pdebug True, writes the filled sqlite-datase to the parameters.dbFilePath()
            :return jsonsstructure created out of ODM info
            :exception if there are sever errors
        """
        tm1 = testsrc.ModelHelper(testsrc.TESTMODEL1)
        tm2 = testsrc.ModelHelper(testsrc.TESTMODEL2)
        crm = testsrc.ModelHelper(testsrc.CRMTEST)

        with self.assertRaises(Exception):
            setodmparams(ODMParameter())
            _ = fillDB.ODM2json()

        _ = fillDB.transferodm2json(pmodelfile=tm1.modeldir / 'IM' / (tm1.modelname + '.dmd'),
                                    pdestdir=None, pconfigdirec=None, pdebug=False)
        #_.write_json(tm1.jsonfile.with_stem(tm1.jsonfile.name + '_odm'))
        _.write_json(str(tm1.jsonfile).replace(tm1.jsonfilename,tm1.modelname + '_odm.json'))  # with_stem macht Probleme

        self.assertEqual(JSModel,type(_))
        _ = fillDB.transferodm2json(pmodelfile=tm2.modeldir / 'IM' / (tm2.modelname + '.dmd'),
                                    pdestdir=None, pconfigdirec='Configuration', pdebug=True)
        #_.write_json(tm2.jsonfile.with_stem(tm2.jsonfile.name + '_odm'))
        _.write_json(str(tm2.jsonfile).replace(tm2.jsonfilename,tm2.modelname + '_odm.json'))  # with_stem macht Probleme
        self.assertEqual(JSModel,type(_))

        crmjson = fillDB.transferodm2json(pmodelfile=crm.modelfile,
                                    pdestdir=None, pconfigdirec='Konfiguration', pdebug=False)
        checksubentimap(attrname="GEOINFORMATION",colname="col1tomany")
        #too complex to search in json
        # checksubentimap(attrname="Name",colname="name",tabname= "natural_person",intfname="MDM"

        tm2db = tm2.dbdir / (tm2.modelname + "_odm.db")
        self.assertTrue(tm2db.is_file())
        tm2db.unlink(missing_ok=False)
        return
