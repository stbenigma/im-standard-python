import json
import unittest
from pathlib import Path
import pytest

from INTERFACES.DATASPOT.imstandard_dataspot import dselements as dse


class Testjson2dataspot(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys

    def setUp(self) -> None:
        return

    def dumptodebug(self,filename,jsonstruct):
        debugpath=Path(Path.home(), "Downloads")
        if debugpath.exists():
            with open (debugpath / filename,'w') as outfile:
                json.dump(jsonstruct, outfile, indent=2)
                print('\n', debugpath / filename, " written")
        return

    def test_dataspotelements(self):

        path1 = Path("dataspottestfiles/schwipsti")
        dsschema = dse.DataspotElements(path1)
        self.assertTrue(len(dsschema.LOVvalues)>0)
        self.assertTrue(len(dsschema.entities)>0)
        return

if __name__ == '__main__':
    unittest.main()
