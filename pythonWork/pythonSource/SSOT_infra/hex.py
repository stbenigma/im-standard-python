def hex2int(phex):
    return None if (phex is None) else int(phex, 16)

def int2hex(pint,lng=6):
    if (pint is None): return pint
    lint = pint if (type(pint) == int) else int(pint)
    retval = hex(lint & 0xfffffff)
    retval = str(retval)[2:2+lng]
    if len(retval)!= lng:
        print (lint)
        print (hex(lint & 0xfffffff))
        print (retval)
        raise Exception()
    return retval