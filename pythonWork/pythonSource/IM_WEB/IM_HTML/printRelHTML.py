import os
import sys
import html
sys.path.append(os.getcwd())
from IM_HTML import printHTML
from IM_DB import parameters
from IM_OBJECTS import Domain,Languagetext,Modelelemtype


def nvl(s, default=''):
    return parameters.nvl(s, default)

getelement = lambda e:printHTML.model.getbyid(e)

def printmapping(pelem):
    # name, list of entries mit {webanker:'name'}
    entities = {e:getelement(e)['name'][parameters.dbDefaultLang()] for e in pelem['entitiesmapped']}
    werte = {0: [[anker, name] for anker,name in entities.items()]}

    for intfanker,intfelem in printHTML.model.jsmodel['systems'].items():
        if intfanker == pelem['interface-id+']: continue
        tablist=[]
        for enti in pelem['entitiesmapped']:
            try:
                tablist += getelement(enti)['tablesmapped+'][intfanker]
            except:
                pass
        if len(tablist) == 0: continue
        werte[intfanker] = [[tabanker,"({})".format(getelement(tabanker)['name'])] for tabanker in tablist]
    #for
    printHTML.printmappinghtml(ptitel=Languagetext.transl('Mapping')
                               , pueberschriften=(Languagetext.transl('Model'), Languagetext.transl('Entitäten / Tabellen'))
                               ,pwerte = werte)
# printmapping

def printcolmapping(pcol):
    lang=parameters.dbDefaultLang()
    attrs = {a:getelement(a) for a in pcol['attributes-mapped']}
    attrlist = []
    for anker,attr in attrs.items():
        if attr['entity'] is None:
            attrlist.append([anker, "{}.{}".format(getelement(attr['relation'])['name']
                                        ,attr['name'][lang])])
        else :
            attrlist.append([anker, "{}.{}".format(getelement(attr['entity'])['name'][lang]
                                               , attr['name'][lang])])
        #fi
    #for
    werte = {0 : attrlist}
    for intfanker,intfelem in printHTML.model.jsmodel['systems'].items():
        if intfanker == pcol['interface-id+']: continue
        collist=[]
        for attr in pcol['attributes-mapped']:
            try:
                collist += getelement(attr)['columnsmapped+'][intfanker]
            except:
                pass
        if len(collist) == 0: continue
        col = lambda c:getelement(c)
        werte[intfanker] = [[colanker,"({}.{})".format(col(colanker)['table-name+']
                                             ,col(colanker)['name'])]
                            for colanker in collist
                            ]
    #for
    printHTML.printmappinghtml(ptitel=Languagetext.transl('Mapping')
                               , pueberschriften=(Languagetext.transl('Model'), Languagetext.transl('Attribute / Columns'))
                               ,pwerte=werte
                               )

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

def printcollist(pcollist):
    colheader = """            <h2>Columns</h2>
                            <div>
    """
    colfooter = """</div>
    """
    lang = parameters.dbDefaultLang()
    if (pcollist is None or len(pcollist) == 0): return
    ueberschr = [Languagetext.transl('Name'), Languagetext.transl('Beschreibung')
        , Languagetext.transl('Wertebereich'), Languagetext.transl('Datentyp')
                 ]
    lbc = str(printHTML.newbarcounter())
    printHTML.fhtml.write(printHTML.starttable(ptitle="Columns", pheaders=ueberschr, plbc=lbc))

    for col in pcollist:
        column = getelement(col)
        domain = getelement(column['domain'])
        colwerte = [printHTML.href(ref=col,anz=column['name'])
                        , nvl(column['descr']), domain['name'][lang], nvl(column['datatype'])]
        printHTML.fhtml.write(printHTML.writetableline(pwerte=colwerte))
    # for
    printHTML.fhtml.write(printHTML.endtable(plabel='Columns',plbc=lbc))
# printcollist

def printcontenttable(pintf):
    tablist = sorted([[anker,getelement(anker)] for anker in pintf['tables+']]
                     ,key=lambda val:val[1]['name'].upper()
                     )
    printHTML.printcontentstart('tables')
    infoheaders = (Languagetext.transl('auf Diagram(en)'), Languagetext.transl('geändert'))
    for t in tablist:
        anker = t[0]
        elem = t[1]
        lbc = str(printHTML.newbarcounter())
        printHTML.printcontent(ptype=Languagetext.transl('Table')
                               , panker=anker
                               , pname=elem['name']
                               , pdescr=printHTML.lf2htmlbr(nvl(elem['descr']))
                               , plbc=lbc)
        infovalues = ('', nvl(elem['um']) + ', ' + nvl(elem['dm']))
        printHTML.printcontentinfo(ptitle=Languagetext.transl('Informationen'), pheaders=infoheaders, pvalues=infovalues)

        printHTML.printelemreflists(pelem=elem, pelemtype=Modelelemtype.TABL)
        printHTML.printUDP(pelem=elem)
        printcollist(pcollist=elem['columns+'])
        printmapping(pelem=elem)
        printHTML.printcontentend(lbc)
    # for
# printcontenttable

def printcontentcolumn(pintf):
    lang = parameters.dbDefaultLang()
    infoheaders = ('Domain','Datatype','Base Type','changed')
    collist = sorted([[anker,elem] for anker,elem in printHTML.model.jsmodel['columns'].items() if elem['interface-id+'] == pintf['interface-id+'] ]
                    ,key=lambda val:val[1]['name'].upper()
                     )
    for col in collist:
        colanker,colelem = col[0],col[1]
        lbc = str(printHTML.newbarcounter())
        domain = getelement(colelem['domain'])
        master = "<p1>{}: {}</p1><br>".format(colelem['name'],colelem['table-name+'])
        printHTML.printcontentstart('columns')
        printHTML.printcontent(ptype=Languagetext.transl('Column')
                               , panker=colanker
                               , pname=colelem['name']
                               ,pmaster= printHTML.href(ref=colelem['table-id'],anz=colelem['table-name+'])
                               , pdescr=printHTML.lf2htmlbr(nvl(colelem['descr']))
                               , plbc=lbc)
        infovalues = (domain['name'][lang] if domain['origin']== Domain.DERIVED \
                        else printHTML.href(ref=colelem['domain'],anz=domain['name'][lang]
                                     ,htmlfile='' if domain['interfaceid'] is not None else printHTML.htmlfilelist[0],pself=True
                                            )
                        ,domain['displdatatype+'][lang],domain['basedatatype+']
                        ,nvl(colelem['um']) + ', ' + nvl(colelem['dm']))
        printHTML.printcontentinfo(ptitle=Languagetext.transl('Information'), pheaders=infoheaders, pvalues=infovalues)

        printHTML.printelemreflists(pelem=colelem, pelemtype=Modelelemtype.COLU)
        printHTML.printUDP(pelem=colelem)
        printcolmapping(pcol=colelem)
        printHTML.printcontentend(lbc)
    # for

def printcontentdomain(pintf):
    pass

def printlistofcontent(pintf):
    printHTML.printlistofcontenthead()
    idxlist = sorted([{'anker':key,'name': value['name']}
                     for key,value in printHTML.model.jsmodel['tables'].items() if key in pintf['tables+']]
                     ,key=lambda val:val['name'].upper())
    printHTML.printlistofcontentelement(pname='Tables'
                                         , plist=idxlist)
    idxlist = sorted([{'anker':key,'name': "{} ({})".format(value['name'],value['table-name+'])}
                     for key,value in printHTML.model.jsmodel['columns'].items() if value['interface-id+'] == pintf['interface-id+']]
                     ,key=lambda val:val['name'].upper())
    printHTML.printlistofcontentelement(pname='Columns'
                                         , plist=idxlist
                                         )

    idxlist = sorted([{'anker':key,'name': "{}".format(value['name'])}
                     for key,value in printHTML.origindomains(pintfid=pintf['interface-id+']).items()]
                     ,key=lambda val:val['name'].upper())
    printHTML.printlistofcontentelement(pname='Domains'
                                         , plist=idxlist
                                         )

    printHTML.printlistofcontentfoot()


# printlistofcontent

def printcontenthead(pfirma, ptitel, pintf):
    contenthead = """    <div class="wrapper">
        <div class="top-container">
            <p3 {} 
            </p3>
            <br>{}
        """
    contentheadend = """          
        </div>
        """
    if Languagetext.reportLang() == Languagetext.DE:
        f = """class="descr">Diese Webseite enthält den ganzen Inhalt 
            des <p2 class="IM">Relationalen Modells {}</p2> von {}. 
            Diese Seite wurde von Software von <p2 class="fyayc">foryouandyourcustomers</p2> 
            erstellt.""".format(ptitel, pfirma)
        ref = """Referenzen in Klammern sind indirekte Referenzen:<br>
                 Tabellenreferenz bei Tabellen: Indirekte Verknüpfung einer Table über eine Entität zu einer Table einer anderen Interface<br>
                 Columnreferenz: Indirekte Verknüpfung einer Column über ein Attribute zu einer Column in einer anderen Interface"""
    else:
        f = """class="descr">This website contains the complete content 
            of the <p2 class="IM">Relational model {}</p2> from {}. 
            This page was created with software from <p2 class="fyayc">foryouandyourcustomers</p2>.""" \
            .format(ptitel, pfirma)
        ref = """References in brackets are indirect references:<br>
                 (Table reference) for tables: Indirect linking of a table via an entity to a table in another interface<br>
                 (Column reference): Indirect linking of a column via an attribute to a column  in another interface"""
    # fi
    printHTML.fhtml.write(contenthead.format(f, ref))
    printHTML.printelemreflists(pelem=pintf, pelemtype=Modelelemtype.INTF)
    printHTML.fhtml.write(contentheadend)
# printcontenthead

def printcontent(pfirma, ptitel, pintf):
    printcontenthead(pfirma=pfirma, ptitel=ptitel, pintf=pintf)
    printcontenttable(pintf=pintf)
    printcontentcolumn(pintf=pintf)
    printHTML.printcontentdoma(pdomains= printHTML.origindomains(pintfid= pintf['interface-id+']))
    printHTML.printcontentfoot()

# printcontent
