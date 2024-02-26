from SSOT_db.IM_JSON import *
from SSOT_db.IM_OBJECTS import *
from SSOT_infra import transl


def domaingroupmembers(pdomaid):
    return [{'name': dg.dgrm_name
                , 'mandatory': Boolean.str2bool(dg.dgrm_is_mandatory)
                , 'domain': jsguid(Modelelemtype.DOMA, dg.dgrm_doma_id_member)
                , 'descr': dg.dgrm_descr
                , 'uc': dg.dgrm_uc
                , 'dc': dg.dgrm_dc
                , 'um': dg.dgrm_um
                , 'dm': dg.dgrm_dm}
            for dg in DomaingroupMember.select(pwhere=("dgrm_doma_id_group=?", pdomaid))
            ]


def domaingroupmembers2sql(presult: Mergeresult, pgrpdomaid, pelements):
    inscnt = 0
    delcnt = DomaingroupMember.delete(pwhere=("dgrm_doma_id_group = ?", pgrpdomaid))
    for jelem in pelements:
        dgrm = DomaingroupMember()
        dgrm.dgrm_name = jelem['name']
        dgrm.dgrm_descr = jelem['descr']
        dgrm.dgrm_is_mandatory = Boolean.bool2str(jelem['mandatory'])
        dgrm.dgrm_doma_id_group = pgrpdomaid
        dgrm.dgrm_doma_id_member = presult.keytransl(jelem['domain'])
        dgrm.dgrm_uc = jelem['uc']
        dgrm.dgrm_dc = jelem['dc']
        dgrm.dgrm_um = jelem['um']
        dgrm.dgrm_dm = jelem['dm']
        try:
            dgrm.insert()
            inscnt += 1
        except Exception as err:
            presult.markdberror(perr=err, pelem=list(jelem))
    # for
    presult.addinscnt(max(0, (inscnt - delcnt)), f"Domaingroupmembers for domain {pgrpdomaid}")
    presult.adddelcnt(max(0, (delcnt - inscnt)), f"Domaingroupmembers for domain {pgrpdomaid}")
    return


def js2deva(pdomaid, pelem):
    deva = DefaultValue()
    deva.deva_doma_id = pdomaid
    deva.deva_sort_order = pelem['sort']
    deva.deva_value = pelem['value']
    deva.deva_displ = pelem['displ']
    deva.deva_descr = pelem['descr']
    deva.deva_uc = pelem['uc']
    deva.deva_dc = pelem['dc']
    deva.deva_um = pelem['um']
    deva.deva_dm = pelem['dm']
    return deva


def defaultvalues2sql(presult: Mergeresult, pdomaid, pvalues):
    """'value':d.deva_value,'sort': d.deva_sort_order
                            , 'displ': d.deva_displ, 'descr': d.deva_descr
                             ,'uc': d.deva_uc, 'dc': d.deva_dc
                             ,'um' : d.deva_um, 'dm': d.deva_dm
    default values are always replaced """
    delcnt = DefaultValue.delete(pwhere=("deva_doma_id=?", str(pdomaid)))
    inscnt = 0
    for val in pvalues:
        deva = js2deva(pdomaid=pdomaid, pelem=val)
        try:
            deva.insert()
            inscnt += 1
        except Exception as err:
            presult.markdberror(perr=err, pelem=val)
    # for
    presult.addinscnt(max(0, (inscnt - delcnt)), f"Defaultvalues for domain {pdomaid}")
    presult.adddelcnt(max(0, (delcnt - inscnt)), f"Defaultvalues for domain {pdomaid}")
    return

DOMAINELEMENTMODEL=["name", "mandatory", "domain", "descr"
            , "uc", "dc", "um", "dm"
                 ]
def domelements(pelems: list = None):
    def domelement(pentries: list = None):
        if pentries is None:
            return fillmodel(pmodel=DOMAINELEMENTMODEL,
                             pentries=['' for idx in range(len(DOMAINELEMENTMODEL))])
        else:
            return fillmodel(pmodel=DOMAINELEMENTMODEL,
                             pentries=pentries)
        # fi

    #

    if pelems is None:
        return [domelement()]
    else:
        return pelems

DOMAINVALUEMODEL=["value", "sort", "displ", "descr"
            , "uc", "dc", "um", "dm",'mappedto','mappedfrom'
                 ]
def jsondomainvalue(value,sort,displ,uc, dc, **kwargs):
    domainvalues = dict()
    initjselement(domainvalues,DOMAINVALUEMODEL)
    domainvalues["value"] = value
    domainvalues["sort"] = sort
    domainvalues["uc"] = uc
    domainvalues["dc"] = dc
    domainvalues["displ"] = displ
    domainvalues["transformationsto"] = []
    domainvalues["mappedfrom"] = []

    fillargs(model=domainvalues,refmodel=DOMAINVALUEMODEL,**kwargs)
    return domainvalues

def jsondomainvaluemap(domainid,value):
    return {"domain":domainid,
                "value":value
    }
def domvalues(pvalues: list = None):
    def domvalue(pentries: list = None):
         
        if pentries is None:
            return fillmodel(pmodel=DOMAINVALUEMODEL,
                             pentries=['' for idx in range(len(DOMAINVALUEMODEL)-1)]+
                                        [jsondomainvaluemap(domainid=jsguid(Modelelemtype.DOMA,'0000')
                                                            ,value='')
                                         ])
        else:
            return fillmodel(pmodel=DOMAINVALUEMODEL,
                             pentries=pentries)
        # fi

    #

    if pvalues is None:
        return [domvalue()]
    else:
        return [domvalue(pentries=[d.deva_value, d.deva_sort_order, d.deva_displ, d.deva_descr
            , d.deva_uc, d.deva_dc, d.deva_um, d.deva_dm]+[[],[]]) #TODO translations of Lov values
                for d in pvalues
                ]

DOMAINMODEL=['name', 'descr'
        , 'origin', 'datamodel-id'
        , 'datamodel+', 'basedatatype+'
        , 'type', 'displdatatype+'
        , 'datatypestr+', 'datatypeid'
        , 'uc', 'um', 'dc', 'dm'
        , 'minvalue', 'maxvalue'
        , 'totaldigits', 'fractdigits'
        , 'roundvalue'
        , 'unit', 'unitid'
        , 'maxlng', 'syntaxrule'
        , 'granularity', 'granularitytext+'
        , 'contenttype', 'contenttypename+'
        , 'format+', 'formatid'
        , 'elements',
        'values', 'mappedto','mappedfrom'
        , 'usedinattrs+', 'usedincols+'
        , 'usedingrps+', 'sourceref'
        , 'referencedby'
             ]
def jsondomain(name:dict,descr,domtype,domorigin,uc, dc,datamodelid=None, **kwargs):
    domain = dict()
    initjselement(domain,DOMAINMODEL)
    domain["name"] = multilangtext(name)
    domain["descr"] = descr
    domain["origin"] = domorigin
    domain["type"] = domtype
    domain["datamodel-id"] = datamodelid
    domain["uc"] = uc
    domain["dc"] = dc
    domain["referencedby"] = []
    domain["userdefprops"] = dict()
    domain["examples"] = []

    fillargs(model=domain,refmodel=DOMAINMODEL,**kwargs)
    reducedoma2type(domatype=domtype,domadict=domain)
    return domain

def reducedoma2type(domatype,domadict):
    if domatype == Domain.NUM:
        for rm in ["maxlng", "syntaxrule", "granularity", "granularitytext+", "contenttype", "contenttypename+"
            , "format+", "formatid", "elements", "values", 'mappedto','mappedfrom'
                   ]:
            domadict.pop(rm,None)
    elif domatype == Domain.TXT:
        for rm in ["minvalue", "maxvalue", "totaldigits", "fractdigits", "roundvalue", "unit", "unitid"
            , "granularity", "granularitytext+", "contenttype", "contenttypename+"
            , "format+", "formatid", "elements", "values", 'mappedto','mappedfrom'
                   ]:
            domadict.pop(rm,None)
    elif domatype == Domain.DAT:
        for rm in ["maxlng", "syntaxrule"
            , "totaldigits", "fractdigits", "roundvalue", "unit", "unitid"
            , "contenttype", "contenttypename+"
            , "elements", "values", 'mappedto','mappedfrom'
                   ]:
            domadict.pop(rm,None)
    elif domatype == Domain.BIN:
        for rm in ["maxlng", "syntaxrule"
            , "minvalue", "maxvalue", "totaldigits", "fractdigits", "roundvalue", "unit", "unitid"
            , "granularity", "granularitytext+"
            , "elements", "values", 'mappedto','mappedfrom'
                   ]:
            domadict.pop(rm,None)
    elif domatype == Domain.GRP:
        for rm in ["maxlng", "syntaxrule"
            , "minvalue", "maxvalue", "totaldigits", "fractdigits", "roundvalue", "unit", "unitid"
            , "granularity", "granularitytext+", "contenttype", "contenttypename+"
            , "format+", "formatid", "values", 'mappedto','mappedfrom'
                   ]:
            domadict.pop(rm,None)
    elif domatype == Domain.LOV:
        for rm in ["syntaxrule"
            , "minvalue", "maxvalue", "totaldigits", "fractdigits", "roundvalue", "unit", "unitid"
            , "granularity", "granularitytext+", "contenttype", "contenttypename+"
            , "format+", "formatid", "elements"
                   ]:
            domadict.pop(rm,None)


def domain2js(pdoma):
    if pdoma is None:
        retval = fillmodel(pmodel=DOMAINMODEL
                           , pentries=[multilangtext(), multilangtext()
                , '', '', '', ''
                , '', multilangtext(), '', ''
                , '', '', '', ''
                , '', '', '', ''
                , ''
                , '', '', '', ''
                , '', multilangtext(), '', ''
                , '', ''
                , domelements(),
                domvalues(),[jsguid(Modelelemtype.DOMA,"0000")],[jsguid(Modelelemtype.DOMA,"0000")]
                , reflist(), reflist()
                , reflist(), sourceref()
                , reflist()
                                       ]
                           )
    else:
        retval = fillmodel(pmodel=DOMAINMODEL
                           , pentries=[multilangtext(pdoma.doma_name_l), multilangtext(pdoma.doma_descr_l)
                , pdoma.doma_origin, jsguid(Modelelemtype.DATM, pdoma.doma_datm_id)
                , None if pdoma.doma_datm_id is None else Datamodel().getbyid(pdoma.doma_datm_id).getname()
                , None if pdoma.doma_daty_id is None else Datatype().getbyid(pdoma.doma_daty_id).daty_name
                , pdoma.doma_type
                , multilangtext(
                    {l.lang_iso_code2: transl(pdoma.doma_type, l.lang_iso_code2) for l in Language.select()})
                , pdoma.typestring(), jsguid(Modelelemtype.DATY, pdoma.doma_daty_id)
                , pdoma.doma_uc, pdoma.doma_um, pdoma.doma_dc, pdoma.doma_dm
                , pdoma.doma_num_minvalue if pdoma.doma_type == Domain.NUM else pdoma.doma_dat_minvalue
                , pdoma.doma_num_maxvalue if pdoma.doma_type == Domain.NUM else pdoma.doma_dat_maxvalue
                , pdoma.doma_num_total_digits, pdoma.doma_num_fract_digits
                , pdoma.doma_num_round_value
                , None if pdoma.doma_num_phyu_id is None else PhysicalUnit().getbyid(pdoma.doma_num_phyu_id).phyu_name
                , jsguid(Modelelemtype.PHYU, pdoma.doma_num_phyu_id)
                , pdoma.doma_txt_maxlng, pdoma.doma_txt_syntaxrule
                , pdoma.doma_dat_granularity, multilangtext(
                    {l.lang_iso_code2: transl(pdoma.doma_dat_granularity, l.lang_iso_code2) for l in Language.select()})
                , pdoma.doma_bin_contenttype, transl(pdoma.doma_bin_contenttype)
                , None if pdoma.doma_bin_stfo_id is None else Storageformat().getbyid(pdoma.doma_bin_stfo_id).stfo_name
                , jsguid(Modelelemtype.STFO, pdoma.doma_bin_stfo_id)
                , domelements(domaingroupmembers(pdoma.doma_id))
                , domvalues(DefaultValue.select(pwhere=("deva_doma_id = ?", pdoma.doma_id))
                            ),[],[] #TODO mappedfrom , transformationsto
                , reflist([jsguid(Modelelemtype.ATTR, a.attr_id)
                           for a in Attribute.select(pwhere=("attr_doma_id = ?", pdoma.doma_id))])
                , reflist([jsguid(Modelelemtype.COLU, c.colu_id) for c in
                           Column.select(pwhere=("colu_doma_id = ?", pdoma.doma_id))])
                , reflist([jsguid(Modelelemtype.DOMA, d.doma_id)
                           for d in Domain.select(pwhere=("""doma_id in (select dgrm_doma_id_group 
                                                                            from domaingroup_members 
                                                                            where dgrm_doma_id_member = ?)""",
                                                          pdoma.doma_id))])
                , sourceref(Externalref.getsrcinfo(pmodeid=pdoma.doma_id))
                , [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=pdoma.doma_id)] \
                                       + [jsguid(Modelelemtype.ORGU, d[0]) for d in
                                          OragnisationalUnit.getreforgulist(pid=pdoma.doma_id)]
                                       ]
                           )
        reducedoma2type(domatype=pdoma.doma_type,domadict=retval)
        # fi
    # fi

    return retval


def domains2js(pemptymodel):
    if pemptymodel:
        domas = {jsguid(Modelelemtype.DOMA, '0000'): domain2js(None)}
    else:
        domas = {jsguid(Modelelemtype.DOMA, d.doma_id): domain2js(d)
                 for d in Domain.select()}
    return domas


def js2doma(pkey, pelem, psrcname=None, psrcid=None, pmodellang=None):
    doma = Domain(srcname=psrcname, srcid=psrcid,
         doma_id = pkey,
         doma_uc = pelem['uc'],
         doma_dc = pelem['dc'],
         doma_um = pelem['um'],
         doma_dm = pelem['dm'],
         doma_type = pelem['type'],
         doma_name = pelem['name'][pmodellang],
         doma_descr = pelem['descr'][pmodellang],
         doma_origin = pelem['origin'],
         doma_datm_id = optionalvalue(pelem, 'datamodel-id'),
         doma_daty_id = optionalvalue(pelem, 'datatypeid'),
         doma_num_minvalue = None if pelem['type'] != Domain.NUM else optionalvalue(pelem, 'minvalue'),
         doma_num_maxvalue = None if pelem['type'] != Domain.NUM else optionalvalue(pelem, 'maxvalue'),
         doma_num_total_digits = optionalvalue(pelem, 'totaldigits'),
         doma_num_fract_digits = optionalvalue(pelem, 'fractdigits'),
         doma_num_round_value = optionalvalue(pelem, 'roundvalue'),
         doma_num_phyu_id = optionalvalue(pelem, 'unitid'),
         doma_txt_maxlng = optionalvalue(pelem, 'maxlng'),
         doma_txt_syntaxrule = optionalvalue(pelem, 'syntaxrule'),
         doma_dat_minvalue = None if pelem['type'] != Domain.DAT else optionalvalue(pelem, 'minvalue'),
         doma_dat_maxvalue = None if pelem['type'] != Domain.DAT else optionalvalue(pelem, 'maxvalue'),
         doma_dat_granularity = optionalvalue(pelem, 'granularity'),
         doma_bin_contenttype = optionalvalue(pelem, 'contenttype'),
         doma_bin_stfo_id = optionalvalue(pelem, 'formatid'))
    return doma


def domains2sql(presult: Mergeresult, pjson: JSModel, pwithextsrcref):
    fromjson2db(presult=presult, pjson=pjson, pelemtype=Modelelemtype.DOMA, pjs2obj=js2doma,
               pwithextsrcref=pwithextsrcref)

    for jid, jelem in pjson.getelements(pelemtype=Modelelemtype.DOMA).items():
        dbdomaid = presult.keytransl(jid)
        if dbdomaid == 0: continue

        if jelem['type'] == Domain.LOV:
            defaultvalues2sql(presult=presult, pdomaid=dbdomaid, pvalues=jelem["values"])

        elif jelem['type'] == Domain.GRP:
            grpdomaid=presult.keytransl(jid)
            if grpdomaid == 0 : continue
            domaingroupmembers2sql(presult=presult, pgrpdomaid=grpdomaid
                                   , pelements=jelem["elements"])
        # fi
        replacelgtx(presult=presult, pmodeid=dbdomaid, pattr=Languagetext.DOMA_NAME, ptexts=jelem['name'])
        replacelgtx(presult=presult, pmodeid=dbdomaid, pattr=Languagetext.DOMA_DESCR, ptexts=jelem['descr'])
        insreferences(presult=presult, pmodeid=dbdomaid, prefs=jelem['referencedby'])
        inssourceref(presult=presult, pmodeid=dbdomaid, psources=jelem["sourceref"])
    return
