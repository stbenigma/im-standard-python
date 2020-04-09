from IM_DB import parameters,dbLookup
import os,sys,shutil,re
sys.path.append(os.getcwd())
from IM_HTML import web_sql,printHTML
from IM_OBJECTS import *

def transl(name):
    return printHTML.transl(name)
def nvl(s,default = ''):
    return printHTML.nvl(s,default)
def reportLang(newval=None):
    return printHTML.reportLang(newval)

def printmapping(ptablid):
    # name, list of entries mit {'name':webanker}
    werte = Tabelle.mappingto(ptablid=ptablid)
    """[[0, name, [[Entitaet]]], [52, name, [[Tabelle]]]]"""
    werte = [[entry[1],
              {'('+tab.tabl_name+')'  if isinstance(tab,Tabelle)
                                else tab[0]\
                   : tab.webanker() if isinstance(tab,Tabelle)
                                else tab[1]
                    for tab in entry[2]
               }
             ] for entry in werte
            ]
    #print(werte)
    printHTML.printmappinthtml(pwerte= werte
                     ,ptitel=transl('Mapping')
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

def printcontenthead(pfirma,ptitel,pschnid):
    contenthead = """    <div class="wrapper">
        <div class="top-container">
            <p3 {} 
            </p3>
        """
    contentheadend = """          
        </div>
        """
    if reportLang() == 'de' :
        f = """class="descr">Diese Webseite enthält den ganzen Inhalt 
            des <p2 class="IM">Relationalen Modells {}</p2> von {}. 
            Diese Seite wurde von Software von <p2 class="fyayc">foryouandyourcustomers</p2> 
            erstellt.""".format(ptitel,pfirma)
    else:
        f = """class="descr">This website contains the complete content 
            of the <p2 class="IM">Relational model {}</p2> from {}. 
            This page was created with software from <p2 class="fyayc">foryouandyourcustomers</p2>."""\
            .format(ptitel,pfirma)
    #fi
    printHTML.fhtml.write(contenthead.format(f))
    printHTML.printreflist(pelemid=pschnid, pelemtype='SCHN')
    printHTML.fhtml.write(contentheadend)
#printcontenthead

def printcontent(pfirma, ptitel, pschnid):
    printcontenthead(pfirma=pfirma, ptitel=ptitel,pschnid=pschnid)
    printcontenttable(plist=Tabelle.selectbyschnid(pschnid=pschnid))
    printHTML.printcontentfoot()

#printcontent
