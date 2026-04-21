import json
import os
import unittest
from pathlib import Path

import pytest

from INTERFACES.DATASPOT import DataspotElements,System2Json


class Test_systemlandscape(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temppath = Path(tmp_path)

    def setUp(self) -> None:
        self.mydebugpath = (Path.home() / "Downloads") if (Path.home() / "Downloads").exists() else self.temppath
        return

    def dumpjson(self, filepath: Path, jsonstruct):
        with open(filepath, 'w') as outfile:
            json.dump(jsonstruct, outfile, indent=2)
            print('\n', filepath, " written")
        return

    def dumptodebug(self, filename, jsonstruct):
        if self.mydebugpath.exists():
            self.dumpjson(filepath=self.mydebugpath / filename,
                          jsonstruct=jsonstruct)
        return


    def test_dataspot2syst(self):
        file1 = Path("dataspottestfiles/Systems.json")
        schema = System2Json(indirec=file1)
        jsonstructsyst = schema.generatejson()
        self.dumptodebug(filename=f"SystemStandard.json",
                         jsonstruct=jsonstructsyst)
        return

    def test_ds2systemlandscape(self):
        inpath = Path(__file__).parent / "dataspottestfiles" / "systemlandscape"
        if not inpath.is_dir(): self.skipTest("no localtestmodels found")
        loaded = DataspotElements(indirec=inpath,
                                  tenant="Sandbox",
                                  modelname="System Landscape"
                                     )
        systems= System2Json(dsmodels=loaded)
        self.dumptodebug(filename="testsystemlandscape.json",
                         jsonstruct=systems.generatejson(modelversion=None,
                                                         targetenv=None,
                                                         language="en",
                                                         languages=["de"])
                         )
        return

if __name__ == '__main__':
    unittest.main()
