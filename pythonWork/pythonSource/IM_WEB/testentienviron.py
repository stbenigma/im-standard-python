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
        if entiid not in ("ENTI315","ENTI313","ENTI316","ENTI318","ENTI307","ENTI335","ENTI329"): continue
        enti =jsmodel.getelements(pelemtype=Modelelemtype.ENTI)[entiid]
        print (entiid,enti['name'][plang],enti["roles+"],enti['subtypes+'],enti["supertypes+"],enti["relations+"])
        entienvir = entityenviron.createentienvironment(pentiid=entiid,pjson=jsmodel,pmodellang=modellang)
        for hkey in range(entienvir.getminhkey(),entienvir.getmaxhkey()+1):
            line = str(hkey).ljust(4)+': '
            for vkey in range(-1,2):
                line += ' | '+entityenviron.nvl(entienvir.getcell(phidx=hkey,pvidx=vkey).getentiname()).ljust(20)[:20]
            print (line)
        #if idx > 10: break
# main


if __name__ == '__main__':
    main(pjson=sys.argv[1],
         plang='de' if len(sys.argv) <= 2 else sys.argv[2])
