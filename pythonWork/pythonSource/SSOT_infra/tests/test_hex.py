from SSOT_infra.hex import hex2int, int2hex


class TestHex:

    def test_hex2int(self):
        assert hex2int(None) is None, "None must return None"
        assert hex2int('1') == 1
        assert hex2int('F') == 15
        assert hex2int('FFFFC9') == 16777161
        assert hex2int('1000000') == 16777216
        assert hex2int('ffffff') == 16777215

    def test_int2hex(self):
        assert int2hex(None) is None, "None must return None"
        assert int2hex(None, 3) is None, "None must return None"
        assert int2hex(15, 1) == 'f'
        assert int2hex(1, 1) == '1'
        assert int2hex(-55, 6) == 'fffffc'
        assert int2hex(-55) == 'fffffc'
        assert int2hex(16777161, 6) == 'ffffc9'
        assert int2hex(-1677721, 6) == 'fe6666'
        assert int2hex(-16777216, 6) == 'f00000'
