import os
import unittest
from tools.LANGTRANSL import exportdata,importdata,langexceldata
from SSOT_db.IM_JSON import JSModel
import SSOT_infra.tests.integration as tb

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tm2 = tb.Testmodel(tb.TESTMODEL2)
        self.tm2.initDB(palways=True)

    def test_metainfo(self):
        mi = langexceldata.Metainfo(modelname='test')
        print (mi)

    def test_calls(self):
        with self.assertRaises(Exception) as exp:
            exportdata.createlangexcel('gugus')
        print ("")

        data = exportdata.Exportdata(pjsonfile=self.tm2.jsonfile).getdata()
        for key in ('ENTI118-name','ENTI118-descr','ENTI118-tooltip','ENTI111-synonym-1',
                    'ATTR123-name','ATTR123-descr','ATTR123-tooltip',
                    'DOMA90-name','DOMA90-descr','ENTI119-example-2'):
            self.assertTrue(key in data)

        destfilename=os.path.join(self.tm2.dbdir,self.tm2.modelname+'.xlsx')
        if os.path.exists(destfilename):
            os.remove(destfilename)
        exportdata.createlangexcel(self.tm2.jsonfile)
        self.assertTrue(os.path.exists(destfilename))
        os.remove(destfilename)
        exportdata.createlangexcel(self.tm2.jsonfile,pdest=self.tm2.dbdir)
        self.assertTrue(os.path.exists(destfilename))
        os.remove(destfilename)
        exportdata.createlangexcel(self.tm2.jsonfile,pdest=destfilename)
        self.assertTrue(os.path.exists(destfilename))
        #os.remove(destfilename)

        return

    def test_importdata(self):
        with self.assertRaises(Exception) as exp:
            importdata.importlangexcel('gugus')
        print ("")
        impfilename = os.path.join(self.tm2.dbdir, self.tm2.modelname + '.xlsx')
        importdata.importlangexcel(impfilename)


if __name__ == '__main__':
    unittest.main()
