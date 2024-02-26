from SSOT_db.IM_JSON import *
from SSOT_db.IM_OBJECTS import Datamodel, Modelelemtype, Table, OragnisationalUnit, Document, Externalref, Domain

DATAMODELMODEL = ['name', 'datamodel-id+'
    , 'descr'
    , 'uc', 'dc', 'um', 'dm'
    , 'sourceref', 'referencedby'
    , 'tables+', 'domains+'
                  ]


def jsondatamodel(name, uc, dc, tables=[], domains=[], **kwargs):
    datamodel = dict()
    initjselement(datamodel, DATAMODELMODEL)
    datamodel["name"] = name
    datamodel["uc"] = uc
    datamodel["dc"] = dc
    datamodel["dc"] = dc
    datamodel["referencedby"] = []
    datamodel["tables+"] = tables
    datamodel["domains+"] = domains

    fillargs(model=datamodel, refmodel=DATAMODELMODEL, **kwargs)
    return datamodel


def datamodels2js(pemptymodel):
    if pemptymodel:
        retval = {
            jsguid(Modelelemtype.DATM, '0000'): fillmodel(pmodel=DATAMODELMODEL, pentries=['', '', '', '', '', '', ''
                , sourceref(), reflist()
                , reflist(), reflist()
                                                                                           ])
            }
    else:
        retval = {jsguid(Modelelemtype.DATM, i.datm_id): fillmodel(pmodel=DATAMODELMODEL,
                                                                   pentries=[i.datm_name,
                                                                             jsguid(Modelelemtype.DATM, i.datm_id)
                                                                       , i.datm_descr
                                                                       , i.datm_uc, i.datm_dc, i.datm_um, i.datm_dm
                                                                       , Externalref.getsrcinfo(pmodeid=i.datm_id)
                                                                       , [jsguid(Modelelemtype.DOCU, d[0]) for d in
                                                                          Document.getrefdoculist(pid=i.datm_id)] \
                                                                             + [jsguid(Modelelemtype.ORGU, d[0]) for d
                                                                                in OragnisationalUnit.getreforgulist(
                                                                               pid=i.datm_id)]
                                                                       , reflist(
                                                                           plist=[jsguid(Modelelemtype.TABL, t.tabl_id)
                                                                                  for t in Table.selectbyschnid(
                                                                                   pschnid=i.datm_id)])
                                                                       , reflist(
                                                                           plist=[jsguid(Modelelemtype.DOMA, d.doma_id)
                                                                                  for d in Domain.select(pwhere=(
                                                                               "doma_datm_id = ?", i.datm_id))])
                                                                             ])
                  for i in Datamodel.select()
                  }
    # fi
    return retval


def js2datm(pkey, pelem, psrcname=None, psrcid=None, pmodellang=None):
    datm = Datamodel(psrcname=psrcname, psrcid=psrcid)
    datm.datm_id = pkey
    datm.datm_name = pelem['name']
    datm.datm_descr = optionalvalue(pelem, 'descr')
    datm.datm_uc = pelem['uc']
    datm.datm_dc = pelem['dc']
    datm.datm_um = pelem['um']
    datm.datm_dm = pelem['dm']
    return datm


def datamodels2sql(presult: Mergeresult, pjson: JSModel, pwithextsrcref):
    fromjson2db(presult=presult, pjson=pjson, pelemtype=Modelelemtype.DATM, pjs2obj=js2datm,
                pwithextsrcref=pwithextsrcref)
    # for jid,jelem in pmodel.getelements(pelemtype=Modelelemtype.DATM).items():
    #     js2datm(pkey=jid,pelem=jelem)
    #     try:
    #         datm.insert()
    #     except Exception as err:
    #         pmodel.markerror(pmsg=err, pelemstr=datm.tostring())
    #         continue
    #
    #     inssourceref(pmodel = pmodel,pmodeid=jsguid2id(jid), psources=jelem["sourceref"])
    # #for
    for jid, jelem in pjson.getelements(pelemtype=Modelelemtype.DATM).items():
        insreferences(presult=presult, pmodeid=presult.keytransl(jid), prefs=jelem['referencedby'])
    return
