import unittest
import logging
from pathlib import Path

import pytest
from IM_STANDARD import StandardJsonModel,ImStandardGithub

class MyTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        caplog.set_level(logging.WARNING)
        self.capsys = capsys

    def setUp(self) -> None:
        self.mydebugpath = (Path.home() / "Downloads") if (Path.home() / "Downloads").exists() else self.temppath
        return


    def test_standardjsonmodel(self):
        testschemfile="im-standard-schema/InformationModel/Attribute-schema.json"
        model=StandardJsonModel(modeljson=ImStandardGithub._getstdjsonschema(githuburl=ImStandardGithub.CONTENTBASEURL+testschemfile))
        self.assertTrue(model.inschema("Attribute"))
        self.assertTrue(model.inschema("BaseAttribute"))
        self.assertTrue(model.inschema("AttributeId"))
        self.assertFalse(model.inschema("NoExist"))
        self.assertTrue("name" in model.getproperties("BaseAttribute"))
        self.assertTrue("mandatory" in model.getproperties("BaseAttribute"))
        return

    def test_validation(self):

        return



if __name__ == '__main__':
    unittest.main()
