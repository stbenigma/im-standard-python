from IM_OBJECTS import *
from IM_JSON import jsguid,domaingroupmembers,jsguid2id,inslgtx,inssourceref,JSModel,jsguid2type,udpv2js,updvs2sql

def defattr(attr):
    doma = Domain().getbyid(attr.attr_doma_id)

    retval = {'techname': attr.attr_tech_name
        , 'name': attr.attr_displ_name_L
        , 'seq': attr.attr_displ_seq
        , 'entity': jsguid(Modelelemtype.ENTI, attr.attr_enti_id)
        , 'domain': jsguid(Modelelemtype.DOMA, attr.attr_doma_id)
        ,'basedatatype+':  None if doma.doma_daty_id is None else Datatype().getbyid(doma.doma_daty_id).daty_name
        ,'type+' : doma.doma_type
        ,'memberattrs+' : domaingroupmembers(pdomaid=attr.attr_doma_id) if (Domain().getbyid(attr.attr_doma_id).doma_type == Domain.GRP) else None
        , 'descriptive': Boolean.str2bool(attr.attr_is_descriptive)
        , 'mandatory': Boolean.str2bool(attr.attr_is_mandatory)
        , 'historicised': Boolean.str2bool(attr.attr_is_historicised)
        , 'repeated': Boolean.str2bool(attr.attr_is_repeated)
        , 'translated': Boolean.str2bool(attr.attr_is_translated)
        , 'encrypted': Boolean.str2bool(attr.attr_is_encrypted)
        , 'tooltip': attr.attr_tooltip_L
        , 'descr': attr.attr_descr_L
        , 'uc': attr.attr_uc
        , 'dc': attr.attr_dc
        , 'um': attr.attr_um
        , 'dm': attr.attr_dm
        , 'sourceref': Externalref.getsrcinfo(pmodeid=attr.attr_id)
        , 'keys+': [jsguid(Modelelemtype.KEYS, k.keys_id) for k in attr.getkeys()]
        , 'refindocuments+': [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=attr.attr_id)]
        , 'refbyorgunits+': [jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=attr.attr_id)]
        , 'userdefprops': udpv2js(pmodeid=attr.attr_id,pmodelemtype=Modelelemtype.ATTR)
        , 'columnsmapped+': {
            jsguid(Modelelemtype.INTF,s.getid()): [jsguid(Modelelemtype.COLU, c.colu_id) for c in
                                                   ColAttrMap.getcolulist(pattrid=attr.attr_id, pintfid=s.getid())]
            for s in Interface.getmapped(pattrid=attr.attr_id)}
        , 'diagrams+': [jsguid(Modelelemtype.DIAG, d.diag_id) for d in Diagram.getdiagrams(pmodeid=attr.attr_id)]
              }
    return retval


def attributes2js():
    attrs = {jsguid(Modelelemtype.ATTR, a.attr_id): defattr(a) for a in Attribute.select()}
    return attrs



def attributes2sql(pmodel:JSModel):
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
        attr.attr_doma_id  = jsguid2id(jelem['domain'])
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
        try:
            attrid = attr.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=[jid] + list(jelem))
            continue
        inslgtx(pmodel = pmodel,pmodeid=attrid, pattr=Languagetext.ATTR_COMMENT, ptexts=jelem['descr'])
        inslgtx(pmodel = pmodel,pmodeid=attrid, pattr=Languagetext.ATTR_TOOLTIP, ptexts=jelem['tooltip'])
        inslgtx(pmodel = pmodel,pmodeid=attrid, pattr=Languagetext.ATTR_NAME, ptexts=jelem['name'])
        inssourceref(pmodel = pmodel,pmodeid=attrid, psources=jelem["sourceref"])
    #for

    """transfer references and subtypes"""

def attrrefs2sql(pmodel):
    for jid, jelem in pmodel.jsmodel['attributes'].items():
        updvs2sql(pmodel=pmodel,pmodeid=jsguid2id(jid), pudps=jelem["userdefprops"])
    return

def keys2js():
    keys = {jsguid(Modelelemtype.KEYS, k.keys_id):
                {'name': k.keys_name
                    , 'entity': jsguid(Modelelemtype.ENTI, k.keys_enti_id)
                    , 'uc': k.keys_uc
                    , 'dc': k.keys_dc
                    , 'um': k.keys_um
                    , 'dm': k.keys_dm
                    ,'sourceref': Externalref.getsrcinfo(pmodeid=k.keys_id)
                    , 'key-elements': {'attributes':[jsguid(Modelelemtype.ATTR , ke.kele_attr_id)
                                                    for ke in k.getkeyelements(Modelelemtype.ATTR)]
                                     ,'relations': [jsguid(Modelelemtype.RELA , ke.kele_rela_id)
                                                    for ke in k.getkeyelements(Modelelemtype.RELA)]
                                   }
                 } for k in Key.select()}
    return keys

def ins1kele(pmodel:JSModel,pkey:Key,pattrid,prelaid):
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
        print (pkey.keys_id,[p.keys_id for p in Key.select(pwhere="keys_id = {}".format(nvl(pkey.keys_id,-1)))])
        print (prelaid,[p.rela_id for p in Relation.select(pwhere="rela_id = {}".format(nvl(prelaid,-1)))])
        print (pattrid,[p.attr_id for p in Attribute.select(pwhere="attr_id = {}".format(nvl(pattrid,-1)))])
        pmodel.markerror(pmsg=err, pelemstr=str(pkey.keys_id) + kele.tostring())
    return

def inskeyelements(pmodel:JSModel,pkey:Key,pkeles):
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
        ins1kele(pmodel=pmodel,pkey=pkey
                 ,pattrid=jsguid2id(jid) if jsguid2type(jid) == Modelelemtype.ATTR else None
                 ,prelaid=jsguid2id(jid) if jsguid2type(jid) == Modelelemtype.RELA else None)


def keys2sql(pmodel:JSModel):
    for jid,jelem in pmodel.jsmodel['keys'].items():
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
        inskeyelements(pmodel=pmodel,pkey=key,pkeles=jelem ['key-elements'])
        inssourceref(pmodel = pmodel,pmodeid=jsguid2id(jid), psources=jelem["sourceref"])
    #for
    return

def keysrefs2sql(pmodel):
    return