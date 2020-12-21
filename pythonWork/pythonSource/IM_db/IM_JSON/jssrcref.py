from IM_OBJECTS import Externalref


def inssourceref(pmodel,pmodeid, psources):
    """   "sourceref": {
        "ODM": "80D2A6F4-56D6-88E4-2E84-676699D4EBF2"
    },"""
    if psources is None: return
    for src, srcid in psources.items():
        extr = Externalref(pmodeid=pmodeid, psrcname=src, psrcid=srcid)
        try:
            extr.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelem=extr.tostring())
    # for

# inssourceref