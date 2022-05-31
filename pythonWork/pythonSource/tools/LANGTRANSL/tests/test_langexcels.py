import json
import os
import tempfile
import unittest

from tools.LANGTRANSL.exportdata import *
from tools.LANGTRANSL.importdata import *
from tools.LANGTRANSL.langexceldata import *
import SSOT_infra.tests.integration as tb
from LOAD_MODELS.LOAD_INFRA import mergedbs


def nocomments(pws):
    for r in pws.iter_rows(min_row=2):
        if r[5].value != '':
            return False
    return True


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tm2 = tb.Testmodel(tb.TESTMODEL2)
        self.tm2.initDB(palways=True)

        with open(self.tm2.jsonfile, 'r') as tm2file:
            self.tm2json = json.load(tm2file)

        self.testdata = [['Key', 'de', 'en', 'fr', 'Description', 'Comments']]
        entities = []
        for key, val in self.tm2json['entities'].items():
            if val['name']['de'] in ('Hauptentität', 'Einzelentität', 'Rollen-Entität 2'):
                entities.append(key)
                self.testdata.append([key + '-name', val['name']['de'], val['name']['en'], val['name']['fr'],
                                      val['name']['de'] + ' Entity-Name', ''])
                self.testdata.append([key + '-descr', val['descr']['de'], val['descr']['en'], val['descr']['fr'],
                                      val['name']['de'] + ' Entity-Description', ''])
                self.testdata.append(
                    [key + '-tooltip', val['tooltip']['de'], val['tooltip']['en'], val['tooltip']['fr'],
                     val['name']['de'] + ' Entity-Tooltip', ''])
                for idx, syno in enumerate(val['synonyms'], start=1):
                    self.testdata.append(
                        [key + '-synonyms-' + str(idx), val['synonyms'][idx - 1]['de'], val['synonyms'][idx - 1]['en'],
                         val['synonyms'][idx - 1]['fr'],
                         val['name']['de'] + '->' + val['synonyms'][idx - 1]['de'] + '  - Synonym-' + str(idx), ''])
                for idx, expl in enumerate(val['examples'], start=1):
                    self.testdata.append(
                        [key + '-examples-' + str(idx), val['examples'][idx - 1]['de'], val['examples'][idx - 1]['en'],
                         val['examples'][idx - 1]['fr'],
                         val['name']['de'] + '  - Example-' + str(idx), ''])
        for key, val in self.tm2json['attributes'].items():
            if val['name']['de'] in ('Name', 'erste Erscheinung'):
                self.testdata.append([key + '-name', val['name']['de'], val['name']['en'], val['name']['fr'],
                                      val['name']['de'] + ' Attribut-Name', ''])
                self.testdata.append([key + '-descr', val['descr']['de'], val['descr']['en'], val['descr']['fr'],
                                      val['name']['de'] + ' Attribut-Description', ''])
            for idx, expl in enumerate(val['examples'], start=1):
                self.testdata.append(
                    [key + '-examples-' + str(idx), val['examples'][idx - 1]['de'], val['examples'][idx - 1]['en'],
                     val['examples'][idx - 1]['fr'],
                     val['name']['de'] + '  - Example-' + str(idx), ''])
        for key, val in self.tm2json['domains'].items():
            if val['name']['de'] in ('XMLTYPE', 'email Address'):
                self.testdata.append([key + '-name', val['name']['de'], val['name']['en'], val['name']['fr'],
                                      val['name']['de'] + ' Domain-Name', ''])
                self.testdata.append([key + '-descr', val['descr']['de'], val['descr']['en'], val['descr']['fr'],
                                      val['name']['de'] + ' Domain-Description', ''])
        for key, val in self.tm2json['relations'].items():
            if (val["to-from"]['enti'] in entities) or (val["from-to"]['enti'] in entities):
                self.testdata.append([key + '-tofrom', val['to-from']['assoc']['de'], val['to-from']['assoc']['en'],
                                      val['to-from']['assoc']['fr'],
                                      val['name'] + ' to-from', ''])
            self.testdata.append([key + '-fromto', val['from-to']['assoc']['de'], val['from-to']['assoc']['en'],
                                  val['from-to']['assoc']['fr'],
                                  val['name'] + ' from-to', ''])
        self.wb = Workbook()
        self.testws = self.wb.active
        for r in self.testdata:
            self.testws.append(r)
        # destfilename=self.tm2.dbdir/"testexcel.xlsx"
        # wb.save(filename=destfilename)
        self.testexcel = Langexceldata()
        self.testexcel.analyzeheader(self.testws['1'])
        self.testjson = JSModel.readfromfile(
            pfilename=self.tm2.jsonfile)

    def test_metainfo(self):
        self.assertTrue(strislang('xx'))
        self.assertFalse(strislang('x'))
        self.assertFalse(strislang(None))
        self.assertFalse(strislang(''))
        self.assertFalse(strislang('xY'))

        mi = Metainfo(modelname='test')
        return

    def test_excelcheck(self):

        # all but header is returned as OK rows
        self.assertEqual(len(self.testdata) - 1,
                         len(checkentries(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)))
        self.assertTrue(nocomments(self.testws))

        # invalid key
        self.testws.cell(row=2, column=1).value = 'gugus'
        self.assertEqual(len(self.testdata) - 2,
                         len(checkentries(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)))
        self.assertFalse(nocomments(self.testws))
        self.testws.cell(row=2, column=1).value = self.testdata[1][0]

        # invalid key
        self.testws.cell(row=2, column=1).value = 'ENTI99999-name'
        self.assertEqual(len(self.testdata) - 2,
                         len(checkentries(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)))
        self.assertFalse(nocomments(self.testws))
        self.testws.cell(row=2, column=1).value = self.testdata[1][0]

        # invalid key
        self.testws.cell(row=2, column=1).value = 'ENTI99999-name'
        self.assertEqual(len(self.testdata) - 2,
                         len(checkentries(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)))
        self.assertFalse(nocomments(self.testws))
        self.testws.cell(row=2, column=1).value = self.testdata[1][0]

        # invalid key
        self.testws.cell(row=2, column=1).value = 'ENTI-synonyms-a'
        self.assertEqual(len(self.testdata) - 2,
                         len(checkentries(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)))
        self.assertFalse(nocomments(self.testws))
        self.testws.cell(row=2, column=1).value = self.testdata[1][0]

        # invalid key
        self.testws.cell(row=2, column=1).value = 'ENTI-synonyms-99'
        self.assertEqual(len(self.testdata) - 2,
                         len(checkentries(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)))
        self.assertFalse(nocomments(self.testws))
        self.testws.cell(row=2, column=1).value = self.testdata[1][0]

        # invalid key
        self.testws.cell(row=2, column=1).value = 'ENTI-synonyms'
        self.assertEqual(len(self.testdata) - 2,
                         len(checkentries(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)))
        self.assertFalse(nocomments(self.testws))
        self.testws.cell(row=2, column=1).value = self.testdata[1][0]

        # invalid key
        self.testws.cell(row=2, column=1).value = 'RELA-to-from'
        self.assertEqual(len(self.testdata) - 2,
                         len(checkentries(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)))
        self.assertFalse(nocomments(self.testws))
        self.testws.cell(row=2, column=1).value = self.testdata[1][0]

        # empty not null column de
        self.testws.cell(row=2, column=2).value = ''
        self.assertEqual(len(self.testdata) - 2,
                         len(checkentries(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)))
        self.assertFalse(nocomments(self.testws))
        self.testws.cell(row=2, column=2).value = self.testdata[1][1]
        # empty not null column en
        self.testws.cell(row=2, column=3).value = ''
        self.assertEqual(len(self.testdata) - 2,
                         len(checkentries(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)))
        self.assertFalse(nocomments(self.testws))
        self.testws.cell(row=2, column=3).value = self.testdata[1][2]

        # duplicate name de
        self.testws.cell(row=5, column=2).value = self.testdata[1][1]
        self.assertEqual(len(self.testdata) - 2,
                         len(checkentries(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)))
        self.assertFalse(nocomments(self.testws))
        self.testws.cell(row=5, column=2).value = self.testdata[4][1]

        # duplicate name fr
        self.testws.cell(row=5, column=4).value = self.testdata[1][3]
        self.assertEqual(len(self.testdata) - 2,
                         len(checkentries(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)))
        self.assertFalse(nocomments(self.testws))
        self.testws.cell(row=5, column=4).value = self.testdata[4][3]

        # two errors in line
        self.testws.cell(row=5, column=4).value = self.testdata[1][3]
        self.testws.cell(row=5, column=3).value = self.testdata[1][2]
        self.assertEqual(len(self.testdata) - 2,
                         len(checkentries(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)))
        self.wb.save(self.tm2.dbdir / "testexcel.xlsx")
        self.assertEqual(redfill.fgColor.value, self.testws.cell(row=5, column=3).fill.fgColor.value)
        self.assertEqual(redfill.fgColor.value, self.testws.cell(row=5, column=4).fill.fgColor.value)
        self.assertFalse(nocomments(self.testws))
        self.testws.cell(row=5, column=4).value = self.testdata[4][3]
        self.testws.cell(row=5, column=3).value = self.testdata[4][2]

        # duplicate attrnames are no error
        self.testws.cell(row=14, column=2).value = self.testws.cell(row=17, column=2).value
        self.assertEqual(len(self.testdata) - 1,
                         len(checkentries(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)))
        self.wb.save(self.tm2.dbdir / "testexcel.xlsx")
        self.assertEqual(emptyfill.fgColor.value, self.testws.cell(row=21, column=2).fill.fgColor.value)
        self.assertTrue(nocomments(self.testws))
        self.testws.cell(row=14, column=2).value = self.testdata[13][1]

        # all comments are removed if it checks ok
        self.assertEqual(len(self.testdata) - 1,
                         len(checkentries(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)))
        self.assertTrue(nocomments(self.testws))
        # os.remove(self.tm2.dbdir / "testexcel.xlsx")
        return

    def test_calls(self):
        with self.assertRaises(Exception) as exp:
            createlangexcel('gugus')
        print("")

        data = Exportdata(pjsonfile=self.tm2.jsonfile).getdata()
        for key, val in self.tm2json['entities'].items():
            self.assertTrue(key + '-name' in data)
            self.assertTrue(key + '-descr' in data)
            self.assertTrue(key + '-tooltip' in data)
            for idx, syno in enumerate(val['synonyms'], start=1):
                self.assertTrue(key + '-synonyms-' + str(idx) in data)
            for idx, expl in enumerate(val['examples'], start=1):
                self.assertTrue(key + '-examples-' + str(idx) in data)
        for key, val in self.tm2json['attributes'].items():
            self.assertTrue(key + '-name' in data)
            self.assertTrue(key + '-descr' in data)
            self.assertTrue(key + '-tooltip' in data)
            for idx, expl in enumerate(val['examples'], start=1):
                self.assertTrue(key + '-examples-' + str(idx) in data)
        for key in self.tm2json['domains'].keys():
            self.assertTrue(key + '-name' in data)
            self.assertTrue(key + '-descr' in data)
        for key in self.tm2json['relations'].keys():
            self.assertTrue(key + '-tofrom' in data)
            self.assertTrue(key + '-fromto' in data)

        destfilename = os.path.join(self.tm2.dbdir, self.tm2.modelname + '.xlsx')
        if os.path.exists(destfilename):
            os.remove(destfilename)
        createlangexcel(self.tm2.jsonfile)
        self.assertTrue(os.path.exists(destfilename))
        os.remove(destfilename)
        createlangexcel(self.tm2.jsonfile, pdest=self.tm2.dbdir)
        self.assertTrue(os.path.exists(destfilename))
        os.remove(destfilename)
        createlangexcel(self.tm2.jsonfile, pdest=destfilename)
        self.assertTrue(os.path.exists(destfilename))
        # os.remove(destfilename)

        return

    def test_exceljson(self):

        # no changes
        changes, newjson = mergeexcel2json(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)
        self.assertEqual(0, changes)
        for key, val in newjson.getelements('entities').items():
            self.assertEqual(self.testjson.getbyid(key)['name']['de'], val['name']['de'])
            self.assertEqual(self.testjson.getbyid(key)['name']['fr'], val['name']['fr'])
            self.assertEqual(self.testjson.getbyid(key)['name']['en'], val['name']['en'])
            self.assertEqual(self.testjson.getbyid(key)['tooltip']['de'], val['tooltip']['de'])
        for key, val in newjson.getelements('domains').items():
            self.assertEqual(self.testjson.getbyid(key)['name']['de'], val['name']['de'])
            self.assertEqual(self.testjson.getbyid(key)['name']['fr'], val['name']['fr'])
            self.assertEqual(self.testjson.getbyid(key)['name']['en'], val['name']['en'])
            self.assertEqual(self.testjson.getbyid(key)['descr']['de'], val['descr']['de'])

        # change 1 name
        entiid = self.testws.cell(row=2, column=1).value.split('-')[0]
        self.testws.cell(row=2, column=2).value = 'gugus'
        changes, newjson = mergeexcel2json(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)
        # self.wb.save(self.tm2.dbdir / "testexcel.xlsx")
        self.assertEqual(1, changes)
        self.assertTrue(nocomments(self.testws))
        self.assertEqual(greenfill.fgColor.value, self.testws.cell(row=2, column=2).fill.fgColor.value)
        self.testws.cell(row=2, column=2).value = self.testdata[1][1]
        self.testws.cell(row=2, column=2).fill = emptyfill
        self.assertEqual('gugus', newjson.getbyid(entiid)['name']['de'])

        changes, newjson = mergeexcel2json(pws=self.testws, pexcel=self.testexcel, pjson=newjson)
        # self.wb.save(self.tm2.dbdir / "testexcel.xlsx")
        self.assertEqual(1, changes)
        self.assertTrue(nocomments(self.testws))
        self.assertEqual(greenfill.fgColor.value, self.testws.cell(row=2, column=2).fill.fgColor.value)
        self.assertEqual(self.testdata[1][1], newjson.getbyid(entiid)['name']['de'])

        # second change
        self.testws.cell(row=2, column=2).value = 'gugus2'
        self.testws.cell(row=4, column=3).value = 'Tooltip Test'
        changes, newjson = mergeexcel2json(pws=self.testws, pexcel=self.testexcel, pjson=self.testjson)
        # self.wb.save(self.tm2.dbdir / "testexcel.xlsx")
        self.assertEqual(2, changes)
        self.assertEqual(greenfill.fgColor.value, self.testws.cell(row=2, column=2).fill.fgColor.value)
        self.assertEqual(greenfill.fgColor.value, self.testws.cell(row=4, column=3).fill.fgColor.value)
        self.testws.cell(row=2, column=2).value = self.testdata[1][1]
        self.testws.cell(row=4, column=3).value = self.testdata[3][2]
        self.assertEqual('gugus2', newjson.getbyid(entiid)['name']['de'])
        self.assertEqual('Tooltip Test', newjson.getbyid(entiid)['tooltip']['en'])
        # os.remove(self.tm2.dbdir / "testexcel.xlsx")

    def test_importdata(self):
        import shutil
        from SSOT_db.SQL_INFRA import dbConnect
        from SSOT_db.IM_OBJECTS import Entity

        resultjson = str(self.tm2.jsonfile).replace('.json', '_result.json')

        with self.assertRaises(Exception) as exp:
            importlangexcel('gugus')
        print("")
        impfilename = os.path.join(self.tm2.dbdir, self.tm2.modelname + '.xlsx')
        importlangexcel(impfilename)
        self.assertFalse(os.path.exists(resultjson))  # nothing changed, no files generated

        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            shutil.copyfile(impfilename, 'myinput.xlsx')
            shutil.copyfile(self.tm2.jsonfile, 'myjson.json')
            shutil.copyfile(self.tm2.dbfile, 'testmodel-2.db')
            wb = load_workbook(filename='myinput.xlsx')
            ws = wb.active
            a1comment = ws["A1"].comment
            self.assertIsNotNone(a1comment)
            a1comment.text = a1comment.text.replace(str(self.tm2.jsonfile), 'myjson.json')
            excel = Langexceldata()
            excel.analyzecomment('' if a1comment is None else a1comment.text)
            self.assertEqual('myjson.json', excel.getmetainfo().getjsonfile())
            ws["A1"].comment = a1comment
            wb.save(filename="myinput.xlsx")
            # wb.save(filename=impfilename.replace('.xlsx','_test.xlsx'))
            changes = importlangexcel("myinput.xlsx")
            self.assertEqual(0, changes)
            # shutil.copyfile("myinput_result.xlsx",self.tm2.dbdir/"myinput_result.xlsx")
            self.assertFalse(os.path.exists("myjson_result.json"))
            self.assertFalse(os.path.exists("myinput_result.xlsx"))

            # teste Änderung im Excel
            cell = ws["B2"]
            cell.value = cell.value + "XX"
            testentityname = cell.value
            cell = ws["C2"]
            cell.value = cell.value + "YY"
            wb.save(filename="myinput.xlsx")
            wb.save(filename=impfilename.replace('.xlsx', '_test.xlsx'))
            changes = importlangexcel("myinput.xlsx")
            self.assertTrue(changes > 0)

            resultjson = JSModel.readfromfile(pfilename="myjson_result.json")
            mergedbs.mergejs2db(pmodel=resultjson, psrcname="TRANSL", pverbose=False, pdbfile="testmodel-2.db")
            self.assertTrue(os.path.exists("myjson_result.json"))
            self.assertTrue(os.path.exists("myinput_result.xlsx"))

            dbConnect.openDB(pfilepath="testmodel-2.db")
            enti = Entity().getbyuk(enti_name=testentityname)
            self.assertTrue(enti.enti_name.endswith("XX"))
            self.assertTrue(enti.enti_name_l['en'].endswith("YY"))

            dbConnect.closeDB()

            shutil.copyfile("myinput_result.xlsx", self.tm2.dbdir / "myinput_result.xlsx")
            shutil.copyfile("myinput.xlsx", self.tm2.dbdir / "myinput.xlsx")
            shutil.copyfile("myjson_result.json", self.tm2.dbdir / "myjson_result.json")

            # self.assertTrue(os.path.exists(resultjson))

    def test_translateexcel(self):
        with self.assertRaises(Exception) as exp:
            translateexcel(None, None)

        if os.path.exists("/Users/stb/.deepl/deeplauthid"):
            with open("/Users/stb/.deepl/deeplauthid") as d:
                deeplid = d.read()
        else:
            print("******* Test with real deeplid skipped")
            return

        with self.assertRaises(Exception) as exp:
            translateexcel(None, deeplid)

        with self.assertRaises(Exception) as exp:
            translateexcel("testexcel.xlsx", deeplid, pmainlanguage=None)

        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            self.wb.save("testexcel.xlsx")
            self.assertEqual(0, translateexcel("testexcel.xlsx", deeplid, pmainlanguage='de'))

            switch = True
            changes = 0
            for row in self.wb.active.iter_rows(min_row=2):
                cell = row[2 if switch else 3]
                if nvl(cell.value, '') != '':
                    changes += 1
                    cell.value = ''
                switch = not switch
            self.wb.save("testexcel.xlsx")
            self.assertEqual(changes, translateexcel("testexcel.xlsx", deeplid, pmainlanguage='de'))

        return


if __name__ == '__main__':
    unittest.main()
