from IM_OBJECTS import *
from IM_JSON import jsguid,domaingroupmembers

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
