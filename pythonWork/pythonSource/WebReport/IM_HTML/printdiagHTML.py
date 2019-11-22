from IM_HTML import web_sql, printHTML


def printlegend(pdata,pwidth,pheigh,px,py):

    legenhead = """<g  fill="rgb(255,255,255)" stroke="rgb(0,0,0)" 
                fill-opacity="1.0" stroke-opacity="1.0" 
                clip-path="url(#clipPathlegend)" 
                transform="translate({},{})" >
                """
    legendentry1 = """
<rect x="0" y="0" width="{}" height="{}" />
<text x="10" y="{}" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
{}:
</text>
<text x="86" y="{}" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
{}
</text>
"""
    legendentry2 = """<line x1="0" y1="{}" x2="261" y2="{}" fill="none" stroke="rgb(0,0,0)"/>
<text x="10" y="{}" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
{}:
</text>
<text x="86" y="{}" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
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
        return "rbg(0,0,0)"
    r = int(phex[0:2], 16)
    g = int(phex[2:4], 16)
    b = int(phex[4:6], 16)
    return "rbg({},{},{})".format(r,g,b)
#hex2rbg
def printelements(pdiagid,plang):
    enti ="""<g  fill="{}" stroke="{}" fill-opacity="{}" stroke-opacity="{}" 
        clip-path="url(#clipPath34_0___dg_rm_4)" transform="translate({},{})" >
<rect x="0" y="0" width="{}" height="{}" rx="10" ry="10" /><a href="#{}" >
<text x="20" y="13" fill="{}" font-weight="bold"  fill-opacity="1.0" font-size="{}" stroke="none">
{} </text></a></g>
"""
    #             eled_position_x xpos,eled_breite breite
    #            ,eled_position_y ypos, eled_hoehe hoehe
    #            ,eled_deckkraft,eled_farbe
    #            ,eled_randbreite,eled_randdeckkraft,eled_randfarbe
    #            ,eled_schriftgroesse, eled_schriftfarbe
    #            ,entiname,enti_id
    elist = web_sql.diagenti(pdiagid,plang)
    if elist is None: return
    for e in elist:
        #print (e[5],e[8],e[10],hex2rbg(e[5]))
        print (enti.format(hex2rbg(e[5]), hex2rbg(e[8])
            ,e[4],e[7]
            ,e[0],e[1],e[1],e[3]
           ,web_sql.entiAnker(e[12]),hex2rbg(e[10]),e[9],e[11]))

        printHTML.fhtml.write(enti.format(hex2rbg(e[5]), hex2rbg(e[8])
            ,e[4],e[7]
            ,e[0],e[1],e[1],e[3]
           ,web_sql.entiAnker(e[12]),hex2rbg(e[10]),e[9],e[11]))
    #for
#printelements

def printcontentdiag(plist,plang):
    contenthead="""        <!--diagramms-->"""

    diagramhead = """        <br><hr><br><br>
       <h3 id="{}">{}</h3>
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
        version="1.1"  width="{}" height="{}">
        <defs id="dmw_defs" >
        <clipPath clipPathUnits="userSpaceOnUse" id="clipPathlegend">
             <rect x="0" y="0" width="{}" height="{}" />
        </clipPath>
        </defs>
"""
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
                                ,dia[4],dia[5]
                                ,legendwidth,legendhigh))

        if (dia[2] is not None):
            #es hat eine Legende
            printlegend(pdata=[dia[0],'*Autor','*Erstellt am','*geändert am'
                ,'*geändert von','*Modell','*modelltyp',]
                        ,pwidth=legendwidth,pheigh=legendhigh
                        ,px=dia[2],py=dia[3])
        #fi

        printelements(pdiagid=dia[1],plang=plang)
        printHTML.fhtml.write(diagramfoot)
    #for
#printcontendiag
