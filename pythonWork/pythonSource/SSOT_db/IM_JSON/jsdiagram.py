from datetime import datetime
import math
from SSOT_db.IM_JSON import *
from SSOT_infra import nvl, logmessages


DIAGRAMMODEL = ['name', 'legend'
    , 'type', 'width', 'height'
    , 'uc', 'dc', 'um', 'dm'
    , 'elements', 'relationships'
    , 'arcs', 'referencedby', 'sourceref']


def jsondiagram(name, diagtype, uc, dc, **kwargs):
    diagram = dict()
    initjselement(model=diagram, refmodel=DIAGRAMMODEL)
    diagram["name"] = name
    diagram["type"] = diagtype
    diagram["elements"] = {"attribute": [],
                           "entity": []
                           }
    diagram["relationships"] = dict()
    diagram['referencedby']=list()
    diagram["uc"] = uc
    diagram["dc"] = dc

    fillargs(model=diagram, refmodel=DIAGRAMMODEL, **kwargs)
    return diagram


DIAGRELAMODEL = ['linewidth', 'linecolor', 'lineopacity'
        , 'startedge', 'startposition', 'start_connector'
        , 'starttext_angle', 'starttext_distance'
        , 'starttext_x', 'starttext_y'
        , 'starttext_width', 'starttext_height'
        , 'endedge', 'endposition', 'end_connector'
        , 'endtext_angle', 'endtext_distance'
        , 'endtext_x', 'endtext_y'
        , 'endtext_width', 'endtext_height'
        , 'fontcolor', 'fontsize'
        , 'uc', 'dc', 'um', 'dm'
        , 'linesegments'
             ]
def jsondiagrela(start_connector,startedge,startposition,
                 end_connector,endedge,endposition,
                 linesegments,**kwargs):
    diagrela =dict()
    initjselement(model=diagrela, refmodel=DIAGRELAMODEL)
    diagrela['linewidth']=1
    diagrela['lineopacity']=100
    diagrela['fontcolor']="000000"
    diagrela['fontsize']=10
    diagrela['start_connector']=start_connector
    diagrela['startedge']=startedge
    diagrela['startposition']=startposition
    diagrela['end_connector']=end_connector
    diagrela['endedge']=endedge
    diagrela['endposition']=endposition
    diagrela['linesegments']=linesegments
    #TODO
    """[jsonlineseg(x=ls["x"],y=ls["y"],
                                          linetype=ls["linetype"]) for ls in linesegments]"""

    fillargs(model=diagrela, refmodel=DIAGRELAMODEL, **kwargs)
    return diagrela

DIAGLINESEGMODEL = ['x', 'y'
    , 'linetype', 'angle'
                    ]
def jsonlineseg(x,y,linetype,**kwargs):
    diaglineseg = dict()
    initjselement(model=diaglineseg, refmodel=DIAGLINESEGMODEL)
    diaglineseg["x"]=x
    diaglineseg["y"]=y
    diaglineseg["linetype"]=linetype
    diaglineseg["angle"]=0
    fillargs(model=diaglineseg, refmodel=DIAGLINESEGMODEL, **kwargs)

    return diaglineseg

def defaultlinesegements(startx, starty, startedge,startmandatory, endx, endy, endedge,endmandatory):
    """" generate 4 linesegs from startposition to endposition
    """
    minoffset = 60

    def linetype(mandatory):
        if mandatory:
            return Linesegment.SOLID
        else:
            return Linesegment.DASHED

    def xoffset(edge):
        if edge == Linesegment.SOUTH:
            return 0
        elif edge == Linesegment.NORTH:
            return 0
        elif edge == Linesegment.WEST:
            return -minoffset
        else:
            return minoffset

    def yoffset(edge):
        if edge == Linesegment.SOUTH:
            return minoffset
        elif edge == Linesegment.NORTH:
            return -minoffset
        elif edge == Linesegment.WEST:
            return 0
        else:
            return 0

    linesegs = list()
    linesegs.append(jsonlineseg(x= startx, y=starty, linetype=linetype(startmandatory)))
    linesegs.append(jsonlineseg(x= max(startx + xoffset(startedge), 0),
                     y= max(starty + yoffset(startedge), 0),
                     linetype= linetype(startmandatory)))
    linesegs.append(jsonlineseg(x= max(endx + xoffset(endedge), 0),
                     y= max(endy + yoffset(endedge), 0),
                     linetype= linetype(endmandatory)))
    linesegs.append(jsonlineseg(x= endx, y= endy, linetype= linetype(endmandatory)))

    return linesegs

DIAGELEMMODEL = ['element', 'index'
    , 'pos_x', 'pos_y'
    , 'uc', 'dc', 'um', 'dm', 'ui'
                 ]
def jsondiagelem(element, index, width, height, color, **kwargs):
    diagelem = dict()
    initjselement(model=diagelem, refmodel=DIAGELEMMODEL)
    diagelem["element"] = element
    diagelem["index"] = index
    diagelem["pos_y"] = 0
    diagelem["pos_x"] = 0
    diagelem["ui"] = UIElement(width=width
                               , height=height
                               , opacity=kwargs.get("opacity")
                               , color=color
                               , marginwidth=kwargs.get('marginwidth')
                               , marginopacity=kwargs.get('marginopacity')
                               , margincolor=kwargs.get('margincolor')
                               , fontsize=kwargs.get('fontsize')
                               , fontcolor=kwargs.get('fontcolor')).js()
    fillargs(model=diagelem, refmodel=DIAGELEMMODEL, **kwargs)

    return diagelem


def elemrep2js(peler, panker):
    if peler is None:
        retval = fillmodel(pmodel=DIAGELEMMODEL, pentries=['XXXX0000'] + ['' for i in range(len(DIAGELEMMODEL) - 2)]
                                                          + [UIElement().js()])
    else:
        retval = fillmodel(pmodel=DIAGELEMMODEL
                           , pentries=[panker
                , peler.eler_index
                , peler.eler_position_x
                , peler.eler_position_y
                , peler.eler_uc, peler.eler_dc, peler.eler_um, peler.eler_dm
                , UIElement(width=peler.eler_width
                            , height=peler.eler_height
                            , opacity=peler.eler_opacity
                            , color=peler.eler_color
                            , marginwidth=peler.eler_marginwidth
                            , marginopacity=peler.eler_marginopacity
                            , margincolor=peler.eler_margincolor
                            , fontsize=peler.eler_fontsize
                            , fontcolor=peler.eler_fontcolor).js()])
    return retval


def ui2eler(pjsui, peler):
    peler.eler_width = pjsui['width']
    peler.eler_height = pjsui['height']
    peler.eler_opacity = pjsui['opacity']
    peler.eler_color = pjsui['color']
    peler.eler_marginwidth = pjsui['marginwidth']
    peler.eler_marginopacity = pjsui['marginopacity']
    peler.eler_margincolor = pjsui['margincolor']
    peler.eler_fontsize = pjsui['fontsize']
    peler.eler_fontcolor = pjsui['fontcolor']
    return


def elemreps2sql(presult: Mergeresult, pdiagid, pelemreps):
    """[elemrep,] """
    inscnt = 0
    for jelem in pelemreps:
        eler = Elementrep()
        eler.eler_diag_id = pdiagid
        eler.eler_mode_id = presult.keytransl(jelem['element'])
        eler.eler_index = jelem['index']
        eler.eler_position_x = jelem['pos_x']
        eler.eler_position_y = jelem['pos_y']
        eler.eler_uc = jelem['uc']
        eler.eler_dc = jelem['dc']
        eler.eler_um = jelem['um']
        eler.eler_dm = jelem['dm']
        ui2eler(pjsui=jelem["ui"], peler=eler)
        try:
            eler.insert()
            inscnt += 1
        except Exception as err:
            presult.markdberror(perr=err, pelem=jelem)
            continue
    # for
    return inscnt


def relarep2js(prelarep):

    if prelarep is None:
        retval = fillmodel(pmodel=DIAGRELAMODEL, pentries=['' for i in range(len(DIAGRELAMODEL) - 1)] \
                                                  + [[lineseg2js(plineseg=None)]])
    else:

        retval = {'linewidth': prelarep.relr_linewidth
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
            , 'fontcolor': nvl(prelarep.relr_fontcolor, '000000')
            , 'fontsize': prelarep.relr_fontsize
            , 'uc': prelarep.relr_uc
            , 'dc': prelarep.relr_dc
            , 'um': prelarep.relr_um
            , 'dm': prelarep.relr_dm
            , 'linesegments': [lineseg2js(plineseg=l) for l in prelarep.getlinesegments()]
                  }
    return retval

DIAGLINESEGMODEL = ['x', 'y'
        , 'linetype', 'angle'
        ]
def lineseg2js(plineseg):
    if plineseg is None:
        retval = fillmodel(pmodel=DIAGLINESEGMODEL, pentries=['' for i in range(len(DIAGLINESEGMODEL))])
    else:
        retval = fillmodel(pmodel=DIAGLINESEGMODEL
                           , pentries=[plineseg.lise_x, plineseg.lise_y
                , plineseg.lise_linetype, plineseg.lise_angle
                                       ]
                           )
    return retval


def lineseg2sql(presult: Mergeresult, prelrid, plinesegs):
    """               "linesegments": [{"x": 276,...},]
    """
    inscnt = 0
    for jidx, jelem in enumerate(plinesegs):
        lise = Linesegment()
        lise.lise_seq = jidx
        lise.lise_relr_id = prelrid
        lise.lise_x = jelem['x']
        lise.lise_y = jelem['y']
        lise.lise_linetype = jelem['linetype']
        lise.lise_angle = jelem['angle']
        try:
            lise.insert()
            inscnt += 1
        except Exception as err:
            presult.markdberror(perr=err, pelem=jelem)
            continue
    # for
    return inscnt


def relarep2sql(presult, pdiagid, prelaid, prelarep):
    inscnt = 0
    relr = Relationrep()
    relr.relr_diag_id = pdiagid
    relr.relr_mode_id = prelaid
    relr.relr_linewidth = prelarep['linewidth']
    relr.relr_linecolor = prelarep['linecolor']
    relr.relr_lineopacity = prelarep['lineopacity']
    relr.relr_startedge = prelarep['startedge']
    relr.relr_startposition = prelarep['startposition']
    relr.relr_start_connector = prelarep['start_connector']
    relr.relr_starttext_angle = prelarep['starttext_angle']
    relr.relr_starttext_distance = prelarep['starttext_distance']
    relr.relr_starttext_x = prelarep['starttext_x']
    relr.relr_starttext_y = prelarep['starttext_y']
    relr.relr_starttext_width = prelarep['starttext_width']
    relr.relr_starttext_height = prelarep['starttext_height']
    relr.relr_endedge = prelarep['endedge']
    relr.relr_endposition = prelarep['endposition']
    relr.relr_end_connector = prelarep['end_connector']
    relr.relr_endtext_angle = prelarep['endtext_angle']
    relr.relr_endtext_distance = prelarep['endtext_distance']
    relr.relr_endtext_x = prelarep['endtext_x']
    relr.relr_endtext_y = prelarep['endtext_y']
    relr.relr_endtext_width = prelarep['endtext_width']
    relr.relr_endtext_height = prelarep['endtext_height']
    relr.relr_fontcolor = prelarep['fontcolor']
    relr.relr_fontsize = prelarep['fontsize']
    relr.relr_uc = prelarep['uc']
    relr.relr_dc = prelarep['dc']
    relr.relr_um = prelarep['um']
    relr.relr_dm = prelarep['dm']
    try:
        relrid = relr.insert()
        inscnt += 1
    except Exception as err:
        presult.markdberror(perr=err, pelem=relr)
        relrid = None

    # linesegmentsinserts are not counted
    if relrid is not None:
        lineseg2sql(presult=presult, prelrid=relrid, plinesegs=prelarep['linesegments'])

    return inscnt


def legend2js(pdiag=None, pmodelname=None):
    model = ['x'
        , 'y'
        , 'model'
             ]
    if pdiag is None:
        retval = fillmodel(pmodel=model, pentries=['', '', ''])
    else:
        retval = fillmodel(pmodel=model, pentries=[pdiag.diag_legendx, pdiag.diag_legendy, pmodelname])
    # fi
    return retval


def diagrams2js(pemptymodel, pmodelname):
    if pemptymodel:
        retval = {jsguid(Modelelemtype.DIAG, '0000'): fillmodel(pmodel=DIAGRAMMODEL,
                                                                pentries=['', legend2js(), '', '', '', '', '', '', ''
                                                                    , elemrep2js(peler=None, panker=None)
                                                                    , {jsguid(Modelelemtype.RELA, "0000"): relarep2js(
                                                                        prelarep=None)}
                                                                    , defarcs(parc=None, pdiagid=None)
                                                                    , reflist(), reflist()])}
    else:
        # would be count of all elements on all diagrams (complex)
        retval = {jsguid(Modelelemtype.DIAG, d.diag_id): fillmodel(pmodel=DIAGRAMMODEL, pentries=[
            d.diag_name, legend2js(pdiag=d, pmodelname=pmodelname)
            , Diagramtype().getbyid(d.diag_diat_id).getname()
            , nvl(d.diagwidth(), 0) + 50  # leave room for icon in entity
            , d.diagheight()
            , d.diag_uc
            , d.diag_dc
            , d.diag_um
            , d.diag_dm
            , {mt.melt_name.lower():
                   [elemrep2js(peler=eler, panker=jsguid(mt.melt_shortname, eler.eler_mode_id))
                    for eler in sorted(Elementrep.select(pwhere=("""eler_diag_id = ? and eler_mode_id in
                                                                (select mode_id
                                                                from modelelement
                                                                where mode_type = ?)""", d.diag_id, mt.melt_shortname))
                                       , key=lambda e: e.displorder())
                    ]
               for mt in Modelelemtype.select(pwhere=("""melt_id in (select medi_melt_id
                                                                    from melt_diats
                                                                    where melt_shortname != ?
                                                                    and medi_diat_id = ?)""",
                                                      Modelelemtype.RELA, d.diag_diat_id)
                                              , porderby="melt_id")
               }
            , {jsguid(Modelelemtype.RELA, rr.relr_mode_id): relarep2js(rr)
               for rr in Relationrep.select(pwhere=("relr_diag_id = ?", d.diag_id)
                                            , porderby="relr_id")
               }
            , {jsguid(Modelelemtype.ARCS, ar.arcs_id): defarcs(parc=ar, pdiagid=d.diag_id)
               for ar in Arc.getdiagarcs(pdiagid=d.diag_id)
               }
            , [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=d.diag_id)] \
              + [jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=d.diag_id)]
            , Externalref.getsrcinfo(pmodeid=d.diag_id)
        ])
                  for d in tqdm(Diagram.select(), desc="Diagram", dynamic_ncols=True)
                  }
    # fi
    return retval


def js2diag(pkey, pelem, psrcname=None, psrcid=None, pmodellang=None):
    diag = Diagram(psrcname=psrcname, psrcid=psrcid)
    diag.diag_id = pkey
    diag.diag_name = pelem['name']
    legend = pelem['legend']
    diag.diag_legendx = None if legend is None else legend['x']
    diag.diag_legendy = None if legend is None else legend['y']
    diag.diag_diat_id = Diagramtype().getbyuk(diat_name=pelem['type']).diat_id
    diag.diag_uc = pelem['uc']
    diag.diag_dc = pelem['dc']
    diag.diag_um = pelem['um']
    diag.diag_dm = pelem['dm']
    return diag


def diagrams2sql(presult: Mergeresult, pjson: JSModel, pwithextsrcref):
    fromjson2db(presult=presult, pjson=pjson, pelemtype=Modelelemtype.DIAG, pjs2obj=js2diag,
                pwithextsrcref=pwithextsrcref)

    for jid, jelem in pjson.getelements(pelemtype=Modelelemtype.DIAG).items():
        newdiagid = presult.keytransl(jid)
        if newdiagid == 0: continue  # element was not handled
        inscnt = 0
        delcnt = Elementrep.delete(pwhere=("eler_diag_id = ?", newdiagid))
        for jelemreps in jelem['elements'].values():
            """ "elements": {
                    "attributes: [{attrrep},]
                    ,"entities": [{entirep},]
                    }
            """

            inscnt += elemreps2sql(presult=presult, pdiagid=newdiagid, pelemreps=jelemreps)
        # for
        presult.addinscnt(max(0, (inscnt - delcnt)), f"Elementreps on diagram {newdiagid}")
        presult.adddelcnt(max(0, (delcnt - inscnt)), f"Elementreps on diagram {newdiagid}")

        inscnt = 0
        delcnt = Relationrep.delete(pwhere=("relr_diag_id = ?", newdiagid))
        for jrelaid, jrelarep in jelem['relationships'].items():
            """ "relationships":{
                    "RELAnnn": {relarep},
                    } 
            """

            inscnt += relarep2sql(presult=presult, pdiagid=newdiagid, prelaid=presult.keytransl(jrelaid),
                                  prelarep=jrelarep)
        # for
        presult.addinscnt(max(0, (inscnt - delcnt)), f"Relationreps on diagram {newdiagid}")
        presult.adddelcnt(max(0, (delcnt - inscnt)), f"Relationreps on diagram {newdiagid}")

        insreferences(presult=presult, pmodeid=newdiagid, prefs=jelem['referencedby'])
        inssourceref(presult=presult, pmodeid=newdiagid, psources=jelem["sourceref"])
        presult.savenewerrors()

    # for
    return


def defarcs(parc: Arc, pdiagid):
    if parc is None:
        return {'arcs': {'ARCS0000': {"circles": ['', '']}
                         }
                }
    arc = {}
    arcselem = parc.getarcselem(pdiagid=pdiagid)
    if len(arcselem) == 0:
        return arc
    entis = Elementrep.select(
        pwhere=("""eler_mode_id=? and eler_diag_id = ? and eler_index = 0""", parc.arcs_enti_id, pdiagid))
    if len(entis) == 0:
        logmessages.writelog(f"Arc-entity not found for diagram:\tDiagram {pdiagid}, Entity {parc.arcs_enti_id}")
        return arc
    enti = entis[0]
    PONTDISTANCE = 20
    entiheight, entiwidth = enti.eler_height, enti.eler_width
    enticenterx, enticentery = enti.eler_position_x + (entiwidth / 2), enti.eler_position_y + (entiheight / 2)

    circles = []
    calcwinkel = lambda ey, sy, ex, sx: math.atan2(ey - sy, ex - sx)
    poswinkel = lambda x: (x if x > 0 else x + (2 * math.pi)) % (2 * math.pi)
    for ae in arcselem:
        relr_id, startx, starty, endx, endy, enti_id, enti_name, angle = ae
        # print(startx,endx,starty,endy,endy - starty, endx - startx,math.atan2(endy - starty, endx - startx))
        winkel = calcwinkel(endy, starty, endx, startx)
        p4 = math.pi / 4
        """side is left,up,right,down side of rectangle
           Angle shows direction of line passing through pint in thiw q"""

        if (startx >= enticenterx + (entiwidth / 2)):
            side, qwinkel = 'right', 2 * p4
        elif (startx <= enticenterx + (entiwidth / 2)):
            side, qwinkel = 'left', 2 * p4
        elif (starty >= enticentery + (entiheight / 2)):
            side, qwinkel = 'lower', 0
        elif (starty <= enticentery - (entiheight / 2)):
            side, qwinkel = 'upper', 0
        else:
            side, qwinkel = 'upper', 0
        """Angle of line towards center of entity. Sort the order of connecting points in an arc"""
        sortwinkel = poswinkel(calcwinkel(starty, enticentery, startx, enticenterx))
        circles.append([startx + round(PONTDISTANCE * math.cos(winkel), 1)  # - arcstartx
                           , starty + round(PONTDISTANCE * math.sin(winkel), 1)  # - arcstarty
                           , qwinkel, sortwinkel, side
                        ])
    # for
    circles.sort(key=lambda elem: elem[3])
    """Append angle to last point in ARC-order"""
    for idx in range(len(circles)):
        circles[idx].append(
            poswinkel(poswinkel(poswinkel(circles[idx][3]) - circles[((idx - 1) if idx > 0 else len(circles) - 1)][3])))

    """deduce shortest path, starting with every point in arc as starting point"""
    shortestangle = 99999
    for idx in range(len(circles)):
        angle = sum([circles[i][5] for i in range(len(circles))]) - circles[idx][5]
        shortestangle = min(shortestangle, angle)
        circles[idx].append(angle)
    """switch to beginning with shortest path"""
    while circles[0][6] != shortestangle:
        rotate = lambda l: l if len(l) == 0 else l[1:] + l[:1]
        circles = rotate(circles)
    arc['circles'] = [(c[0], c[1]) for c in circles]

    if False:
        """lines of arcs are not yet rendered. Circles are ok. draw your line yourself, if you need to"""
        xfactor = {'right': [0, -1], 'upper': [-1, 1], 'left': [0, 1], 'lower': [1, -1]}
        yfactor = {'right': [-1, -1], 'upper': [0, -1], 'left': [1, 1], 'lower': [0, 1]}
        currentside = None
        arcline = []
        arcpoint = lambda x, y, s: {'x': x, 'y': y, 'side': s}
        prevside = lambda s: 'lower' if s == 'left' else 'left' if s == 'upper' \
            else 'upper' if s == 'right' else 'left'
        nextside = lambda s: 'lower' if s == 'right' else 'right' if s == 'upper' \
            else 'upper' if s == 'left' else 'left'
        for idx, c in enumerate(circles):
            if currentside is None:
                """1. arc point """
                currentside = c[4]
                lastx = c[0] + (PREDISTANCE * xfactor[currentside][0])
                lasty = c[1] + (PREDISTANCE * yfactor[currentside][0])
                arcline.append(arcpoint(lastx, lasty, currentside))
            else:
                # same side is skipped
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
                    # fi
                    arcline.append(arcpoint(newx, newy, currentside))
                    currentside = nextside(currentside)
                    lastx, lasty = newx, newy

            # fi
            if idx == len(circles) - 1:
                currentside = c[4]
                """lasat point of Arc 
                   Linie vom aktuellen arc-Ende bis zum Punkt + vorhalt der letzten Beziehung"""
                arcline.append(arcpoint(round(c[0] + (PREDISTANCE * -xfactor[currentside][0]), 1)
                                        , round(c[1] + (PREDISTANCE * -yfactor[currentside][0]), 1)
                                        , currentside))

            # fi
        # for
        arc['line'] = arcline
    # fi code not yet used
    return arc
# defarcs
