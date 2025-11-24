import os
import unittest
import logging


import pytest
from IM_STANDARD import IMStandardJsonModel,StandardJsonModel


class MyTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        caplog.set_level(logging.WARNING)
        self.capsys = capsys

    def setUp(self) -> None:
        self.testschema="Attribute-schema.json"

    def test_standardjsonmodel(self):
        self.assertTrue((StandardJsonModel.SCHEMADEFPATH/self.testschema).exists())
        model=StandardJsonModel(modelfilepath=StandardJsonModel.SCHEMADEFPATH/self.testschema)
        self.assertTrue(model.inschema("Attribute"))
        self.assertTrue(model.inschema("BaseAttribute"))
        self.assertTrue(model.inschema("AttributeId"))
        self.assertFalse(model.inschema("NoExist"))
        self.assertTrue("name" in model.getproperties("BaseAttribute"))
        self.assertTrue("mandatory" in model.getproperties("BaseAttribute"))
        return

    def test_imstandardjsonmodel(self):
        self.assertTrue(IMStandardJsonModel.IMDEFINITIONFILEPATH.is_file())
        model=IMStandardJsonModel()
        self.assertTrue("Entities" in model.getimelements())
        self.assertTrue("description" in model.getimelement("Categories"))
        return

if __name__ == '__main__':
    unittest.main()
