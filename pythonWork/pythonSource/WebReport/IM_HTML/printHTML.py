from IM_DB import parameters,dbLookup
import os,shutil,re
from IM_HTML import web_sql

outputDirectory:str = None
webDirectory:str = "";
webFileName:str = "";
webFileNamePath:str = "";
libSourceDirec:str = "";
imagedirec:str = "";
cssdirec:str = "";
icondirec:str = "";

"""zum Zählen der lokaen Ziele für collapse"""
barcounter:int = 0
def newbarcounter():
    global barcounter
    barcounter += 1
    return barcounter
#newbarcounter

fhtml = None

greportLang:str = None
def reportLang(newval=None):
    global greportLang
    if (newval is None):
        return greportLang
    else:
        greportLang = newval
#reportLang




def nvl(x,default=''):
    return x if (x is not None) else default
#nvl

def href(ref,anz):
    return """<a href="#{}" target="details">{}</a>""".format(ref,anz)
#href

def isiconstr(w):
    if (w is None) or (type(w) != str ):
        return False
    elif (w.startswith('class="')):
        return True
    else:
        return False
#isiconstr
translNameEN = {'Anzeige': 'Display'
                ,'Arc': 'Arc'
                ,'Anzeige': 'Display'
                ,'Attribut': 'Attribute'
                ,'Attribut(e)': 'Attribute(s)'
                ,'Attribute': 'Attributes'
                , 'Attributgruppe': 'Attribut group'
                ,'auf Diagramm(en)':'on diagram(s)'
                ,'Author': 'Author'
                ,'Beschreibung': 'Description'
                ,'Beziehung': 'Relationship'
                ,'Beziehung(en)': 'relationship(s)'
                ,'Beziehungen': 'Relationships'
                ,'Benutzerdefinerte Eigenschaften': 'User defined properties'
                ,'Bild' : 'Picture'
                ,'Binär': 'Binary'
                ,'Datentyp': 'Datatype'
                ,'Deskriptor': 'descriptor'
                ,'Domänen': 'Domains'
                ,'Diagramm': 'Diagram'
                ,'Diagramme': 'Diagrams'
                ,'Domäne': 'Domain'
                ,'Einheit' : 'Unit'
                ,'Element': 'Element'
                ,'Elemente': 'Elements'
                ,'Entität': 'Entity'
                ,'Entität/Tabelle': 'Entity/Table'
                ,'Entitäten': 'Entities'
                ,'erstellt': 'created'
                ,'Film' : 'Video'
                ,'geändert': 'updated'
                ,'Gruppenattribut': 'Groupattribute'
                ,'Grafik' : 'Graphic'
                ,'Granularität' : 'Granularity'
                ,'historisiert': 'historicized'
                ,'in Schlüssel': 'within key'
                ,'Informationsmodell {} (Stand: {})': 'Informationmodel {} (Status: {})'
                ,'Inhaltstyp' : 'Content type'
                ,'Ja': 'Yes'
                ,'Jahr' : 'year'
                ,'Max. Länge' : 'Max. length'
                ,'Max. Wert' : 'Max. value'
                ,'Mehr': 'more'
                ,'Millisekunde' : 'millisecond'
                ,'Minute' : 'minute'
                ,'Min. Wert' : 'Min. value'
                ,'Monat' : 'month'
                ,'Nachkommast.' : 'digits after period'
                ,'Name': 'Name'
                ,'Nein': 'No'
                ,'Nr': 'Nr'
                ,'Numerisch': 'Numerical'
                ,'Pflichtattribut': 'Attribute of duty'
                ,'Quartal' : 'quarter'
                ,'Rundungseinh.' : 'rounding unit'
                ,'Schlüssel': 'Key'
                ,'Sekunde' : 'second'
                ,'Semester' : 'half-year'
                ,'Sort': 'Sort'
                ,'Stunde' : 'hour'
                ,'Subentität': 'Subentity'
                ,'Subentitäten': 'Subentities'
                ,'Suchbegriff': 'search key'
                ,'Superentität': 'Superentity'
                ,'Synonyme': 'Synonyms'
                ,'Syntaxregel' : 'Syntax rule'
                ,'Tag' : 'day'
                ,'Technischer Name': 'Technical Name'
                ,'Text': 'Text'
                ,'Ton' : 'Sound'
                ,'Tooltip': 'Tooltip'
                ,'Treffer': 'Hits'
                ,'Typ': 'Type'
                ,'UDP-Matrix': 'UDP-Matrix'
                ,'übersetzt': 'translated'
                ,'verschlüsselt': 'encrypted'
                ,'Verwendet für Attribute':'Used for attributes'
                ,'Verwendet in Attributgruppen':'Used in attribute groups'
                ,'Verwendet von': 'used by'
                ,'Vorkommast.' : 'digits before period'
                ,'Wert': 'Value'
                ,'Wertebereich': 'Domain'
                ,'Werteliste': 'List of values'
                ,'wiederholt': 'repeated'
                ,'Woche' : 'week'
                ,'Zeitpunkt': 'Point in Time'
                }
def transl(pname):
   if (greportLang == 'de'):
       return pname
   elif (greportLang == 'en'):
       try:
           return translNameEN[pname]
       except:
           return pname
   else:
       return pname
#transl


def bool2icon(b):
    lb = b if (type(b) == bool) else True if (b == 'TRUE') else False
#    print (b,lb,type(b))
    return       'class="symbol"><img class="icon-check" src="icons/checkmark.svg"'  \
       if lb else 'class="symbol"><img class="icon-remove" src="icons/cross.svg"'
#bool2icon

def arrow2icon(direc):
    if (direc == 'up'):
        return 'class="leftsymbol"><img class="icon-up" src="icons/uparrow.svg"'
    elif (direc == 'down'):
       return 'class="leftsymbol"><img class="icon-down" src="icons/downarrow.svg"'
    else:
        return direc
#arrow2icon

def anzDatentyp(dt):
    anzDT = {'BIN': transl('Binär')
             ,'GRP': transl('Gruppenattribut')
             ,'LOV': transl('Werteliste')
             ,'NUM': transl('Numerisch')
             ,'TEXT': transl('Text')
             ,'ZPKT': transl('Zeitpunkt')}
    return anzDT[dt]
#anzDatentyp

def anzinhalttyp(dt):
    anzDT = {'BILD': transl('Bild')
             ,'FILM': transl('Film')
             ,'GRAPH': transl('Grafik')
             ,'TEXT': transl('Text')
             ,'TON': transl('Ton')}
    return anzDT[dt]
#anzinhalttyp
def anzgranul(dt):
    anzDT = {
    'JAHR' : transl('Jahr'),
    'MILLISEKUNDE' : transl('Millisekunde'),
    'MINUTE' : transl('Minute'),
    'MONAT' : transl('Monat'),
    'QUARTAL' : transl('Quartal'),
    'SEKUNDE' : transl('Sekunde'),
    'SEMESTER' : transl('Semester'),
    'STUNDE' : transl('Stunde'),
    'TAG' : transl('Tag'),
    'WOCHE' : transl('Woche')
    }
    return anzDT[dt]
#anzgranul



def list2href(p_list):
    """Verandelt eine kommagetrennte Liste von nnn:xxxx in einen String von kommagetrennten  HREF-Webeinträgen"""
    list = p_list.split(",")
    elem = []
    for el in list:
        el1  = el.split(':')
        elem.append(href(ref=web_sql.entiAnker(el1[0]), anz=el1[1]))
    return ', '.join(elem)
#list2href

contentelementfoot:str = """                 <div class="panel">
                <div class="panel-heading collapsed" data-toggle="collapse" data-target="#bar{}">
                    <img class="icon-chevron-up" alt="minus" src="icons/chevron-up.svg">
                    <img class="icon-chevron-down" alt="plus" src="icons/chevron-down.svg">
                    <label class="label1">{}</label>
                </div>
            </div>
        </div>
        </div>
    """

def printhead(p_firma,p_titel,p_info,p_logofilename):
    htmlhead:str = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>{}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="css/main.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

</head>

<body>

    <div class="header" id="TopBar">
        <p4>{}</p4>
        <p4>{}</p4>
        <p5>{}</p5>
        <img src="image/{}" alt="{}" id="LLogo">
    </div>
    """.format (p_titel,p_firma,p_titel,p_info,p_logofilename,p_firma)
    fhtml.write(htmlhead)
#printhead

def printfoot():
    htmlend:str = """    <!-- modal für mobile devices (search) -->
    <div class="modal" id="MobileSearch" tabindex="-1" role="dialog" aria-hidden="true">
        <div class="modal-dialog modal-full" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Filter</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close" id="closeM0">
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <div class="modal-body" id="modalContent">
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal" id="closeM1">OK</button>
                </div>
            </div>
        </div>
    </div>
        
    <script>
        //Code for filtering input
        function $x(pNd) {
            var lThis;
            switch (typeof(pNd)) {
                case 'string':
                    lThis = document.getElementById(pNd);
                    break;
                case 'object':
                    lThis = pNd;
                    break;
                default:
                    return false;
                    break;
            }
            return (lThis.nodeType == 1) ? lThis : false;
        }

        var gRegex = false;
        var gHeight = 0;

        function $d_Find(pThis, pString, pTags, pClass) {
            if (!pTags) {
                pTags = 'DIV';
            }
            pThis = $x(pThis);
            if (pThis) {
                var d = pThis.getElementsByTagName(pTags);
                pThis.style.display = "none";
                if (!gRegex) {
                    gRegex = new RegExp("test");
                }
                var c = 0; // Versuch eines Counters für die Resultate
                //var e = 0; //
                var rowCount = 0;
                gRegex.compile(pString, "i");
                for (var i = 0, len = d.length; i < len; i++) {
                    if (gRegex.test(d[i].innerHTML)) {
                        d[i].style.display = "table-row";
                        d[i].style.visiblilty = "visible";
                        d[i].style.height = gHeight;
                        c++; // 
                    } else {
                        if (gHeight == 0) gHeight = d[i].style.height;
                        d[i].style.height = '0';
                        d[i].style.display = "none";
                        d[i].style.visiblilty = "hidden";
                    }

                }
                pThis.style.display = "block";
            }
            document.getElementById("count").innerHTML = c;
            return;
        }

        //placeholder animation
        $('input').focus(function() {
            $(this).parents('.form-group').addClass('focused');
        });

        $('input').blur(function() {
            var inputValue = $(this).val();
            if (inputValue == "") {
                $("#searcher").show();
                $(this).removeClass('filled');
                $(this).parents('.form-group').removeClass('focused');
            } else {
                $(this).addClass('filled');
            }
        })

        //serchclearer 
        $(document).ready(function() {
            $("#first").keyup(function() {
                $("#searchclear").toggle(Boolean($(this).val()));
                $("#searcher").hide();
            });
            $("#searchclear").toggle(Boolean($("#first").val()));
            $("#searchclear").click(function() {
                $("#searcher").show();
                $("#first").val('').focus();
                $(this).hide();
            });
        });


        //content view for sidebar(desktop) and modal (mobile)
        document.getElementById("btnF").addEventListener("click", function() {

            $("body").css("overflow", "hidden");

            var tree = document.createDocumentFragment();
            var div = document.getElementById("toc_list");

            tree.appendChild(div);

            document.getElementById("modalContent").appendChild(tree);
        });

        document.getElementById("closeM0").addEventListener("click", function() {
            $("body").css("overflow", "auto");

            var tree = document.createDocumentFragment();
            var div = document.getElementById("toc_list");

            tree.appendChild(div);

            document.getElementById("sidebar").appendChild(tree);
        });
        
        document.getElementById("closeM1").addEventListener("click", function() {
            $("body").css("overflow", "auto");

            var tree = document.createDocumentFragment();
            var div = document.getElementById("toc_list");

            tree.appendChild(div);

            document.getElementById("sidebar").appendChild(tree);
        });
    </script>
</body>
</html>
"""
    fhtml.write(htmlend)
    fhtml.close()
#printfoot

def printlistofcontenthead():
    contenhead = """    <button id="btnF" type="button" class="btn btn-info" data-toggle="modal" data-target="#MobileSearch">
        <img class="icon-filter" alt="filter" src="icons/search.svg">
    </button>
    <div class="container" id="sidebar">
        <div id="toc_list">
            <div class="form-wrapper">
                <form autocomplete="off">
                    <div class="form-group">
                        <label class="form-label" for="first">{}</label>
                        <input id="first" class="form-input" type="text" onkeyup="$d_Find('toc_list',this.value,'a')" />
                        <img id="searchclear" class="icon-times" src="icons/cross.svg">
                        <img class="icon-search" alt="minus" src="icons/search.svg" id="searcher">
                    </div>
                </form>
            </div>
            <p6>{}:</p6>
                <output id="count"></output>
                <div class="contentView">
""".format(transl("Suchbegriff"),transl("Treffer"))
    fhtml.write(contenhead)
#printlistofcontenthead

def printlistofcontentfoot():
    contentfoot = """
            </div>
        </div>
    </div>
"""
    fhtml.write(contentfoot)
#printlistofcontentfoot


def printlistofcontentelement(p_name, p_list):
    lbc = str(newbarcounter())
    contentelementhead= """
                <div class="panel-body" id="{}L">
                    <div class="panel">
                        <div class="panel-heading collapsed" data-toggle="collapse" data-target="#bar{}">
                            <label class="label0">{}</label>
                            <img class="icon-minus" alt="minus" src="icons/minus.svg">
                            <img class="icon-plus" alt="plus" src="icons/plus.svg">
                        </div>
                    </div>
                    <!-- The inside div eliminates the 'jumping' animation. -->
                    <div class="collapse" id="bar{}">
                        <ol class="tree" id="{}List">
    """
    contentline="""
                <li class="obj"><a href="#{}" target="details">{}</a></li>"""
    contentelementfoot="""
                    </ol>
            </div>
        </div>
""";
    fhtml.write(contentelementhead.format(p_name,lbc,transl(p_name),lbc,p_name))
    for l in p_list:
        fhtml.write(contentline.format(l[1],l[0]))
    fhtml.write(contentelementfoot)
#printlistofcontentelement

def printcontenthead():
    contenthead = """    <div class="wrapper">
        <div class="top-container">
            <p3 {} 
            </p3>
        </div>
""".format("""class="descr">Diese Webseite enthält den ganzen Inhalt 
            des <p2 class="IM">Informationsmodells</p2>. 
            Diese Seite wurde von Software von <p2 class="fyayc">foryouandyourcustomers</p2> 
            erstellt.""")
    fhtml.write(contenthead)
#printcontenthead

def printcontentfoot():
    contentfoot= """      </div>
"""
    fhtml.write(contentfoot)
# printcontentfoot


def printattrlist(p_entiid):
    attrhead = """             <h2>{}</h2>
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
    attrfoot = """              
                                </tbody>
                            </table>
                            </div>
                                </div>
    """

    attrline = """                                    <tr>
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
    alist = web_sql.attrlist( p_lang=reportLang(), p_entiid=p_entiid)
    if (len(alist)==0):
        return
    fhtml.write(attrhead.format(transl('Attribute'), transl('Name'), transl('Domäne'), transl('Typ')
                            , transl('Pflichtattribut'),transl('Schlüssel'), transl('Deskriptor'), transl('übersetzt')
                            , transl('historisiert'), transl('wiederholt'), transl('verschlüsselt')))
    for a in alist:
        fhtml.write(attrline.format(web_sql.attrAnker(a[0]), a[1], web_sql.wrtbAnker(a[3]), a[2], anzDatentyp(a[4])
                                    , bool2icon(a[5]), bool2icon(a[11]), bool2icon(a[6]), bool2icon(a[7])
                                    , bool2icon(a[8]), bool2icon(a[9]), bool2icon(a[10])))
    #for
    fhtml.write(attrfoot)
#printattrlist

def startabschnitt(p_titel):
    start = """        <h2>{}</h2>
                            <div id="container0">
    """
    return start.format(p_titel)
#startabschnitt
def endabschnitt():
    end = """        </div>
    """
    return end
#startabschnitt
def starttable(ptitel, pueberschriften, plevel=2):
    tabhead= """        <h{}>{}</h{}>
                        <div id="container1">
                            <div class="table-responsive">
                   <table class="table borderless">
                                            <tbody>
                                        <tr>
"""
    tabheads="""             <th>{}</th>
"""
#    tabheads="""<th class="attribute">{}</th>"""
    retval = []
    retval.append(tabhead.format(plevel, ptitel, plevel))
    for u in pueberschriften:
        retval.append(tabheads.format(u))
    return ''.join(retval)
#starttable

def writetableline(pwerte,pid = None):
    linestart = """            <tr>
""" if pid is None else """            <tr id = "{}">
""".format(pid)
    line = """             <td>{}</td>
"""
    iconline= """           <td {}></td>
"""
    lineend ="""               </tr>
"""
    retval = []
    retval.append(linestart)
    for w in pwerte:
        if (isiconstr(w)):
            retval.append(iconline.format(w))
        else:
            retval.append(line.format(nvl(w)))
    retval.append(lineend)
    return ''.join(retval)
#writetableline

def endtable():
    return """        
                     </tbody>
                            </table>
                            </div>
                                </div>
    """
#endtable


def printentikeys(pentiid):
    keylist = web_sql.keylist(p_entiid=pentiid, p_lang=reportLang())
    if (len(keylist) == 0):
        return
    fhtml.write(starttable(transl('Schlüssel'), (transl('Nr'), transl('Name'), transl('Attribut(e)'), transl('Beziehung(en)'))))
    for k in keylist:
        fhtml.write(writetableline(pwerte=k))
    fhtml.write(endtable())
#printentikeys

def printentirela(p_entiid):

    relalist = web_sql.relalist(p_entiid=p_entiid,p_lang=reportLang())
    if (len(relalist) == 0):
        return
    fhtml.write(starttable(transl('Beziehungen'), (transl('Name'), transl('Entität')+'-1', '',transl('Beziehung'), '',transl('Entität')+'-2'
                                                        , transl('Arc'), transl('Schlüssel'),)))
    for r in relalist:
        if (p_entiid == r[0]):
            #'Name','Entität1','','Beziehung','', 'Entität2','Arc','Schluessel'
            fhtml.write(writetableline(pwerte=(nvl(r[16]), r[1], '->', nvl(r[3], '--'), r[4]
                                                        , arrow2icon('down'), nvl(r[14]), bool2icon(r[17]))))
            fhtml.write(writetableline(pwerte=(''        , arrow2icon('up')  , r[9], nvl(r[8], '--'), '<-'
                                                        , href(ref=web_sql.entiAnker(r[5]),anz=r[6]))))
        else:
            fhtml.write(writetableline(pwerte=(nvl(r[16]), r[6], '->', nvl(r[8], '--'), r[9]
                                                            , arrow2icon('down'),'', bool2icon(r[17]))))
            fhtml.write(writetableline(pwerte=(''        , arrow2icon('up')  , r[4], nvl(r[3], '--'), '<-'
                                                            , href(ref=web_sql.entiAnker(r[0]), anz=r[1]))))
        #if
    #for
    fhtml.write(endtable())
#printentirela

def printUDP(p_meltname, p_id):
    startgeschrieben = False

    udpnamen = web_sql.udpnamen(p_meltname=p_meltname)
    for udpname in udpnamen:
        werte = web_sql.udpwerte(p_meltname=p_meltname,p_id=p_id
                         ,p_thema=udpname[0],p_gruppe=udpname[1])
        #print(udpName[0],udpName[1],lwerte)
        lw = [];
        for l in werte:
            lw.append(nvl(l[0]))
        #rof

        if (len(lw) > lw.count('')):
            if (not  startgeschrieben):
                fhtml.write(startabschnitt(p_titel=transl('Benutzerdefinerte Eigenschaften')))
                startgeschrieben = True
            #fi
            namenliste = udpname[2].split(',')
            namenliste.sort() #SQl kann keine sortierte group_concat liefern

            fhtml.write(starttable(ptitel=' {} - {} '.format(udpname[0], udpname[1])
                                   , pueberschriften=namenliste
                                   , plevel=3))
            fhtml.write(writetableline(pwerte=lw))
            fhtml.write(endtable())
        #fi
    #rof
    if (startgeschrieben):
        fhtml.write(endabschnitt())
    # fi
#printUDP

def printentiudp(p_entiid):
    printUDP(p_meltname='ENTI',p_id=p_entiid)
#printentiudp

def printattrudp(p_attrid):
    printUDP(p_meltname='ATTR',p_id=p_attrid)
#printattrudp

def printcontententi(p_list):
    contenthead="""        <!--entities-->"""

    contentelementhead = """        <div class="entity" id="{}">
            <div class="describtion">
                <p>{}</p> 
                <h1>{}</h1>
                <p1>{}</p1>
            </div>
             <div class="panel-body">
            <div class="collapse" id="bar{}">                    
        """
    detailshead = """           
                <!-- The inside div eliminates the 'jumping' animation. -->
"""
    detailsfoot = """            
                            </div>
"""
    infohead = """
                            <h2>{}</h2>
                        <div id="container2">
                        <div class="table-responsive">
                            <table class="table borderless">
                                <tbody>
"""
    infoline = """
                                    <tr>
                                        <th>{}</th>
                                        <td class="attribute">{}</td>
                                    </tr>
"""
    infofoot = """
                                </tbody>
                            </table>
                        </div>
                        </div>
"""
    fhtml.write(contenthead)
    for e in p_list:
        lbc = str(newbarcounter())
        fhtml.write(contentelementhead.format(web_sql.entiAnker(e[0]) #id
                                            ,transl('Entität')
                                            ,e[1] #name
                                            , nvl(e[2])
                                            ,lbc)) #descr

        fhtml.write(detailshead)
        """print entity Info"""
        fhtml.write(infohead.format(transl('Informationen')))
        if (e[8] is not None):
            fhtml.write(infoline.format(transl('Synonyme'),e[8]))
        if (e[6] is not None):
            fhtml.write(infoline.format(transl('Superentität'),href(ref=web_sql.entiAnker(e[6]),anz=e[5])))
        if (e[7] is not None):
            fhtml.write(infoline.format(transl('Subentitäten'),list2href(e[7])))
        fhtml.write(infoline.format(transl('geändert'),nvl(e[3]) + ', ' + nvl(e[4])))
        fhtml.write(infofoot)

        printattrlist(p_entiid=e[0])
        printentikeys(pentiid=e[0])
        printentirela(p_entiid=e[0])
        printentidiag(pentiid=e[0])
        printentiudp(p_entiid=e[0])

        fhtml.write(detailsfoot)
        fhtml.write(contentelementfoot.format(lbc,transl('Mehr')))
    #for
#printcontententi

def printcontentattr(plist):
    contenthead="""        <!--attributes-->"""

    contentelementhead = """        <div class="entity" id="{}">
            <div class="describtion">
                <p>{}</p>
                <h1>{}</h1>
                <p1>{}: {}</p1><br>
                <p1>{}</p1>
            </div>
             <div class="panel-body">
            <div class="collapse" id="bar{}">                    
        """
    detailshead = """           
                <!-- The inside div eliminates the 'jumping' animation. -->
"""
    detailsfoot = """            
                            </div>
"""
    infohead = """
                            <h2>{}</h2>
                        <div id="container2">
                        <div class="table-responsive">
                            <table class="table borderless">
                                <tbody>
"""
    flaghead = """                      <tr>
                                                <th class="thAlgn">{}</th>
                                                <th class="thAlgn">{}</th>
                                                <th class="thAlgn">{}</th>
                                                <th class="thAlgn">{}</th>
                                                <th class="thAlgn">{}</th>
                                                <th class="thAlgn">{}</th>
                                                <th class="thAlgn">{}</th>
                                            </tr>
    """
    flagline = """
                                        <tr>
                                                    <td class="symbol"><img {}></td>
                                                    <td class="symbol"><img {}></td>
                                                    <td class="symbol"><img {}></td>
                                                    <td class="symbol"><img {}></td>
                                                    <td class="symbol"><img {}></td>
                                                    <td class="symbol"><img {}></td>
                                                    <td class="symbol"><img {}></td>                                    
                                        </tr>
    """
    techhead = """                      <tr>
                                                <th>{}</th>
                                                <th>{}</th>
                                                <th>{}</th>
                                            </tr>
    """
    techline = """
                                        <tr>
                                                   <td class="attribute">{}</td>
                                                    <td class="attribute">{}</td>
                                                    <td class="attribute">{}</td>                                    
                                        </tr>
    """
    infofoot = """
                                </tbody>
                            </table>
                        </div>
                        </div>
"""
    fhtml.write(contenthead)
    for a in plist:
        lbc = str(newbarcounter())
        fhtml.write(contentelementhead.format(web_sql.attrAnker(a[0]) #id
                                            ,transl('Attribut')
                                            ,a[1] #anzname
                                            , transl('Entität')
                                            ,href(ref=web_sql.entiAnker(a[22])
                                                ,anz=web_sql.enti_name(p_lang=reportLang()
                                                                       ,p_modeid=dbLookup.modeid(p_entiid=a[22])))
                                            , nvl(a[18]) #Beschreib ung
                                            ,lbc))

        fhtml.write(detailshead)
        fhtml.write(infohead.format(transl('Informationen')))

        fhtml.write(techhead.format(transl('Tooltip'), transl('erstellt'), transl('geändert')))
        fhtml.write(techline.format(nvl(a[13],''),re.sub(r'^, $','',nvl(a[16]) + ', ' + nvl(a[17]))
                                          ,re.sub(r'^, $','',nvl(a[14]) + ', ' + nvl(a[15]))))

        fhtml.write(techhead.format(transl('Technischer Name'), transl('Wertebereich'), transl('Datentyp')))
        fhtml.write(techline.format(nvl(a[12],''),href(ref=web_sql.wrtbAnker(a[3])
                                                ,anz=a[23])
                                        ,nvl(a[4]),''))

        fhtml.write(flaghead.format(transl('Pflichtattribut'), transl('Schlüssel'), transl('Deskriptor'),
                                    transl('übersetzt')
                                    , transl('historisiert'), transl('wiederholt'), transl('verschlüsselt')))
        fhtml.write(flagline.format(bool2icon(a[5]), bool2icon(a[11]), bool2icon(a[6]), bool2icon(a[7])
                                        , bool2icon(a[8]), bool2icon(a[9]), bool2icon(a[10])))
        fhtml.write(infofoot)

        printattrudp(p_attrid=a[0])

        fhtml.write(detailsfoot)
        fhtml.write(contentelementfoot.format(lbc,transl('Mehr')))
    #for
#printcontentattr


def printwrtbattrlist(pwrtbid, wrtgruppe=False):
    alist = web_sql.namelist(ptype='ATTG' if wrtgruppe else 'ATTR'
                             , plang=reportLang(), pwrtbid=pwrtbid)
    if (len(alist)==0):
        return
    fhtml.write(starttable(ptitel=transl('Verwendet in Attributgruppen' if wrtgruppe
                                                else 'Verwendet für Attribute')
                           , pueberschriften=[transl('Attribut' if wrtgruppe
                                                else 'Attributgruppe')]))
    for a in alist:
        fhtml.write(writetableline(pwerte=[href(ref=a[1], anz=a[0])])
                    )
    #for
    fhtml.write(endtable())
#printattrlist
def printwrtbmembers(pwrtbid):
    elems = web_sql.wbgrelements(wrtbid=pwrtbid)
    if (len(elems)==0):
        return
    fhtml.write(starttable(ptitel=transl('Elemente')
                           , pueberschriften=
                                [transl('Element')
                                ,transl('Beschreibung')
                                ,transl('Wertebereich')
                                ,transl('geändert')
                                 ]))
    for e in elems:
        fhtml.write(writetableline(pwerte=[e[0], e[1]
                                            , href(ref=web_sql.wrtbAnker(e[9])
                                                    ,anz=e[2]+' ('+anzDatentyp(e[3])+')')
                                            , e[5] +' , ' + e[6]]
                                   ))#,pid=web_sql.attgAnker(e[10])))
    #for
    fhtml.write(endtable())
#printwrtbmembers

def printwertelist(p_wrtbid):

    wlist = web_sql.wrtbwerte(p_wrtbid=p_wrtbid)
    if (len(wlist)==0):
        return
    fhtml.write(starttable(ptitel=transl('Werteliste')
                           , pueberschriften=(transl('Nr'), transl('Wert'), transl('Anzeige'), transl('Beschreibung'))
                           , plevel=3))
    for w in wlist:
        fhtml.write(writetableline(pwerte=w))
    fhtml.write(endtable())

#printwertelist

def printcontentwrtb(p_list):
    contenthead="""        <!--domains-->"""

    contentelementhead = """        <div class="entity" id="{}">
            <div class="describtion">
                <p>{}</p>
                <h1>{}</h1>
                <p1>{}</p1>
            </div>
             <div class="panel-body">
            <div class="collapse" id="bar{}">                    
        """
    detailshead = """           
                <!-- The inside div eliminates the 'jumping' animation. -->
"""
    detailsfoot = """            
                            </div>
"""
    infohead = """
                            <h2>{}</h2>
                        <div id="container2">
                        <div class="table-responsive">
                            <table class="table borderless">
                                <tbody>
"""
    techhead = """                      <tr>
                                                <th>{}</th>
                                                <th>{}</th>
                                                <th>{}</th>
                                                <th>{}</th>
                                                <th>{}</th>
                                                <th>{}</th>
                                                <th>{}</th>
                                            </tr>
    """
    techline = """
                                        <tr>
                                                   <td class="attribute">{}</td>
                                                    <td class="attribute">{}</td>
                                                    <td class="attribute">{}</td>                                    
                                                    <td class="attribute">{}</td>                                    
                                                    <td class="attribute">{}</td>                                    
                                                    <td class="attribute">{}</td>                                    
                                                    <td class="attribute">{}</td>                                    
                                        </tr>
    """
    infofoot = """
                                </tbody>
                            </table>
                        </div>
                        </div>
"""
    fhtml.write(contenthead)
    for w in p_list:
        lbc = str(newbarcounter())
        fhtml.write(contentelementhead.format(web_sql.wrtbAnker(w[0]) #id
                                            ,transl('Wertebereich')
                                            ,w[1] #anzname
                                            , nvl(w[4]) #Beschreibung
                                            ,lbc))

        fhtml.write(detailshead)
        fhtml.write(infohead.format(transl('Informationen')))

        if (w[5] == 'TEXT'):
            fhtml.write(techhead.format(transl('Datentyp'),transl('Max. Länge'),transl('Syntaxregel'),'','','',''))
            fhtml.write(techline.format(nvl(anzDatentyp(w[5])),nvl(w[9]),nvl(w[10]),'','','',''))
        elif (w[5] == 'BIN'):
            fhtml.write(techhead.format(transl('Datentyp'), transl('Inhaltstyp'), transl('Format'),'','','',''))
            fhtml.write(techline.format(nvl(anzDatentyp(w[5])), nvl(w[17]),anzinhalttyp(nvl(w[18]),'','','','')))
        elif (w[5] == 'GRP'):
            fhtml.write(techhead.format(transl('Datentyp'),transl(''), transl(''),'','','',''))
            fhtml.write(techline.format(nvl(anzDatentyp(w[5])),nvl(w[9]),nvl(w[10]),'','','',''))
        elif (w[5] == 'NUM'):
            fhtml.write(techhead.format(transl('Datentyp'),transl('Vorkommast.'), transl('Nachkommast.')
                                                            ,transl('Rundungseinh.')
                                        ,transl('Einheit'),transl('Min. Wert'),transl('Max. Wwert')))
            fhtml.write(techline.format(nvl(anzDatentyp(w[5])),nvl(w[13]),nvl(w[14]),nvl(w[15]),nvl(w[16]),nvl(w[12]),nvl(w[11])))
        elif (w[5] == 'ZPKT'):
            fhtml.write(techhead.format(transl('Datentyp'),transl('Min. Wert'), transl('Max. Wert'),transl('Granularität'),'','',''))
            fhtml.write(techline.format(nvl(anzDatentyp(w[5])),nvl(w[6]),nvl(w[7]),anzgranul(nvl(w[8])),'','',''))
        #fi

        fhtml.write(techhead.format(transl('erstellt'), transl('geändert'),'','','','',''))

        fhtml.write(infofoot)
        if (w[5] == 'LOV'):
            printwertelist(p_wrtbid=w[0])

        if (w[5] == 'GRP'):
            printwrtbmembers(pwrtbid=w[0])
        printwrtbattrlist(pwrtbid=w[0])
        printwrtbattrlist(pwrtbid=w[0],wrtgruppe=True)
        fhtml.write(detailsfoot)
        fhtml.write(contentelementfoot.format(lbc,transl('Mehr')))
    #for
#printcontentwrtb


def searchlogo(p_imagedirec):
    retval=''
    for ext in ('png','jpg','svg'):
        if os.path.isfile(p_imagedirec+'logo.'+ext): retval = 'logo.'+ ext
    return retval
#searchlogo

def setWebDirec(p_webdirec):
    global webDirectory ,webFileName,webFileNamePath
    global libSourceDirec,imagedirec,cssdirec,icondirec

    webDirectory =  p_webdirec if (p_webdirec is not None)  else parameters.webDirec();
    webFileName = parameters.odmModelName();
    imagedirec = webDirectory + 'image/';
    cssdirec = webDirectory + "css/";
    icondirec = webDirectory + "icons/";
    webFileNamePath = webDirectory + webFileName + '.html';
    libSourceDirec = os.path.dirname(os.path.abspath(__file__))
    libSourceDirec +='/../html-lib/';
    if (parameters.logoFileName() is None) :parameters.logoFileName(searchlogo(imagedirec));

# setWebDirec


def createFile():
    global fhtml

    if os.path.exists(webFileNamePath):
        os.remove(webFileNamePath)
    if os.path.exists(cssdirec):
        shutil.rmtree(cssdirec)
    if os.path.exists(icondirec):
        shutil.rmtree(icondirec)
    if os.path.exists(imagedirec):
        shutil.rmtree(imagedirec)

    shutil.copytree(libSourceDirec+'icons',icondirec)
    shutil.copytree(libSourceDirec+'css',cssdirec)
    shutil.copytree(libSourceDirec+'image',imagedirec)

    fhtml = open(webFileNamePath,'w')

#createFile


def printentidiag(pentiid):
    diaglist  = web_sql.diaglist(pentiid=pentiid)
    if (len(diaglist) == 0):
        return
    fhtml.write(starttable(ptitel=transl('auf Diagramm(en)')
                           ,pueberschriften=[transl('Diagramm')]
                           ,plevel = 3))
    for d in diaglist:
        fhtml.write(writetableline(pwerte=[href(ref=web_sql.diagAnker(d[1])
                                                ,anz=d[0])]))
    fhtml.write(endtable())
#printentidiag
