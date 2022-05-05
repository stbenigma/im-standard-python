import datetime
import json
import logging
import shutil
import unittest
from contextlib import closing
from pathlib import Path

import pytest

from LOAD_MODELS.LOAD_INFRA import mergedbs
from SSOT_db.IM_JSON import JSModel, sql2json, jsbusinessrule, jsguid, jsmergetosql
from SSOT_db.SQL_INFRA import dbConnect
from SSOT_db.IM_OBJECTS import BusinessRule, Attribute, Table
import sqlite3
import SSOT_infra.tests.integration as testsrc
from LOAD_MODELS.LOAD_INFRA import mergedbs, fillmodel2db
from LOAD_MODELS.LOAD_ODM.transferModel import transferODMModel
from SSOT_db import createnewDB
from SSOT_db.IM_JSON import JSModel, sql2json, jsbusinessrule, jsguid, jsactorroles
from SSOT_db.IM_OBJECTS import BusinessRule, Attribute, Table, Actorrole,Domain,Languagetext,Entity
from SSOT_db.SQL_INFRA import dbConnect
from SSOT_infra import parameters



class TestMergeJson(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def setUp(self) -> None:
        self.testmodelcrm: testsrc.Testmodel = testsrc.Testmodel(testsrc.CRMTEST)
        self.testmodel1: testsrc.Testmodel = testsrc.Testmodel(testsrc.TESTMODEL1)
        self.testmodel2: testsrc.Testmodel = testsrc.Testmodel(testsrc.TESTMODEL2)
        self.riddle: testsrc.Testmodel = testsrc.Testmodel(testsrc.RIDDLE)
        return

    def test_merge(self):
        dbConnect.openDB(self.testmodelcrm.dbfile, pversioncheck=False)
        self.newbrname = 'test-BR10'
        self.crmmodel = JSModel(pmodel=sql2json(pdbname=self.testmodelcrm.modelname))
        try:
            buru = BusinessRule(buru_name=self.newbrname,
                                buru_rule='nichts',
                                buru_level='ATTR',
                                buru_type='CHECK',
                                buru_uc='me',
                                buru_dc=datetime.datetime.now(),
                                srcid='9999',
                                srcname='test_mergejs')
            burujs = jsbusinessrule.businessrule2js(buru, plangs=('de', 'en', 'fr'))
            attrid = jsguid('ATTR', Attribute.select()[0].attr_id)
            tablid = jsguid('TABL', Table.select()[0].tabl_id)
            burujs['elements'] = {attrid: {"r/w": "R"},
                                  tablid: {"r/w": "R"}
                                  }
            burujs['sourceref']['test_mergejs'][1] = str(datetime.datetime.now())
            self.crmmodel.jsmodel['businessrules']["BURU9999"] = burujs

            with self._caplog.at_level(logging.DEBUG):
                mergedbs.mergejson2sql(pmodeljson=self.crmmodel)

            """generate json from merged DB"""
            newjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
            newburuid = newjson.jsmodel['attributes'][attrid]['businessrules+'][0]
            self.assertEqual(newburuid, newjson.jsmodel['tables'][tablid]['businessrules+'][0])

            newburu = newjson.getbyid(newburuid)
            self.assertTrue(newburuid in newjson.jsmodel['businessrules'])
            self.assertTrue(attrid in newburu['elements'])
            self.assertTrue(tablid in newburu['elements'])

            self.assertEqual('9999', newburu['sourceref']['test_mergejs'][0])

            # now test an update
            updjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
            updburu = updjson.getelements('businessrules')[newburuid]
            updburu['errormsg']['en'] = "new error message"
            updburu['um'] = "meandmyself"
            del updburu['elements'][tablid]
            updburu['sourceref']['test_updatemergejs'] = ['9999-111',str(datetime.datetime.now())]
            mergedbs.mergejson2sql(pmodeljson=updjson)
            #now check the merge
            newjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
            newburu = newjson.getbyid(newburuid)
            self.assertEqual('9999-111', newburu['sourceref']['test_updatemergejs'][0])
            self.assertEqual(newburu['errormsg']['en'], "new error message")
            self.assertTrue(attrid in newburu['elements'])
            self.assertFalse(tablid in newburu['elements'])
            # self.assertEqual("meandmyself",newburu['um'])
        finally:
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
        parameters.initparam(pbasedirec=self.testmodel2.modeldir, pparamfile=self.testmodel2.paramfile)
        #test dryrun on exisisting files
        dbConnect.openDB(pfilepath=self.testmodel2.dbfile)
        curmodel = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
        dbConnect.closeDB()

        capturedOutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  # and redirect stdout.
        newjson = mergedbs.mergejs2db(pdbfile=self.testmodel2.dbfile,pmodel=curmodel,
                                      pverbose=True,pdryrun=True)
        sys.stdout = sys.__stdout__  # Reset redirect.
        stdprint = capturedOutput.getvalue()
        self.assertTrue(stdprint.startswith("***** dry merge-run on db"))

        #set up my model in memory to reuse it for several tests
        createnewDB(pdbfilepath=None)  # create in memory
        originaldbconn = dbConnect.getdbcon()
        # create transferModel.transferODMModel
        fillmodel2db.filldb(transferODMModel)
        firstjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))


        # create copy of filled db
        seconddbconn = mergedbs.connecttodbcopy()
        # first merge with itself
        result = mergedbs.mergejson2sql(pmodeljson=firstjson)
        for c in result.changes:
            print(c)
        self.assertEqual(0, result.updatecnt)
        self.assertEqual(0, result.insertcnt)
        self.assertEqual(0, result.deletecnt)
        self.assertEqual(0, len(result.warnings))
        self.assertEqual(0, len(result.errors))

        firstjson.jsmodel["entities"]["ENTI118"]["name"]["de"] += 'XX'
        result = mergedbs.mergejson2sql(pmodeljson=firstjson,pverbose=True,psrcname="TEST")
        for c in result.changes:
            print(c)
        self.assertEqual(1, result.updatecnt)
        self.assertEqual(0, result.insertcnt)
        self.assertEqual(0, result.deletecnt)

        dbConnect.closeDB()

        return

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
            mergedbs.mergejson2db(pmodeljson=new_model)

        with closing(dbConnect.openDBbasic(tmpdb)) as connection:
            with closing(connection.execute(f"SELECT COUNT(*) FROM [columns]")) as cursor:
                r = cursor.fetchall()
                self.assertEqual(len(jsmodel['columns']), r[0][0])
                self.assertEqual(previous + 1, r[0][0])

        val = jsmergetosql.keytransl(new_column_key)
        self.assertIsInstance(val, int)
        self.assertIsNotNone(jsmodel['columns'][new_column_key], f"Expecting unaltered json")

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
                mergedbs.mergejson2db(pmodeljson=new_model)
                with open('unittest-log.json', 'w') as out:
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

            with closing(connection.execute("SELECT COUNT(*) FROM [columns]")) as cursor:
                r = cursor.fetchall()
                self.assertEqual(len(jsmodel['columns']), r[0][0])
                self.assertEqual(previous_column_count + 1, r[0][0])

            with closing(connection.execute(
                    f"SELECT COUNT(*) FROM [columns] WHERE [colu_column_name] = '{column_name}'")) as cursor:
                r = cursor.fetchall()
                self.assertEqual(1, r[0][0])

        val = jsmergetosql.keytransl(new_table_key)
        self.assertIsInstance(val, int)
        self.assertIsNotNone(jsmodel['tables'][new_table_key], f"Expecting unaltered json")

        val = jsmergetosql.keytransl(new_column_key)
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
            mergedbs.mergejson2db(pmodeljson=new_model)

        with closing(dbConnect.openDBbasic(tmpdb)) as connection:
            with closing(connection.execute(f"SELECT COUNT(*) FROM [columns]")) as cursor:
                r = cursor.fetchall()
                self.assertEqual(len(jsmodel['columns']), r[0][0])
                self.assertEqual(previous + 1, r[0][0])

        val = jsmergetosql.keytransl(new_column_key)
        self.assertIsInstance(val, int)
        self.assertIsNotNone(jsmodel['columns'][new_column_key], f"Expecting unaltered json")

    def set_defaults(self, element: dict):
        defaults = {'uc': 'test', 'dc': '2022-02-02',
                    'um': None, 'dm': None,
                    'publstatus': None,
                    'userdefprops': {},
                    'minzoomlevel': None, 'maxzoomlevel': None,
                    'referencedby': [],
                    'sourceref': {
                        'JSON': ['test_merge_riddle 1', '2022-04-28 15:38:01.1'],
                    }}
        element.update(defaults)

    if __name__ == '__main__':
        unittest.main()
