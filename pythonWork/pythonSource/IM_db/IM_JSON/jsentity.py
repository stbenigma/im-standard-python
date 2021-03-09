from IM_JSON import *
from IM_OBJECTS import *
from mystring import nvl

""" builds a dictionary of all entities
    jsguid: {<entity>}
"""

def synonyms (psynos:dict=None):
    """ None = emptymodel"""
    """    {
            "SYNO1112": {
               "de": "Jemand",
               "en": "Contact person",
               "fr": "**Personne de contact"
            },
    """
    if psynos is None:
        return {"SYNO000": multilangtext(None)}
    else:
        return {s:multilangtext(v) for s,v in psynos.items()}

def entities2js(pemptymodel):
    model = ['name', 'shortname'
        , 'descr', 'tooltip'
        , 'exptuple#', 'prefix'
        , 'subtypellevel+'
        , 'uc', 'dc', 'um', 'dm'
        , 'minzoomlevel', 'maxzoomlevel', 'devstatus'
        , 'synonyms', 'sourceref'
        , 'supertypes+','roles+'
        , 'subtypes+', 'attributes+'
        , 'relations+', 'keys+'
        , 'inarcs+', 'refindocuments+'
        ,'refbyorgunits+', 'userdefprops'
        , 'tablesmapped+', 'diagrams+'
        ]
    if pemptymodel:
        entis = {jsguid(Modelelemtype.ENTI, '0000'): fillmodel(pmodel=model,
                                       pentries=[multilangtext(None), ''
                                       ,multilangtext(None),multilangtext(None)
                                       ,'',''
                                       ,''
                                       ,'','','',''
                                        ,0,4,'DEV'
                                       ,synonyms(None),sourceref(None)
                                       ,reflist(None),reflist(None)
                                       ,reflist(None),reflist(None)
                                       , reflist(None),reflist(None)
                                       , reflist(None),reflist(None)
                                       , reflist(None), userdefprops(None)
                                        , tabreflist(None),reflist(None)
                                            ]
                                       )
                }
    else:
        entis = {jsguid(Modelelemtype.ENTI, e.enti_id):
                     fillmodel(pmodel=model,
                            pentries=[multilangtext(ptext=e.enti_name_L), nvl(e.enti_short_name)
                    , multilangtext(e.enti_descr_L),multilangtext(e.enti_tooltip_L)
                    , e.enti_exp_tuplecnt,e.enti_prefix
                    , e.getsubtypelevel()
                    , e.enti_uc, e.enti_dc, e.enti_um,e.enti_dm
                    , e.getminzoomlevel(),e.getmaxzoomlevel(),e.getdevstatus()
                    , synonyms(psynos={jsguid(Modelelemtype.SYNO, s.syno_id): s.syno_name_L for s in e.getsynonyms()})
                         ,sourceref(pvalues=Externalref.getsrcinfo(pmodeid=e.enti_id))
                    ,  reflist(plist=[jsguid(Modelelemtype.ENTI, es.enti_id) for es in e.getparents()])
                         ,reflist(plist=[jsguid(Modelelemtype.ENTI, es.enti_id) for es in e.getchildren(ptype=Relation.ISAROLE)])
                    , reflist(plist=[jsguid(Modelelemtype.ENTI, es.enti_id) for es in e.getchildren(ptype=Relation.ISASUBTYPE)])
                         , reflist(plist=[jsguid(Modelelemtype.ATTR, a.attr_id) for a in e.getattributes()])
                    , reflist(plist=[jsguid(Modelelemtype.RELA, r.rela_id) for r in Relation.getbyentity(pentiid=e.enti_id)])
                         , reflist(plist=[jsguid(Modelelemtype.KEYS, k.keys_id) for k in Key.select(pwhere="keys_enti_id = {}".format(e.enti_id))])
                    , reflist(plist=[jsguid(Modelelemtype.ARCS, a.arcs_id) for a in Arc.select(pwhere="arcs_enti_id = {}".format(e.enti_id))])
                         , reflist(plist=[jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=e.enti_id)])
                    , reflist(plist=[jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=e.enti_id)])
                         , userdefprops(pprops=udpv2js(pmodeid=e.enti_id, pmodelemtype=Modelelemtype.ENTI))
                    , tabreflist(plist={
                                jsguid(Modelelemtype.INTF, s.getid()): [jsguid(Modelelemtype.TABL, t.tabl_id) for t in
                                                                 TablEntiMap.gettabllist(pentiid=e.enti_id,
                                                                                         pintfid=s.getid())]
                                for s in Interface.getmapped(pentiid=e.enti_id)})
                        ,reflist(plist=[jsguid(Modelelemtype.DIAG, d.diag_id) for d in Diagram.getdiagrams(pmodeid=e.enti_id)])
                            ]
                        ) for e in Entity.select()
                 }

    return entis
# entities2js

"""inserts all entities from json structure (like the one in entities2js to the sql database
  prints out all error and ends with exception if there was an error"""


def js2enti(pkey,pelem):
    enti = Entity()
    enti.enti_id = jsguid2id(pkey)
    enti.enti_name = pelem['name'][pmodel.modellanguage()]
    enti.enti_short_name = pelem['shortname']
    enti.enti_prefix = pelem['prefix']
    enti.enti_tooltip = pelem['tooltip'][pmodel.modellanguage()]
    enti.enti_descr = pelem['descr'][pmodel.modellanguage()]
    enti.enti_exp_tuplecnt = pelem['exptuple#']
    enti.enti_uc = pelem['uc']
    enti.enti_dc = pelem['dc']
    enti.enti_um = pelem['um']
    enti.enti_dm = pelem['dm']
    return enti

def entities2sql(pmodel: JSModel):
    for jid, jelem in pmodel.jsmodel['entities'].items():
        enti = js2enti(pkey=jsjid,pelem=jelem)
        try:
            entiid = enti.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=[jid] + list(jelem))
            continue

        minzoomlevel = pelem['minzoomlevel']
        maxzoomlevel = pelem['maxzoomlevel']
        devstatus = pelem['devstatus']
        Modelelement.upddisplelements(pmodeid=entiid, pminzl=minzoomlevel, pmaxzl=maxzoomlevel, pdevstat=devstatus)
        inslgtx(pmodel=pmodel, pmodeid=entiid, pattr=Languagetext.ENTI_NAME, ptexts=jelem['name'])
        inslgtx(pmodel=pmodel, pmodeid=entiid, pattr=Languagetext.ENTI_COMMENT, ptexts=jelem['descr'])
        inslgtx(pmodel=pmodel, pmodeid=entiid, pattr=Languagetext.ENTI_TOOLTIP, ptexts=jelem['tooltip'])
        inssourceref(pmodel=pmodel, pmodeid=entiid, psources=jelem["sourceref"])
        updvs2sql(pmodel=pmodel, pmodeid=jsguid2id(jid), pudps=jelem["userdefprops"])

        """      "ENTI109": {
         "synonyms":
            {
               "de": "Jemand",
               "en": "Contact person",
            },..
        """
        for synoid, jsyno in jelem["synonyms"].items():
            syno = Synonym(pname=jsyno[pmodel.modellanguage()], pentiid=entiid)
            syno.syno_id = jsguid2id(synoid)
            try:
                syno.insert()
            except Exception as err:
                pmodel.markerror(pmsg=err, pelemstr=jsyno)
                continue
            inslgtx(pmodel=pmodel, pmodeid=syno.syno_id, pattr=Languagetext.ENTI_SYNONYM, ptexts=jsyno)
        # for

    # for
# entities2sql

"""transfer references and subtypes"""


def entirefs2sql(pmodel: JSModel):
    return
