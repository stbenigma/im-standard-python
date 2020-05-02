from IM_DB import parameters,dbLookup
import os,sys,shutil,re
sys.path.append(os.getcwd())
from IM_HTML import web_sql,printHTML
from IM_OBJECTS import *

def nvl(s,default = ''):
    return printHTML.nvl(s,default)

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
                     ,ptitel=Sprachtext.transl('Mapping')
                     ,pueberschriften=(Sprachtext.transl('Model'), Sprachtext.transl('Entitäten / Tabellen'))
                     )
#printmapping

def printcolmapping(pschaid,pschnid):
    # name, list of entries mit {'name':webanker}
    werte = Schnittstelleattr.mappingto(pschaid=pschaid)
    """[[0, name, [[Attribute]]], [52, name, [[Schnittstelleattr]]]]"""
    werte = [[entry[1],
              {'('+scha.gettablname() + '.' + scha.scha_column_name+')'  if isinstance(scha,Schnittstelleattr)
                                else scha[0]\
                   : scha.webanker(pmodelid=pschnid) if isinstance(scha,Schnittstelleattr)
                                else scha[1]
                    for scha in entry[2]
               }
             ] for entry in werte
            ]
    #print(werte)
    printHTML.printmappinthtml(pwerte= werte
                     ,ptitel=Sprachtext.transl('Mapping')
                     ,pueberschriften=(Sprachtext.transl('Model'), Sprachtext.transl('Attribute / Columns'))
                     )
#printcolmapping
def printcolumninfo(pname,panker,pheaders,pvalues):
    infohead = """
          <!-- The inside div eliminates the 'jumping' animation. -->
                            <h3>{}</h3>
                            <div id="{}">
                            <div class="table-responsive">
                                <table class="table borderless">
                                    <tbody>"""
    trstart = """
                    <tr>"""
    trend = """
                      </tr>"""
    techheadline = """
                     <th>{}</th>"""
    techlineline = """
                      <td class="attribute">{}</td>"""
    infofoot = """
                    </tbody>
                    </table>
                </div>
            </div>"""
    printHTML.fhtml.write(infohead.format(pname,panker))
    printHTML.fhtml.write(trstart)
    for h in pheaders:
        printHTML.fhtml.write(techheadline.format(h))
    printHTML.fhtml.write(trstart)
    for v in pvalues:
        printHTML.fhtml.write(techlineline.format(v))
    printHTML.fhtml.write(trend)
    printHTML.fhtml.write(infofoot)
#printcolumninfo

def printcollist(pcollist,pschnid):
    colheader = """            <h2>Columns</h2>
                            <div>
    """
    colfooter= """</div>
    """
    if (pcollist is None or len(pcollist)==0): return
    printHTML.fhtml.write(colheader)
    for col in pcollist:
        if col.scha_wrtb_id is None:
            wrtbname = ''
            if col.scha_daty_id is not None:
                wrtbtyp = wrtb.typestring()
                #printHTML.anzDatentyp(Datatype().getbyid(col.scha_daty_id).daty_grundtyp)
            else:
                wrtbtyp = ''
            #fi
        else:
            wrtb = Wertebereich().getbyid(nvl(col.scha_wrtb_id,0))
            wrtbname='' if wrtb.wrtb_herkunft == Wertebereich.DERIVED else wrtb.getwrtb_name(Sprachtext.reportLang())
            wrtbtyp = wrtb.typestring()# printHTML.anzDatentyp(wrtb.wrtb_typ)
        #fi
        printcolumninfo(pname=col.scha_column_name, panker=col.webanker(pmodelid=pschnid).anker()
                        ,pheaders= [Sprachtext.transl('Beschreibung')\
                                            , Sprachtext.transl('Wertebereich'), Sprachtext.transl('Datentyp')]
                                         ,pvalues= [nvl(col.scha_beschr), wrtbname, wrtbtyp] )
        printcolmapping(pschaid=col.scha_id,pschnid=pschnid)
    #for
    printHTML.fhtml.write(colfooter)

#printcollist

def printcontenttable(plist):
    printHTML.printcontentstart ('tables')
    infoheaders = (Sprachtext.transl('auf Diagramm(en)'),Sprachtext.transl('geändert'))
    for t in plist:
        lbc = str(printHTML.newbarcounter())
        printHTML.printcontent(ptype=Sprachtext.transl('Tabelle')
                    ,panker=t.webanker().anker()
                    ,pname=t.tabl_name
                    ,pdescr=printHTML.lf2htmlbr(nvl(t.tabl_beschr))
                    ,plbc=lbc)
        infovalues = ('', nvl(t.tabl_um) + ', ' + nvl(t.tabl_dm))
        printHTML.printcontentinfo(ptitle=Sprachtext.transl('Informationen'),pheaders=infoheaders,pvalues=infovalues)

        printHTML.printreflist(pelemid=t.tabl_id,pelemtype='TABL')
        printHTML.printUDP(p_meltname=t.prefix().upper(), p_id=t.tabl_id)
        printmapping(ptablid=t.tabl_id)
        printcollist(pcollist= Schnittstelleattr.columnlist(ptablid=t.tabl_id),pschnid=t.tabl_schn_id)
        printHTML.printcontentend(lbc)
    #for
#printcontenttable

def printlistofcontent(pschnid):
    printHTML.printlistofcontenthead()
    printHTML.printlistofcontentelement(pname='Tabellen'
                                        , plist=web_sql.namelist(ptype='TABL'
                                                     , plang=Sprachtext.reportLang()
                                                    ,pid=pschnid)
                                        )
    printHTML.printlistofcontentelement(pname='Columns'
                                        , plist=web_sql.namelist(ptype='SCHA'
                                                     , plang=Sprachtext.reportLang()
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
    if Sprachtext.reportLang() == 'de' :
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
