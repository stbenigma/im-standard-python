import unittest
import os
from pathlib import Path
from SSOT_infra.tests.integration import resolve_project_root

LOCALTESTMODELS:str = 'localtestmodels'

class MyTestCase(unittest.TestCase):
    def test_localODMs(self):
        def stable_file_list(folder: str) -> list:
            assert os.path.isdir(folder), f"Path '{folder}' is not a valid folder"
            result = list(os.listdir(folder))
            for f in result:
                if f.startswith('.'):
                    result.remove(f)
            return result

        filelist = stable_file_list(resolve_project_root() / LOCALTESTMODELS)
        print (filelist)



if __name__ == '__main__':
    unittest.main()
