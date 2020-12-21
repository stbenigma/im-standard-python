from IM_OBJECTS import *
from IM_JSON import jsguid

def domaingroupmembers(pdomaid):
    return [{'name': dg.dgrm_name
            ,'mandatory': dg.dgrm_is_mandatory
            , 'domain': jsguid(Modelelemtype.DOMA, dg.dgrm_doma_id_member)
            , 'descr': dg.dgrm_descr}
            for dg in DomaingroupMember.select(pwhere="dgrm_doma_id_group={}".format(pdomaid))
            ]


def domain2js(doma):
    retval = {'name': doma.doma_name_L
        , 'descr': doma.doma_descr_L
        , 'origin': doma.doma_origin
        , 'basedatatype': None if doma.doma_daty_id is None else Datatype().getbyid(doma.doma_daty_id).daty_name
        , 'type': doma.doma_type
        , 'displdatatype': {l.lang_iso_code2:doma.displdatatype(l.lang_iso_code2) for l in Language.select()}
        , 'datatypestr': doma.typestring()
        , 'uc': doma.doma_uc
        , 'um': doma.doma_um
        , 'dc': doma.doma_dc
        , 'dm': doma.doma_dm
              }
    if doma.doma_type == Domain.NUM:
        retval['minvalue'] = doma.doma_num_minvalue
        retval['maxvalue'] = doma.doma_num_maxvalue
        retval['totaldigits'] = doma.doma_num_total_digits
        retval['fractdigits'] = doma.doma_num_fract_digits
        retval['roundvalue'] = doma.doma_num_round_value
        if doma.doma_num_phyu_id is None:
            retval['unit'] = None
        else:
            retval['unit'] = PhysicalUnit().getbyid(doma.doma_num_phyu_id).phyu_name
    elif doma.doma_type == Domain.TXT:
        retval['maxlng'] = doma.doma_txt_maxlng
        retval['syntaxrule'] = doma.doma_txt_syntaxrule
    elif doma.doma_type == Domain.DAT:
        retval['minvalue'] = doma.doma_dat_minvalue
        retval['maxvalue'] = doma.doma_dat_maxvalue
        retval['granularity'] = doma.doma_dat_granularity
        retval['granularitytext'] = {l.lang_iso_code2: doma.displgranul(l.lang_iso_code2) for l in Language.select()}
    elif doma.doma_type == Domain.BIN:
        retval['contenttype'] = doma.doma_bin_contenttype
        retval['contenttypename'] = doma.displcontenttype()
        if doma.doma_bin_stfo_id is not None:
            retval['format'] = Storageformat().getbyid(doma.doma_bin_stfo_id).stfo_name
    elif doma.doma_type == Domain.GRP:
        retval['elements'] = domaingroupmembers(doma.doma_id)
    elif doma.doma_type == Domain.LOV:
        retval['maxlng'] = doma.doma_txt_maxlng
        retval['values'] = [{'value':d.deva_value,'sort': d.deva_sort_order, 'displ': d.deva_displ, 'descr': d.deva_descr}
                            for d in DefaultValue.select(pwhere="deva_doma_id = {}".format(doma.doma_id),
                                                         porderby="deva_sort_order")]
    retval['usedinattrs'] = [jsguid(Modelelemtype.ATTR, a.attr_id) for a in
                                Attribute.select(pwhere="attr_doma_id = {}".format(doma.doma_id))]
    retval['usedincols']= [jsguid(Modelelemtype.COLU, c.colu_id) for c in
                           Column.select(pwhere="colu_doma_id = {}".format(doma.doma_id))]
    retval['usedingrps']= [jsguid(Modelelemtype.DOMA, d.doma_id) for d in
                     Domain.select(pwhere="doma_id in (select dgrm_doma_id_group from domaingroup_members where dgrm_doma_id_member = {})"
                                            .format(doma.doma_id))]
    retval['sourceref']= {s : Externalref.getsrcid(psrcname=s, pmodeid=doma.doma_id) for s in Externalref.getsources()}
    retval['refindocuments'] = [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=doma.doma_id)]
    retval['refbyorgunits'] = [jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=doma.doma_id)]

    return retval

def domains2js():
    domas = {jsguid(Modelelemtype.DOMA, d.doma_id):domain2js(d)
             for d in Domain.select()}
    return domas
