# -*- coding: latin-1 -*-
import sys
from IM_OBJECTS import Modelelemtype
from IM_JSON import JSModel
from IM_HTML import entityenviron

# Main Programm
def main(pjson, plang):
    jsmodel = JSModel.readfromfile(pfilename=pjson)
    modellang = jsmodel.getelements(pelemtype='PROJ')["language"] if plang is None else plang

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
        print (entityenviron.entienviro2svg(penviron = entienvir))
    #for

# main


if __name__ == '__main__':
    main(pjson=sys.argv[1],
         plang='de' if len(sys.argv) <= 2 else sys.argv[2])
