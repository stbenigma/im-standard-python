import os
import re
import shutil
from distutils.dir_util import copy_tree

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
jsdirec: str = "";
htmlfilelist = {}
model = {}

"""zum Zählen der lokalen Ziele für collapse"""
barcounter: int = 0


getentity = lambda e:model['entities'][e]
getattribute = lambda a:model['attributes'][a]
getrelation = lambda r:model['relations'][r]

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


def filehref(pref, panz, plang, pself=False,pimg=None):
    img = nvl2(pimg,'','<img class="icon-check" src="icons/{}">'.format(pimg))
    return """<a href="{}{}" target="_{}" >{}{}</a>""" \
        .format(webFileName + '_' + plang.lower() + '.html', nvl2(pref,"","#") , 'self' if pself else 'blank',panz, img)


def href(ref, anz, htmlfile='',pself=False):
    if anz is None: return ''
    sep = '#' if nvl(ref) !='' else ''
    return """<a href="{}{}{}" target="{}">{}</a>""".format(htmlfile
                                                          , sep, ref
                                                          , '_self' if ((htmlfile == '') or pself) else  '_blank'
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


def printlistofcontentelement(pname, plist, pfileonly=False):
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
    #local = re.match(r'/(.+/)*{}'.format(htmlfilelist[pintfid]), fhtml.name)
    for entry in plist:
        if pfileonly:
            anker = htmlfilelist[entry['anker']]
        else:
            anker = '#' + entry['anker']
        fhtml.write(listcontentline.format(anker, '_blank' if pfileonly else '_self', entry['name']))
    #for
    fhtml.write(listcontentelementfoot)
#printlistofcontentelement


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
        str += filehref(pref=None, panz=l + '   ', pself=True,plang=l, pimg=lang2img(l.lower()))
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

def printcontent(ptype, pname, panker, plbc, pdescr="", pmaster="", piconfilename=""):
    contentelementhead = """        <div class="entity" id="{}">
            <div class="describtion">
				 <span> 
					 <script>entityheader('{}','{}','{}','{}','{}');</script>
			     </span>
            </div>
             <div class="panel-body">
            <div class="collapse" id="bar{}">                    
"""
# """                <p>{}</p>
#                 <h1>{}{}</h1>
#                 {}
#                 {}
# """
    fhtml.write(contentelementhead.format(panker, ptype, html.escape(pname )
                                          , piconfilename
                                          , pmaster
                                          , pdescr.replace('\n', '').replace('\r', '').replace("'",'&#39;')  #"" if (pdescr == "") else "<p1>{}</p1>".format(pdescr)
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


def printattrlist(penti):
    global model
    lang = Sprachtext.reportLang()
    alist = [{'anker':a,'element':model['attributes'][a]} for a in penti['attributes']]
    if (len(alist) == 0):
        return
    fhtml.write(starttable(ptitel=Sprachtext.transl('Attribute')
                           , pueberschriften=(
            Sprachtext.transl('Name'), Sprachtext.transl('Wertebereich'), Sprachtext.transl('Typ')
            , Sprachtext.transl('Pflichtattribut'), Sprachtext.transl('Schlüssel'), Sprachtext.transl('Deskriptor'),
            Sprachtext.transl('übersetzt')
            , Sprachtext.transl('historisiert'), Sprachtext.transl('wiederholt'), Sprachtext.transl('verschlüsselt'))))

    for attr in alist:
        elem = attr['element']
        domanker = elem['domain']
        if nvl(domanker) == '':
            domelem = None
        else:
            domelem= model['domains'][domanker]

        domname = html.escape(domelem['name'][lang])
        domref = domname if domelem['origin']==Domain.DERIVED \
                        else href(ref=domanker, anz=domname)
        fhtml.write(writetableline(pwerte=(href(ref=attr['anker'], anz=elem['name'][lang])
                                           , domref
                                           , html.escape(nvl(domelem['datatypestr']))
                                           , bool2icon(elem['mandatory']), bool2icon(len(elem['keys']) > 0),
                                           bool2icon(elem['descriptive'])
                                           , bool2icon(elem['translated']), bool2icon(elem['historicised'])
                                           , bool2icon(elem['repeated']), bool2icon(elem['encrypted']))))
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


def printkeys(pelem,plang):
    keylist = [{'anker':k,'element':model['keys'][k]} for k in pelem['keys']]
    if (len(keylist) == 0):
        return
    keyprint = []
    for k in keylist:
        attrs = ', '.join(href(ref=a,anz=model['attributes'][a]['name'][plang]) for a in k['element']['key-elements']['attributes'])
        relas = ', '.join(model['relations'][r]['name'] for r in k['element']['key-elements']['relations'])
        key = (k['anker'],attrs,relas)
        keyprint.append(key)
    #for
    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Schlüssel')
                          , pueberschriften=(
                Sprachtext.transl('Name'), Sprachtext.transl('Attribute(e)'),
                Sprachtext.transl('Beziehung(en)'))
                        , pwerteliste=keyprint
                  )
                )
# printkeys

def printmappinghtml(pwerte, ptitel, pueberschriften, pheadlevel=2):
    # pwerte, list of entries mit {intf:[(tabanker,tabname)]}
    if (pwerte is None or len(pwerte) == 0):
        return
    werte = []
    for intf,tabs in pwerte.items():
        commalist = ', '.join([href(ref=tab[0] , anz=tab[1], htmlfile=htmlfilelist[intf]) for tab in tabs])
        name = model['systems'][intf]['name'] if intf != 0 else 'Information Model'
        werte.append([name, commalist])
    fhtml.write(tablehtml(ptitel=ptitel
                          , pueberschriften=pueberschriften
                          , pheadlevel=pheadlevel
                          , pwerteliste=werte
                          )
                )
# printmappinghtml

def printmapping(penti=None, pattr=None):
    if penti is not None:
        werte = {intf:[(tid, model['tables'][tid]['name']) for tid in tables] for intf,tables in penti['tablesmapped'].items()}
        titel = Sprachtext.transl('Relational Mapping (Tabellen)')
        ueberschr = (Sprachtext.transl('Relational Model'), Sprachtext.transl('Tabellen'))
    elif pattr is not None:
        werte = {intf:[(cid, model['columns'][cid]['name']) for cid in columns] for intf,columns in pattr['columnsmapped'].items()}
        titel = Sprachtext.transl('Relational Mapping (Columns)')
        ueberschr = (Sprachtext.transl('Relational Model'), Sprachtext.transl('Columns'))
    else:
        return
    # fi
    printmappinghtml(pwerte=werte, ptitel=titel, pueberschriften=ueberschr)
#printmapping



def printentirela(penti,plang):
    relalist = [{'anker': r, 'element': model['relations'][r]} for r in penti['element']['relations']]
    if (len(relalist) == 0):
        return
    fhtml.write(starttable(ptitel=Sprachtext.transl('Beziehungen')
                           , pueberschriften=(
            Sprachtext.transl('Name'), Sprachtext.transl('Entität') + '-1', '', Sprachtext.transl('Beziehung'), '',
            Sprachtext.transl('Entität') + '-2'
            , Sprachtext.transl('Arc'), Sprachtext.transl('Schlüssel'),)))
    for rela in relalist:
        elem = rela['element']
        if elem['type'] in (Relation.ISAROLE,Relation.ISASUBTYPE): continue
        fromarc = '' if (elem['from-to']['arc'] is None) else model['arcs'][elem['from-to']['arc']]['name']
        toarc = '' if (elem['to-from']['arc'] is None) else model['arcs'][elem['to-from']['arc']]['name']
        if (penti['anker'] == elem['from-to']['enti']):
            otherentiname = model['entities'][elem['to-from']['enti']]['name'][plang]

            # 'Name','Entität1','','Beziehung','', 'Entität2','Arc','Key'
            fhtml.write(writetableline(pwerte=(html.escape(nvl(elem['name'])), html.escape(penti['element']['name'][plang])
                                                        , '->', html.escape(nvl(elem['from-to']['assoc'][plang], '--'))
                                               , elem['from-to']['cardstr']
                                               , arrow2icon('down'), fromarc, bool2icon(len(elem['isinkeys']) > 0))))
            fhtml.write(writetableline(pwerte=('', arrow2icon('up'), elem['to-from']['cardstr'], html.escape(nvl(elem['to-from']['assoc'][plang], '--')), '<-'
                                               , href(ref=elem['to-from']['enti'], anz=html.escape(otherentiname)))))
        else:
            otherentiname = model['entities'][elem['from-to']['enti']]['name'][plang]
            fhtml.write(writetableline(pwerte=(html.escape(nvl(elem['name'])), html.escape(penti['element']['name'][plang])
                                               , '->', html.escape(nvl(elem['to-from']['assoc'][plang], '--'))
                                               , elem['to-from']['cardstr']
                                               , arrow2icon('down'), toarc, bool2icon(len(elem['isinkeys']) > 0))))
            fhtml.write(writetableline(pwerte=('', arrow2icon('up'), elem['from-to']['cardstr'], html.escape(nvl(elem['from-to']['assoc'][plang], '--')), '<-'
                                               , href(ref=elem['from-to']['enti'], anz=html.escape(otherentiname)))))
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


def printUDP(pelem):
    startwritten = False

    for udptheme,udpval in pelem['userdefprop'].items():
        """theme,group"""

        """translations are not printed"""
        if (udptheme == parameters.odmUDPTranslFileName()): continue

        for grp,props in udpval.items():
            displvalues = {html.escape(name): html.escape(nvl(value)) for name,value in props.items()}

            """write only if there is at least one value not empty"""
            if (len(displvalues) > list(displvalues.values()).count('')):
                if (not startwritten):
                    fhtml.write(startabschnitt(p_titel=Sprachtext.transl('Benutzerdefinerte Eigenschaften')))
                    startwritten = True
                # fi

                fhtml.write(tablehtml(ptitel=html.escape(' {} - {} '.format(udptheme,grp))
                                  , pueberschriften=list(displvalues.keys())
                                  , pheadlevel=3
                                  , pwerteliste=[list(displvalues.values())])
                        )
            #fi
        #for
    #for
    if (startwritten):
        fhtml.write(endabschnitt())
# printUDP

def entidiag(pwebenti):
    doppelanker = "{}-{}"
    diaglist = WebDiagram.contentlist(pentiid=pwebenti.enti_id)
    if (len(diaglist) == 0):
        return ''
    diagstring = ', '.join(href(ref=doppelanker.format(diag.webanker().anker(), pwebenti.webanker().anker())
                                , anz=diag.getname()) for diag in diaglist)
    return diagstring
# entidiag

def iconfilename(pfilename):
    lfilename = re.sub(r'[^a-zäöüñéàè_-]+', '', pfilename.lower())
    fullfilename = "{}/{}.{}".format('image',lfilename,'png').lower()
    if os.path.isfile(parameters.webDirec()+ fullfilename):
        retval =  lfilename
    else:
        retval = ''
    return retval

def printcontententi():
    global model
    lang = Sprachtext.reportLang()
    deflang = Sprache.getdefaultlang().lang_iso_code2
    printcontentstart('entities')
    infoheaders = (Sprachtext.transl('Synonyme'), Sprachtext.transl('Superentitäten')
                   , Sprachtext.transl('Subentitäten'), Sprachtext.transl('Rollen'), Sprachtext.transl('auf Diagramm(en)')
                   , Sprachtext.transl('geändert'))

    for enti in sorted([{'anker':key,'element': value}
                     for key,value in model['entities'].items()]
                     ,key=lambda val:val['element']['name'][lang]):
        elem = enti['element']
        lbc = str(newbarcounter())
        printcontent(ptype=Sprachtext.transl('Entität')
                     , panker=enti['anker']
                     , pname=elem['name'][lang]
                     , piconfilename=iconfilename(pfilename=elem['name'][deflang])
                     , pdescr=lf2htmlbr(nvl(elem['descr'][lang]))
                     , plbc=lbc)
        """print entity Info"""
        synostr =  ', '.join(s[lang] for s in elem['synonyms'])
        parentstr = ", ".join(href(ref=p, anz=getentity(p)['name'][lang]) for p in elem['supertypes'])
        subtypestr = ', '.join(href(ref=st, anz=getentity(st)['name'][lang]) for st in elem['subtypes'])
        rolesstr = ', '.join(href(ref=r, anz=getentity(r)['name'][lang]) for r in elem['roles'])
        diagstr = ', '.join(href(ref="{}-{}".format(d, enti['anker'])
                                    , anz=model['diagrams'][d]['name']) for d in elem['diagrams'])
        infovalues = (nvl(synostr), parentstr, subtypestr,rolesstr
                      , diagstr, nvl(elem['uc']) + ', ' + nvl(elem['dc']))
        printcontentinfo(ptitle=Sprachtext.transl('Informationen'), pheaders=infoheaders, pvalues=infovalues)
        printattrlist(penti=elem)
        printkeys(pelem=elem,plang=lang)
        printentirela(penti=enti,plang=lang)
        printdocureflist(pelem=elem, pelemtype=Modelelemtype.ENTI)
        printtransl(penti=enti)
        printUDP(pelem=elem)
        printmapping(penti=elem)
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

    for attr in sorted([{'anker':key,'element': value}
                     for key,value in model['attributes'].items()]
                     ,key=lambda val:val['element']['name'][lang]):
        elem = attr['element']
        printcontentstart('attributes')
        if elem['entity'] is None:
            master = 'Relation tbd'
        else:
            enti = model['entities'][elem['entity']]
            master = "<p1>{}: {}</p1><br>" \
                .format(Sprachtext.transl('Entität'), href(ref=elem['entity'], anz=enti['name'][lang]))
        #fi

        lbc = str(newbarcounter())
        printcontent(ptype=Sprachtext.transl('Attribute')
                     , panker=attr['anker']
                     , pname=elem['name'][lang]
                     , pmaster=master
                     , pdescr=lf2htmlbr(nvl(elem['descr'][lang]))
                     , plbc=lbc)
        domain = model['domains'][elem['domain']]
        domainname=domain['name'][lang]
        domainref =  domainname if  domain['origin'] == Domain.DERIVED\
                     else href(ref=elem['domain'], anz=domainname)
        infovalues = (nvl(elem['techname'], ''), domainref, domain['displdatatype'][lang]
                      , nvl(elem['tooltip'][lang]), re.sub(r'^, $', '', nvl(elem['uc']) + ', ' + nvl(elem['dc'])))
        printcontentinfo(ptitle=Sprachtext.transl('Informationen'), pheaders=infoheaders, pvalues=infovalues)

        flagvalues = (bool2icon(elem['mandatory']), bool2icon(len(elem['keys'])>0), bool2icon(elem['descriptive'])
                      , bool2icon(elem['translated'])
                      , bool2icon(elem['historicised']), bool2icon(elem['repeated']),
                      bool2icon(elem['encrypted']))
        printflagline(pheaders=flagheaders, pvalues=flagvalues)
        printkeys(pelem=elem,plang=lang)
        printdocureflist(pelem=elem, pelemtype=Modelelemtype.ATTR)
        printtransl(pattr=attr)
        printUDP(pelem=elem)
        printmapping(pattr=elem)
        printcontentend(lbc)
    # for
# printcontentattr

def printdocureflist(pelem, pelemtype):
    refentries = [[d,model['documents'][d]] for d in pelem['refindocuments']]
    if (len(refentries) == 0): return
    fhtml.write(starttable(ptitel=Sprachtext.transl('Referenziert in')
                           , pueberschriften=[Sprachtext.transl('Dokument')]))

    for refentry in refentries:
        # aus schn-html zurück ins Main
        htmlname = htmlfilelist[0] if (pelemtype in (Modelelemtype.TABL, Modelelemtype.INTF, Modelelemtype.COLU))\
                                    else ''
        docuentry = href(ref=refentry[0],anz=refentry[1]['name'],htmlfile=htmlname)
        fhtml.write(writetableline(pwerte=[docuentry]))
    # for
    fhtml.write(endtable())


def printdomaattrlist(pdoma, plang,pisgroup=False):
    if pisgroup:
        """all domains of type group containing parameter domain in elements of its group"""
        alist = [[href(ref=domaanker
                       ,anz=model['domains'][domaanker]['name'][plang])]
                 for domaanker in pdoma['element']['usedingrps']
                ]
    else:
        alist = [[href(ref=attranker
                       ,anz="{} ({})".format(getattribute(attranker)['name'][plang]
                                            ,'' if getattribute(attranker)['entity'] is     None\
                                               else getentity(getattribute(attranker)['entity'])['name'][plang]
                                             ))]
                for attranker in pdoma['element']['usedinattrs']
                ]
    if (pisgroup and len(alist)==0):return

    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Verwendet in Attributgruppen' if pisgroup
                                                   else 'Verwendet für Attribute')
                          , pueberschriften=['']#[Sprachtext.transl('Attributgruppe' if pisgroup
                                                #               else 'Attribute')]
                          , pwerteliste=alist))
#printdomaattrlist

def printdomacollist(pdoma):
    clist = [[href(ref=colanker
                       ,anz=model['columns'][colanker]['name']
                   ,htmlfile=htmlfilelist[model['columns'][colanker]['interface-id']])
              ,href(ref=model['columns'][colanker]['table-id']
                   , anz=model['columns'][colanker]['table-name']
                   , htmlfile=htmlfilelist[model['columns'][colanker]['interface-id']])
              ,href(ref=''
                   , anz=model['columns'][colanker]['interface-name']
                   , htmlfile=htmlfilelist[model['columns'][colanker]['interface-id']])

              ]
                for colanker in pdoma['element']['usedincols']
                ]

    if (len(clist) == 0): return
    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Verwendet für Columns')
                          , pueberschriften=[Sprachtext.transl('Column'),Sprachtext.transl('Tabelle'),Sprachtext.transl('System')]
                          , pwerteliste=clist))
#printdomacollist

def printdomamembers(pelem):
    elems = pelem['elements']
    if (len(elems) == 0):
        return
    lang =Sprachtext.reportLang()
    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Elemente')
                          , pueberschriften=
                          [Sprachtext.transl('Element')
                              , Sprachtext.transl('Beschreibung')
                              , Sprachtext.transl('Wertebereich')
                              , Sprachtext.transl('Pflichtattribut')
                           ]
                          , pwerteliste=[[e['name']
                                         , e['descr']
                                        , href(ref=e['domain']
                                            , anz="{} ({})".format(model['domains'][e['domain']]['name'][lang]
                                                                ,model['domains'][e['domain']]['displdatatype'][lang]))
                                        , bool2icon(e['mandatory'])
                                       ] for e in elems]))

# printdomamembers

def printwertelist(pelem):
    vlist = sorted([(val['sort'],val['value'],val['displ'],val['descr'])
                        for val in pelem['values']]
            , key=lambda val: val[0])
    if (len(vlist) == 0):
        return
    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Werteliste')
                          , pueberschriften=(
                            Sprachtext.transl('Nr'), Sprachtext.transl('Wert')
                            , Sprachtext.transl('Anzeige'), Sprachtext.transl('Beschreibung')
                            )
                          , pheadlevel=3
                          , pwerteliste=vlist)
                        )
# printwertelist

def origindomains():
    #dict of domain with origin DOMAIN
    return {key: value for key, value in model['domains'].items() if value['origin'] == Domain.DOMAIN}

def printcontentdoma():

    lang = Sprachtext.reportLang()
    for doma in sorted([{'anker': key, 'element': value}
                        for key, value in origindomains().items()]
            , key=lambda val: val['element']['name'][lang]):
        elem = doma['element']
        printcontentstart('domains')
        lbc = str(newbarcounter())
        printcontent(ptype=Sprachtext.transl('Wertebereich')
                     , panker=doma['anker']
                     , pname=elem['name'][lang]
                     , pdescr=lf2htmlbr(nvl(elem['descr'][lang]))
                     , plbc=lbc)

        if (elem['type'] in (Domain.TXT, Domain.LOV)):
            infoheaders = (
                Sprachtext.transl('Datentyp'), Sprachtext.transl('Max. Länge'), Sprachtext.transl('Syntaxregel'),
                Sprachtext.transl('geändert'))
            infovalues = (
                nvl(elem['displdatatype'][lang]), nvl(elem['maxlng']), nvl(elem['syntaxrule'] if elem['type'] == Domain.TXT else ''),
                nvl(elem['uc']) + ',' + nvl(elem['dc']))
        elif (elem['type'] == Domain.BIN):
            infoheaders = (Sprachtext.transl('Datentyp'), Sprachtext.transl('Inhaltstyp'), Sprachtext.transl('Format'),
                           Sprachtext.transl('geändert'))
            infovalues = (
            nvl(elem['displdatatype'][lang]), nvl(elem['contenttype']),
                nvl(elem['contenttypename']), nvl(elem['uc']) + ',' + nvl(elem['dc']))
        elif (elem['type'] == Domain.GRP):
            infoheaders = (Sprachtext.transl('Datentyp'), Sprachtext.transl('geändert'))
            infovalues = (elem['displdatatype'][lang], nvl(elem['uc']) + ',' + nvl(elem['dc']))
        elif (elem['type'] == Domain.NUM):
            infoheaders = (
                Sprachtext.transl('Datentyp'), Sprachtext.transl('Vorkommast.'), Sprachtext.transl('Nachkommast.')
                , Sprachtext.transl('Rundungseinh.'), Sprachtext.transl('Einheit'), Sprachtext.transl('Min. Wert'),
                Sprachtext.transl('Max. Wwert')
                , Sprachtext.transl('geändert'))
            infovalues = (
                nvl(elem['displdatatype'][lang]), nvl(elem['totaldigits']), nvl(elem['fractdigits']),
                nvl(elem['roundvalue']), nvl(elem['unit'])
                , nvl(elem['minvalue']), nvl(elem['maxvalue'])
                , nvl(elem['uc']) + ',' + nvl(elem['dc']))
        elif (elem['type'] == Domain.DAT):
            infoheaders = (
                Sprachtext.transl('Datentyp'), Sprachtext.transl('Min. Wert'), Sprachtext.transl('Max. Wwert'),
                Sprachtext.transl('Granularität')
                , Sprachtext.transl('geändert'))
            infovalues = (elem['displdatatype'][lang], nvl(elem['minvalue']), nvl(elem['maxvalue']),
                          nvl(elem['granularitytext'][lang]), nvl(elem['uc']) + ',' + nvl(elem['dc']))
        else:
            infoheaders, infovalues = None, None
        # fi
        if infoheaders is not None: printcontentinfo(ptitle=Sprachtext.transl('Informationen'), pheaders=infoheaders,
                                                     pvalues=infovalues)

        if (elem['type'] == Domain.LOV):
            printwertelist(pelem=elem)

        if (elem['type'] == Domain.GRP):
            printdomamembers(pelem=elem)
        printdomaattrlist(pdoma=doma, plang=lang,pisgroup=False)
        printdomaattrlist(pdoma=doma, plang=lang,pisgroup=True)
        printdomacollist(pdoma=doma)

        printcontentend(lbc)  # for
# printcontentdoma

def type2name(ptyp,plang):
    if ptyp == 'entities':
        return Sprachtext.transl('Entitäten',plang)
    elif ptyp == 'attributes':
        return Sprachtext.transl('Attribute', plang)
    elif ptyp == 'attributes':
        return Sprachtext.transl('Attribute', plang)
    elif ptyp == 'domains':
        return Sprachtext.transl('Wertebereiche', plang)
    elif ptyp == 'diagrams':
        return Sprachtext.transl('Diagramme', plang)
    elif ptyp == 'tables':
        return Sprachtext.transl('Tabellen', plang)
    elif ptyp == 'systems':
        return Sprachtext.transl('Systeme', plang)
    elif ptyp == 'columns':
        return 'Columns'
    else:
        return ptyp
    #fi
#type2name

def printreflist(pelem,plang):
    refentries = {typ: [{'anker': e
                        , 'name': model[typ][e]['name']
                        ,'interface-id': model[typ][e]['interface-id'] if (typ in ('tables','columns','systems')) else 0
                         } for e in ref] for typ,ref in pelem['references'].items()}
    if (len(refentries) == 0): return
    fhtml.write(starttable(ptitel=Sprachtext.transl('Referenziert')
                           , pueberschriften=[Sprachtext.transl('Typ'),Sprachtext.transl('Element')]))

    for typ,ref in refentries.items():
        if len(ref)==0: continue
        # aus schn-html zurück ins Main
        docuentry = ', '.join (href(ref='' if (typ in ('systems')) else elem['anker']
                                    ,anz=elem['name'] if (typ in ('tables','columns','systems'))\
                                                else elem['name'][plang]
                                    ,htmlfile=htmlfilelist[elem['interface-id']]
                                    ) for elem in ref)
        fhtml.write(writetableline(pwerte=[type2name(ptyp=typ,plang=plang),docuentry]))
    # for
    fhtml.write(endtable())
#printreflist

def printcontentdoku():
    docus = sorted([{'anker': key, 'element': value}
            for key, value in model['documents'].items()]
            ,key=lambda val : val['element']['name'])
    printcontentstart('documents')
    infoheaders = (Sprachtext.transl('Format'), Sprachtext.transl('Referenz'), Sprachtext.transl('Vaterdokument')
                   , Sprachtext.transl('Unterdokumente'))
    for doc in docus:
        elem = doc['element']
        lbc = str(newbarcounter())
        parentanker=elem['parent']
        parentname = None if parentanker is None else model['documents'][parentanker]['name']
        printcontent(ptype=Sprachtext.transl('Dokument')
                     , panker=doc['anker']
                     , pname=elem['name']
                     , pdescr=""
                     , plbc=lbc)

        children = [href(ref=key,anz=val['name']) for key,val in model['documents'].items() if val['parent'] == doc['anker']]
        kinder = ', '.join(c for c in children)

        infovalues = (nvl(elem['format']), nvl(elem['reference']),
                      nvl2(parentanker,'',href(ref=parentanker,anz=parentname)), kinder)
        printcontentinfo(ptitle=Sprachtext.transl('Informationen'), pheaders=infoheaders, pvalues=infovalues)
        printreflist(pelem=elem,plang=Sprachtext.reportLang())
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
    global libSourceDirec, imagedirec, cssdirec, icondirec,jsdirec

    webDirectory = nvl(p_webdirec, parameters.webDirec());
    webFileName = parameters.odmModelName();
    imagedirec = webDirectory + 'image/';
    cssdirec = webDirectory + "css/";
    icondirec = webDirectory + "icons/";
    jsdirec = webDirectory + "js/";
    libSourceDirec = os.path.dirname(os.path.abspath(__file__))
    libSourceDirec += '/../html-lib/';
    if (parameters.logoFileName() is None): parameters.logoFileName(searchlogo(imagedirec));


def createlib():
    global cssdirec,icondirec,imagedirec,jsdirec
    if not os.path.exists(cssdirec):
        shutil.copytree(libSourceDirec + 'css', cssdirec)
    if not os.path.exists(jsdirec):
        shutil.copytree(libSourceDirec + 'js', jsdirec)
    if not os.path.exists(icondirec):
        shutil.copytree(libSourceDirec + 'icons', icondirec)
    if not os.path.exists(imagedirec):
        shutil.copytree(libSourceDirec + 'image', imagedirec)
# createlib

def copyimages():
    global imagedirec
    """copy all file from the modeler-image directory into the web-image directory"""
    copy_tree(parameters.odmFilesDirec()+'images', imagedirec)
# copyimages

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


def printtransl(penti=None, pattr=None):
    global webFileName
    langfilename = "{}_{}.html".format(webFileName,'{}')
    langs = [k for k in model['languages'].keys()]
    try:
        langs.remove(Sprachtext.reportLang())
    except:
        pass
    if len(langs) == 0: return
    head = [Sprachtext.transl('Element')]
    head.extend(langs)
    name = [Sprachtext.transl('Name')]
    descr = [Sprachtext.transl('Beschreibung')]
    synonym = [Sprachtext.transl('Synonym')]
    if (penti is not None):
        name +=[href(ref=penti['anker'], anz=penti['element']['name'][lang]
                     ,htmlfile=langfilename.format(lang),pself=True) for lang in langs]
        synonym += [','.join(s[lang] for s in penti['element']['synonyms']) for lang in langs]
        descr += [penti['element']['descr'][lang] for lang in langs]
        transllist = [name,synonym,descr]
    elif (pattr is not None):
        name +=[href(ref=pattr['anker'], anz=pattr['element']['name'][lang]
                     ,htmlfile=langfilename.format(lang),pself=True) for lang in langs]
        descr += [pattr['element']['descr'][lang] for lang in langs]
        transllist = [name,descr]
    #fi
    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Übersetzungen')
                          , pueberschriften=head
                          , pheadlevel=2
                          , pwerteliste=transllist))
# printtransl
