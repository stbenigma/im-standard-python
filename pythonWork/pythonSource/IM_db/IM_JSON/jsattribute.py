from IM_OBJECTS import *
from IM_JSON import jsguid,domaingroupmembers,jsguid2id,inslgtx,inssourceref

def defattr(attr):
    retval = {'techname': attr.attr_tech_name
        , 'name': attr.attr_displ_name_L
        , 'seq': attr.attr_displ_seq
        , 'entity': jsguid(Modelelemtype.ENTI, attr.attr_enti_id)
        , 'relation': jsguid(Modelelemtype.RELA, attr.attr_rela_id)
        , 'domain': jsguid(Modelelemtype.DOMA, attr.attr_doma_id)
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
        , 'sourceref': {s: Externalref.getsrcid(psrcname=s, pmodeid=attr.attr_id) for s in Externalref.getsources()}
        , 'keys': [jsguid(Modelelemtype.KEYS, k.keys_id) for k in attr.getkeys()]
        , 'refindocuments': [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=attr.attr_id)]
        , 'refbyorgunits': [jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=attr.attr_id)]
        , 'userdefprop': {t[0]: {g[1]: {u.udpr_name: Userdefpropvalue.udpvalue(pudprid=u.udpr_id, pmodeid=attr.attr_id)
                                        for u in
                                        Userdefprop.getudps(ptheme=t[0], pgroup=g[1], pmeltname=Modelelemtype.ATTR)}
                                 for g in Userdefprop.grouplist(pudptheme=t[0], pmelttype=Modelelemtype.ATTR)}
                          for t in Userdefprop.themelist(pmelttype=Modelelemtype.ATTR)}
        , 'columnsmapped': {
            jsguid(Modelelemtype.INTF,s.getid()): [jsguid(Modelelemtype.COLU, c.colu_id) for c in
                          AttrTransf.getcolulist(pattrid=attr.attr_id, pintfid=s.getid())]
            for s in Interface.getmapped(pattrid=attr.attr_id)}
        , 'diagrams': [jsguid(Modelelemtype.DIAG, d.diag_id) for d in Diagram.getdiagrams(pmodeid=attr.attr_id)]
              }
    doma = Domain().getbyid(attr.attr_doma_id)
    retval['basedatatype'] = None if doma.doma_daty_id is None else Datatype().getbyid(
        doma.doma_daty_id).daty_name
    retval['type'] = doma.doma_type
    if (Domain().getbyid(attr.attr_doma_id).doma_type == Domain.GRP):
        retval['memberattrs'] = domaingroupmembers(pdomaid=attr.attr_doma_id)
    return retval


def attributes2js():
    attrs = {jsguid(Modelelemtype.ATTR, a.attr_id): defattr(a) for a in Attribute.select()}
    return attrs


def keys2js():
    keys = {jsguid(Modelelemtype.KEYS, k.keys_id):
                {'name': k.keys_name
                    , 'entity': jsguid(Modelelemtype.ENTI, k.keys_enti_id)
                    , 'uc': k.keys_uc
                    , 'dc': k.keys_dc
                    , 'um': k.keys_um
                    , 'dm': k.keys_dm
                    ,'sourceref': {s: Externalref.getsrcid(psrcname=s, pmodeid=k.keys_id) for s in Externalref.getsources()}
                    , 'key-elements': {'attributes':[jsguid(Modelelemtype.ATTR , ke.kele_attr_id)
                                                    for ke in k.getkeyelements(Modelelemtype.ATTR)]
                  ,'relations': [jsguid(Modelelemtype.RELA , ke.kele_rela_id)
                                                    for ke in k.getkeyelements(Modelelemtype.RELA)]
                                   }
                 } for k in Key.select()}
    return keys


def attributes2sql(pmodel):
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
    for janker, jattr in pmodel.jsmodel['attributes'].items():
        attr = Attribute()
        attr.attr_id = jsguid2id(janker)
        attr.attr_enti_id = jsguid2id(jattr['entity'])
        attr.attr_rela_id = jsguid2id(jattr['relation'])
        attr.attr_doma_id  = jsguid2id(jattr['domain'])
        attr.attr_tech_name = jattr['techname']
        attr.attr_displ_name = jattr['name'][pmodel.language()]
        attr.attr_displ_seq = jattr['seq']
        attr.attr_tooltip = jattr['tooltip'][pmodel.language()]
        attr.attr_descr = jattr['descr'][pmodel.language()]
        attr.attr_is_descriptive = Boolean.bool2str(jattr['descriptive'])
        attr.attr_is_mandatory = Boolean.bool2str(jattr['mandatory'])
        attr.attr_is_historicised = Boolean.bool2str(jattr['historicised'])
        attr.attr_is_repeated = Boolean.bool2str(jattr['repeated'])
        attr.attr_is_translated = Boolean.bool2str(jattr['translated'])
        attr.attr_is_encrypted = Boolean.bool2str(jattr['encrypted'])
        attr.attr_uc = jattr['uc']
        attr.attr_dc = jattr['dc']
        attr.attr_um = jattr['um']
        attr.attr_dm = jattr['dm']
        try:
            attrid = attr.insert()
        except Exception as err:
            error(pmsg=err, pelem=[janker] + list(jattr))
            continue

    inslgtx(pmodel = pmodel,pmodeid=attrid, pattr=Languagetext.ATTR_COMMENT, ptexts=jattr['descr'])
    inslgtx(pmodel = pmodel,pmodeid=attrid, pattr=Languagetext.ATTR_TOOLTIP, ptexts=jattr['tooltip'])
    inslgtx(pmodel = pmodel,pmodeid=attrid, pattr=Languagetext.ATTR_NAME, ptexts=jattr['name'])
    inssourceref(pmodel = pmodel,pmodeid=attrid, psources=jattr["sourceref"])

    """      "ATTR11890": {

         "keys": [],
         "refindocuments": [],
         "refbyorgunits": [],
         "userdefprop": {
            "datamapping": {
               "DHL": {
                  "DHL AttrName": null,
                  "DHL AttrName Receiver": null,
                  "DHL AttrName Shipper": null
               },
               "PENTA": {
                  "PENTA AttrID": null,
                  "PENTA AttrName": null,
                  "PENTA datatype": null,
                  "PENTA usage": null
               },
               "PIM": {
                  "PIM AttrID": null,
                  "PIM AttrName": null,
                  "PIM EnglName": null,
                  "PIM datatype": null,
                  "PIM usage": null
               },
               "SAPByD": {
                  "SAPByD AttrName": null,
                  "SAPByD AttrName Receiver": null,
                  "SAPByD AttrName Shipper": null
               }
            },
            "translation": {
               "DE": {
                  "DE_ATTR_COMMENT": null,
                  "DE_ATTR_NAME": "eMail"
               },
               "EN": {
                  "EN_ATTR_COMMENT": null,
                  "EN_ATTR_NAME": "eMail"
               },
               "FR": {
                  "FR_ATTR_COMMENT": null,
                  "FR_ATTR_NAME": "Courriel"
               }
            }
         },
         "columnsmapped": {
            "INTF12068": [
               "COLU12375"
            ],
            "INTF12850": [
               "COLU12966"
            ],
            "INTF12440": [
               "COLU12613"
            ],
            "INTF12633": [
               "COLU12786"
            ]
         },
         "diagrams": [
            "DIAG12066",
            "DIAG12067"
         ],
         "basedatatype": "unknown",
         "type": "TXT"
      },"""
