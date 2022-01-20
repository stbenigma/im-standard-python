import os
import shutil
import subprocess
import unittest


class test_sql_files(unittest.TestCase):
    SQLSOURCE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dbstructure'))
    TESTSCRIPTPATH = os.path.join(SQLSOURCE, "testddlscript")
    DIFFSCRIPTPATH = os.path.abspath(os.path.join(SQLSOURCE, '..', '..', '..', '..', "unittest-tmp-dir", 'test_sqlfiles'))
    DIFFSCRIPT1 = "schemadiff.txt"
    DIFFSCRIPT2 = "schemaupgradediff.txt"


    def test_script(self):
        def movescripts():
            if os.path.exists(os.path.join(self.SQLSOURCE, self.DIFFSCRIPT1)):
                shutil.move(os.path.join(self.SQLSOURCE, self.DIFFSCRIPT1), os.path.join(self.DIFFSCRIPTPATH,self.DIFFSCRIPT1))
            if os.path.exists(os.path.join(self.SQLSOURCE, self.DIFFSCRIPT2)):
                shutil.move(os.path.join(self.SQLSOURCE, self.DIFFSCRIPT2), os.path.join(self.DIFFSCRIPTPATH,self.DIFFSCRIPT2))

        if not os.path.exists(self.DIFFSCRIPTPATH):
            os.mkdir(self.DIFFSCRIPTPATH)
        result = subprocess.Popen([self.TESTSCRIPTPATH, "xxx"])
        res = result.communicate(0)
        movescripts()
        self.assertTrue(result.returncode == 1)

        result = subprocess.Popen([self.TESTSCRIPTPATH, "1.6"])
        res = result.communicate(0)
        movescripts()
        self.assertTrue(result.returncode == 0)

        print("*********************************************")
        print(f"check sql differences in {os.path.abspath(self.DIFFSCRIPTPATH)}")
        print("*********************************************")
