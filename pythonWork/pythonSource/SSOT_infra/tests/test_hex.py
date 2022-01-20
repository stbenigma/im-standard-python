import unittest
from SSOT_infra.hex import hex2int, int2hex


class TestHex(unittest.TestCase):

    def test_hex2int(self):
        assert hex2int(None) is None, "None must return None"
        assert hex2int('1') == 1
        assert hex2int('F') == 15
        assert hex2int('FFFFC9') == 16777161
        assert hex2int('1000000') == 16777216
        assert hex2int('ffffff') == 16777215


class ODMColorCodingFunctions(unittest.TestCase):
    def test_int2hex255(self):
        self.assertEqual("0000ff", int2hex(0xff0000ff))  # add assertion here

    def test_int2hex001(self):
        self.assertEqual("000001", int2hex(0xff000001))

    def test_int2hex_red(self):
        self.assertEqual("ff0000", int2hex(0xffff0000))

    def test_int2hex_red_no_alpha(self):
        self.assertEqual("ff0000", int2hex(0xff0000))

    def test_int2hex_black_no_alpha(self):
        self.assertEqual("000000", int2hex(0x00))

    def test_int2hex_almost_white_no_alpha(self):
        self.assertEqual("ffeeff", int2hex(0xffeeff))

    def test_hex2int_int2hex(self):
        # forward backward conversion just removes alpha channel
        values = [0xffffffff, -1, 0, 1, 255, 0x00ff00, 0x00ff0000, 0xafafafaf]
        for value in values:
            self.assertEqual(value & 0xffffff, hex2int(int2hex(value)))
