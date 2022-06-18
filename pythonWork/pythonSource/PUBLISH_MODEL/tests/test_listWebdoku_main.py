import os
import re
import tempfile
import unittest

import SSOT_infra.tests.integration as testsrc
from IM_WEB import listWebdoku
from SSOT_infra.tests.test_translateprompt import TestTranslation


class TestListWebDocumentation(unittest.TestCase):

    def purgefiles(self, ppath, ppattern):
        if not os.path.exists(ppath):
            return
        for f in os.listdir(ppath):
            if re.search(ppattern, f):
                os.remove(os.path.join(ppath, f))

    def setUp(self) -> None:
        """Prepare test models"""

        translation = TestTranslation()
        translation.setUp()
        self.testmodel1 = testsrc.Testmodel(testsrc.TESTMODEL1)
        self.testmodel2 = testsrc.Testmodel(testsrc.TESTMODEL2)
        self.testmodelcrm = testsrc.Testmodel(testsrc.CRMTEST)

        assert os.path.isdir(
            testsrc.testmodels_dir()), f"Cannot find testmodels {os.path.abspath(testsrc.testmodels_dir())}"
        return

    def test_main(self):
        with self.assertRaises(SystemExit) as cm:
            listWebdoku.main(psysargs=['listWebdoku.py', '--unittest'])
        self.assertEqual(cm.exception.code, 1)
        listWebdoku.main(psysargs=['listWebdoku.py', '-m', 'bla', '--unittest'])

        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)  # we need a current directory
            basedir = testsrc.testmodels_dir() / testsrc.TESTMODEL2
            listWebdoku.main(psysargs=['listWebdoku.py', f'--paramfile={basedir}/testmodel-2.params'])
            # this web file directory must not be in curr-dir
            self.assertFalse(os.path.exists(tempdir + "/Web"))

        return

    def test_webmain(self):
        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)  # we need a current directory
            with self.assertRaises(AssertionError):
                listWebdoku.webmain()
            with self.assertRaises(AssertionError):
                listWebdoku.webmain(pjsonfilepath='x')

        os.chdir(testsrc.testmodels_dir() / testsrc.TESTMODEL1)  # we need a current directory
        listWebdoku.webmain(
            pjsonfilepath=testsrc.testmodels_dir() / testsrc.TESTMODEL1 / 'DB' / (testsrc.TESTMODEL1 + '.json'),
            pwebdirec=testsrc.testmodels_dir() / testsrc.TESTMODEL1 / 'Web')

        os.chdir(testsrc.testmodels_dir())  # we need a current directory
        listWebdoku.webmain(pparamfile=testsrc.testmodels_dir() / testsrc.TESTMODEL2 / (testsrc.TESTMODEL2 + '.params'))

        os.chdir(testsrc.testmodels_dir() / testsrc.CRMTEST)  # we need a current directory
        listWebdoku.webmain(pparamfile=testsrc.testmodels_dir() / testsrc.CRMTEST / (testsrc.CRMTEST + '.params'))
