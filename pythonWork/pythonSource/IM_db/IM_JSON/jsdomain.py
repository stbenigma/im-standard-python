from datetime import date
from IM_JSON import *
from IM_OBJECTS import *


def domaingroupmembers(pdomaid):
    return [{'name': dg.dgrm_name
            ,'mandatory': Boolean.str2bool(dg.dgrm_is_mandatory)
            , 'domain': jsguid(Modelelemtype.DOMA, dg.dgrm_doma_id_member)
            , 'descr': dg.dgrm_descr
            ,'uc': dg.dgrm_uc
             ,'dc': dg.dgrm_dc
            ,'um': dg.dgrm_um
            ,'dm': dg.dgrm_dm}
            for dg in DomaingroupMember.select(pwhere="dgrm_doma_id_group={}".format(pdomaid))
            ]

def domaingroupmembers2sql(pmodel:JSModel,pdomaid,pelements):
    for jelem in pelements:
        dgrm =DomaingroupMember()
        dgrm.dgrm_uc = 'sys'
        dgrm.dgrm_dc = date.today()
        dgrm.dgrm_name = jelem['name']
        dgrm.dgrm_descr = jelem['descr']
        dgrm.dgrm_is_mandatory = Boolean.bool2str(jelem['mandatory'])
        dgrm.dgrm_doma_id_group = pdomaid
        dgrm.dgrm_doma_id_member = jsguid2id(jelem['domain'])
        dgrm.dgrm_uc = jelem['uc']
        dgrm.dgrm_dc = jelem['dc']
        dgrm.dgrm_um = jelem['um']
        dgrm.dgrm_dm = jelem['dm']
        try:
            dgrm.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=list(jelem))
    #for
    return


def defaultvalues2sql(pmodel:JSModel, pdomaid, pvalues):
    """'value':d.deva_value,'sort': d.deva_sort_order
                            , 'displ': d.deva_displ, 'descr': d.deva_descr
                             ,'uc': d.deva_uc, 'dc': d.deva_dc
                             ,'um' : d.deva_um, 'dm': d.deva_dm"""
    for val in pvalues:
        deva = DefaultValue()
        deva.deva_doma_id = pdomaid
        deva.deva_sort_order = val['sort']
        deva.deva_value = val['value']
        deva.deva_displ = val['displ']
        deva.deva_descr = val['descr']
        deva.deva_uc = val['uc']
        deva.deva_dc = val['dc']
        deva.deva_um = val['um']
        deva.deva_dm = val['dm']
        try:
            deva.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=val)


def domelements(pelems:list=None):
    def domelement(pentries: list = None):
        model = ["name", "mandatory", "domain", "descr"
            , "uc", "dc", "um", "dm"
                 ]
        if pentries is None:
            return fillmodel(pmodel=model, pentries=['' for idx in range(len(model))])
        else:
            return fillmodel(pmodel=model, pentries=pentries)
        # fi
    #

    if pelems is None:
        return [domelement()]
    else:
        return pelems

def domvalues(pvalues:list=None):
    def domvalue(pentries: list = None):
        model = ["value", "sort", "displ", "descr"
            , "uc", "dc", "um", "dm"
                 ]
        if pentries is None:
            return fillmodel(pmodel=model, pentries=['' for idx in range(len(model))])
        else:
            return fillmodel(pmodel=model, pentries=pentries)
        # fi
    #

    if pvalues is None:
        return [domvalue()]
    else:
        return [domvalue(pentries=[d.deva_value, d.deva_sort_order, d.deva_displ, d.deva_descr
                                    , d.deva_uc, d.deva_dc, d.deva_um, d.deva_dm])
                for d in pvalues
                ]

def domain2js(pdoma):
    model = ['name', 'descr'
        , 'origin','interfaceid' 
        ,'interface+' , 'basedatatype+'
        , 'type', 'displdatatype+'
        , 'datatypestr+', 'datatypeid' 
        , 'uc', 'um', 'dc', 'dm'
        ,'minvalue','maxvalue'
        ,'totaldigits','fractdigits'
        ,'roundvalue'
        ,'unit','unitid'
        ,'maxlng','syntaxrule'
        ,'granularity','granularitytext+'
        ,'contenttype','contenttypename+'
        ,'format+','formatid'
        ,'elements','values'
        ,'usedinattrs+', 'usedincols+'
        ,'usedingrps+','sourceref'
        ,'refindocuments+','refbyorgunits+'
        ]
    if pdoma is None:
        retval = fillmodel(pmodel=model
                           ,pentries=[multilangtext(),multilangtext()
                                     , '','','',''
                                    ,'',multilangtext(),'',''
                                     ,'','','',''
                                     ,'','','',''
                                    ,''
                                     ,'','','',''
                                     ,'',multilangtext(),'',''
                                     ,'',''
                                     ,domelements(),domvalues()
                                     ,reflist(),reflist()
                                     ,reflist(),sourceref()
                                     ,reflist(),reflist()
                                    ]
                           )
    else:
        retval = fillmodel(pmodel=model
                           ,pentries=[multilangtext(pdoma.doma_name_L),multilangtext(pdoma.doma_descr_L)
                                     , pdoma.doma_origin,jsguid(Modelelemtype.INTF, pdoma.doma_intf_id)
                                    ,None if pdoma.doma_intf_id is None else Interface().getbyid(pdoma.doma_intf_id).getname()
                                        ,None if pdoma.doma_daty_id is None else Datatype().getbyid(pdoma.doma_daty_id).daty_name
                                    ,pdoma.doma_type
                                    ,multilangtext({l.lang_iso_code2: pdoma.displdatatype(l.lang_iso_code2) for l in Language.select()})
                                    ,pdoma.typestring(),jsguid(Modelelemtype.DATY, pdoma.doma_daty_id)
                                     ,pdoma.doma_uc,pdoma.doma_um,pdoma.doma_dc,pdoma.doma_dm
                                     ,pdoma.doma_num_minvalue if pdoma.doma_type == Domain.NUM else pdoma.doma_dat_minvalue
                                        ,pdoma.doma_num_maxvalue if pdoma.doma_type == Domain.NUM else pdoma.doma_dat_maxvalue
                                    ,pdoma.doma_num_total_digits,pdoma.doma_num_fract_digits
                                    ,pdoma.doma_num_round_value
                                     ,None if pdoma.doma_num_phyu_id is None else PhysicalUnit().getbyid(pdoma.doma_num_phyu_id).phyu_name
                                          ,jsguid(Modelelemtype.PHYU,pdoma.doma_num_phyu_id)
                                    ,pdoma.doma_txt_maxlng ,pdoma.doma_txt_syntaxrule
                                     ,pdoma.doma_dat_granularity,multilangtext({l.lang_iso_code2: pdoma.displgranul(l.lang_iso_code2) for l in Language.select()})
                                      ,pdoma.doma_bin_contenttype,pdoma.displcontenttype()
                                     ,None if pdoma.doma_bin_stfo_id is None else Storageformat().getbyid(pdoma.doma_bin_stfo_id).stfo_name
                                        ,jsguid(Modelelemtype.STFO,pdoma.doma_bin_stfo_id)
                                     ,domelements(domaingroupmembers(pdoma.doma_id))
                                        ,domvalues(DefaultValue.select(pwhere="deva_doma_id = {}".format(pdoma.doma_id),
                                                             porderby="deva_sort_order")
                                                   )
                                     ,reflist([jsguid(Modelelemtype.ATTR, a.attr_id)
                                                for a in Attribute.select(pwhere="attr_doma_id = {}".format(pdoma.doma_id))])
                                        ,reflist([jsguid(Modelelemtype.COLU, c.colu_id) for c in Column.select(pwhere="colu_doma_id = {}".format(pdoma.doma_id))])
                                     ,reflist([jsguid(Modelelemtype.DOMA, d.doma_id)
                                                    for d in Domain.select(pwhere="""doma_id in (select dgrm_doma_id_group 
                                                                                    from domaingroup_members 
                                                                                    where dgrm_doma_id_member = {})"""
                                                .format(pdoma.doma_id))])
                                    ,sourceref(Externalref.getsrcinfo(pmodeid=pdoma.doma_id))
                                     ,reflist([jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=pdoma.doma_id)])
                                    ,reflist([jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=pdoma.doma_id)])
                                      ]
                            )
        if pdoma.doma_type == Domain.NUM:
            for rm in ["maxlng","syntaxrule","granularity","granularitytext+","contenttype","contenttypename+"
                        ,"format+","formatid","elements","values"
                       ]:
                del retval[rm]
        elif pdoma.doma_type == Domain.TXT:
            for rm in ["minvalue","maxvalue","totaldigits","fractdigits","roundvalue","unit","unitid"
                        ,"granularity","granularitytext+","contenttype","contenttypename+"
                        ,"format+","formatid","elements","values"
                       ]:
                del retval[rm]
        elif pdoma.doma_type == Domain.DAT:
            for rm in ["maxlng","syntaxrule"
                        ,"totaldigits","fractdigits","roundvalue","unit","unitid"
                        ,"contenttype","contenttypename+"
                        ,"elements","values"
                       ]:
                del retval[rm]
        elif pdoma.doma_type == Domain.BIN:
            for rm in ["maxlng","syntaxrule"
                        ,"minvalue","maxvalue","totaldigits","fractdigits","roundvalue","unit","unitid"
                        ,"granularity","granularitytext+"
                        ,"elements","values"
                       ]:
                del retval[rm]
        elif pdoma.doma_type == Domain.GRP:
            for rm in ["maxlng","syntaxrule"
                        ,"minvalue","maxvalue","totaldigits","fractdigits","roundvalue","unit","unitid"
                        ,"granularity","granularitytext+","contenttype","contenttypename+"
                        ,"format+","formatid","values"
                       ]:
                del retval[rm]
        elif pdoma.doma_type == Domain.LOV:
            for rm in ["syntaxrule"
                        ,"minvalue","maxvalue","totaldigits","fractdigits","roundvalue","unit","unitid"
                        ,"granularity","granularitytext+","contenttype","contenttypename+"
                        ,"format+","formatid","elements"
                       ]:
                del retval[rm]
        # fi
    # fi

    return retval

def domains2js(pemptymodel):
    if pemptymodel:
        domas = {jsguid(Modelelemtype.DOMA, '0000'):domain2js(None)}
    else:
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
        doma.doma_intf_id = jsguid2id(optionalvalue(jelem,'interfaceid'))
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
        try:
            domaid = doma.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=[jid] + list(jelem))
            continue

        if doma.doma_type == Domain.LOV:
            defaultvalues2sql(pmodel=pmodel,pdomaid=domaid, pvalues=jelem["values"])

        inslgtx(pmodeid=domaid,pmodel=pmodel,pattr=Languagetext.DOMA_NAME,ptexts=jelem['name'])
        inslgtx(pmodeid=domaid,pmodel=pmodel,pattr=Languagetext.DOMA_DESCR,ptexts=jelem['descr'])
        inssourceref(pmodel = pmodel,pmodeid=domaid, psources=jelem["sourceref"])
    return

"""transfer references and subtypes"""
def domarefs2sql(pmodel:JSModel):
    for jid,jelem in pmodel.jsmodel['domains'].items():
        if jelem['type'] == Domain.GRP:
            domaingroupmembers2sql(pmodel=pmodel, pdomaid=jsguid2id(jid), pelements=jelem["elements"])
        #fi
    #for
    return
