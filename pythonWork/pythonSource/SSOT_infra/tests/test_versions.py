import tempfile
import unittest
from pathlib import Path

import SSOT_infra.parameters as t


class TestVersions(unittest.TestCase):

    def read_tool_version(self):
        v = t.toolversion()
        self.assertIsInstance(v, str)
        self.assertTrue(3 < len(v))

    def test_read_git_repo_version(self):
        r = t.read_git_description()
        self.assertIsInstance(r, str)
        self.assertTrue(len(r) > 3)

    def test_read_non_git_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = t.read_git_description(Path(tmp))
            self.assertIsInstance(r, str)
            self.assertTrue(r.startswith('<unknown'))
