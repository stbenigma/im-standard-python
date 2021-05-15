from IM_HTML import printHTML
import math
import os,re
from IM_DB import parameters 
from IM_OBJECTS import Language

LEGENDWIDTH: int = 363
LEGENDHEIGHT: int = 128
DEFAULT_LINEWIDTH: int = 1
ICONSIZE: int = 40
FONTPIXEL: int = 5


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
    retval += legenhead.format(parameters.nvl(px,0)+2,parameters.nvl(py,0)+1)
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
def printtext(px, py, ptext, pfillcolor, pfontsize, pstandalone=False):
    showtext= """<text x="{}" y="{}" fill="{}" fill-opacity="1.0" font-size="{}" stroke="none">
    {}
    </text>
    """
    retval = ""
    if pstandalone: retval += "<g >"
    retval += showtext.format(px, py,pfillcolor,pfontsize, ptext)
    if pstandalone: retval += "</g>\n"
    return retval
#printtext

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
        for idx,point in points.items():
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

def textpos(pangle,px,py,ptextlen,pstart):
    if ((pstart and (pangle >= 0) and (pangle < math.pi / 2)) 
       or (not pstart and (pangle >= math.pi / 2))):
        x = px + 5
        y = py - 5
    elif ((pstart and (pangle >= math.pi / 2) and (pangle < math.pi))
         or(not pstart and (pangle < 0))):
        x = px + 5
        y = py + 10
    elif (pstart and (pangle >= math.pi)
         or (not pstart and (pangle >= 0) and (pangle < math.pi / 2))):
        x = px - 5 - ptextlen
        y = py + 10
    else:
        x = px + 5
        y = py - 5
    # fi
    return (x,y)
#textpos

def printtexte(plist,plang):
    """beda_starttext_x,beda_starttext_y
       ,beda_starttext_breite,beda_starttext_hoehe
        ,beda_endtext_x,beda_endtext_y
        ,beda_endtext_breite,beda_endtext_hoehe
       ,beda_schriftfarbe,beda_schriftgroesse
       ,sfrom.sptx_text fromname
       ,sto.sptx_text toname
        ,beda_id
       ,beda_liniefarbe,beda_linienbreite,beda_liniedeckkraft"""
    retval= ""
    for relaanker,relaelem in plist.items():
        startx, starty = relaelem['starttext_x'],relaelem['starttext_y']
        starttextw,starttexth=parameters.nvl(relaelem['starttext_width'],0),parameters.nvl(relaelem['starttext_height'],0)
        starttext=getelement(relaanker)['from-to']['assoc'][plang]
        fontcolor = relaelem['fontcolor']
        fontsize = relaelem['fontsize']
        endx,endy =relaelem['endtext_x'],relaelem['endtext_y']
        endtextw,endtexth=parameters.nvl(relaelem['endtext_width'],0),parameters.nvl(relaelem['endtext_height'],0)
        endtext=getelement(relaanker)['to-from']['assoc'][plang]

        linesegs = relaelem['linesegments']
        if len(linesegs)> 0:
            linestartx,linestarty,linestartangle = linesegs[0]['x'],linesegs[0]['y'],linesegs[0]['angle']
            lineendx,lineendy,lineendangle = linesegs[len(linesegs)-1]['x'],linesegs[len(linesegs)-1]['y'],linesegs[len(linesegs)-2]['angle']

        textlength = lambda s: len(parameters.nvl(s)) * FONTPIXEL
        if starttext is not None:
            if ((((linestartangle >= math.pi / 2) and (linestartangle < math.pi )) or (linestartangle < 0))):
                s = starttext.split(' ')
            else:
                s =[starttext]
            posx, posy = textpos(pangle=linestartangle, px=linestartx, py=linestarty, ptextlen=textlength(starttext),
                                 pstart=True)
            for t in s:
                retval += printtext(px=posx, py=posy, ptext=t
                  , pfillcolor=hex2rbg(fontcolor), pfontsize=fontsize
                  ,pstandalone=True)
                posy += 12 
                
        if endtext is not None:
            if ((((lineendangle >= math.pi / 2) and (lineendangle < math.pi )) or (lineendangle < 0))):
                s = endtext.split(' ')
            else:
                s =[endtext]
            posx,posy = textpos(pangle=lineendangle,px=lineendx,py=lineendy,ptextlen=textlength(endtext),pstart=False)
            if lineendangle > 0:
                posy -= 12 *(len(s)-1)
            for t in s:
                retval += printtext(px=posx, py=posy, ptext=t
                          , pfillcolor=hex2rbg(fontcolor), pfontsize=fontsize
                          , pstandalone=True)
                posy += 12 
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

def printarcs(plist):
    colors = ["blue","yellow","purple","green","red","black"]
    """select arcs_id,beda_id"""
    retval = ""
    idx = 0
    lastenti = None
    arcs = [(getelement(arc)["entity"], arc) for arc in sorted(plist.keys(), key=lambda k: getelement(k)["entity"])]
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

getelement = lambda e:printHTML.getmodel().getbyid(e)

def printelements(pdiag, pdiaganker,plang):
    entistart ="""<g  fill="{}" stroke="{}" fill-opacity="{}" stroke-opacity="{}" 
        transform="translate({},{})" >
        <rect x="0" y="0" width="{}" height="{}" rx="10" ry="10" /><a href="#{}" >
        <text id="{}" x="20" y="13" fill="{}" font-weight="bold"  fill-opacity="1.0" font-size="{}" stroke="none">
            {} </text></a>
        """
    entiende="""</g>"""
    imagehtml=""""<image href = "{}" width = "{}px" height = "{}px" class ="entity-image" x="{}px" y="{}px"></image>"""\
        .format('{}',ICONSIZE,ICONSIZE,'{}','{}')

    retval = ""
    for eler in pdiag['elements']['entity']:
        retval += entistart.format(hex2rbg(eler['Color']), hex2rbg(eler['margincolor'])
                                               , round(eler['opacity']/100,2), round(eler['marginopacity']/100,2)
                                               , eler['pos_x'], eler['pos_y'], eler['width'], eler['height']
                                               , eler['element']
                                               , pdiaganker + '-' + eler['element']
                                               , hex2rbg(eler['fontcolor'])
                                               , 11  #vorläufig mal fix verdrahtet e[9], font size
                                               , getelement(eler['element'])['name'][plang] + ('' if (eler['index'] == 0) else ':' + str(eler['index'])))

        retval += entiende
        iconsrc = printHTML.iconsrc(pjsenti=getelement(eler['element']),pdefaultlang=printHTML.getmodel().getdefaultlang())
        if iconsrc != "":
            retval += imagehtml.format(iconsrc
                                               ,eler['pos_x']+eler['width']-ICONSIZE/2,
                                                eler['pos_y'] - ICONSIZE/2)

    #for
    #  attr_id, attr_displ_name, attr_is_mandatory ,attr_is_descriptive, schluessel, mode_id
    for attr in pdiag['elements']['attribute']:
        x = attr['pos_x']
        y = attr['pos_y']
        aelem = getelement(attr['element'])
        retval += printtext(px=x, py=y, ptext=printHTML.href(ref=attr['element'], anz=aelem['name'][plang])
                  , pfillcolor=hex2rbg(attr['fontcolor']), pfontsize=attr['fontsize']
                  )
    # for
    retval += printrela(plist=pdiag['relationships'])
    retval += printtexte(plist=pdiag['relationships'],plang=plang)
    retval += printarcs(plist=pdiag['arcs'])
    return retval
#printelements

def putrefinsvg(ptext,pdiagid,plang):
    imagehtml = """<image href = "image/{}.png" width = "{}px" height = "{}px" class ="entity-image" x="{}px" y="{}px"></image>"""\
                .format('{}', ICONSIZE, ICONSIZE, '{}', '{}')
    deflang = printHTML.getmodel().jsmodel["model"]["language"]

    retval = ptext
    for entiid,entival in printHTML.getmodel().getelements(pelemtype='ENTI').items():
        try:
            odmref = entival["sourceref"]["ODM"][0]
        except:
            continue

        entisearch = re.search(r'<g.*"translate\((\d+),(\d+)\)".*\n<rect.*width="(\d+)".*rx="(\d+)".*\n.*<text id="{}-{}"[\d\D]*?</g>'
                            .format(re.escape(odmref[:8]),re.escape(odmref[-12:])), retval)
        if entisearch is None:
            continue
        entistr = entisearch.group()
        xstart, ystart, xwidth, xoffset = None,None,None,None
        if ((entisearch.groups() is not None) and (len(entisearch.groups()) > 3)):
            xstart, ystart, xwidth, xoffset = int(entisearch.groups()[0]), int(entisearch.groups()[1]), int(entisearch.groups()[2]), int(entisearch.groups()[3])

        newenti = entistr
        #replace id by diagid-entiid
        newenti = re.sub('"{}-{}"'.format(re.escape(odmref[:8]),re.escape(odmref[-12:])), '"{}-{}"'.format(re.escape(pdiagid),re.escape(entiid)), newenti)
        #add <a href= to enti
        newenti = re.sub('<text id="', '<a href="#{}"><text id="'.format(re.escape(entiid)), newenti)
        newenti = re.sub(r'(<text id="[\d\D]+?</text>)', r'\1</a>', newenti)

        for attrid in entival["attributes+"]:
            attrval = printHTML.getelement(attrid)
            newenti = re.sub(r'(<text x=".*\n\s*{}\s*\n</text>)'.format(re.escape(attrval["name"][plang])),
                             r'<a href="#{}">\1</a>'.format(re.escape(attrid)), newenti)
        #add image if exists
        filename = printHTML.iconsrc(pjsenti=entival,pdefaultlang=printHTML.getmodel().getdefaultlang())
        if filename != "":
            newenti += '\n<image href="{}" width="40px" height="40px" class ="entity-image" x="{}px" y="{}px"></image>' \
                        .format(filename,xstart + xwidth - (ICONSIZE/2), ystart - (ICONSIZE/2))

        retval = re.sub(re.escape(entistr),newenti,retval)
    #for

    return retval

def svgfilename(pname,plang=None):
    retval = None
    if (plang is not None):
        svgfn = parameters.webDirec() + "/image/" + pname + "_" + plang + ".svg"
        if os.path.exists(svgfn): retval = svgfn
    #fi
    if retval is None: #try filename without language marker
        svgfn = parameters.webDirec() + "/image/" + pname + ".svg"
        if os.path.exists(svgfn):
            retval = svgfn
        else:
            retval = None
        #fi
    #fi
    return retval


def diaghtmlhead(panker, pname, pwidth, pheight):
    return """        <br><hr><br><br>
        <div id="{}-container">
       <h3 id="{}">{}</h3>
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
        version="1.1"  width="{}" height="{}">
        <defs id="dmw_defs" >
        </defs>
    """.format (panker,panker,pname,pwidth,pheight)
    #wäre in defs drin
    #           <clipPath clipPathUnits="userSpaceOnUse" id="clipPathlegend">
    #             <rect x="0" y="0" width="{}" height="{}" />
    #        </clipPath>

def diaghtmlfoot():
    return """
        <div class="print-button-container">
            <button class="print-button" onclick="printElem(this)">print</button>
        </div>
    </div>
    """


def getsvgtext( plang,pdiaganker,pdiagelem,ptitel=None):
    svgfn = svgfilename(pname=pdiagelem["name"], plang=plang)
    if svgfn is not None:
        """add links to svg and include it in html"""
        with (open(file=svgfn, mode="r")) as f:
            svgtext = f.read()
        retval = putrefinsvg(ptext=svgtext, pdiagid=pdiaganker, plang=plang)
    else:
        """render diagram"""
        retval = ""
        if ('legend' in pdiagelem.keys()):
            # es hat eine Legende
            retval += printlegend(pdata=[pdiagelem['name'], parameters.nvl(pdiagelem['uc']), parameters.nvl(pdiagelem['dc']),
                                          parameters.nvl(pdiagelem['dm'])
                , parameters.nvl(pdiagelem['um']), ptitel, 'Logical']
                                   , pwidth=LEGENDWIDTH, pheigh=LEGENDHEIGHT
                                   , px=pdiagelem['legend']['x'], py=pdiagelem['legend']['y'])
        # fi
        retval += printelements(pdiag=pdiagelem, pdiaganker=pdiaganker, plang=plang)
    # fi
    return retval

def printcontentdiag(plist, plang, ptitel):
    contenthead="""        <!--diagramms-->"""

    detailshead = """           
                <!-- The inside div eliminates the 'jumping' animation. -->
"""
    detailsfoot = """            
                            </div>
"""
    infohead = """
                            <h2>{}</h2>
                        <div id="container2">
                        <div class="table-responsive">
                            <table class="table borderless">
                                <tbody>
"""
    retval = ""
    for diaanker,diaelem in plist.items():
        #diag_name,diag_id,diag_legendx,diag_legendy,breite,hoehe
        retval += diaghtmlhead(panker=diaanker, pname=diaelem['name']
                                                  , pwidth=diaelem['width'], pheight=diaelem['height'])
                                #wäre clippath,legendwidth,legendhigh))

        svgtext = getsvgtext(plang = plang,pdiaganker=diaanker,pdiagelem=diaelem,ptitel=ptitel)

        printHTML.fhtml.write(svgtext)
        printHTML.fhtml.write(diaghtmlfoot())
    #for
    return retval
#printcontendiag
