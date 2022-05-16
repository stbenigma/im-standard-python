import os
import unittest

import SSOT_infra.tests.integration as tb
from tools.LANGTRANSL import exportdata, importdata, langexceldata


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tm2 = tb.Testmodel(tb.TESTMODEL2)
        self.tm2.initDB(palways=True)

    def test_metainfo(self):
        self.assertTrue(langexceldata.strislang('xx'))
        self.assertFalse(langexceldata.strislang('x'))
        self.assertFalse(langexceldata.strislang(None))
        self.assertFalse(langexceldata.strislang(''))
        self.assertFalse(langexceldata.strislang('xY'))

        mi = langexceldata.Metainfo(modelname='test')
        print(mi)
        return

    def test_excelcheck(self):
        from openpyxl import Workbook,styles
        testdata = [
        ["Key", "de", "fr", "Description", "Comments"],
        ['ENTI118-name','D1','F1','',None],
        ['ENTI118-descr','DD1','DD1','',''],
        ['ENTI118-tooltip',None,None,None,None],
        ['ENTI111-synonyms-1','DS1','FS1',None,None],
        ['ATTR123-name','A1','FA1',None,None],
        ['ATTR123-descr',None,None,None,None],
        ['ATTR123-tooltip',"""asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfsdfadfas
                        adfasföajsl adöslkfj aösdlkfj aösldkjf aösldkjf öalsdkjf d""",'x','',''],
        ['DOMA90-name','D1','D1',None,None],
        ['DOMA90-descr',None,None,None,None],
        ['ENTI119-examples-2','E1','E1',None,None]
        ]
        wb = Workbook()
        ws= wb.active
        for r in testdata:
            ws.append(r)
        #destfilename=self.tm2.dbdir/"testexcel.xlsx"
        #wb.save(filename=destfilename)
        excel:Lan = Langexceldata()
        excel.analyzeheader(ws['1'])
        jsonfile = getjsonfile(pmodeldb, pjsonfile=self.tm2.jsonfile)
        importdata.checkentries(pws=ws,pexcel=excel,pjson=json,pkeyidx=excel.keyrowidx())
        #os.remove(destfilename)
        return

    def test_calls(self):
        with self.assertRaises(Exception) as exp:
            exportdata.createlangexcel('gugus')
        print("")

        data = exportdata.Exportdata(pjsonfile=self.tm2.jsonfile).getdata()
        for key in ('ENTI118-name', 'ENTI118-descr', 'ENTI118-tooltip', 'ENTI111-synonyms-1',
                    'ATTR123-name', 'ATTR123-descr', 'ATTR123-tooltip',
                    'DOMA90-name', 'DOMA90-descr', 'ENTI119-examples-2'):
            self.assertTrue(key in data)

        destfilename = os.path.join(self.tm2.dbdir, self.tm2.modelname + '.xlsx')
        if os.path.exists(destfilename):
            os.remove(destfilename)
        exportdata.createlangexcel(self.tm2.jsonfile)
        self.assertTrue(os.path.exists(destfilename))
        os.remove(destfilename)
        exportdata.createlangexcel(self.tm2.jsonfile, pdest=self.tm2.dbdir)
        self.assertTrue(os.path.exists(destfilename))
        os.remove(destfilename)
        exportdata.createlangexcel(self.tm2.jsonfile, pdest=destfilename)
        self.assertTrue(os.path.exists(destfilename))
        # os.remove(destfilename)

        return

    def test_importdata(self):
        with self.assertRaises(Exception) as exp:
            importdata.importlangexcel('gugus')
        print("")
        impfilename = os.path.join(self.tm2.dbdir, self.tm2.modelname + '.xlsx')
        importdata.importlangexcel(impfilename)


if __name__ == '__main__':
    unittest.main()
