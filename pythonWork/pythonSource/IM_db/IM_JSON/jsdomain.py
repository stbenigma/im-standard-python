from IM_OBJECTS import *
from IM_JSON import jsguid,inssourceref,jsguid2id,inslgtx,JSModel,optionalvalue
from datetime import date

"""      "DOMA11860": {
     "name": {
        "de": "Zeitpunkt",
     },
     "descr": {
        "de": null,
        "en": null,
     },
     "origin": "DOM",
     "basedatatype": "Timestamp",
     "type": "TXT",
     "displdatatype": {
        "de": "Text",
     },
     "datatypestr": "Timestamp",
     "uc": "stb",
     "um": null,
     "dc": "2018-05-17 16:19:03 UTC",
     "dm": null,
     "maxlng": null,
     "syntaxrule": null,
     "usedinattrs": [],
     "usedincols": [],
     "usedingrps": [],
     "sourceref": {
        "ODM": "0AD80E26-0F5C-D068-29EA-4740A04582AE"
     },
     "refindocuments": [],
     "refbyorgunits": []"""

def domaingroupmembers(pdomaid):
    return [{'name': dg.dgrm_name
            ,'mandatory': dg.dgrm_is_mandatory
            , 'domain': jsguid(Modelelemtype.DOMA, dg.dgrm_doma_id_member)
            , 'descr': dg.dgrm_descr}
            for dg in DomaingroupMember.select(pwhere="dgrm_doma_id_group={}".format(pdomaid))
            ]

def domaingroupmembers2sql(pdomaid,pelements):
    for jelem in pelements:
        dgrm =DomaingroupMember()
        dgrm.dgrm_uc = 'sys'
        dgrm.dgrm_dc = date.today()
        dgrm.dgrm_name = jelem['name']
        dgrm.dgrm_descr = jelem['descr']
        dgrm.dgrm_is_mandatory = Boolean.str2bool(jelem['mandatory'])
        dgrm.dgrm_doma_id_group = pdomaid
        dgrm.dgrm_doma_id_member = jsguid2id(jelem['domain'])
        try:
            dgrm.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=list(jelem))
    #for


def domain2js(doma):
    retval = {'name': doma.doma_name_L
        , 'descr': doma.doma_descr_L
        , 'origin': doma.doma_origin
        , 'basedatatype': None if doma.doma_daty_id is None else Datatype().getbyid(doma.doma_daty_id).daty_name
        , 'type': doma.doma_type
        , 'displdatatype': {l.lang_iso_code2:doma.displdatatype(l.lang_iso_code2) for l in Language.select()}
        , 'datatypestr': doma.typestring()
        , 'datatypeid' : jsguid(Modelelemtype.DATY,doma.doma_daty_id)
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
            retval['unitid'] = None
        else:
            retval['unit'] = PhysicalUnit().getbyid(doma.doma_num_phyu_id).phyu_name
            retval['unitid'] = jsguid(Modelelemtype.PHYU,doma.doma_num_phyu_id)
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
        retval['format'] = None
        retval['formatid'] = None
        if doma.doma_bin_stfo_id is not None:
            retval['format'] = Storageformat().getbyid(doma.doma_bin_stfo_id).stfo_name
            retval['formatid'] = jsguid(Modelelemtype.STFO,doma.doma_bin_stfo_id)
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
    retval['sourceref']= Externalref.getsrcinfo(pmodeid=doma.doma_id)
    retval['refindocuments'] = [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=doma.doma_id)]
    retval['refbyorgunits'] = [jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=doma.doma_id)]

    return retval

def domains2js():
    domas = {jsguid(Modelelemtype.DOMA, d.doma_id):domain2js(d)
             for d in Domain.select()}
    return domas

def domains2sql(pmodel:JSModel):
    for jid,jelem in pmodel.jsmodel['domains'].items():
        doma = Domain()
        doma.doma_id = jsguid2id(jid)
        doma.doma_uc = jelem['uc']
        doma.doma_dc = jelem['dc']
        doma.doma_um = jelem['um']
        doma.doma_dm = jelem['dm']
        doma.doma_type = jelem['type']
        doma.doma_name = jelem['name'][pmodel.modellanguage()]
        doma.doma_descr = jelem['descr'][pmodel.modellanguage()]
        doma.doma_origin = jelem['origin']
        doma.doma_daty_id = jsguid2id(optionalvalue(jelem,'datatypeid'))
        doma.doma_num_minvalue = None if doma.doma_type != Domain.NUM else optionalvalue(jelem,'minvalue')
        doma.doma_num_maxvalue = None if doma.doma_type != Domain.NUM else optionalvalue(jelem,'maxvalue')
        doma.doma_num_total_digits = optionalvalue(jelem,'totaldigits')
        doma.doma_num_fract_digits = optionalvalue(jelem,'fractdigits')
        doma.doma_num_round_value = optionalvalue(jelem,'roundvalue')
        doma.doma_phyu_id = jsguid2id(optionalvalue(jelem,'unitid'))
        doma.doma_txt_maxlng = optionalvalue(jelem,'maxlng')
        doma.doma_txt_syntaxrule = optionalvalue(jelem,'syntaxrule')
        doma.doma_dat_minvalue = None if doma.doma_type != Domain.DAT else optionalvalue(jelem,'minvalue')
        doma.doma_dat_maxvalue = None if doma.doma_type != Domain.DAT else optionalvalue(jelem,'maxvalue')
        doma.doma_dat_granularity = optionalvalue(jelem,'granularity')
        doma.doma_bin_contenttype = optionalvalue(jelem,'contenttype')
        doma.doma_bin_stfo_id = jsguid2id(optionalvalue(jelem,'formatid'))
        doma.doma_txt_maxlng = optionalvalue(jelem,'maxlng')
        jelem['elements'] = domaingroupmembers(doma.doma_id)
        try:
            domaid = doma.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=[jid] + list(jelem))
            continue

        if doma.doma_type == Domain.LOV:
            domaingroupmembers2sql(pdomaid=domaid, pelements=jelem["elements"])
        inslgtx(pmodeid=domaid,pmodel=pmodel,pattr=Languagetext.DOMA_NAME,ptexts=jelem['name'])
        inslgtx(pmodeid=domaid,pmodel=pmodel,pattr=Languagetext.DOMA_DESCR,ptexts=jelem['descr'])
        inssourceref(pmodel = pmodel,pmodeid=domaid, psources=jelem["sourceref"])
    return

"""transfer references and subtypes"""
def domarefs2sql(pmodel):
    #    insudp(pmodeid=entiid, pudps=jenti["userdefprop"])
    return
