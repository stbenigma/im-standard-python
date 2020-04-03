from IM_DB import parameters,dbLookup
import os,sys,shutil,re
sys.path.append(os.getcwd())
from IM_HTML import web_sql,printHTML
from IM_OBJECTS import *

def transl(name):
    return printHTML.transl(name)
def nvl(s,default = ''):
    return printHTML.nvl(s,default)

def printmapping(ptablid):
    # name, list of entries mit {'name':webanker}
    werte = Tabelle.mappingto(ptablid=ptablid)
    """[[0, name, [[Entitaet]]], [52, name, [[Tabelle]]]]"""
    werte = [[entry[1],
              {"({})".format (tab.tabl_name if isinstance(tab,Tabelle) else '')\
                   :tab.webanker()       for tab in entry[2]
               }
             ] for entry in werte
            ]
    #print(werte)
    printHTML.printmappinthtml(pwerte= werte
                     ,ptitel=transl('Mapping (Tabellen)')
                     ,pueberschriften=(transl('Model'), transl('Entitäten / Tabellen'))
                     )
#printmapping

def printcontenttable(plist):
    printHTML.printcontentstart ('tables')
    infoheaders = (transl('auf Diagramm(en)'),transl('geändert'))
    for t in plist:
        lbc = str(printHTML.newbarcounter())
        printHTML.printcontent(ptype=transl('Tabelle')
                    ,panker=t.webanker().anker()
                    ,pname=t.tabl_name
                    ,pdescr=printHTML.lf2htmlbr(nvl(t.tabl_beschr))
                    ,plbc=lbc)
        infovalues = ('', nvl(t.tabl_um) + ', ' + nvl(t.tabl_dm))
        printHTML.printcontentinfo(pheaders=infoheaders,pvalues=infovalues)

        printHTML.printreflist(pelemid=t.tabl_id,pelemtype='TABL')
        printHTML.printUDP(p_meltname=t.prefix().upper(), p_id=t.tabl_id)
        printmapping(ptablid=t.tabl_id)
        """
        printattrlist(pentiid=enti_id)
        printentikeys(pentiid=enti_id)
        printentirela(pentiid=enti_id)
        printmapping(pentiid=enti_id)
"""
        printHTML.printcontentend(lbc)
    #for
#printcontenttable

def printlistofcontent(pschnid):
    printHTML.printlistofcontenthead()
    printHTML.printlistofcontentelement(pname='Tabellen'
                                        , plist=web_sql.namelist(ptype='TABL'
                                                     , plang=printHTML.reportLang()
                                                    ,pid=pschnid)
                                        )
    printHTML.printlistofcontentfoot()
#printlistofcontent


def printcontent(pfirma, ptitel, pschnid):
    printHTML.printcontenthead(pfirma=pfirma, ptitel=ptitel)
    printcontenttable(plist=Tabelle.selectbyschnid(pschnid=pschnid))
    printHTML.printcontentfoot()

#printcontent
