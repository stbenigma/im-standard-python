from IM_OBJECTS import Externalref, Document, Modelelemtype, OragnisationalUnit, Storageformat,ModelelementProperty,Userdefprop
from IM_JSON import jsguid

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


def udps2js():
    udp = {jsguid ('UDPR',u.udpr_id) : {'theme': u.udpr_theme
                                       ,'group': u.udpr_group
                                       ,'name':u.udpr_name
                                       ,'usedfor' : [Modelelemtype.getshortname(metp.metp_melt_id)
                                                     for metp in ModelelementProperty().select(pwhere="METP_UDPR_ID = {}".format(u.udpr_id))]
                                       }
                 for u in Userdefprop().select()
            }
    return udp

def documents2js():
    docus = {jsguid(Modelelemtype.DOCU, d.docu_id):
        {
            'name': d.docu_name
            , 'reference': d.docu_reference
            , 'content': d.docu_content
            , 'format': None if d.docu_stfo_id is None else Storageformat().getbyid(d.docu_stfo_id).stfo_name
            , 'parent': None if d.docu_docu_id is None else jsguid(Modelelemtype.DOCU, d.docu_docu_id)
            ,'referencecnt': len(d.getrefmodes())
            , 'references': {
                            'entities': [jsguid(m.mode_type, m.mode_id) for m in d.getrefmodes(pmelttype=Modelelemtype.ENTI)]
                            ,'attributes': [jsguid(m.mode_type, m.mode_id) for m in d.getrefmodes(pmelttype=Modelelemtype.ATTR)]
                                ,'domains': [jsguid(m.mode_type, m.mode_id) for m in d.getrefmodes(pmelttype=Modelelemtype.DOMA)]
                                ,'systems': [jsguid(m.mode_type, m.mode_id) for m in d.getrefmodes(pmelttype=Modelelemtype.INTF)]
                                ,'tables': [jsguid(m.mode_type, m.mode_id) for m in d.getrefmodes(pmelttype=Modelelemtype.TABL)]
                                ,'columns': [jsguid(m.mode_type, m.mode_id) for m in d.getrefmodes(pmelttype=Modelelemtype.COLU)]
                                ,'diagrams': [jsguid(m.mode_type, m.mode_id) for m in d.getrefmodes(pmelttype=Modelelemtype.DIAG)]
                                }
        }
        for d in Document.select()}
    return docus

def orgUnits2js():
    orgus = {jsguid(Modelelemtype.ORGU, o.orgu_id):
        {
            'name': o.orgu_name
            , 'descr': o.orgu_descr
            , 'uc': o.orgu_uc
            , 'dc': o.orgu_dc
            , 'um': o.orgu_um
            , 'dm': o.orgu_dm
            , 'mail': o.orgu_mail
            , 'telefon': o.orgu_telefon
            , 'address': o.orgu_address
            , 'parent': None if o.orgu_orgu_id is None else jsguid(Modelelemtype.ORGU, o.orgu_orgu_id)
            ,'referencecnt': len(o.getrefmodes())
            , 'references': {
                            'entities': [jsguid(m.mode_type, m.mode_id) for m in o.getrefmodes(pmelttype=Modelelemtype.ENTI)]
                            ,'attributes': [jsguid(m.mode_type, m.mode_id) for m in o.getrefmodes(pmelttype=Modelelemtype.ATTR)]
                            ,'domains': [jsguid(m.mode_type, m.mode_id) for m in o.getrefmodes(pmelttype=Modelelemtype.DOMA)]
                            ,'systems': [jsguid(m.mode_type, m.mode_id) for m in o.getrefmodes(pmelttype=Modelelemtype.INTF)]
                            ,'tables': [jsguid(m.mode_type, m.mode_id) for m in o.getrefmodes(pmelttype=Modelelemtype.TABL)]
                            ,'columns': [jsguid(m.mode_type, m.mode_id) for m in o.getrefmodes(pmelttype=Modelelemtype.COLU)]
                            }
        }
        for o in OragnisationalUnit.select()}
    return orgus