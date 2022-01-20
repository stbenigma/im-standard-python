def hex2int(phex):
    return None if (phex is None) else int(phex, 16)


def int2hex(pint):
    if pint is None: return None
    if type(pint) == str:
        # TODO move to str2hex
        pint = int(pint)
    rgba = hex(pint & 0xffffff)  # AARRGGBB
    hex_value = rgba.replace('0x', '')  # strip 0xFF
    digits = len(hex_value)
    if digits < 6:
        return hex_value.zfill(6)
    return hex_value
