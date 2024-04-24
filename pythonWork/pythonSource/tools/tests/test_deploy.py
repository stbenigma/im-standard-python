import os
import subprocess
import unittest
import zipfile
from pathlib import Path

import pytest

from SSOT_infra.tests.integration import resolve_project_root, path_to_testmodels
from tools.deploy import main


class TestDeploy(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def init(self, tmp_path):
        self.temp_folder = Path(tmp_path)


    def test_deploy_generator(self):
        self.skipTest("================Muss nochmal überprüft werden================== ")
        notebook = resolve_project_root() / 'notebooks' \
                   / 'mig' / 'generator.ipynb'
        self.assertTrue(notebook.is_file())
        arguments = ['--verbose', str(notebook.resolve())]

        try:
            cwd = os.getcwd()
        except FileNotFoundError:
            cwd = None

        try:
            os.chdir(self.temp_folder)
            archive = main(resolve_project_root(), arguments)
        finally:
            # restore previous path if any
            if cwd is not None:
                os.chdir(cwd)

        self.assertTrue(archive.exists())

        generator_script = archive.parent / 'generator.py'
        self.assertTrue(generator_script.is_file())

        print(f"Extracting archive to {self.temp_folder}")
        with zipfile.ZipFile(archive) as zip_archive:
            zip_archive.extractall(path=str(self.temp_folder))

        try:
            py_ver = subprocess.check_output(['python', '--version'])
            print(f"Working with {py_ver.decode()}")
        except RuntimeError:
            pass

        try:
            execution = self.temp_folder / 'run'
            execution.mkdir(exist_ok=True)
            os.chdir(execution)
            print(f"Starting generator {generator_script} in {self.temp_folder.resolve()}")
            result = subprocess.check_output(
                ['python', str(generator_script),
                 '--languages', 'en',
                 '--tools-path', str((resolve_project_root() / 'pythonWork' / 'pythonSource').resolve()),
                 '-m', str(path_to_testmodels() / 'riddle' / 'IM')])
            print(result.decode())
        finally:
            # restore previous path if any
            if cwd is not None:
                os.chdir(cwd)
