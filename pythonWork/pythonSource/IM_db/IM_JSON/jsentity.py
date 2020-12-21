from IM_OBJECTS import *
from mystring import nvl
from IM_JSON import jsguid

""" builds a dictionary of all entities
    jsguid: {<entity>}
"""
def entities2js():
    entis = {jsguid(Modelelemtype.ENTI, e.enti_id):
                 {'name': e.enti_name_L
                     , 'shortname': nvl(e.enti_short_name)
                     , 'descr': e.enti_descr_L
                     , 'tooltip': e.enti_tooltip_L
                     , 'exptuple#': e.enti_exp_tuplecnt
                     , 'prefix': e.enti_prefix
                     , 'subtypellevel': e.getsubtypelevel()
                     , 'uc': e.enti_uc
                     , 'dc': e.enti_dc
                     , 'um': e.enti_um
                     , 'dm': e.enti_dm
                     , 'synonyms': [s.syno_name_L for s in e.getsynonyms()]
                     , 'sourceref': {s: Externalref.getsrcid(psrcname=s, pmodeid=e.enti_id) for s in
                                     Externalref.getsources()}
                     , 'supertypes': [jsguid(Modelelemtype.ENTI, es.enti_id) for es in e.getparents()]
                     , 'roles': [jsguid(Modelelemtype.ENTI, es.enti_id) for es in e.getchildren(ptype=Relation.ISAROLE)]
                     ,
                  'subtypes': [jsguid(Modelelemtype.ENTI, es.enti_id) for es in e.getchildren(ptype=Relation.ISASUBTYPE)]
                    , 'attributes': [jsguid(Modelelemtype.ATTR, a.attr_id) for a in e.getattributes()]
                     ,'relations': [jsguid(Modelelemtype.RELA, r.rela_id) for r in Relation.getbyentity(pentiid=e.enti_id)]
                     ,'keys': [jsguid(Modelelemtype.KEYS, k.keys_id) for k in Key.select(pwhere="keys_enti_id = {}".format(e.enti_id))]
                     ,'inarcs': [jsguid(Modelelemtype.ARCS, a.arcs_id) for a in Arc.select(pwhere="arcs_enti_id = {}".format(e.enti_id))]
                     ,'refindocuments': [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=e.enti_id)]
                     ,'refbyorgunits': [jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=e.enti_id)]
                     , 'userdefprop': {
                     t[0]: {g[1]: {u.udpr_name: Userdefpropvalue.udpvalue(pudprid=u.udpr_id, pmodeid=e.enti_id)
                                   for u in Userdefprop.getudps(ptheme=t[0], pgroup=g[1], pmeltname=Modelelemtype.ENTI)}
                            for g in Userdefprop.grouplist(pudptheme=t[0], pmelttype=Modelelemtype.ENTI)}
                     for t in Userdefprop.themelist(pmelttype=Modelelemtype.ENTI)}

                     , 'tablesmapped': {jsguid(Modelelemtype.INTF,s.getid()): [jsguid(Modelelemtype.TABL, t.tabl_id) for t in
                                                      TablEntiMap.gettabllist(pentiid=e.enti_id, pintfid=s.getid())]
                                        for s in Interface.getmapped(pentiid=e.enti_id)}
                     ,
                  'diagrams': [jsguid(Modelelemtype.DIAG, d.diag_id) for d in Diagram.getdiagrams(pmodeid=e.enti_id)]
                  } for e in Entity.select()}
    return entis
#entities2js

"""inserts all entities from json structure (like the one in entities2js to the sql database
  prints out all error and ends with exception if there was an error"""
def entities2sql(pmodel):
    """      "ENTI109": {
         "name": {
            "de": "Administrativgebiet",
            "en": "Administrative Territoryxx",
         },
         "shortname": "",
         "descr": {
            "de": "Gebietsunterteilung ",
            "en": "Gebietsunterteilung ",
         },
         "tooltip": {
            "de": null,
            "en": null,
         },
         "exptuple#": null,
         "prefix": null,
         "subtypellevel": 2,
         "uc": "stb",
         "dc": "2019-05-06 08:36:39 UTC",
         "um": null,
         "dm": null,
    ..
      },"""
    for anker, jenti in pmodel.jsmodel['entities'].items():
        enti = Entity()
        enti.enti_id = jsguid2id(anker)
        enti.enti_name = jenti['name'][pmodel.language()]
        enti.enti_short_name = jenti['name'][pmodel.language()]
        enti.enti_prefix = jenti['prefix']
        enti.enti_tooltip = jenti['tooltip'][pmodel.language()]
        enti.enti_descr = jenti['descr'][pmodel.language()]
        enti.enti_exp_tuplecnt = jenti['exptuple#']
        enti.enti_uc = jenti['uc']
        enti.enti_dc = jenti['dc']
        enti.enti_um = jenti['um']
        enti.enti_dm = jenti['dm']
        try:
            entiid = enti.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelem=[anker] + list(jenti))
            continue

        """      "ENTI109": {
         "name": {
            "de": "Administrativgebiet",
            "en": "Administrative Territoryxx",
         },
         "descr": {
            "de": "Gebietsunterteilung ",
            "en": "Gebietsunterteilung ",
         },
         "tooltip": {
            "de": null,
            "en": null,
         },
        """
        inslgtx(pmodel=pmodel,pmodeid=entiid, pattr=Languagetext.ENTI_NAME, ptexts=jenti['name'])
        inslgtx(pmodel=pmodel,pmodeid=entiid, pattr=Languagetext.ENTI_COMMENT, ptexts=jenti['descr'])
        inslgtx(pmodel=pmodel,pmodeid=entiid, pattr=Languagetext.ENTI_TOOLTIP, ptexts=jenti['tooltip'])
        inssourceref(pmodel=pmodel,pmodeid=entiid, psources=jenti["sourceref"])

        """      "ENTI109": {
         "synonyms":
            {
               "de": "Jemand",
               "en": "Contact person",
            },..
        """
        for jsyno in jenti["synonyms"]:
            syno = Synonym(pname=jsyno[pmodel.language()], pentiid=entiid)
            try:
                synoid = syno.insert()
            except Exception as err:
                model.markerror(pmsg=err, pelem=jsyno)
                continue
            inslgtx(pmodel = pmodel,pmodeid=synoid, pattr=Languagetext.SYNO_NAME, ptexts=jsyno)
        # for

    # for
# entities2sql

"""transfer references and subtypes"""
def entirefs2sql(pmodel):
    #    insudp(pmodeid=entiid, pudps=jenti["userdefprop"])

    """      "ENTI109": {
     "supertypes": [
        "ENTI185"
     ],
     "roles": [],
     "subtypes": [],
     "attributes": [
        "ATTR110"
     ],
     "relations": [
        "RELA263"
     ],
     "keys": [],
     "inarcs": [],
     "refindocuments": [],
     "refbyorgunits": [],
     "tablesmapped": {
        "INTF283": [
           "TABL582"
        ],
     },
     "diagrams": [
        "DIAG281",
        "DIAG282"
     ]
  },"""
