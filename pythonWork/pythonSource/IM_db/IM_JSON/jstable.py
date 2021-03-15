from IM_OBJECTS import Table,Modelelemtype,Document,Interface,TablEntiMap,Externalref,OragnisationalUnit
from IM_JSON import *

def tables2js(pemptymodel):
    model = ['name','interface-name+'
                ,'interface-id+','prefix'
               ,'descr'
                , 'uc', 'dc', 'um', 'dm'
        , 'minzoomlevel', 'maxzoomlevel', 'devstatus'
        ,'columns+', 'userdefprops'
                ,'entitiesmapped', 'sourceref'
               , 'refindocuments+', 'refbyorgunits+'
             ]
    if pemptymodel:
        retval = {jsguid(Modelelemtype.TABL,'0000') : fillmodel(pmodel=model, pentries=['' for i in range(9)]
                                                   + [0,4,'DEV',reflist(), userdefprops()
                                                       , reflist(), sourceref()
                                                       , reflist(), reflist()])}
    else: 
        retval={jsguid(Modelelemtype.TABL,t.tabl_id) :
                fillmodel(pmodel=model,pentries=[t.tabl_name
                   ,Interface().getbyid(t.tabl_intf_id).getname()
                   ,jsguid(Modelelemtype.INTF, Interface().getbyid(t.tabl_intf_id).getid())
                   ,t.tabl_prefix,t.tabl_descr
                , t.tabl_uc, t.tabl_dc, t.tabl_um, t.tabl_dm
                , t.getminzoomlevel(),t.getmaxzoomlevel(),t.getdevstatus()
                 ,[jsguid(Modelelemtype.COLU, c.colu_id) for c in t.getcolumns()]
                , udpv2js(pmodeid=t.tabl_id,pmodelemtype=Modelelemtype.TABL)
                    , [jsguid(Modelelemtype.ENTI, e.enti_id) for e in
                             TablEntiMap.getentilist(ptablid=t.tabl_id)]
              , Externalref.getsrcinfo(pmodeid=t.tabl_id)
               , reflist(plist=[jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=t.tabl_id)])
                    , [jsguid(Modelelemtype.ORGU, d[0]) for d in
                                         OragnisationalUnit.getreforgulist(pid=t.tabl_id)]
                ])
         for t in Table.select(porderby="tabl_id")
            }
    # fi
    return retval

def tables2sql(pmodel:JSModel):
    for jid,jelem in pmodel.getelements(pelemtype=Modelelemtype.TABL).items():
        tabl = Table()
        tabl.tabl_name = jelem['name']
        tabl.tabl_id = jsguid2id(jid)
        tabl.tabl_intf_id = jsguid2id(jelem['interface-id+'])
        tabl.tabl_prefix = jelem['prefix']
        tabl.tabl_descr = jelem['descr']
        tabl.tabl_uc = jelem['uc']
        tabl.tabl_dc = jelem['dc']
        tabl.tabl_um = jelem['um']
        tabl.tabl_dm = jelem['dm']
        minzoomlevel = jelem['minzoomlevel']
        maxzoomlevel = jelem['maxzoomlevel']
        devstatus = jelem['devstatus']
        try:
            tabl.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=tabl.tostring())
            continue

        Modelelement.upddisplelements(pmodeid=jsguid2id(jid), pminzl=minzoomlevel, pmaxzl=maxzoomlevel, pdevstat=devstatus)
        inssourceref(pmodel = pmodel,pmodeid=jsguid2id(jid), psources=jelem["sourceref"])
        instablemapping(pmodel=pmodel, ptablid=jsguid2id(jid), pentities=jelem['entitiesmapped'])
        updvs2sql(pmodel=pmodel,pmodeid=jsguid2id(jid), pudps=jelem["userdefprops"])
    return


def instablemapping(pmodel, ptablid=None,prelaid=None, pentities=None):
    for jentiid in pentities:
        tema = TablEntiMap()
        tema.tema_tabl_id = ptablid
        tema.tema_rela_id = prelaid
        tema.tema_enti_id = jsguid2id(jentiid)
        try:
            tema.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr="tablid={}, entiid={}".format(ptablid,jsguid2id(jentiid)))
            continue
    #for
    return

