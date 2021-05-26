from IM_JSON import *
from IM_OBJECTS import *
from mystring import nvl
import re

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

def entityicon(penti:Entity = None):
    """ None = emptymodel"""
    """    "icon": {
               "type": "", 
               "reference": ""
            },
    """
    urlregex = re.compile("((http|https)://)(www.)?[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)")
    iconnoregexp = re.compile(r"^[0-9]{2,5}$")

    icontype,iconref = None,None
    retval = lambda t,r : {"type" : t, "reference": r}
    if penti is None:
        return retval(icontype,iconref)
    else:
        docus = Document.geticons(penti.enti_id)
        """if there is more than 1, choose the first one"""
        if len(docus) > 0:
            ref = docus[0].docu_reference
            if ref is not None and re.match(iconnoregexp,ref):
                icontype = 'FYAYCICON'
                iconref = ref
            elif ref is not None and re.match(urlregex,docus[0].docu_reference):
                icontype = 'URL'
                iconref = ref
            else:
                icontype ='FILE'
                iconref = ref if ref is not None else docus[0].docu_name
            #fi
        return retval(icontype,iconref)

def entities2js(pemptymodel):
    model = ['name', 'shortname'
        , 'descr', 'tooltip'
        , 'exptuple#', 'prefix'
        , 'subtypellevel+'
        , 'uc', 'dc', 'um', 'dm'
        , 'minzoomlevel', 'maxzoomlevel', 'devstatus'
        , 'icon'
        , 'synonyms', 'sourceref'
        , 'supertypes+','roles+'
        , 'subtypes+', 'attributes+'
        , 'relations+', 'keys+'
        , 'inarcs+', 'referencedby', 'userdefprops'
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
                                        ,entityicon()
                                       ,synonyms(None),sourceref(None)
                                       ,reflist(None),reflist(None)
                                       ,reflist(None),reflist(None)
                                       , reflist(None),reflist(None)
                                       , reflist(None),reflist(None)
                                       , userdefprops(None)
                                        , tabreflist(None),reflist(None)
                                            ]
                                       )
                }
    else:
        entis = {jsguid(Modelelemtype.ENTI, e.enti_id):
                     fillmodel(pmodel=model,
                            pentries=[multilangtext(ptext=e.enti_name_l), e.enti_short_name
                        , multilangtext(e.enti_descr_l),multilangtext(e.enti_tooltip_l)
                        , e.enti_exp_tuplecnt,e.enti_prefix
                        , e.getsubtypelevel()
                        , e.enti_uc, e.enti_dc, e.enti_um,e.enti_dm
                        , e.getminzoomlevel(),e.getmaxzoomlevel(),e.getdevstatus()
                        , entityicon(penti=e)
                        , synonyms(psynos={jsguid(Modelelemtype.SYNO, s.syno_id): s.syno_name_l for s in e.getsynonyms()})
                        , sourceref(pvalues=Externalref.getsrcinfo(pmodeid=e.enti_id))
                        , reflist(plist=[jsguid(Modelelemtype.ENTI, es.enti_id) for es in e.getparents()])
                        , reflist(plist=[jsguid(Modelelemtype.ENTI, es.enti_id) for es in e.getchildren(ptype=Relation.ISAROLE)])
                        , reflist(plist=[jsguid(Modelelemtype.ENTI, es.enti_id) for es in e.getchildren(ptype=Relation.ISASUBTYPE)])
                        , reflist(plist=[jsguid(Modelelemtype.ATTR, a.attr_id) for a in e.getattributes()])
                        , reflist(plist=[jsguid(Modelelemtype.RELA, r.rela_id) for r in Relation.getbyentity(pentiid=e.enti_id)])
                        , reflist(plist=[jsguid(Modelelemtype.KEYS, k.keys_id) for k in Key.select(pwhere=("keys_enti_id = ?", e.enti_id))])
                        , reflist(plist=[jsguid(Modelelemtype.ARCS, a.arcs_id) for a in Arc.select(pwhere=("arcs_enti_id = ?",e.enti_id))])
                             , [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=e.enti_id)]\
                                +[jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=e.enti_id)]
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


def js2enti(pkey,pelem,psrcname=None,psrcid=None,pmodellang=None):
    enti = Entity(psrcname=psrcname,psrcid=psrcid)
    enti.enti_id = jsguid2id(pkey)
    enti.enti_name = pelem['name'][pmodellang]
    enti.enti_short_name = pelem['shortname']
    enti.enti_prefix = pelem['prefix']
    enti.enti_tooltip = pelem['tooltip'][pmodellang]
    enti.enti_descr = pelem['descr'][pmodellang]
    enti.enti_exp_tuplecnt = pelem['exptuple#']
    enti.enti_uc = pelem['uc']
    enti.enti_dc = pelem['dc']
    enti.enti_um = pelem['um']
    enti.enti_dm = pelem['dm']
    return enti

def entities2sql(presult:Mergeresult, podmjson: JSModel, pwithextsrcref):
    fromodm2db(presult=presult, podmjson=podmjson,  pelemtype=Modelelemtype.ENTI, pjs2obj=js2enti,
                   pwithextsrcref=pwithextsrcref)

    for jid, jelem in podmjson.getelements(pelemtype=Modelelemtype.ENTI).items():
        entiid = keytransl(jid)
        minzoomlevel = jelem['minzoomlevel']
        maxzoomlevel = jelem['maxzoomlevel']
        devstatus = jelem['devstatus']

        """Synonyms have in ODM no guid. Delete them and fill new synonyms"""
        inscnt = 0
        delcnt = Synonym.delete(pwhere=("syno_enti_id=?",entiid))
        for synoid, jsyno in jelem["synonyms"].items():
            syno = Synonym(pname=jsyno[podmjson.modellanguage()], pentiid=entiid)
            syno.syno_id = jsguid2id(synoid)
            try:
                syno.insert()
                inscnt += 1
            except Exception as err:
                presult.markdberror(perr=err, pelem=jsyno)
                continue
            """synonyms and their lang-texts are alreday deleted"""
            insertlgtx(pmodeid=syno.syno_id, pattr=Languagetext.ENTI_SYNONYM, ptexts=jsyno)
        # for
        presult.insertcnt += max(0, (inscnt - delcnt))
        presult.deletecnt += max(0, (delcnt - inscnt))

        Modelelement.upddisplelements(pmodeid=entiid, pminzl=minzoomlevel, pmaxzl=maxzoomlevel, pdevstat=devstatus)
        replacelgtx(presult=presult, pmodeid=entiid, pattr=Languagetext.ENTI_NAME, ptexts=jelem['name'])
        replacelgtx(presult=presult, pmodeid=entiid, pattr=Languagetext.ENTI_COMMENT, ptexts=jelem['descr'])
        replacelgtx(presult=presult, pmodeid=entiid, pattr=Languagetext.ENTI_TOOLTIP, ptexts=jelem['tooltip'])
        insreferences(presult=presult,pmodeid=entiid,prefs=jelem['referencedby'])
        inssourceref(presult=presult, pmodeid=entiid, psources=jelem["sourceref"])
        udpvs2sql(presult=presult, pmodeid=entiid, pudps=jelem["userdefprops"])
    #for
# entities2sql
