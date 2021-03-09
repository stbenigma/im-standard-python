from IM_JSON import *
from IM_OBJECTS import *


def businessrule2js(pburuid=None):
    model = ['name','level', 'type'
            , 'readwrite', 'rule', 'errosmsg', 'refelements'
             ]
    if pburuid is None:
        retval = fillmodel(pmodel=model,pentries=['' for idx in range(len(model))])
    else:
        bures = BusinessruleElement.getburuelements(pmodeid=pburuid)
        if not bures: return []
        retval = []
        for bure in bures:
            buru: BusinessRule = bure.getparent()
            refobjs = []
            if (buru.buru_type == BusinessRule.BURU_TYPE_CALC) or \
                    (buru.buru_type == BusinessRule.BURU_TYPE_CHECK and buru.buru_level != BusinessRule.BURU_LEVEL_ATTR):
                refobjs = []  # fill jsguids
            # print (bure.getparent().buru_name)
            burujs = {'name': buru.buru_name, 'level': buru.buru_level, 'type': buru.buru_type
                , 'readwrite': "W" if Boolean.str2bool(bure.bure_writeable) else 'R', 'rule': buru.buru_rule
                      }
            if buru.buru_type == BusinessRule.BURU_TYPE_CHECK:
                burujs['errosmsg'] = buru.buru_errormsg
            if len(refobjs) > 0:
                burujs['refelements'] = [r for r in refobjs]
            retval.append(burujs)
    #fi
    return retval


def attr2js(pattr):
    model = ['techname', 'name'
            , 'seq', 'entity'
            , 'domain', 'basedatatype+'
            , 'type+', 'memberattrs+'
            , 'descriptive', 'mandatory'
            , 'historicised', 'repeated'
            , 'translated', 'encrypted'
            , 'tooltip', 'descr'
            , 'uc', 'dc', 'um', 'dm'
        , 'minzoomlevel', 'maxzoomlevel', 'devstatus'
        , 'sourceref', 'keys+'
             #, 'businessrules'
            , 'refindocuments+'
            , 'refbyorgunits+', 'userdefprops'
            , 'columnsmapped+', 'diagrams+'
        ]
    if pattr is None:
        retval = fillmodel(pmodel=model
                           ,pentries=['', multilangtext()
                                     ,'',''
                                    ,'',''
                                    ,'', reflist()
                                     ,'',''
                                    ,'',''
                                    ,'',''
                                    , multilangtext(), multilangtext()
                                     ,'','','','',0,4,'DEV'
                                     , sourceref(), reflist()
                                     #, businessrules2js()
                                      , reflist()
                                     , reflist(), userdefprops()
                                    , reflist(), reflist()
                                      ]
                           )
    else:
        doma = Domain().getbyid(pattr.attr_doma_id)

        retval = fillmodel(pmodel=model
                           ,pentries=[ pattr.attr_tech_name,multilangtext( pattr.attr_displ_name_l)
            ,  pattr.attr_displ_seq, jsguid(Modelelemtype.ENTI, pattr.attr_enti_id)
            ,  jsguid(Modelelemtype.DOMA, pattr.attr_doma_id),  None if doma.doma_daty_id is None else Datatype().getbyid(doma.doma_daty_id).daty_name
            ,  doma.doma_type,  None if (Domain().getbyid(pattr.attr_doma_id).doma_type != Domain.GRP) else domaingroupmembers(pdomaid=pattr.attr_doma_id)
            , Boolean.str2bool(pattr.attr_is_descriptive),Boolean.str2bool(pattr.attr_is_mandatory)
            , Boolean.str2bool(pattr.attr_is_historicised), Boolean.str2bool(pattr.attr_is_repeated)
            , Boolean.str2bool(pattr.attr_is_translated),  Boolean.str2bool(pattr.attr_is_encrypted)
            , multilangtext(pattr.attr_tooltip_l)
            , multilangtext(pattr.attr_descr_l)
            , pattr.attr_uc, pattr.attr_dc,  pattr.attr_um, pattr.attr_dm
            , pattr.getminzoomlevel(), pattr.getmaxzoomlevel(), pattr.getdevstatus()
            , Externalref.getsrcinfo(pmodeid=pattr.attr_id), [jsguid(Modelelemtype.KEYS, k.keys_id) for k in pattr.getkeys()]
            #, businessrules2js(pburuid=pattr.attr_id)
                , [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=pattr.attr_id)]
            , reflist(plist=[jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=pattr.attr_id)])
                ,  userdefprops(udpv2js(pmodeid=pattr.attr_id, pmodelemtype=Modelelemtype.ATTR))
            ,  colureflist({jsguid(Modelelemtype.INTF, s.getid()): [jsguid(Modelelemtype.COLU, c.colu_id) for c in
                                                        ColAttrMap.getcolulist(pattrid=pattr.attr_id, pintfid=s.getid())]
                            for s in Interface.getmapped(pattrid=pattr.attr_id)
                            }
                           )
            , reflist(plist=[jsguid(Modelelemtype.DIAG, d.diag_id) for d in Diagram.getdiagrams(pmodeid=pattr.attr_id)])
                ])
        if (Domain().getbyid(pattr.attr_doma_id).doma_type != Domain.GRP):
            del retval['memberattrs+']
    # fi
    return retval


def attributes2js(pemptymodel):
    if pemptymodel:
        attrs = {jsguid(Modelelemtype.ATTR,'0000') : attr2js(None)}
    else:
        attrs = {jsguid(Modelelemtype.ATTR, a.attr_id): attr2js(a) for a in Attribute.select()}
    return attrs


def attributes2sql(pmodel: JSModel):
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
    for jid, jelem in pmodel.jsmodel['attributes'].items():
        attr = Attribute()
        attr.attr_id = jsguid2id(jid)
        attr.attr_enti_id = jsguid2id(jelem['entity'])
        attr.attr_doma_id = jsguid2id(jelem['domain'])
        attr.attr_tech_name = jelem['techname']
        attr.attr_displ_name = jelem['name'][pmodel.modellanguage()]
        attr.attr_displ_seq = jelem['seq']
        attr.attr_tooltip = jelem['tooltip'][pmodel.modellanguage()]
        attr.attr_descr = jelem['descr'][pmodel.modellanguage()]
        attr.attr_is_descriptive = Boolean.bool2str(jelem['descriptive'])
        attr.attr_is_mandatory = Boolean.bool2str(jelem['mandatory'])
        attr.attr_is_historicised = Boolean.bool2str(jelem['historicised'])
        attr.attr_is_repeated = Boolean.bool2str(jelem['repeated'])
        attr.attr_is_translated = Boolean.bool2str(jelem['translated'])
        attr.attr_is_encrypted = Boolean.bool2str(jelem['encrypted'])
        attr.attr_uc = jelem['uc']
        attr.attr_dc = jelem['dc']
        attr.attr_um = jelem['um']
        attr.attr_dm = jelem['dm']
        minzoomlevel = jelem['minzoomlevel']
        maxzoomlevel = jelem['maxzoomlevel']
        devstatus = jelem['devstatus']
        try:
            attrid = attr.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=[jid] + list(jelem))
            continue

        Modelelement.upddisplelements(pmodeid=attrid, pminzl=minzoomlevel, pmaxzl=maxzoomlevel, pdevstat=devstatus)
        inslgtx(pmodel=pmodel, pmodeid=attrid, pattr=Languagetext.ATTR_COMMENT, ptexts=jelem['descr'])
        inslgtx(pmodel=pmodel, pmodeid=attrid, pattr=Languagetext.ATTR_TOOLTIP, ptexts=jelem['tooltip'])
        inslgtx(pmodel=pmodel, pmodeid=attrid, pattr=Languagetext.ATTR_NAME, ptexts=jelem['name'])
        inssourceref(pmodel=pmodel, pmodeid=attrid, psources=jelem["sourceref"])
    # for

    """transfer references and subtypes"""


def attrrefs2sql(pmodel):
    for jid, jelem in pmodel.getelements(Modelelemtype.ATTR).items():
        updvs2sql(pmodel=pmodel, pmodeid=jsguid2id(jid), pudps=jelem["userdefprops"])
    return


def keyelems2js(pkey):
    model = ['attributes', 'relations']
    if pkey is None:
        retval = fillmodel(pmodel=model,pentries=[reflist(),reflist()])
    else:
        retval = fillmodel(pmodel=model
                           ,pentries=[[jsguid(Modelelemtype.ATTR, ke.kele_attr_id)
                                           for ke in pkey.getkeyelements(Modelelemtype.ATTR)]
                                        ,[jsguid(Modelelemtype.RELA, ke.kele_rela_id)
                                            for ke in pkey.getkeyelements(Modelelemtype.RELA)]
                                      ]
                           )
    # fi
    return retval


def keys2js(pemptymodel):
    model =    [ 'name', 'entity'
                    , 'uc', 'dc', 'um', 'dm'
                    , 'sourceref', 'key-elements'
                 ]
    if pemptymodel:
        retval = {jsguid(Modelelemtype.KEYS, "0000") : fillmodel(pmodel=model, pentries=['', '', '', '', '', '', sourceref(), keyelems2js(None)])}
    else:

        retval = {jsguid(Modelelemtype.KEYS, k.keys_id):
                      fillmodel(pmodel=model
                               ,pentries=[k.keys_name, jsguid(Modelelemtype.ENTI, k.keys_enti_id)
                                        , 'uc', 'dc', 'um', 'dm'
                                    , Externalref.getsrcinfo(pmodeid=k.keys_id)
                                    ,  keyelems2js(k)
                                      ]
                                )
                 for k in Key.select()}

    return retval


def ins1kele(pmodel: JSModel, pkey: Key, pattrid, prelaid):
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
        from mystring import nvl
        print(pkey.keys_id, [p.keys_id for p in Key.select(pwhere="keys_id = {}".format(nvl(pkey.keys_id, -1)))])
        print(prelaid, [p.rela_id for p in Relation.select(pwhere="rela_id = {}".format(nvl(prelaid, -1)))])
        print(pattrid, [p.attr_id for p in Attribute.select(pwhere="attr_id = {}".format(nvl(pattrid, -1)))])
        pmodel.markerror(pmsg=err, pelemstr=str(pkey.keys_id) + kele.tostring())
    return


def inskeyelements(pmodel: JSModel, pkey: Key, pkeles):
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
    for jid in pkeles['attributes'] + pkeles['relations']:
        ins1kele(pmodel=pmodel, pkey=pkey
                 , pattrid=jsguid2id(jid) if jsguid2type(jid) == Modelelemtype.ATTR else None
                 , prelaid=jsguid2id(jid) if jsguid2type(jid) == Modelelemtype.RELA else None)


def keys2sql(pmodel: JSModel):
    for jid, jelem in pmodel.getelements(Modelelemtype.KEYS).items():
        key = Key()
        key.keys_id = jsguid2id(jid)
        key.keys_name = jelem['name']
        key.keys_enti_id = jsguid2id(jelem['entity'])
        key.keys_uc = jelem['uc']
        key.keys_dc = jelem['dc']
        key.keys_um = jelem['um']
        key.keys_dm = jelem['dm']
        try:
            key.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=[jsguid2id(jid)] + list(jelem))
            continue
        inskeyelements(pmodel=pmodel, pkey=key, pkeles=jelem['key-elements'])
        inssourceref(pmodel=pmodel, pmodeid=jsguid2id(jid), psources=jelem["sourceref"])
    # for
    return


def keysrefs2sql(pmodel):
    return
