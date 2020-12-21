
from IM_JSON import jsguid
from IM_OBJECTS import Interface,Modelelemtype,Table,OragnisationalUnit,Document,Externalref

def systems2js():
    intfs = {jsguid(Modelelemtype.INTF,i.intf_id) : {'name':i.intf_name
                                                    ,'interface-id':jsguid(Modelelemtype.INTF,i.intf_id)
                                                    ,'descr':i.intf_descr
                                                , 'sourceref': {s: Externalref.getsrcid(psrcname=s, pmodeid=i.intf_id)
                                                            for s in Externalref.getsources()}
                                                ,'refindocuments': [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=i.intf_id)]
                                        , 'refbyorgunits': [jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=i.intf_id)]
                                        ,'tables' : [jsguid(Modelelemtype.TABL,t.tabl_id) for t in Table.selectbyschnid(pschnid=i.intf_id)]
                                                    }
             for i in Interface.select()}
    return intfs
