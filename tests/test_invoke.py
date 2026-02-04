import os
import subprocess
import unittest
from pathlib import Path

import pytest

from IM_STANDARD import StandardJsonModel


class TestInvoke(unittest.TestCase):
    """
    Test invoke tasks.
    """

    @pytest.fixture(autouse=True)
    def init(self, tmp_path):
        self.temp_folder = Path(tmp_path)

    def setUp(self) -> None:
        super().setUp()
        self.root = Path(__file__).parent.parent
        # Ensure working directory exists
        os.chdir(Path(__file__).parent)

    def test_version(self):
        generate = [
            'invoke',
            'version',
        ]
        print(f"Running {' '.join(generate)}")
        result = subprocess.run(generate, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stderr, result.stdout, result.returncode)

        self.assertIn("im-standard", result.stdout.decode())
        generate = [
            'invoke',
            'version',
            '--element', 'im-standard'
        ]
        result = subprocess.run(generate, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stderr, result.stdout, result.returncode)
        self.assertNotIn("im-standard", result.stdout.decode())
        self.assertIn("json-schema", result.stdout.decode())
        return

    def test_validate(self):
        generate = [
            'invoke',
            'validateStandard',
            "--injson",
            str(StandardJsonModel.SCHEMADEFPATH.parent / "Example models" / "Astronomie" / "astronomie-schema.json")
        ]
        result = subprocess.run(generate, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(0, result.returncode)
        print(result.stderr, result.stdout, result.returncode)

        generate = [
            'invoke',
            'validateStandard',
            "--verbose",
            "--schemaonly",
            "--schemafile", "bla.json",
            "--injson",
            str(StandardJsonModel.SCHEMADEFPATH.parent / "Example models" / "Astronomie" / "astronomie-schema.json")
        ]
        result = subprocess.run(generate, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(255, result.returncode)
        self.assertIn("ERROR", str(result.stderr))
        print(result.stderr, result.stdout, result.returncode)
        return

    def test_dataspot2standard(self):
        outfile = self.temp_folder / "astronomie-assets-schema.json"
        generate = ['invoke',
                    'dataspot2standard',
                    "--inpath", str(Path(
                __file__).parent.parent / "INTERFACES" / "DATASPOT" / "imstandard_dataspot" / "tests" / "dataspottestfiles" / "astronomie"),
                    "--outpath", str(outfile),
                    "--modelname", "astronomie",
                    "--languages", "(en)",
                    "--language", "de"
                    ]
        result = subprocess.run(generate, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.returncode,result.stderr, result.stdout)

        self.assertIn("assets-schema.json written",str(result.stdout))
        self.assertEqual(0, result.returncode)
        self.assertTrue(outfile.is_file())
        return

    def test_standard2schema(self):
        outfile=self.temp_folder / "astronomie-assets-schema.json"
        generate = ['invoke',
                    'std2schema',
                    "--inpath", str(Path(
                __file__).parent.parent / "IM_STANDARD" / "tests" / "json-test-standard-files" / "astronomie-assets-standard.json"),
                    "--outpath", str(outfile),
                    "--entity", "Mond Datenblatt",
                    "-w",
                    "--nid", "myastronomy"
                    ]
        result = subprocess.run(generate, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.returncode,result.stderr, result.stdout)
        self.assertIn("Schema json w",str(result.stdout))
        self.assertTrue(outfile.is_file())
        return


if __name__ == '__main__':
    unittest.main()
