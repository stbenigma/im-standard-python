from IM_JSON import *
from mystring import nvl
from IM_OBJECTS import *

def inssourceref(presult:Mergeresult,pmodeid, psources):
    """   "sourceref": {
        "ODM": ["80D2A6F4-56D6-88E4-2E84-676699D4EBF2","2021-02-13 15:23:41.412333"]
    },"""
    if psources is None: return
    for src, entry in psources.items():
        extr = Externalref(pmodeid=pmodeid, psrcname=src, psrcid=entry[0],plastupd=entry[1])
        try:
            extr.insert(pdoerrhdlng=False)
        except Exception as err:
            """simple version **** ignore error, it could be the first entry of the loading system
            laster version: if it is duplicate ID, ignore it, otherwise report it"""
            continue
            presult.markdberror(perr=err, pelem=extr.tostring())
    # for
    return


def udps2js(pemptymodel):
    model = ['theme','group'
            ,'name','defvalue','descr'
            ,'uc','dc','um','dm'
             ,'usedfor']
    if pemptymodel:
        retval = {jsguid (Modelelemtype.UDPR, '0000') : fillmodel(pmodel=model, pentries=['' for i in range(len(model)-1)]+[reflist()])}
    else:
        retval =  {jsguid (Modelelemtype.UDPR,u.udpr_id) : fillmodel(pmodel=model,pentries=
                                [u.udpr_theme,u.udpr_group,u.udpr_name,u.udpr_defaultvalue,u.udpr_descr
                                 ,u.udpr_uc,u.udpr_dc,u.udpr_um,u.udpr_dm
                                       ,reflist(plist= [Modelelemtype.getshortname(metp.metp_melt_id)
                                                     for metp in ModelelementProperty.select(pwhere=("METP_UDPR_ID = ?", u.udpr_id))])
                                ])
                 for u in Userdefprop.select()
            }
    return retval

def js2udpr(pkey,pelem,psrcname=None,psrcid=None,pmodellang=None):
    udpr = Userdefprop()
    udpr.udpr_id = jsguid2id(pkey)
    udpr.udpr_theme = pelem['theme']
    udpr.udpr_group = pelem['group']
    udpr.udpr_name = pelem['name']
    udpr.udpr_defaultvalue = pelem['defvalue']
    udpr.udpr_descr = pelem['descr']
    udpr.udpr_uc = pelem['uc']
    udpr.udpr_dc = pelem['dc']
    udpr.udpr_um = pelem['um']
    udpr.udpr_dm = pelem['dm']
    return udpr

def udps2sql(presult:Mergeresult, podmjson: JSModel, pwithextsrcref):
    global fktranslate
    fromodm2db(presult=presult, podmjson=podmjson,  pelemtype=Modelelemtype.UDPR, pjs2obj=js2udpr,
                   pwithextsrcref=pwithextsrcref)

    for jskey,jselem in podmjson.getelements(pelemtype=Modelelemtype.UDPR).items():
        """mdelelemetype_properties are emptied and loaded from source"""
        newudprid = keytransl(jskey)
        inscnt = 0
        delcnt = ModelelementProperty.delete(pwhere=("metp_udpr_id = ?", newudprid))
        for elemtype in jselem["usedfor"]:
            try:
                metp = ModelelementProperty(pmeltid=Modelelemtype.getbyshortname(elemtype).getid(),pudprid=newudprid)
                metp.insert()
                inscnt += 1
            except Exception as err:
                presult.markdberror(perr=err,pelem=list(jselem))
        #for
        presult.insertcnt += max(0,(inscnt-delcnt))
        presult.deletecnt += max(0,(delcnt-inscnt))
    #for
    return

def udpv2js(pmodeid,pmodelemtype):
    return {
        th[0]: {gr[1]: {jsguid(mtype=Modelelemtype.UDPR,id=u.udpr_id): {'name': u.udpr_name
                                    ,'value': Userdefpropvalue.udpvalue(pudprid=u.udpr_id, pmodeid=pmodeid)}
                        for u in Userdefprop.getudps(ptheme=th[0], pgroup=gr[1], pmeltname=pmodelemtype)}
                for gr in Userdefprop.grouplist(pudptheme=th[0], pmelttype=pmodelemtype)}
        for th in Userdefprop.themelist(pmelttype=pmodelemtype)
    }

def udpvs2sql(presult, pmodeid, pudps):
    if pudps is None: return
    """ "userdefprop": {
            "-theme-": {
                "-group-": {
                   UDPR1234:  {'name':"PENTA TabName", 'value': null}
                },
            },
        },
    """
    inscnt = 0
    delcnt = Userdefpropvalue.delete(pwhere=("udpv_mode_id = ?", pmodeid))
    for theme,jtheme in pudps.items():
        for group,jgroup in jtheme.items():
            for jid,jelem in jgroup.items():
                #only non-null-udpr are copied to the database
                if jelem['value'] is None: continue
                udpr = Userdefprop().getbyid(keytransl(jid))
                if ((nvl(udpr.udpr_theme) != nvl(theme)) or (nvl(udpr.udpr_group) != nvl(group))
                        or (nvl(udpr.udpr_name) != nvl(jelem['name']))):
                    presult.markdberror(perr="User defined property has unknown theme or group"
                                        ,pelem="Theme '{}', group '{}'".format(theme,group))
                    continue
                udpv = Userdefpropvalue(pmodeid=pmodeid,pudprid=udpr.udpr_id,pvalue=jelem['value'])
                try:
                    udpv.insert()
                    inscnt += 1
                except Exception as err:
                    presult.markdberror(perr=err, pelem=udpv.tostring())
            #for
        #for
    #for
    presult.insertcnt += max(0,(inscnt-delcnt))
    presult.deletecnt += max(0,(delcnt-inscnt))
    return

def documents2js(pemtpymodel):
    model = [ 'name', 'reference'
            , 'content', 'format+'
            , 'formatid', 'parent'
            ,'sourceref'
            ,'referencecnt+', 'references+']
    if pemtpymodel:
        retval = {jsguid(Modelelemtype.DOCU, "0000"):
                      fillmodel(pmodel=model,pentries=['' for i in range(6)]+[sourceref(),'0',references()])}
    else:
        retval = {jsguid(Modelelemtype.DOCU, d.docu_id):
                    fillmodel(pmodel=model,pentries=[d.docu_name,d.docu_reference
                                                  ,d.docu_content, None if d.docu_stfo_id is None else Storageformat().getbyid(d.docu_stfo_id).stfo_name
                                                  ,None if d.docu_stfo_id is None else jsguid(Modelelemtype.STFO,d.docu_stfo_id)
                                                    ,None if d.docu_docu_id is None else jsguid(Modelelemtype.DOCU, d.docu_docu_id)
                                                  ,sourceref(pvalues=Externalref.getsrcinfo(pmodeid=d.docu_id))
                                                     ,str(len(d.getrefmodes())),references(pmode=d)

                                      ]
                           )
        for d in Document.select()}
    return retval

def js2docu(pkey,pelem,psrcname=None,psrcid=None,pmodellang=None):
    docu = Document(psrcname=psrcname,psrcid=psrcid)
    docu.docu_id = jsguid2id(pkey)
    docu.docu_name = pelem['name']
    docu.docu_reference = pelem['reference']
    docu.docu_content = pelem['content']
    docu.docu_stfo_id = jsguid2id(pelem['formatid'])
    docu.docu_docu_id = jsguid2id(pelem['parent'])
    return docu

def documents2sql(presult:Mergeresult, podmjson: JSModel, pwithextsrcref):
    fromodm2db(presult=presult, podmjson=podmjson,  pelemtype=Modelelemtype.DOCU, pjs2obj=js2docu,
                   pwithextsrcref=pwithextsrcref)
    # parents = [] #(docu_id, parent_id)
    # for jid,jelem in pmodel.getelements(Modelelemtype.DOCU).items():
    #     docu = js2docu(pkey=jid,pelem=jelem)
    #     try:
    #         docuid = docu.insert()
    #     except Exception as err:
    #         pmodel.markerror(pmsg=err, pelemstr=docu.tostring())
    #         continue
    #
    #     parents.append(jsguid2id(pelem['parent']))
    #     inssourceref(pmodel=pmodel, pmodeid=docuid, psources=jelem["sourceref"])
    # #for
    # Document.updparentpairs(pparents=parents)
    return


def insreferences(presult:Mergeresult, pmodeid, prefs):
    inscnt = 0
    delcnt = ModelelemOrgu.delete(pwhere=("moou_mode_id = ?", pmodeid))
    delcnt += ModelelemDocu.delete(pwhere=("modo_mode_id = ?", pmodeid))
    for refid in prefs:
        elemtype = jsguid2type(refid)
        if elemtype == Modelelemtype.ORGU:
            obj = ModelelemOrgu(pmodeid=pmodeid, porguid=keytransl(refid))
        elif elemtype == Modelelemtype.DOCU:
            obj = ModelelemDocu(pmodeid=pmodeid, pdocuid=keytransl(refid))
        else:
            raise Exception("*****insreferences: Illegal type of element {}".format(elemtype))
        try:
            obj.insert()
            inscnt += 1
        except Exception as err:
            presult.markdberror(perr=err, pelem=[refid,pmodeid])
            continue
    # for
    presult.insertcnt += max(0,(inscnt-delcnt))
    presult.deletecnt += max(0,(delcnt-inscnt))
    return

def references(pmode=None):
    if pmode is None:
        retval = []
    else:
        retval = [jsguid(m.mode_type, m.mode_id) for m in pmode.getrefmodes(pmelttype=Modelelemtype.ENTI)]\
            +[jsguid(m.mode_type, m.mode_id) for m in pmode.getrefmodes(pmelttype=Modelelemtype.ATTR)]\
            +[jsguid(m.mode_type, m.mode_id) for m in pmode.getrefmodes(pmelttype=Modelelemtype.DOMA)]\
            +[jsguid(m.mode_type, m.mode_id) for m in pmode.getrefmodes(pmelttype=Modelelemtype.INTF)]\
            +[jsguid(m.mode_type, m.mode_id) for m in pmode.getrefmodes(pmelttype=Modelelemtype.TABL)]\
            +[jsguid(m.mode_type, m.mode_id) for m in pmode.getrefmodes(pmelttype=Modelelemtype.COLU)]\
            +[jsguid(m.mode_type, m.mode_id) for m in pmode.getrefmodes(pmelttype=Modelelemtype.DIAG)]
    # fi
    return retval


def orgUnits2js(pemptymodel):
    model = ['name', 'descr'
            , 'uc', 'dc', 'um', 'dm'
            , 'mail', 'telefon'
            , 'address', 'parent'
            , 'sourceref'
            ,'referencecnt+', 'references+'
            ]
    if pemptymodel:
        retval = {jsguid(Modelelemtype.ORGU, '0000') : fillmodel(pmodel=model
                            , pentries=['' for i in range(len(model) - 3)] + [sourceref(),0,references()]
                            )}
    else:
        retval = {jsguid(Modelelemtype.ORGU, o.orgu_id):
              fillmodel(pmodel=model,pentries=[
                  o.orgu_name,o.orgu_descr
                ,o.orgu_uc,o.orgu_dc, o.orgu_um,o.orgu_dm
                ,o.orgu_mail, o.orgu_telefon
                  , o.orgu_address, None if o.orgu_orgu_id is None else jsguid(Modelelemtype.ORGU, o.orgu_orgu_id)
                ,sourceref(pvalues=Externalref.getsrcinfo(pmodeid=o.orgu_id))
                  ,str(len(o.getrefmodes())), references(pmode=o)
                 ])
                for o in OragnisationalUnit.select()
            }
    return retval

def js2orgu(pkey,pelem,psrcname=None,psrcid=None,pmodellang=None):
    orgu:OragnisationalUnit = OragnisationalUnit(psrcname=psrcname,psrcid=psrcid)
    orgu.orgu_id = jsguid2id(pkey)
    orgu.orgu_name = pelem['name']
    orgu.orgu_orgu_id = None
    orgu.orgu_descr = pelem['descr']
    orgu.orgu_uc = pelem['uc']
    orgu.orgu_dc = pelem['dc']
    orgu.orgu_um = pelem['um']
    orgu.orgu_dm = pelem['dm']
    orgu.orgu_mail = pelem['mail']
    orgu.orgu_telefon = pelem['telefon']
    orgu.orgu_address = pelem['address']
    orgu.orgu_orgu_id = jsguid2id(pelem['parent'])
    return orgu


def orgunits2sql(presult, podmjson: JSModel, pwithextsrcref):
    fromodm2db(presult=presult, podmjson=podmjson,  pelemtype=Modelelemtype.ORGU, pjs2obj=js2orgu,
                   pwithextsrcref=pwithextsrcref)

    for jid,jelem in podmjson.getelements(pelemtype=Modelelemtype.ORGU).items():
        inssourceref(presult=presult,pmodeid=keytransl(jid), psources=jelem["sourceref"])
    #for
    return

