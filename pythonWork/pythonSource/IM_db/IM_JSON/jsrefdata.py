
from IM_JSON import *
from IM_OBJECTS import Modelelemtype,PhysicalUnit,Document,Storageformat,Datatype,Domain,Externalref

def physicalunits2js(pemptymodel):
    model = ['name'
                                        ,'si-unit'
                                        ,'descr' 
                                        , 'uc'
                                        , 'dc'
                                        , 'um'
                                        , 'dm'
                                        ,'refindomains+']

    if pemptymodel:
        retval = {jsguid(Modelelemtype.PHYU,'0000'): fillmodel(pmodel=model, pentries=['' for i in range(len(model) - 1)] + [reflist()])}
    else:
        retval= {jsguid(Modelelemtype.PHYU,p.phyu_id) : fillmodel(pmodel=model,pentries=
                [p.phyu_name
                                        ,p.phyu_si_unit
                                        ,p.phyu_descr
                                        , p.phyu_uc, p.phyu_dc, p.phyu_um, p.phyu_dm
                                        ,reflist(plist= [jsguid(Modelelemtype.DOMA, d.doma_id)
                                                            for d in Domains.select(pwhere="doma_num_phyu_id ={}".format(p.phyu_id))])
                    ])
                for p in PhysicalUnit.select()
             }
    # fi
    return retval

def physicalunits2sql(pmodel:JSModel):
    for jid,jelem in pmodel.jsmodel['physicalunits'].items():
        phyu = PhysicalUnit()
        phyu.phyu_id = jsguid2id(jid)
        phyu.phyu_si_unit = jelem['si-unit']
        phyu.phyu_descr = jelem['descr']
        phyu.phyu_name = jelem['name']
        phyu.phyu_uc = jelem['uc']
        phyu.phyu_dc = jelem['dc']
        phyu.phyu_um = jelem['um']
        phyu.phyu_dm = jelem['dm']
        try:
            phyu.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=phyu.tostring())
            continue
    # for
    return

"""transfer references and subtypes"""
def phyurefs2sql(pmodel:JSModel):
    #    insudp(pburuid=entiid, pudps=jenti["userdefprop"])
    return

def storageformats2js(pemptymodel):
    model = ['name'
                                        ,'descr' 
                                        , 'uc'
                                        , 'dc'
                                        , 'um'
                                        , 'dm'
                                        ,'refindocuments+'
                                        , 'refindomains+']

    if pemptymodel:
        retval = {jsguid(Modelelemtype.STFO,'0000') : fillmodel(pmodel=model, pentries=['' for i in range(len(model) - 2)] + [reflist(),reflist()])}
    else:
        retval = {jsguid(Modelelemtype.STFO,s.stfo_id) : fillmodel(pmodel=model,pentries=
        [s.stfo_name, s.stfo_descr
                                        ,s.stfo_uc, s.stfo_dc, s.stfo_um, s.stfo_dm
                                        ,reflist(plist=[jsguid(Modelelemtype.DOCU, d.docu_id)
                                                            for d in Document.select(pwhere="docu_stfo_id ={}".format(s.stfo_id))])
                                        , reflist(plist= [jsguid(Modelelemtype.DOMA, d.doma_id)
                                                for d in Domain.select(pwhere="doma_bin_stfo_id ={}".format(s.stfo_id))])

        ])
                for s in Storageformat.select()
             }
    # fi
    return retval

def storageformats2sql(pmodel:JSModel):
    for jid,jelem in pmodel.jsmodel['storageformats'].items():
        stfo = Storageformat()
        stfo.stfo_id = jsguid2id(jid)
        stfo.stfo_name = jelem['name']
        stfo.stfo_descr = jelem['descr']
        stfo.stfo_uc = jelem['uc']
        stfo.stfo_dc = jelem['dc']
        stfo.stfo_um = jelem['um']
        stfo.stfo_dm = jelem['dm']
        try:
            stfo.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=stfo.tostring())
            continue
    #for
    return

"""transfer references and subtypes"""
def stforefs2sql(pmodel:JSModel):
    #    insudp(pburuid=entiid, pudps=jenti["userdefprop"])
    return


def datatypes2js(pemptymodel):
    model = ['name'
                                        ,'basetype' 
                                        , 'uc'
                                        , 'dc'
                                        , 'um'
                                        , 'dm'
                                        , 'sourceref']
    if pemptymodel:
        retval = {jsguid(Modelelemtype.DATY,'0000') : fillmodel(pmodel=model,pentries=['' for i in range(len(model)-1)]+[sourceref()])}
    else:
        retval = {jsguid(Modelelemtype.DATY,d.daty_id) : fillmodel(pmodel=model,pentries=
        [d.daty_name
                                        ,d.daty_basetype
                                        ,d.daty_uc, d.daty_dc, d.daty_um, d.daty_dm
                                        ,Externalref.getsrcinfo(pmodeid=d.daty_id)
        ])
                for d in Datatype.select()
             }
    # fi
    return retval

def datatypes2sql(pmodel:JSModel):
    for jid,jelem in pmodel.jsmodel['datatypes'].items():
        daty= Datatype(pname=jelem['name'],pbasetype=jelem['basetype'])
        daty.daty_id = jsguid2id(jid)
        daty.daty_uc = jelem['uc']
        daty.daty_dc = jelem['dc']
        daty.daty_um = jelem['um']
        daty.daty_dm = jelem['dm']
        try:
            daty.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=daty.tostring())
            continue        
        inssourceref(pmodel = pmodel,pmodeid=jsguid2id(jid), psources=jelem["sourceref"])
    #for
    return

"""transfer references and subtypes"""
def dtayrefs2sql(pmodel:JSModel):
    #    insudp(pburuid=entiid, pudps=jenti["userdefprop"])
    return


