import os
import re
import shutil

from IM_DB import parameters
from IM_OBJECTS import *
from WEB_OBJECTS import *
import html
from parameters import nvl,nvl2

outputDirectory: str = None
webDirectory: str = "";
webFileName: str = "";
webFileNamePath: str = "";
libSourceDirec: str = "";
imagedirec: str = "";
cssdirec: str = "";
icondirec: str = "";
htmlfilelist = {}
model = {}

"""zum Zählen der lokalen Ziele für collapse"""
barcounter: int = 0


def newbarcounter():
    global barcounter
    barcounter += 1
    return barcounter


# newbarcounter

fhtml = None


def lf2htmlbr(pstr):
    try:
        return re.sub(r"\n", "<br>\n", pstr)
    except:
        return pstr


# lf2htmlbr


def filehref(pref, panz, plang, pimg=None):
    img = nvl2(pimg,'','<img class="icon-check" src="icons/{}">'.format(pimg))
    return """<a href="{}{}" target="_blank" >{}{}</a>""" \
        .format(webFileName + '_' + plang.lower() + '.html', nvl2(pref,"","#") , panz, img)


def href(ref, anz, htmlfile=''):
    if anz is None: return ''
    sep = nvl(ref,'#')
    return """<a href="{}{}" target="{}">{}</a>""".format(htmlfile
                                                          , '{}{}'.format(sep, ref)
                                                          , '_self' if htmlfile == '' else '_blank'
                                                          , html.escape(anz))


def isIconstr(w):
    if (w is None) or (type(w) != str):
        return False
    elif (w.startswith('class="')):
        return True
    else:
        return False


def bool2icon(b):
    lb = b if (type(b) == bool) else True if (b == 'TRUE') else False
    #    print (b,lb,type(b))
    return 'class="symbol"><img class="icon-check" src="icons/checkmark.svg"' \
        if lb else 'class="symbol"><img class="icon-remove" src="icons/cross.svg"'


# bool2icon

def arrow2icon(direc):
    if (direc == 'up'):
        return 'class="leftsymbol"><img class="icon-up" src="icons/uparrow.svg"'
    elif (direc == 'down'):
        return 'class="leftsymbol"><img class="icon-down" src="icons/downarrow.svg"'
    else:
        return direc


# arrow2icon

# def list2href(p_list, ptype):
#     """Verandelt eine kommagetrennte Liste von nnn:xxxx in einen String von kommagetrennten  HREF-Webeinträgen"""
#     if p_list is None: return None
#     list = p_list.split(",")
#     elem = []
#     for el in list:
#         el1  = el.split(':')
#         elem.append(href(pref=
#             web_sql.entiAnker(el1[0]) if ptype == 'ENTI' else
#             web_sql.dokuAnker(el1[0]) if ptype == 'DOKU' else
#             el1[0]
#         , panz=el1[1]))
#     return ', '.join(elem)
# #list2href

contentelementfoot: str = """                 <div class="panel">
                <div class="panel-heading collapsed" data-toggle="collapse" data-target="#bar{}">
                    <img class="icon-chevron-up" alt="minus" src="icons/chevron-up.svg">
                    <img class="icon-chevron-down" alt="plus" src="icons/chevron-down.svg">
                    <label class="label1">{}</label>
                </div>
            </div>
        </div>
        </div>
    """


def printhead(p_firma, piconfilename, p_titel, p_info, p_logofilename):
    htmlhead: str = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>{}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" type="image/png" href="{}">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="css/main.css">
    <script src="js/IM.js"></script>
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
    """.format(p_titel, piconfilename, p_firma, p_titel, p_info, p_logofilename, p_firma)
    fhtml.write(htmlhead)


# printhead

def printfoot():
    htmlend: str = """    <!-- modal für mobile devices (search) -->
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


# printfoot

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
""".format(Sprachtext.transl("Suchbegriff"), Sprachtext.transl("Treffer"))
    fhtml.write(contenhead)


# printlistofcontenthead

def printlistofcontentfoot():
    contentfoot = """
            </div>
        </div>
    </div>
"""
    fhtml.write(contentfoot)


# printlistofcontentfoot


def printlistofcontentelement(pname, plist, pintfid=0,pfileonly=False):
    if (plist is None or len(plist) == 0): return
    lbc = str(newbarcounter())
    listcontentelementhead = """
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
    listcontentline = """
                <li class="obj"><a href="{}" target="{}">{}</a></li>"""

    listcontentelementfoot = """
                    </ol>
            </div>
        </div>
"""
    fhtml.write(listcontentelementhead.format(pname, lbc, Sprachtext.transl(pname), lbc, pname))
    local = re.match(r'/(.+/)*{}'.format(htmlfilelist[pintfid]), fhtml.name)
    for entry in plist:
        anker = '#' + entry['anker']
        fhtml.write(listcontentline.format(anker, '_self' if local else '_blank', entry['name']))
    fhtml.write(listcontentelementfoot)
    return
    for l in plist:
        inanker = l[1]
        local = re.match(r'/(.+/)*{}'.format(htmlfilelist[inanker.modelid()])
                         , fhtml.name)
        anker = '' if (local) else htmlfilelist[inanker.modelid()]
        if not pfileonly:
            anker += '#' + inanker.anker()
        #fi
        anzeige = l[0]
        fhtml.write(listcontentline.format(anker, '_self' if local else '_blank', anzeige))
    #for
    fhtml.write(listcontentelementfoot)


def lang2img(plang):
    if plang in (Sprachtext.DE, Sprachtext.FR):
        return plang + ".png"
    elif plang == Sprachtext.EN:
        return "gb.png"
    else:
        return None


# lang2img
def printcontenthead(pfirma, ptitel):
    contenthead = """    <div class="wrapper">
        <div class="top-container">
            <p3 {} 
            </p3>
        <div>
            {}
        </div>          
        </div>
"""
    if Sprachtext.reportLang() == Sprachtext.DE:
        f = """class="descr">Diese Webseite enthält den ganzen Inhalt 
            des <p2 class="IM">Informationsmodells {}</p2> von {}. 
            Diese Seite wurde von Software von <p2 class="fyayc">foryouandyourcustomers</p2> 
            erstellt.""".format(ptitel, pfirma)
    elif Sprachtext.reportLang() == Sprachtext.FR:
            f = """class="descr">Ce site web contient l'intégralité du contenu 
                du <p2 class="IM">Modèle d'Information {}</p2> de {}. 
                Cette page a été créée par le logiciel de <p2 class="fyayc">foryouandyourcustomers</p2>. 
                """.format(ptitel, pfirma)
    else:
        f = """class="descr">This website contains the complete content 
            of the <p2 class="IM">Information model {}</p2> from {}. 
            This page was created with software from <p2 class="fyayc">foryouandyourcustomers</p2>.""" \
            .format(ptitel, pfirma)
    # fi
    langs = projekt.projektlangs().split(',')
    try:
        langs.remove(Sprachtext.reportLang().lower())
    except:
        pass
    str = ''
    for l in langs:
        str += filehref(pref=None, panz=l + '   ', plang=l, pimg=lang2img(l.lower()))
    fhtml.write(contenthead.format(f, str))


# printcontenthead

def printcontentfoot():
    contentfoot = """      </div>
"""
    fhtml.write(contentfoot)


# printcontentfoot

def printcontentstart(pname):
    fhtml.write("        <!--{}-->".format(pname))


# printcontentsstart
def printcontentend(plbc):
    fhtml.write("""            
                            </div>""")
    fhtml.write(contentelementfoot.format(plbc, Sprachtext.transl('Mehr')))
# printcontentend

def printcontent(ptype, pname,panker, plbc, pdescr="", pmaster="", piconstr= ""):
    contentelementhead = """        <div class="entity" id="{}">
            <div class="describtion">
				 <span> 
					 <script>entityheader('{}','{}','{}','{}','{}');</script>
			     </span>
            </div>
             <div class="panel-body">
            <div class="collapse" id="bar{}">                    
"""
    """                <p>{}</p>
                <h1>{}{}</h1>
                {}
                {}
"""
    fhtml.write(contentelementhead.format(panker, ptype, html.escape(pname )
                                          ,piconstr
                                          , pmaster
                                          , pdescr.replace('\n', '').replace('\r', '').replace("'",'&#39;') #"" if (pdescr == "") else "<p1>{}</p1>".format(pdescr)
                                          , plbc))
# printcontent

def printflagline(pheaders, pvalues):
    infohead = """
      <!-- The inside div eliminates the 'jumping' animation. -->
                        <div id="containerflag">
                        <div class="table-responsive">
                            <table class="table borderlessl">
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


# printcontentinfo


def printcontentinfo(ptitle, pheaders, pvalues):
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
    fhtml.write(infohead.format(ptitle))
    fhtml.write(trstart)
    for h in pheaders:
        fhtml.write(techheadline.format(h))
    fhtml.write(trend)
    fhtml.write(trstart)
    for v in pvalues:
        fhtml.write(techlineline.format(v))
    fhtml.write(trend)
    fhtml.write(infofoot)


# printcontentinfo


def printattrlist(pwebenti):
    alist = pwebenti.getwebattributes()
    if (len(alist) == 0):
        return

    fhtml.write(starttable(ptitel=Sprachtext.transl('Attribute')
                           , pueberschriften=(
            Sprachtext.transl('Name'), Sprachtext.transl('Wertebereich'), Sprachtext.transl('Typ')
            , Sprachtext.transl('Pflichtattribut'), Sprachtext.transl('Schlüssel'), Sprachtext.transl('Deskriptor'),
            Sprachtext.transl('übersetzt')
            , Sprachtext.transl('historisiert'), Sprachtext.transl('wiederholt'), Sprachtext.transl('verschlüsselt'))))

    for webattr in alist:
        attr = webattr.dbobject()
        webdomain = webattr.getwebdomain()
        domain = webdomain.dbobject()
        domname = html.escape(webdomain.getname(Sprachtext.reportLang()))
        domainref = domname if domain.isderived() \
                        else href(ref=webdomain.webanker().anker(), anz=domname)
        fhtml.write(writetableline(pwerte=(href(ref=webattr.webanker().anker(), anz=webattr.getname(Sprachtext.reportLang()))
                                           , domainref
                                           , html.escape(domain.displdatatype())
                                           , bool2icon(attr.attr_is_mandatory), bool2icon(attr.isinkey()),
                                           bool2icon(attr.attr_is_descriptive)
                                           , bool2icon(attr.attr_is_translated), bool2icon(attr.attr_is_historicised)
                                           , bool2icon(attr.attr_is_repeated), bool2icon(attr.attr_is_encrypted))))
    # for
    fhtml.write(endtable())


# printattrlist

def startabschnitt(p_titel):
    start = """        <h2>{}</h2>
                            <div id="container0">
    """
    return start.format(html.escape(p_titel))


# startabschnitt
def endabschnitt():
    end = """        </div>
    """
    return end


# startabschnitt
def starttable(ptitel, pueberschriften, pheadlevel=2, ptabid=None, pselfanker=None):
    tabhead = """        <h{}>{}</h{}>{}
                        <div id="container1">
                            <div class="table-responsive">
                   <table class="table borderless" {}>
                                            <tbody>
                                        <tr>
"""
    tabheads = """             <th>{}</th>
"""
    #    tabheads="""<th class="attribute">{}</th>"""
    retval = []
    retval.append(tabhead.format(pheadlevel, ptitel, pheadlevel
                                 , nvl2(ptabid,'','<a href="#{}" onclick="download_table_as_csv(\'{}\');">download as CSV</a>'
                                                    .format(
            pselfanker, ptabid))
                                 , nvl2(ptabid,'','id="{}"'.format(ptabid))))
    for u in pueberschriften:
        retval.append(tabheads.format(html.escape(u)))
    return ''.join(retval)


# starttable

def writetableline(pwerte, plineid=None):
    linestart = """            <tr>
        """ if plineid is None else """            <tr id = "{}">
        """.format(plineid)
    line = """             <td>{}</td>
    """
    iconline = """           <td {}></td>
    """
    lineend = """               </tr>
    """
    retval = []
    retval.append(linestart)
    for w in pwerte:
        if (isIconstr(w)):
            retval.append(iconline.format(lf2htmlbr(nvl(w))))
        else:
            retval.append(line.format(nvl(lf2htmlbr(nvl(w)))))
    retval.append(lineend)
    return ''.join(retval)


def endtable():
    return """        
                     </tbody>
                            </table>
                            </div>
                                </div>
    """


# endtable

def tablehtml(ptitel, pueberschriften, pwerteliste, plineid=None, pheadlevel=2, ptabid=None, pselfanker=None):
    retval = starttable(ptitel=ptitel, pueberschriften=pueberschriften, pheadlevel=pheadlevel, ptabid=ptabid,
                        pselfanker=pselfanker)
    for lw in pwerteliste:
        retval += writetableline(pwerte=lw, plineid=plineid)
    retval += endtable()
    return retval


def printentikeys(pwebenti,plang):
    keylist = pwebenti.getkeylist(plang=plang)
    """(key-name,attrlist (commaseparated),relation-list sommaseparated)"""
    if (len(keylist) == 0):
        return
    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Schlüssel')
                          , pueberschriften=(
                Sprachtext.transl('Name'), Sprachtext.transl('Attribute(e)'),
                Sprachtext.transl('Beziehung(en)'))
                        , pwerteliste=[(k[0],k[1],k[2]) for k in keylist]
                  )
                )
# printentikeys

def printmappinghtml(pwerte, ptitel, pueberschriften, pheadlevel=2):
    # pwerte, list of entries mit {'name':webanker}
    if (pwerte is None or len(pwerte) == 0):
        return
    werte = []
    for t in pwerte:
        name, tabs = t[0], t[1]
        commalist = ', '.join([href(ref=value.anker() , anz=key, htmlfile=htmlfilelist[value.modelid()]) if isinstance(value,Webanker) else value \
                               for key, value in tabs.items()])
        werte.append([name, commalist])
    fhtml.write(tablehtml(ptitel=ptitel
                          , pueberschriften=pueberschriften
                          , pheadlevel=pheadlevel
                          , pwerteliste=werte
                          )
                )


# printmappinghtml

def printmapping(pentiid=None, pattrid=None):
    # name, list of entries mit {'name':webanker}
    if pentiid is not None:
        werte = TablEntiMap.tablelist(pentiid=pentiid)
        titel = Sprachtext.transl('Relational Mapping (Tabellen)')
        ueberschr = (Sprachtext.transl('Relational Model'), Sprachtext.transl('Tabellen'))
    elif pattrid is not None:
        werte = AttrTransf.columnlist(pattrid=pattrid)
        titel = Sprachtext.transl('Relational Mapping (Columns)')
        ueberschr = (Sprachtext.transl('Relational Model'), Sprachtext.transl('Columns'))
    else:
        return
    # fi
    printmappinghtml(pwerte=werte, ptitel=titel, pueberschriften=ueberschr)


def printentirela(pwebenti):
    lang = Sprachtext.reportLang()
    relalist = WebRelation.relalist(pentiid=pwebenti.enti_id, plang=lang,pwith1to1=False)
    if (len(relalist) == 0):
        return
    fhtml.write(starttable(ptitel=Sprachtext.transl('Beziehungen')
                           , pueberschriften=(
            Sprachtext.transl('Name'), Sprachtext.transl('Entität') + '-1', '', Sprachtext.transl('Beziehung'), '',
            Sprachtext.transl('Entität') + '-2'
            , Sprachtext.transl('Arc'), Sprachtext.transl('Schlüssel'),)))
    for webrela in relalist:
        if (pwebenti.enti_id == webrela.from_enti.enti_id):
            # 'Name','Entität1','','Beziehung','', 'Entität2','Arc','Key'
            fhtml.write(writetableline(pwerte=(html.escape(nvl(webrela.rela_name)), html.escape(webrela.from_enti.getname(plang=lang)), '->', html.escape(nvl(webrela.from_rela_assoc, '--'))
                                               , html.escape(nvl(webrela.from_card))
                                               , arrow2icon('down'), nvl(webrela.arcs_name(pentiid=pwebenti.enti_id)), bool2icon(webrela.isinkey))))
            fhtml.write(writetableline(pwerte=('', arrow2icon('up'), webrela.to_card, html.escape(nvl(webrela.to_rela_assoc, '--')), '<-'
                                               , href(ref=webrela.to_enti.webanker().anker(), anz=html.escape(webrela.to_enti.getname(plang=lang))))))
        else:
            fhtml.write(writetableline(pwerte=(html.escape(nvl(webrela.rela_name)), html.escape(webrela.to_enti.getname(plang=lang)), '->', html.escape(nvl(webrela.to_rela_assoc, '--'))
                                               , html.escape(nvl(webrela.to_card))
                                               , arrow2icon('down'), nvl(webrela.arcs_name(pentiid=pwebenti.enti_id)), bool2icon(webrela.isinkey))))
            fhtml.write(writetableline(pwerte=('', arrow2icon('up'), webrela.from_card, html.escape(nvl(webrela.from_rela_assoc, '--')), '<-'
                                               , href(ref=webrela.from_enti.webanker().anker(), anz=html.escape(webrela.from_enti.getname(plang=lang))))))
        # if
    # for
    fhtml.write(endtable())
# printentirela

def printcontentmapping(ptheme=None):
    grouplist= WebUdp.indexlist(ptheme=ptheme)
    if (grouplist is None or len(grouplist) == 0): return
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
    for group in grouplist:
        """[(theme,group)]"""
        lgroup = group[0]
        lanker = group[1]
        headerlist = [Sprachtext.transl('Attribute')]
        udps = WebUdp.contentlist(ptheme=ptheme,pgroup=lgroup,pmeltname=Modelelemtype.ATTR)
        if len(udps) == 0: continue
        udpnames = [html.escape(u.dbobject().udpr_name) for u in udps]
        headerlist.extend(udpnames)

        webattrs = WebUdp.getattributes(ptheme=ptheme, pgroup=lgroup )
        lines = []
        for webattr in webattrs:
            line = [href(ref=webattr.webanker().anker(), anz=webattr.getqualifiedname(plang=Sprachtext.reportLang()))]
            udpvalues = WebUdp.getvalues(ptheme=ptheme, pgroup=lgroup, pmodeid=webattr.getid(),pmeltype=Modelelemtype.ATTR)
            """[(udpr_name,udpv_value)]"""
            if (udpvalues is None or len(udpvalues)==0): continue
            udpvaldict = {html.escape(v[0]): html.escape(v[1]) for v in udpvalues}
            line.extend(udpvaldict[udpname] if udpname in udpvaldict else '' for udpname in udpnames)
            lines.append(line)

        lbc = str(newbarcounter())
        fhtml.write(contentelementhead.format(lanker.anker()
                                              , Sprachtext.transl('Attribute - Mapping')
                                              , lgroup  # anzname
                                              , lbc))
        fhtml.write(detailshead)

        fhtml.write(starttable(ptitel='Mapping'
                               , pueberschriften=headerlist
                               , pheadlevel=3
                               , ptabid='TAB-{}'.format(lgroup if lgroup != '*' else 'ALL')
                               , pselfanker=lanker.anker()))
        for line in lines: fhtml.write(writetableline(pwerte=line))
        fhtml.write(endtable())

        fhtml.write(detailsfoot)
        fhtml.write(contentelementfoot.format(lbc, Sprachtext.transl('Mehr')))
    # for


def printUDP(p_meltname, pid):
    startwritten = False

    for udpgroup in Userdefprop.grouplist():
        """[(theme,group)]"""

        """translations are not printed"""
        if (udpgroup[0] == parameters.odmUDPTranslFileName()): continue

        udpentries = [WebUdp(pdbobj=udp) for udp in Userdefprop.getudps(pmeltname=p_meltname,ptheme=udpgroup[0],pgroup=udpgroup[1])]
        """[(theme,group,namelist (comma separated))]"""
        displvalues = {html.escape(udpr.getname()): '' for udpr in udpentries}
        values = Userdefpropvalue.udpvalues(ptheme=udpgroup[0], pgroup=udpgroup[1], pmodeid=pid,pmeltype=p_meltname)
        """[propname, propvalue]"""
        for l in values:
            displvalues[l[0]] = html.escape(l[1])

        """write only if there is at least one value not empty"""
        if (len(displvalues) > list(displvalues.values()).count('')):
            if (not startwritten):
                fhtml.write(startabschnitt(p_titel=Sprachtext.transl('Benutzerdefinerte Eigenschaften')))
                startwritten = True
            # fi

            titel = href(ref=WebUdp.groupwebanker(ptheme=udpgroup[0],pgroup=udpgroup[1]).anker()
                         , anz=html.escape(' {} - {} '.format(udpgroup[0], udpgroup[1])))
            fhtml.write(tablehtml(ptitel=titel
                                  , pueberschriften=list(displvalues.keys())
                                  , pheadlevel=3
                                  , pwerteliste=[list(displvalues.values())])
                        )
        #fi
    #for
    if (startwritten):
        fhtml.write(endabschnitt())
# printUDP

def printentiudp(pentiid):
    printUDP(p_meltname='ENTI', pid=pentiid)
# printentiudp

def printattrudp(pattrid):
    printUDP(p_meltname='ATTR', pid=pattrid)
# printattrudp

def entidiag(pwebenti):
    doppelanker = "{}-{}"
    diaglist = WebDiagram.contentlist(pentiid=pwebenti.enti_id)
    if (len(diaglist) == 0):
        return ''
    diagstring = ', '.join(href(ref=doppelanker.format(diag.webanker().anker(), pwebenti.webanker().anker())
                                , anz=diag.getname()) for diag in diaglist)
    return diagstring
# entidiag

def icontag(pfilename, psize=WebDiagram.ICONSIZE):
    fullfilename = "{}/{}.{}".format('image',pfilename,'png').lower()
    if os.path.isfile(parameters.webDirec()+ fullfilename):
        return pfilename.lower()
        retval = '   <img src="{}" height="{}px" width="{}px">'.format(fullfilename, psize,psize)
    else:
        retval = ''
    return retval


def printcontententi():
    lang = Sprachtext.reportLang()
    printcontentstart('entities')
    infoheaders = (Sprachtext.transl('Synonyme'), Sprachtext.transl('Superentitäten')
                   , Sprachtext.transl('Subentitäten'), Sprachtext.transl('Rollen'), Sprachtext.transl('auf Diagramm(en)')
                   , Sprachtext.transl('geändert'))

    for enti in WebEntity.contentlist(plang=lang):
        lbc = str(newbarcounter())
        printcontent(ptype=Sprachtext.transl('Entität')
                     , panker=enti.webanker().anker()
                     , pname=enti.getname(plang=lang)
                     ,piconstr=icontag(pfilename=enti.dbobject().enti_name)
                     , pdescr=lf2htmlbr(nvl(enti.getdescr(plang=lang)))
                     , plbc=lbc)

        """print entity Info"""
        synos = enti.dbobject().getsynonyms()
        synonyms = '' if (synos is None or len(synos) == 0) else ', '.join(s.getname(plang=lang) for s in synos)
        parents = enti.getparents()
        if (parents is None or len(parents) == 0):
            parentstr = ''
        else:
            parentstr = ", ".join(href(ref=p.webanker().anker(), anz=p.getname(plang=lang)) for p in parents)

        subtypes = enti.getchildren(ptype=Relation.ISASUBTYPE)
        if (subtypes is None or len(subtypes) == 0):
            subtypestr = ''
        else:
            subtypestr = ', '.join(href(ref=c.webanker().anker(), anz=c.getname(plang=lang)) for c in subtypes)

        roles = enti.getchildren(ptype=Relation.ISAROLE)
        if (roles is None or len(roles) == 0):
            rolesstr = ''
        else:
            rolesstr = ', '.join(href(ref=c.webanker().anker(), anz=c.getname(plang=lang)) for c in roles)

        infovalues = (nvl(synonyms), parentstr, subtypestr,rolesstr
                      , entidiag(pwebenti=enti), nvl(enti.enti_uc) + ', ' + nvl(enti.enti_dc))
        printcontentinfo(ptitle=Sprachtext.transl('Informationen'), pheaders=infoheaders, pvalues=infovalues)

        printattrlist(pwebenti=enti)
        printentikeys(pwebenti=enti,plang=lang)
        printentirela(pwebenti=enti)
        printreflist(pelemid=enti.enti_id, pelemtype=Modelelemtype.ENTI)
        printtransl(pwebenti=enti)
        printentiudp(pentiid=enti.enti_id)
        printmapping(pentiid=enti.enti_id)
        printcontentend(lbc)
    # for
# printcontententi

def printcontentattr():
    infoheaders = (
        Sprachtext.transl('Technischer Name'), Sprachtext.transl('Wertebereich'), Sprachtext.transl('Datentyp'),
        Sprachtext.transl('Tooltip')
        , Sprachtext.transl('geändert'))
    flagheaders = (
        Sprachtext.transl('Pflichtattribut'), Sprachtext.transl('Schlüssel'), Sprachtext.transl('Deskriptor'),
        Sprachtext.transl('übersetzt')
        , Sprachtext.transl('historisiert'), Sprachtext.transl('wiederholt'), Sprachtext.transl('verschlüsselt'))
    lang = Sprachtext.reportLang()

    webattrs = [WebAttribute(pdbobj=attr) for attr in Attribute.select(porderby='attr_displ_name')]
    for webattr in webattrs:
        attr = webattr.dbobject()
        printcontentstart('attributes')
        webenti = webattr.getwebentity()
        if webenti is not None:
            master = "<p1>{}: {}</p1><br>" \
                .format(Sprachtext.transl('Entität'), href(ref=webenti.webanker().anker(), anz=webenti.getname(plang=lang)))
        else:
            master = 'Relation tbd'

        lbc = str(newbarcounter())
        printcontent(ptype=Sprachtext.transl('Attribute')
                     , panker=webattr.webanker().anker()
                     , pname=attr.getname(plang=Sprachtext.reportLang())
                     , pmaster=master
                     , pdescr=lf2htmlbr(nvl(attr.getdescr(plang=lang)))
                     , plbc=lbc)
        webdomain = webattr.getwebdomain()
        domainref = webdomain.getname(lang) \
            if webdomain.dbobject().isderived() \
            else href(ref=webdomain.webanker().anker(), anz=webdomain.getname(lang))
        infovalues = (nvl(attr.attr_tech_name, ''), domainref, webdomain.dbobject().displdatatype()
                      , nvl(attr.gettooltip(plang=lang), ''), re.sub(r'^, $', '', nvl(attr.attr_uc) + ', ' + nvl(attr.attr_dc)))
        printcontentinfo(ptitle=Sprachtext.transl('Informationen'), pheaders=infoheaders, pvalues=infovalues)

        flagvalues = (bool2icon(attr.attr_is_mandatory), bool2icon(attr.isinkey()), bool2icon(attr.attr_is_descriptive)
                      , bool2icon(attr.attr_is_translated)
                      , bool2icon(attr.attr_is_historicised), bool2icon(attr.attr_is_repeated),
                      bool2icon(attr.attr_is_encrypted))
        printflagline(pheaders=flagheaders, pvalues=flagvalues)

        printreflist(pelemid=webattr.attr_id, pelemtype='ATTR')
        printtransl(pwebattr=webattr)
        printattrudp(pattrid=webattr.attr_id)
        printmapping(pattrid=webattr.attr_id)
        printcontentend(lbc)
    # for
# printcontentattr

def printreflist(pelemid, pelemtype):
    if (pelemtype == Modelelemtype.DOCU):
        refentries = WebDocument.docureflist(pdocuid=pelemid, plang=Sprachtext.reportLang())
    else:
        refentries = WebDocument.refdokulist(pid=pelemid)
    # fi
    if (refentries is None or len(refentries) == 0): return

    fhtml.write(starttable(ptitel=Sprachtext.transl('Referenziert von')
                           , pueberschriften=[Sprachtext.transl('Typ'), Sprachtext.transl('Elemente')]))

    curtype = ''  # Annahme: Dokumentenliste ist sortiert nach typ und Name
    kinder = ''
    for refentry in refentries:
        htmlname = ''
        anker = None
        if (pelemtype in (Modelelemtype.DOCU, Modelelemtype.ENTI, Modelelemtype.ATTR, Modelelemtype.DOMA)):
            if (refentry.elemtype == Modelelemtype.TABL):
                # Tabellen sind in schn-file
                print ("Table indirect noch zu lösen")
                #tabl = Tabelle().getbyid(refentry.elemid)
                htmlname = htmlfilelist[0]
            elif (refentry.elemtype == Modelelemtype.INTF):
                htmlname = htmlfilelist[refentry.elemid]
                anker = ''  # Schnittstellen haben keinen Anker ausser dem Namen
            # fi
        elif (pelemtype in (Modelelemtype.TABL, Modelelemtype.INTF, Modelelemtype.COLU)):  # aus schn-html zurück ins Main
            if (refentry.elemtype in (Modelelemtype.DOCU, Modelelemtype.ENTI, Modelelemtype.ATTR, Modelelemtype.DOMA)):
                # geh zurück ins Basefile
                htmlname = htmlfilelist[0]
            # fi
        # fi
        if curtype != refentry.typename:
            if curtype != '':
                fhtml.write(writetableline(pwerte=[Sprachtext.transl(curtype), kinder.rstrip(', ')]))
                kinder = ''
            # fi
            curtype = refentry.typename
        # fi
        anker = nvl(anker, refentry.anker.anker() if type(refentry.anker) == Webanker else refentry.anker)
        kinder += href(ref=anker, anz=refentry.name if refentry.direct else '(' + refentry.name + ')'
                       , htmlfile=htmlname) + ', '
    # for
    fhtml.write(writetableline(pwerte=[Sprachtext.transl(curtype), kinder.rstrip(', ')]))
    fhtml.write(endtable())


def printdomaattrlist(pdomaid, pisgroup=False):
    alist = WebDomain.indexlist(porigin=Domain.DOMAIN,pdomaid=pdomaid,plang=Sprachtext.reportLang()) \
        if pisgroup else WebAttribute.indexlist(pdomaid=pdomaid,plang=Sprachtext.reportLang())
    """[(name,anker,id)]"""
    if (len(alist) == 0):
        return

    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Verwendet in Attributgruppen' if pisgroup
                                                   else 'Verwendet für Attribute')
                          , pueberschriften=[Sprachtext.transl('Attributgruppe' if pisgroup
                                                               else 'Attribute')]
                          , pwerteliste=[[href(ref=a[1].anker(), anz=a[0])] for a in alist]))


def printdomacollist(pdomaid):
    clist = Schnittstelleattr.select(pwhere='scha_doma_id = {}'.format(pdomaid))
    webclist = clist
    if (len(clist) == 0):
        return
    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Verwendet für Columns')
                          , pueberschriften=[Sprachtext.transl('Column')]
                          , pwerteliste=[[href(ref="COL"+str(col.scha_id) #col.webanker().anker()
                                               , anz="{} ({}:{})".format(col.scha_column_name, col.getintfname(),
                                                                         col.gettablname())
                                               , htmlfile=htmlfilelist[col.getintfid()]
                                               )
                                          ] for col in clist
                                         ]))


def printdomamembers(pdoma):
    elems = pdoma.dgrmelements()
    if (len(elems) == 0):
        return
    lang =Sprachtext.reportLang()
    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Elemente')
                          , pueberschriften=
                          [Sprachtext.transl('Element')
                              , Sprachtext.transl('Beschreibung')
                              , Sprachtext.transl('Wertebereich')
                              , Sprachtext.transl('Pflichtattribut')
                              , Sprachtext.transl('geändert')
                           ]
                          , pwerteliste=[[e.getname(plang=lang)
                                        , e.dbobject().getdescr(plang=lang)
                                        , href(ref=e.webdomain.webanker().anker()
                                            , anz="{} ({})".format(e.webdomain.getname(plang=lang),e.webdomain.dbobject().displdatatype()))
                                        , bool2icon(e.dbobject().dgrm_is_mandatory)
                                     , e.dbobject().dgrm_uc + ' , ' + e.dbobject().dgrm_dc] for e in elems]))

# printdomamembers

def printwertelist(pdoma):
    vlist = DefaultValue.select(pwhere="deva_doma_id= {}".format(pdoma.doma_id))
    if (len(vlist) == 0):
        return
    vlist = [(w.deva_sort_order,w.deva_value,w.deva_displ,w.deva_descr) for w in vlist]
    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Werteliste')
                          , pueberschriften=(
                            Sprachtext.transl('Nr'), Sprachtext.transl('Wert')
                            , Sprachtext.transl('Anzeige'), Sprachtext.transl('Beschreibung')
                            )
                          , pheadlevel=3
                          , pwerteliste=vlist)
                        )
# printwertelist

def printcontentdoma():
    domas = Domain.select(pwhere="doma_origin = 'DOM'", porderby='doma_name')
    webdomas = [WebDomain(pdbobj=doma) for doma in domas]
    printcontentstart('domains')
    lang = Sprachtext.reportLang()
    for webdoma in webdomas:
        doma = webdoma.dbobject()

        lbc = str(newbarcounter())
        printcontent(ptype=Sprachtext.transl('Wertebereich')
                     , panker=webdoma.webanker().anker()
                     , pname=webdoma.getname(plang=lang)
                     , pdescr=lf2htmlbr(nvl(doma.doma_descr))
                     , plbc=lbc)

        if (doma.doma_type in (Domain.TXT, Domain.LOV)):
            infoheaders = (
                Sprachtext.transl('Datentyp'), Sprachtext.transl('Max. Länge'), Sprachtext.transl('Syntaxregel'),
                Sprachtext.transl('geändert'))
            infovalues = (
                nvl(doma.displdatatype()), nvl(doma.doma_txt_maxlng), nvl(doma.doma_txt_syntaxrule),
                nvl(doma.doma_uc) + ',' + nvl(doma.doma_dc))
        elif (doma.doma_type == Domain.BIN):
            infoheaders = (Sprachtext.transl('Datentyp'), Sprachtext.transl('Inhaltstyp'), Sprachtext.transl('Format'),
                           Sprachtext.transl('geändert'))
            infovalues = (
                nvl(doma.displdatatype()), Domain.displcontenttype(nvl(doma.doma_bin_contenttype)),
                nvl(doma.doma_bin_stfo_id), nvl(doma.doma_uc) + ',' + nvl(doma.doma_dc))
        elif (doma.doma_type == Domain.GRP):
            infoheaders = (Sprachtext.transl('Datentyp'), Sprachtext.transl('geändert'))
            infovalues = (doma.displdatatype(), nvl(doma.doma_uc) + ',' + nvl(doma.doma_dc))
        elif (doma.doma_type == Domain.NUM):
            infoheaders = (
                Sprachtext.transl('Datentyp'), Sprachtext.transl('Vorkommast.'), Sprachtext.transl('Nachkommast.')
                , Sprachtext.transl('Rundungseinh.'), Sprachtext.transl('Einheit'), Sprachtext.transl('Min. Wert'),
                Sprachtext.transl('Max. Wwert')
                , Sprachtext.transl('geändert'))
            infovalues = (
                nvl(doma.displdatatype()), nvl(doma.doma_num_total_digits), nvl(doma.doma_num_fract_digits),
                nvl(doma.doma_num_round_value), nvl(doma.doma_num_phyu_id)
                , nvl(doma.doma_num_minvalue), nvl(doma.doma_num_maxvalue)
                , nvl(doma.doma_uc) + ',' + nvl(doma.doma_dc))
        elif (doma.doma_type == Domain.DAT):
            infoheaders = (
                Sprachtext.transl('Datentyp'), Sprachtext.transl('Min. Wert'), Sprachtext.transl('Max. Wwert'),
                Sprachtext.transl('Granularität')
                , Sprachtext.transl('geändert'))
            infovalues = (doma.displdatatype(), nvl(doma.doma_dat_minvalue), nvl(doma.doma_dat_maxvalue),
                          Domain.displgranul(nvl(doma.doma_dat_granularity)), nvl(doma.doma_uc) + ',' + nvl(doma.doma_dc))
        else:
            infoheaders, infovalues = None, None
        # fi
        if infoheaders is not None: printcontentinfo(ptitle=Sprachtext.transl('Informationen'), pheaders=infoheaders,
                                                     pvalues=infovalues)

        if (doma.doma_type == 'LOV'):
            printwertelist(pdoma=webdoma)

        if (doma.doma_type == 'GRP'):
            printdomamembers(pdoma=webdoma)

        printdomaattrlist(pdomaid=doma.doma_id, pisgroup=False)
        printdomaattrlist(pdomaid=doma.doma_id, pisgroup=True)
        printdomacollist(pdomaid=doma.doma_id)

        printcontentend(lbc)  # for

# printcontentdoma

def printcontentdoku(plist):
    """
    #            select child.docu_ID,child.docu_NAME,child.docu_FORMAT,child.docu_REFERENZ
    #             ,parent.docu_ID parent_id ,parent.docu_name parent_name
    #             ,(select group_concat(grandchild.docu_id||':'||grandchild.docu_name, '|') kinder
    #                from DOKUMENTE grandchild
    #                where grandchild.docu_docu_ID = child.docu_ID) kinder
    #            from DOKUMENTE child
    #            left join dokumente parent on parent.docu_ID = child.docu_docu_ID
    #            order by upper(child.docu_name)
    #            """
    printcontentstart('documents')
    infoheaders = (Sprachtext.transl('Format'), Sprachtext.transl('Referenz'), Sprachtext.transl('Vaterdokument')
                   , Sprachtext.transl('Unterdokumente'))
    for webdoc in plist:
        doc = webdoc.dbobject()
        lbc = str(newbarcounter())
        docu_id = doc.docu_id
        parent = doc.getparent()
        webparent = nvl2(parent,None, WebDocument(pdbobj=parent))
        children = doc.getchildren()
        printcontent(ptype=Sprachtext.transl('Dokument')
                     , panker=webdoc.webanker().anker()
                     , pname=doc.docu_name
                     , pdescr=""
                     , plbc=lbc)

        """docu_ID,docu_NAME,docu_FORMAT,docu_REFERENZ
            ,parent_id, parent_name, kinder"""
        #        kinder = ''
        #        if children is not None:
        #            for child in children:
        #                kinder += href(pref=child.webanker.anker(),panz=child.docu_name) + ', '
        #            #for
        #            kinder = kinder.rstrip(', ')
        #        #fi
        webchildren = nvl2(children,[] , [WebDocument(pdbobj=child) for child in children])
        if children is None:
            kinder = ''
        else:
            kinder = ', '.join(href(ref=webchild.webanker().anker(), anz=webchild.getname(plang=Sprachtext.reportLang())) for webchild in webchildren)
        # fi

        infovalues = (nvl(doc.getformat()), nvl(doc.docu_reference),
                      nvl2(webparent,'',href(ref=webparent.webanker().anker(), anz=nvl(webparent.getname(plang=Sprachtext.reportLang()))))
                      , kinder)
        printcontentinfo(ptitle=Sprachtext.transl('Informationen'), pheaders=infoheaders, pvalues=infovalues)
        printreflist(pelemid=docu_id, pelemtype=Modelelemtype.DOCU)
        printcontentend(lbc)
    # for
# printcontentdoku


def searchlogo(p_imagedirec):
    retval = ''
    for ext in ('png', 'jpg', 'svg'):
        if os.path.isfile(p_imagedirec + 'logo.' + ext): retval = 'logo.' + ext
    return retval


# searchlogo

def setWebDirec(p_webdirec):
    global webDirectory, webFileName, webFileNamePath
    global libSourceDirec, imagedirec, cssdirec, icondirec

    webDirectory = nvl(p_webdirec, parameters.webDirec());
    webFileName = parameters.odmModelName();
    imagedirec = webDirectory + 'image/';
    cssdirec = webDirectory + "css/";
    icondirec = webDirectory + "icons/";
    libSourceDirec = os.path.dirname(os.path.abspath(__file__))
    libSourceDirec += '/../html-lib/';
    if (parameters.logoFileName() is None): parameters.logoFileName(searchlogo(imagedirec));


def createlib():
    if os.path.exists(cssdirec):
        pass
        # shutil.rmtree(cssdirec)
    else:
        shutil.copytree(libSourceDirec + 'css', cssdirec)

    if os.path.exists(icondirec):
        pass
        # shutil.rmtree(icondirec)
    else:
        shutil.copytree(libSourceDirec + 'icons', icondirec)
    if os.path.exists(imagedirec):
        pass
        # shutil.rmtree(imagedirec)
    else:
        shutil.copytree(libSourceDirec + 'image', imagedirec)


# createlib

def createFile(pfilename):
    global fhtml
    webfile = webDirectory + pfilename
    if os.path.exists(webfile):
        os.remove(webfile)
    fhtml = open(webfile, 'w')


# createFile
def closefile():
    global fhtml
    fhtml.close()


# closefile

def attname2element(pattrname):
    if pattrname in ['ENTI_NAME', 'ATTR_NAME']:
        return Sprachtext.transl('Name')
    elif pattrname in ['ENTI_COMMENT', 'ATTR_COMMENT']:
        return Sprachtext.transl('Beschreibung')
    elif pattrname in ['SYNO_NAME']:
        return Sprachtext.transl('Synonym')
    else:
        return pattrname
    # fi


def findtransl(pattrname, pmodeid, plangs, panker = None):
    tl = [attname2element(pattrname)]
    for l in plangs:
        name = Sprachtext.transltext(pattrname=pattrname, pmodeid=pmodeid, plang=l)
        if panker is None:
            eintrag = name
        else:
            eintrag = filehref(panz=name, pref=panker, plang=l)
        tl.extend([eintrag])
    return tl


def printtransl(pwebenti=None, pwebattr=None):
    langs = projekt.projektlangs().split(',')
    try:
        langs.remove(Sprachtext.reportLang())
    except:
        pass
    if len(langs) == 0: return
    head = [Sprachtext.transl('Element')]
    head.extend(langs)
    if (pwebenti is not None):
        transllist = [findtransl(pattrname='ENTI_NAME', pmodeid=pwebenti.enti_id, plangs=langs, panker=pwebenti.webanker().anker())
            , findtransl(pattrname='ENTI_SYNONYM', pmodeid=pwebenti.enti_id, plangs=langs)
            , findtransl(pattrname='ENTI_COMMENT', pmodeid=pwebenti.enti_id, plangs=langs)]
    elif (pwebattr is not None):
        transllist = [findtransl(pattrname='ATTR_NAME', pmodeid=pwebattr.attr_id, plangs=langs, panker=pwebattr.webanker().anker())
            , findtransl(pattrname='ATTR_COMMENT', pmodeid=pwebattr.attr_id, plangs=langs)]
    # print(transllist)
    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Übersetzungen')
                          , pueberschriften=head
                          , pheadlevel=2
                          , pwerteliste=transllist))
# printtransl
