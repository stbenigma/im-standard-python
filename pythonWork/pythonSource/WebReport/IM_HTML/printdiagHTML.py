from IM_HTML import web_sql, printHTML
import math

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
            linewidth = 1
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
    startx,starty = pentipos[0]-punktabstand, pentipos[1]-punktabstand
    print (startx,starty)
    printHTML.fhtml.write(startarcstr.format(startx,starty))
#    printHTML.fhtml.write(circle.format(0, 0))
    """select beda_id,startx,starty, endx,endy"""
    arcselem = web_sql.liesarcselem(pdiagid=pdiagid, parcsid=parcid)
    circles=[]
    for ae in arcselem:
        winkel = calcwinkel(ae[3], ae[1],ae[4], ae[2])
        print(ae, winkel / math.pi * 180
              ,ae[1] - startx + round(punktabstand * math.sin(winkel),1),round(punktabstand * math.sin(winkel),1)
              ,ae[2] - starty + round(punktabstand * math.cos(winkel),1),round(punktabstand * math.cos(winkel),1)
              )
        circles.append([ae[1] - startx + round(punktabstand * math.sin(winkel),1)
                        ,ae[2] - starty  + round(punktabstand * math.cos(winkel),1)
                        ,winkel
                        ])
    #for
    # circles sortieren, damit Pfad des arc
    #    minimal wird und nicht springt: Winkel zum Start von der Mitte der Entität aus
    for c in circles:
        printHTML.fhtml.write(circle.format(c[0],c[1]))
    # for
    for idx,c in enumerate(circles):
        print(idx,c
              ,round(math.cos(c[2]),1),round(10.0 * math.cos(c[2]),1),c[0] - round(10.0 * math.cos(c[2]),1)
              , round(math.sin(c[2]),1), round(10.0 * math.sin(c[2]),1),c[1] - round(10.0 * math.sin(c[2]),1))
        mx, my = c[0] - round(vorhalt * math.cos(c[2]), 1), c[1] - round(vorhalt * math.sin(c[2]), 1)
        startc, endc = '', ''
        if idx == 0:
            mx,my = c[0] - round((bogenlng) * math.sin(c[2]),1) , c[1] - round((vorhalt + bogenlng) * math.sin(c[2]),1)
            startc = 'c{} {} {} {} {} {}'.format(0,0,bogenlng,0,bogenlng,bogenlng)
        elif idx == len(c)-1:
            pass
        else:
            pass
        #fi
        printHTML.fhtml.write(endarcstr.
                                format("M{} {} {} l{} {} {}".
                                       format(mx,my
                                              ,startc
                                              ,round(20.0 * math.cos(c[2]),1),round(20.0 * math.sin(c[2]),1)
                                              ,endc)))
    # for
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
        print (arc)
        print1arc(pdiagid=pdiagid,parcid=arc[0],pentipos=[arc[4],arc[5]])
    #for
#printarcs
def printelements(pdiagid,plang):
    entistart ="""<g  fill="{}" stroke="{}" fill-opacity="{}" stroke-opacity="{}" 
        transform="translate({},{})" >
<rect x="0" y="0" width="{}" height="{}" rx="10" ry="10" /><a href="#{}" >
<text id="{}" x="20" y="13" fill="{}" font-weight="bold"  fill-opacity="1.0" font-size="{}" stroke="none">
{} </text></a>
"""
    entiende="""</g>"""
    #             eled_position_x xpos,eled_breite breite
    #            ,eled_position_y ypos, eled_hoehe hoehe
    #            ,eled_deckkraft,eled_farbe
    #            ,eled_randbreite,eled_randdeckkraft,eled_randfarbe
    #            ,eled_schriftgroesse, eled_schriftfarbe
    #            ,entiname,enti_id
    elist = web_sql.diagenti(pdiagid,plang)
    if elist is None: return
    for e in elist:
        #print(e[11]+('' if (e[13]==0) else':'+str(e[13])) ,e[0],e[1],e[2],e[3])
        ex=e[0]
        ebreite=e[1]
        ey=e[2]
        ehoehe=e[3]
        printHTML.fhtml.write(entistart.format(hex2rbg(e[5]), hex2rbg(e[8])
            ,round(e[4]/100,2),round(e[7]/100,2)
            ,ex,ey,ebreite,ehoehe
            ,web_sql.entiAnker(e[12])
            ,web_sql.diagAnker(pdiagid)+'-'+web_sql.entiAnker(e[12])
            ,hex2rbg(e[10])
            ,12 #vorläufig mal fix verdrahtet e[9], font size
            ,e[11]+('' if (e[13]==0) else':'+str(e[13]))))

        attrs=web_sql.diagattrlist(plang=plang,pdiagid=pdiagid)
        #  attr_id, attr_anzname, attr_pflichtattr ,attr_deskriptor, schluessel, mode_id
        for a in attrs:
            #printtext(px=x1, py=y, ptext='*' if a[5] == 'TRUE' else 'o'
            #, pfillcolor=hex2rbg(e[10]), pfontsize=10  #vorläufig mal fix verdrahtet e[9]
            #)
            ax,ay=a[6],a[7]
            aname = a[1]
            printtext(px=ax-ex, py=ay-ey, ptext=printHTML.href(ref=web_sql.attrAnker(a[0]),anz=a[1])
                      , pfillcolor=hex2rbg(e[10]), pfontsize=10  #vorläufig mal fix verdrahtet e[9]
                      )
        #for
        printHTML.fhtml.write(entiende)
    #for
    diagrela = web_sql.diagrelalist(pdiagid=pdiagid,plang=plang)
    printrela(plist=diagrela)
    printtexte(plist=diagrela)
    printarcs(pdiagid=pdiagid)
#printelements

def printcontentdiag(plist, plang, ptitel):
    contenthead="""        <!--diagramms-->"""

    diagramhead = """        <br><hr><br><br>
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
    legendwidth = 363
    legendhigh = 128
    for dia in plist:
        #diag_name,diag_id,diag_legendx,diag_legendy,breite,hoehe
        printHTML.fhtml.write (diagramhead.format(web_sql.diagAnker(dia[1]),dia[0]
                                ,dia[4],dia[5]))
                                #wäre clippath,legendwidth,legendhigh))

        if (dia[2] is not None):
            #es hat eine Legende
            printlegend(pdata=[dia[0], dia[6], dia[7],''
                , dia[8], ptitel, 'Logical']
                    ,pwidth=legendwidth,pheigh=legendhigh
                    ,px=dia[2],py=dia[3])
        #fi

        printelements(pdiagid=dia[1],plang=plang)
        printHTML.fhtml.write(diagramfoot)
    #for
#printcontendiag
