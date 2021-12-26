from IM_db.IM_JSON import  *

def tables2js(pemptymodel):
    model = ['name', 'interface-name+'
        , 'interface-id', 'prefix'
        , 'descr'
        , 'uc', 'dc', 'um', 'dm'
        , 'minzoomlevel', 'maxzoomlevel', 'devstatus'
        ,'CRUD'
        , 'columns+', 'userdefprops'
        , 'entitiesmapped', 'relationsmapped'
        , 'sourceref', 'referencedby'
             ]
    if pemptymodel:
        retval = {jsguid(Modelelemtype.TABL, '0000'): fillmodel(pmodel=model, pentries=['' for i in range(9)]
                                                                                       + [0, 4, 'DEV'
                                                                                          ,crudstr()
                                                                                           , reflist(),userdefprops()
                                                                                           ,[jsguid(Modelelemtype.ENTI, '0000')]
                                                                                          , [jsguid(Modelelemtype.RELA, '0000')]
                                                                                           , sourceref(), reflist()])
                  }
    else:
        retval = {jsguid(Modelelemtype.TABL, t.tabl_id):
                      fillmodel(pmodel=model, pentries=[t.tabl_name
                          , Interface().getbyid(t.tabl_intf_id).getname()
                          , jsguid(Modelelemtype.INTF, Interface().getbyid(t.tabl_intf_id).getid())
                          , t.tabl_prefix, t.tabl_descr
                          , t.tabl_uc, t.tabl_dc, t.tabl_um, t.tabl_dm
                          , t.getminzoomlevel(), t.getmaxzoomlevel(), t.getdevstatus()
                          , crudstr(pcreate=t.tabl_create,pread=t.tabl_read,pupdate=t.tabl_update,pdelete=t.tabl_delete)
                          , [jsguid(Modelelemtype.COLU, c.colu_id) for c in t.getcolumns()]
                          , udpv2js(pmodeid=t.tabl_id, pmodelemtype=Modelelemtype.TABL)
                          , [jsguid(Modelelemtype.ENTI, e.enti_id)
                                    for e in TablEntiMap.getentilist(ptablid=t.tabl_id)]
                        , [jsguid(Modelelemtype.RELA,r.rela_id)
                                 for r in TablEntiMap.getrelalist(ptablid=t.tabl_id)]
                          , Externalref.getsrcinfo(pmodeid=t.tabl_id)
                          , [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=t.tabl_id)] \
                                                        + [jsguid(Modelelemtype.ORGU, d[0]) for d in
                                                           OragnisationalUnit.getreforgulist(pid=t.tabl_id)]
                                                        ])
                  for t in Table.select(porderby="tabl_id")
                  }
    # fi
    return retval


def js2tabl(pkey, pelem, psrcname=None, psrcid=None, pmodellang=None):
    tabl = Table()
    tabl.tabl_name = pelem['name']
    tabl.tabl_id = jsguid2id(pkey)
    tabl.tabl_intf_id = jsguid2id(pelem['interface-id'])
    tabl.tabl_prefix = pelem['prefix']
    tabl.tabl_descr = pelem['descr']
    tabl.tabl_uc = pelem['uc']
    tabl.tabl_dc = pelem['dc']
    tabl.tabl_um = pelem['um']
    tabl.tabl_dm = pelem['dm']
    return tabl


def tables2sql(presult: Mergeresult, podmjson: JSModel, pwithextsrcref):
    fromodm2db(presult=presult, podmjson=podmjson, pelemtype=Modelelemtype.TABL, pjs2obj=js2tabl,
               pwithextsrcref=pwithextsrcref)

    for jid, jelem in podmjson.getelements(pelemtype=Modelelemtype.TABL).items():
        minzoomlevel = jelem['minzoomlevel']
        maxzoomlevel = jelem['maxzoomlevel']
        devstatus = jelem['devstatus']
        newtablid = keytransl(jid)
        Modelelement.upddisplelements(pmodeid=newtablid, pminzl=minzoomlevel, pmaxzl=maxzoomlevel, pdevstat=devstatus)
        insreferences(presult=presult, pmodeid=newtablid, prefs=jelem['referencedby'])
        inssourceref(presult=presult, pmodeid=newtablid, psources=jelem["sourceref"])
        instablemapping(presult=presult, ptablid=newtablid,
                        pmappedelems=jelem['entitiesmapped'] + jelem['relationsmapped'])
        udpvs2sql(presult=presult, pmodeid=newtablid, pudps=jelem["userdefprops"])
    return


def instablemapping(presult: Mergeresult, ptablid, pmappedelems):
    inscnt = 0
    delcnt = TablEntiMap.delete(pwhere=("tema_tabl_id = ?", ptablid))
    for jid in pmappedelems:
        elemtype = jsguid2type(jid)
        tema = TablEntiMap()
        tema.tema_tabl_id = ptablid
        tema.tema_rela_id = keytransl(jid) if elemtype == Modelelemtype.RELA else None
        tema.tema_enti_id = keytransl(jid) if elemtype == Modelelemtype.ENTI else None
        try:
            tema.insert()
            inscnt += 1
        except Exception as err:
            presult.markdberror(perr=err, pelem="tablid={}, enti/relaid={}".format(ptablid, jsguid2id(jentiid)))
            continue
    # for
    presult.addinscnt(max(0, (inscnt - delcnt)))
    presult.adddelcnt(max(0, (delcnt - inscnt)))
    return
