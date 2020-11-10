# -*- coding: latin-1 -*-
import json

from IM_DB import dbConnect, parameters, logmessages
from IM_OBJECTS import *
from mystring import nvl

EMPTYJSONFILE = 'emptyjsonmodel'


# Main Programm
def getJSONfile(pfilename):
    with open(pfilename, 'r') as handle:
        model = json.load(handle)
    return model


def elemrep(elers):
    if elers is None: return {}
    return {'index': elers.eler_index
        , 'pos_x': elers.eler_position_x
        , 'pos_y': elers.eler_position_y
        , 'width': elers.eler_width
        , 'height': elers.eler_height
        , 'opacity': elers.eler_opacity
        , 'color': elers.eler_color
        , 'marginwidth': elers.eler_marginwidth
        , 'marginopacity': elers.eler_marginopacity
        , 'margincolor': elers.eler_margincolor
        , 'fontsize': elers.eler_fontsize
        , 'fontcolor': elers.eler_fontcolor
            }


anker = lambda n, i: n + str(i)


def entities():
    entis = {anker(Modelelemtype.ENTI, e.enti_id):
                 {'name': e.enti_name_L
                     , 'shortname': nvl(e.enti_short_name)
                     , 'descr': e.enti_descr_L
                     , 'tooltip': e.enti_tooltip_L
                     , 'exptuple#': e.enti_exp_tuplecnt
                     , 'prefix': e.enti_prefix
                     , 'subtypellevel': e.getsubtypelevel()
                     , 'uc': e.enti_uc
                     , 'dc': e.enti_dc
                     , 'um': e.enti_um
                     , 'dm': e.enti_dm
                     , 'synonyms': [s.syno_name_L for s in e.getsynonyms()]
                     , 'sourceref': {s: Externalref.getsrcid(psrcname=s, pmodeid=e.enti_id) for s in
                                     Externalref.getsources()}
                     , 'supertypes': [anker(Modelelemtype.ENTI, es.enti_id) for es in e.getparents()]
                     , 'roles': [anker(Modelelemtype.ENTI, es.enti_id) for es in e.getchildren(ptype=Relation.ISAROLE)]
                     ,
                  'subtypes': [anker(Modelelemtype.ENTI, es.enti_id) for es in e.getchildren(ptype=Relation.ISASUBTYPE)]
                     , 'attributes': [anker(Modelelemtype.ATTR, a.attr_id) for a in e.getattributes()]
                     ,
                  'relations': [anker(Modelelemtype.RELA, r.rela_id) for r in Relation.getbyentity(pentiid=e.enti_id)]
                     ,
                  'inarcs': [anker(Modelelemtype.ARCS, a.arcs_id) for a in Arc.select(pwhere="arcs_enti_id = {}".format(e.enti_id))]
                     ,
                  'refindocuments': [anker(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=e.enti_id)]
                     , 'userdefprop': {
                     t[0]: {g[1]: {u.udpr_name: Userdefpropvalue.udpvalue(pudprid=u.udpr_id, pmodeid=e.enti_id)
                                   for u in Userdefprop.getudps(ptheme=t[0], pgroup=g[1], pmeltname=Modelelemtype.ENTI)}
                            for g in Userdefprop.grouplist(pudptheme=t[0], pmelttype=Modelelemtype.ENTI)}
                     for t in Userdefprop.themelist(pmelttype=Modelelemtype.ENTI)}

                     , 'tablesmapped': {s.getname(): [anker(Modelelemtype.TABL, t.tabl_id) for t in
                                                      TablEntiMap.gettabllist(pentiid=e.enti_id, pintfid=s.getid())]
                                        for s in Schnittstelle.getmapped(pentiid=e.enti_id)}
                     ,
                  'diagrams': [anker(Modelelemtype.DIAG, d.diag_id) for d in Diagram.getdiagrams(pmodeid=e.enti_id)]
                  } for e in Entity.select()}
    return entis


def defattr(attr):
    retval = {'techname': attr.attr_tech_name
        , 'name': attr.attr_displ_name_L
        , 'seq': attr.attr_displ_seq
        , 'entity': anker(Modelelemtype.ENTI, attr.attr_enti_id)
        , 'domain': anker(Modelelemtype.DOMA, attr.attr_doma_id)
        , 'descriptive': Boolean.str2bool(attr.attr_is_descriptive)
        , 'mandatory': Boolean.str2bool(attr.attr_is_mandatory)
        , 'historicised': Boolean.str2bool(attr.attr_is_historicised)
        , 'repeated': Boolean.str2bool(attr.attr_is_repeated)
        , 'translated': Boolean.str2bool(attr.attr_is_translated)
        , 'encrypted': Boolean.str2bool(attr.attr_is_encrypted)
        , 'descr': attr.attr_descr_L
        , 'uc': attr.attr_uc
        , 'dc': attr.attr_dc
        , 'um': attr.attr_um
        , 'dm': attr.attr_dm
        , 'sourceref': {s: Externalref.getsrcid(psrcname=s, pmodeid=attr.attr_id) for s in Externalref.getsources()}
        , 'keys': [anker(Modelelemtype.KEYS, k.keys_id) for k in attr.getkeys()]
        , 'refindocuments': [anker(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=attr.attr_id)]
        , 'userdefprop': {t[0]: {g[1]: {u.udpr_name: Userdefpropvalue.udpvalue(pudprid=u.udpr_id, pmodeid=attr.attr_id)
                                        for u in
                                        Userdefprop.getudps(ptheme=t[0], pgroup=g[1], pmeltname=Modelelemtype.ATTR)}
                                 for g in Userdefprop.grouplist(pudptheme=t[0], pmelttype=Modelelemtype.ATTR)}
                          for t in Userdefprop.themelist(pmelttype=Modelelemtype.ATTR)}
        , 'columnsmapped': {
            s.getname(): [anker(Modelelemtype.COLU, c.scha_id) for c in
                          AttrTransf.getcolulist(pattrid=attr.attr_id, pintfid=s.getid())]
            for s in Schnittstelle.getmapped(pattrid=attr.attr_id)}
        , 'diagrams': [anker(Modelelemtype.DIAG, d.diag_id) for d in Diagram.getdiagrams(pmodeid=attr.attr_id)]
              }
    doma = Domain().getbyid(attr.attr_doma_id)
    retval['basedatatype'] = None if doma.doma_daty_id is None else Datatype().getbyid(
        doma.doma_daty_id).daty_name
    retval['type'] = doma.doma_type
    if (Domain().getbyid(attr.attr_doma_id).doma_type == Domain.GRP):
        retval['memberattrs'] = domaingroupmembers(pdomaid=attr.attr_doma_id)
    return retval


def attributes():
    attrs = {anker(Modelelemtype.ATTR, a.attr_id): defattr(a) for a in Attribute.select()}
    return attrs


def domaingroupmembers(pdomaid):
    return {dg.dgrm_name: {'mandatory': dg.dgrm_is_mandatory
        , 'domain': anker(Modelelemtype.DOMA, dg.dgrm_doma_id_member)
        , 'descr': dg.dgrm_descr
                           }
            for dg in DomaingroupMember.select(pwhere="dgrm_doma_id_group={}".format(pdomaid))
            }


def defdomain(doma):
    retval = {'name': doma.doma_name_L
        , 'descr': doma.doma_descr_L
        , 'origin': doma.doma_origin
        , 'basedatatype': None if doma.doma_daty_id is None else Datatype().getbyid(doma.doma_daty_id).daty_name
        , 'type': doma.doma_type
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
        if doma.doma_num_phyu_id is not None:
            retval['unit'] = PhysicalUnit().getbyid(doma.doma_num_phyu_id).phyu_name
    elif doma.doma_type == Domain.TXT:
        retval['maxlng'] = doma.doma_txt_maxlng
        retval['syntaxrule'] = doma.doma_txt_syntaxrule
    elif doma.doma_type == Domain.DAT:
        retval['minvalue'] = doma.doma_dat_minvalue
        retval['maxvalue'] = doma.doma_dat_maxvalue
        retval['granularity'] = doma.doma_dat_granularity
    elif doma.doma_type == Domain.BIN:
        retval['contenttype'] = doma.doma_bin_contenttype
        if doma.doma_bin_stfo_id is not None:
            retval['format'] = Storageformat().getbyid(doma.doma_bin_stfo_id).stfo_name
    elif doma.doma_type == Domain.GRP:
        retval['elements'] = domaingroupmembers(doma.doma_id)
    elif doma.doma_type == Domain.LOV:
        retval['values'] = [{d.deva_value: {'sort': d.deva_sort_order, 'displ': d.deva_displ, 'descr': d.deva_descr}}
                            for d in DefaultValue.select(pwhere="deva_doma_id = {}".format(doma.doma_id),
                                                         porderby="deva_sort_order")]
    retval['usedinattrs'] = [anker(Modelelemtype.ATTR, a.attr_id) for a in
                                Attribute.select(pwhere="attr_doma_id = {}".format(doma.doma_id))]
    retval['usedincols']= [anker(Modelelemtype.COLU, c.scha_id) for c in
                     Schnittstelleattr.select(pwhere="scha_doma_id = {}".format(doma.doma_id))]
    retval['sourceref']= {s : Externalref.getsrcid(psrcname=s, pmodeid=doma.doma_id) for s in Externalref.getsources()}
    retval['refindocuments'] = [anker(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=doma.doma_id)]

    return retval

def arcs():
    arcs = {anker(Modelelemtype.ARCS,a.arcs_id): {
        'name':a.arcs_name
        ,'entity': anker(Modelelemtype.ENTI,a.arcs_enti_id)
        ,'relations': [anker(Modelelemtype.RELA,r.rela_id) for r in a.getrelalist()]
        ,'uc': a.arcs_uc
        ,'dc': a.arcs_dc
        ,'um': a.arcs_um
        ,'dm': a.arcs_dm
        }
            for a in Arc.select()
            }
    return arcs

def doamains():
    domas = {anker(Modelelemtype.DOMA, d.doma_id):defdomain(d)
             for d in Domain.select()}
    return domas


def keys():
    keys = {anker(Modelelemtype.KEYS, k.keys_id):
                {'key': {'name': k.keys_name
                    , 'entity': anker(Modelelemtype.ENTI, k.keys_enti_id)
                    , 'uc': k.keys_uc
                    , 'dc': k.keys_dc
                    , 'um': k.keys_um
                    , 'dm': k.keys_dm
                         }
                    ,
                 'sourceref': {s: Externalref.getsrcid(psrcname=s, pmodeid=k.keys_id) for s in Externalref.getsources()}
                , 'key-elements': [anker(Modelelemtype.RELA , ke.kele_rela_id) if ke.kele_rela_id is not None
                                   else anker(Modelelemtype.ATTR , ke.kele_attr_id)
                                   for ke in k.getkeyelements()]
                 } for k in Key.select()}
    return keys


def relation(prela):
    if prela is None: return {}
    return {
               'name': prela.rela_name
               , 'type': prela.rela_type
               , 'from-to': {
                   'enti': anker(Modelelemtype.ENTI, prela.rela_enti_id_from)
                   , 'arc': None if prela.rela_arcs_id_from is None else anker(Modelelemtype.ARCS, prela.rela_arcs_id_from)
                   , 'assoc': prela.rela_assoc_from_to_L
                   , 'maptype': prela.rela_maptype_from_to
                   , 'hist': Boolean.str2bool(prela.rela_hist_from_to)
                   , 'mandatory': Boolean.str2bool(prela.rela_mandatory_from_to)
                }
                , 'to-from-':{
                    'enti': anker(Modelelemtype.ENTI, prela.rela_enti_id_to)
                    , 'arc': None if prela.rela_arcs_id_to is None else anker(Modelelemtype.ARCS, prela.rela_arcs_id_to)
                    , 'assoc': prela.rela_assoc_to_from_L
                    , 'maptype': prela.rela_maptype_to_from
                    , 'hist': Boolean.str2bool(prela.rela_hist_to_from)
                    , 'mandatory': Boolean.str2bool(prela.rela_mandatory_to_from)
                }
                ,'uc': prela.rela_uc
                ,'dc': prela.rela_dc
                ,'um': prela.rela_um
                ,'dm': prela.rela_dm
    }

def relations():
    relas = {anker(Modelelemtype.RELA, r.rela_id): relation(r)
             for r in Relation.select()}
    return relas

def documents():
    docus = {anker(Modelelemtype.DOCU, d.docu_id):
        {
            'name': d.docu_name
            , 'reference': d.docu_reference
            , 'content': d.docu_content
            , 'format': None if d.docu_stfo_id is None else Storageformat().getbyid(d.docu_stfo_id).stfo_name
            , 'parent': anker(Modelelemtype.DOCU, d.docu_docu_id)
            ,'referencedfrom':[anker(m.mode_type,m.mode_id) for m in d.getrefmodes()]
        }
        for d in Document.select()}
    return docus

def relarep(prelarep):
    if prelarep is None: return {}
    return {'linewidth': prelarep.relr_linewidth
        , 'linecolor': prelarep.relr_linecolor
        , 'lineopacity': prelarep.relr_lineopacity
        , 'startedge': prelarep.relr_startedge
        , 'startposition': prelarep.relr_startposition
        , 'start_connector': prelarep.relr_start_connector
        , 'starttext_angle': prelarep.relr_starttext_angle
        , 'starttext_distance': prelarep.relr_starttext_distance
        , 'starttext_x': prelarep.relr_starttext_x
        , 'starttext_y': prelarep.relr_starttext_y
        , 'starttext_width': prelarep.relr_starttext_width
        , 'starttext_height': prelarep.relr_starttext_height
        , 'endedge': prelarep.relr_endedge
        , 'endposition': prelarep.relr_endposition
        , 'end_connector': prelarep.relr_end_connector
        , 'endtext_angle': prelarep.relr_endtext_angle
        , 'endtext_distance': prelarep.relr_endtext_distance
        , 'endtext_x': prelarep.relr_endtext_x
        , 'endtext_y': prelarep.relr_endtext_y
        , 'endtext_width': prelarep.relr_endtext_width
        , 'endtext_height': prelarep.relr_endtext_height
        , 'fontcolor': prelarep.relr_fontsize
        , 'fontsize': prelarep.relr_fontsize
        , 'uc': prelarep.relr_uc
        , 'dc': prelarep.relr_dc
        , 'um': prelarep.relr_um
        , 'dm': prelarep.relr_dm
        , 'linesegments': {l.lise_seq: {'x': l.lise_x
            , 'y': l.lise_y
            , 'linetpye': l.lise_linetype
            , 'angle': l.lise_angle
                                        }
                           for l in prelarep.getlinesegments()}
            }

def diagrams():
    diags = {anker(Modelelemtype.DIAG, d.diag_id):
        {
            'name': d.diag_name
            , 'legend': {'x': d.diag_legendx
                , 'y': d.diag_legendy
                , 'model': parameters.odmModelName()
                         }
            , 'type': Diagramtype().getbyid(d.diag_diat_id).getname()
            , 'width': d.diagwidth()
            , 'height': d.diagheight()
            , 'uc': d.diag_uc
            , 'dc': d.diag_dc
            , 'um': d.diag_um
            , 'dm': d.diag_dm
            , 'elements': {mt.melt_name.lower():
                               {anker(mt.melt_shortname, eler.eler_mode_id):
                                    elemrep(Elementrep().getbydiagmode(pdiagid=d.diag_id, pmodeid=eler.eler_mode_id,
                                                                       pidx=eler.eler_index))
                                for eler in Elementrep().select(pwhere="""eler_diag_id = {} and eler_mode_id in
                                                                (select mode_id
                                                                from modelelement
                                                                where mode_type ='{}')""".format(d.diag_id,
                                                                                                 mt.melt_shortname))
                                }
                           for mt in Modelelemtype.select(pwhere="""melt_id in (select medi_melt_id
                                                                    from melt_diats
                                                                    where melt_shortname != '{}'
                                                                    and medi_diat_id = {})"""
                                                          .format(Modelelemtype.RELA, d.diag_diat_id))
                           }
            , 'relationships': {anker(Modelelemtype.RELA, rr.relr_mode_id): relarep(rr)
                                for rr in Relationrep.select(pwhere="relr_diag_id = {}".format(d.diag_id))
                                }
            , 'refindocuments': [anker(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=d.diag_id)]
        }
        for d in Diagram.select()}
    return diags

def systems():
    intfs = {anker(Modelelemtype.INTF,i.schn_id) : {'name':i.schn_name
                                                    ,'descr':i.schn_beschr
                                                , 'sourceref': {s: Externalref.getsrcid(psrcname=s, pmodeid=i.schn_id)
                                                            for s in Externalref.getsources()}
                                        ,'refindocuments': [anker(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=i.schn_id)]
                                                    ,'tables' : [anker(Modelelemtype.TABL,t.tabl_id) for t in Tabelle.selectbyschnid(pschnid=i.schn_id)]
                                                    }
             for i in Schnittstelle.select()}
    return intfs

def columns():
    cols = {anker(Modelelemtype.COLU,c.scha_id) :
        {'name':c.scha_column_name
         ,'table-name':Tabelle().getbyid(c.scha_tabl_id).getname()
         ,'table-id':anker(Modelelemtype.TABL,Tabelle().getbyid(c.scha_tabl_id).getid())
        , 'interface-name': Schnittstelle().getbyid(Tabelle().getbyid(c.scha_tabl_id).tabl_schn_id).getname()
        , 'interface-id': anker(Modelelemtype.INTF, Schnittstelle().getbyid(Tabelle().getbyid(c.scha_tabl_id).tabl_schn_id).getid())
            ,'basedatatype' : None if c.scha_daty_id is None else Datatype().getbyid(c.scha_daty_id).daty_name
        ,'datatype':c.scha_type_string
        ,'format':c.scha_format
        ,'domain':anker(Modelelemtype.DOMA,c.scha_doma_id)
        ,'descr':c.scha_beschr
       ,'interface_col_id':c.scha_fremdsystem_id
            , 'uc': c.scha_uc
            , 'dc': c.scha_dc
            , 'um': c.scha_um
            , 'dm': c.scha_dm
        , 'attributes-mapped': [anker(Modelelemtype.ATTR, a.attr_id) for a in
                             AttrTransf.getattrlist(pcoluid=c.scha_id)]

        , 'sourceref': {s: Externalref.getsrcid(psrcname=s, pmodeid=c.scha_id)
                        for s in Externalref.getsources()}
        , 'refindocuments': [anker(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=c.scha_id)]
            }
        for c in Schnittstelleattr.select()
    }
    return cols

def tables():
    tabs = {anker(Modelelemtype.TABL,t.tabl_id) :
                {'name':t.tabl_name
                   ,'interface-name':Schnittstelle().getbyid(t.tabl_schn_id).getname()
                   ,'interface-id':anker(Modelelemtype.INTF,Schnittstelle().getbyid(t.tabl_schn_id).getid())
                   ,'prefix':t.tabl_prefix
                   ,'descr':t.tabl_beschr
                , 'uc': t.tabl_uc
                , 'dc': t.tabl_dc
                , 'um': t.tabl_um
                , 'dm': t.tabl_dm
                ,'entitiesmapped': [anker(Modelelemtype.ENTI, e.enti_id) for e in
                             TablEntiMap.getentilist(ptablid=t.tabl_id)]
              , 'sourceref': {s: Externalref.getsrcid(psrcname=s, pmodeid=t.tabl_id)
                            for s in Externalref.getsources()}
               , 'refindocuments': [anker(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=t.tabl_id)]
                } for t in Tabelle.select()
            }
    return tabs

def project():
    proj = Projekt.select()[0]
    model = {'name': proj.proj_name
        , 'type': Projekt.LOGICALTYPE
        , 'language': proj.proj_akt_sprache.lower()
        , 'uc': proj.proj_uc
        , 'dc': proj.proj_dc
             # , 'dm': None
             }
    return model

def languages():
    langs = {l.lang_iso_code2: {'name': l.lang_iso_name
        , 'iso3': l.lang_iso_code3
        , 'modellanguage': Boolean.str2bool(l.lang_is_base_lang)
        , 'replacementlang': None if l.lang_lang_id is None else Sprache().getbyid(l.lang_lang_id).lang_iso_code2
                                }
             for l in Sprache.select()
             }
    return langs

def lastupd(pmodel):
    dm = lambda  objs: max('0' if val['dm'] is None else val['dm'] for val in pmodel[objs].values())
    return max(dm( 'attributes'), dm( 'domains'), dm( 'entities'))

def sql2json():
    model = {}
    model['model'] = project()
    model['languages'] = languages()
    model['entities'] = entities()
    model['attributes'] = attributes()
    model['relations'] = relations()
    model['arcs'] = arcs()
    model['domains'] = doamains()
    model['keys'] = keys()
    model['documents'] = documents()
    model['diagrams'] = diagrams()
    model['systems'] = systems()
    model['tables'] = tables()
    model['columns'] = columns()
    model['model']['dm'] = lastupd(model)
    return model

def jsonfilename(pfilename):
    return pfilename + '.json'

emptystruct = lambda x: x == EMPTYJSONFILE

def createJSON(pfilepath, pfilename):
    if pfilename is not None:
        dbConnect.openDB(parameters.dbFilePath(), fks='ON')

    model = sql2json(pwithdata=not emptystruct(EMPTYJSONFILE))
    jsonfile = open(pfilepath + jsonfilename(pfilename), 'w')
    jsonfile.write(json.dumps(model, indent=3, sort_keys=False))
    jsonfile.close()
    if (not emptystruct(EMPTYJSONFILE)):
        dbConnect.myDbConn.close()

# createJSON
def json2xml(json_obj, line_padding=""):
    result_list = list()

    json_obj_type = type(json_obj)

    if json_obj_type is list:
        for sub_elem in json_obj:
            result_list.append(json2xml(sub_elem, line_padding))

        return "\n".join(result_list)

    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            if sub_obj is None: continue
            result_list.append("%s<%s>" % (line_padding, tag_name))
            result_list.append(json2xml(sub_obj, "\t" + line_padding))
            result_list.append("%s</%s>" % (line_padding, tag_name))

        return "\n".join(result_list)

    return "%s%s" % (line_padding, json_obj)
#json2xml

def main(param1):
    if emptystruct(param1):
        filename = param1
        filepath = '~/Downloads/'
    else:
        parameters.initparam(p_callarg=param1)
        logmessages.initlog('createJSON')
        filename = parameters.odmModelName()
        filepath = parameters.dbDirect()
    # fi
    try:
        createJSON(pfilepath=filepath, pfilename=filename)
    finally:
        if emptystruct:
            print("JSON file {} for model {} created"
                  .format(filepath + jsonfilename(filename), EMPTYJSONFILE))
        else:
            logmessages.showmessages("JSON file {} for model {} created"
                                     .format(filepath + jsonfilename(filename), parameters.odmModelName()))

    #model = getJSONfile(filepath + jsonfilename(filename))
    #print (json2xml(model))
#  main

if __name__ == '__main__':
    import sys
    main(param1=EMPTYJSONFILE if len(sys.argv) <= 1 else sys.argv[1])
