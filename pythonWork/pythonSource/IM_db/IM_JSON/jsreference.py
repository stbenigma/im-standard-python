
from IM_OBJECTS import Externalref, Document, Modelelemtype, OragnisationalUnit, Storageformat,ModelelementProperty,Userdefprop,ModelelemOrgu,ModelelemDocu
from IM_JSON import jsguid,JSModel,jsguid2id

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
            pmodel.markerror(pmsg=err, pelemstr=extr.tostring())
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

def udps2sql(pmodel:JSModel):
    for udpranker,judp in pmodel.jsmodel['userdefprops'].items():
        udpr = Userdefprop(ptheme=judp['theme'],pgroup=judp['group'],pname=judp['name'])
        udpr.udpr_id = jsguid2id(udpranker)
        try:
            udpr.insert()
        except Exception as err:
            error(pmsg=err, pelem=list(judp))
            continue

        for melttype in judp['usedfor']:
            try:
                ModelelementProperty(pmeltid=Modelelemtype.getbyshortname(melttype).getid(),pudprid=udpr.udpr_id).insert()
            except Exception as err:
                error(pmsg=err, pelem=list(judp))
        #for
    #for

"""transfer references and subtypes"""
def udprefs2sql(pmodel):
    #    insudp(pmodeid=entiid, pudps=jenti["userdefprops"])
    return


def documents2js():
    docus = {jsguid(Modelelemtype.DOCU, d.docu_id):
        {
            'name': d.docu_name
            , 'reference': d.docu_reference
            , 'content': d.docu_content
            , 'format': None if d.docu_stfo_id is None else Storageformat().getbyid(d.docu_stfo_id).stfo_name
            , 'formatid': None if d.docu_stfo_id is None else jsguid(Modelelemtype.STFO,d.docu_stfo_id)
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

def documents2sql(pmodel):
    parents = [] #(docu_id, parent_id)
    for jid,jelem in pmodel.jsmodel['documents'].items():
        docu = Document()
        docu.docu_id = jsguid2id(jid)
        docu.docu_name = jelem['name']
        docu.docu_reference = jelem['reference']
        parentid = jsguid2id(jelem['parent'])
        if parentid is not None: parents.append((docu.docu_id, parentid))
        docu.docu_content = jelem['content']
        docu.docu_stfo_id = jsguid2id(jelem['formatid'])
        try:
            docu.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=docu.tostring())
            continue
    #for
    Document.updparentpairs(pparents=parents)
    return

"""transfer references and subtypes"""
def docurefs2sql(pmodel):
    for jid,jelem in pmodel.jsmodel['documents'].items():
        jrefs = jelem['references']
        for refid in jrefs['entities'] + jrefs['attributes'] +jrefs['domains'] +jrefs['systems'] +jrefs['tables'] +jrefs['columns'] :
            modo = ModelelemDocu(pmodeid=jsguid2id(refid),pdocuid=jsguid2id(jid))
            try:
                modo.insert()
            except Exception as err:
                pmodel.markerror(pmsg=err, pelemstr=[refid]+list(jelem))
                continue
        #for
    #for
    #    insudp(pmodeid=entiid, pudps=jenti["userdefprop"])
    return

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

def orgunits2sql(pmodel:JSModel):
    parents = [] #(orgu_id, parent_id)
    for jid,jelem in pmodel.jsmodel['orgunits'].items():
        orgu = OragnisationalUnit()
        orgu.orgu_id = jsguid2id(jid)
        orgu.orgu_name = jelem['name']
        orgu.orgu_orgu_id = None
        parentid = jsguid2id(jelem['parent'])
        if parentid is not None: parents.append((orgu.orgu_id,parentid))
        orgu.orgu_descr = jelem['descr']
        orgu.orgu_uc = jelem['uc']
        orgu.orgu_dc = jelem['dc']
        orgu.orgu_um = jelem['um']
        orgu.orgu_dm = jelem['dm']
        orgu.orgu_mail = jelem['mail']
        orgu.orgu_telefon = jelem['telefon']
        orgu.orgu_address = jelem['address']
        try:
            orguid = orgu.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=orgu.tostring())
            continue
        # inssourceref(pmodel = pmodel,pmodeid=jsguid2id(jid), psources=jelem["sourceref"])
    #for
    OragnisationalUnit.updparentpairs(pparents=parents)
    return

"""transfer references and subtypes"""
def orgurefs2sql(pmodel:JSModel):
    for jid,jelem in pmodel.jsmodel['orgunits'].items():
        jrefs = jelem['references']
        for refid in jrefs['entities'] + jrefs['attributes'] +jrefs['domains'] +jrefs['systems'] +jrefs['tables'] +jrefs['columns'] :
            moou = ModelelemOrgu(pmodeid=jsguid2id(refid),porguid=jsguid2id(jid))
            try:
                moou.insert()
            except Exception as err:
                pmodel.markerror(pmsg=err, pelemstr=[refid]+list(jelem))
                continue
        #for
    #for
    #    insudp(pmodeid=entiid, pudps=jenti["userdefprop"])
    return
