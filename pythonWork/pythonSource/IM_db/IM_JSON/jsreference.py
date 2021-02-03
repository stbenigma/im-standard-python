
from IM_OBJECTS import Externalref, Document, Modelelemtype, OragnisationalUnit, Storageformat,ModelelementProperty,Userdefprop,ModelelemOrgu,ModelelemDocu,Userdefpropvalue
from IM_JSON import *
from mystring import nvl

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
    return


def udps2js():
    udp = {jsguid (Modelelemtype.UDPR,u.udpr_id) : {'theme': u.udpr_theme
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
    return

"""transfer references and subtypes"""
def udprefs2sql(pmodel):
    #    insudp(pmodeid=entiid, pudps=jenti["userdefprops"])
    return

def udpv2js(pmodeid,pmodelemtype):
    return {
        th[0]: {gr[1]: {jsguid(type=Modelelemtype.UDPR,id=u.udpr_id): {'name': u.udpr_name
                                    ,'value': Userdefpropvalue.udpvalue(pudprid=u.udpr_id, pmodeid=pmodeid)}
                        for u in Userdefprop.getudps(ptheme=th[0], pgroup=gr[1], pmeltname=pmodelemtype)}
                for gr in Userdefprop.grouplist(pudptheme=th[0], pmelttype=pmodelemtype)}
        for th in Userdefprop.themelist(pmelttype=pmodelemtype)
    }

def updvs2sql(pmodel:JSModel, pmodeid, pudps):
    if pudps is None: return
    """ "userdefprop": {
            "-theme-": {
                "-group-": {
                   UDPR1234:  {'name':"PENTA TabName", 'value': null}
                },
            },
        },
    """
    for theme,jtheme in pudps.items():
        for group,jgroup in jtheme.items():
            for jid,jelem in jgroup.items():
                udpr = Userdefprop().getbyid(jsguid2id(jid))
                if ((nvl(udpr.udpr_theme) != nvl(theme)) or (nvl(udpr.udpr_group) != nvl(group))
                        or (nvl(udpr.udpr_name) != nvl(jelem['name']))):
                    pmodel.markerror(pmsg="User defined property has unknown theme or group",pelemstr="Theme '{}', group '{}'".format(theme,group))
                    continue
                udpv = Userdefpropvalue(pmodeid=pmodeid,pudprid=udpr.udpr_id,pvalue=jelem['value'])
                try:
                    udpv.insert()
                except Exception as err:
                    pmodel.markerror(pmsg=err, pelemstr=udpv.tostring())
            #for
        #for
    #for
    return

def documents2js(pemtpymodel):
    model = [ 'name', 'reference'
            , 'content', 'format+'
            , 'formatid', 'parent'
            ,'referencecnt+', 'references']
    if pemtpymodel:
        retval = {"DOCU0000": fillmodel(pmodel=model,pentries=['' for i in range(len(model)-1)]+[references()])}
    else:
        retval = {jsguid(Modelelemtype.DOCU, d.docu_id):
                    fillmodel(pmodel=model,pentries=[d.docu_name,d.docu_reference
                                                  ,d.docu_content, None if d.docu_stfo_id is None else Storageformat().getbyid(d.docu_stfo_id).stfo_name
                                                  ,None if d.docu_stfo_id is None else jsguid(Modelelemtype.STFO,d.docu_stfo_id)
                                                    ,None if d.docu_docu_id is None else jsguid(Modelelemtype.DOCU, d.docu_docu_id)
                                                  ,len(d.getrefmodes()),references(pmode=d)

                                      ]
                           )
        for d in Document.select()}
    return retval

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

def references(pmode=None):
    model = [ 'entities', 'attributes'
            ,'domains','systems'
            ,'tables','columns','diagrams'
            ]
    if pmode is None:
        retval = fillmodel(pmodel=model,pentries=[[] for i in range(len(model))])
    else:
        retval = fillmodel(pmodel=model,pentries=[
            [jsguid(m.mode_type, m.mode_id) for m in pmode.getrefmodes(pmelttype=Modelelemtype.ENTI)]
            ,[jsguid(m.mode_type, m.mode_id) for m in pmode.getrefmodes(pmelttype=Modelelemtype.ATTR)]
            ,[jsguid(m.mode_type, m.mode_id) for m in pmode.getrefmodes(pmelttype=Modelelemtype.DOMA)]
            ,[jsguid(m.mode_type, m.mode_id) for m in pmode.getrefmodes(pmelttype=Modelelemtype.INTF)]
            ,[jsguid(m.mode_type, m.mode_id) for m in pmode.getrefmodes(pmelttype=Modelelemtype.TABL)]
            ,[jsguid(m.mode_type, m.mode_id) for m in pmode.getrefmodes(pmelttype=Modelelemtype.COLU)]
            , [jsguid(m.mode_type, m.mode_id) for m in pmode.getrefmodes(pmelttype=Modelelemtype.DIAG)]
        ])
    # fi
    return retval


def orgUnits2js(pemptymodel):
    model = ['name', 'descr'
            , 'uc', 'dc', 'um', 'dm'
            , 'mail', 'telefon'
            , 'address', 'parent'
            ,'referencecnt+', 'references'
            ]
    if pemptymodel:
        retval = fillmodel(pmodel=model
                           ,pentries=['' for i in range(len(model)-1)]+[references()]
                           )
    else:
        retval = {jsguid(Modelelemtype.ORGU, o.orgu_id):
              fillmodel(pmodel=model,pentries=[
                  o.orgu_name,o.orgu_descr
                ,o.orgu_uc,o.orgu_dc, o.orgu_um,o.orgu_dm
                ,o.orgu_mail, o.orgu_telefon
                  , o.orgu_address, None if o.orgu_orgu_id is None else jsguid(Modelelemtype.ORGU, o.orgu_orgu_id)
                ,str(len(o.getrefmodes()))
                , references(pmode=o)
                 ])
                for o in OragnisationalUnit.select()
            }
    return retval

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
