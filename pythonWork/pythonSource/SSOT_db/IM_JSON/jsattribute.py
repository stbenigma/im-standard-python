from SSOT_db.IM_JSON import *
from SSOT_db.IM_OBJECTS import *
from SSOT_db.IM_JSON.jsdomain import domaingroupmembers
from SSOT_db.IM_JSON import jsentity

def buruinelements(pelemid=None):
    if pelemid is None:
        retval = {'checked': [],
                  'referenced': [],
                  'changed': []}
    else:
        bures = BusinessruleElement.select(pwhere=("bure_mode_id = ?", pelemid))
        retval = {'checked': [jsguid(Modelelemtype.BURU,be.bure_buru_id) for be in bures if be.bure_role == BusinessruleElement.AFFECTED],
                  'referenced': [jsguid(Modelelemtype.BURU,be.bure_buru_id) for be in bures if be.bure_role == BusinessruleElement.REFERENCED],
                  'changed': [jsguid(Modelelemtype.BURU,be.bure_buru_id) for be in bures if Boolean.str2bool(be.bure_writeable) ]}
    return retval


def buruelement2js(pbure=None):
    if pbure is None:
        retval = {'elemid': 'xxxx0000', 'role': '', 'r/w': ''}
    else:
        mode = Modelelement().getbyid(pbure.bure_mode_id)
        retval = {'elemid': jsguid(mode.mode_type, mode.mode_id),
                  'role': pbure.bure_role,
                  'r/w': pbure.bure_writeable}
    return retval


def businessrule2js(pburu):
    model = ['name', 'descr', 'level', 'type'
        , 'impact', 'rule', 'errosmsg', 'elements'
             ]
    if pburu is None:
        retval = fillmodel(pmodel=model,
                           pentries=[multilangtext(), multilangtext(),
                                     '', '', '', '',
                                     multilangtext(),
                                     [buruelement2js()]
                                     ]
                           )
    else:
        retval = fillmodel(pmodel=model,
                           pentries=[multilangtext(pburu.buru_name_l),
                                     multilangtext(pburu.buru_descr_l),
                                     pburu.buru_level, pburu.buru_type,
                                     pburu.buru_impact, pburu.buru_rule,
                                     multilangtext(pburu.buru_errormsg_l),
                                     [buruelement2js(be) for be in pburu.getchildren()]
                                     ]
                           )
    # fi
    return retval


def businessrules2js(pemptymodel):
    if pemptymodel:
        burus = {jsguid(Modelelemtype.BURU, '0000'): businessrule2js(None)}
    else:
        burus = {jsguid(Modelelemtype.BURU, b.buru_id): businessrule2js(b) for b in BusinessRule.select()}
    return burus


def attr2js(pattr):
    model = ['techname', 'name'
        , 'seq', 'entity'
        , 'domain', 'basedatatype+'
        , 'type+', 'memberattrs+'
        , 'descriptive', 'mandatory'
        , 'historicised', 'repeated'
        , 'translated', 'encrypted'
        , 'examples', 'tooltip', 'descr'
        , 'uc', 'dc', 'um', 'dm'
        , 'minzoomlevel', 'maxzoomlevel', 'publstatus'
        , 'sourceref', 'keys+', 'businessrules+'
        , 'referencedby', 'userdefprops'
        , 'columnsmapped+', 'diagrams+'
             ]
    if pattr is None:
        retval = fillmodel(pmodel=model
                           , pentries=['', multilangtext()
                , '', ''
                , '', ''
                , '', reflist()
                , '', ''
                , '', ''
                , '', ''
                , jentity.examples2js(None), multilangtext(), multilangtext()
                , '', '', '', '', 0, 4, 'DRAFT'
                , sourceref(), reflist(), buruinelements(None)
                , reflist(), userdefprops()
                , {jsguid(Modelelemtype.INTF, "0000"):
                       [jsguid(Modelelemtype.COLU, "0000")]}, reflist()
                                       ]
                           )
    else:
        doma = Domain().getbyid(pattr.attr_doma_id)

        retval = fillmodel(pmodel=model,
                           pentries=[pattr.attr_tech_name, multilangtext(pattr.attr_displ_name_l),
                                     pattr.attr_displ_seq, jsguid(Modelelemtype.ENTI, pattr.attr_enti_id),
                                     jsguid(Modelelemtype.DOMA, pattr.attr_doma_id),
                                     None if doma.doma_daty_id is None else Datatype().getbyid(
                                         doma.doma_daty_id).daty_name,
                                     doma.doma_type,
                                     None if (doma.doma_type != Domain.GRP) else \
                                         domaingroupmembers(pdomaid=pattr.attr_doma_id),
                                     Boolean.str2bool(pattr.attr_is_descriptive),
                                     Boolean.str2bool(pattr.attr_is_mandatory),
                                     Boolean.str2bool(pattr.attr_is_historicised),
                                     Boolean.str2bool(pattr.attr_is_repeated),
                                     Boolean.str2bool(pattr.attr_is_translated),
                                     Boolean.str2bool(pattr.attr_is_encrypted),
                                     examples2js(pexpls=pattr.getexamples()),
                                     multilangtext(pattr.attr_tooltip_l),
                                     multilangtext(pattr.attr_descr_l),
                                     pattr.attr_uc, pattr.attr_dc, pattr.attr_um, pattr.attr_dm,
                                     pattr.getminzoomlevel(), pattr.getmaxzoomlevel(), pattr.getpublstatus(),
                                     Externalref.getsrcinfo(pmodeid=pattr.attr_id),
                                     [jsguid(Modelelemtype.KEYS, k.keys_id) for k in pattr.getkeys()],
                                     buruinelements(pattr.attr_id),
                                     [jsguid(Modelelemtype.DOCU, d[0]) for d in
                                      Document.getrefdoculist(pid=pattr.attr_id)] \
                                     + [jsguid(Modelelemtype.ORGU, d[0]) for d in
                                        OragnisationalUnit.getreforgulist(pid=pattr.attr_id)],
                                     userdefprops(udpv2js(pmodeid=pattr.attr_id, pmodelemtype=Modelelemtype.ATTR)),
                                     colureflist({jsguid(Modelelemtype.INTF, s.getid()): [
                                         jsguid(Modelelemtype.COLU, c.colu_id) for c in
                                         ColAttrMap.getcolulist(pattrid=pattr.attr_id,
                                                                pintfid=s.getid())]
                                         for s in Interface.getmapped(pattrid=pattr.attr_id)
                                     }
                                     ),
                                     reflist(
                                         plist=[jsguid(Modelelemtype.DIAG, d.diag_id) for d in
                                                Diagram.getdiagrams(pmodeid=pattr.attr_id)])
                                     ])
        if (doma.doma_type != Domain.GRP):
            del retval['memberattrs+']
    # fi
    return retval


def attributes2js(pemptymodel):
    if pemptymodel:
        attrs = {jsguid(Modelelemtype.ATTR, '0000'): attr2js(None)}
    else:
        attrs = {jsguid(Modelelemtype.ATTR, a.attr_id): attr2js(a) for a in Attribute.select()}
    return attrs


def js2attr(pkey, pelem, psrcname=None, psrcid=None, pmodellang=None):
    attr = Attribute(psrcname=psrcname, psrcid=psrcid)
    attr.attr_id = jsguid2id(pkey)
    attr.attr_enti_id = jsguid2id(pelem['entity'])
    attr.attr_doma_id = jsguid2id(pelem['domain'])
    attr.attr_tech_name = pelem['techname']
    attr.attr_displ_name = pelem['name'][pmodellang]
    attr.attr_displ_seq = pelem['seq']
    attr.attr_tooltip = pelem['tooltip'][pmodellang]
    attr.attr_descr = pelem['descr'][pmodellang]
    attr.attr_is_descriptive = Boolean.bool2str(pelem['descriptive'])
    attr.attr_is_mandatory = Boolean.bool2str(pelem['mandatory'])
    attr.attr_is_historicised = Boolean.bool2str(pelem['historicised'])
    attr.attr_is_repeated = Boolean.bool2str(pelem['repeated'])
    attr.attr_is_translated = Boolean.bool2str(pelem['translated'])
    attr.attr_is_encrypted = Boolean.bool2str(pelem['encrypted'])
    attr.attr_uc = pelem['uc']
    attr.attr_dc = pelem['dc']
    attr.attr_um = pelem['um']
    attr.attr_dm = pelem['dm']
    return attr


def attributes2sql(presult: Mergeresult, podmjson: JSModel, pwithextsrcref):
    fromodm2db(presult=presult, podmjson=podmjson, pelemtype=Modelelemtype.ATTR, pjs2obj=js2attr,
               pwithextsrcref=pwithextsrcref)
    """      "ATTR11890": {
         "techname": "EMAIL",
         "name": {
            "de": "eMail",
            "en": "eMail",
            "fr": "Courriel"
         },
         "seq": 1,
         "entity": "ENTI11889",
         "relation": null,
         "domain": "DOMA11877",
         "descriptive": false,
         "mandatory": false,
         "historicised": false,
         "repeated": false,
         "translated": false,
         "encrypted": false,
         "examples": {
            "de": null,
            "en": null,
            "fr": null
         },
         "tooltip": {
            "de": null,
            "en": null,
            "fr": null
         },
         "descr": {
            "de": null,
            "en": null,
            "fr": null
         },
         "uc": "stb",
         "dc": "2019-06-01 10:36:20 UTC",
         "um": null,
         "dm": null,

      },"""
    for jid, jelem in podmjson.getelements(pelemtype=Modelelemtype.ATTR).items():
        attrid = keytransl(jid)
        minzoomlevel = jelem['minzoomlevel']
        maxzoomlevel = jelem['maxzoomlevel']
        publstatus = jelem['publstatus']
        Modelelement.upddisplelements(pmodeid=attrid, pminzl=minzoomlevel, pmaxzl=maxzoomlevel, ppublstat=publstatus)

        """Examples have in ODM no guid. Delete them and fill new synonyms"""
        jsentity.mergeexamples(pelem=jelem, pmodellang=podmjson.modellanguage(),
                               presult=presult, pattrid=attrid)

        replacelgtx(presult=presult, pmodeid=attrid, pattr=Languagetext.ATTR_COMMENT, ptexts=jelem['descr'])
        replacelgtx(presult=presult, pmodeid=attrid, pattr=Languagetext.ATTR_TOOLTIP, ptexts=jelem['tooltip'])
        replacelgtx(presult=presult, pmodeid=attrid, pattr=Languagetext.ATTR_NAME, ptexts=jelem['name'])
        insreferences(presult=presult, pmodeid=attrid, prefs=jelem['referencedby'])
        inssourceref(presult=presult, pmodeid=attrid, psources=jelem["sourceref"])
        udpvs2sql(presult=presult, pmodeid=attrid, pudps=jelem["userdefprops"])
    # for


def keyelems2js(pkey):
    model = ['attributes', 'relations']
    if pkey is None:
        retval = fillmodel(pmodel=model, pentries=[reflist(), reflist()])
    else:
        retval = fillmodel(pmodel=model,
                           pentries=[[jsguid(Modelelemtype.ATTR, ke.kele_attr_id)
                                      for ke in pkey.getkeyelements(Modelelemtype.ATTR)],
                                     [jsguid(Modelelemtype.RELA, ke.kele_rela_id)
                                      for ke in pkey.getkeyelements(Modelelemtype.RELA)]
                                     ]
                           )
    # fi
    return retval


def keys2js(pemptymodel):
    model = ['name', 'entity',
             'uc', 'dc', 'um', 'dm',
             'sourceref', 'key-elements'
             ]
    if pemptymodel:
        retval = {jsguid(Modelelemtype.KEYS, "0000"): fillmodel(pmodel=model,
                                                                pentries=['', '', '', '', '', '', sourceref(),
                                                                          keyelems2js(None)])}
    else:
        keys = Key.select()

        retval = {jsguid(Modelelemtype.KEYS, k.keys_id):
                      fillmodel(pmodel=model,
                                pentries=[k.keys_name, jsguid(Modelelemtype.ENTI, k.keys_enti_id),
                                          k.keys_uc, k.keys_dc, k.keys_um, k.keys_dm,
                                          Externalref.getsrcinfo(pmodeid=k.keys_id),
                                          keyelems2js(k)
                                          ]
                                )
                  for k in keys}

    return retval


def ins1kele(presult: Mergeresult, pkey: Key, pattrid, prelaid):
    kele = Keyelement()
    kele.kele_keys_id = pkey.keys_id
    kele.kele_attr_id = pattrid
    kele.kele_rela_id = prelaid
    kele.kele_uc = pkey.keys_uc
    kele.kele_dc = pkey.keys_dc
    kele.kele_um = pkey.keys_um
    kele.kele_dm = pkey.keys_dm
    try:
        kele.insert()
    except Exception as err:
        presult.markdberror(perr=err, pelem=str(pkey.keys_id) + kele.tostring())
    return


def inskeyelements(presult: Mergeresult, pkey: Key, pkeles):
    """         "key-elements": {
            "attributes": [
               "ATTR11911",
               "ATTR11912",
               "ATTR11913"
            ],
            "relations": [
               "RELA11992"
            ]
         }
    """
    inscnt = 0
    delcnt = Keyelement.delete(pwhere=("kele_keys_id = ?", pkey.keys_id))
    for jid in pkeles['attributes'] + pkeles['relations']:
        ins1kele(presult=presult, pkey=pkey,
                 pattrid=keytransl(jid) if jsguid2type(jid) == Modelelemtype.ATTR else None,
                 prelaid=keytransl(jid) if jsguid2type(jid) == Modelelemtype.RELA else None)
        inscnt += 1
    # for
    presult.addinscnt(max(0, (inscnt - delcnt)))
    presult.adddelcnt(max(0, (delcnt - inscnt)))
    return


def js2keys(pkey, pelem, psrcname=None, psrcid=None, pmodellang=None):
    key = Key(psrcname=psrcname, psrcid=psrcid)
    key.keys_id = jsguid2id(pkey)
    key.keys_name = pelem['name']
    key.keys_enti_id = jsguid2id(pelem['entity'])
    key.keys_uc = pelem['uc']
    key.keys_dc = pelem['dc']
    key.keys_um = pelem['um']
    key.keys_dm = pelem['dm']
    return key


def keys2sql(presult: Mergeresult, podmjson: JSModel, pwithextsrcref):
    fromodm2db(presult=presult, podmjson=podmjson, pelemtype=Modelelemtype.KEYS, pjs2obj=js2keys,
               pwithextsrcref=pwithextsrcref)

    for jid, jelem in podmjson.getelements(pelemtype=Modelelemtype.KEYS).items():
        key = Key().getbyid(pid=keytransl(jid))
        inskeyelements(presult=presult, pkey=key, pkeles=jelem['key-elements'])
        if pwithextsrcref:
            inssourceref(presult=presult, pmodeid=key.keys_id, psources=jelem["sourceref"])
    # for
    return
