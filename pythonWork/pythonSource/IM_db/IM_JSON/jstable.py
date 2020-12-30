from IM_OBJECTS import Table,Modelelemtype,Document,Interface,TablEntiMap,Externalref,OragnisationalUnit
from IM_JSON import jsguid,jsguid2id,inssourceref,udpv2js,JSModel,updvs2sql

def tables2js():
    tabs = {jsguid(Modelelemtype.TABL,t.tabl_id) :
                {'name':t.tabl_name
                   ,'interface-name+':Interface().getbyid(t.tabl_intf_id).getname()
                   ,'interface-id+':jsguid(Modelelemtype.INTF, Interface().getbyid(t.tabl_intf_id).getid())
                   ,'prefix':t.tabl_prefix
                   ,'descr':t.tabl_descr
                , 'uc': t.tabl_uc
                , 'dc': t.tabl_dc
                , 'um': t.tabl_um
                , 'dm': t.tabl_dm
                 ,'columns+':[jsguid(Modelelemtype.COLU, c.colu_id) for c in t.getcolumns()]
                , 'userdefprops': udpv2js(pmodeid=t.tabl_id,pmodelemtype=Modelelemtype.TABL)
                    ,'entitiesmapped': [jsguid(Modelelemtype.ENTI, e.enti_id) for e in
                             TablEntiMap.getentilist(ptablid=t.tabl_id)]
              , 'sourceref': Externalref.getsrcinfo(pmodeid=t.tabl_id)
               , 'refindocuments+': [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=t.tabl_id)]
                    , 'refbyorgunits+': [jsguid(Modelelemtype.ORGU, d[0]) for d in
                                         OragnisationalUnit.getreforgulist(pid=t.tabl_id)]
                 } for t in Table.select()
            }
    return tabs

def tables2sql(pmodel:JSModel):
    for jid,jelem in pmodel.jsmodel['tables'].items():
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
        try:
            tabl.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=tabl.tostring())
            continue

        inssourceref(pmodel = pmodel,pmodeid=jsguid2id(jid), psources=jelem["sourceref"])
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

"""transfer references and subtypes"""
def tablrefs2sql(pmodel:JSModel):
    for jid,jelem in pmodel.jsmodel['tables'].items():
        instablemapping(pmodel=pmodel, ptablid=jsguid2id(jid), pentities=jelem['entitiesmapped'])
        updvs2sql(pmodel=pmodel,pmodeid=jsguid2id(jid), pudps=jelem["userdefprops"])
    return
