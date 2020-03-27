from IM_DB import parameters,dbLookup
import os,shutil,re
from IM_HTML import web_sql
from  IM_OBJECTS import *

outputDirectory:str = None
webDirectory:str = "";
webFileName:str = "";
webFileNamePath:str = "";
libSourceDirec:str = "";
imagedirec:str = "";
cssdirec:str = "";
icondirec:str = "";
htmlfilelist = {}

"""zum Zählen der lokalen Ziele für collapse"""
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


def lf2htmlbr (pstr):
    try:
        return re.sub(r"\n","<br>\n",pstr)
    except:
        return pstr
#lf2htmlbr

def nvl(x,default=''):
    return x if (x is not None) else default
#nvl

def filehref(ref,anz,plang,pimg=None):
    img = '' if pimg is None else '<img class="icon-check" src="icons/{}">'.format(pimg)
    return """<a href="{}{}" target="_blank" >{}{}</a>"""\
        .format(webFileName + '_' + plang.lower() + '.html',"#"+ref if ref is not None else "",anz,img)
#filehref
def href(ref,anz,htmlfile=''):
    if anz is None: return None
    return """<a href="{}{}" target="{}">{}</a>""".format(htmlfile,'{}{}'.format('' if ref == '' else '#', ref)
                                                ,'_self' if htmlfile == '' else '_blank', anz)
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
                ,'Attributgruppe': 'Attribut group'
                ,'auf Diagramm(en)': 'on diagram(s)'
                ,'Author': 'Author'
                ,'Beschreibung': 'Description'
                ,'Beziehung': 'Relationship'
                ,'Beziehung(en)': 'relationship(s)'
                ,'Beziehungen': 'Relationships'
                ,'Benutzerdefinerte Eigenschaften': 'User defined properties'
                ,'Bild': 'Picture'
                ,'Binär': 'Binary'
                ,'Datentyp': 'Datatype'
                ,'Deskriptor': 'descriptor'
                ,'Domänen': 'Domains'
                ,'Diagramm': 'Diagram'
                ,'Diagramme': 'Diagrams'
                ,'Dokument': 'Document'
                ,'Domäne': 'Domain'
                ,'Einheit': 'Unit'
                ,'Element': 'Element'
                ,'Elemente': 'Elements'
                ,'Entität': 'Entity'
                ,'Entität/Tabelle': 'Entity/Table'
                ,'Entitäten': 'Entities'
                ,'erstellt': 'created'
                ,'Film': 'Video'
                ,'geändert': 'updated'
                ,'Gruppenattribut': 'Groupattribute'
                ,'Grafik': 'Graphic'
                ,'Granularität': 'Granularity'
                ,'historisiert': 'historicized'
                ,'in Schlüssel': 'within key'
                ,'Informationsmodell {} (Stand: {})': 'Informationmodel {} (Status: {})'
                ,'Informationen': 'Informations'
                ,'Inhaltstyp': 'Content type'
                ,'Ja': 'Yes'
                ,'Jahr': 'year'
                ,'Max. Länge': 'Max. length'
                ,'Max. Wert': 'Max. value'
                ,'Mehr': 'more'
                ,'Millisekunde': 'millisecond'
                ,'Minute': 'minute'
                ,'Min. Wert': 'Min. value'
                ,'Monat': 'month'
                ,'Nachkommast.': 'digits after period'
                ,'Name': 'Name'
                ,'Nein': 'No'
                ,'Nr': 'Nr'
                ,'Numerisch': 'Numerical'
                ,'Pflichtattribut': 'Attribute of duty'
                ,'Quartal': 'quarter'
                ,'Relational Mapping (Tabellen)':'Relational Mapping (tables)'
                ,'Rundungseinh.': 'rounding unit'
                ,'Schlüssel': 'Key'
                ,'Sekunde': 'second'
                ,'Semester': 'half-year'
                ,'Sort': 'Sort'
                ,'Stunde': 'hour'
                ,'Subentität': 'Subentity'
                ,'Subentitäten': 'Subentities'
                ,'Suchbegriff': 'search key'
                ,'Superentität': 'Superentity'
                ,'Synonyme': 'Synonyms'
                ,'Syntaxregel': 'Syntax rule'
                ,'Systeme': 'Systems'
                ,'Tag': 'day'
                ,'Tabellen': 'Tables'
                ,'Technischer Name': 'Technical Name'
                ,'Text': 'Text'
                ,'Ton': 'Sound'
                ,'Tooltip': 'Tooltip'
                ,'Treffer': 'Hits'
                ,'Typ': 'Type'
                ,'UDP-Matrix': 'UDP-Matrix'
                ,'übersetzt': 'translated'
                ,'Übersetzungen': 'Translations'
                ,'Unterdokumente': 'Children'
                , "Vaterdokument": "Parent"
                ,'verschlüsselt': 'encrypted'
                ,'Verwendet für Attribute': 'Used for attributes'
                ,'Verwendet in Attributgruppen': 'Used in attribute groups'
                ,'Verwendet von': 'used by'
                ,'Vorkommast.': 'digits before period'
                ,'Wert': 'Value'
                ,'Wertebereich': 'Domain'
                ,'Werteliste': 'List of values'
                ,'wiederholt': 'repeated'
                ,'Woche': 'week'
                ,'Zeitpunkt': 'Point in Time'
                }
translNameFR = {"Anzeige":"Affichage"
,"Arc":"Arc"
,"Attribut":"Attribut"
,"Attribut(e)":"Attribut(s)"
,"Attribute":"Attributs"
,"Attributgruppe":"Groupe d'attributs"
,"auf Diagramm(en)":"sur ce diagramme(s)"
,"Autor":"Auteur"
,"Beschreibung":"Déscription"
,"Beziehung":"Relation"
,"Beziehung(en)":"Relation(s)"
,"Beziehungen":"Relations"
,"Benutzerdefinerte Eigenschaften":"Propriétés définies par l'utilisateur"
,"Bild":"Image"
,"Binär":"Binaire"
,"Datentyp":"Type de données"
,"Deskriptor":"Descripteur"
,"Domänen":"Domaines"
,"Diagramm":"Diagramme"
,"Diagramme":"Diagrammes"
,"Domäne":"Domaine"
,"Dokument":"Document"
,"Einheit":"Unité"
,"Element":"Élément"
,"Elemente":"Éléments"
,"Entität":"Entité"
,"Entität/Tabelle":"Entité/Tableau"
,"Entitäten":"Entités"
,"erstellt":"Élaboré"
,"Film":"Film"
,"geändert":"changé"
,"Gruppenattribut":"Attribut de groupe"
,"Grafik":"Graphique"
,"Granularität":"Granularité"
,"historisiert":"historisé"
,"in Schlüssel":"dans une clef"
,"Informationsmodell {} (Stand {})":"Modèle d'informations {} (État {})"
,"Informationen":"Informations"
,"Inhaltstyp":"Type de contenu"
,"Ja":"Oui"
,"Jahr":"Année"
,"Max. Länge":"Longueur max."
,"Max. Wert":"Valeur max."
,"Mehr":"Plus"
,"Millisekunde":"Milliseconde"
,"Minute":"Minute"
,"Min. Wert":"Valeur min."
,"Monat":"Mois"
,"Nachkommastellen":"Décimales"
,"Name":"Nom"
,"Nein":"Non"
,"Nr":"N°"
,"Numerisch":"Numérique"
,"Pflichtattribut":"Attribut obligatoire"
,"Quartal":"Trimestre"
,"Relational Mapping (Tabellen)":"Relational Mapping (tables)"
,"Rundungseinheit":"Unité de l'arrondi"
,"Schlüssel":"Clef"
,"Sekunde":"Seconde"
,"Semester":"Semestre"
,"Sort":"Sorte"
,"Stunde":"Heure"
,"Subentität":"Sous-entité"
,"Subentitäten":"Sous-entités"
,"Suchbegriff":"Clef de reherche"
,"Superentität":"Superentité"
,"Synonyme":"Synonyme"
,"Syntaxregel":"Règle syntaxique"
,"Systeme": "Systèmes"
,'Tabellen': 'Tables'
,"Tag":"Jour"
,"Technischer Name":"Terme technique"
,"Text":"Texte"
,"Ton":"Ton"
,"Tooltip":"Info-bulle"
,"Treffer":"Occurrence"
,"Typ":"Type"
,"UDP-Matrix":"Matrice UDP"
,"übersetzt":"traduit"
,"Übersetzungen":"Traductions"
, 'Unterdokumente': 'Enfants'
,"Vaterdokument":"Document père"
,"verschlüsselt":"Chiffré"
,"Verwendet für Attribute":"Utilisé par les attributs"
,"Verwendet in Attributgruppen":"Utilisé dans les groupes d'attributs"
,"Verwendet von":"Utilisé pour"
,"Vorkommastellen":"Position avant la décimale"
,"Wert":"Valeur"
,"Wertebereich":"Domaine de valeurs"
,"Werteliste":"Liste des Valeur"
,"wiederholt":"répété"
,"Woche":"Semaine"
,"Zeitpunkt":"Instant"
}
def transl(pname):
    if (greportLang == 'de'):
       return pname
    elif (greportLang == 'en'):
        try:
            return translNameEN[pname]
        except:
            return pname
    elif (greportLang == 'fr'):
        try:
           return translNameFR[pname]
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


def list2href(p_list, ptype):
    """Verandelt eine kommagetrennte Liste von nnn:xxxx in einen String von kommagetrennten  HREF-Webeinträgen"""
    if p_list is None: return None
    list = p_list.split(",")
    elem = []
    for el in list:
        el1  = el.split(':')
        elem.append(href(ref=
            web_sql.entiAnker(el1[0]) if ptype == 'ENTI' else
            web_sql.dokuAnker(el1[0]) if ptype == 'DOKU' else
            el1[0]
        , anz=el1[1]))
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
		// Quick and simple export target #table_id into a csv
		function download_table_as_csv(table_id) {
		    // Select rows from table_id
		    var rows = document.querySelectorAll('table#' + table_id + ' tr');
		    // Construct csv
		    var csv = [];
		    for (var i = 0; i < rows.length; i++) {
		        var row = [], cols = rows[i].querySelectorAll('td, th');
		        for (var j = 0; j < cols.length; j++) {
		            // Clean innertext to remove multiple spaces and jumpline (break csv)
		            var data = cols[j].innerText.replace(/(\\r\\n|\\n|\\r)/gm, '').replace(/(\\s\\s)/gm, ' ')
		            // Escape double-quote with double-double-quote (see https://stackoverflow.com/questions/17808511/properly-escape-a-double-quote-in-csv)
		            data = data.replace(/"/g, '""');
		            // Push escaped string
		            row.push('"' + data + '"');
		        }
		        csv.push(row.join(';'));
		    }
		    var csv_string = csv.join('\\n');
		    // Download it
		    var filename = 'export_' + table_id + '_' + new Date().toLocaleDateString() + '.csv';
		    var link = document.createElement('a');
		    link.style.display = 'none';
		    link.setAttribute('target', '_blank');
		    link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv_string));
		    link.setAttribute('download', filename);
		    document.body.appendChild(link);
		    link.click();
		    document.body.removeChild(link);
		}
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
                var c = 0; // Counter for results
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

            // Code for automatic expanding after results < 30 
            if (c <= 30) {
                $('#bar1').collapse('show');
                $('#bar2').collapse('show');
                $('#bar3').collapse('show');
            } else {
                $('#bar1').collapse('hide');
                $('#bar2').collapse('hide');
                $('#bar3').collapse('hide');
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

        //serchclearer (clears input in searchbar)
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


        $('a[href^="#"]').on('click', function(e) {

            window.location.hash = "-------";

            e.preventDefault();
            var target = $(this).attr('href');
            var $target = $(target);
            $('html, body').stop().animate({
                'scrollTop': $target.offset().top
            }, 900, 'swing', function() {
                $tblshow();
                window.location.hash = target;
            });
        });

        function $tblshow() {

            //locating the clicked table
            var url = window.location.href;
            var sID = url.substring(url.indexOf('#') + 1);

            //collapsing table
            temp = (sID + ' > div > .collapse');
            $('#' + temp).collapse('show');


            //checking if its using the right data
            console.log("URL: " + url + " \\n ");
            console.log("ID der Tabelle: " + sID + " \\n ");
            console.log("Suchid: " + temp);

        }

        $(document).ready(function() {
            $(window).scroll(function() {
                if ($(this).scrollTop() > 700) {
                    $('#btnTop').fadeIn();
                } else {
                    $('#btnTop').fadeOut();
                }
            });
            // scroll content to top by clicking on button
            $('#btnTop').click(function() {
                $('body,html').animate({
                    scrollTop: 0
                }, 400);
                return false;
            });
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


def printlistofcontentelement(pname, plist,pfileonly = False):
    if len(plist) == 0: return
    lbc = str(newbarcounter())
    listcontentelementhead= """
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
    listcontentline="""
                <li class="obj"><a href="{}" target="{}">{}</a></li>"""

    listcontentelementfoot="""
                    </ol>
            </div>
        </div>
"""
    fhtml.write(listcontentelementhead.format(pname, lbc, transl(pname), lbc, pname))
    for l in plist:
        inanker = l[1]
        local = False
        if type(inanker) == Webanker:
            local = re.match(r'/(.+/)*{}'.format(htmlfilelist[inanker.modelid()])
                             ,fhtml.name)
            anker = '' if (local) else htmlfilelist[inanker.modelid()]
            if not pfileonly:
                anker += '#' + inanker.anker()
        else:
            anker = '#' + l[1]
        anzeige = l[0]
        fhtml.write(listcontentline.format(anker,'_self' if local else '_blank',anzeige))
    fhtml.write(listcontentelementfoot)
#printlistofcontentelement

def lang2img(plang):
    if plang in ('de','fr'):
        return plang+".png"
    elif plang == 'en':
        return "gb.png"
    else:
        return None
#lang2img
def printcontenthead(pfirma,ptitel):
    contenthead = """    <div class="wrapper">
        <div class="top-container">
            <p3 {} 
            </p3>
        <div>
            {}
        </div>          
        </div>
"""
    if reportLang()== 'de' :
        f = """class="descr">Diese Webseite enthält den ganzen Inhalt 
            des <p2 class="IM">Informationsmodells {}</p2> von {}. 
            Diese Seite wurde von Software von <p2 class="fyayc">foryouandyourcustomers</p2> 
            erstellt.""".format(ptitel,pfirma)
    else:
        f = """class="descr">This website contains the complete content 
            of the <p2 class="IM">Information model {}</p2> from {}. 
            This page was created with software from <p2 class="fyayc">foryouandyourcustomers</p2>."""\
            .format(ptitel,pfirma)
    #fi
    langs = projekt.projektlangs().split(',')
    try:
        langs.remove(reportLang().lower())
    except:
        pass
    str = ''
    for l in langs:
        str += filehref(ref=None,anz=l+'   ',plang=l,pimg=lang2img(l.lower()))
    fhtml.write(contenthead.format(f,str))
#printcontenthead

def printcontentfoot():
    contentfoot= """      </div>
"""
    fhtml.write(contentfoot)
# printcontentfoot

def printcontentstart(pname):
    fhtml.write("        <!--{}-->".format(pname))
#printcontentsstart
def printcontentend(plbc):
    fhtml.write("""            
                            </div>""")
    fhtml.write(contentelementfoot.format(plbc, transl('Mehr')))
#printcontentend

def printcontent (ptype,pname,panker,plbc,pdescr="",pmaster=""):
    contentelementhead = """        <div class="entity" id="{}">
            <div class="describtion">
                <p>{}</p>
                <h1>{}</h1>
                {}
                {}
            </div>
             <div class="panel-body">
            <div class="collapse" id="bar{}">                    
"""

    lbc = str(newbarcounter())
    fhtml.write(contentelementhead.format(panker, ptype, pname
                                          , pmaster
                                          , "" if (pdescr == "") else  "<p1>{}</p1>".format(pdescr)
                                          , plbc))

#printcontent

def printflagline(pheaders,pvalues):
    infohead = """
      <!-- The inside div eliminates the 'jumping' animation. -->
                        <div id="containerflag">
                        <div class="table-responsive">
                            <table class="table borderless">
                                <tbody>"""
    trstart = """
                <tr>"""
    trend = """
                  </tr>"""
    flaghead = """
                <th class="thAlgn">{}</th>"""
    flagline = """
                    <td class="symbol"><img {}></td>"""
    infofoot = """
                </tbody>
                </table>
            </div>
        </div>"""

    fhtml.write(infohead)
    fhtml.write(trstart)
    for h in pheaders:
        fhtml.write(flaghead.format(h))
    fhtml.write(trstart)
    for v in pvalues:
        fhtml.write(flagline.format(v))
    fhtml.write(trend)
    fhtml.write(infofoot)
#printcontentinfo


def printcontentinfo(pheaders,pvalues):
    infohead = """
          <!-- The inside div eliminates the 'jumping' animation. -->
                            <h2>{}</h2>
                            <div id="container2">
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
    fhtml.write(infohead.format(transl('Informationen')))
    fhtml.write(trstart)
    for h in pheaders:
        fhtml.write(techheadline.format(h))
    fhtml.write(trstart)
    for v in pvalues:
        fhtml.write(techlineline.format(v))
    fhtml.write(trend)
    fhtml.write(infofoot)
#printcontentinfo


def printattrlist(pentiid):
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
    alist = web_sql.attrlist(p_lang=reportLang(), p_entiid=pentiid)
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
def starttable(ptitel, pueberschriften, pheadlevel=2, ptabid=None, pselfanker=None):
    tabhead= """        <h{}>{}</h{}>{}
                        <div id="container1">
                            <div class="table-responsive">
                   <table class="table borderless" {}>
                                            <tbody>
                                        <tr>
"""
    tabheads="""             <th>{}</th>
"""
#    tabheads="""<th class="attribute">{}</th>"""
    retval = []
    retval.append(tabhead.format(pheadlevel, ptitel, pheadlevel
                                 ,'' if ptabid is None
                                    else  '<a href="#{}" onclick="download_table_as_csv(\'{}\');">download as CSV</a>'.format(pselfanker,ptabid)
                                 ,'' if ptabid is None
                                    else 'id="{}"'.format(ptabid)))
    for u in pueberschriften:
        retval.append(tabheads.format(u))
    return ''.join(retval)
#starttable

def writetableline(pwerte, plineid = None):
    linestart = """            <tr>
    """ if plineid is None else """            <tr id = "{}">
    """.format(plineid)
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
            retval.append(iconline.format(lf2htmlbr(nvl(w))))
        else:
            retval.append(line.format(nvl(lf2htmlbr(nvl(w)))))
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

def tablehtml(ptitel, pueberschriften, pwerteliste, plineid= None,pheadlevel=2, ptabid=None, pselfanker=None):
    retval = starttable(ptitel=ptitel,pueberschriften=pueberschriften,pheadlevel=pheadlevel,ptabid=ptabid,pselfanker=pselfanker)
    for lw in pwerteliste:
        retval += writetableline(pwerte=lw,plineid=plineid)
    retval += endtable()
    return retval
#tablehtml

def printentikeys(pentiid):
    keylist = web_sql.keylist(p_entiid=pentiid, p_lang=reportLang())
    if (len(keylist) == 0):
        return
    fhtml.write(tablehtml(ptitel=transl('Schlüssel')
                           , pueberschriften=(transl('Nr'), transl('Name'), transl('Attribut(e)'), transl('Beziehung(en)'))
                          ,pwerteliste=keylist
                          )
                )
#printentikeys

def printmapping(pentiid):
    tl = tablentimap.tablelist(pentiid=pentiid)
    if (tl is None or len(tl) == 0):
        return
    fhtml.write(tablehtml(ptitel=transl('Relational Mapping (Tabellen)')
                           , pueberschriften=(transl('Relational Model'), transl('Tabellen'))
                          ,pheadlevel=2
                          ,pwerteliste=tl
                          )
                )
#printmapping

def printentirela(pentiid):

    relalist = web_sql.relalist(p_entiid=pentiid, p_lang=reportLang())
    if (len(relalist) == 0):
        return
    fhtml.write(starttable(ptitel=transl('Beziehungen')
                        ,pueberschriften= (transl('Name'), transl('Entität')+'-1', '',transl('Beziehung'), '',transl('Entität')+'-2'
                                                        , transl('Arc'), transl('Schlüssel'),)))
    for r in relalist:
        if (pentiid == r[0]):
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

def printcontentmapping(plist):
    if len(plist)==0: return
    contenthead = """        <!--mapping-->"""

    contentelementhead = """        <div class="entity" id="{}">
                <div class="describtion">
                    <p>{}</p>
                    <h1>{}</h1>
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

    fhtml.write(contenthead)
    for m in plist:
        lthema=m[2]
        lgruppe=m[0]
        lanker=m[1]
        namenliste = [transl('Attribut')]
        udpnamen = web_sql.udpnamen(pmeltname='ATTR',pthema=lthema,pgruppe=lgruppe)
        #print ('udpnamen=',udpnamen,m[2],m[0])
        if len(udpnamen) == 0: continue
        udpnamen = udpnamen[0][2].split(',')
        udpnamen.sort()  # SQl kann keine sortierte group_concat liefern

        #print ('udpnamen=',udpnamen)
        namenliste.extend(udpnamen)

        al = web_sql.udpattrlist(pthema=lthema,pgruppe=lgruppe,plang=reportLang())
        werte = []
        for a in al:
            zeile = [href(ref=a[1],anz=a[0])]
            udpwerte = web_sql.udpwerte(pmeltname='ATTR',pthema=lthema,pgruppe=lgruppe,pid = a[2])
            if udpwerte is None: continue
            zeile.extend(w[0] for w in udpwerte)
            werte.append(zeile)

        lbc = str(newbarcounter())
        fhtml.write(contentelementhead.format(lanker
                                              , transl('Attribute - Mapping')
                                              , lgruppe  # anzname
                                              , lbc))
        fhtml.write(detailshead)


        fhtml.write(starttable(ptitel='Mapping'
                               , pueberschriften=namenliste
                               , pheadlevel=3
                               , ptabid='TAB-{}'.format(lgruppe if lgruppe != '*' else 'ALL')
                               , pselfanker=lanker))
        for w in werte: fhtml.write(writetableline(pwerte=w))
        fhtml.write(endtable())

        fhtml.write(detailsfoot)
        fhtml.write(contentelementfoot.format(lbc, transl('Mehr')))
    # for
#printcontentmapping

def printUDP(p_meltname, p_id):
    startgeschrieben = False

    udpnamen = web_sql.udpnamen(pmeltname=p_meltname)
    for udpname in udpnamen:
        if udpname[0] == parameters.odmUDPTranslFileName():
            continue
        werte = web_sql.udpwerte(pmeltname=p_meltname, pthema=udpname[0], pgruppe=udpname[1], pid=p_id)
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

            fhtml.write(tablehtml(ptitel=href(ref=web_sql.udpAnker('{}-{}'.format(udpname[0],udpname[1]))
                                               ,anz=' {} - {} '.format(udpname[0], udpname[1]))
                                   , pueberschriften=namenliste
                                   , pheadlevel=3
                                  ,pwerteliste=lw)
                                )
#            fhtml.write(starttable(ptitel=href(ref=web_sql.udpAnker('{}-{}'.format(udpname[0],udpname[1]))
#                                               ,anz=' {} - {} '.format(udpname[0], udpname[1]))
#                                   , pueberschriften=namenliste
#                                   , pheadlevel=3))
#            fhtml.write(writetableline(pwerte=lw))
#            fhtml.write(endtable())
        #fi
    #rof
    if (startgeschrieben):
        fhtml.write(endabschnitt())
    # fi
#printUDP

def printentiudp(pentiid):
    printUDP(p_meltname='ENTI', p_id=pentiid)
#printentiudp

def printattrudp(pattrid):
    printUDP(p_meltname='ATTR', p_id=pattrid)
#printattrudp

def entidiag(pentiid):
    doppelanker="{}-{}"
    diaglist  = web_sql.diaglist(pentiid=pentiid)
    if (len(diaglist) == 0):
        return
    diagdict = {dl[0] : dl[1] for dl in diaglist}
    diagstring = ', '.join(href(ref=doppelanker.format(web_sql.diagAnker(id)
                                    ,web_sql.entiAnker(pentiid))
                                ,anz=str(name)) for name, id in diagdict.items())
    #print (diagstring)
    return diagstring
#entidiag

def printcontententi(plist):
    printcontentstart ('entities')
    infoheaders = (transl('Synonyme'), transl('Superentität'), transl('Subentitäten'),transl('auf Diagramm(en)')
                   ,transl('geändert'))
    for e in plist:
        enti_id = e[0]
        enti_name = e[1]
        enti_descr = e[2]
        lbc = str(newbarcounter())
        printcontent(ptype=transl('Entität')
                    ,panker=web_sql.entiAnker(enti_id) #id
                    ,pname=enti_name
                    ,pdescr=lf2htmlbr(nvl(enti_descr))
                    ,plbc=lbc)

        """print entity Info"""
        infovalues = (nvl(e[8]), nvl(href(ref=web_sql.entiAnker(e[6]),anz=e[5])), nvl(list2href(p_list=e[7],ptype='ENTI'))
                      ,entidiag(pentiid=enti_id),nvl(e[3]) + ', ' + nvl(e[4]))
        printcontentinfo(pheaders=infoheaders,pvalues=infovalues)

        printattrlist(pentiid=enti_id)
        printentikeys(pentiid=enti_id)
        printentirela(pentiid=enti_id)
        printreflist(pelemid=enti_id,pelemtype='ENTI')
        printtransl(pentiid=enti_id)
        printentiudp(pentiid=enti_id)
        printmapping(pentiid=enti_id)

        printcontentend(lbc)
    #for
#printcontententi

def printcontentattr(plist):
    printcontentstart ('attributes')
    infoheaders = (transl('Technischer Name'), transl('Wertebereich'), transl('Datentyp'), transl('Tooltip')
                   , transl('geändert'))
    flagheaders = (transl('Pflichtattribut'), transl('Schlüssel'), transl('Deskriptor'),
                   transl('übersetzt')
                   , transl('historisiert'), transl('wiederholt'), transl('verschlüsselt'))

    for a in plist:
        attr_id = a[0]
        attr_anzname = a[1]
        attr_descr = a[18]
        enti_id = a[22]
        lbc = str(newbarcounter())
        printcontent(ptype=transl('Attribut')
                    ,panker=web_sql.attrAnker(attr_id) #id
                    ,pname=attr_anzname
                    ,pmaster= "<p1>{}: {}</p1><br>".format(transl('Entität')
                                    ,href(ref=web_sql.entiAnker(enti_id)
                                        ,anz=web_sql.enti_name(p_lang=reportLang()
                                                    ,p_modeid=dbLookup.modeid(p_entiid=enti_id))))
                    ,pdescr=lf2htmlbr(nvl(attr_descr))
                    ,plbc=lbc)

        infovalues = (nvl(a[12],''),href(ref=web_sql.wrtbAnker(a[3]),anz=a[23]), anzDatentyp(a[4])
                            ,nvl(a[13],''),re.sub(r'^, $','',nvl(a[14]) + ', ' + nvl(a[15])))
        printcontentinfo(pheaders=infoheaders,pvalues=infovalues)

        flagvalues = (bool2icon(a[5]), bool2icon(a[11]), bool2icon(a[6]), bool2icon(a[7])
                    , bool2icon(a[8]), bool2icon(a[9]), bool2icon(a[10]))
        printflagline(pheaders=flagheaders,pvalues=flagvalues)

        printreflist(pelemid=attr_id,pelemtype='ATTR')
        printtransl(pattrid=attr_id)
        printattrudp(pattrid=attr_id)
        printcontentend(lbc)
    #for
#printcontentattr



def printreflist(pelemid,pelemtype):
    if (pelemtype == 'DOKU'):
        refentries = web_sql.dokureflist(pid=pelemid, plang=reportLang())
    else:
        refentries = web_sql.refdokulist(pid=pelemid, pelemtype=pelemtype)
    #fi
    if (refentries is None or len(refentries)==0): return

    fhtml.write(starttable(ptitel=transl('Referenziert von' )
                           , pueberschriften=[transl('Typ'),transl('Elemente')]))

    curtype = '' #Annahme: Dokumentenliste ist sortiert nach typ und Name
    kinder = ''
    for refentry in refentries:
        htmlname = ''
        if (pelemtype in ('DOKU','ENTI','ATTR','WRTB')):
            if (refentry.elemtype == 'TABL'):
                #Tabellen sind in schn-file
                tabl = Tabelle().getbyid(refentry.elemid)
                htmlname = htmlfilelist[tabl.tabl_schn_id]
            elif (refentry.elemtype == 'SCHN'):
                htmlname = htmlfilelist[refentry.elemid]
            #fi
        elif (pelemtype in ('TABL','SCHN','SCHA')): # aus schn-html zurück ins Main
            if (refentry.elemtype in ('ENTI','ATTR','WRTB','DOKU')):
                #geh zurück ins Basefile
                htmlname = htmlfilelist[0]
            #fi
        #fi
        if curtype != refentry.typename:
            if curtype != '':
                fhtml.write(writetableline(pwerte=[transl(curtype), kinder.rstrip(', ')]))
                kinder = ''
            #fi
            curtype = refentry.typename
        #fi
        kinder += href(ref=refentry.anker, anz=refentry.name,htmlfile=htmlname) + ', '
    #for
    fhtml.write(writetableline(pwerte=[transl(curtype), kinder.rstrip(', ')]))
    fhtml.write(endtable())
#printreflist

def printwrtbattrlist(pwrtbid, wrtgruppe=False):
    alist = web_sql.namelist(ptype='ATTG' if wrtgruppe else 'ATTR'
                             , plang=reportLang(), pid=pwrtbid)
    if (len(alist)==0):
        return
    fhtml.write(tablehtml(ptitel=transl('Verwendet in Attributgruppen' if wrtgruppe
                                                else 'Verwendet für Attribute')
                           , pueberschriften=[transl('Attribut' if wrtgruppe
                                                else 'Attributgruppe')]
                          ,pwerteliste= [[href(ref=a[1], anz=a[0])] for a in alist]))
#printattrlist

def printwrtbmembers(pwrtbid):
    elems = web_sql.wbgrelements(wrtbid=pwrtbid)
    if (len(elems)==0):
        return
    fhtml.write(tablehtml(ptitel=transl('Elemente')
                           , pueberschriften=
                                [transl('Element')
                                ,transl('Beschreibung')
                                ,transl('Wertebereich')
                                ,transl('geändert')
                                 ]
                          ,pwerteliste= [[e[0], e[1]
                                            , href(ref=web_sql.wrtbAnker(e[9])
                                                    ,anz=e[2]+' ('+anzDatentyp(e[3])+')')
                                            , e[5] +' , ' + e[6]] for e in elems]))
#printwrtbmembers

def printwertelist(p_wrtbid):

    wlist = web_sql.wrtbwerte(p_wrtbid=p_wrtbid)
    if (len(wlist)==0):
        return
    fhtml.write(tablehtml(ptitel=transl('Werteliste')
                           , pueberschriften=(transl('Nr'), transl('Wert'), transl('Anzeige'), transl('Beschreibung'))
                           , pheadlevel=3
                          ,pwerteliste= wlist))
    #fhtml.write(starttable(ptitel=transl('Werteliste')
    #                       , pueberschriften=(transl('Nr'), transl('Wert'), transl('Anzeige'), transl('Beschreibung'))
    #                       , pheadlevel=3))
    #for w in wlist:
    #    fhtml.write(writetableline(pwerte=w))
    #fhtml.write(endtable())
#printwertelist

def printcontentwrtb(p_list):
    printcontentstart ('domains')
    for w in p_list:
        wrtb_id = w[0]
        wrtb_name = w[1]
        wrtb_descr = w[4]
        wrtb_typ = w[5]

        lbc = str(newbarcounter())
        printcontent(ptype=transl('Wertebereich')
                    ,panker=web_sql.wrtbAnker(wrtb_id) #id
                    ,pname=wrtb_name
                    ,pdescr=lf2htmlbr(nvl(wrtb_descr))
                    ,plbc=lbc)

        if (wrtb_typ in ('TEXT','LOV')):
            infoheaders = (transl('Datentyp'), transl('Max. Länge'), transl('Syntaxregel'), transl('geändert'))
            infovalues = (nvl(anzDatentyp(wrtb_typ)),nvl(w[9]),nvl(w[10]),nvl(w[22])+','+nvl(w[21]))
        elif (wrtb_typ == 'BIN'):
            infoheaders = (transl('Datentyp'), transl('Inhaltstyp'), transl('Format'), transl('geändert'))
            infovalues = (nvl(anzDatentyp(wrtb_typ)),anzinhalttyp(nvl(w[17])), nvl(w[18]),nvl(w[22])+','+nvl(w[21]))
        elif (wrtb_typ == 'GRP'):
            infoheaders = (transl('Datentyp'), transl('geändert'))
            infovalues = (anzDatentyp(wrtb_typ),nvl(w[22])+','+nvl(w[21]))
        elif (wrtb_typ == 'NUM'):
            infoheaders = (transl('Datentyp'), transl('Vorkommast.'), transl('Nachkommast.')
                           , transl('Rundungseinh.'), transl('Einheit'), transl('Min. Wert'), transl('Max. Wwert')
                           , transl('geändert'))
            infovalues = (nvl(anzDatentyp(wrtb_typ)),nvl(w[13]),nvl(w[14]),nvl(w[15]),nvl(w[16]),nvl(w[12]),nvl(w[11])
                          ,nvl(w[22])+','+nvl(w[21]))
        elif (wrtb_typ == 'ZPKT'):
            infoheaders = (transl('Datentyp'), transl('Min. Wert'), transl('Max. Wwert'), transl('Granularität')
                           , transl('geändert'))
            infovalues = (nvl(anzDatentyp(wrtb_typ)),nvl(w[6]),nvl(w[7]),anzgranul(nvl(w[8])), nvl(w[22]) + ',' + nvl(w[21]))
        else: infoheaders,infovalues = None,None
        #fi
        if infoheaders is not None: printcontentinfo(pheaders=infoheaders, pvalues=infovalues)

        if (wrtb_typ == 'LOV'):
            printwertelist(p_wrtbid=wrtb_id)

        if (wrtb_typ == 'GRP'):
            printwrtbmembers(pwrtbid=wrtb_id)

        printwrtbattrlist(pwrtbid=wrtb_id,wrtgruppe=False)
        printwrtbattrlist(pwrtbid=wrtb_id,wrtgruppe=True)

        printcontentend(lbc)    #for
#printcontentwrtb

def printcontentdoku(plist):
    printcontentstart ('documents')
    infoheaders = (transl('Format'), transl('Referenz'), transl('Vaterdokument')
               , transl('Unterdokumente'))
    for d in plist:
        lbc = str(newbarcounter())
        doku_id = d[0]
        doku_name = d[1]
        doku_format = d[2]
        doku_referenz = d[3]
        parent_id = d[4]
        parent_name = d[5]
        doku_kinder = d[6]
        printcontent(ptype=transl('Dokument')
                    ,panker=web_sql.dokuAnker(doku_id) #id
                    ,pname=doku_name
                    ,pdescr=""
                    ,plbc=lbc)

        """DOKU_ID,DOKU_NAME,DOKU_FORMAT,DOKU_REFERENZ
            ,parent_id, parent_name, kinder"""
        kinder = ''
        if doku_kinder is not None:
            #print(kinder, kinder.split('|'), sep=' | ')
            for k in doku_kinder.split('|'):
                k1 = k.split(':')
                kinder += href(ref=web_sql.dokuAnker(k1[0]),anz=k1[1]) + ', '
            #for
            kinder = kinder.rstrip(', ')
        #fi
        infovalues = (nvl(doku_format), nvl(doku_referenz), href(ref=web_sql.dokuAnker(parent_id), anz=nvl(parent_name))
                , kinder)
        printcontentinfo(pheaders=infoheaders,pvalues=infovalues)

        printreflist(pelemid=doku_id,pelemtype='DOKU')

        printcontentend(lbc)
    #for
#printcontentdoku


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
    libSourceDirec = os.path.dirname(os.path.abspath(__file__))
    libSourceDirec +='/../html-lib/';
    if (parameters.logoFileName() is None) :parameters.logoFileName(searchlogo(imagedirec));

# setWebDirec

def createlib():
    if os.path.exists(cssdirec):
        pass
        #shutil.rmtree(cssdirec)
    else:
        shutil.copytree(libSourceDirec+'css',cssdirec)

    if os.path.exists(icondirec):
        pass
        #shutil.rmtree(icondirec)
    else:
        shutil.copytree(libSourceDirec + 'icons', icondirec)
    if os.path.exists(imagedirec):
        pass
        #shutil.rmtree(imagedirec)
    else:
        shutil.copytree(libSourceDirec+'image',imagedirec)
#createlib

def createFile(pfilename):
    global fhtml
    webfile = webDirectory + pfilename
    if os.path.exists(webfile):
        os.remove(webfile)
    fhtml = open(webfile,'w')
#createFile
def closefile():
    global fhtml
    fhtml.close()
#closefile

def attname2element(pattrname):
    if pattrname in ['ENTI_NAME','ATTR_NAME']:
        return transl('Name')
    elif pattrname in ['ENTI_COMMENT','ATTR_COMMENT']:
        return transl('Beschreibung')
    elif pattrname in ['ENTI_SYNONYM']:
        return transl('Synonym')
    else:
        return pattrname
    #fi
#attrname2element
def findtransl(pattr,pmodeid,plangs):
    tl = [attname2element(pattr)]
    for l in plangs:
        eintrag = web_sql.transltext(pattr=pattr, pmodeid=pmodeid, plang=l)
        if (pattr in ('ENTI_NAME','ATTR_NAME')):
            id=web_sql.elementid(pmodeid=pmodeid,ptyp=pattr[0:4])
            eintrag = filehref(ref=web_sql.entiAnker(id) if pattr == 'ENTI_NAME'
                                        else web_sql.attrAnker(id)
                               ,anz=eintrag,plang=l)
        #fi
        tl.extend([eintrag])
    return tl
#findtransl

def printtransl(pentiid=None, pattrid=None):
    langs=projekt.projektlangs().split(',')
    try: langs.remove(reportLang())
    except: pass
    if len(langs)== 0 : return
    head=[transl('Element')]
    head.extend(langs)
    if (pentiid is not None):
        modeid=dbLookup.modeid(p_entiid=pentiid)
        transllist= [findtransl(pattr='ENTI_NAME',pmodeid=modeid,plangs=langs)
                    ,findtransl(pattr='ENTI_SYNONYM',pmodeid=modeid,plangs=langs)
                    ,findtransl(pattr='ENTI_COMMENT',pmodeid=modeid,plangs=langs)]
    elif (pattrid is not None):
        modeid=dbLookup.modeid(p_attrid=pattrid)
        transllist= [findtransl(pattr='ATTR_NAME',pmodeid=modeid,plangs=langs)
                    ,findtransl(pattr='ATTR_COMMENT',pmodeid=modeid,plangs=langs)]
    #print(transllist)
    fhtml.write(tablehtml(ptitel=transl('Übersetzungen')
                           , pueberschriften=head
                           , pheadlevel= 2
                          ,pwerteliste=transllist))
    #fhtml.write(starttable(ptitel=transl('Übersetzungen')
    #                       , pueberschriften=head
    #                       , pheadlevel= 2))
    #for d in transllist:
    #    fhtml.write(writetableline(pwerte=d))
    #fhtml.write(endtable())
#printtransl

