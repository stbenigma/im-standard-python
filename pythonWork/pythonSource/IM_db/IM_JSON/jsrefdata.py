
from IM_JSON import jsguid,inssourceref,jsguid2id,JSModel
from IM_OBJECTS import Modelelemtype,PhysicalUnit,Document,Storageformat,Datatype,Domain,Externalref

def physicalunits2js():
    phyus = {jsguid('PHYU',p.phyu_id) : {'name':p.phyu_name
                                        ,'si-unit': p.phyu_si_unit
                                        ,'descr' : p.phyu_descr
                                        , 'uc': p.phyu_uc
                                        , 'dc': p.phyu_dc
                                        , 'um': p.phyu_um
                                        , 'dm': p.phyu_dm
                                        ,'refindomains': [jsguid(Modelelemtype.DOMA, d.doma_id)
                                                            for d in Domains.select(pwhere="doma_num_phyu_id ={}".format(p.phyu_id))]
                                         }
                for p in PhysicalUnit.select()
             }
    return phyus

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
    #    insudp(pmodeid=entiid, pudps=jenti["userdefprop"])
    return

def storageformats2js():
    stfos = {jsguid('STFO',s.stfo_id) : {'name':s.stfo_name
                                        ,'descr' : s.stfo_descr
                                        , 'uc': s.stfo_uc
                                        , 'dc': s.stfo_dc
                                        , 'um': s.stfo_um
                                        , 'dm': s.stfo_dm
                                        ,'refindocuments': [jsguid(Modelelemtype.DOCU, d.docu_id)
                                                            for d in Document.select(pwhere="docu_stfo_id ={}".format(s.stfo_id))]
                                        , 'refindomains': [jsguid(Modelelemtype.DOMA, d.doma_id)
                                                for d in Domain.select(pwhere="doma_bin_stfo_id ={}".format(s.stfo_id))]
                                         }
                for s in Storageformat.select()
             }
    return stfos

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
    #    insudp(pmodeid=entiid, pudps=jenti["userdefprop"])
    return


def datatypes2js():
    datys = {jsguid(Modelelemtype.DATY,d.daty_id) : {'name':d.daty_name
                                        ,'basetype' : d.daty_basetype
                                        , 'uc': d.daty_uc
                                        , 'dc': d.daty_dc
                                        , 'um': d.daty_um
                                        , 'dm': d.daty_dm
                                        , 'sourceref' : Externalref.getsrcinfo(pmodeid=d.daty_id)
                                         }
                for d in Datatype.select()
             }
    return datys

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
    #    insudp(pmodeid=entiid, pudps=jenti["userdefprop"])
    return


