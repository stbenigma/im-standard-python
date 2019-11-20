from IM_HTML import web_sql, printHTML


def printlegend(pdiagname,pwidth,pheigh):

    legenhead = """<g  fill="rgb(255,255,255)" stroke="rgb(0,0,0)" 
                fill-opacity="1.0" stroke-opacity="1.0" 
                clip-path="url(#clipPath271_0___dg_rm_4)" 
                transform="translate(10,10)" >
                """
    legendentry1 = """
<rect x="0" y="0" width="{}" height="{}" />
<text x="{}" y="{}" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
{}:
</text>
<text x="{}" y="{}" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
{}
</text>
"""
    legendentry2 = """<line x1="0" y1="19" x2="261" y2="19" fill="none" stroke="rgb(0,0,0)"/>
<text x="10" y="32" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Author:
</text>
<text x="86" y="32" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
stb
</text>
"""
    """<line x1="0" y1="37" x2="261" y2="37" fill="none" stroke="rgb(0,0,0)"/>
<text x="10" y="50" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Created on:
</text>
<text x="86" y="50" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
2019-02-03 11:51:30 UTC
</text>
<line x1="0" y1="55" x2="261" y2="55" fill="none" stroke="rgb(0,0,0)"/>
<text x="10" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Modified on:
</text>
<text x="86" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
2019-09-12 14:29:23 UTC
</text>
<line x1="0" y1="73" x2="261" y2="73" fill="none" stroke="rgb(0,0,0)"/>
<text x="10" y="86" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Modified by:
</text>
<text x="86" y="86" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
stb
</text>
<line x1="0" y1="91" x2="261" y2="91" fill="none" stroke="rgb(0,0,0)"/>
<text x="10" y="104" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Design:
</text>
<text x="86" y="104" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
ModellModell
</text>
<line x1="0" y1="109" x2="261" y2="109" fill="none" stroke="rgb(0,0,0)"/>
<text x="10" y="122" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Model:
</text>
<text x="86" y="122" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Logical
</text>
"""
    legendfoot= """</g>
"""
    startx=10
    starty=14
    printHTML.fhtml.write('TEST')
    printHTML.fhtml.write(legenhead)
    printHTML.fhtml.write(legendentry1.format(pwidth,pheigh
                                    ,startx,starty,'Diagram'
                                    ,startx + 76,starty,pdiagname))
    printHTML.fhtml.write(legendfoot)


#printlegend
def printcontentdiag(plist):
    contenthead="""        <!--diagramms-->"""

    contentelementhead = """        <br><hr><br><br>
       <h3 id="{}">{}</h3>
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
        version="1.1"  width="1252" height="1778">
        <defs id="dmw_defs" >
        <svg id="fk_sym" viewBox="0 0 48.665 48.665" style="enable-background:new 0 0 48.665 48.665;" >
"""
    contentelementfoot = """
<g>
<path d="M40.332,31.592c-2.377,0-4.515,1-6.033,2.598l-17.737-8.686c0.061-0.406,0.103-0.82,0.103-1.246    c0-0.414-0.04-0.818-0.098-1.215l17.711-8.589c1.519,1.609,3.666,2.619,6.054,2.619c4.603,0,8.333-3.731,8.333-8.333    c0-4.603-3.73-8.333-8.333-8.333s-8.333,3.73-8.333,8.333c0,0.414,0.04,0.817,0.098,1.215l-17.709,8.589    c-1.519-1.609-3.666-2.619-6.054-2.619C3.73,15.925,0,19.656,0,24.258c0,4.603,3.73,8.333,8.333,8.333    c2.377,0,4.515-1,6.033-2.596l17.736,8.685c-0.062,0.406-0.104,0.82-0.104,1.245c0,4.604,3.73,8.333,8.333,8.333    s8.333-3.729,8.333-8.333C48.665,35.322,44.935,31.592,40.332,31.592z" fill="#13bf3b"/>
</g>
</svg>
</defs>
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
    for dia in plist:
        printHTML.fhtml.write (contentelementhead.format(web_sql.diagAnker(dia[1]),dia[0]))

        printlegend(pdiagname=dia[0],pwidth=262,pheigh=127)
        printHTML.fhtml.write(contentelementfoot)
#printcontendiag
