# -*- coding: latin-1 -*-
import sys,os
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'/../IM_db')
from datetime import date,datetime
from IM_DB import parameters,dbConnect,dbParam
from IM_OBJECTS import *


def printhtmlfile(pfirma, ptitel, pinfo, plogofilename,pfilename):
    printHTML.createFile(pfilename=pfilename)
    printHTML.printhead(p_firma=pfirma
                        , p_titel=ptitel
                        , p_info=pinfo
                        , p_logofilename=plogofilename);
    printlistofcontent();
    printcontent(pfirma=pfirma, ptitel=ptitel);
    printHTML.printfoot();
    printHTML.closefile ();


#printhtmlfile

def printhtmlsysfile(pfirma, pfilename, ptitel, pinfo, plogofilename,pschnid):
    printHTML.createFile (pfilename=pfilename)
    printHTML.printhead(p_firma=pfirma
                        , p_titel=ptitel
                        , p_info=pinfo
                        , p_logofilename=plogofilename)
    printRelHTML.printlistofcontent(pschnid)
    printRelHTML.printcontent(pfirma=pfirma, ptitel=ptitel,pschnid=pschnid)
    printHTML.printfoot();
    printHTML.closefile ();
#printhtmlsysfile

def listentitable(plang):
    
def main(pdirec, plang):
    parameters.initparam(p_callarg=pdirec)

    print ("listmapping",parameters.odmBaseDirec(),parameters.odmModelName())

    dbConnect.openDB(p_filepath= parameters.dbFilePath());
    deflang = Sprache.liesdeflangiso2()
    if deflang is not None : parameters.dbDefaultLang(deflang)
    listentitable(plang=plang)
    dbConnect.myDbConn.close()
#main

if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv)>2) else None
    main(pdirec=direc, plang=lang)