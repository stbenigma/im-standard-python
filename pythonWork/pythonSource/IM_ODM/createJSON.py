# -*- coding: latin-1 -*-
import json
import math

from IM_DB import dbConnect, parameters, logmessages
from IM_OBJECTS import *
from mystring import nvl

EMPTYJSONFILE = 'emptyjsonmodel'


# Main Programm
def getJSONfile(pfilename):
    with open(pfilename, 'r') as handle:
        model = json.load(handle)
    return model


def elemrep(peler,panker):
    if peler is None: return {}
    return {'element':panker
        , 'index': peler.eler_index
        , 'pos_x': peler.eler_position_x
        , 'pos_y': peler.eler_position_y
        , 'width': peler.eler_width
        , 'height': peler.eler_height
        , 'opacity': peler.eler_opacity
        , 'color': peler.eler_color
        , 'marginwidth': peler.eler_marginwidth
        , 'marginopacity': peler.eler_marginopacity
        , 'margincolor': peler.eler_margincolor
        , 'fontsize': peler.eler_fontsize
        , 'fontcolor': peler.eler_fontcolor
            }


anker = lambda n, i: None if i is None else n + str(i)


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
                     ,'relations': [anker(Modelelemtype.RELA, r.rela_id) for r in Relation.getbyentity(pentiid=e.enti_id)]
                     ,'keys': [anker(Modelelemtype.KEYS, k.keys_id) for k in Key.select(pwhere="keys_enti_id = {}".format(e.enti_id))]
                     ,'inarcs': [anker(Modelelemtype.ARCS, a.arcs_id) for a in Arc.select(pwhere="arcs_enti_id = {}".format(e.enti_id))]
                     ,'refindocuments': [anker(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=e.enti_id)]
                     , 'userdefprop': {
                     t[0]: {g[1]: {u.udpr_name: Userdefpropvalue.udpvalue(pudprid=u.udpr_id, pmodeid=e.enti_id)
                                   for u in Userdefprop.getudps(ptheme=t[0], pgroup=g[1], pmeltname=Modelelemtype.ENTI)}
                            for g in Userdefprop.grouplist(pudptheme=t[0], pmelttype=Modelelemtype.ENTI)}
                     for t in Userdefprop.themelist(pmelttype=Modelelemtype.ENTI)}

                     , 'tablesmapped': {anker(Modelelemtype.INTF,s.getid()): [anker(Modelelemtype.TABL, t.tabl_id) for t in
                                                      TablEntiMap.gettabllist(pentiid=e.enti_id, pintfid=s.getid())]
                                        for s in Interface.getmapped(pentiid=e.enti_id)}
                     ,
                  'diagrams': [anker(Modelelemtype.DIAG, d.diag_id) for d in Diagram.getdiagrams(pmodeid=e.enti_id)]
                  } for e in Entity.select()}
    return entis


def defattr(attr):
    retval = {'techname': attr.attr_tech_name
        , 'name': attr.attr_displ_name_L
        , 'seq': attr.attr_displ_seq
        , 'entity': anker(Modelelemtype.ENTI, attr.attr_enti_id)
        , 'relation': anker(Modelelemtype.RELA, attr.attr_rela_id)
        , 'domain': anker(Modelelemtype.DOMA, attr.attr_doma_id)
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
        , 'keys': [anker(Modelelemtype.KEYS, k.keys_id) for k in attr.getkeys()]
        , 'refindocuments': [anker(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=attr.attr_id)]
        , 'userdefprop': {t[0]: {g[1]: {u.udpr_name: Userdefpropvalue.udpvalue(pudprid=u.udpr_id, pmodeid=attr.attr_id)
                                        for u in
                                        Userdefprop.getudps(ptheme=t[0], pgroup=g[1], pmeltname=Modelelemtype.ATTR)}
                                 for g in Userdefprop.grouplist(pudptheme=t[0], pmelttype=Modelelemtype.ATTR)}
                          for t in Userdefprop.themelist(pmelttype=Modelelemtype.ATTR)}
        , 'columnsmapped': {
            anker(Modelelemtype.INTF,s.getid()): [anker(Modelelemtype.COLU, c.colu_id) for c in
                          AttrTransf.getcolulist(pattrid=attr.attr_id, pintfid=s.getid())]
            for s in Interface.getmapped(pattrid=attr.attr_id)}
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
    return [{'name': dg.dgrm_name
            ,'mandatory': dg.dgrm_is_mandatory
            , 'domain': anker(Modelelemtype.DOMA, dg.dgrm_doma_id_member)
            , 'descr': dg.dgrm_descr}
            for dg in DomaingroupMember.select(pwhere="dgrm_doma_id_group={}".format(pdomaid))
            ]


def defdomain(doma):
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
    retval['usedinattrs'] = [anker(Modelelemtype.ATTR, a.attr_id) for a in
                                Attribute.select(pwhere="attr_doma_id = {}".format(doma.doma_id))]
    retval['usedincols']= [anker(Modelelemtype.COLU, c.colu_id) for c in
                           Column.select(pwhere="colu_doma_id = {}".format(doma.doma_id))]
    retval['usedingrps']= [anker(Modelelemtype.DOMA, d.doma_id) for d in
                     Domain.select(pwhere="doma_id in (select dgrm_doma_id_group from domaingroup_members where dgrm_doma_id_member = {})"
                                            .format(doma.doma_id))]
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
                {'name': k.keys_name
                    , 'entity': anker(Modelelemtype.ENTI, k.keys_enti_id)
                    , 'uc': k.keys_uc
                    , 'dc': k.keys_dc
                    , 'um': k.keys_um
                    , 'dm': k.keys_dm
                    ,'sourceref': {s: Externalref.getsrcid(psrcname=s, pmodeid=k.keys_id) for s in Externalref.getsources()}
                    , 'key-elements': {'attributes':[anker(Modelelemtype.ATTR , ke.kele_attr_id)
                                                    for ke in k.getkeyelements(Modelelemtype.ATTR)]
                  ,'relations': [anker(Modelelemtype.RELA , ke.kele_rela_id)
                                                    for ke in k.getkeyelements(Modelelemtype.RELA)]
                                   }
                 } for k in Key.select()}
    return keys


def relation(prela):
    if prela is None: return {}
    keys = [k for k in Key.select(pwhere="""keys_id in (select kele_keys_id 
                                                from key_elements 
                                                where kele_rela_id = {})""".format(prela.rela_id))]
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
                    ,'cardstr': prela.to_cardstr()
                }
                , 'to-from':{
                    'enti': anker(Modelelemtype.ENTI, prela.rela_enti_id_to)
                    , 'arc': None if prela.rela_arcs_id_to is None else anker(Modelelemtype.ARCS, prela.rela_arcs_id_to)
                    , 'assoc': prela.rela_assoc_to_from_L
                    , 'maptype': prela.rela_maptype_to_from
                    , 'hist': Boolean.str2bool(prela.rela_hist_to_from)
                    , 'mandatory': Boolean.str2bool(prela.rela_mandatory_to_from)
                  , 'cardstr': prela.from_cardstr()
                }
                ,'isinkeys': [anker(Modelelemtype.KEYS,k.keys_id) for k in keys]
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
            , 'parent': None if d.docu_docu_id is None else anker(Modelelemtype.DOCU, d.docu_docu_id)
            ,'referencecnt': len(d.getrefmodes())
            , 'references': {
                            'entities': [anker(m.mode_type, m.mode_id) for m in d.getrefmodes(pmelttype=Modelelemtype.ENTI)]
                            ,'attributes': [anker(m.mode_type, m.mode_id) for m in d.getrefmodes(pmelttype=Modelelemtype.ATTR)]
                                ,'domains': [anker(m.mode_type, m.mode_id) for m in d.getrefmodes(pmelttype=Modelelemtype.DOMA)]
                                ,'systems': [anker(m.mode_type, m.mode_id) for m in d.getrefmodes(pmelttype=Modelelemtype.INTF)]
                                ,'tables': [anker(m.mode_type, m.mode_id) for m in d.getrefmodes(pmelttype=Modelelemtype.TABL)]
                                ,'columns': [anker(m.mode_type, m.mode_id) for m in d.getrefmodes(pmelttype=Modelelemtype.COLU)]
                                ,'diagrams': [anker(m.mode_type, m.mode_id) for m in d.getrefmodes(pmelttype=Modelelemtype.DIAG)]
                                }
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
        , 'fontcolor': nvl(prelarep.relr_fontcolor,'000000')
        , 'fontsize': prelarep.relr_fontsize
        , 'uc': prelarep.relr_uc
        , 'dc': prelarep.relr_dc
        , 'um': prelarep.relr_um
        , 'dm': prelarep.relr_dm
        , 'linesegments': {l.lise_seq: {'x': l.lise_x
            , 'y': l.lise_y
            , 'linetype': l.lise_linetype
            , 'angle': l.lise_angle
                                        }
                           for l in prelarep.getlinesegments()}
            }

def defarcs(parc,pdiagid):
    arc = {}
    arcselem = parc.getarcselem(pdiagid=pdiagid)
    enti=Elementrep().select(pwhere="""eler_mode_id={} and eler_diag_id = {} and eler_index = 0""".format(parc.arcs_enti_id,pdiagid))
    enti = enti[0]
    PONTDISTANCE = 20
    ARCLNG = 10
    PREDISTANCE = 10
    entiheight,entiwidth = enti.eler_height, enti.eler_width
    enticenterx,enticentery = enti.eler_position_x + (entiwidth / 2),enti.eler_position_y + (entiheight / 2)
    entistartx,entistarty = enti.eler_position_x ,enti.eler_position_y

    circles=[]
    calcwinkel = lambda ey, sy, ex, sx:math.atan2(ey - sy, ex - sx)
    poswinkel = lambda x: (x if x > 0 else x + (2 * math.pi)) % (2 * math.pi)
    for ae in arcselem:
        relr_id, startx, starty, endx, endy, enti_id, enti_name, angle = ae
        #print(startx,endx,starty,endy,endy - starty, endx - startx,math.atan2(endy - starty, endx - startx))
        winkel = calcwinkel(endy, starty,endx, startx)
        p4 = math.pi / 4
        """side is left,up,right,down side of rectangle
           Angle shows direction of line passing through pint in thiw q"""
        if (startx >= enticenterx + (entiwidth/2)): side,qwinkel='right',2*p4
        elif (startx <= enticenterx - (entiwidth/2)): side,qwinkel='left',2*p4
        elif (starty >= enticentery + (entiheight/2)): side,qwinkel='lower',0
        elif (starty <= enticentery - (entiheight/2)): side,qwinkel='upper',0
        """Angle of line towards center of entity. Sort the order of connecting points in an arc"""
        sortwinkel = poswinkel(calcwinkel(starty, enticentery, startx, enticenterx))
        circles.append([startx + round(PONTDISTANCE * math.cos(winkel),1) #- arcstartx
                        ,starty + round(PONTDISTANCE * math.sin(winkel),1) #- arcstarty
                        ,qwinkel,sortwinkel,side
                        ])
    #for
    circles.sort(key=lambda elem: elem[3])
    """Append angle to last point in ARC-order"""
    for idx in range(len(circles)):
        circles[idx].append(poswinkel(poswinkel(poswinkel(circles[idx][3]) - circles[((idx-1) if idx > 0 else len(circles) - 1)][3])))

    """deduce shortest path, starting with every point in acr as starting point"""
    shortestangle=99999
    for idx in range(len(circles)):
        angle = sum([circles[i][5] for i in range(len(circles))])-circles[idx][5]
        shortestangle = min(shortestangle,angle)
        circles[idx].append(angle)
    """switch to beginning with shortest path"""
    while circles[0][6] != shortestangle:
        rotate = lambda l: l if len(l)== 0 else l[1:]+l[:1]
        circles = rotate(circles)
    arc['circles'] = [(c[0],c[1]) for c in circles]
    xfactor = {'right':[0,-1],'upper':[-1,1],'left':[0,1],'lower':[1,-1]}
    yfactor = {'right':[-1,-1],'upper':[0,-1],'left':[1,1],'lower':[0,1]}
    currentside = None
    arcline = []
    arcpoint =lambda x,y,s :{'x':x,'y':y,'side':s}
    prevside =lambda s:'lower' if s=='left' else 'left' if s =='upper'\
                                else 'upper' if s == 'right' else 'left'
    nextside =lambda s:'lower' if s=='right' else 'right' if s =='upper'\
                                else 'upper' if s == 'left' else 'left'
    for idx,c in enumerate(circles):
        if currentside is None:
            """1. arc point """
            currentside = c[4]
            lastx = c[0] + (PREDISTANCE * xfactor[currentside][0])
            lasty = c[1] + (PREDISTANCE * yfactor[currentside][0])
            if lastx == 980.2:
                print(lastx,lasty)
            arcline.append(arcpoint(lastx,lasty,currentside))
        else:
            #same side is skipped
            while (currentside != c[4]):
                """new side meaning corner point(s)"""
                """line from current point to the other axis of new point"""
                if currentside == 'left':
                    newx = lastx
                    newy = entistarty - PONTDISTANCE
                elif currentside == 'upper':
                    newx = entistartx + entiwidth + PONTDISTANCE
                    newy = lasty
                elif currentside == 'right':
                    newx = lastx
                    newy = entistarty + entiheight + PONTDISTANCE
                else:
                    newx = entistartx - PONTDISTANCE
                    newy = lasty
                #fi
                arcline.append(arcpoint(newx,newy,currentside))
                currentside = nextside(currentside)
                lastx,lasty = newx,newy

        #fi
        if idx == len(circles) - 1:
            currentside = c[4]
            """lasat point of Arc 
               Linie vom aktuellen arc-Ende bis zum Punkt + vorhalt der letzten Beziehung"""
            arcline.append(arcpoint(round(c[0] + (PREDISTANCE * -xfactor[currentside][0]), 1)
                                          ,round(c[1] + (PREDISTANCE * -yfactor[currentside][0]), 1)
                                          ,currentside))

        #fi
    #for
    arc['line'] = arcline
    return arc
#defarcs

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
                               [elemrep(peler=eler, panker=anker(mt.melt_shortname, eler.eler_mode_id))
                                for eler in sorted(Elementrep().select(pwhere="""eler_diag_id = {} and eler_mode_id in
                                                                (select mode_id
                                                                from modelelement
                                                                where mode_type ='{}')""".format(d.diag_id,
                                                                                                 mt.melt_shortname))
                                                   ,key=lambda e : e.displorder())
                                ]
                           for mt in Modelelemtype.select(pwhere="""melt_id in (select medi_melt_id
                                                                    from melt_diats
                                                                    where melt_shortname != '{}'
                                                                    and medi_diat_id = {})"""
                                                          .format(Modelelemtype.RELA, d.diag_diat_id))
                           }
            , 'relationships': {anker(Modelelemtype.RELA, rr.relr_mode_id): relarep(rr)
                                for rr in Relationrep.select(pwhere="relr_diag_id = {}".format(d.diag_id))
                                }
            , 'arcs': {anker(Modelelemtype.ARCS, ar.arcs_id): defarcs(parc=ar,pdiagid=d.diag_id)
                                        for ar in Arc.getdiagarcs(pdiagid=d.diag_id)
                                }
            , 'refindocuments': [anker(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=d.diag_id)]
        }
        for d in Diagram.select()}
    return diags

def systems():
    intfs = {anker(Modelelemtype.INTF,i.intf_id) : {'name':i.intf_name
                                                    ,'interface-id':anker(Modelelemtype.INTF,i.intf_id)
                                                    ,'descr':i.intf_descr
                                                , 'sourceref': {s: Externalref.getsrcid(psrcname=s, pmodeid=i.intf_id)
                                                            for s in Externalref.getsources()}
                                        ,'refindocuments': [anker(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=i.intf_id)]
                                                    ,'tables' : [anker(Modelelemtype.TABL,t.tabl_id) for t in Table.selectbyschnid(pschnid=i.intf_id)]
                                                    }
             for i in Interface.select()}
    return intfs

def columns():
    cols = {anker(Modelelemtype.COLU,c.colu_id) :
        {'name':c.colu_column_name
         ,'table-name':Table().getbyid(c.colu_tabl_id).getname()
         ,'table-id':anker(Modelelemtype.TABL, Table().getbyid(c.colu_tabl_id).getid())
        , 'interface-name': Interface().getbyid(Table().getbyid(c.colu_tabl_id).tabl_intf_id).getname()
        , 'interface-id': anker(Modelelemtype.INTF, Interface().getbyid(Table().getbyid(c.colu_tabl_id).tabl_intf_id).getid())
            ,'basedatatype' : None if c.colu_daty_id is None else Datatype().getbyid(c.colu_daty_id).daty_name
        ,'datatype':c.colu_type_string
        ,'format':c.colu_format
        ,'domain':anker(Modelelemtype.DOMA,c.colu_doma_id)
        ,'descr':c.colu_descr
       ,'interface_col_id':c.colu_ext_system_id
            , 'uc': c.colu_uc
            , 'dc': c.colu_dc
            , 'um': c.colu_um
            , 'dm': c.colu_dm
        , 'attributes-mapped': [anker(Modelelemtype.ATTR, a.attr_id) for a in
                             AttrTransf.getattrlist(pcoluid=c.colu_id)]
        , 'userdefprop': {
            th[0]: {gr[1]: {u.udpr_name: Userdefpropvalue.udpvalue(pudprid=u.udpr_id, pmodeid=c.colu_id)
                            for u in Userdefprop.getudps(ptheme=th[0], pgroup=gr[1], pmeltname=Modelelemtype.COLU)}
                    for gr in Userdefprop.grouplist(pudptheme=th[0], pmelttype=Modelelemtype.COLU)}
            for th in Userdefprop.themelist(pmelttype=Modelelemtype.COLU)
        }
            , 'sourceref': {s: Externalref.getsrcid(psrcname=s, pmodeid=c.colu_id)
                        for s in Externalref.getsources()}
        , 'refindocuments': [anker(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=c.colu_id)]
            }
            for c in Column.select()
            }
    return cols

def tables():
    tabs = {anker(Modelelemtype.TABL,t.tabl_id) :
                {'name':t.tabl_name
                   ,'interface-name':Interface().getbyid(t.tabl_intf_id).getname()
                   ,'interface-id':anker(Modelelemtype.INTF, Interface().getbyid(t.tabl_intf_id).getid())
                   ,'prefix':t.tabl_prefix
                   ,'descr':t.tabl_descr
                , 'uc': t.tabl_uc
                , 'dc': t.tabl_dc
                , 'um': t.tabl_um
                , 'dm': t.tabl_dm
                 ,'columns':[anker(Modelelemtype.COLU, c.colu_id) for c in t.getcolumns()]
                , 'userdefprop': {
                    th[0]: {gr[1]: {u.udpr_name: Userdefpropvalue.udpvalue(pudprid=u.udpr_id, pmodeid=t.tabl_id)
                                  for u in Userdefprop.getudps(ptheme=th[0], pgroup=gr[1], pmeltname=Modelelemtype.TABL)}
                           for gr in Userdefprop.grouplist(pudptheme=th[0], pmelttype=Modelelemtype.TABL)}
                    for th in Userdefprop.themelist(pmelttype=Modelelemtype.TABL)
                }
                    ,'entitiesmapped': [anker(Modelelemtype.ENTI, e.enti_id) for e in
                             TablEntiMap.getentilist(ptablid=t.tabl_id)]
              , 'sourceref': {s: Externalref.getsrcid(psrcname=s, pmodeid=t.tabl_id)
                            for s in Externalref.getsources()}
               , 'refindocuments': [anker(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=t.tabl_id)]
                } for t in Table.select()
            }
    return tabs

def project():
    proj = Project.select()[0]
    model = {'name': proj.proj_name
        , 'type': Project.LOGICALTYPE
        , 'language': proj.proj_curr_lang.lower()
        , 'uc': proj.proj_uc
        , 'dc': proj.proj_dc
             # , 'dm': None
             }
    return model

def languages():
    langs = {l.lang_iso_code2: {'name': l.lang_iso_name
        , 'iso3': l.lang_iso_code3
        , 'modellanguage': Boolean.str2bool(l.lang_is_base_lang)
        , 'replacementlang': None if l.lang_lang_id is None else Language().getbyid(l.lang_lang_id).lang_iso_code2
                                }
             for l in Language.select()
             }
    return langs

def lastupd(pmodel):
    dm = lambda  objs: max('0' if val['dm'] is None else val['dm'] for val in pmodel[objs].values())
    return max(dm( 'attributes'), dm( 'domains'), dm( 'entities'))

def sql2json(pwithdata=True):
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
