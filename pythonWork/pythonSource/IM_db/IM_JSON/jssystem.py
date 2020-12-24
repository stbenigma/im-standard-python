
from IM_JSON import jsguid,inssourceref,jsguid2id,optionalvalue
from IM_OBJECTS import Interface,Modelelemtype,Table,OragnisationalUnit,Document,Externalref

def systems2js():
    intfs = {jsguid(Modelelemtype.INTF,i.intf_id) : {'name':i.intf_name
                                                    ,'interface-id':jsguid(Modelelemtype.INTF,i.intf_id)
                                                    ,'descr':i.intf_descr
                                                     ,'uc' : i.intf_uc
                                                    , 'dc': i.intf_dc
                                                    , 'um': i.intf_um
                                                    , 'dm': i.intf_dm
                                                    , 'sourceref': Externalref.getsrcinfo(pmodeid=i.intf_id)
                                                ,'refindocuments': [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=i.intf_id)]
                                        , 'refbyorgunits': [jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=i.intf_id)]
                                        ,'tables' : [jsguid(Modelelemtype.TABL,t.tabl_id) for t in Table.selectbyschnid(pschnid=i.intf_id)]
                                                    }
             for i in Interface.select()}
    return intfs

def systems2sql(pmodel):
    for jid,jelem in pmodel.jsmodel['systems'].items():
        intf = Interface()
        intf.intf_id = jsguid2id(jid)
        intf.intf_name = jelem['name']
        intf.intf_descr = optionalvalue(jelem,'descr')
        intf.intf_uc = jelem['uc']
        intf.intf_dc = jelem['dc']
        intf.intf_um = jelem['um']
        intf.intf_dm = jelem['dm']
        try:
            intf.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=intf.tostring())
            continue

        inssourceref(pmodel = pmodel,pmodeid=jsguid2id(jid), psources=jelem["sourceref"])
    #for
    return

"""transfer references and subtypes"""
def systrefs2sql(pmodel):
    #    insudp(pmodeid=entiid, pudps=jenti["userdefprop"])
    return
