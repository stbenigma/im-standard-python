import os.path
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from SSOT_infra.tests import integration as tb
from SSOT_db.IM_JSON import JSModel, filterjson


class FilteredJson(unittest.TestCase):
    def setUp(self) -> None:
        self.crm = tb.ModelHelper(tb.CRMTEST)
        self.crm.initDB(palways=False)
        self.localrun = os.path.isdir(Path.home()/"Downloads")


    def comparefiles(self,file1,file2):
        import difflib
        with open(file1) as lfile1:
            file1text = lfile1.readlines()
        with open(file2) as lfile2:
            file2text = lfile2.readlines()

        # Find and print the diff:
        return difflib.unified_diff(
                file1text, file2text, fromfile=str(file1),tofile=str(file2), lineterm='')

    def test_filteredjson(self):
        with tempfile.TemporaryDirectory() as tempdir:
            testfile = Path(tempdir + "/testfile.json")
            filteredfile = Path(tempdir + "/testfiltered.json")
            shutil.copy(self.crm.jsonfile, testfile)
            destfile= filterjson.filterjsonfile(pjsonfile=testfile, pdestination=filteredfile,
                                                pstatus=None, pdiagrams=None)
            self.assertTrue(os.path.isfile(destfile))
            cmp=[l for l in self.comparefiles(file1=testfile, file2=destfile)]
            self.assertEqual(0,len(cmp))

            destfile= filterjson.filterjsonfile(pjsonfile=testfile, pdestination=filteredfile,
                                                pstatus=None, pdiagrams=["DUMMY"])
            self.assertTrue(os.path.isfile(destfile))
            jsmodel=JSModel.readfromfile(pfilename=destfile)
            self.assertTrue(1,len(jsmodel.jsmodel["diagrams"].keys()))
            cmp=[l for l in self.comparefiles(file1=testfile, file2=destfile)]
            # DEBUG
            if self.localrun:
                shutil.copy(testfile, Path.home() / "Downloads")
                print(f"DEBUG: copied original json to {Path.home() / 'Downloads'}")
                shutil.copy(destfile, Path.home() / "Downloads")
                print(f"DEBUG: copied filtered json to {Path.home() / 'Downloads'}")
            self.assertLess(0,len(cmp))
        return

    def test_call(self):
        sys.argv = [
            filterjson.__file__,
            str(self.crm.jsonfile)
        ]
        filterjson.main()

        with tempfile.TemporaryDirectory() as tempdir:
            testfile = tempdir + "myfilteredjson.json"
            sys.argv = [
                filterjson.__file__,
                '--destination', testfile,
                str(self.crm.jsonfile)
            ]
            filterjson.main()
            self.assertTrue(os.path.isfile(testfile))

            # test diagrams and stat filters
            sys.argv = [
                filterjson.__file__,
                '-s', 'GTOP',
                '--diagrams=DUMMY',
                '--destination', testfile,
                str(self.crm.jsonfile)
            ]
            filterjson.main()
            self.assertTrue(os.path.isfile(testfile))
            if self.localrun:
                shutil.copy(testfile, Path.home() / "Downloads" / "filtered.json")

        return


if __name__ == '__main__':
    unittest.main()
