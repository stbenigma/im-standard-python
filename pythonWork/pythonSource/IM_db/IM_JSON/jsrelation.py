from IM_JSON import jsguid, jsguid2id, JSModel, inssourceref
from IM_OBJECTS import Key, Relation, Modelelemtype, Boolean, Arc,Externalref


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
            , 'cardstr': prela.to_cardstr()
        }
        , 'to-from': {
            'enti': jsguid(Modelelemtype.ENTI, prela.rela_enti_id_to)
            , 'arc': None if prela.rela_arcs_id_to is None else jsguid(Modelelemtype.ARCS, prela.rela_arcs_id_to)
            , 'assoc': prela.rela_assoc_to_from_L
            , 'maptype': prela.rela_maptype_to_from
            , 'hist': Boolean.str2bool(prela.rela_hist_to_from)
            , 'mandatory': Boolean.str2bool(prela.rela_mandatory_to_from)
            , 'cardstr': prela.from_cardstr()
        }
        , 'isinkeys': [jsguid(Modelelemtype.KEYS, k.keys_id) for k in keys]
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
    """      "RELA11990": {
         "name": "Relation_76",
         "type": "M:1",
         "from-to": {
            "enti": "ENTI11889",
            "arc": null,
            "assoc": {
               "de": "ist",
               "en": "is",
               "fr": "est"
            },
            "maptype": "1",
            "hist": false,
            "mandatory": false,
            "cardstr": "1..N"
         },
         "to-from": {
            "enti": "ENTI11909",
            "arc": "ARCS12031",
            "assoc": {
               "de": "definiert",
               "en": "defines",
               "fr": "d\u00e9finit"
            },
            "maptype": "M",
            "hist": false,
            "mandatory": true,
            "cardstr": "0..1"
         },
         "isinkeys": [],
         "sourceref": {
            "ODM": "22F83753-485E-0A8B-38A2-6C89F1ACCD4E"
         },
         "uc": "stb",
         "dc": "2019-05-07 12:07:04 UTC",
         "um": null,
         "dm": null
      },"""
    for janker, jrela in pmodel.jsmodel['relations'].items():
        rela = Relation()
        rela.rela_id = jsguid2id(janker)
        rela.rela_name = jrela['name']
        rela.rela_type = jrela['type']
        rela.rela_enti_id_from = jsguid2id(jrela['from-to']['enti'])
        rela.rela_arcs_id_from = jsguid2id(jrela['from-to']['arc'])
        rela.rela_assoc_from_to = jrela['from-to']['assoc'][pmodel.modellanguage()]
        rela.rela_maptype_from_to = jrela['from-to']['maptype']
        rela.rela_mandatory_from_to = Boolean.bool2str(jrela['from-to']['mandatory'])
        rela.rela_hist_from_to = Boolean.bool2str(jrela['from-to']['hist'])
        rela.rela_enti_id_to = jsguid2id(jrela['to-from']['enti'])
        rela.rela_arcs_id_to = jsguid2id(jrela['to-from']['arc'])
        rela.rela_assoc_to_from = jrela['to-from']['assoc'][pmodel.modellanguage()]
        rela.rela_maptype_to_from = jrela['to-from']['maptype']
        rela.rela_mandatory_to_from = Boolean.bool2str(jrela['to-from']['mandatory'])
        rela.rela_hist_to_from = Boolean.bool2str(jrela['to-from']['hist'])
        rela.rela_uc = jrela['uc']
        rela.rela_dc = jrela['dc']
        rela.rela_um = jrela['um']
        rela.rela_dm = jrela['dm']
        try:
            relaid = rela.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=rela.tostring())
            continue
        inssourceref(pmodel=pmodel,pmodeid=relaid, psources=jrela["sourceref"])
    # for
    return


"""transfer references and subtypes"""


def relarefs2sql(pmodel):
    #    insudp(pmodeid=entiid, pudps=jenti["userdefprop"])
    return


"""      "ARCS12030": {
         "name": "Arc_7",
         "entity": "ENTI11926",
         "relations": [
            "RELA12010",
            "RELA12025",
            "RELA12026"
         ],
          "sourceref": {
            "ODM": "22F83753-485E-0A8B-38A2-6C89F1ACCD4E"
         },
        "uc": "stb",
         "dc": "2019-06-01 10:52:11 UTC",
         "um": null,
         "dm": null
      },"""


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
