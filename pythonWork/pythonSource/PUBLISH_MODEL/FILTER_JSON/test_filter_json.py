import json
import unittest
from SSOT_db.IM_OBJECTS import Modelelement
from SSOT_db.IM_JSON import JSModel
import  SSOT_infra.tests.integration as testsrc
from .filter_json import filter_json

def jsonequal(pjson1, pjson2):
    return json.dumps(pjson1, sort_keys=True) == json.dumps(pjson2, sort_keys=True)


class MyTestCase(unittest.TestCase):
    def setUp(self):
        from LOAD_MODELS.LOAD_ODM.tests.test_fillDB import create_testmodel1
        testmodelname, testdir, dbfilepath = testsrc.testmodel1()
        create_testmodel1(testmodelname=testmodelname,testdir=testdir,dbfilepath=dbfilepath,new=True)
        self.model = JSModel.readfromfile(dbfilepath.__str__().replace("db","json"))

    def test_unchanged_model(self):
        # no filter return full model
        self.assertEqual(self.model, filter_json(pmodel=self.model))
        self.assertEqual(self.model, filter_json(pmodel=self.model
                                                 , ppubl_status=None
                                                 , pIMdiagrams=None))

        # DAFT includes all stati
        self.assertEqual(jsonequal(self.model.jsmodel
                                   ,filter_json(pmodel=self.model
                                                , ppubl_status=Modelelement.DRAFT).jsmodel)
                        ,True)

if __name__ == '__main__':
    unittest.main()
