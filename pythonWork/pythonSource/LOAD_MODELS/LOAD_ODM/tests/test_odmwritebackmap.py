import logging
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from LOAD_MODELS.LOAD_ODM import odmwritebackmap as wbm
from SSOT_infra.tests import integration


class OdmWriteBack(unittest.TestCase):
    def setUp(self) -> None:
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        root.addHandler(handler)

        from SSOT_db.IM_JSON import JSModel
        self.tm1 = integration.ModelHelper(integration.TESTMODEL1)
        self.tm2 = integration.ModelHelper(integration.TESTMODEL2)
        self.crm = integration.ModelHelper(integration.CRMTEST)
        self.tm1.initDB(palways=False)
        self.tm2.initDB(palways=False)
        self.crm.initDB(palways=False)
        self.tm1json = JSModel.readfromfile(self.tm1.jsonfile)
        self.tm2json = JSModel.readfromfile(self.tm2.jsonfile)
        self.crmjson = JSModel.readfromfile(self.crm.jsonfile)

    def test_calls(self):
        with self.assertRaises(SystemExit):
            wbm.main([__name__])

        with self.assertRaises(AssertionError):
            wbm.main([__name__,
                      'dummy.dum'])

        with self.assertRaises(AssertionError):
            wbm.main([__name__,
                      "--logfile=gugus/dummy.dum",
                      str(self.tm2.jsonfile)])

        with self.assertRaises(AssertionError):
            wbm.main([__name__,
                      "--destination=gugus",
                      str(self.tm2.jsonfile)])

        return

    def test_writeback(self):
        with tempfile.TemporaryDirectory() as tempdir:
            # testdir = self.tm2.modeldir
            testdir = Path(tempdir, 'tm2')
            shutil.copytree(self.tm2.modeldir, testdir)

            written = wbm.writemappings(pIMdirec=testdir/"IM",pjson=self.tm2json,pintfs=['xxyy'])
            self.assertEqual(0,len(written))

            written = wbm.writemappings(pIMdirec=testdir/"IM",pjson=self.tm2json,pintfs=[])
            self.assertEqual(0,len(written))

            written = wbm.writemappings(pIMdirec=testdir / "IM", pjson=self.tm2json, pintfs=None)
            self.assertEqual(0, len(written))

        with tempfile.TemporaryDirectory() as tempdir:
            testdir = Path(tempdir, 'crm')
            shutil.copytree(self.crm.modeldir, testdir)

            written = wbm.writemappings(pIMdirec=testdir / "IM", pjson=self.crmjson, pintfs=None)
            self.assertEqual(len(self.crmjson.jsmodel["systems"]), len(written))

        return


if __name__ == '__main__':
    unittest.main()
