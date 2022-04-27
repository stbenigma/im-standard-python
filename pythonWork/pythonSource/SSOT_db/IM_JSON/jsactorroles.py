from SSOT_db.IM_JSON import  *
from SSOT_db.IM_OBJECTS import  *

def actorconcerns2js(pactcs=None):
    if pactcs is None:
        retval = {'xxxx0000': 'RACI'}
    else:
        retval = dict()
        for actc in pactcs:
            mode = Modelelement().getbyid(actc.actc_mode_id)
            retval[jsguid(mode.mode_type, mode.mode_id)] = actc.getraci()
    return retval

def js2actc(pactrid,pmodeid,praci):
    actc = Actorconcern(actc_mode_id=pmodeid,actc_actr_id = pactrid,
                        actc_responsible=Boolean.bool2str('R' in praci),
                        actc_accountable=Boolean.bool2str('A' in praci),
                        actc_consulted=Boolean.bool2str('C' in praci),
                        actc_informed=Boolean.bool2str('I' in praci)
                        )
    return actc

def actorconcerns2sql(presult, podmjson):
    """actor concerns are emptied and loaded from source"""
    inscnt,delcnt = 0,0
    newactrs = podmjson.getelements(Modelelemtype.ACTR)
    for actrjsid,actr in newactrs.items():
        delcnt += Actorconcern.delete(pwhere=("actc_actr_id = ?", jsguid2id(actrjsid)))
        """  "concerns": {
            "ENTI93": "I",
            "ATTR94": "I"},
            """
        for modejsid,raci in actr["concerns"].items():
            try:
                actc = js2actc(pactrid=jsmergetosql.keytransl(actrjsid),
                               pmodeid = jsmergetosql.keytransl(modejsid),
                               praci=raci)
                actc.insert()
                inscnt += 1
            except Exception as err:
                presult.markdberror(perr=err, pelem=actr)
        # for
    # for
    presult.addinscnt(max(0, (inscnt - delcnt)))
    presult.adddelcnt(max(0, (delcnt - inscnt)))

    return


def actorrole2js(pactr):
    model = ['name', 'descr'
        , 'uc', 'um', 'dc', 'dm'
        ,'concerns','sourceref'
        ]
    if pactr is None:
        retval = fillmodel(pmodel=model
                           ,pentries=['',''
                                     , '','','','',
                                      actorconcerns2js(),
                                      sourceref()
                                    ]
                           )
    else:
        retval = fillmodel(pmodel=model
                   ,pentries=[pactr.actr_name,pactr.actr_descr
                             ,pactr.actr_uc,pactr.actr_um,pactr.actr_dc,pactr.actr_dm,
                              actorconcerns2js(pactr.getchildren()),
                              Externalref.getsrcinfo(pmodeid=pactr.actr_id),
                              ]
                    )
    # fi
    return retval

def actorroles2js(pemptymodel):
    if pemptymodel:
        actrs = {jsguid(Modelelemtype.ACTR, '0000'):actorrole2js(None)}
    else:
        actrs = {jsguid(Modelelemtype.ACTR, a.actr_id):actorrole2js(a)
                 for a in Actorrole.select()}
    return actrs

def js2actr(pkey,pelem,psrcname=None,psrcid=None,pmodellang=None):
    actr = Actorrole(srcname=psrcname,srcid=psrcid,
                     actr_id = jsguid2id(pkey),
                     actr_uc = pelem['uc'],
                     actr_dc = pelem['dc'],
                     actr_um = pelem['um'],
                     actr_dm = pelem['dm'],
                     actr_name = pelem['name'],
                     actr_descr = pelem['descr'])
    return actr

def actorroles2sql(presult:Mergeresult, podmjson: JSModel, pwithextsrcref):
    fromodm2db(presult=presult, podmjson=podmjson,  pelemtype=Modelelemtype.ACTR, pjs2obj=js2actr,
                   pwithextsrcref=pwithextsrcref)

    for jid,jelem in podmjson.getelements(pelemtype=Modelelemtype.ACTR).items():
        dbactrid = jsmergetosql.keytransl(jid)

        #insactorcons(presult=presult,pactrid=dbactrid,pcons=jelem["concerns"])
        inssourceref(presult=presult,pmodeid=dbactrid, psources=jelem["sourceref"])
    return

