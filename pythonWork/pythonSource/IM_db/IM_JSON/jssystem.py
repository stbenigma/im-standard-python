
from IM_JSON import *
from IM_OBJECTS import Interface,Modelelemtype,Table,OragnisationalUnit,Document,Externalref,Domain

def systems2js(pemptymodel):
    model = ['name','interface-id+'
             ,'descr'
            ,'uc', 'dc', 'um', 'dm'
            , 'sourceref','referencedby'
            ,'tables+' , 'domains+'
             ]
    if pemptymodel:
        retval = {jsguid(Modelelemtype.INTF, '0000') : fillmodel(pmodel=model, pentries=['', '', '', '', '', '', ''
                                                    ,sourceref(), reflist()
                                                , reflist(), reflist()
                                                    ])
                  }
    else:
        retval = {jsguid(Modelelemtype.INTF,i.intf_id) : fillmodel(pmodel=model,pentries=[i.intf_name,jsguid(Modelelemtype.INTF,i.intf_id)
                                                    ,i.intf_descr
                                                      ,i.intf_uc,i.intf_dc,i.intf_um,i.intf_dm
                                                     ,Externalref.getsrcinfo(pmodeid=i.intf_id)
                                                 ,[jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=i.intf_id)]\
                                                   +[jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=i.intf_id)]
                                         ,reflist(plist=[jsguid(Modelelemtype.TABL,t.tabl_id) for t in Table.selectbyschnid(pschnid=i.intf_id)])
                                         ,reflist(plist=[jsguid(Modelelemtype.DOMA, d.doma_id) for d in Domain.select(pwhere="doma_intf_id = {}".format(i.intf_id))])
                                        ]   )
                    for i in Interface.select()
                 }
    # fi
    return retval

def js2intf(pkey,pelem,psrcname=None,psrcid=None,pmodellang=None):
    intf = Interface(psrcname=psrcname,psrcid=psrcid)
    intf.intf_id = jsguid2id(pkey)
    intf.intf_name = pelem['name']
    intf.intf_descr = optionalvalue(pelem, 'descr')
    intf.intf_uc = pelem['uc']
    intf.intf_dc = pelem['dc']
    intf.intf_um = pelem['um']
    intf.intf_dm = pelem['dm']
    return intf


def systems2sql(presult:Mergeresult, podmjson: JSModel, pwithextsrcref):
    fromodm2db(presult=presult, podmjson=podmjson,  pelemtype=Modelelemtype.INTF, pjs2obj=js2intf,
                   pwithextsrcref=pwithextsrcref)
    # for jid,jelem in pmodel.getelements(Modelelemtype.INTF).items():
    #     js2intf(pkey=jid,pelem=jelem)
    #     try:
    #         intf.insert()
    #     except Exception as err:
    #         pmodel.markerror(pmsg=err, pelemstr=intf.tostring())
    #         continue
    #
    #     inssourceref(pmodel = pmodel,pmodeid=jsguid2id(jid), psources=jelem["sourceref"])
    # #for
    for jid,jelem in podmjson.getelements(Modelelemtype.INTF).items():
        insreferences(presult=presult, pmodeid=keytransl(jid), prefs=jelem['referencedby'])
    return
