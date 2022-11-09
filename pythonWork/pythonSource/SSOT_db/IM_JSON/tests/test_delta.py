import json
import unittest
import difflib
import copy

from SSOT_db.IM_JSON import JSModel
from SSOT_db.IM_JSON.delta import delta_spod

blank = {'_imprint_': {}}


class DiffTest(unittest.TestCase):

    def test_empty(self):
        result = delta_spod(JSModel(pmodel=blank,pwithversioncheck=False), JSModel(pmodel=blank,pwithversioncheck=False))
        print(json.dumps(result, indent=2))

    def test_insert(self):
        right = copy.deepcopy(blank)
        right['columns'] = {'C0': {}}

        result = delta_spod(JSModel(pmodel=blank,pwithversioncheck=False), JSModel(pmodel=right,pwithversioncheck=False))
        print(json.dumps(result, indent=2))

    def test_update(self):
        left = copy.deepcopy(blank)
        left['columns'] = {
            'C0': {'a': 1},
            'S': {'x': 'y'},
        }

        right = copy.deepcopy(left)
        right['columns']['C0']['a'] = 2

        result = delta_spod(JSModel(pmodel=left,pwithversioncheck=False), JSModel(pmodel=right,pwithversioncheck=False))
        print(json.dumps(result, indent=2))
