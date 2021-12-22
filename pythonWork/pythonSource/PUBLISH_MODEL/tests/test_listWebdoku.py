import os.path
import unittest

from IM_ODM import fillDB
from IM_WEB import listWebdoku

from os import path, remove, listdir
import re

from SSOT_infra.tests.test_translateprompt import TestTranslation


class TestListWebDocumentation(unittest.TestCase):

    testdirectory = path.join(path.dirname(__file__), '..', '..', 'testenvironment', 'odmloadtest',
                              'testmodels')

    def setUp(self) -> None:
        """Prepare test models"""

        translation = TestTranslation()
        translation.setUp()

        assert os.path.isdir(self.testdirectory), f"Cannot find testmodels {os.path.abspath(self.testdirectory)}"
        fillDB.main(os.path.join(self.testdirectory, 'testmodel-1', 'IM'), create_base_folder=True)

        fillDB.main(os.path.join(self.testdirectory, 'crmTest', 'IM'), create_base_folder=True)

    def test_main(self):
        modelpath = path.join(self.testdirectory, 'testmodel-1')
        webfilepath = path.join(modelpath, 'Web')
        self.purgefiles(webfilepath, '.*\.html')
        listWebdoku.main(pdirec=modelpath, pinputtype="JSON", plang='de')

        modelpath = path.join(self.testdirectory, 'crmTest')
        webfilepath = path.join(modelpath, 'Web')
        self.purgefiles(webfilepath, '.*\.html')
        listWebdoku.main(pdirec=modelpath, pinputtype="JSON", plang='de')

    def purgefiles(self, ppath, ppattern):
        if not os.path.exists(ppath):
            return
        for f in listdir(ppath):
            if re.search(ppattern, f):
                remove(path.join(ppath, f))
