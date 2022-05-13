import unittest
from pathlib import Path

from LOAD_MODELS.LOAD_ODM.transferModel import stable_file_list
from SSOT_infra.tests import integration as tc
from SSOT_db.SQL_INFRA import dbConnect
from SSOT_db.IM_OBJECTS import Actorrole,Attribute,Entity


class TestTransferModel(unittest.TestCase):

    def setUp(self) -> None:
        self.testmodel1 = tc.Testmodel(tc.TESTMODEL1)

    def test_stable_file_list(self):
        folder = Path('..').resolve()
        left = stable_file_list(str(folder))
        self.assertTrue(len(left) > 0)

        right = list(map(lambda f: f.name, folder.iterdir()))
        right.sort()
        self.assertEqual(left, right)

    def test_raciload(self):
        dbConnect.openDB(self.testmodel1.dbfile)
        try:
            sales = Actorrole.getbyuk(actr_name='Sales')
            enti1 = Entity.getbyuk(enti_name ="Multi UK Entity")
            attr1 = Attribute.getbyuk(attr_enti_id=enti1.enti_id,attr_tech_name='ATTRIBUTE1')
            salescons = {c.actc_mode_id: c.getraci() for c in sales.getchildren()}
            self.assertEqual('I',salescons[enti1.enti_id])
            self.assertEqual('RI',salescons[attr1.attr_id])
        finally:
            dbConnect.closeDB()