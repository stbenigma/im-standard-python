import unittest
from pathlib import Path

from LOAD_MODELS.LOAD_ODM.transferModel import stable_file_list


class TestTransferModel(unittest.TestCase):

    def test_stable_file_list(self):
        folder = Path('..').resolve()
        left = stable_file_list(str(folder))
        self.assertTrue(len(left) > 0)

        right = list(map(lambda f: f.name, folder.iterdir()))
        right.sort()
        self.assertEqual(left, right)

