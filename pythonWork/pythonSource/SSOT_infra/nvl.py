
def nvl(pval1, pval2=''):
    """oracles nvl function: return val1 if it is not None, val2 otherwise"""

    return pval1 if pval1 is not None else pval2


def nvl2(pval, pvalNone, pvalnNone):
    """oracles nvl2 function: return valNone if val is None, valnNone otherwise """
    return pvalNone if pval is None else pvalnNone
