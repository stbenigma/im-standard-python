from IM_HTML import printHTML
import web_sql
import math
from parameters import nvl
from WEB_OBJECTS import WebDiagram
from IM_OBJECTS import Sprache

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
    starty=14
    printHTML.fhtml.write(legenhead.format(px+2,py+1))
    printHTML.fhtml.write(legendentry1.format(pwidth-100,pheigh-2
                                    ,starty,'Diagram'
                                    ,starty,pdata[0]))
    starty += 18
    printHTML.fhtml.write(legendentry2.format(starty-13,starty-13
                                    ,starty,'Author'
                                    ,starty,pdata[1]))
    starty += 18
    printHTML.fhtml.write(legendentry2.format(starty-13,starty-13
                                    ,starty,'Created on:'
                                    ,starty,pdata[2]))
    starty += 18
    printHTML.fhtml.write(legendentry2.format(starty-13,starty-13
                                    ,starty,'Modified on'
                                    ,starty,pdata[3]))
    starty += 18
    printHTML.fhtml.write(legendentry2.format(starty-13,starty-13
                                    ,starty,'Modified by'
                                    ,starty,pdata[4]))
    starty += 18
    printHTML.fhtml.write(legendentry2.format(starty-13,starty-13
                                    ,starty,'Model'
                                    ,starty,pdata[5]))
    starty += 18
    printHTML.fhtml.write(legendentry2.format(starty-13,starty-13
                                    ,starty,'Modeltype'
                                    ,starty,pdata[6]))
    printHTML.fhtml.write(legendfoot)
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
    if pstandalone: printHTML.fhtml.write("<g >")
    printHTML.fhtml.write(showtext.format(px, py,pfillcolor,pfontsize, ptext))
    if pstandalone: printHTML.fhtml.write("</g>\n")
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
    for line in plist.values():
        """lise_x,lise_y,lise_konnektor,lise_linientyp"""
        points = line['linesegments']
        printHTML.fhtml.write(relastart)
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
            printHTML.fhtml.write(relaline.format(opacity,linewidth,dash,startx,starty,endx,endy))
            if startconnector or endconnector:
                """zeichne die Krähenfüsse"""
                xoffset, yoffset, xl, yl = calccrowfoot(pstartx=startx, pstarty=starty, pendx=endx, pendy=endy)
                if (startconnector):
                    """print('START',startx, starty, endx, endy
                      , round(winkel,1), winkel / math.pi * 180
                      , round(winkel1,1), winkel1 / math.pi * 180
                      ,xoffset,yoffset,xl,yl
                      , sep=', ')"""
                    printHTML.fhtml.write(konnektor.format(opacity, linewidth, startx-xoffset, starty+yoffset
                                               ,-xl,yl,yl,xl
                                                       ))
                #fi
                if (endconnector) :
                    printHTML.fhtml.write(konnektor.format(opacity, linewidth, endx+xoffset, endy-yoffset
                                               ,xl,-yl,-yl,-xl
                                                       ))
                #fi
            #fi
        #for
        printHTML.fhtml.write(relaend)
    #for
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
    for relaanker,relaelem in plist.items():
        startx, starty = relaelem['starttext_x'],relaelem['starttext_y']
        starttextw,starttexth=nvl(relaelem['starttext_width'],0),nvl(relaelem['starttext_height'],0)
        starttext=getrelation(relaanker)['from-to']['assoc'][plang]
        fontcolor = relaelem['fontcolor']
        fontsize = relaelem['fontsize']
        endx,endy =relaelem['endtext_x'],relaelem['endtext_y']
        endtextw,endtexth=nvl(relaelem['endtext_width'],0),nvl(relaelem['endtext_height'],0)
        endtext=getrelation(relaanker)['to-from']['assoc'][plang]

        linesegs = relaelem['linesegments']
        if len(linesegs)> 0:
            linestartx,linestarty,linestartangle = linesegs[0]['x'],linesegs[0]['y'],linesegs[0]['angle']
            lineendx,lineendy,lineendangle = linesegs[len(linesegs)-1]['x'],linesegs[len(linesegs)-1]['y'],linesegs[len(linesegs)-2]['angle']

        textlength = lambda s: len(nvl(s)) * FONTPIXEL
        if starttext is not None:
            if ((((linestartangle >= math.pi / 2) and (linestartangle < math.pi )) or (linestartangle < 0))):
                s = starttext.split(' ')
            else:
                s =[starttext]
            posx, posy = textpos(pangle=linestartangle, px=linestartx, py=linestarty, ptextlen=textlength(starttext),
                                 pstart=True)
            for t in s:
                printtext(px=posx, py=posy, ptext=t
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
                printtext(px=posx, py=posy, ptext=t
                          , pfillcolor=hex2rbg(fontcolor), pfontsize=fontsize
                          , pstandalone=True)
                posy += 12 
    #for
#printtexte

def print1arc(parc):

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
            stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
    """
    endarcstr = """    
        <path d=" {}"/>
        </g>
    """
    printHTML.fhtml.write(startarcstr.format(0,0))
    for c in parc['circles']:
        #print(circledraw.format(c[0],c[1],c[0],c[1]))
        printHTML.fhtml.write(circle.format(c[0],c[1]))
    # for
    arcline = ''
    for idx,line in enumerate(parc['line']):
        if idx == 0:
            arcline = "M{} {}".format(line['x'],line['y'])
        else:
            arcline += ' L{} {} '.format(line['x'],line['y'])
        #fi
    #for
    printHTML.fhtml.write(endarcstr.format(arcline))
    return
    pointdistance = 20
    arclng = 10
    predistance = 10
    arcstartx,arcstarty = pentipos[0]-pointdistance, pentipos[1]-pointdistance
    entiheight,entiwidth = pentipos[2],pentipos[3]
    enticenterx,enticentery = pentipos[0] + (entiwidth / 2),pentipos[1] + (entiheight / 2)
    arcwidth,archeight = entiwidth + (2 * (pointdistance - arclng)),  entiheight + (2 * (pointdistance - arclng))
    printHTML.fhtml.write(startarcstr.format(arcstartx,arcstarty))

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
    printHTML.fhtml.write(endarcstr.format(arcline))
#print1arc

def printarcs(plist):
    """select arcs_id,beda_id"""
    for arc in plist.values():
        print1arc(parc=arc)
    #for
#printarcs

getentity = lambda e:printHTML.model['entities'][e]
getattribute = lambda a:printHTML.model['attributes'][a]
getrelation = lambda r:printHTML.model['relations'][r]

def printelements(pdiag, pdiaganker,plang):
    entistart ="""<g  fill="{}" stroke="{}" fill-opacity="{}" stroke-opacity="{}" 
        transform="translate({},{})" >
<rect x="0" y="0" width="{}" height="{}" rx="10" ry="10" /><a href="#{}" >
<text id="{}" x="20" y="13" fill="{}" font-weight="bold"  fill-opacity="1.0" font-size="{}" stroke="none">
{} </text></a>
"""
    entiende="""</g>"""
    imagehtml=""""<image href = "image/{}.png" width = "{}px" height = "{}px" class ="entity-image" x="{}px" y="{}px"></image>""".format('{}',WebDiagram.ICONSIZE,WebDiagram.ICONSIZE,'{}','{}')

    for eler in pdiag['elements']['entity']:
        printHTML.fhtml.write(entistart.format(hex2rbg(eler['color']), hex2rbg(eler['margincolor'])
                                                   , round(eler['opacity']/100,2), round(eler['marginopacity']/100,2)
                                                   , eler['pos_x'], eler['pos_y'], eler['width'], eler['height']
                                                   , eler['element']
                                                   , pdiaganker + '-' + eler['element']
                                                   , hex2rbg(eler['fontcolor'])
                                                   , 12  #vorläufig mal fix verdrahtet e[9], font size
                                                   ,getentity(eler['element'])['name'][plang] + ('' if (eler['index']==0) else':'+str(eler['index']))))

        printHTML.fhtml.write(entiende)
        filename = printHTML.iconfilename(getentity(eler['element'])['name'][Sprache.getdefaultlang().lang_iso_code2])
        if filename != "":
            printHTML.fhtml.write(imagehtml.format(filename
                                               ,eler['pos_x']+eler['width']-ICONSIZE/2,
                                                eler['pos_y'] - ICONSIZE/2))

    #for
    #  attr_id, attr_displ_name, attr_is_mandatory ,attr_is_descriptive, schluessel, mode_id
    for attr in pdiag['elements']['attribute']:
        x = attr['pos_x']
        y = attr['pos_y']
        aelem = ge  tattribute(attr['element'])
        printtext(px=x, py=y, ptext=printHTML.href(ref=attr['element'], anz=aelem['name'][plang])
                  , pfillcolor=hex2rbg(attr['fontcolor']), pfontsize=attr['fontsize']
                  )
    # for
    printrela(plist=pdiag['relationships'])
    printtexte(plist=pdiag['relationships'],plang=plang)
    printarcs(plist=pdiag['arcs'])
#printelements

def printcontentdiag(plist, plang, ptitel):
    contenthead="""        <!--diagramms-->"""

    diagramhead = """        <br><hr><br><br>
        <div id="{}-container">
       <h3 id="{}">{}</h3>
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
        version="1.1"  width="{}" height="{}">
        <defs id="dmw_defs" >
        </defs>
"""
#wäre in defs drin
#           <clipPath clipPathUnits="userSpaceOnUse" id="clipPathlegend">
#             <rect x="0" y="0" width="{}" height="{}" />
#        </clipPath>

    diagramfoot = """
</svg>
    <div class="print-button-container">
        <button class="print-button" onclick="printElem(this)">print</button>
    </div>
</div>
"""
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
    for diaanker,diaelem in plist.items():
        #diag_name,diag_id,diag_legendx,diag_legendy,breite,hoehe
        printHTML.fhtml.write (diagramhead.format(diaanker,diaanker, diaelem['name']
                                                  , diaelem['width'], diaelem['height']))
                                #wäre clippath,legendwidth,legendhigh))

        if ('legend' in diaelem.keys()):
            #es hat eine Legende
            printlegend(pdata=[diaelem['name'], nvl(diaelem['uc']), nvl(diaelem['dc']),nvl(diaelem['dm'])
                , nvl(diaelem['um']), ptitel, 'Logical']
                    ,pwidth=LEGENDWIDTH,pheigh=LEGENDHEIGHT
                    ,px=diaelem['legend']['x'],py=diaelem['legend']['y'])
        #fi

        printelements(pdiag=diaelem, pdiaganker=diaanker,plang=plang)
        printHTML.fhtml.write(diagramfoot)
    #for
#printcontendiag
