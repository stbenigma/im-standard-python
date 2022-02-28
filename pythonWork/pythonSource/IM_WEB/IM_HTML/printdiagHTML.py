import math
import os,re
import logging
import html

from SSOT_db.IM_OBJECTS import Modelelemtype
from .printHTML import HTMLExport
from SSOT_infra import parameters, nvl

LEGENDWIDTH: int = 363
LEGENDHEIGHT: int = 128
DEFAULT_LINEWIDTH: int = 1
ICONSIZE: int = 40

def printlegend(pdata,pwidth,pheigh,px,py):

    legenhead = """<g  fill="rgb(255,255,255)" stroke="rgb(0,0,0)" 
                fill-opacity="1.0" stroke-opacity="1.0" 
                clip-path="url(#clipPathlegend)" 
                transform="translate({},{})" >
                """
    legendentry1 = """
<rect x="0" y="0" width="{}" height="{}" />
<text x="10" y="{}" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
{}:
</text>
<text x="86" y="{}" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
{}
</text>
"""
    legendentry2 = """<line x1="0" y1="{}" x2="261" y2="{}" fill="none" stroke="rgb(0,0,0)"/>
<text x="10" y="{}" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
{}:
</text>
<text x="86" y="{}" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
{}
</text>
"""
    legendfoot= """</g>
"""
    retval = ""
    starty=14
    retval += legenhead.format(nvl(px, 0) + 2, nvl(py, 0) + 1)
    retval += legendentry1.format(pwidth-100,pheigh-2
                                    ,starty,'Diagram'
                                    ,starty,pdata[0])
    starty += 18
    retval += legendentry2.format(starty-13,starty-13
                                    ,starty,'Author'
                                    ,starty,pdata[1])
    starty += 18
    retval += legendentry2.format(starty-13,starty-13
                                    ,starty,'Created on:'
                                    ,starty,pdata[2])
    starty += 18
    retval += legendentry2.format(starty-13,starty-13
                                    ,starty,'Modified on'
                                    ,starty,pdata[3])
    starty += 18
    retval += legendentry2.format(starty-13,starty-13
                                    ,starty,'Modified by'
                                    ,starty,pdata[4])
    starty += 18
    retval += legendentry2.format(starty-13,starty-13
                                    ,starty,'Model'
                                    ,starty,pdata[5])
    starty += 18
    retval += legendentry2.format(starty-13,starty-13
                                    ,starty,'Modeltype'
                                    ,starty,pdata[6])
    retval += legendfoot
    return retval
#printlegend

def hex2rbg(phex):
    if phex is None:
        return "rgb(0,0,0)"
    try:
        r = int(phex[0:2], 16)
        g = int(phex[2:4], 16)
        b = int(phex[4:6], 16)
    except:
        print(phex)
        raise
    return "rgb({},{},{})".format(r,g,b)
#hex2rbg


def printtext(px, py, ptext, pfillcolor, pfontsize, pstandalone=False, pdescr=None):
    MAXATTRDESCR = 300
    showtext = """<text x="{posx}" y="{posy}" fill="{color}" fill-opacity="1.0" font-size="{fontsize}" stroke="none">
    {text}{title}
    </text>
    """
    retval = ""
    if pstandalone: retval += "<g >"

    description = html.escape(" " if pdescr is None else pdescr[:MAXATTRDESCR])

    retval += showtext.format(posx=px, posy=py, color=pfillcolor, fontsize=pfontsize, text=ptext
                              , title="" if pstandalone
            else "<title>{}</title>".format(description))
    if pstandalone: retval += "</g>\n"
    return retval


# printtext


calcwinkel = lambda ey,sy,ex,sx : math.atan2(ey - sy, ex - sx)

def calccrowfoot(pstartx, pstarty, pendx, pendy):
    fusslaenge = 9
    fussseite = math.sqrt((fusslaenge ** 2) / 2)
#    winkel = math.atan2(pendy - pstarty, pendx - pstartx)
    winkel = calcwinkel(pendy,pstarty,pendx, pstartx)
    winkel1 = winkel + (5 / 4 * math.pi)
    xoffset, yoffset = round(fussseite * math.sin(winkel), 2), round(fussseite * math.cos(winkel), 2)
    xl, yl = round(fusslaenge * math.sin(winkel1), 2), round(fusslaenge * math.cos(winkel1), 2)
    return xoffset,yoffset,xl,yl
#calccrowfoot

def printrela(plist):
    relastart = """<g stroke-linecap="butt" >
                """
    relaline = """<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="{}"  stroke-width="{}" 
            stroke-dasharray="{}"  d="M{} {} L{} {}" />
            """
    konnektor = """<path stroke-opacity="{}" stroke-width="{}" stroke-dasharray="none" 
                        d="M{} {} l{} {} {} {}" 
                        fill="none"  
                        stroke="rgb(0,0,0)" />
            """
    relaend = """</g>
               """
    retval = ""
    for line in plist.values():
        """lise_x,lise_y,lise_konnektor,lise_linientyp"""
        points = line['linesegments']
        retval += relastart
        for idx,point in enumerate(points):
            if idx == len(points)-1: break #letzter Punkt ist endx/y
            startx=point['x']
            starty=point['y']
            endx=points[idx+1]['x']
            endy=points[idx+1]['y']
            opacity = 1.0
            linewidth = DEFAULT_LINEWIDTH
            startconnector = ((line['start_connector'] == 'M') and (idx == 0))
            endconnector = ((line['end_connector'] == 'M') and (idx == len(points)-2))
            dash = "8,8" if point['linetype']=='DASHED' else 'none'
            retval += relaline.format(opacity,linewidth,dash,startx,starty,endx,endy)
            if startconnector or endconnector:
                """zeichne die Krähenfüsse"""
                xoffset, yoffset, xl, yl = calccrowfoot(pstartx=startx, pstarty=starty, pendx=endx, pendy=endy)
                if (startconnector):
                    """print('START',startx, starty, endx, endy
                      , round(winkel,1), winkel / math.pi * 180
                      , round(winkel1,1), winkel1 / math.pi * 180
                      ,xoffset,yoffset,xl,yl
                      , sep=', ')"""
                    retval += konnektor.format(opacity, linewidth, startx-xoffset, starty+yoffset
                                               ,-xl,yl,yl,xl
                                                       )
                #fi
                if (endconnector) :
                    retval += konnektor.format(opacity, linewidth, endx+xoffset, endy-yoffset
                                               ,xl,-yl,-yl,-xl
                                                       )
                #fi
            #fi
        #for
        retval += relaend
    #for
    return retval
#printrela

def print1text(ptext,px,py,pwidth,pcolor,psize):
    FONTPIXEL: int = 5
    textlength = lambda s: len(nvl(s)) * FONTPIXEL
    retval = ""
    if ptext is not None and px is not None:
        if px is None:
            logging.warning(f"Label {ptext} has no coordinates px: {px}, py: {py}")
            return retval
        words = ptext.split(' ')
        posx,posy = int(px),int(py)
        idx,t = 0,words[0]
        while idx < len(words):
            idx += 1
            while idx < len(words) and textlength(t + words[idx]) < pwidth:
                t = t + " " + words[idx]
                idx += 1
            # while
            retval += printtext(px=px, py=posy, ptext=t
                                , pfillcolor=hex2rbg(pcolor), pfontsize=psize
                                , pstandalone=True)
            if idx < len(words): t = words[idx]
            posy += 12
        # while    
    # fi
    return retval

def printtexte(export: HTMLExport, plist,plang):
    retval= ""
    for relaanker,relaelem in plist.items():
        retval += print1text(ptext=export.getelement(relaanker)['from-to']['assoc'][plang],px=relaelem["starttext_x"],py=relaelem["starttext_y"],pwidth=relaelem["starttext_width"],pcolor=relaelem['fontcolor'],psize=relaelem['fontsize'])
        retval += print1text(ptext=export.getelement(relaanker)['to-from']['assoc'][plang],px=relaelem["endtext_x"],py=relaelem["endtext_y"],pwidth=relaelem["endtext_width"],pcolor=relaelem['fontcolor'],psize=relaelem['fontsize'])
    #for
    return retval
#printtexte

def print1arc(parc,pcolor):

    startarcstr = """
        <g fill="none" stroke="rgb(0,0,0)" transform="translate({},{})" >
    """
    circledraw = """
        <g fill="none" stroke="rgb(0,0,0)" transform="translate({},{})" >
        <circle stroke-dasharray="none" cx="{}" cy="{}"
            stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
        </g>
    """
    circle = """<circle stroke-dasharray="none" cx="{}" cy="{}"
            stroke="rgb(0,0,0)" r="3" fill="{}" stroke-width="0" />
    """
    pathstr = """    
        <path d=" {}"/>
        </g>
    """
    endarcstr = """    
        </g>
    """
    retval = ""
    if len(parc) == 0: return retval
    retval += startarcstr.format(0,0)
    for c in parc['circles']:
        #print(circledraw.format(c[0],c[1],c[0],c[1]))
        retval += circle.format(c[0],c[1],pcolor)
    # for
    if False: # mal probieren ohne Linien. Es hat noch Fehler
        arcline = ''
        for idx,line in enumerate(parc['line']):
            if idx == 0:
                arcline = "M{} {}".format(line['x'],line['y'])
            else:
                arcline += ' L{} {} '.format(line['x'],line['y'])
            #fi
        #for
        retval += pathstr.format(arcline)
    # fi
    retval += endarcstr
    return
    pointdistance = 20
    arclng = 10
    predistance = 10
    arcstartx,arcstarty = pentipos[0]-pointdistance, pentipos[1]-pointdistance
    entiheight,entiwidth = pentipos[2],pentipos[3]
    enticenterx,enticentery = pentipos[0] + (entiwidth / 2),pentipos[1] + (entiheight / 2)
    arcwidth,archeight = entiwidth + (2 * (pointdistance - arclng)),  entiheight + (2 * (pointdistance - arclng))
    retval += startarcstr.format(arcstartx,arcstarty)

    xfactor = {1:[0,-1],2:[1,1],3:[0,1],4:[-1,-1]}
    yfactor = {1:[-1,-1],2:[0,-1],3:[1,1],4:[0,1]}
    currentq = None
    arcline = ''
    for idx,c in enumerate(circles):
        if currentq is None:
            """1. arc beziehung"""
            currentq = c[4]
            mx = c[0] + (predistance * xfactor[currentq][0]) + (arclng * xfactor[currentq][1])
            my = c[1] + (predistance * yfactor[currentq][0]) + (arclng * yfactor[currentq][1])
            arcline += "M{} {}".format(mx,my)
            arcline += ' q{} {} {} {}'.format(arclng * -yfactor[currentq][0],arclng * xfactor[currentq][0]
                                                   ,arclng * -xfactor[currentq][1],arclng * -yfactor[currentq][1])
        else:
            qanz = (c[4] - currentq + 5) % 5-1
            for q in range(currentq,currentq + qanz ):
                qm = q if q < 5 else  q % 5 + 1
                #print (c[4],currentq,qanz,q,qm)

                currentq = qm
                """ neuer Quadrant, zeichne arc um ecke q4->q1, 4->2, 4->3, 1->2, 1->3 1->4, 2->3 2->4 2->1"""
                """Linie ab aktuellem Punkt bis ans Ende der Entität"""
                x2factor = {1: [1,2,1,1], 2: [0,1,1,2], 3: [0,0,0,1], 4: [1,1,0,0]}
                arcline += ' L{} {} '.format(x2factor[currentq][0]*arcwidth + x2factor[currentq][1]*arclng
                                        ,x2factor[currentq][2]*archeight + x2factor[currentq][3]*arclng)

                """Bogen um die Ecke"""
                arcline += ' q{} {} {} {}'.format(arclng * -xfactor[currentq][0], arclng * -yfactor[currentq][0]
                                          , arclng * yfactor[currentq][1], arclng * -xfactor[currentq][1])
            #for
        #fi Beziehungen im gleichen Quadranten kann ich vergessen, ausser es ist die letzte (siehe nächsten Abschnitt)
        if idx == len(circles) - 1:
            currentq = c[4]
            """letzte Beziehung des Arc 
               Linie vom aktuellen arc-Ende bis zum Punkt + vorhalt der letzten Beziehung"""
            arcline += ' L{} {}'.format(round(c[0] + (predistance * -xfactor[currentq][0]),1)
                                        ,round(c[1] + (predistance * -yfactor[currentq][0])),1)
            """ Abschlussbogen"""
            arcline += ' q{} {} {} {}'.format(arclng * -xfactor[currentq][0],arclng * -yfactor[currentq][0]
                                            ,arclng * yfactor[currentq][1],arclng * -xfactor[currentq][1])
        #fi
    #for
    retval += endarcstr.format(arcline)
    return retval
#print1arc

def printarcs(export: HTMLExport, plist):
    colors = ["blue","yellow","purple","green","red","black"]
    """select arcs_id,beda_id"""
    retval = ""
    idx = 0
    lastenti = None
    arcs = [(export.getelement(arc)["entity"], arc) for arc in sorted(plist.keys(), key=lambda k: export.getelement(k)["entity"])]
    for arc in arcs:
        if lastenti != arc[0]:
            lastenti = arc[0]
            idx = 0
        else:
            idx = (idx+1) % len(colors)
        # fi
        print1arc(parc=plist[arc[1]],pcolor=colors[idx])
    #for
    return retval
#printarcs


def printelements(export: HTMLExport, pdiag, pdiaganker, plang):
    entistart = """<g  fill="{color}" stroke="{margcolor}" fill-opacity="{fopacity}" stroke-opacity="{sopacity}" 
        transform="translate({posx},{posy})" >
        <rect x="0" y="0" width="{width}" height="{height}" rx="10" ry="10" >{title}</rect><a href="{hyperlink}" >
        <text id="{textref}" x="20" y="13" fill="{fontcolor}" font-weight="bold"  fill-opacity="1.0" font-size="{fontsize}" stroke="none">
            {name} </text>{title}</a>
        </g>"""
    imagehtml = """"<image href = "{}" width = "{}px" height = "{}px" class ="entity-image" x="{}px" y="{}px"></image>""" \
        .format('{}', ICONSIZE, ICONSIZE, '{}', '{}')

    retval = ""
    MAXDESCRCHARS = 300

    # stack up elements in subtype-level order
    levels = list(map(lambda e: int(e['subtypellevel+']),
                      export.model.getelements(Modelelemtype.ENTI).values()))
    deepest_subtype_level: int = max(levels)

    # higher subtypelevels => topmost
    for subtypelevel in range(0, deepest_subtype_level + 1):
        for eler in pdiag['elements']['entity']:
            entity = export.getelement(eler['element'])
            if int(entity['subtypellevel+']) == subtypelevel:
                elerui = eler["ui"]
                entidescr = export.getelement(eler['element'])['descr'][plang]
                if entidescr is None:
                    entidescr = ' '
                else:
                    entidescr = entidescr[: MAXDESCRCHARS]

                # fallback: element anchor
                hyperlink = export.custom_hyperlink(entity)
                if hyperlink is None:
                    hyperlink = '#' + eler['element']
                entity_svg = entistart.format(color=hex2rbg(elerui['color']), margcolor=hex2rbg(elerui['margincolor'])
                                           , fopacity=round(elerui['opacity'] / 100, 2),
                                           sopacity=round(elerui['marginopacity'] / 100, 2)
                                           , posx=eler['pos_x'], posy=eler['pos_y'], width=elerui['width'],
                                           height=elerui['height']
                                           , hyperlink=html.escape(hyperlink)
                                           , textref=pdiaganker + '-' + eler['element']
                                           , fontcolor=hex2rbg(elerui['fontcolor'])
                                           , fontsize=11  # vorläufig mal fix verdrahtet e[9], font size
                                           , name=entity['name'][plang] + (
                        '' if (eler['index'] == 0) else ':' + str(eler['index']))
                                           , title="" if entidescr is None else f"<title>{html.escape(entidescr)}</title>")

                # whole entity box carries the hyperlink
                retval += f"""<a href="{html.escape(hyperlink)}">{entity_svg}</a>\n"""

                iconsrc = export.iconsrc(pjsenti=export.getelement(eler['element']),
                                         pdefaultlang=export.getmodel().getdefaultlang())
                if iconsrc != "":
                    retval += imagehtml.format(iconsrc
                                               , eler['pos_x'] + elerui['width'] - ICONSIZE / 2,
                                               eler['pos_y'] - ICONSIZE / 2)
        # for

    #  attr_id, attr_displ_name, attr_is_mandatory ,attr_is_descriptive, schluessel, mode_id
    for attr in pdiag['elements']['attribute']:
        attrui = attr["ui"]
        x = attr['pos_x']
        y = attr['pos_y']
        aelem = export.getelement(attr['element'])

        hyperlink = export.href(ref=attr['element'], anz=aelem['name'][plang])
        description = aelem['descr'][plang]

        if description.lower().startswith('http') and not hyperlink.lower().startswith('http'):
            logging.warning(f"Attribute {attr['element']} '{aelem['name'][plang]}' description is an URL. Using this as link.")
            hyperlink = f"""<a href="{html.escape(description)}"><title>{aelem['name'][plang]}</title></a>"""
            description = ""

        retval += printtext(px=x, py=y, ptext=hyperlink
                            , pfillcolor=hex2rbg(attrui['fontcolor']), pfontsize=attrui['fontsize']
                            , pdescr=description)
    # for
    retval += printrela(plist=pdiag['relationships'])
    retval += printtexte(export, plist=pdiag['relationships'], plang=plang)
    retval += printarcs(export=export, plist=pdiag['arcs'])
    return retval


# printelements

def putrefinsvg(export: HTMLExport, ptext,pdiagid,plang):
    MAXDESCR=300
    retval = ptext
    for entiid,entival in export.getmodel().getelements(pelemtype='ENTI').items():
        try:
            odmref = entival["sourceref"]["ODM"][0]
        except:
            continue
        diagodm=re.escape(odmref[:8])
        entiodm=re.escape(odmref[-12:])
        entisearch = re.search(r'<g.*"translate\((\d+),(\d+)\)".*\n<rect.*width="(\d+)".*rx="(\d+)".*\n.*<text id="{diagodm}-{entiodm}"[\d\D]*?</g>'
                            .format(diagodm=diagodm,entiodm=entiodm), retval)
        if entisearch is None:
            continue
        entistr = entisearch.group()
        xstart, ystart, xwidth, xoffset = None,None,None,None
        if ((entisearch.groups() is not None) and (len(entisearch.groups()) > 3)):
            xstart, ystart, xwidth, xoffset = int(entisearch.groups()[0]), int(entisearch.groups()[1]), int(entisearch.groups()[2]), int(entisearch.groups()[3])

        newenti = entistr
        #replace id by diagid-entiid
        newenti = re.sub(f'"{diagodm}-{entiodm}"', f'"{re.escape(pdiagid)}-{re.escape(entiid)}"', newenti)
        #add title to rect
        entidescr = entival["descr"][plang]
        entidescr = " " if entidescr is None else entidescr[:MAXDESCR]
        newenti = re.sub('/>.*\n<text id=', '>{}</rect><text id="'.format("<title>{}</title>".format(entidescr)), newenti)
        newenti = re.sub('(<text id="[\d\D]+?</text>)', r'\1{}'.format("<title>{}</title>".format(entidescr)), newenti)
        #add <a href= to enti
        newenti = re.sub('<text id="', '<a href="#{}"><text id="'.format(re.escape(entiid)), newenti)
        newenti = re.sub(r'(<text id="[\d\D]+?</text>)', r'\1</a>', newenti)

        for attrid in entival["attributes+"]:
            attrval = export.getelement(attrid)
            newenti = re.sub(r'(<text x=".*\n\s*{}\s*\n</text>)'.format(re.escape(attrval["name"][plang])),
                             r'<a href="#{}">\1</a>'.format(re.escape(attrid)), newenti)
            attrdescr = attrval["descr"][plang]
            attrdescr = " " if attrdescr in (None,"") else attrdescr[:MAXDESCR]
            newenti = re.sub(r'(<text x=".*\n\s*{}\s*\n</text>)'.format(re.escape(attrval["name"][plang]))
                             ,r'\1{}'.format("<title>{}</title>".format(attrdescr)),
                             newenti)
        #add image if exists
        filename = export.iconsrc(pjsenti=entival,pdefaultlang=export.getmodel().getdefaultlang())
        if filename != "":
            newenti += '\n<image href="{}" width="40px" height="40px" class ="entity-image" x="{}px" y="{}px"></image>' \
                        .format(filename,xstart + xwidth - (ICONSIZE/2), ystart - (ICONSIZE/2))

        retval = re.sub(re.escape(entistr),newenti,retval)
    #for

    return retval

def checkforfile(pname,ptype,plang=None):
    retval = None
    if plang is not None:
        filepath = os.path.join(parameters.webDirec(), "image" , pname + "_" + plang + "." + ptype)
        if os.path.exists(filepath):
            retval = filepath
    #fi
    if retval is None:
        """check for file without language_marker"""
        filepath = os.path.join(parameters.webDirec(),  "image" , pname + "." + ptype)
        if os.path.exists(filepath):
            retval = filepath

    return retval

def svgfilename(pname,plang=None):
    return checkforfile(pname = pname,plang = plang,ptype = "svg")
def pdffilename(pname,plang=None):
    retval = None
    if checkforfile(pname = pname,plang = plang,ptype = "pdf") is not None:
        retval = "image/"+pname+"."+"pdf"
    return retval

def getsvgfromfile(pname, plang=None):
    retval = None
    svgfn = svgfilename(pname=pname, plang=plang)
    if svgfn is not None:
        """add links to svg and include it in html"""
        with (open(file=svgfn, mode="r")) as f:
            retval = f.read()
    #fi
    return retval

def getsvgtext(export: HTMLExport, plang,pdiaganker,pdiagelem,ptitel=None):
    retval = getsvgfromfile(pname=pdiagelem["name"],plang=plang)
    if retval is not None:
        retval = putrefinsvg(export=export,ptext=retval, pdiagid=pdiaganker, plang=plang)
    elif pdffilename(pname=pdiagelem["name"],plang=plang) is not None:
        retval = None
    else:
        """render diagram"""
        retval = f"""<svg id="{pdiaganker}-SVG" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
                version="1.1"  width="{pdiagelem["width"]}" height="{pdiagelem["height"]}">
                <defs id="dmw_defs" >
                </defs>"""
        if ('legend' in pdiagelem.keys() and pdiagelem['legend']['x'] is not None and pdiagelem['legend']['y'] is not None ):
            # es hat eine Legende
            retval += printlegend(pdata=[pdiagelem['name'], nvl(pdiagelem['uc']), nvl(pdiagelem['dc']),
                                         nvl(pdiagelem['dm'])
                , nvl(pdiagelem['um']), ptitel, 'Logical']
                                   , pwidth=LEGENDWIDTH, pheigh=LEGENDHEIGHT
                                   , px=pdiagelem['legend']['x'], py=pdiagelem['legend']['y'])
        # fi
        retval += printelements(export=export, pdiag=pdiagelem, pdiaganker=pdiaganker, plang=plang)
        retval += """</svg>"""
    # fi
    return retval


