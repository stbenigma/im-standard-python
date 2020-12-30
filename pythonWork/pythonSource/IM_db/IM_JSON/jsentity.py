from IM_OBJECTS import *
from mystring import nvl
from IM_JSON import jsguid,jsguid2id,inslgtx,inssourceref,JSModel,updvs2sql,udpv2js

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
                     , 'subtypellevel+': e.getsubtypelevel()
                     , 'uc': e.enti_uc
                     , 'dc': e.enti_dc
                     , 'um': e.enti_um
                     , 'dm': e.enti_dm
                     , 'synonyms': {jsguid(Modelelemtype.SYNO,s.syno_id): s.syno_name_L for s in e.getsynonyms()}
                     , 'sourceref': Externalref.getsrcinfo(pmodeid=e.enti_id)
                     , 'supertypes+': [jsguid(Modelelemtype.ENTI, es.enti_id) for es in e.getparents()]
                     , 'roles+': [jsguid(Modelelemtype.ENTI, es.enti_id) for es in e.getchildren(ptype=Relation.ISAROLE)]
                     ,'subtypes+': [jsguid(Modelelemtype.ENTI, es.enti_id) for es in e.getchildren(ptype=Relation.ISASUBTYPE)]
                    , 'attributes+': [jsguid(Modelelemtype.ATTR, a.attr_id) for a in e.getattributes()]
                     ,'relations+': [jsguid(Modelelemtype.RELA, r.rela_id) for r in Relation.getbyentity(pentiid=e.enti_id)]
                     ,'keys+': [jsguid(Modelelemtype.KEYS, k.keys_id) for k in Key.select(pwhere="keys_enti_id = {}".format(e.enti_id))]
                     ,'inarcs+': [jsguid(Modelelemtype.ARCS, a.arcs_id) for a in Arc.select(pwhere="arcs_enti_id = {}".format(e.enti_id))]
                     ,'refindocuments+': [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=e.enti_id)]
                     ,'refbyorgunits+': [jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=e.enti_id)]
                     , 'userdefprops': udpv2js(pmodeid=e.enti_id,pmodelemtype=Modelelemtype.ENTI)
                     , 'tablesmapped+': {jsguid(Modelelemtype.INTF,s.getid()): [jsguid(Modelelemtype.TABL, t.tabl_id) for t in
                                                      TablEntiMap.gettabllist(pentiid=e.enti_id, pintfid=s.getid())]
                                        for s in Interface.getmapped(pentiid=e.enti_id)}
                     ,
                  'diagrams+': [jsguid(Modelelemtype.DIAG, d.diag_id) for d in Diagram.getdiagrams(pmodeid=e.enti_id)]
                  } for e in Entity.select()}
    return entis
#entities2js

"""inserts all entities from json structure (like the one in entities2js to the sql database
  prints out all error and ends with exception if there was an error"""
def entities2sql(pmodel:JSModel):
    for jid, jelem in pmodel.jsmodel['entities'].items():
        enti = Entity()
        enti.enti_id = jsguid2id(jid)
        enti.enti_name = jelem['name'][pmodel.modellanguage()]
        enti.enti_short_name = jelem['shortname']
        enti.enti_prefix = jelem['prefix']
        enti.enti_tooltip = jelem['tooltip'][pmodel.modellanguage()]
        enti.enti_descr = jelem['descr'][pmodel.modellanguage()]
        enti.enti_exp_tuplecnt = jelem['exptuple#']
        enti.enti_uc = jelem['uc']
        enti.enti_dc = jelem['dc']
        enti.enti_um = jelem['um']
        enti.enti_dm = jelem['dm']
        try:
            entiid = enti.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=[jid] + list(jelem))
            continue

        inslgtx(pmodel=pmodel,pmodeid=entiid, pattr=Languagetext.ENTI_NAME, ptexts=jelem['name'])
        inslgtx(pmodel=pmodel,pmodeid=entiid, pattr=Languagetext.ENTI_COMMENT, ptexts=jelem['descr'])
        inslgtx(pmodel=pmodel,pmodeid=entiid, pattr=Languagetext.ENTI_TOOLTIP, ptexts=jelem['tooltip'])
        inssourceref(pmodel=pmodel,pmodeid=entiid, psources=jelem["sourceref"])
        updvs2sql(pmodel=pmodel, pmodeid=jsguid2id(jid), pudps=jelem["userdefprops"])

        """      "ENTI109": {
         "synonyms":
            {
               "de": "Jemand",
               "en": "Contact person",
            },..
        """
        for synoid,jsyno in jelem["synonyms"].items():
            syno = Synonym(pname=jsyno[pmodel.modellanguage()], pentiid=entiid)
            syno.syno_id = jsguid2id(synoid)
            try:
                syno.insert()
            except Exception as err:
                pmodel.markerror(pmsg=err, pelemstr=jsyno)
                continue
            inslgtx(pmodel = pmodel,pmodeid=syno.syno_id, pattr=Languagetext.SYNO_NAME, ptexts=jsyno)
        # for

    # for
# entities2sql

"""transfer references and subtypes"""
def entirefs2sql(pmodel:JSModel):
    return
