from IM_DB import parameters,dbLookup
import os,sys,shutil,re
sys.path.append(os.getcwd())
from IM_HTML import web_sql,printHTML

def printlistofcontent(pschnid):
    printHTML.printlistofcontenthead()
    printHTML.printlistofcontentelement(pname='Tabellen'
                                        , plist=web_sql.namelist(ptype='TABL'
                                                     , plang=printHTML.reportLang()
                                                    ,pid=pschnid)
                                        )
    printHTML.printlistofcontentfoot()
#printlistofcontent

def printcontent(pfirma, ptitel):
    pass
#printcontent
