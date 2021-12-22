# -*- coding: latin-1 -*-
import sys,os
from IM_OBJECTS import Modelelemtype
from IM_JSON import JSModel
from IM_HTML import entityenviron


def createFile(pfilename):
    webfile = pfilename
    if os.path.exists(webfile):
        os.remove(webfile)
    fhtml = open(webfile, 'w')
    return fhtml


def main(pjson, plang):
    jsmodel = JSModel.readfromfile(pfilename=pjson)
    model =jsmodel.getelements(pelemtype=JSModel.ELEMTYPE_PROJ)
    modellang = model["language"] if plang is None else plang

    for idx, entiid in enumerate(jsmodel.getelements(pelemtype=Modelelemtype.ENTI).keys()):
        #if entiid not in ("ENTI315","ENTI313","ENTI316","ENTI318","ENTI307","ENTI335","ENTI329"): continue
        enti =jsmodel.getelements(pelemtype=Modelelemtype.ENTI)[entiid]
        entienvir = entityenviron.createentienvironment(pentiid=entiid,pjson=jsmodel,pmodellang=modellang)
        #print (entiid,enti['name'][plang],enti["roles+"],enti['subtypes+'],enti["supertypes+"],enti["relations+"],entienvir.getminvkey(),entienvir.getmaxvkey())
        for vkey in range(entienvir.getminvkey(),entienvir.getmaxvkey()+1):
            line = str(vkey).ljust(4)+': '
            cellleft = entienvir.getcell(phidx='left', pvidx=vkey)
            cellcenter = entienvir.getcell(phidx='center', pvidx=vkey)
            cellright = entienvir.getcell(phidx='right', pvidx=vkey)
            #print ('**',vkey,cellleft,cellcenter,cellright,line)

            if cellleft.gettype() == entityenviron.EntityCell.SUPER:
                line += ' | '+entityenviron.nvl(cellleft.getentiname()).ljust(20)[:20]
            elif cellcenter.gettype() == entityenviron.EntityCell.PARENT:
                line += ' | ' + entityenviron.nvl(cellcenter.getentiname()).ljust(20)[:20]
            else:
                line += ' | ' + ' '.ljust(20)
            #fi
            if cellcenter.gettype() == entityenviron.EntityCell.CENTER:
                line += ' | '+entityenviron.nvl(cellcenter.getentiname()).ljust(20)[:20]
            elif cellcenter.gettype() == entityenviron.EntityCell.PARENT:
                line += ' | ' + entityenviron.nvl(cellcenter.getassoc()).ljust(20)[:20]
            elif cellcenter.gettype() == entityenviron.EntityCell.CHILD:
                line += ' | ' + entityenviron.nvl(cellcenter.getassoc()).ljust(20)[:20]
            else:
                line += ' | ' + ' '.ljust(20)
            #fi
            if cellright.gettype() == entityenviron.EntityCell.ROLE:
                line += ' | '+entityenviron.nvl(cellright.getentiname()).ljust(20)[:20]
            elif cellcenter.gettype() == entityenviron.EntityCell.CHILD:
                line += ' | ' + entityenviron.nvl(cellcenter.getentiname()).ljust(20)[:20]
            else:
                line += ' | ' + ' '.ljust(20)
            #fi
            print(line)
        #for
        #if idx > 10: break
        print()
        #print (entityenviron.entienviro2svg(penviron = entienvir))

    #for
    path = os.path.dirname(pjson)
    with createFile(path + '/' + 'svgtest' + '.html') as svgfile:
        svgfile.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <title>crmTest (de)</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" type="image/png" href="image/imicon.png">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="css/main.css">
    <script src="js/IM.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>

<body>""")
        for idx, entiid in enumerate(jsmodel.getelements(pelemtype=Modelelemtype.ENTI).keys()):
            enti =jsmodel.getelements(pelemtype=Modelelemtype.ENTI)[entiid]
            entienvir = entityenviron.createentienvironment(pentiid=entiid,pjson=jsmodel,pmodellang=modellang)
            svgfile.write("<h2>{}</h2>".format (entiid))
            svgfile.write(entityenviron.entienviro2svg(pentiid=entiid,penviron=entienvir))
        #for
        svgfile.write("""</body>    </html>""")
    # with

#main

def maindraw(pjson, plang):
    jsmodel = JSModel.readfromfile(pfilename=pjson)
    model =jsmodel.getelements(pelemtype=JSModel.ELEMTYPE_PROJ)
    modellang = model["language"] if plang is None else plang
    for idx, entiid in enumerate(jsmodel.getelements(pelemtype=Modelelemtype.ENTI).keys()):
        enti =jsmodel.getelements(pelemtype=Modelelemtype.ENTI)[entiid]
        if enti["name"]["de"]!= "Land": continue
        entienvir = entityenviron.createentienvironment(pentiid=entiid,pjson=jsmodel,pmodellang=modellang)
        print (entityenviron.generate_drawio_content(penviron=entienvir))
    return
if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv)>2) else None
    #main(pjson=direc, plang=lang)
    maindraw(pjson=direc, plang=lang)

