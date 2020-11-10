from IM_HTML import printHTML
import web_sql
import math
from WEB_OBJECTS import WebDiagram,WebEntity

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
    printHTML.fhtml.write(showtext.format(px, py,pfillcolor, pfontsize, ptext))
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
    for line in plist:
        """lise_x,lise_y,lise_konnektor,lise_linientyp"""
        points = web_sql.pointlist(line[12])
        printHTML.fhtml.write(relastart)
        for idx,point in enumerate(points):
            if idx == len(points)-1: break #letzter Punkt ist endx/y
            startx=point[0]
            starty=point[1]
            endx=points[idx+1][0]
            endy=points[idx+1][1]
            opacity = 1.0
            linewidth = WebDiagram.DEFAULT_LINEWIDTH
            startconnector = (point[2] == 'M')
            endconnector = (points[idx+1][2] == 'M')
            dash = "8,8" if point[3]=='DASHED' else 'none'
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

def printtexte(plist):
    """beda_starttext_x,beda_starttext_y
       ,beda_starttext_breite,beda_starttext_hoehe
        ,beda_endtext_x,beda_endtext_y
        ,beda_endtext_breite,beda_endtext_hoehe
       ,beda_schriftfarbe,beda_schriftgroesse
       ,sfrom.sptx_text fromname
       ,sto.sptx_text toname
        ,beda_id
       ,beda_liniefarbe,beda_linienbreite,beda_liniedeckkraft"""
    for t in plist:
        startx = t[0]
        starty=t[1]
        starttext=t[10]
        fontcolor = t[8]
        endx=t[4]
        endy=t[5]
        endtext=t[11]
        printtext(px=startx, py=starty, ptext=starttext
                  , pfillcolor=hex2rbg(fontcolor), pfontsize=10  #vorläufig mal fix verdrahtet e[9]
                  ,pstandalone=True)
        printtext(px=endx, py=endy, ptext=endtext
                  , pfillcolor=hex2rbg(fontcolor), pfontsize=10  #vorläufig mal fix verdrahtet e[9]
                  ,pstandalone=True)
    #for
#printtexte

def forthelem(elem):
    """sortfunction returning 4 elemt in list"""
    return elem[3]
#forthelem
def print1arc(pdiagid,parcid,pentipos):
    startarcstr = """
        <g fill="none" stroke="rgb(0,0,0)" transform="translate({},{})" >
    """
    circle = """<circle stroke-dasharray="none" cx="{}" cy="{}"
            stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
    """
    endarcstr = """    
        <path d=" {}"/>
        </g>
    """
    punktabstand = 20
    bogenlng = 10
    vorhalt = 10
    arcstartx,arcstarty = pentipos[0]-punktabstand, pentipos[1]-punktabstand
    entihoehe,entibreite = pentipos[2],pentipos[3]
    enticenterx,enticentery = pentipos[0] + (entibreite / 2),pentipos[1] + (entihoehe / 2)
    arcbreite,archoehe = entibreite + (2 * (punktabstand - bogenlng)),  entihoehe + (2 * (punktabstand - bogenlng))
    print ("entiinfo",arcstartx,arcstarty,enticenterx,enticentery,arcbreite,archoehe)
    printHTML.fhtml.write(startarcstr.format(arcstartx,arcstarty))
    """select beda_id,arcstartx,arcstarty, endx,endy"""
    arcselem = web_sql.liesarcselem(pdiagid=pdiagid, parcsid=parcid)
    circles=[]
    for ae in arcselem:
        print (ae[6], ae[8],(ae[1],ae[2]),(ae[3],ae[4]),sep=', ')
        winkel = calcwinkel(ae[4], ae[2],ae[3], ae[1])
        p4 = math.pi / 4
        if winkel >= -p4 and winkel < p4: q,qwinkel=1,0
        elif winkel >= p4 and winkel < 3*p4: q,qwinkel=2,p4
        elif winkel >= 3*p4 and winkel < 5*p4: q,qwinkel=3,2*p4
        else: q,qwinkel=4,-p4
        #fi
        sortwinkel = calcwinkel(ae[2], enticentery, ae[1], enticenterx)
        #print('gelesen {}  gerechnet {}'.format(ae[9],winkel),ae[1],ae[2], sortwinkel,sep=', ')
        """print(ae, winkel / math.pi * 180
              ,ae[1] - arcstartx + round(punktabstand * math.sin(winkel),1),round(punktabstand * math.sin(winkel),1)
              ,ae[2] - arcstarty + round(punktabstand * math.cos(winkel),1),round(punktabstand * math.cos(winkel),1)
              ,ae[2],ae[4],ae[1],ae[3])"""
        circles.append([ae[1] - arcstartx + round(punktabstand * math.cos(winkel),1)
                        ,ae[2] - arcstarty  + round(punktabstand * math.sin(winkel),1)
                        ,winkel,sortwinkel,q
                        ])
    #for
    # circles sortieren, damit Pfad des arc
    #    minimal wird und nicht springt: Winkel zum Start von der Mitte der Entität aus
    circles.sort(key=forthelem)
    for c in circles:
        printHTML.fhtml.write(circle.format(c[0],c[1]))
    # for
    xfactor = {1:[0,-1],2:[1,1],3:[0,1],4:[-1,-1]}
    yfactor = {1:[-1,-1],2:[0,-1],3:[1,1],4:[0,1]}
    currentq = None
    arcline = ''
    for idx,c in enumerate(circles):
        if currentq is None:
            """1. arc beziehung"""
            currentq = c[4]
            mx = c[0] + (vorhalt * xfactor[currentq][0]) + (bogenlng * xfactor[currentq][1])
            my = c[1] + (vorhalt * yfactor[currentq][0]) + (bogenlng * yfactor[currentq][1])
            arcline += "M{} {}".format(mx,my)
            arcline += ' q{} {} {} {}'.format(bogenlng * -yfactor[currentq][0],bogenlng * xfactor[currentq][0]
                                                   ,bogenlng * -xfactor[currentq][1],bogenlng * -yfactor[currentq][1])
        else:
            qanz = (c[4] - currentq + 5) % 5-1
            for q in range(currentq,currentq + qanz ):
                qm = q if q < 5 else  q % 5 + 1
                print (c[4],currentq,qanz,q,qm)

                currentq = qm
                """ neuer Quadrant, zeichne arc um ecke q4->q1, 4->2, 4->3, 1->2, 1->3 1->4, 2->3 2->4 2->1"""
                """Linie ab aktuellem Punkt bis ans Ende der Entität"""
                x2factor = {1: [1,2,1,1], 2: [0,1,1,2], 3: [0,0,0,1], 4: [1,1,0,0]}
                if parcid == 10:
                    print(parcid)
                arcline += ' L{} {} '.format(x2factor[currentq][0]*arcbreite + x2factor[currentq][1]*bogenlng
                                        ,x2factor[currentq][2]*archoehe + x2factor[currentq][3]*bogenlng)

                """Bogen um die Ecke"""
                arcline += ' q{} {} {} {}'.format(bogenlng * -xfactor[currentq][0], bogenlng * -yfactor[currentq][0]
                                          , bogenlng * yfactor[currentq][1], bogenlng * -xfactor[currentq][1])
            #for
        #fi Beziehungen im gleichen Quadranten kann ich vergessen, ausser es ist die letzte (siehe nächsten Abschnitt)
        if idx == len(circles) - 1:
            currentq = c[4]
            print('last',currentq,c[4], c[0] , -xfactor[currentq][0], c[1] , -yfactor[currentq][0])
            """letzte Beziehung des Arc 
               Linie vom aktuellen arc-Ende bis zum Punkt + vorhalt der letzten Beziehung"""
            arcline += ' L{} {}'.format(round(c[0] + (vorhalt * -xfactor[currentq][0]),1)
                                        ,round(c[1] + (vorhalt * -yfactor[currentq][0])),1)
            """ Abschlussbogen"""
            arcline += ' q{} {} {} {}'.format(bogenlng * -xfactor[currentq][0],bogenlng * -yfactor[currentq][0]
                                            ,bogenlng * yfactor[currentq][1],bogenlng * -xfactor[currentq][1])
        #fi
    #for
    print(currentq, arcline)
    printHTML.fhtml.write(endarcstr.format(arcline))
#    printHTML.fhtml.write(endarcstr.format(""))
#    printHTML.fhtml.write(startarcstr.format(120,930))
#    printHTML.fhtml.write(circle.format(0,0))
#    printHTML.fhtml.write(circle.format(30,50))
#    printHTML.fhtml.write(circle.format(186,89))
#    printHTML.fhtml.write(endarcstr.format(
#        "M177.0 40.0 C 177.0 40.0 187.0 40.0 187.0 50.0 L187.0 100.0 C 187.0 100.0 187.0 110.0 177.0 110.0"))

#print1arc

def printarcs(pdiagid):

    """select arcs_id,beda_id"""
    arcs = web_sql.liesarcs(pdiagid=pdiagid)
    for arc in arcs:
        #print (arc)
        print1arc(pdiagid=pdiagid,parcid=arc[0],pentipos=[arc[4],arc[5],arc[6],arc[7]])
    #for
#printarcs

def printelements(pwebdiag,plang):
    entistart ="""<g  fill="{}" stroke="{}" fill-opacity="{}" stroke-opacity="{}" 
        transform="translate({},{})" >
<rect x="0" y="0" width="{}" height="{}" rx="10" ry="10" /><a href="#{}" >
<text id="{}" x="20" y="13" fill="{}" font-weight="bold"  fill-opacity="1.0" font-size="{}" stroke="none">
{} </text></a>
"""
    entiende="""</g>"""
    imagehtml=""""<image href = "image/{}.png" width = "{}px" height = "{}px" class ="entity-image" x="{}px" y="{}px"></image>""".format('{}',WebDiagram.ICONSIZE,WebDiagram.ICONSIZE,'{}','{}')

    for wenti in WebEntity.diaglist(pdiagid=pwebdiag.getid(),plang=plang):
        for eler in wenti.diagreps[pwebdiag.getid()]:
            printHTML.fhtml.write(entistart.format(hex2rbg(eler.eler_color), hex2rbg(eler.eler_margincolor)
                                               , round(eler.eler_opacity/100,2), round(eler.eler_marginopacity/100,2)
                                               , eler.eler_position_x, eler.eler_position_y, eler.eler_width, eler.eler_height
                                               , wenti.webanker().anker()
                                               , pwebdiag.webanker().anker()+ '-' + wenti.webanker().anker()
                                               , hex2rbg(eler.eler_fontcolor)
                                               , 12  #vorläufig mal fix verdrahtet e[9], font size
                                               , wenti.getname(plang=plang) + ('' if (eler.eler_index==0) else':'+str(eler.eler_index))))

        # attrs= web_sql.diagattrlist(plang=plang, pdiagid=pdiagid)
        # #  attr_id, attr_displ_name, attr_is_mandatory ,attr_is_descriptive, schluessel, mode_id
        # for a in attrs:
        #     #printtext(px=x1, py=y, ptext='*' if a[5] == 'TRUE' else 'o'
        #     #, pfillcolor=hex2rbg(e[10]), pfontsize=10  #vorläufig mal fix verdrahtet e[9]
        #     #)
        #     ax,ay=a[6],a[7]
        #     aname = a[1]
        #     printtext(px=ax-ex, py=ay-ey, ptext=printHTML.href(ref=web_sql.attrAnker(a[0]), anz=a[1])
        #               , pfillcolor=hex2rbg(e[10]), pfontsize=10  #vorläufig mal fix verdrahtet e[9]
        #               )
        # #for
            printHTML.fhtml.write(entiende)
            printHTML.fhtml.write(imagehtml.format(wenti.dbobject().enti_name.lower(),eler.eler_position_x+eler.eler_width-WebDiagram.ICONSIZE/2,
                                                   eler.eler_position_y - WebDiagram.ICONSIZE/2))

        #for
    #for
    return
    diagrela = web_sql.diagrelalist(pdiagid=pdiagid, plang=plang)
    printrela(plist=diagrela)
    printtexte(plist=diagrela)
    print ("printarcs disabled noch zu überprüfen mit")
    #printarcs(pdiagid=pdiagid)
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
    for dia in plist:
        #diag_name,diag_id,diag_legendx,diag_legendy,breite,hoehe
        printHTML.fhtml.write (diagramhead.format(dia.webanker().anker(),dia.webanker().anker(), dia.getname(plang=plang)
                                                  , dia.dbobject().diagwidth(), dia.dbobject().diagheight()))
                                #wäre clippath,legendwidth,legendhigh))

        if (dia.haslegend()):
            #es hat eine Legende
            printlegend(pdata=[dia.getname(), dia.dbobject().diag_uc, dia.dbobject().diag_dc,''
                , dia.dbobject().diag_um, ptitel, 'Logical']
                    ,pwidth=WebDiagram.LEGENDWIDTH,pheigh=WebDiagram.LEGENDHEIGHT
                    ,px=dia.dbobject().diag_legendx,py=dia.dbobject().diag_legendy)
        #fi

        printelements(pwebdiag=dia,plang=plang)
        printHTML.fhtml.write(diagramfoot)
    #for
#printcontendiag
