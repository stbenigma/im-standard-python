import logging
import subprocess
import unittest
from pathlib import Path
import json

import pytest

from SSOT_infra.tests import integration as ti


class TestInvoke(unittest.TestCase):
    """Test invoke tasks.
    If this tests fail, but unittests are passing,
    we are missing a unittest 🤓
    """

    @pytest.fixture(autouse=True)
    def init(self, tmp_path):
        self.temp_folder = Path(tmp_path)

    def setUp(self) -> None:
        super().setUp()
        self.root = ti.resolve_project_root()
        self.testmodel = ti.Testmodel(ti.RIDDLE)

    def test_create_db(self):
        model_folder = Path(self.testmodel.modeldir) / 'IM'
        self.assertEqual(1, len(list(model_folder.glob("*.dmd"))),
                         f"Expecting model (*.dmd) in {model_folder}")

        dbfile = Path(self.testmodel.dbfile)
        dbfile.unlink(missing_ok=True)
        self.assertFalse(dbfile.is_file())

        jsonfile = self.testmodel.jsonfile
        jsonfile.unlink(missing_ok=True)
        self.assertFalse(jsonfile.is_file())

        generate = [
            'invoke',
            'generator',
            '--spod-only',
            '--model',
            str(model_folder.resolve())
        ]
        print(f"Generating riddle using subprocess: {' '.join(generate)}")
        result = subprocess.check_output(generate)
        self.assertTrue(dbfile.is_file(),
                        f"Expecting SPOD db in '{dbfile.resolve()}'")
        self.assertTrue(self.testmodel.jsonfile.is_file(),
                        f"Expecting SPOD json in '{self.testmodel.jsonfile.resolve()}'")
        print(f"SPOD created in {dbfile} / {jsonfile}")
        logging.debug(f"Generator output:\n{result}")

        with open(jsonfile, "r") as src:
            spod = json.load(src)

        entity1 = next(iter(spod['entities'].values()))
        entity1['shortname'] = 'test_shortname'

        destination_json = Path(self.temp_folder) / 'riddle-altered.json'
        with open(destination_json, 'w') as out:
            json.dump(spod, out)

        destination_db = Path(self.temp_folder) / 'riddle-altered.db'
        store = [
            'invoke',
            'json2db',
            '--source',
            str(destination_json.resolve()),
            '--srcname',
            'unittest',
            '--output',
            str(destination_db.resolve()),
        ]

        print(f"Creating new db from JSON")
        subprocess.check_output(store)
