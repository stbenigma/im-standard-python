import os, sys
import sys
import html
sys.path.append(os.getcwd())
from IM_HTML import web_sql, printHTML
from IM_OBJECTS import *


def nvl(s, default=''):
    return printHTML.nvl(s, default)


def printmapping(ptablid):
    # name, list of entries mit {'name':webanker}
    werte = Tabelle.mappingto(ptablid=ptablid)
    """[[0, name, [[Entitaet]]], [52, name, [[Tabelle]]]]"""
    werte = [[entry[1],
              {'(' + tab.getname() + ')' if isinstance(tab, Tabelle)
                  else tab.getname(plang=Sprachtext.reportLang()) \
               : tab.webanker()
               for tab in entry[2]
               }
              ] for entry in werte
             ]
    #print('prinrelhtml->printmapping:', werte)
    printHTML.printmappinthtml(pwerte= werte
                      ,ptitel=Sprachtext.transl('Mapping')
                      ,pueberschriften=(Sprachtext.transl('Model'), Sprachtext.transl('Entitäten / Tabellen'))
                      )


# printmapping

def printcolmapping(pcolid):
    # name, list of entries mit {'name':webanker}
    werte = Schnittstelleattr.mappingto(pschaid=pcolid)
    """[[0, name, [[Attribute]]], [52, name, [[Schnittstelleattr]]]]"""
    werte = [[entry[1],
              {'(' + ref.gettablname() + '.' + ref.scha_column_name + ')' if isinstance(ref, Schnittstelleattr)\
                  else ref.getname(plang=Sprachtext.reportLang()) \
               : ref.webanker()
               for ref in entry[2]
               }
              ] for entry in werte
             ]
    # print(werte)
    printHTML.printmappinthtml(pwerte=werte
                               , ptitel=Sprachtext.transl('Mapping')
                               , pueberschriften=(Sprachtext.transl('Model'), Sprachtext.transl('Attribute / Columns'))
                               )


def getcolmapping(pschaid, pschnid):
    # name, list of entries mit {'name':webanker}
    werte = Schnittstelleattr.mappingto(pschaid=pschaid)
    """[[0, name, [[Attribut]]], [52, name, [[Schnittstelleattr]]]]"""
    werte = [[entries[1],
              {'(' + entry.gettablname() + '.' + entry.scha_column_name + ')'
               if isinstance(entry, Schnittstelleattr)
               else '(' + entry.getentiname() + '.' + entry.attr_anzname + ')' if isinstance(entry, Attribut)
              else 'unknown ' + type(entry)
               : entry.webanker().anker()
               for entry in entries[2]
               }
              ] for entries in werte
             ]
    """[['Logisches Modell', {'attrname':'ATTR1234'}],['Aurea':{'(columnname)':colwebanker}]]"""
    # print(werte)
    return werte


# getcolmapping
def printcolumninfo(pname, panker, pheaders, pvalues):
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
    printHTML.fhtml.write(infohead.format(html.escape(pname), panker))
    printHTML.fhtml.write(trstart)
    for h in pheaders:
        printHTML.fhtml.write(techheadline.format(html.escape(h)))
    printHTML.fhtml.write(trstart)
    for v in pvalues:
        printHTML.fhtml.write(techlineline.format(html.escape(v)))
    printHTML.fhtml.write(trend)
    printHTML.fhtml.write(infofoot)


# printcolumninfo

def printcollist(pcollist, pschnid):
    colheader = """            <h2>Columns</h2>
                            <div>
    """
    colfooter = """</div>
    """
    schnname = Schnittstelle.getname(pid=pschnid)
    if (pcollist is None or len(pcollist) == 0): return
    ueberschr = [Sprachtext.transl('Name'), Sprachtext.transl('Beschreibung')
        , Sprachtext.transl('Domain'), Sprachtext.transl('Datentyp')
                 ]
#    ueberschr.append('Logical Model')
#    for schn in Schnittstelle.indexlist():
#        if (schn[0] != schnname):
#            ueberschr.append(schn[0])
    printHTML.fhtml.write(printHTML.starttable(ptitel="Columns", pueberschriften=ueberschr))

    for col in pcollist:

        wrtbinfo = getwrtbinfo(pcol=col,plang=Sprachtext.reportLang())

        colwerte = [printHTML.href(ref=col.webanker().anker(),anz=col.scha_column_name)
                        , nvl(col.scha_beschr), wrtbinfo[0], wrtbinfo[1]]
        # zuerst das logical Model
        # mappings = getcolmapping(pschaid=col.scha_id, pschnid=pschnid)
        # """[['Logisches Modell', {'attrname':'ATTR1234'}],['Aurea':{'(columnname)':colwebanker}]]"""
        # colwerte.append('')  # logisches Modell
        # for maps in mappings:
        #     if (maps[0] == 'Logisches Modell'):
        #         colwerte[len(colwerte) - 1] = ', '.join(
        #             [printHTML.href(ref=val, anz=key, htmlfile=printHTML.htmlfilelist[0]) \
        #              for key, val in maps[1].items()])
        # for schn in Schnittstelle.indexlist():
        #     if (schn[0] != schnname):
        #         colwerte.append('')  # logisches Modell
        #         for maps in mappings:
        #             if (maps[0] == schn[0]):
        #                 # Aktuell noch keine Columns-Anker in Schnittstellen HTML. Darum nur der Name
        #                 # commalist = ', '.join ([printHTML.href(ref=val.anker(), anz=key, htmlfile=printHTML.htmlfilelist[val.modelid()])\
        #                 #                        for key,val in maps[1].items()])
        #                 commalist = ', '.join(key for key in maps[1].keys())
        #                 colwerte[len(colwerte) - 1] = commalist
        #
        #             # if
        #         # for
        #     # if
        # # for

        printHTML.fhtml.write(printHTML.writetableline(pwerte=colwerte))

        # printcolmapping(pschaid=col.scha_id,pschnid=pschnid)
    # for
    printHTML.fhtml.write(printHTML.endtable())


#    printHTML.fhtml.write(colfooter)
# printcollist

def printcontenttable(plist):
    printHTML.printcontentstart('tables')
    infoheaders = (Sprachtext.transl('auf Diagramm(en)'), Sprachtext.transl('geändert'))
    for t in plist:
        lbc = str(printHTML.newbarcounter())
        printHTML.printcontent(ptype=Sprachtext.transl('Tabelle')
                               , panker=t.webanker().anker()
                               , pname=t.tabl_name
                               , pdescr=printHTML.lf2htmlbr(nvl(t.tabl_beschr))
                               , plbc=lbc)
        infovalues = ('', nvl(t.tabl_um) + ', ' + nvl(t.tabl_dm))
        printHTML.printcontentinfo(ptitle=Sprachtext.transl('Informationen'), pheaders=infoheaders, pvalues=infovalues)

        printHTML.printreflist(pelemid=t.tabl_id, pelemtype=Modelelemtype.TABL)
        printHTML.printUDP(p_meltname=t.prefix().upper(), p_id=t.tabl_id)
        printcollist(pcollist=t.getcolumns(), pschnid=t.tabl_schn_id)
        printmapping(ptablid=t.tabl_id)
        printHTML.printcontentend(lbc)
    # for


# printcontenttable

def getwrtbinfo(pcol,plang):
    daty = pcol.getdaty()
    wrtbname = ''
    wrtbtyp = ''
    wrtbgrundtyp = ''
    if daty is None is not None:
        wrtbtyp = daty.daty_name
        wrtbgrundtyp = daty.daty_grundtyp
    # fi
    wrtb = pcol.getwrtb()
    if wrtb is not None:
        wrtbname = wrtb.getname(plang=plang)\
                    if wrtb.wrtb_herkunft == Domain.DERIVED \
                    else printHTML.href(ref=wrtb.webanker().anker()
                                        ,anz=html.escape(wrtb.getname(plang))
                                        ,htmlfile=printHTML.htmlfilelist[wrtb.webanker().modelid()])
        wrtbtyp = wrtb.typestring()
        wrtbgrundtyp = wrtb.displdatatype()
    # fi
    return (wrtbname,wrtbtyp,wrtbgrundtyp)


def printcontentcolumn(pcols):
    infoheaders = ('Domain','Datatype','Base Type','changed')
    for col in pcols:
        lbc = str(printHTML.newbarcounter())
        tabl = col.gettable()
        wrtbinfo = getwrtbinfo(pcol=col,plang=Sprachtext.reportLang())

        master = "<p1>{}: {}</p1><br>" \
            .format(Sprachtext.transl('Table'), printHTML.href(ref=tabl.webanker().anker(), anz=tabl.getname()))
        printHTML.printcontentstart('columns')
        printHTML.printcontent(ptype=Sprachtext.transl('Column')
                               , panker=col.webanker().anker()
                               , pname=col.scha_column_name
                               ,pmaster= master
                               , pdescr=printHTML.lf2htmlbr(nvl(col.scha_beschr))
                               , plbc=lbc)
        infovalues = (wrtbinfo[0], wrtbinfo[1],wrtbinfo[2] ,nvl(col.scha_um) + ', ' + nvl(col.scha_dm),)
        printHTML.printcontentinfo(ptitle=Sprachtext.transl('Information'), pheaders=infoheaders, pvalues=infovalues)

        printHTML.printreflist(pelemid=col.scha_id, pelemtype=Modelelemtype.INTF)
        printHTML.printUDP(p_meltname=col.prefix().upper(), p_id=col.scha_id)
        printcolmapping(pcolid=col.scha_id)
        printHTML.printcontentend(lbc)
    # for


def printlistofcontent(pschnid):
    printHTML.printlistofcontenthead()
    printHTML.printlistofcontentelement(pname='Tables'
                                        , plist=web_sql.namelist(ptype='TABL'
                                                                 , pid=pschnid)
                                        )
    printHTML.printlistofcontentelement(pname='Columns'
                                        , plist=web_sql.namelist(ptype='INTF'
                                                                 , pid=pschnid)
                                        )

    printHTML.printlistofcontentfoot()


# printlistofcontent

def printcontenthead(pfirma, ptitel, pschnid):
    contenthead = """    <div class="wrapper">
        <div class="top-container">
            <p3 {} 
            </p3>
            <br>{}
        """
    contentheadend = """          
        </div>
        """
    if Sprachtext.reportLang() == Sprachtext.DE:
        f = """class="descr">Diese Webseite enthält den ganzen Inhalt 
            des <p2 class="IM">Relationalen Modells {}</p2> von {}. 
            Diese Seite wurde von Software von <p2 class="fyayc">foryouandyourcustomers</p2> 
            erstellt.""".format(ptitel, pfirma)
        ref = """Referenzen in Klammern sind indirekte Referenzen:<br>
                 Dokumentenreferenz bei Tabellen: Dokumente, die mit der Schnittstelle (relationales Modell) verknüpft sind<br>
                 Tabellenreferenz bei Tabellen: Indirekte Verknüpfung einer Tabelle über eine Entität zu einer anderen Tabelle<br>
                 Columnreferenz: Indirekte Verknüpfung einer Column über ein Attribut zu einer anderen Column"""
    else:
        f = """class="descr">This website contains the complete content 
            of the <p2 class="IM">Relational model {}</p2> from {}. 
            This page was created with software from <p2 class="fyayc">foryouandyourcustomers</p2>.""" \
            .format(ptitel, pfirma)
        ref = """References in brackets are indirect references:<br>
                 (Document reference) for tables: Documents that are linked to the interface (relational model)<br>
                 (Table reference) for tables: Indirect linking of a table via an entity to another table<br>
                 (Column reference): Indirect linking of a column to another column via an attribute"""
    # fi
    printHTML.fhtml.write(contenthead.format(f, ref))
    printHTML.printreflist(pelemid=pschnid, pelemtype='INTF')
    printHTML.fhtml.write(contentheadend)


# printcontenthead

def printcontent(pfirma, ptitel, pschnid):
    printcontenthead(pfirma=pfirma, ptitel=ptitel, pschnid=pschnid)
    printcontenttable(plist=Tabelle.selectbyschnid(pschnid=pschnid))
    printcontentcolumn(pcols=Schnittstelleattr.selectbyschnid(pschnid=pschnid))
    printHTML.printcontentfoot()

# printcontent
