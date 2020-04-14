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

def printcollist(ptabld):
    colhead = """             <h2>{}</h2>
                        <div id="container1">
                            <div class="table-responsive">
                   <table class="table borderless">
                                            <tbody>
                                        <tr>
                                            <th class="attribute">{}</th>
                                            <th class="attribute">{}</th>
                                            <th>{}</th>
                                            <th class="thAlgn">{}</th>
                                            <th class="thAlgn">{}</th>
                                            <th class="thAlgn">{}</th>
                                            <th class="thAlgn">{}</th>
                                            <th class="thAlgn">{}</th>
                                            <th class="thAlgn">{}</th>
                                            <th class="thAlgn">{}</th>
                                        </tr>"""
    colfoot = """              
                                </tbody>
                            </table>
                            </div>
                                </div>
    """

    colline = """                                    <tr>
                                                <td class="attribute"><a href="#{}">{}</a></td>
                                                <td class="attribute"><a href="#{}">{}</a></td>
                                                <td>{}</td>
                                                <td class="symbol"><img {}></td>
                                                <td class="symbol"><img {}></td>
                                                <td class="symbol"><img {}></td>
                                                <td class="symbol"><img {}></td>
                                                <td class="symbol"><img {}></td>
                                                <td class="symbol"><img {}></td>
                                                <td class="symbol"><img {}></td>
                                            </tr>
    """
    clist = [1]#web_sql.attrlist(p_lang=reportLang(), p_entiid=ptabld)
    if (len(clist)==0):
        return
    printHTML.fhtml.write(printHTML.starttable(ptitel='Columns', pueberschriften=[transl('Name'),transl('Wertebereich'), transl('Datentyp')]
            , pheadlevel=2))
    for a in clist:
        printHTML.fhtml.write(printHTML.writetableline(pwerte=[('x','y','z')], plineid=None))
    #for
    printHTML.fhtml.write(printHTML.endtable())
#printcollist

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
        printHTML.printcontentinfo(ptitle=transl('Informationen'),pheaders=infoheaders,pvalues=infovalues)

        printHTML.printreflist(pelemid=t.tabl_id,pelemtype='TABL')
        printHTML.printUDP(p_meltname=t.prefix().upper(), p_id=t.tabl_id)
        printmapping(ptablid=t.tabl_id)
        printcollist(ptabld=t.tabl_id)
        """
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
            <br>{}
        """
    contentheadend = """          
        </div>
        """
    if reportLang() == 'de' :
        f = """class="descr">Diese Webseite enthält den ganzen Inhalt 
            des <p2 class="IM">Relationalen Modells {}</p2> von {}. 
            Diese Seite wurde von Software von <p2 class="fyayc">foryouandyourcustomers</p2> 
            erstellt.""".format(ptitel,pfirma)
        ref = """Referenzen in Klammern sind indirekte Referenzen:<br>
                 Dokumentenreferenz bei Tabellen: Dokumente, die mit der Schnittstelle (relationales Modell) verknüpft sind<br>
                 Tabellenreferenz bei Tabellen: Indirekte Verknüpfung einer Tabelle über eine Entität zu einer anderen Tabelle<br>
                 Columnreferenz: Indirekte Verknüpfung einer Column über ein Attribut zu einer anderen Column"""
    else:
        f = """class="descr">This website contains the complete content 
            of the <p2 class="IM">Relational model {}</p2> from {}. 
            This page was created with software from <p2 class="fyayc">foryouandyourcustomers</p2>."""\
            .format(ptitel,pfirma)
        ref = """References in brackets are indirect references:<br>
                 (Document reference) for tables: Documents that are linked to the interface (relational model)<br>
                 (Table reference) for tables: Indirect linking of a table via an entity to another table<br>
                 (Column reference): Indirect linking of a column to another column via an attribute"""
    #fi
    printHTML.fhtml.write(contenthead.format(f,ref))
    printHTML.printreflist(pelemid=pschnid, pelemtype='SCHN')
    printHTML.fhtml.write(contentheadend)
#printcontenthead

def printcontent(pfirma, ptitel, pschnid):
    printcontenthead(pfirma=pfirma, ptitel=ptitel,pschnid=pschnid)
    printcontenttable(plist=Tabelle.selectbyschnid(pschnid=pschnid))
    printHTML.printcontentfoot()

#printcontent
