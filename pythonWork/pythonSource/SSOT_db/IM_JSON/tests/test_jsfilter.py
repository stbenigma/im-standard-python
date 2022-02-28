import json
import unittest
from SSOT_db.IM_OBJECTS import Modelelement
from SSOT_db.IM_JSON import JSModel,JSFILTER
import  SSOT_infra.tests.integration as testsrc

def jsonequal(pjson1, pjson2):
    return json.dumps(pjson1, sort_keys=True) == json.dumps(pjson2, sort_keys=True)


class MyTestCase(unittest.TestCase):
    def setUp(self):
        from LOAD_MODELS.LOAD_ODM.tests.test_fillDB import create_testmodel1
        testmodelname, testdir, dbfilepath = testsrc.testmodel1()
        create_testmodel1(testmodelname=testmodelname,testdir=testdir,dbfilepath=dbfilepath,new=True)
        self.model = JSModel.readfromfile(dbfilepath.__str__().replace("db","json"))

    def test_publish_function(self):
        defaultfilter = JSFILTER()
        draftfilter = JSFILTER(ppublstatus=Modelelement.DRAFT)
        gtopfilter = JSFILTER(ppublstatus=Modelelement.GTOP)
        publfilter = JSFILTER(ppublstatus=Modelelement.PUBL)
        element = {"id":0}
        self.assertTrue(defaultfilter.publish(element))
        self.assertTrue(gtopfilter.publish(element))
        element["publstatus"]=None
        self.assertTrue(defaultfilter.publish(element))
        self.assertTrue(publfilter.publish(element))
        self.assertTrue(draftfilter.publish(element))
        element["publstatus"]=Modelelement.DRAFT
        self.assertTrue(defaultfilter.publish(element))
        self.assertFalse(publfilter.publish(element))
        self.assertFalse(gtopfilter.publish(element))
        self.assertTrue(draftfilter.publish(element))
        element["publstatus"]=Modelelement.GTOP
        self.assertTrue(defaultfilter.publish(element))
        self.assertFalse(publfilter.publish(element))
        self.assertTrue(gtopfilter.publish(element))
        self.assertTrue(draftfilter.publish(element))
        element["publstatus"]=Modelelement.PUBL
        self.assertTrue(defaultfilter.publish(element))
        self.assertTrue(publfilter.publish(element))
        self.assertTrue(gtopfilter.publish(element))
        self.assertTrue(draftfilter.publish(element))
        return

    def test_unchanged_model(self):
        # no filter return full original model
        assert (self.model.getfilter(), None)
        self.assertEqual(self.model.jsmodel, self.model.filtered_json())
        #check with empty (default) filter
        self.model.setfilter(JSFILTER())
        self.assertTrue(jsonequal(self.model.jsmodel, self.model.filtered_json()))

        # DAFT includes all stati, no diagramlist do no filter diagrams
        self.model.setfilter(JSFILTER(ppublstatus=Modelelement.DRAFT))
        self.assertTrue(jsonequal(self.model.jsmodel, self.model.filtered_json()))

    def test_filtered_models(self):
        # do not select any diagram
        self.model.setfilter(JSFILTER(pimdiagrams=[]))
        filteredjson = self.model.filtered_json()
        self.assertEqual(0,len(filteredjson["diagrams"]))

if __name__ == '__main__':
    unittest.main()
