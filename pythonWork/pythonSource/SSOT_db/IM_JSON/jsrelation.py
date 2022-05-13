from SSOT_db.IM_OBJECTS import Modelelemtype
from SSOT_db.IM_JSON import  *

def relaend2js(prelaend=None):
    model = ['enti',
            'arc',
            'assoc',
            'maptype',
            'hist',
            'mandatory',
            'cardstr+']
    if prelaend  is None:
        retval = fillmodel(pmodel=model,pentries=['','',multilangtext(),
                                                  '','','','']
                           )
    else:
        retval = fillmodel(pmodel=model, pentries=prelaend
                           )
    #fi
    return retval

def relation2js(prela):
    model = [ 'name', 'type',
        'from-to', 'to-from',
        'isinkeys+', 'sourceref',
        'uc', 'dc', 'um', 'dm',
        'minzoomlevel', 'maxzoomlevel', 'publstatus',"businessrules+",
        'userdefprops','referencedby',
         'tablesmapped+'
              ]
    if prela is None:
        retval = fillmodel(pmodel=model,
                           pentries=['', '',
                                    relaend2js(), relaend2js(),
                                       reflist(), sourceref(),
                                      '', '','','',
                                    0,4,'DRAFT',buruinelements(None),
                                    userdefprops(),reflist(),tabreflist()
                                    ]
                           )
    else:
        keys = [k for k in Key.select(pwhere=("""keys_id in (select kele_keys_id 
                                                    from key_elements 
                                                    where kele_rela_id = ?)""", prela.rela_id))]
        retval = fillmodel(pmodel=model,
                   pentries=[prela.rela_name, prela.rela_type,
                                relaend2js(prelaend= [jsguid(Modelelemtype.ENTI, prela.rela_enti_id_from),
                                 None if prela.rela_arcs_id_from is None else jsguid(Modelelemtype.ARCS, prela.rela_arcs_id_from),
                                 multilangtext(prela.rela_assoc_from_to_l),
                                 prela.rela_maptype_from_to,
                                 Boolean.str2bool(prela.rela_hist_from_to),
                                 Boolean.str2bool(prela.rela_mandatory_from_to),
                                 prela.to_cardstr()
                                 ]),
                                relaend2js(prelaend=[ jsguid(Modelelemtype.ENTI, prela.rela_enti_id_to),
                                   None if prela.rela_arcs_id_to is None else jsguid(Modelelemtype.ARCS, prela.rela_arcs_id_to),
                                   multilangtext(prela.rela_assoc_to_from_l),
                                   prela.rela_maptype_to_from,
                                   Boolean.str2bool(prela.rela_hist_to_from),
                                   Boolean.str2bool(prela.rela_mandatory_to_from),
                                   prela.from_cardstr()
                                ]),
                                 reflist(plist=[jsguid(Modelelemtype.KEYS, k.keys_id) for k in keys]),
                              sourceref(pvalues=Externalref.getsrcinfo(pmodeid=prela.rela_id)),
                                prela.rela_uc, prela.rela_dc, prela.rela_um, prela.rela_dm,
                                prela.getminzoomlevel(), prela.getmaxzoomlevel(), prela.getpublstatus(),
                                buruinelements(prela.rela_id),
                                userdefprops(pprops=udpv2js(pmodeid=prela.rela_id, pmodelemtype=Modelelemtype.RELA)),
                               [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=prela.rela_id)]\
                                +[jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=prela.rela_id)],
                            tabreflist(plist={
                                jsguid(Modelelemtype.INTF, s.getid()):
                                    [jsguid(Modelelemtype.TABL, t.tabl_id)
                                     for t in TablEntiMap.gettabllist(prelaid=prela.rela_id,
                                                             pintfid=s.getid())
                                    ]
                    for s in Interface.getmapped(prelaid=prela.rela_id)})

                               ]
                   )
    # fi
    return retval


def relations2js(pemptymodel):
    if pemptymodel:
        relas = {jsguid(Modelelemtype.RELA, '0000') : relation2js(None)}
    else:
        relas = {jsguid(Modelelemtype.RELA, r.rela_id): relation2js(r) for r in Relation.select()}
    return relas

def js2rela (pkey,pelem,psrcname=None,psrcid=None,pmodellang=None):
    rela = Relation(psrcname=psrcname,psrcid=psrcid)
    rela.rela_id = pkey
    rela.rela_name = pelem['name']
    rela.rela_type = pelem['type']
    rela.rela_enti_id_from = pelem['from-to']['enti']
    rela.rela_arcs_id_from = pelem['from-to']['arc']
    rela.rela_assoc_from_to = pelem['from-to']['assoc'][pmodellang]
    rela.rela_maptype_from_to = pelem['from-to']['maptype']
    rela.rela_mandatory_from_to = Boolean.bool2str(pelem['from-to']['mandatory'])
    rela.rela_hist_from_to = Boolean.bool2str(pelem['from-to']['hist'])
    rela.rela_enti_id_to = pelem['to-from']['enti']
    rela.rela_arcs_id_to = pelem['to-from']['arc']
    rela.rela_assoc_to_from = pelem['to-from']['assoc'][pmodellang]
    rela.rela_maptype_to_from = pelem['to-from']['maptype']
    rela.rela_mandatory_to_from = Boolean.bool2str(pelem['to-from']['mandatory'])
    rela.rela_hist_to_from = Boolean.bool2str(pelem['to-from']['hist'])
    rela.rela_uc = pelem['uc']
    rela.rela_dc = pelem['dc']
    rela.rela_um = pelem['um']
    rela.rela_dm = pelem['dm']
    return rela

def relations2sql(presult:Mergeresult, pjson: JSModel, pwithextsrcref):
    """there are arcs without extref (those generated for subtypes) will be handled in fromjson2db"""
    fromjson2db(presult=presult, pjson=pjson,  pelemtype=Modelelemtype.RELA, pjs2obj=js2rela,
                   pwithextsrcref=pwithextsrcref)

    for jid, jelem in pjson.getelements(pelemtype=Modelelemtype.RELA).items():
        newrelaid = presult.keytransl(jid)
        if newrelaid  == 0: continue  # element was not treated
        minzoomlevel = jelem['minzoomlevel']
        maxzoomlevel = jelem['maxzoomlevel']
        publstatus = jelem['publstatus']
        Modelelement.upddisplelements(pmodeid=newrelaid, pminzl=minzoomlevel, pmaxzl=maxzoomlevel, ppublstat=publstatus)
        replacelgtx(presult=presult, pmodeid=newrelaid, pattr=Languagetext.RELA_TEXT_TO, ptexts=jelem['to-from']['assoc'])
        replacelgtx(presult=presult, pmodeid=newrelaid, pattr=Languagetext.RELA_TEXT_FROM, ptexts=jelem['from-to']['assoc'])
        insreferences(presult=presult, pmodeid=newrelaid, prefs=jelem['referencedby'])
        if pwithextsrcref:
            inssourceref(presult=presult,pmodeid=newrelaid, psources=jelem["sourceref"])
        udpvs2sql(presult=presult, pmodeid=newrelaid, pudps=jelem["userdefprops"])

    # for
    return


def arcs2js(pemptymodel):
    model = ['name', 'entity',
        'relations', 'sourceref',
        'uc', 'dc', 'um', 'dm'
             ]
    if pemptymodel:
        retval= {jsguid(Modelelemtype.ARCS, "0000") : fillmodel(pmodel=model,pentries=['','',reflist(),sourceref(),'','','',''])}
    else:
        retval = {jsguid(Modelelemtype.ARCS, a.arcs_id): fillmodel(pmodel=model,
                                                                pentries=[a.arcs_name,
                        jsguid(Modelelemtype.ENTI, a.arcs_enti_id),
                        [jsguid(Modelelemtype.RELA, r.rela_id) for r in a.getrelalist()],
                        Externalref.getsrcinfo(pmodeid=a.arcs_id),
                        a.arcs_uc,
                        a.arcs_dc,
                        a.arcs_um,
                        a.arcs_dm
                                ]
                                                               )
                for a in Arc.select()
                }
    # fi
    return retval

def js2arcs(pkey,pelem,psrcname=None,psrcid=None,pmodellang=None):
    arc = Arc(srcname=psrcname,srcid=psrcid,arcs_name=pelem['name'],
            arcs_id = pkey,
            arcs_enti_id = pelem['entity'],
            arcs_uc = pelem['uc'],
            arcs_dc = pelem['dc'],
            arcs_um = pelem['um'],
            arcs_dm = pelem['dm'])
    return arc

def arcs2sql(presult:Mergeresult, pjson: JSModel, pwithextsrcref):
    """there are arcs without extref (those generated for subtypes) will be handled in fromjson2db"""
    fromjson2db(presult=presult, pjson=pjson,  pelemtype=Modelelemtype.ARCS, pjs2obj=js2arcs,
                   pwithextsrcref=pwithextsrcref)

    for jid, jelem in pjson.getelements(pelemtype=Modelelemtype.ARCS).items():
        if pwithextsrcref:
            inssourceref(presult=presult,pmodeid=presult.keytransl(jid), psources=jelem["sourceref"])
    # for
    return

