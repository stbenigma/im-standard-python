import logging
import subprocess
import unittest
from pathlib import Path
import json

import pytest

from SSOT_infra.tests import integration as ti
from SSOT_infra.tests.integration import Testmodel, RIDDLE


class TestInvoke(unittest.TestCase):
    """
    Test invoke tasks.
    If failing, but unittests are passing, we are missing a unittest 🤓
    """

    @pytest.fixture(autouse=True)
    def init(self, tmp_path):
        self.temp_folder = Path(tmp_path)

    def setUp(self) -> None:
        super().setUp()
        self.root = ti.resolve_project_root()
        self.testmodel = ti.Testmodel(ti.RIDDLE)

    def test_version(self):
        generate = [
            'invoke',
            'version',
        ]
        print(f"Running {' '.join(generate)}")
        result = subprocess.check_output(generate).decode('utf-8')
        from SSOT_infra import version
        ver = version()
        self.assertIn(ver['TOOLVERSION'], result)

    def test_info(self):
        generate = [
            'invoke',
            'info',
        ]
        print(f"Running {' '.join(generate)}")
        result = subprocess.check_output(generate).decode('utf-8')
        self.assertIn('riddle.db', result)

    def test_json2db(self):
        tm = self.testmodel
        tm.initDB()
        self.assertTrue(tm.jsonfile.exists(), "Need a json source to work")
        db_destination = Path(self.temp_folder, 'riddle.db')
        generate = [
            'invoke',
            'json2db',
            '--nomerge',
            '--source', str(tm.jsonfile.resolve()),
            '--srcname', __name__,
            '--output', str(db_destination),
        ]
        print(f"Running {' '.join(generate)}")
        result = subprocess.check_output(generate).decode('utf-8')
        self.assertTrue(db_destination.is_file(),
                        f"Expecting created database in '{db_destination}'")
        self.assertIn('riddle.db', result,
                      f"Expecting database name in output")

    def test_json2db_dry(self):
        tm = self.testmodel
        self.assertTrue(tm.jsonfile.exists(), "Need a json source to work")
        db_destination = Path(self.temp_folder, 'riddle_dry.db')
        db_destination.unlink(missing_ok=True)
        generate = [
            'invoke',
            'json2db',
            '--nomerge',
            '--source', str(tm.jsonfile.resolve()),
            '--srcname', __name__,
            '--output', str(db_destination),
            '--dry',
        ]
        print(f"Running {' '.join(generate)}")
        result = subprocess.check_output(generate).decode('utf-8')
        self.assertFalse(db_destination.is_file(),
                         f"Expecting no database in '{db_destination}'")
        self.assertIn(db_destination.name, result,
                      f"Expecting database name in output")

    def test_db2json(self):
        tm = self.testmodel
        self.assertTrue(tm.dbfile.exists(), "Need a db/ssod source to work")
        json_destination = Path(self.temp_folder, 'riddle.json')
        generate = [
            'invoke',
            'db2json',
            '--source', str(tm.dbfile.resolve()),
            '--output', str(json_destination),
        ]
        print(f"Running {' '.join(generate)}")
        result = subprocess.check_output(generate).decode('utf-8')
        self.assertTrue(json_destination.is_file(),
                        f"Expecting created database in '{json_destination}'")
        self.assertIn('riddle.json', result,
                      f"Expecting database name in output")

    def test_invoke_create_and_alter(self):
        tm = self.testmodel
        model_folder = tm.modeldir / 'IM'
        tm.dbfile.unlink(missing_ok=True)
        self.assertFalse(tm.dbfile.is_file())

        jsonfile = self.testmodel.jsonfile
        jsonfile.unlink(missing_ok=True)
        self.assertFalse(jsonfile.is_file())

        generate = [
            'invoke',
            'generator',
            '--ssod-only',
            '--model', str(model_folder.resolve())
        ]
        print(f"Generating riddle using subprocess: {' '.join(generate)}")
        result = subprocess.check_output(generate)
        self.assertTrue(tm.dbfile.is_file(),
                        f"Expecting SSOD db in '{tm.dbfile.resolve()}'")
        self.assertTrue(tm.jsonfile.is_file(),
                        f"Expecting SSOD json in '{tm.jsonfile.resolve()}'")
        print(f"SSOD created in {tm.dbfile} / {jsonfile}")
        logging.debug(f"Generator output:\n{result}")

        with open(jsonfile, "r") as src:
            ssod = json.load(src)

        entity1 = next(iter(ssod['entities'].values()))
        entity1['shortname'] = 'test_shortname'

        destination_json = Path(self.temp_folder) / 'riddle-altered.json'
        with open(destination_json, 'w') as out:
            json.dump(ssod, out)

        destination_db = Path(self.temp_folder) / 'riddle-altered.db'
        store = [
            'invoke',
            'json2db',
            '--source', str(destination_json),
            '--srcname', __name__,
            '--output', str(destination_db.resolve()),
        ]

        print(f"Creating new db from JSON")
        subprocess.check_output(store)

        self.assertTrue(tm.dbfile.is_file())
