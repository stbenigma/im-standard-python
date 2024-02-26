from SSOT_db.IM_JSON import *
from SSOT_db.IM_JSON import buruinelements
from SSOT_infra import nvl

TABLEMODEL = ['name', 'datamodel-name+',
              'datamodel-id', 'prefix',
              'descr',
              'uc', 'dc', 'um', 'dm',
              'minzoomlevel', 'maxzoomlevel', 'publstatus',
              'CRUD',
              'columns+', "businessrules+", 'userdefprops',
              'entitiesmapped', 'tablesmapped', 'relationsmapped',
              'sourceref', 'raci+', 'referencedby'
              ]


def jsontable(name, datamodelid,uc, dc, **kwargs):
    table = dict()
    initjselement(table, TABLEMODEL)
    table["name"] = name
    table["uc"] = uc
    table["dc"] = dc
    table['datamodel-id'] = datamodelid
    table['prefix'] = None
    table['entitiesmapped'] = []
    table['tablesmapped'] = []
    table['relationsmapped'] = []
    table["referencedby"] = []
    table["userdefprops"] = dict()

    fillargs(model=table, refmodel=TABLEMODEL, **kwargs)
    return table


def tables2js(pemptymodel):
    if pemptymodel:
        retval = {jsguid(Modelelemtype.TABL, '0000'):
                      fillmodel(pmodel=TABLEMODEL,
                                pentries=['' for i in range(9)]
                                         + [0, 4, 'DRAFT',
                                            crudstr(),
                                            reflist(),
                                            buruinelements(None),
                                            userdefprops(),
                                            [jsguid(
                                                Modelelemtype.ENTI,
                                                '0000')],
                                            [jsguid(
                                                Modelelemtype.TABL,
                                                '0000')],
                                            [jsguid(
                                                Modelelemtype.RELA,
                                                '0000'), jsguid(
                                                Modelelemtype.ENTI,
                                                '0000')],
                                            sourceref(),
                                            jsentity.racilist(),
                                            reflist()])
                  }
    else:
        retval = {jsguid(Modelelemtype.TABL, t.tabl_id):
                      fillmodel(pmodel=TABLEMODEL,
                                pentries=[t.tabl_name,
                                          Datamodel().getbyid(t.tabl_datm_id).getname(),
                                          jsguid(Modelelemtype.DATM, Datamodel().getbyid(t.tabl_datm_id).getid()),
                                          t.tabl_prefix, t.tabl_descr,
                                          t.tabl_uc, t.tabl_dc, t.tabl_um, t.tabl_dm,
                                          t.getminzoomlevel(), t.getmaxzoomlevel(), t.getpublstatus(),
                                          crudstr(pcreate=t.tabl_create, pread=t.tabl_read, pupdate=t.tabl_update,
                                                  pdelete=t.tabl_delete),
                                          [jsguid(Modelelemtype.COLU, c.colu_id) for c in t.getcolumns()],
                                          buruinelements(t.tabl_id),
                                          udpv2js(pmodeid=t.tabl_id, pmodelemtype=Modelelemtype.TABL),
                                          [jsguid(Modelelemtype.ENTI, e.enti_id)
                                           for e in ModeMap.getentilist(tablid=t.tabl_id)],
                                          [jsguid(Modelelemtype.TABL, ta.tabl_id)
                                           for ta in ModeMap.gettabllist(tablid=t.tabl_id)],
                                          [jsguid(Modelelemtype.RELA, rid[0])
                                           for rid in ModeMap.getrelaidlist(modeid=t.tabl_id)],
                                          Externalref.getsrcinfo(pmodeid=t.tabl_id), jsentity.racilist(t.tabl_id),
                                          [jsguid(Modelelemtype.DOCU, d[0]) for d in
                                           Document.getrefdoculist(pid=t.tabl_id)] \
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
    tabl.tabl_id = pkey
    tabl.tabl_datm_id = pelem['datamodel-id']
    tabl.tabl_prefix = pelem['prefix']
    tabl.tabl_descr = pelem['descr']
    tabl.tabl_uc = pelem['uc']
    tabl.tabl_dc = pelem['dc']
    tabl.tabl_um = pelem['um']
    tabl.tabl_dm = pelem['dm']
    return tabl


def tables2sql(presult: Mergeresult, pjson: JSModel, pwithextsrcref):
    fromjson2db(presult=presult, pjson=pjson, pelemtype=Modelelemtype.TABL, pjs2obj=js2tabl,
                pwithextsrcref=pwithextsrcref)

    for jid, jelem in pjson.getelements(pelemtype=Modelelemtype.TABL).items():
        minzoomlevel = jelem['minzoomlevel']
        maxzoomlevel = jelem['maxzoomlevel']
        publstatus = jelem['publstatus']
        newtablid = presult.keytransl(jid)
        if newtablid == 0: continue  # element was not treated
        Modelelement.upddisplelements(pmodeid=newtablid, pminzl=minzoomlevel, pmaxzl=maxzoomlevel, ppublstat=publstatus)
        insreferences(presult=presult, pmodeid=newtablid, prefs=jelem['referencedby'])
        inssourceref(presult=presult, pmodeid=newtablid, psources=jelem["sourceref"])
        instablemapping(presult=presult, ptablid=newtablid,
                        pmappedentis=nvl(jelem.get('entitiesmapped'),[]) ,
                        pmappedrelas= nvl(jelem.get('relationsmapped'),[]),
                        pmappedtabs= nvl(jelem.get('tablesmapped'),[]))
        udpvs2sql(presult=presult, pmodeid=newtablid, pudps=jelem["userdefprops"])
    return


def instablemapping(presult: Mergeresult, ptablid, pmappedentis,pmappedrelas,pmappedtabs):
    def maponetype(result,tablid,mappedelems,elemtype):
        inscnt=0

        for jid in mappedelems:
            newkey = presult.keytransl(jid)
            tabl = Table().getbyid(tablid)
            if elemtype in (Modelelemtype.ENTI, Modelelemtype.RELA):
                mapping = Mapping.selectorcreate(maptype=Mapping.MAPTYPE_DATM_IM,
                                              name=str(tabl.tabl_datm_id) + "-" + tabl.tabl_name,
                                              modeid1=tabl.tabl_datm_id,
                                              modeid2=None) #DATM-IM has no second modeid2
            elif elemtype in (Modelelemtype.TABL,):
                tabl2 = Table().getbyid(newkey)
                mapping = Mapping.selectorcreate(maptype=Mapping.MAPTYPE_DATM_DATM,
                                              name=str(tabl.tabl_datm_id) + "-" + tabl.tabl_name + "-" + str(tabl2.tabl_datm_id),
                                              modeid1=tabl.tabl_datm_id,
                                              modeid2=tabl2.tabl_datm_id)


            momo = ModeMap(momo_maps_id=mapping.maps_id,
                            momo_mode_id1=tablid,
                            momo_mode_id2=newkey,
                            momo_sub_enti_id=None,
                            momo_onedirection=Boolean.TRUE,
                            momo_uc=mapping.maps_uc, momo_dc=mapping.maps_dc,
                            momo_descr=None,
                            momo_rule_frwd=None,
                            momo_rule_bckw=None
                            )
            momo.insert()
            # tema = TablEntiMap()
            # tema.tema_tabl_id = tablid
            # tema.tema_enti_id = newkey if elemtype == Modelelemtype.ENTI else None
            # tema.tema_rela_id = newkey if elemtype == Modelelemtype.RELA else None
            # tema.tema_tabl_id = newkey if elemtype == Modelelemtype.TABL else None
            # try:
            #     tema.insert()
            #     inscnt += 1
            # except Exception as err:
            #     result.markdberror(perr=err, pelem="tablid={}, enti/relaid={}".format(tablid, newkey))
            #     continue
        # for
        return inscnt

    inscnt = 0
    delcnt = ModeMap.delete(pwhere=("momo_mode_id1 = ?", ptablid))
    delcnt += Mapping.delete(pwhere=("maps_mode_id1 = ?", ptablid))
    inscnt += maponetype(result=presult,tablid=ptablid,
                         mappedelems=pmappedentis,
                         elemtype=Modelelemtype.ENTI
                         )
    inscnt += maponetype(result=presult,tablid=ptablid,
                         mappedelems=pmappedrelas,
                         elemtype=Modelelemtype.RELA
                         )
    inscnt += maponetype(result=presult,tablid=ptablid,
                         mappedelems=pmappedtabs,
                         elemtype=Modelelemtype.TABL
                         )

    presult.addinscnt(max(0, (inscnt - delcnt)),f"Table to Entity mapping  for Element {ptablid}")
    presult.adddelcnt(max(0, (delcnt - inscnt)),f"Table to Entity mapping  for Element {ptablid}")
    return
