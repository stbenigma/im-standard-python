from IM_OBJECTS import Key, Relation, Modelelemtype, Boolean, Arc,Externalref,Languagetext
from IM_JSON import *

def relaend2js(prelaend=None):
    model = ['enti'
            , 'arc'
            , 'assoc'
            , 'maptype'
            , 'hist'
            , 'mandatory'
            , 'cardstr+']
    if prelaend  is None:
        retval = fillmodel(pmodel=model,pentries=['','',multilangtext(),
                                                  '','','','']
                           )
    else:
        retval = fillmodel(pmodel=model, pentries=prelaend
                           )
    #fi
    return retval

def relation2js(prela):
    model = [ 'name', 'type'
        , 'from-to', 'to-from'
        , 'isinkeys+', 'sourceref'
        , 'uc', 'dc', 'um', 'dm'
        , 'minzoomlevel', 'maxzoomlevel', 'devstatus'
              ]
    if prela is None:
        retval = fillmodel(pmodel=model
                           , pentries=['', ''
                                    , relaend2js(), relaend2js()
                                       , reflist(), sourceref()
                                     , '', '', '', '',0,4,'DEV'
                                       ]
                           )
    else:
        keys = [k for k in Key.select(pwhere="""keys_id in (select kele_keys_id 
                                                    from key_elements 
                                                    where kele_rela_id = {})""".format(prela.rela_id))]
        retval = fillmodel(pmodel=model
                           , pentries=[prela.rela_name, prela.rela_type
                                       ,relaend2js(prelaend= [jsguid(Modelelemtype.ENTI, prela.rela_enti_id_from)
                                        ,None if prela.rela_arcs_id_from is None else jsguid(Modelelemtype.ARCS, prela.rela_arcs_id_from)
                                        ,multilangtext(prela.rela_assoc_from_to_l)
                                        ,prela.rela_maptype_from_to
                                        ,Boolean.str2bool(prela.rela_hist_from_to)
                                        ,Boolean.str2bool(prela.rela_mandatory_from_to)
                                        ,prela.to_cardstr()
                                         ])
                                       ,relaend2js(prelaend=[ jsguid(Modelelemtype.ENTI, prela.rela_enti_id_to)
                                          ,None if prela.rela_arcs_id_to is None else jsguid(Modelelemtype.ARCS, prela.rela_arcs_id_to)
                                          ,multilangtext(prela.rela_assoc_to_from_l)
                                          ,prela.rela_maptype_to_from
                                          ,Boolean.str2bool(prela.rela_hist_to_from)
                                          ,Boolean.str2bool(prela.rela_mandatory_to_from)
                                          ,prela.from_cardstr()
                                        ])
                                        ,reflist(plist=[jsguid(Modelelemtype.KEYS, k.keys_id) for k in keys])
                                      , sourceref(pvalues=Externalref.getsrcinfo(pmodeid=prela.rela_id))
                                       ,prela.rela_uc, prela.rela_dc, prela.rela_um, prela.rela_dm
                                    , prela.getminzoomlevel(), prela.getmaxzoomlevel(), prela.getdevstatus()

                                       ]
                           )
    # fi
    return retval


def relations2js(pemptymodel):
    if pemptymodel:
        relas = {jsguid(Modelelemtype.RELA, '0000') : relation2js(None)}
    else:
        relas = {jsguid(Modelelemtype.RELA, r.rela_id): relation2js(r) for r in Relation.select()}
    return relas



def relations2sql(pmodel: JSModel):
    for jid, jelem in pmodel.getelements(pelemtype=Modelelemtype.RELA).items():
        rela = Relation()
        rela.rela_id = jsguid2id(jid)
        rela.rela_name = jelem['name']
        rela.rela_type = jelem['type']
        rela.rela_enti_id_from = jsguid2id(jelem['from-to']['enti'])
        rela.rela_arcs_id_from = jsguid2id(jelem['from-to']['arc'])
        rela.rela_assoc_from_to = jelem['from-to']['assoc'][pmodel.modellanguage()]
        rela.rela_maptype_from_to = jelem['from-to']['maptype']
        rela.rela_mandatory_from_to = Boolean.bool2str(jelem['from-to']['mandatory'])
        rela.rela_hist_from_to = Boolean.bool2str(jelem['from-to']['hist'])
        rela.rela_enti_id_to = jsguid2id(jelem['to-from']['enti'])
        rela.rela_arcs_id_to = jsguid2id(jelem['to-from']['arc'])
        rela.rela_assoc_to_from = jelem['to-from']['assoc'][pmodel.modellanguage()]
        rela.rela_maptype_to_from = jelem['to-from']['maptype']
        rela.rela_mandatory_to_from = Boolean.bool2str(jelem['to-from']['mandatory'])
        rela.rela_hist_to_from = Boolean.bool2str(jelem['to-from']['hist'])
        rela.rela_uc = jelem['uc']
        rela.rela_dc = jelem['dc']
        rela.rela_um = jelem['um']
        rela.rela_dm = jelem['dm']
        minzoomlevel = jelem['minzoomlevel']
        maxzoomlevel = jelem['maxzoomlevel']
        devstatus = jelem['devstatus']
        try:
            relaid = rela.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=rela.tostring())
            continue
        Modelelement.upddisplelements(pmodeid=relaid, pminzl=minzoomlevel, pmaxzl=maxzoomlevel, pdevstat=devstatus)
        inslgtx(pmodel=pmodel,pmodeid=rela.rela_id,pattr=Languagetext.RELA_TEXT_TO,ptexts=jelem['to-from']['assoc'])
        inslgtx(pmodel=pmodel,pmodeid=rela.rela_id,pattr=Languagetext.RELA_TEXT_FROM,ptexts=jelem['from-to']['assoc'])
        inssourceref(pmodel=pmodel,pmodeid=relaid, psources=jelem["sourceref"])
    # for
    return

"""transfer references and subtypes"""
def relarefs2sql(pmodel):
    #for jid, jelem in pmodel.jsmodel['relations'].items():
        #updvs2sql(pmodel=pmodel,pburuid=jsguid2id(jid), pudps=jelem["userdefprops"])
    return


def arcs2js(pemptymodel):
    model = ['name', 'entity'
        , 'relations', 'sourceref'
        , 'uc', 'dc', 'um', 'dm'
             ]
    if pemptymodel:
        retval= {jsguid(Modelelemtype.ARCS, "0000") : fillmodel(pmodel=model,pentries=['','',reflist(),sourceref(),'','','',''])}
    else:
        retval = {jsguid(Modelelemtype.ARCS, a.arcs_id): fillmodel(pmodel=model
                                                               ,pentries=[a.arcs_name
                        , jsguid(Modelelemtype.ENTI, a.arcs_enti_id)
                        , [jsguid(Modelelemtype.RELA, r.rela_id) for r in a.getrelalist()]
                        , Externalref.getsrcinfo(pmodeid=a.arcs_id)
                        , a.arcs_uc
                        , a.arcs_dc
                        , a.arcs_um
                        , a.arcs_dm
                                ]
                                                               )
                for a in Arc.select()
                }
    # fi
    return retval


def arcs2sql(pmodel):
    for jid, jelem in pmodel.getelements(Modelelemtype.ARCS).items():
        arc = Arc()
        arc.arcs_id = jsguid2id(jid)
        arc.arcs_name = jelem['name']
        arc.arcs_enti_id = jsguid2id(jelem['entity'])
        arc.arcs_uc = jelem['uc']
        arc.arcs_dc = jelem['dc']
        arc.arcs_um = jelem['um']
        arc.arcs_dm = jelem['dm']
        try:
            arcid = arc.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=arc.tostring())
            continue
        inssourceref(pmodel = pmodel,pmodeid=arcid, psources=jelem["sourceref"])
    # for
    return

def arcsref2sql(pmodel):
    return
