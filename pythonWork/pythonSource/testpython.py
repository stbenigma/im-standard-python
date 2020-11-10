from IM_OBJECTS import Synonym
def int2hex(pint):
    if (pint is None): return pint
    lint = pint if (type(pint) == int) else int(pint)
    retval = hex(lint & 0xfffffff)
    retval = retval[3:]
    return retval

#print (hex(-16776961 & 0xffffffff),int2hex(-16776961))
s = Synonym.select()
print (s)