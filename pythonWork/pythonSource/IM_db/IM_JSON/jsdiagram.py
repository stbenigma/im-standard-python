import math
from IM_OBJECTS import *
from IM_JSON import jsguid
from mystring import nvl




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

def diagrams2js(pmodelname):
    diags = {jsguid(Modelelemtype.DIAG, d.diag_id):
        {
            'name': d.diag_name
            , 'legend': {'x': d.diag_legendx
                , 'y': d.diag_legendy
                , 'model': pmodelname
                         }
            , 'type': Diagramtype().getbyid(d.diag_diat_id).getname()
            , 'width': d.diagwidth()
            , 'height': d.diagheight()
            , 'uc': d.diag_uc
            , 'dc': d.diag_dc
            , 'um': d.diag_um
            , 'dm': d.diag_dm
            , 'elements': {mt.melt_name.lower():
                               [elemrep(peler=eler, panker=jsguid(mt.melt_shortname, eler.eler_mode_id))
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
            , 'relationships': {jsguid(Modelelemtype.RELA, rr.relr_mode_id): relarep(rr)
                                for rr in Relationrep.select(pwhere="relr_diag_id = {}".format(d.diag_id))
                                }
            , 'arcs': {jsguid(Modelelemtype.ARCS, ar.arcs_id): defarcs(parc=ar,pdiagid=d.diag_id)
                                        for ar in Arc.getdiagarcs(pdiagid=d.diag_id)
                                }
            , 'refindocuments': [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=d.diag_id)]
            ,'refbyorgunits': [jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=d.diag_id)]
        }
        for d in Diagram.select()}
    return diags

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
        elif (startx <= enticenterx + (entiwidth/2)): side,qwinkel='left',2*p4
        elif (starty >= enticentery + (entiheight/2)): side,qwinkel='lower',0
        elif (starty <= enticentery - (entiheight/2)): side,qwinkel='upper',0
        else:
            side,qwinkel = 'upper',0
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

def diagrams2sql(pmodel):
    for jid,jelem in pmodel.jsmodel['diagrams'].items():
        pass
        #inssourceref(pmodel = pmodel,pmodeid=jsguid2id(jid), psources=jelem["sourceref"])
    return

"""transfer references and subtypes"""
def diagrefs2sql(pmodel):
    #    insudp(pmodeid=entiid, pudps=jenti["userdefprop"])
    return
