import difflib
import json
import unittest
from SSOT_db.IM_OBJECTS import Modelelement
from SSOT_db.IM_JSON import JSModel,FILTEREDJSModel,printJSON
import  SSOT_infra.tests.integration as testsrc

def jsonequal(a, b):
    type_a = type(a)
    type_b = type(b)

    if type_a != type_b:
        return False

    if isinstance(a, dict):
        if len(a) != len(b):
            return False
        for key in a:
            if key not in b:
                return False
            if not jsonequal(a[key], b[key]):
                return False
        return True

    elif isinstance(a, list):
        if len(a) != len(b):
            return False
        while len(a):
            x = a.pop()
            try:
                index = b.index(x)
            except:
                return False
            del b[index]
        return True

    else:
        return a == b


class MyTestCase(unittest.TestCase):
    def setUp(self):
        from LOAD_MODELS.LOAD_ODM.tests.test_fillDB import create_testmodel1
        testmodelname, testdir, dbfilepath = testsrc.testmodel1()
        create_testmodel1(testmodelname=testmodelname,testdir=testdir,dbfilepath=dbfilepath,new=True)
        self.model = JSModel.readfromfile(dbfilepath.__str__().replace("db","json"))
        self.emptyfilter = FILTEREDJSModel(pmodel=self.model.jsmodel)
        self.draftfilter = FILTEREDJSModel(ppublstatus=Modelelement.DRAFT,pmodel=self.model.jsmodel)
        self.gtopfilter = FILTEREDJSModel(ppublstatus=Modelelement.GTOP,pmodel=self.model.jsmodel)
        self.publfilter = FILTEREDJSModel(ppublstatus=Modelelement.PUBL,pmodel=self.model.jsmodel)
        printJSON(self.model.jsmodel,pfilepath="/Users/stb/Downloads",pfilename="model")
        printJSON(self.emptyfilter.jsmodel,pfilepath="/Users/stb/Downloads",pfilename="jsonempty")
        printJSON(self.draftfilter.jsmodel,pfilepath="/Users/stb/Downloads",pfilename="jsondraft")
        printJSON(self.gtopfilter.jsmodel,pfilepath="/Users/stb/Downloads",pfilename="jsongtop")
        printJSON(self.publfilter.jsmodel,pfilepath="/Users/stb/Downloads",pfilename="jsonpubl")


    def test_publish_function(self):
        element = {"id":0}
        self.assertTrue(self.emptyfilter._publishable(element))
        self.assertTrue(self.gtopfilter._publishable(element))
        element["publstatus"]=None
        self.assertTrue(self.emptyfilter._publishable(element))
        self.assertTrue(self.publfilter._publishable(element))
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
        compidlist:set = {key for key in self.model.jsmodel[JSModel.elemtype2label("ENTI")].keys()}
        self.assertSetEqual(compidlist,compidlist.intersection(self.draftfilter.getfilteredidlist()))

        compidlist:set = {key for key,val in self.model.jsmodel[JSModel.elemtype2label("ENTI")].items()
                          if val["publstatus"] in ("GTOP","PUBL")}
        self.assertSetEqual(compidlist,compidlist.intersection(self.gtopfilter.getfilteredidlist()))

        compidlist:set = {key for key,val in self.model.jsmodel[JSModel.elemtype2label("ENTI")].items()
                          if val["publstatus"] in ("PUBL")}
        self.assertSetEqual(compidlist,compidlist.intersection(self.publfilter.getfilteredidlist()))


    def test_unchanged_model(self):
        #check with empty (default) filter
        self.assertTrue(jsonequal(self.model.jsmodel, self.emptyfilter.jsmodel))

        # DAFT includes all stati, no diagramlist do no filter diagrams
        self.assertTrue(jsonequal(self.model.jsmodel, self.draftfilter.jsmodel))

    def test_filtered_models(self):
        # do not select any diagram
        nodiag = FILTEREDJSModel(self.model.jsmodel,pimdiagrams=[])
        self.assertEqual(0,len(nodiag.jsmodel["diagrams"]))

        textjson = json.dumps(self.draftfilter.jsmodel)
        self.assertRegex(textjson,r'.*"ENTI92".*')
        self.assertRegex(textjson,r'.*"ENTI100".*')
        self.assertRegex(textjson,r'.*"ENTI105".*')

        textjson = json.dumps(self.gtopfilter.jsmodel)
        self.assertNotRegex(textjson,r'.*"ENTI92".*')
        self.assertRegex(textjson,r'.*"ENTI100".*')
        self.assertRegex(textjson,r'.*"ENTI105".*')

        textjson = json.dumps(self.publfilter.jsmodel)
        self.assertNotRegex(textjson,r'.*"ENTI92".*')
        self.assertNotRegex(textjson,r'.*"ENTI100".*')
        self.assertRegex(textjson,r'.*"ENTI105".*')
        return


if __name__ == '__main__':
    unittest.main()
