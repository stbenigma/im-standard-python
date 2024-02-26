import re
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

def colorhex(color:str,withhashtag=True):
    """translates a color into a hexcode,
        withhashtag True -> code has to start with #
                    False -> code is only hexdigits
    """
    from matplotlib.colors import cnames
    if color is None:
        return None
    elif type(color)==int:
        return ('#' if withhashtag else "")  + int2hex(color)
    elif color.startswith('#') and withhashtag:
        return color
    elif color.startswith('#') and  withhashtag:
        return color
    elif color.startswith('#') and not withhashtag:
        return color[1:]
    else:
        try:
            int(color,16) #if all hex characters ok
            return ('#' if withhashtag else "")  +color
        except:
            if color.isascii():
                #translate name
                loccolor = color.replace("_", "")
                if loccolor in cnames:
                    lochex=cnames[loccolor]
                    if not withhashtag:
                        lochex=lochex[1:]
                    return lochex
            #fallback, I can't handle this code
            return color


