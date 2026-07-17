import unittest
import logging


import pytest
from IM_STANDARD import IMStandardJsonModel,StandardJsonModel, IMSTANDARDPATH



class MyTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        caplog.set_level(logging.WARNING)
        self.capsys = capsys

    def setUp(self) -> None:
        self.testschema="Attribute-schema.json"

    def test_standardjsonmodel(self):
        testpath=(IMSTANDARDPATH / "Model" / "im-standard-schema" / "InformationModel" / self.testschema)
        self.assertTrue(testpath.exists())
        model=StandardJsonModel(modelfilepath=testpath)
        self.assertTrue(model.inschema("Attribute"))
        self.assertTrue(model.inschema("BaseAttribute"))
        self.assertTrue(model.inschema("AttributeId"))
        self.assertFalse(model.inschema("NoExist"))
        self.assertTrue("name" in model.getproperties("BaseAttribute"))
        self.assertTrue("mandatory" in model.getproperties("BaseAttribute"))
        return


if __name__ == '__main__':
    unittest.main()
