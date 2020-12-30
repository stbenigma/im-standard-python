from IM_OBJECTS import Key, Relation, Modelelemtype, Boolean, Arc,Externalref,Languagetext
from IM_JSON import jsguid, jsguid2id, JSModel, inssourceref,inslgtx


def relation(prela):
    if prela is None: return {}
    keys = [k for k in Key.select(pwhere="""keys_id in (select kele_keys_id 
                                                from key_elements 
                                                where kele_rela_id = {})""".format(prela.rela_id))]
    return {
        'name': prela.rela_name
        , 'type': prela.rela_type
        , 'from-to': {
            'enti': jsguid(Modelelemtype.ENTI, prela.rela_enti_id_from)
            , 'arc': None if prela.rela_arcs_id_from is None else jsguid(Modelelemtype.ARCS, prela.rela_arcs_id_from)
            , 'assoc': prela.rela_assoc_from_to_L
            , 'maptype': prela.rela_maptype_from_to
            , 'hist': Boolean.str2bool(prela.rela_hist_from_to)
            , 'mandatory': Boolean.str2bool(prela.rela_mandatory_from_to)
            , 'cardstr+': prela.to_cardstr()
        }
        , 'to-from': {
            'enti': jsguid(Modelelemtype.ENTI, prela.rela_enti_id_to)
            , 'arc': None if prela.rela_arcs_id_to is None else jsguid(Modelelemtype.ARCS, prela.rela_arcs_id_to)
            , 'assoc': prela.rela_assoc_to_from_L
            , 'maptype': prela.rela_maptype_to_from
            , 'hist': Boolean.str2bool(prela.rela_hist_to_from)
            , 'mandatory': Boolean.str2bool(prela.rela_mandatory_to_from)
            , 'cardstr+': prela.from_cardstr()
        }
        , 'isinkeys+': [jsguid(Modelelemtype.KEYS, k.keys_id) for k in keys]
        , 'sourceref': Externalref.getsrcinfo(pmodeid=prela.rela_id)
        , 'uc': prela.rela_uc
        , 'dc': prela.rela_dc
        , 'um': prela.rela_um
        , 'dm': prela.rela_dm
    }


def relations2js():
    relas = {jsguid(Modelelemtype.RELA, r.rela_id): relation(r)
             for r in Relation.select()}
    return relas


def relations2sql(pmodel: JSModel):
    for jid, jelem in pmodel.jsmodel['relations'].items():
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
        try:
            relaid = rela.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=rela.tostring())
            continue
        inslgtx(pmodel=pmodel,pmodeid=rela.rela_id,pattr=Languagetext.RELA_TEXT_TO,ptexts=jelem['to-from']['assoc'])
        inslgtx(pmodel=pmodel,pmodeid=rela.rela_id,pattr=Languagetext.RELA_TEXT_FROM,ptexts=jelem['from-to']['assoc'])
        inssourceref(pmodel=pmodel,pmodeid=relaid, psources=jelem["sourceref"])
    # for
    return

"""transfer references and subtypes"""
def relarefs2sql(pmodel):
    #for jid, jelem in pmodel.jsmodel['relations'].items():
        #updvs2sql(pmodel=pmodel,pmodeid=jsguid2id(jid), pudps=jelem["userdefprops"])
    return


def arcs2js():
    arcs = {jsguid(Modelelemtype.ARCS, a.arcs_id): {
        'name': a.arcs_name
        , 'entity': jsguid(Modelelemtype.ENTI, a.arcs_enti_id)
        , 'relations': [jsguid(Modelelemtype.RELA, r.rela_id) for r in a.getrelalist()]
        , 'sourceref': Externalref.getsrcinfo(pmodeid=a.arcs_id)
        , 'uc': a.arcs_uc
        , 'dc': a.arcs_dc
        , 'um': a.arcs_um
        , 'dm': a.arcs_dm
        }
        for a in Arc.select()
    }
    return arcs


def arcs2sql(pmodel):
    for jid, jelem in pmodel.jsmodel['arcs'].items():
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
