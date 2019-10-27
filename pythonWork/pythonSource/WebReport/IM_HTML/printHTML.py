from IM_DB import parameters
import os,shutil
from IM_HTML import web_sql

outputDirectory:str = None
webDirectory:str = "";
webFileName:str = "";
webFileNamePath:str = "";
libSourceDirec:str = "";
imagedirec:str = "";
cssdirec:str = "";
icondirec:str = "";

fhtml = None

greportLang:str = None
def reportLang(newval=None):
    global greportLang
    if (newval is None):
        return greportLang
    else:
        greportLang = newval
#reportLang

translNameEN = {'Anzeige': 'Display'
                ,'Arc': 'Arc'
                ,'Attribut': 'Attribute'
                ,'Attribut(e)': 'Attribute(s)'
                ,'Attribute': 'Attributes'
                ,'Author': 'Author'
                ,'Beschreibung': 'Description'
                ,'Beziehung': 'Relationship'
                ,'Beziehung(en)': 'relationship(s)'
                ,'Beziehungen': 'Relationships'
                ,'Binär': 'Binary'
                ,'Datentyp': 'Datatype'
                ,'Deskriptor': 'descriptor'
                ,'Domänen': 'Domains'
                ,'Domäne': 'Domain'
                ,'Entität': 'Entity'
                ,'Entität1': 'Entity1'
                ,'Entität2': 'Entity2'
                ,'Entität/Tabelle': 'Entity/Table'
                ,'Entitäten': 'Entities'
                ,'Erstellt': 'Generates'
                ,'geändert': 'updated'
                ,'Gruppenattribut': 'Groupattribute'
                ,'historisiert': 'historicized'
                ,'in Schlüssel': 'within key'
                ,'Informationsmodell {} (Stand: {})': 'Informationmodel {} (Status: {})'
                ,'Ja': 'Yes'
                ,'Mehr': 'more'
                ,'Name': 'Name'
                ,'Nein': 'No'
                ,'Nr': 'Nr'
                ,'Numerisch': 'Numerical'
                ,'Pflichtattribut': 'Attribute of duty'
                ,'Schlüssel': 'Key'
                ,'Sort': 'Sort'
                ,'Subentität': 'Subentity'
                ,'Subentitäten': 'Subentities'
                ,'Suchbegriff': 'search key'
                ,'Superentität': 'Superentity'
                ,'Synonyme': 'Synonyms'
                ,'Technischer Name': 'Technical Name'
                ,'Text': 'Text'
                ,'Treffer': 'Hits'
                ,'Typ': 'Type'
                ,'UDP-Matrix': 'UDP-Matrix'
                ,'übersetzt': 'translated'
                ,'verschlüsselt': 'encrypted'
                ,'Verwendet von': 'used by'
                ,'Wert': 'Value'
                ,'Wertebereich': 'Domain'
                ,'Werteliste': 'Valuelist'
                ,'wiederholt': 'repeated'
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
    lb = b if (type(b) == 'bool') else True if (b == 'TRUE') else False
#    print (b,lb,type(b))
    return       'class="icon-check" src="icons/checkmark.svg"'  \
       if lb else 'class="icon-remove" src="icons/cross.svg"'
#bool2icon
def anzDatentyp(dt):
    anzDT = {'BIN': transl('Binär')
             ,'GRP': transl('Gruppenattribut')
             ,'LOV': transl('Werteliste')
             ,'NUM': transl('Numerisch')
             ,'TEXT': transl('Text')
             ,'ZPKT': transl('Zeitpunkt')}
    return anzDT[dt]
#anzDatentyp

def printhead(p_firma,p_titel,p_info,p_logofilename):
    htmlhead:str = """<html lang="en">

<head>
    <title>IME - Webseite</title>
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
    """.format (p_firma,p_titel,p_info,p_logofilename,p_firma)
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
""".format(transl("Suchbegriff"),transl("Treffer"))
    fhtml.write(contenhead)
#printlistofcontenthead

def printlistofcontentfoot():
    contentfoot = """
            </div>
    </div>
"""
    fhtml.write(contentfoot)
#printlistofcontentfoot

def printlistofcontentelementstart():
    contentstart="""    <div class="contentView">
"""
    fhtml.write(contentstart)
#printlistofcontentelementstart
def printlistofcontentelementend():
    contentend = """    </div>
"""
    fhtml.write(contentend)
#printlistofcontentelementend

def printlistofcontentelement(p_name, p_list):
    contentelementhead= """
                <div class="panel-body" id="entityL">
                    <div class="panel">
                        <div class="panel-heading collapsed" data-toggle="collapse" data-target="#bar00">
                            <label class="label0">{}</label>
                            <img class="icon-minus" alt="minus" src="icons/minus.svg">
                            <img class="icon-plus" alt="plus" src="icons/plus.svg">
                        </div>
                    </div>
                    <!-- The inside div eliminates the 'jumping' animation. -->
                    <div class="collapse" id="bar00">
                        <ol class="tree" id="entityList">
    """.format(transl(p_name))
    contentline="""
                <li class="obj"><a href="#{}" target="details">{}</a></li>"""
    contentelementfoot="""
                    </ol>
            </div>
        </div>
""";
    fhtml.write(contentelementhead)
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
""".format("""class="descr">Diese Webseite enhtält den ganzen Inhalt 
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


def printcontententi(p_list):
    contenthead="""        <!--entities-->"""

    contentelementhead = """        <div class="entity" id="{}">
            <div class="describtion">
                <p>{}</p>
                <h1>{}</h1>
                <p1>{}</p1>
            </div>
        """
    contentelementfoot = """                 <div class="panel">
                <div class="panel-heading collapsed" data-toggle="collapse" data-target="#bar0">
                    <img class="icon-chevron-up" alt="minus" src="icons/chevron-up.svg">
                    <img class="icon-chevron-down" alt="plus" src="icons/chevron-down.svg">
                    <label class="label1">{}</label>
                </div>
            </div>
        </div>
    """
    detailshead = """            <div class="panel-body">
                <!-- The inside div eliminates the 'jumping' animation. -->
                    <div class="collapse" id="bar0">                    
"""
    detailsfoot = """            
                            </div>
                            </div>
"""

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
                                        </tr>
"""
    infohead = """
                            <h2>{}</h2>
                            <table class="table borderless">
                                <tbody>
"""
    infoline = """
                                    <tr>
                                        <td>{}</td>
                                        <td>{}</td>
                                    </tr>
"""
    infofoot = """
                                </tbody>
                            </table>
"""
    fhtml.write(contenthead)
    for e in p_list:
        fhtml.write(contentelementhead.format(web_sql.entiAnker(e[0]) #id
                                            ,transl('Entität')
                                            ,e[1] #name
                                            , nvl(e[2]))) #descr

        fhtml.write(detailshead)
        fhtml.write(infohead.format(transl('Informationen')))
        if (e[8] is not None):
            fhtml.write(infoline.format(transl('Synonyme'),e[8]))
        if (e[6] is not None):
            fhtml.write(infoline.format(transl('Superentität'),e[6]))
        if (e[7] is not None):
            fhtml.write(infoline.format(transl('Subentitäten'),e[7]))
        fhtml.write(infoline.format(transl('geändert'),nvl(e[3]) + ', ' + nvl(e[4])))
        fhtml.write(infofoot)

        #####Attribute block
        fhtml.write(attrhead.format(transl('Attribute'),transl('Name'),transl('Domäne'),transl('Typ')
                                    ,transl('Pflichtattribut'),transl('Deskriptor'),transl('übersetzt')
                                    ,transl('historisiert'),transl('wiederholt'),transl('verschlüsselt')))
        alist = web_sql.attrlist(p_entiid=e[0],p_lang=reportLang())
        if (alist is not None):
            for a in alist:
                fhtml.write(attrline.format(web_sql.attrAnker(a[0]), a[1], web_sql.wrtbAnker(a[3]), a[2], anzDatentyp(a[4])
                                            ,bool2icon(a[5]),bool2icon(a[6]),bool2icon(a[7])
                                            ,bool2icon(a[8]),bool2icon(a[9]),bool2icon(a[10])))
            #for
        #fi

        fhtml.write(attrfoot)

        fhtml.write(detailsfoot)
        fhtml.write(contentelementfoot.format(transl('Mehr')))
    #for
#printcontent

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


def writeToc(str):
    global ftoc
    ftoc.write(str)


def closeToc(str):
    global ftoc
    ftoc.write(str)
    ftoc.write ("""</body> </html>""")
    ftoc.close()

def writeCont(str,values=()):
    global fcont
    vals:str = '' if values == () else ','.join(values)
    fcont.write(str .format(vals))

def closeCont(str):
    global fcont
    fcont.write(str)
    fcont.write("""</body> </html>""")
    fcont.close()

def printTable(werte,anker=''):
    global fcont
    fcont.write("""<table class="w_15">
		<tbody>
    """)
    idx = 0
    for w in werte:
        idx += 1
        if (anker == '' or idx > 1):
            fcont.write("""<tr> <td class="td_h_v w_4" ><span>{}</span></td>\
	    	    <td class="td w_16"><span>{}</span></td></tr>""" \
                .format(w,werte[w]))
        else:
            fcont.write("""<tr> <td class="td_h_v w_4" > <span>{}</span></td>\
        		    <td class="td obj_name w_12"><a name="{}">{}</a></td></tr>""" \
                    .format(w,  anker , werte[w]))

    fcont.write("""</tbody></table><p></p>""")
#printTable

def startTable(titel,ueberschriften,anker=''):
    global fcont
    if (anker == ''):
        fcont.write("""<p></p><span class="t_cap">{}</span>
	            <table class="w_5"><thead><tr>
                """.format(titel))
    else:
        fcont.write("""<p></p><span class="t_cap">{}</span>
        	            <table id="{}"  class="w_5"><thead><tr>
                        """.format(titel,anker))

    for w in ueberschriften:
        fcont.write("""<th class="td_h_v w_4"><span>{}</span></th>""" \
                .format(w))

    fcont.write("""</tr></thead><tbody>""")
#startTable
def nvl(x):
    return x if (x is not None) else ''
#nvl
def writeTable(werte):
    global fcont
    fcont.write("""<tr>""")
    for w in werte:
        fcont.write("""<td class="td_r">{}</td>""" .format(nvl(w)))
    #rof
    fcont.write("""</tr>""")

#writeTable

def endTable(str):
    global fcont
    fcont.write("""</tr></tbody></table><p></p>""")
#endTable
