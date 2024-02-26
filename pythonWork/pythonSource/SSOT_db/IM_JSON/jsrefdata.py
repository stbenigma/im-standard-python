
from SSOT_db.IM_JSON import  *
from SSOT_db.IM_OBJECTS import  Modelelemtype,PhysicalUnit,Document,Storageformat,Datatype,Domain,Externalref

def physicalunits2js(pemptymodel):
    model = ['name'
            ,'si-unit'
            ,'descr'
            , 'uc'
            , 'dc'
            , 'um'
            , 'dm'
            ,'usedindomains+']

    if pemptymodel:
        retval = {jsguid(Modelelemtype.PHYU,'0000'): fillmodel(pmodel=model, pentries=['' for i in range(len(model) - 1)] + [reflist()])}
    else:
        retval= {jsguid(Modelelemtype.PHYU,p.phyu_id) : fillmodel(pmodel=model,pentries=
                [p.phyu_name
                                        ,p.phyu_si_unit
                                        ,p.phyu_descr
                                        , p.phyu_uc, p.phyu_dc, p.phyu_um, p.phyu_dm
                                        ,reflist(plist= [jsguid(Modelelemtype.DOMA, d.doma_id)
                                                            for d in Domain.select(pwhere=("doma_num_phyu_id = ?", p.phyu_id))])
                    ])
                for p in PhysicalUnit.select()
             }
    # fi
    return retval

def js2phyu(pkey,pelem,psrcname=None,psrcid=None,pmodellang=None):
    phyu:PhysicalUnit = PhysicalUnit()
    phyu.phyu_id = pkey
    phyu.phyu_si_unit = pelem['si-unit']
    phyu.phyu_descr = pelem['descr']
    phyu.phyu_name = pelem['name']
    phyu.phyu_uc = pelem['uc']
    phyu.phyu_dc = pelem['dc']
    phyu.phyu_um = pelem['um']
    phyu.phyu_dm = pelem['dm']
    return phyu


def physicalunits2sql(presult, pjson:JSModel,pwithextsrcref):
    fromjson2db(presult=presult,pjson=pjson,pelemtype=Modelelemtype.PHYU,pjs2obj=js2phyu,pwithextsrcref=pwithextsrcref)
    # for jid,jelem in pmodel.mirojsmodel['physicalunits'].items():
    #     phyu = js2phyu(pkey=jid,pelem=jelem)
    #     try:
    #         phyu.insert()
    #     except Exception as err:
    #         pmodel.markerror(pmsg=err, pelemstr=phyu.tostring())
    #         continue
    # # for
    return

def storageformats2js(pemptymodel):
    model = ['name'
            ,'descr'
            , 'uc'
            , 'dc'
            , 'um'
            , 'dm'
            ,'usedindocuments+'
            ,'usedindomains+']

    if pemptymodel:
        retval = {jsguid(Modelelemtype.STFO,'0000') : fillmodel(pmodel=model, pentries=['','','','','','', reflist(),reflist()])}
    else:
        retval = {jsguid(Modelelemtype.STFO,s.stfo_id) : fillmodel(pmodel=model,pentries=
        [s.stfo_name, s.stfo_descr
                                        ,s.stfo_uc, s.stfo_dc, s.stfo_um, s.stfo_dm
                                        ,[jsguid(Modelelemtype.DOCU, d.docu_id)
                                                            for d in Document.select(pwhere=("docu_stfo_id = ?", s.stfo_id))]
                                         ,[jsguid(Modelelemtype.DOMA, d.doma_id)
                                                for d in Domain.select(pwhere=("doma_bin_stfo_id = ?", s.stfo_id))]

        ])
                for s in Storageformat.select()
             }
    # fi
    return retval

def js2stfo(pkey,pelem,psrcname=None,psrcid=None,pmodellang=None):
    stfo:Storageformat = Storageformat()
    stfo.stfo_id = pkey
    stfo.stfo_name = pelem['name']
    stfo.stfo_descr = pelem['descr']
    stfo.stfo_uc = pelem['uc']
    stfo.stfo_dc = pelem['dc']
    stfo.stfo_um = pelem['um']
    stfo.stfo_dm = pelem['dm']
    return stfo

def storageformats2sql(presult, pjson: JSModel, pwithextsrcref):
    fromjson2db(presult=presult, pjson=pjson,  pelemtype=Modelelemtype.STFO, pjs2obj=js2stfo,
                   pwithextsrcref=pwithextsrcref)

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

def js2daty(pkey,pelem,psrcname=None,psrcid=None,pmodellang=None):
    daty = Datatype(pname=pelem['name'],pbasetype=pelem['basetype'],psrcname=psrcname,pscrid=psrcid)
    daty.daty_id = pkey
    daty.daty_uc = pelem['uc']
    daty.daty_dc = pelem['dc']
    daty.daty_um = pelem['um']
    daty.daty_dm = pelem['dm']
    return daty


def datatypes2sql(presult, pjson:JSModel,pwithextsrcref):
    fromjson2db(presult=presult,pjson=pjson,pelemtype=Modelelemtype.DATY,pjs2obj=js2daty,pwithextsrcref=pwithextsrcref)

    return


