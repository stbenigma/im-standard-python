import re,os

with (open(file="/Users/stb/Documents/Projekte/FYAYC_intern/fyyccim-tools/pythonWork/testModels/crmTest/Web/crmTest.html", mode="r")) as f:
    svgtext = f.read()

enti =re.search(r'<g.*"translate\((\d+),(\d+)\)".*\n<rect.*width="(\d+)".*rx="(\d+)".*\n.*<text id="{}-{}"[\d\D]*?</g>'.format("27E0E472","94F83ED0393E"),svgtext)
xstart,ystart,xwidth,xoffset=int(enti.groups()[0]),int(enti.groups()[1]),int(enti.groups()[2]),int(enti.groups()[3])
newenti = enti.group()
newenti = re.sub('<text id="','<a href="{}"><text id="'.format(re.escape("ENTI145")),newenti)
newenti = re.sub(r'(<text id="[\d\D]+?</text>)',r'\1</a>',newenti)
newenti = re.sub(r'(<text x=".*\n\s*{}\s*\n</text>)'.format(re.escape("ISO2_Code")),r'<a href="{}">\1</a>'.format(re.escape("ATTR123")),newenti)
newenti += '\n<image href = "image/land.png" width = "40px" height = "40px" class ="entity-image" x="210.0 {}px" y="{}px"></image>'.format(xstart+xwidth-20,ystart-20)
print (newenti)

    #"""<g[\w\W]*?translate\((\d+),(\d+)\)[\w\W]*?<text id="{}-{}"[\w\W]*?</g>)""".format("27E0E472","94F83ED0393E")
    #        ,r'\1\n<image href = "image/{}.png" width = "{}px" height = "{}px" class ="entity-image" x="\2px" y="\3px"></image>'.format(filename,ICONSIZE,ICONSIZE)
    #                         , retval)
"""<g  fill="rgb(51,255,255)" stroke="rgb(0,204,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath14_0_)" transform="translate(1710,1250)" >
<rect x="0" y="0" width="320" height="770" rx="20" ry="20" />
<a href="#ENTI159"><text id="DIAG292-ENTI159" x="121" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit
</text></a>
</g>"""