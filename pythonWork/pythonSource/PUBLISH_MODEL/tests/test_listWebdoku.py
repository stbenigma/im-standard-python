import os
import re
import tempfile
import unittest

from LOAD_MODELS.LOAD_ODM import fillDB
from IM_WEB import listWebdoku
from SSOT_infra.tests.test_translateprompt import TestTranslation
import SSOT_infra.tests.integration as testsrc


class TestListWebDocumentation(unittest.TestCase):

    def purgefiles(self, ppath, ppattern):
        if not os.path.exists(ppath):
            return
        for f in listdir(ppath):
            if re.search(ppattern, f):
                remove(os.path.join(ppath, f))

    def setUp(self) -> None:
        """Prepare test models"""

        translation = TestTranslation()
        translation.setUp()

        assert os.path.isdir(testsrc.testmodels_dir()), f"Cannot find testmodels {os.path.abspath(testsrc.testmodels_dir())}"
        if not os.path.exists(testsrc.testmodels_dir() / testsrc.TESTMODEL1/ 'DB' / (testsrc.TESTMODEL1 + '.db')):
            os.chdir(testsrc.testmodels_dir() / testsrc.TESTMODEL1)
            fillDB.filldbmain(pmodelname=testsrc.TESTMODEL1)

        if not os.path.exists(testsrc.testmodels_dir() / testsrc.TESTMODEL2/ 'DB' / (testsrc.TESTMODEL2 + '.db')):
            os.chdir(testsrc.testmodels_dir() / testsrc.TESTMODEL2)
            fillDB.filldbmain(pmodelname=testsrc.TESTMODEL2)

        if not os.path.exists(testsrc.testmodels_dir() / testsrc.CRMTEST/ 'DB' / (testsrc.CRMTEST + '.db')):
            os.chdir(testsrc.testmodels_dir() / testsrc.CRMTEST)
            fillDB.filldbmain(pmodelname=testsrc.CRMTEST)
        return

    def test_main(self):
        with self.assertRaises(SystemExit) as cm:
            listWebdoku.main(psysargs=['listWebdoku.py', '--unittest'])
        self.assertEqual(cm.exception.code, 1)
        listWebdoku.main(psysargs=['listWebdoku.py', '-m', 'bla', '--unittest'])

        with tempfile.TemporaryDirectory() as tempdir:
            basedir =  testsrc.testmodels_dir() / testsrc.TESTMODEL2
            os.chdir(tempdir)
            listWebdoku.main(psysargs=['listWebdoku.py', f'--paramfile={basedir}/testmodel-2.params'])
            #this web file directory must not be in curr-dir
            self.assertFalse(os.path.exists(tempdir + "/Web"))

        return

    def test_webmain(self):
        with tempfile.TemporaryDirectory() as tempdir:
            with self.assertRaises(AssertionError):
                listWebdoku.webmain()
            with self.assertRaises(AssertionError):
                listWebdoku.webmain(pjsonfilepath='x')

        listWebdoku.webmain(pjsonfilepath=testsrc.testmodels_dir() / testsrc.TESTMODEL1/ 'DB' / (testsrc.TESTMODEL1 + '.json'),
                            pwebdirec=testsrc.testmodels_dir() / testsrc.TESTMODEL1 / 'Web')
        with self.assertRaises(Exception):
            #aktuell noch keine Modell
            listWebdoku.webmain(pparamfile=testsrc.testmodels_dir() / testsrc.TESTMODEL2/ (testsrc.TESTMODEL2 + '.params'))
        listWebdoku.webmain(pparamfile=testsrc.testmodels_dir() / testsrc.CRMTEST/ (testsrc.CRMTEST + '.params'))


