from IM_OBJECTS import Key,Relation,Modelelemtype,Boolean,Arc
from IM_JSON import jsguid

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
                    ,'cardstr': prela.to_cardstr()
                }
                , 'to-from':{
                    'enti': jsguid(Modelelemtype.ENTI, prela.rela_enti_id_to)
                    , 'arc': None if prela.rela_arcs_id_to is None else jsguid(Modelelemtype.ARCS, prela.rela_arcs_id_to)
                    , 'assoc': prela.rela_assoc_to_from_L
                    , 'maptype': prela.rela_maptype_to_from
                    , 'hist': Boolean.str2bool(prela.rela_hist_to_from)
                    , 'mandatory': Boolean.str2bool(prela.rela_mandatory_to_from)
                  , 'cardstr': prela.from_cardstr()
                }
                ,'isinkeys': [jsguid(Modelelemtype.KEYS,k.keys_id) for k in keys]
                ,'uc': prela.rela_uc
                ,'dc': prela.rela_dc
                ,'um': prela.rela_um
                ,'dm': prela.rela_dm
    }

def relations2js():
    relas = {jsguid(Modelelemtype.RELA, r.rela_id): relation(r)
             for r in Relation.select()}
    return relas


def arcs2js():
    arcs = {jsguid(Modelelemtype.ARCS,a.arcs_id): {
        'name':a.arcs_name
        ,'entity': jsguid(Modelelemtype.ENTI,a.arcs_enti_id)
        ,'relations': [jsguid(Modelelemtype.RELA,r.rela_id) for r in a.getrelalist()]
        ,'uc': a.arcs_uc
        ,'dc': a.arcs_dc
        ,'um': a.arcs_um
        ,'dm': a.arcs_dm
        }
            for a in Arc.select()
            }
    return arcs

