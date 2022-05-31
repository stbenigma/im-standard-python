import datetime
import json
import logging
import shutil
import unittest
from contextlib import closing
from pathlib import Path

import pytest
import io
import sys

import SSOT_infra.tests.integration as testsrc
from LOAD_MODELS.LOAD_INFRA import mergedbs, fillmodel2db
from LOAD_MODELS.LOAD_ODM import fillDB
from SSOT_db import createnewDB
from SSOT_db.IM_JSON import JSModel, sql2json, jsbusinessrule, jsguid, jsactorroles
from SSOT_db.IM_OBJECTS import *
from SSOT_db.SQL_INFRA import dbConnect
from SSOT_infra import parameters


class TestMergeJson(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path):
        self._caplog = caplog
        self.temp_folder = Path(tmp_path)

    def setUp(self) -> None:
        self.testmodelcrm = testsrc.Testmodel(testsrc.CRMTEST).initDB()
        self.testmodel1 = testsrc.Testmodel(testsrc.TESTMODEL1).initDB()
        self.riddle = testsrc.Testmodel(testsrc.RIDDLE).initDB()
        self.testmodel2 = testsrc.Testmodel(testsrc.TESTMODEL2).initDB()
        self.srcname = "TestMergeJson"

    def test_merge(self):
        dbConnect.openDB(self.testmodelcrm.dbfile, pversioncheck=False)
        mergedbs.connecttodbcopy()
        self.newbrname = 'test-BR10'
        # make sure legacy test entries are gone
        BusinessRule.delete(pwhere=("buru_name = ?", self.newbrname))
        self.crmmodel = JSModel(pmodel=sql2json(pdbname=self.testmodelcrm.modelname))
        buru = BusinessRule(buru_name=self.newbrname,
                            buru_rule='nichts',
                            buru_level='ATTR',
                            buru_type='CHECK',
                            buru_uc='me',
                            buru_dc=str(datetime.datetime.now()),
                            srcid='9999',
                            srcname=self.srcname)
        burujs = jsbusinessrule.businessrule2js(buru, plangs=('de', 'en', 'fr'))
        attrid = jsguid('ATTR', Attribute.select()[0].attr_id)
        tablid = jsguid('TABL', Table.select()[0].tabl_id)
        burujs['elements'] = {attrid: {"r/w": "R"},
                              tablid: {"r/w": "R"}
                              }
        burujs['sourceref'][self.srcname][1] = str(datetime.datetime.now())
        self.crmmodel.jsmodel['businessrules']["BURU9999"] = burujs

        with self._caplog.at_level(logging.DEBUG):
            mergedbs.mergejson2sql(self.crmmodel, psrcname=self.srcname)
        assert dbConnect.isopenDB()
        """generate json from merged DB"""
        newjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
        newburuid = newjson.jsmodel['attributes'][attrid]['businessrules+'][0]
        self.assertEqual(newburuid, newjson.jsmodel['tables'][tablid]['businessrules+'][0])

        newburu = newjson.getbyid(newburuid)
        self.assertTrue(newburuid in newjson.jsmodel['businessrules'])
        self.assertTrue(attrid in newburu['elements'])
        self.assertTrue(tablid in newburu['elements'])

        self.assertEqual('9999', newburu['sourceref'][self.srcname][0])

        # dbConnect.openDB(self.testmodelcrm.dbfile, pversioncheck=False)
        # now test an update
        updjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
        updburu = updjson.getelements('businessrules')[newburuid]
        updburu['errormsg']['en'] = "new error message"
        updburu['um'] = "meandmyself"
        del updburu['elements'][tablid]
        updburu['sourceref'][self.srcname] = ['9999-111', str(datetime.datetime.now())]
        with self._caplog.at_level(level=logging.ERROR):
            check = mergedbs.checkjsonmodel(pmodel=updjson, pverbose=False)
            if not check:
                for c in self._caplog.records:
                    if c.levelname == logging.ERROR:
                        print(c.getMessage())
            self.assertTrue(check)

        result = mergedbs.mergejson2sql(updjson, psrcname=self.srcname)
        # now check the merge
        newjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
        newburu = newjson.getbyid(newburuid)
        self.assertEqual('9999-111', newburu['sourceref'][self.srcname][0])
        self.assertEqual(newburu['errormsg']['en'], "new error message")
        self.assertTrue(attrid in newburu['elements'])
        self.assertFalse(tablid in newburu['elements'])
        # self.assertEqual("meandmyself",newburu['um'])

        # remove created elements
        BusinessRule.delete(pwhere=("buru_name = ?", self.newbrname))
        dbConnect.closeDB()

        return

    def test_mergeactorrole(self):
        dbConnect.openDB(self.testmodel1.dbfile, pversioncheck=False)
        try:
            # neuen Eintrag in json mergen in Datenbank
            actrjs = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
            actrjs.jsmodel['actorroles']['ACTR9999'] = \
                jsactorroles.actorrole2js(
                    Actorrole(srcid='99999', srcname='test',
                              actr_id=99999,
                              actr_name='test2', actr_descr='descr2'))

            # colus = actrjs.getelements('COLU')
            # attrs = actrjs.getelements('ATTR')
            actrjs.jsmodel['actorroles']['ACTR9999']["concerns"] = {'ATTR94': 'RC', 'ENTI93': 'IAC'}
        finally:
            dbConnect.closeDB()

    def test_mergefull(self):
        def savecurrentdbandjson(pjson):
            # can be used to save the current (memory-)database and a json file to filesystem
            # import sqlite3
            # locconn = sqlite3.connect("savedb.db")
            # dbConnect.getdbcon().backup(locconn)
            # locconn.close()
            # pjson.printmodel(pfilepath=".", pfilename="savejson.json")
            return

        parameters.initparam(pbasedirec=self.testmodel2.modeldir, pparamfile=self.testmodel2.paramfile)
        # test dryrun on exisisting files
        dbConnect.openDB(pfilepath=self.testmodel2.dbfile)
        curmodel = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
        dbConnect.closeDB()
        curmodel.printSPOD(self.temp_folder / 'curmodel.json')
        capturedOutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  # and redirect stdout.

        newjson = mergedbs.mergejs2db(pdbfile=self.testmodel2.dbfile, pmodel=curmodel, psrcname=self.srcname,
                                      pverbose=True, pdryrun=True)
        sys.stdout = sys.__stdout__  # Reset redirect.
        stdprint = capturedOutput.getvalue()
        # don't care about other errors I only test the dry-run-merge
        self.assertTrue(stdprint.startswith("***** dry merge-run on db"))

        # set up my model in memory to reuse it for several tests
        createnewDB(pdbfilepath=None)  # create in memory
        print("")

        firstjson = fillDB.transferodm2json(pmodelfile=self.testmodel2.modelfile)

        # create copy of filled db
        # first merge with itself
        createnewDB(pdbfilepath=None)
        result = mergedbs.mergejson2sql(firstjson, pverbose=True, psrcname="TEST")
        # for c in result.changes:
        #    print(c)
        enti2key = list(firstjson.jsmodel["entities"].keys())[1]

        self.assertEqual(0, result.updatecnt)
        self.assertTrue(result.insertcnt>0)
        self.assertEqual(0, result.deletecnt)
        self.assertEqual(0, len(result.warnings))
        self.assertEqual(0, len(result.errors))
        self.assertIsNotNone(firstjson.jsmodel["entities"][enti2key]["name"]["de"])

        firstjson.jsmodel["entities"][enti2key]["name"]["de"] += 'XX'
        result = mergedbs.mergejson2sql(firstjson, pverbose=True, psrcname="TEST", pcheckonly=False)
        result.write_json(self.temp_folder / 'test_mergefull.json')
        self.assertEqual(1, result.updatecnt)
        self.assertEqual(0, result.insertcnt)
        self.assertEqual(0, result.deletecnt)

        # check delete of existing
        # check create new entry
        # delete of my entry = last source is removed

        dbConnect.closeDB()

        curmodel.jsmodel['entities'] = {"blabla": {}}
        with self.assertRaises(Exception) as exp:
            mergedbs.mergejs2db(pdbfile=self.testmodel2.dbfile, pmodel=curmodel, psrcname=self.srcname,
                                pverbose=True, pdryrun=False)

    def test_merge_column_riddle(self):
        js_file = Path(self.riddle.dbdir, self.riddle.jsonfilename)
        self.assertTrue(js_file.is_file())
        with open(js_file, 'r') as src:
            jsmodel = json.load(src)

        previous = len(jsmodel['columns'])

        table_ref_key = next(iter(jsmodel['tables'].keys()))

        default_domain = \
            next(filter(lambda d: next(iter(d[1]['name'].values())) == 'Unknown', jsmodel['domains'].items()))[0]

        # apply changes to model
        new_column = {'name': 'test',
                      'table-id': table_ref_key,
                      'interface_col_id': '12-34',
                      'attributesmapped': [],
                      'mandatory': False,
                      'datatype': 'unknown',
                      'format': None,
                      'domain': default_domain,
                      'descr': "Created by unittest",
                      }

        self.set_defaults(new_column)
        new_column_key = 'COLU-1'
        jsmodel['columns'][new_column_key] = new_column
        tmpdb = Path('/tmp/test_merge_riddle.db')
        shutil.copy(self.riddle.dbfile, tmpdb)
        with closing(dbConnect.openDBbasic(tmpdb)):
            new_model = JSModel(jsmodel)
            result = mergedbs.mergejson2sql(new_model, psrcname=self.srcname)

        with closing(dbConnect.openDBbasic(tmpdb)) as connection:
            with closing(connection.execute(f"SELECT COUNT(*) FROM [columns]")) as cursor:
                r = cursor.fetchall()
                self.assertEqual(len(jsmodel['columns']), r[0][0])
                self.assertEqual(previous + 1, r[0][0])

        val = result.keytransl(new_column_key)
        self.assertIsInstance(val, int)
        self.assertIsNotNone(jsmodel['columns'][new_column_key], f"Expecting unaltered json")

        reloaded_jsmodel = JSModel(pmodel=sql2json(pdbname=str(tmpdb)))

        for category in filter(lambda c: c in ['entities', 'attributes', 'columns'], jsmodel.keys()):
            for key in jsmodel[category].keys():
                self.assertIsNotNone(reloaded_jsmodel[category].get(key), f"Missing {category} element {key}")

    def test_merge_table_and_column_riddle(self):
        js_file = Path(self.riddle.dbdir, self.riddle.jsonfilename)
        self.assertTrue(js_file.is_file())
        with open(js_file, 'r') as src:
            jsmodel = json.load(src)

        previous_table_count = len(jsmodel['tables'])
        previous_column_count = len(jsmodel['columns'])

        sys_ref_key = next(iter(jsmodel['systems'].keys()))

        default_domain = \
            next(filter(lambda d: next(iter(d[1]['name'].values())) == 'Unknown', jsmodel['domains'].items()))[0]

        # apply changes to model
        new_table = {
            'name': 'main',
            'interface-id': sys_ref_key,
            'entitiesmapped': [],
            'relationsmapped': [],
            'columnsmapped': [],
            'prefix': None, 'descr': "Unittest",
        }
        self.set_defaults(new_table)
        new_table_key = 'TABL-1'
        jsmodel['tables'][new_table_key] = new_table

        # apply changes to model
        column_name = 'unitttest-abc'
        new_column = {'name': column_name,
                      'table-id': new_table_key,
                      'interface_col_id': '12-34',
                      'attributesmapped': [],
                      'mandatory': False,
                      'datatype': 'unknown',
                      'format': None,
                      'domain': default_domain,
                      'descr': "Created by unittest",
                      }
        self.set_defaults(new_column)
        new_column_key = 'COLU-1'
        jsmodel['columns'][new_column_key] = new_column

        tmpdb = Path('/tmp/test_merge_riddle.db')
        shutil.copy(self.riddle.dbfile, tmpdb)
        with closing(dbConnect.openDBbasic(tmpdb)):
            new_model = JSModel(jsmodel)
            with self._caplog.at_level(logging.DEBUG):
                result = mergedbs.mergejson2sql(new_model, psrcname=self.srcname)

                with open('log.log', 'w') as out:
                    records = []
                    for rec in self._caplog.records:
                        records.append({'msg': rec.msg, 'lvl': rec.levelname})
                    json.dump(records, out, indent=4, sort_keys=True)
                print(f"Wrote {len(self._caplog.records)} records to 'log.log'")

        with closing(dbConnect.openDBbasic(tmpdb)) as connection:
            with closing(connection.execute("SELECT COUNT(*) FROM [tables]")) as cursor:
                r = cursor.fetchall()
                self.assertEqual(len(jsmodel['tables']), r[0][0])
                self.assertEqual(previous_table_count + 1, r[0][0])

            cols = Column.select(pwhere="colu_column_name = 'unitttest-abc'")
            with closing(connection.execute("SELECT COUNT(*) FROM [columns]")) as cursor:
                r = cursor.fetchall()
                self.assertEqual(len(jsmodel['columns']), r[0][0])
                self.assertEqual(previous_column_count + 1, r[0][0])

            with closing(connection.execute(
                    f"SELECT COUNT(*) FROM [columns] WHERE [colu_column_name] = '{column_name}'")) as cursor:
                r = cursor.fetchall()
                self.assertEqual(1, r[0][0])

        val = result.keytransl(new_table_key)
        self.assertIsInstance(val, int)
        self.assertIsNotNone(jsmodel['tables'][new_table_key], f"Expecting unaltered json")

        val = result.keytransl(new_column_key)
        self.assertIsInstance(val, int)
        self.assertIsNotNone(jsmodel['columns'][new_column_key], f"Expecting unaltered json")

    def test_merge_column_riddle(self):
        js_file = Path(self.riddle.dbdir, self.riddle.jsonfilename)
        self.assertTrue(js_file.is_file())
        with open(js_file, 'r') as src:
            jsmodel = json.load(src)

        previous = len(jsmodel['columns'])

        table_ref_key = next(iter(jsmodel['tables'].keys()))

        default_domain = \
            next(filter(lambda d: next(iter(d[1]['name'].values())) == 'Unknown', jsmodel['domains'].items()))[0]

        # apply changes to model
        new_column = {'name': 'test',
                      'table-id': table_ref_key,
                      'interface_col_id': '12-34',
                      'attributesmapped': [],
                      'mandatory': False,
                      'datatype': 'unknown',
                      'format': None,
                      'domain': default_domain,
                      'descr': "Created by unittest",
                      }

        self.set_defaults(new_column)
        new_column_key = 'COLU-1'
        jsmodel['columns'][new_column_key] = new_column
        tmpdb = Path('/tmp/test_merge_riddle.db')
        shutil.copy(self.riddle.dbfile, tmpdb)
        with closing(dbConnect.openDBbasic(tmpdb)):
            new_model = JSModel(jsmodel)
            result = mergedbs.mergejson2sql(new_model, psrcname=self.srcname)

        with closing(dbConnect.openDBbasic(tmpdb)) as connection:
            with closing(connection.execute(f"SELECT COUNT(*) FROM [columns]")) as cursor:
                r = cursor.fetchall()
                self.assertEqual(len(jsmodel['columns']), r[0][0])
                self.assertEqual(previous + 1, r[0][0])

        val = result.keytransl(new_column_key)
        self.assertIsInstance(val, int)
        self.assertIsNotNone(jsmodel['columns'][new_column_key], f"Expecting unaltered json")
        return

    def test_checkjson(self):
        jstm1 = JSModel.readfromfile(self.testmodel1.jsonfile)
        print("")
        self.assertTrue(mergedbs.checkjsonfile(self.testmodel1.jsonfile, pverbose=True))
        enti1key = list(jstm1.jsmodel["entities"].keys())[0]
        enti2key = list(jstm1.jsmodel["entities"].keys())[1]
        jstm1.jsmodel["entities"][enti1key]["category"] = "gugu000"
        jstm1.printmodel(pfilepath="/tmp", pfilename="test.json")
        self.assertFalse(mergedbs.checkjsonfile(pjsonfilepath="/tmp/test.json", pverbose=False))
        jstm1 = JSModel.readfromfile(self.testmodel1.jsonfile)
        jstm1.jsmodel["entities"][enti1key]["name"]['en'] = ''
        jstm1.jsmodel["entities"][enti2key]["name"]['en'] = ''
        jstm1.printmodel(pfilepath="/tmp", pfilename="test.json")
        self.assertFalse(mergedbs.checkjsonfile(pjsonfilepath="/tmp/test.json", pverbose=False))
        jstm1 = JSModel.readfromfile(self.testmodel1.jsonfile)
        jstm1.jsmodel["entities"][enti1key]["name"]['en'] = None
        jstm1.printmodel(pfilepath="/tmp", pfilename="test.json")
        self.assertFalse(mergedbs.checkjsonfile(pjsonfilepath="/tmp/test.json", pverbose=False))
        jstm1 = JSModel.readfromfile(self.testmodel1.jsonfile)
        del jstm1.jsmodel["categories"]["CATG1"]
        jstm1.printmodel(pfilepath="/tmp", pfilename="test.json")
        with self._caplog.at_level(level=logging.INFO):
            self.assertFalse(mergedbs.checkjsonfile(pjsonfilepath="/tmp/test.json", pverbose=False))
            for c in self._caplog.records:
                print(c.getMessage())

        with self._caplog.at_level(logging.DEBUG):
            self.assertTrue(mergedbs.checkjsonfile(pjsonfilepath=self.testmodel2.jsonfile, pverbose=False))
            self.assertTrue(mergedbs.checkjsonfile(pjsonfilepath=self.testmodelcrm.jsonfile, pverbose=False))
            self.assertTrue(mergedbs.checkjsonfile(pjsonfilepath=self.riddle.jsonfile, pverbose=False))

    def set_defaults(self, element: dict):
        defaults = {'uc': 'test', 'dc': '2022-02-02',
                    'um': None, 'dm': None,
                    'publstatus': None,
                    'userdefprops': {},
                    'minzoomlevel': None, 'maxzoomlevel': None,
                    'referencedby': [],
                    'sourceref': {}
                    }
        element.update(defaults)
        return

if __name__ == '__main__':
    unittest.main()
