import os
import re
import shutil
from distutils.dir_util import copy_tree

from IM_DB import parameters
from IM_OBJECTS import *
import html
from IM_JSON import JSModel,jsguid2type
from IM_HTML import entityenviron

outputDirectory: str = None
webDirectory: str = "";
webFileName: str = "";
webFileNamePath: str = "";
libSourceDirec: str = "";
imagedirec: str = "";
cssdirec: str = "";
icondirec: str = "";
jsdirec: str = "";
jinadirec: str = "";
htmlfilelist = {}
model:JSModel = None

def setmodel(pmodel:JSModel):
    global model
    model = pmodel
    return
def getmodel():
    global model
    return model

"""zum Zählen der lokalen Ziele für collapse"""
barcounter: int = 0


getelement = lambda e:getmodel().getbyid(e)

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
    img =  parameters.nvl2(pimg,'','<img class="icon-check" src="icons/{}">'.format(pimg))
    return """<a href="{}{}" target="_{}" >{}{}</a>""" \
        .format(webFileName + '_' + plang.lower() + '.html',  parameters.nvl2(pref,"","#") , 'self' if pself else 'blank',panz, img)


def href(ref, anz, htmlfile='',pself=False):
    if anz is None: return ''
    sep = '#' if parameters.nvl(ref) !='' else ''
    return """<a href="{}{}{}" target="{}">{}</a>""".format(htmlfile, sep, ref
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
    console.log("ID der Table: " + sID + " \\n ");
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
""".format(Languagetext.transl("Suchbegriff"), Languagetext.transl("Treffer"))
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
    fhtml.write(listcontentelementhead.format(pname, lbc, Languagetext.transl(pname), lbc, pname))
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
    if plang in (Languagetext.DE, Languagetext.FR):
        return plang + ".png"
    elif plang == Languagetext.EN:
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
    if Languagetext.reportLang() == Languagetext.DE:
        f = """class="descr">Diese Webseite enthält den ganzen Inhalt 
            des <p2 class="IM">Informationsmodells {}</p2> von {}. 
            Diese Seite wurde von Software von <p2 class="fyayc">foryouandyourcustomers</p2> 
            erstellt.""".format(ptitel, pfirma)
    elif Languagetext.reportLang() == Languagetext.FR:
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
    langs = project.projektlangs().split(',')
    try:
        langs.remove(Languagetext.reportLang().lower())
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
    fhtml.write(contentelementfoot.format(plbc, Languagetext.transl('Mehr')))
# printcontentend

def printcontent(ptype, pname, panker, plbc, pdescr="", pmaster="", piconsrc=""):
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
                                          , piconsrc
                                          , pmaster
                                          , pdescr.replace('\n', '').replace('\r', '').replace("'",'&#39;')
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
    fhtml.write(trend)
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
    lang = Languagetext.reportLang()
    alist = [{'anker':a,'element':getelement(a)} for a in penti['attributes+']]
    if (len(alist) == 0):
        return
    fhtml.write(starttable(ptitle=Languagetext.transl('Attribute')
                           , pheaders=(
            Languagetext.transl('Name'), Languagetext.transl('Wertebereich'), Languagetext.transl('Typ')
            , Languagetext.transl('Pflichtattribut'), Languagetext.transl('Schlüssel'), Languagetext.transl('Deskriptor'),
            Languagetext.transl('übersetzt')
            , Languagetext.transl('historisiert'), Languagetext.transl('wiederholt'), Languagetext.transl('verschlüsselt'))))

    for attr in alist:
        elem = attr['element']
        domanker = elem['domain']
        if parameters.nvl(domanker) == '':
            domelem = None
        else:
            domelem= getelement(domanker)

        domname = html.escape(domelem['name'][lang])
        domref = domname if domelem['origin']==Domain.DERIVED \
                        else href(ref=domanker, anz=domname)
        fhtml.write(writetableline(pwerte=(href(ref=attr['anker'], anz=elem['name'][lang])
                                           , domref
                                           , html.escape(parameters.nvl(domelem['datatypestr+']))
                                           , bool2icon(elem['mandatory']), bool2icon(len(elem['keys+']) > 0),
                                           bool2icon(elem['descriptive'])
                                           , bool2icon(elem['translated']), bool2icon(elem['historicised'])
                                           , bool2icon(elem['repeated']), bool2icon(elem['encrypted']))))
    # for
    fhtml.write(endtable())
# printattrlist

def startabschnitt(ptitle, pheadlevel=2, ptabid=None, pselfanker=None, plbc=None):
    head = """<h{}>{}</h{}>{}"""
    start = """{}        
        <div id="container1">
    """
    collapsestart = """
        <div class="panel">
            <div class="panel-heading collapsed" data-toggle="collapse"  data-target="#bar{}">
                <img class="icon-chevron-up" alt="minus" src="icons/chevron-up.svg">
                <img class="icon-chevron-down" alt="plus" src="icons/chevron-down.svg">
                <label class="label1">{}</label>				
            </div>
        </div>
        <div class="collapse" id="bar{}">
    """
    if plbc is None:
        retval = start.format(head.format(pheadlevel, html.escape(ptitle), pheadlevel
                                      , parameters.nvl2(ptabid,'','<a href="#{}" onclick="download_table_as_csv(\'{}\');">download as CSV</a>'
                                                    .format(pselfanker, ptabid)
                                           ))
                              )
    else:
        retval = collapsestart.format(plbc
                                      ,head.format(pheadlevel+1, html.escape(ptitle), pheadlevel+1
                                                    , parameters.nvl2(ptabid,'','<a href="#{}" onclick="download_table_as_csv(\'{}\');">download as CSV</a>'
                                                                    .format(pselfanker, ptabid)
                                           ))
                                      , plbc)
    return retval
# startabschnitt
def endabschnitt(plbc=None,plabel=None):
    retval = """ 
    </div>
    """
    return retval
# startabschnitt

def starttable(ptitle, pheaders, pheadlevel=2, ptabid=None, pselfanker=None, plbc=None):
    tabhead = """
        <div class="table-responsive">
            <table class="table borderless" {}>
                <tbody>
                    <tr>
"""
    tabheads = """             <th>{}</th>
    """
    lineend = """               </tr>
    """

    retval = [startabschnitt(ptitle=ptitle, plbc=plbc, ptabid=ptabid, pheadlevel=pheadlevel, pselfanker=pselfanker)]
    retval.append(tabhead.format(parameters.nvl2(ptabid,'','id="{}"'.format(ptabid))))
    for u in pheaders:
        retval.append(tabheads.format(html.escape(u)))
    retval.append(lineend)
    return ''.join(retval)
# starttable

def writetableline(pwerte, plineid=None):
    linestart = """<tr>
        """ if plineid is None else """<tr id = "{}">
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
            retval.append(iconline.format(lf2htmlbr(parameters.nvl(w))))
        else:
            retval.append(line.format(parameters.nvl(lf2htmlbr(parameters.nvl(w)))))
    retval.append(lineend)
    return ''.join(retval)


def endtable(plbc=None,plabel="Details"):
    closetable = """
        </tbody>
      </table>
    </div>"""
    retval = closetable + endabschnitt(plbc=plbc,plabel=plabel)
    return retval

# endtable

def tablehtml(ptitel, pueberschriften, pwerteliste, plineid=None, pheadlevel=2, ptabid=None, pselfanker=None,plbc=None):
    retval = starttable(ptitle=ptitel, pheaders=pueberschriften, pheadlevel=pheadlevel, ptabid=ptabid,
                        pselfanker=pselfanker, plbc=plbc)
    for lw in pwerteliste:
        retval += writetableline(pwerte=lw, plineid=plineid)
    retval += endtable(plbc=plbc,plabel=ptitel)
    return retval


def printkeys(pelem,plang):
    keylist = [{'anker':k,'element':getelement(k)} for k in pelem['keys+']]
    if (len(keylist) == 0):
        return
    keyprint = []
    for k in keylist:
        attrs = ', '.join(href(ref=a,anz=getelement(a)['name'][plang]) for a in k['element']['key-elements']['attributes'])
        relas = ', '.join(getelement(r)['name'] for r in k['element']['key-elements']['relations'])
        key = (k['anker'],attrs,relas)
        keyprint.append(key)
    #for
    fhtml.write(tablehtml(ptitel=Languagetext.transl('Schlüssel')
                          , pueberschriften=(
            Languagetext.transl('Name'), Languagetext.transl('Attribute(e)'),
            Languagetext.transl('Beziehung(en)'))
                        , pwerteliste=keyprint
                          ,plbc=str(newbarcounter())
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
        name = getelement(intf)['name'] if intf != 0 else 'Information Model'
        werte.append([name, commalist])
    fhtml.write(tablehtml(ptitel=ptitel
                          , pueberschriften=pueberschriften
                          , pheadlevel=pheadlevel
                          , pwerteliste=werte
                          ,plbc=str(newbarcounter())
                          )
                )
# printmappinghtml

def printmapping(penti=None, pattr=None):
    if penti is not None:
        werte = {intf:[(tid, getelement(tid)['name']) for tid in tables] for intf,tables in penti['tablesmapped+'].items()}
        titel = Languagetext.transl('Relational Mapping (Tabellen)')
        ueberschr = (Languagetext.transl('Relational Model'), Languagetext.transl('Tabellen'))
    elif pattr is not None:
        werte = {intf:[(cid, getelement(cid)['name']) for cid in columns] for intf,columns in pattr['columnsmapped+'].items()}
        titel = Languagetext.transl('Relational Mapping (Columns)')
        ueberschr = (Languagetext.transl('Relational Model'), Languagetext.transl('Columns'))
    else:
        return
    # fi
    printmappinghtml(pwerte=werte, ptitel=titel, pueberschriften=ueberschr)
#printmapping



def printentirela(penti,plang):

    relalist = [{'anker': r, 'element': getelement(r)}
                  for r in penti['element']['relations+'] if not getelement(r)['type'] in (Relation.ISAROLE,Relation.ISASUBTYPE)]
    if ((len(relalist) == 0) and len(penti['element']["supertypes+"]+penti['element']["roles+"]+penti['element']["subtypes+"])==0):
        return
    lbc = str(newbarcounter())
    fhtml.write(starttable(ptitle=Languagetext.transl('Beziehungen'), plbc=lbc
                           , pheaders=(
            Languagetext.transl('Name'), Languagetext.transl('Entität') + '-1', '', Languagetext.transl('Beziehung'), '',
            Languagetext.transl('Entität') + '-2'
            , Languagetext.transl('Arc'), Languagetext.transl('Schlüssel'),)))
    for rela in relalist:
        elem = rela['element']
        if elem['type'] in (Relation.ISAROLE,Relation.ISASUBTYPE): continue
        fromarc = '' if (elem['from-to']['arc'] is None) else getelement(elem['from-to']['arc'])['name']
        toarc = '' if (elem['to-from']['arc'] is None) else getelement(elem['to-from']['arc'])['name']
        if (penti['anker'] == elem['from-to']['enti']):
            otherentiname = getelement(elem['to-from']['enti'])['name'][plang]

            # 'Name','Entität1','','Beziehung','', 'Entität2','Arc','Key'
            fhtml.write(writetableline(pwerte=(html.escape(parameters.nvl(elem['name'])), html.escape(penti['element']['name'][plang])
                                                        , '->', html.escape(parameters.nvl(elem['from-to']['assoc'][plang], '--'))
                                               , elem['from-to']['cardstr+']
                                               , arrow2icon('down'), fromarc, bool2icon(len(elem['isinkeys+']) > 0))))
            fhtml.write(writetableline(pwerte=('', arrow2icon('up'), elem['to-from']['cardstr+'], html.escape(parameters.nvl(elem['to-from']['assoc'][plang], '--')), '<-'
                                               , href(ref=elem['to-from']['enti'], anz=html.escape(otherentiname)))))
        else:
            otherentiname = getelement(elem['from-to']['enti'])['name'][plang]
            fhtml.write(writetableline(pwerte=(html.escape(parameters.nvl(elem['name'])), html.escape(penti['element']['name'][plang])
                                               , '->', html.escape(parameters.nvl(elem['to-from']['assoc'][plang], '--'))
                                               , elem['to-from']['cardstr+']
                                               , arrow2icon('down'), toarc, bool2icon(len(elem['isinkeys+']) > 0))))
            fhtml.write(writetableline(pwerte=('', arrow2icon('up'), elem['from-to']['cardstr+'], html.escape(parameters.nvl(elem['from-to']['assoc'][plang], '--')), '<-'
                                               , href(ref=elem['from-to']['enti'], anz=html.escape(otherentiname)))))
        # if
    # for
    entienvir = entityenviron.createentienvironment(pentiid=penti['anker'],pjson=getmodel(),pmodellang=plang)
    fhtml.write(entityenviron.entienviro2svg(pentiid=penti['anker'],penviron=entienvir))
    fhtml.write(endtable(plabel=Languagetext.transl('Beziehungen'), plbc=lbc))
# printentirela

def printcontentmapping(ptheme=None):
    grouplist=   WebUdp.indexlist(ptheme=ptheme)
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
        headerlist = [Languagetext.transl('Attribute')]
        udps = WebUdp.contentlist(ptheme=ptheme,pgroup=lgroup,pmeltname=Modelelemtype.ATTR)
        if len(udps) == 0: continue
        udpnames = [html.escape(u.dbobject().udpr_name) for u in udps]
        headerlist.extend(udpnames)

        webattrs = WebUdp.getattributes(ptheme=ptheme, pgroup=lgroup )
        lines = []
        for webattr in webattrs:
            line = [href(ref=webattr.webanker().anker(), anz=webattr.getqualifiedname(plang=Languagetext.reportLang()))]
            udpvalues = WebUdp.getvalues(ptheme=ptheme, pgroup=lgroup, pmodeid=webattr.getid(),pmeltype=Modelelemtype.ATTR)
            """[(udpr_name,udpv_value)]"""
            if (udpvalues is None or len(udpvalues)==0): continue
            udpvaldict = {html.escape(v[0]): html.escape(v[1]) for v in udpvalues}
            line.extend(udpvaldict[udpname] if udpname in udpvaldict else '' for udpname in udpnames)
            lines.append(line)

        lbc = str(newbarcounter())
        fhtml.write(contentelementhead.format(lanker.anker()
                                              , Languagetext.transl('Attribute - Mapping')
                                              , lgroup  # anzname
                                              , lbc))
        fhtml.write(detailshead)

        fhtml.write(starttable(ptitle='Mapping'
                               , pheaders=headerlist
                               , pheadlevel=3
                               , ptabid='TAB-{}'.format(lgroup if lgroup != '*' else 'ALL')
                               , pselfanker=lanker.anker()))
        for line in lines: fhtml.write(writetableline(pwerte=line))
        fhtml.write(endtable())

        fhtml.write(detailsfoot)
        fhtml.write(contentelementfoot.format(lbc, Languagetext.transl('Mehr')))
    # for


def printUDP(pelem):
    startwritten = False

    for theme,jtheme in pelem['userdefprops'].items():
        """theme"""
        """translations are not printed"""
        if (theme == parameters.odmUDPTranslFileName()): continue

        for group,jgroup in jtheme.items():
            displvalues = {html.escape(prop['name']): html.escape(parameters.nvl(prop['value'])) for prop in jgroup.values()}

            """write only if there is at least one value not empty"""
            if (len(displvalues) > list(displvalues.values()).count('')):
                if (not startwritten):
                    lbc = str(newbarcounter())
                    fhtml.write(startabschnitt(ptitle=Languagetext.transl('Benutzerdefinerte Eigenschaften'), plbc=lbc))
                    startwritten = True
                # fi

                fhtml.write(tablehtml(ptitel=html.escape(' {} - {} '.format(theme,group))
                                  , pueberschriften=list(displvalues.keys())
                                  , pheadlevel=3
                                  , pwerteliste=[list(displvalues.values())]
                                )
                           )
            #fi
        #for
    #for
    if (startwritten):
        fhtml.write(endabschnitt(plabel=Languagetext.transl('Benutzerdefinerte Eigenschaften'), plbc=lbc))
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

def hasiconfiles():
    iconmaster = [key for key,val in getmodel().getelements(pelemtype=Modelelemtype.DOCU).items()
                            if val["name"]== parameters.iconmasterdocumentname()]
    return len(iconmaster) == 1

def iconsrc(pjsenti):
    icon = pjsenti["icon"]
    if icon['type']== 'FYAYCICON':
        filename = ''  #to be resolved
    elif icon['type']== 'URL':
        return icon['reference']
    elif icon['type']== 'FILE':
        filename = icon['reference']
    else:
        """look for entityname in defaultlanguage"""
        filename = pjsenti["name"][getmodel().getdefaultlang()]
        filename = re.sub(r'[^a-zäöüñéàè0-9_-]+', '', filename.lower())
    #fi
    #filename found search in image
    if os.path.isfile(filename):
        #absolute path, return it
        return filename

    #search for filename with extensions in image directory
    for ext in ('png','jpg','jpeg','gif'):
        fullfilename = "{}/{}.{}".format('image',filename,ext).lower()
        if os.path.isfile(parameters.webDirec()+ fullfilename):
            return fullfilename
    return ''


def printcontententi():
    lang = Languagetext.reportLang()
    printcontentstart('entities')
    infoheaders = (Languagetext.transl('Synonyme'), Languagetext.transl('Superentitäten')
                   , Languagetext.transl('Subentitäten'), Languagetext.transl('Rollen')
                   ,'Zoom levels','Dev. Status'
                   , Languagetext.transl('auf Diagramm(en)')
                   , Languagetext.transl('geändert'))

    for enti in sorted([{'anker':key,'element': value}
                     for key,value in getmodel().getelements(pelemtype='entities').items()]
                     ,key=lambda val:val['element']['name'][lang]):
        elem = enti['element']
        lbc = str(newbarcounter())
        printcontent(ptype=Languagetext.transl('Entität')
                     , panker=enti['anker']
                     , pname=elem['name'][lang]
                     , piconsrc=iconsrc(pjsenti=elem)
                     , pdescr=lf2htmlbr(parameters.nvl(elem['descr'][lang]))
                     , plbc=lbc)
        """print entity Info"""
        synostr = ', '.join(s[lang] for s in elem['synonyms'].values())
        parentstr = ", ".join(href(ref=p, anz=getelement(p)['name'][lang]) for p in elem['supertypes+'])
        subtypestr = ', '.join(href(ref=st, anz=getelement(st)['name'][lang]) for st in elem['subtypes+'])
        rolesstr = ', '.join(href(ref=r, anz=getelement(r)['name'][lang]) for r in elem['roles+'])
        diagstr = ', '.join(href(ref="{}-{}".format(d, enti['anker'])
                                    , anz=getelement(d)['name']) for d in elem['diagrams+'])
        infovalues = (parameters.nvl(synostr), parentstr, subtypestr,rolesstr
                      ,'{} - {}'.format(elem['minzoomlevel'],elem['maxzoomlevel']),Modelelement.longdevstatus(elem['devstatus'])
                      , diagstr, parameters.nvl(elem['uc']) + ', ' + parameters.nvl(elem['dc']))
        printcontentinfo(ptitle=Languagetext.transl('Informationen'), pheaders=infoheaders, pvalues=infovalues)
        printattrlist(penti=elem)
        printkeys(pelem=elem,plang=lang)
        printentirela(penti=enti,plang=lang)
        printelemreflists(pelem=elem, pelemtype=Modelelemtype.ENTI)
        printtransl(penti=enti)
        printUDP(pelem=elem)
        printmapping(penti=elem)
        printcontentend(lbc)
    # for
# printcontententi

def printcontentattr():
    infoheaders = (
        Languagetext.transl('Technischer Name'), Languagetext.transl('Wertebereich'), Languagetext.transl('Datentyp'),
        Languagetext.transl('Tooltip')
        , 'Zoom levels', 'Dev. Status'
    , Languagetext.transl('geändert'))
    flagheaders = (
        Languagetext.transl('Pflichtattribut'), Languagetext.transl('Schlüssel'), Languagetext.transl('Deskriptor'),
        Languagetext.transl('übersetzt')
        , Languagetext.transl('historisiert'), Languagetext.transl('wiederholt'), Languagetext.transl('verschlüsselt'))
    lang = Languagetext.reportLang()

    for attr in sorted([{'anker':key,'element': value}
                     for key,value in getmodel().getelements(pelemtype='attributes').items()]
                     ,key=lambda val:val['element']['name'][lang]):
        elem = attr['element']
        printcontentstart('attributes')
        if elem['entity'] is None:
            master = 'Relation tbd'
        else:
            enti = getelement(elem['entity'])
            master = "<p1>{}: {}</p1><br>" \
                .format(Languagetext.transl('Entität'), href(ref=elem['entity'], anz=enti['name'][lang]))
        #fi

        lbc = str(newbarcounter())
        printcontent(ptype=Languagetext.transl('Attribute')
                     , panker=attr['anker']
                     , pname=elem['name'][lang]
                     , pmaster=master
                     , pdescr=lf2htmlbr(parameters.nvl(elem['descr'][lang]))
                     , plbc=lbc)
        domain = getelement(elem['domain'])
        domainname=domain['name'][lang]
        domainref =  domainname if  domain['origin'] == Domain.DERIVED\
                     else href(ref=elem['domain'], anz=domainname)
        infovalues = (parameters.nvl(elem['techname'], ''), domainref, domain['displdatatype+'][lang]
                      , parameters.nvl(elem['tooltip'][lang])
                      , '{} - {}'.format(elem['minzoomlevel'], elem['maxzoomlevel']),Modelelement.longdevstatus(elem['devstatus'])
                      , re.sub(r'^, $', '', parameters.nvl(elem['uc']) + ', ' + parameters.nvl(elem['dc'])))
        printcontentinfo(ptitle=Languagetext.transl('Informationen'), pheaders=infoheaders, pvalues=infovalues)

        flagvalues = (bool2icon(elem['mandatory']), bool2icon(len(elem['keys+'])>0), bool2icon(elem['descriptive'])
                      , bool2icon(elem['translated'])
                      , bool2icon(elem['historicised']), bool2icon(elem['repeated']),
                      bool2icon(elem['encrypted']))
        printflagline(pheaders=flagheaders, pvalues=flagvalues)
        printkeys(pelem=elem,plang=lang)
        printelemreflists(pelem=elem, pelemtype=Modelelemtype.ATTR)
        printtransl(pattr=attr)
        printUDP(pelem=elem)
        printmapping(pattr=elem)
        printcontentend(lbc)
    # for
# printcontentattr


def printelemreflists(pelem, pelemtype):
    def refelements(pentries):
        elementries = []
        for refentry in pentries:
            # aus schn-html zurück ins Main
            htmlname = htmlfilelist[0] if (pelemtype in (Modelelemtype.TABL, Modelelemtype.INTF, Modelelemtype.COLU)) \
                else ''
            elementries.append(href(ref=refentry[0], anz=refentry[1]['name'], htmlfile=htmlname))
        # for
        return elementries
    #dorefelements

    docentries = [] if not 'refindocuments+' in pelem else refelements(pentries=[[d, getelement(d)] for d in pelem['refindocuments+']])
    orguentries = [] if not 'refbyorgunits+' in pelem else refelements(pentries=[[d, getelement(d)] for d in pelem['refbyorgunits+']])
    if (len(docentries) > 0 or len(orguentries)>0) :
        lbc = str(newbarcounter())
        fhtml.write(starttable(ptitle=Languagetext.transl('Referenziert in'), plbc=lbc
                                   , pheaders=[Languagetext.transl('Typ'), Languagetext.transl('Elemente')]))

        if len(docentries) > 0: fhtml.write(writetableline(pwerte=[Languagetext.transl('Dokumente'), ', '.join(docentries)]))
        if len(orguentries) > 0: fhtml.write(writetableline(pwerte=[Languagetext.transl('Org. Einheiten'), ', '.join(orguentries)]))

        fhtml.write(endtable(plabel=Languagetext.transl('Referenziert in'), plbc=lbc))
    # if
#printelemreflists

def origindomains(pintfid):
    #dict of domain with origin DOMAIN and defined in interface intfid (or im if None)
    return {key: value for key, value in getmodel().jsmodel['domains'].items()
                                                if (value['origin'] == Domain.DOMAIN
                                                and value['interface-id'] == pintfid)}


def printdomaattrlist(pdoma, plang,pisgroup=False):
    if pisgroup:
        """all domains of type group containing parameter domain in elements of its group"""
        alist = [[href(ref=domaanker
                       ,anz=getelement(domaanker)['name'][plang])]
                 for domaanker in pdoma['element']['usedingrps+']
                ]
    else:
        alist = [[href(ref=attranker
                       ,anz="{} ({})".format(getelement(attranker)['name'][plang]
                                            ,'' if getelement(attranker)['entity'] is     None\
                                               else getelement(getelement(attranker)['entity'])['name'][plang]
                                             ))]
                for attranker in pdoma['element']['usedinattrs+']
                ]
    if (len(alist)==0):return

    fhtml.write(tablehtml(ptitel=Languagetext.transl('Verwendet in Attributgruppen' if pisgroup
                                                   else 'Verwendet für Attribute')
                          , pueberschriften=['']#[Languagetext.transl('Attributgruppe' if pisgroup
                                                #               else 'Attribute')]
                          , pwerteliste=alist
                          ,plbc=str(newbarcounter())))
#printdomaattrlist

def printdomacollist(pdoma):
    domaintfid = pdoma['element']['interface-id']
    clist = [[href(ref=colanker
                       ,anz=getelement(colanker)['name']
                   ,htmlfile='' if domaintfid == getelement(colanker)['interface-id+'] else htmlfilelist[getelement(colanker)['interface-id+']])
              ,href(ref=getelement(colanker)['table-id']
                   , anz=getelement(colanker)['table-name+']
                   , htmlfile='' if domaintfid == getelement(colanker)['interface-id+'] else htmlfilelist[getelement(colanker)['interface-id+']])
              ,href(ref=''
                   , anz=getelement(colanker)['interface-name+']
                   , htmlfile='' if domaintfid == getelement(colanker)['interface-id+'] else htmlfilelist[getelement(colanker)['interface-id+']])

              ]
                for colanker in pdoma['element']['usedincols+']
                ]

    if (len(clist) == 0): return
    fhtml.write(tablehtml(ptitel=Languagetext.transl('Verwendet für Columns')
                          , pueberschriften=[Languagetext.transl('Column'), Languagetext.transl('Table'), Languagetext.transl('System')]
                          , pwerteliste=clist
                          ,plbc=str(newbarcounter())
                          ))
#printdomacollist

def printdomamembers(pelem):
    elems = pelem['elements']
    if (len(elems) == 0):
        return
    lang =Languagetext.reportLang()
    fhtml.write(tablehtml(ptitel=Languagetext.transl('Elemente')
                          , pueberschriften=
                          [Languagetext.transl('Element')
                              , Languagetext.transl('Beschreibung')
                              , Languagetext.transl('Wertebereich')
                              , Languagetext.transl('Pflichtattribut')
                           ]
                          , pwerteliste=[[e['name']
                                         , e['descr']
                                        , href(ref=e['domain']
                                            , anz="{} ({})".format(getelement(e['domain'])['name'][lang]
                                                                ,getelement(e['domain'])['displdatatype+'][lang]))
                                        , bool2icon(e['mandatory'])
                                       ] for e in elems]))

# printdomamembers

def printwertelist(pelem):
    vlist = sorted([(val['sort'],val['value'],val['displ'],val['descr'])
                        for val in pelem['values']]
            , key=lambda val: val[0])
    if (len(vlist) == 0):
        return
    fhtml.write(tablehtml(ptitel=Languagetext.transl('Werteliste')
                          , pueberschriften=(
            Languagetext.transl('Nr'), Languagetext.transl('Wert')
                            , Languagetext.transl('Anzeige'), Languagetext.transl('Beschreibung')
                            )
                          , pheadlevel=3
                          , pwerteliste=vlist)
                        )
# printwertelist


def printcontentdoma(pdomains):

    lang = Languagetext.reportLang()
    for doma in sorted([{'anker': key, 'element': value}
                        for key, value in pdomains.items()]
            , key=lambda val: val['element']['name'][lang]):
        elem = doma['element']
        printcontentstart('domains')
        lbc = str(newbarcounter())

        printcontent(ptype=Languagetext.transl('Wertebereich')
                     , panker=doma['anker']
                     , pname=elem['name'][lang]
                     , pdescr=lf2htmlbr(parameters.nvl(elem['descr'][lang]))
                     , plbc=lbc)

        if (elem['type'] in (Domain.TXT, Domain.LOV)):
            infoheaders = (
                Languagetext.transl('Datentyp'), Languagetext.transl('Max. Länge'), Languagetext.transl('Syntaxregel'),
                Languagetext.transl('geändert'))
            infovalues = (
                parameters.nvl(elem['displdatatype+'][lang]), parameters.nvl(elem['maxlng']), parameters.nvl(elem['syntaxrule'] if elem['type'] == Domain.TXT else ''),
                parameters.nvl(elem['uc']) + ',' + parameters.nvl(elem['dc']))
        elif (elem['type'] == Domain.BIN):
            infoheaders = (Languagetext.transl('Datentyp'), Languagetext.transl('Inhaltstyp'), Languagetext.transl('Format'),
                           Languagetext.transl('geändert'))
            infovalues = (
            parameters.nvl(elem['displdatatype+'][lang]), parameters.nvl(elem['contenttype']),
                parameters.nvl(elem['contenttypename+']), parameters.nvl(elem['uc']) + ',' + parameters.nvl(elem['dc']))
        elif (elem['type'] == Domain.GRP):
            infoheaders = (Languagetext.transl('Datentyp'), Languagetext.transl('geändert'))
            infovalues = (elem['displdatatype+'][lang], parameters.nvl(elem['uc']) + ',' + parameters.nvl(elem['dc']))
        elif (elem['type'] == Domain.NUM):
            infoheaders = (
                Languagetext.transl('Datentyp'), Languagetext.transl('Vorkommast.'), Languagetext.transl('Nachkommast.')
                , Languagetext.transl('Rundungseinh.'), Languagetext.transl('Einheit'), Languagetext.transl('Min. Wert'),
                Languagetext.transl('Max. Wert')
                , Languagetext.transl('geändert'))
            infovalues = (
                parameters.nvl(elem['displdatatype+'][lang]), parameters.nvl(elem['totaldigits']), parameters.nvl(elem['fractdigits']),
                parameters.nvl(elem['roundvalue']), parameters.nvl(elem['unit'])
                , parameters.nvl(elem['minvalue']), parameters.nvl(elem['maxvalue'])
                , parameters.nvl(elem['uc']) + ',' + parameters.nvl(elem['dc']))
        elif (elem['type'] == Domain.DAT):
            infoheaders = (
                Languagetext.transl('Datentyp'), Languagetext.transl('Min. Wert'), Languagetext.transl('Max. Wert'),
                Languagetext.transl('Granularität')
                , Languagetext.transl('geändert'))
            infovalues = (elem['displdatatype+'][lang], parameters.nvl(elem['minvalue']), parameters.nvl(elem['maxvalue']),
                          parameters.nvl(elem['granularitytext+'][lang]), parameters.nvl(elem['uc']) + ',' + parameters.nvl(elem['dc']))
        else:
            infoheaders, infovalues = None, None
        # fi
        if infoheaders is not None: printcontentinfo(ptitle=Languagetext.transl('Informationen'), pheaders=infoheaders,
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
    if ptyp == Modelelemtype.ENTI:
        return Languagetext.transl('Entität', plang)
    elif ptyp == Modelelemtype.ATTR:
        return Languagetext.transl('Attribut', plang)
    elif ptyp == Modelelemtype.DOMA:
        return Languagetext.transl('Wertebereich', plang)
    elif ptyp == Modelelemtype.DIAG:
        return Languagetext.transl('Diagramm', plang)
    elif ptyp == Modelelemtype.TABL:
        return Languagetext.transl('Tabelle', plang)
    elif ptyp == Modelelemtype.DOCU:
        return Languagetext.transl('Dokument', plang)
    elif ptyp == Modelelemtype.ORGU:
        return Languagetext.transl('Organisatioseinheit', plang)
    elif ptyp == Modelelemtype.INTF:
        return Languagetext.transl('System', plang)
    elif ptyp == Modelelemtype.COLU:
        return Languagetext.transl('Column', plang)
    else:
        return ptyp
    #fi
#type2name

def printreflist(pelem,plang):
    fhtml.write(starttable(ptitle=Languagetext.transl('Referenziert')
                           , pheaders=[Languagetext.transl('Typ'), Languagetext.transl('Elemente')]))

    types = set([jsguid2type(ref) for ref in pelem['references+']])
    refentries = {typ: [{'anker': e
                        , 'name': getelement(e)['name']
                        ,'htmlfile': htmlfilelist[getelement(e)['interface-id+']] if (typ in (Modelelemtype.COLU,Modelelemtype.INTF))
                                     else htmlfilelist[getelement(e)['interface-id']] if (typ in (Modelelemtype.TABL)) else ''
                         } for e in pelem['references+'] if jsguid2type(e) == typ] for typ in types}
    if (len(refentries) == 0): return
    for typ,ref in refentries.items():
        if len(ref)==0: continue
        # aus schn-html zurück ins Main
        docuentry = ', '.join (href(ref='' if (typ in (Modelelemtype.INTF)) else elem['anker']
                                    ,anz=elem['name'] if (typ in (Modelelemtype.TABL,Modelelemtype.COLU,Modelelemtype.INTF))\
                                                else elem['name'][plang]
                                    ,htmlfile=elem['htmlfile']
                                    ) for elem in ref)
        fhtml.write(writetableline(pwerte=[type2name(ptyp=typ,plang=plang),docuentry]))
    # for
    fhtml.write(endtable())
#printreflist

def printcontentdoku():
    docus = sorted([{'anker': key, 'element': value}
            for key, value in getmodel().jsmodel['documents'].items()]
            ,key=lambda val : val['element']['name'])
    printcontentstart('documents')
    infoheaders = (Languagetext.transl('Format'), Languagetext.transl('Referenz'), Languagetext.transl('Vaterdokument')
                   , Languagetext.transl('Unterdokumente'))
    for doc in docus:
        elem = doc['element']
        lbc = str(newbarcounter())
        parentanker=elem['parent']
        parentname = None if parentanker is None else getelement(parentanker)['name']
        printcontent(ptype=Languagetext.transl('Dokument')
                     , panker=doc['anker']
                     , pname=elem['name']
                     , pdescr=""
                     , plbc=lbc)

        children = [href(ref=key,anz=val['name']) for key,val in getmodel().jsmodel['documents'].items() if val['parent'] == doc['anker']]
        kinder = ', '.join(c for c in children)

        infovalues = (parameters.nvl(elem['format+']), parameters.nvl(elem['reference']),
                      parameters.nvl2(parentanker,'',href(ref=parentanker,anz=parentname)), kinder)
        printcontentinfo(ptitle=Languagetext.transl('Informationen'), pheaders=infoheaders, pvalues=infovalues)
        printreflist(pelem=elem, plang=Languagetext.reportLang())
        printcontentend(lbc)
    # for
# printcontentdoku

def printcontentorgu():
    orgus = sorted([{'anker': key, 'element': value}
            for key, value in getmodel().jsmodel['orgunits'].items()]
            ,key=lambda val : val['element']['name'])
    printcontentstart('orgunits')
    infoheaders = (Languagetext.transl('descr'), Languagetext.transl('Mail'),Languagetext.transl('Telefon') , Languagetext.transl('Adresse')
                    ,Languagetext.transl('übergeordnet'), Languagetext.transl('untergeordnet'))
    for orgu in orgus:
        elem = orgu['element']
        lbc = str(newbarcounter())
        parentanker=elem['parent']
        parentname = None if parentanker is None else getelement(parentanker)['name']
        printcontent(ptype=Languagetext.transl('Organisationseinheit')
                     , panker=orgu['anker']
                     , pname=elem['name']
                     , pdescr=""
                     , plbc=lbc)

        children = [href(ref=key,anz=val['name']) for key,val in getmodel().jsmodel['orgunits'].items() if val['parent'] == orgu['anker']]
        kinder = ', '.join(c for c in children)

        infovalues = (parameters.nvl(elem['descr']), parameters.nvl(elem['mail']),parameters.nvl(elem['telefon']),parameters.nvl(elem['address']),
                      parameters.nvl2(parentanker,'',href(ref=parentanker,anz=parentname)), kinder)
        printcontentinfo(ptitle=Languagetext.transl('Informationen'), pheaders=infoheaders, pvalues=infovalues)
        printreflist(pelem=elem, plang=Languagetext.reportLang())
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
    global libSourceDirec, imagedirec, cssdirec, icondirec,jsdirec,jinadirec

    webDirectory = parameters.nvl(p_webdirec, parameters.webDirec());
    webFileName = parameters.odmModelName();
    imagedirec = webDirectory + 'image/';
    cssdirec = webDirectory + "css/";
    icondirec = webDirectory + "icons/";
    jsdirec = webDirectory + "js/";
    jinadirec = webDirectory + "jinjatemplates/";

    libSourceDirec = os.path.dirname(os.path.abspath(__file__))
    libSourceDirec += '/../html-lib/';
    if (parameters.logoFileName() is None): parameters.logoFileName(searchlogo(imagedirec));


def createlib():
    global cssdirec,icondirec,imagedirec,jsdirec,libSourceDirec,jinadirec
    if not os.path.exists(cssdirec):
        shutil.copytree(libSourceDirec + 'css', cssdirec)
    if not os.path.exists(jsdirec):
        shutil.copytree(libSourceDirec + 'js', jsdirec)
    if not os.path.exists(icondirec):
        shutil.copytree(libSourceDirec + 'icons', icondirec)
    if not os.path.exists(imagedirec):
        shutil.copytree(libSourceDirec + 'image', imagedirec)
    if not os.path.exists(jinadirec):
        shutil.copytree(libSourceDirec + 'jinjatemplates', jinadirec)
    else: #replace the original files every time
        shutil.copytree(libSourceDirec + 'jinjatemplates/original', jinadirec + 'original/',dirs_exist_ok=True)


# createlib

def copyimages():
    global imagedirec
    """copy all file from the modeler-image directory into the web-image directory"""
    if os.path.exists(parameters.odmFilesDirec()+'images'):
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
        return Languagetext.transl('Name')
    elif pattrname in ['ENTI_COMMENT', 'ATTR_COMMENT']:
        return Languagetext.transl('Beschreibung')
    elif pattrname in ['ENTI_SYNONYM']:
        return Languagetext.transl('Synonym')
    else:
        return pattrname
    # fi


def findtransl(pattrname, pmodeid, plangs, panker = None):
    tl = [attname2element(pattrname)]
    for l in plangs:
        name = Languagetext.transltext(pattrname=pattrname, pmodeid=pmodeid, plang=l)
        if panker is None:
            eintrag = name
        else:
            eintrag = filehref(panz=name, pref=panker, plang=l)
        tl.extend([eintrag])
    return tl


def printtransl(penti=None, pattr=None):
    global webFileName
    langfilename = "{}_{}.html".format(webFileName,'{}')
    langs = [k for k in getmodel().jsmodel['languages'].keys()]
    try:
        langs.remove(Languagetext.reportLang())
    except:
        pass
    if len(langs) == 0: return
    head = [Languagetext.transl('Element')]
    head.extend(langs)
    name = [Languagetext.transl('Name')]
    descr = [Languagetext.transl('Beschreibung')]
    synonym = [Languagetext.transl('Synonym')]
    if (penti is not None):
        name +=[href(ref=penti['anker'], anz=penti['element']['name'][lang]
                     ,htmlfile=langfilename.format(lang),pself=True) for lang in langs]
        synonym += [','.join(s[lang] for s in penti['element']['synonyms'].values()) for lang in langs]
        descr += [penti['element']['descr'][lang] for lang in langs]
        transllist = [name,synonym,descr]
    elif (pattr is not None):
        name +=[href(ref=pattr['anker'], anz=pattr['element']['name'][lang]
                     ,htmlfile=langfilename.format(lang),pself=True) for lang in langs]
        descr += [pattr['element']['descr'][lang] for lang in langs]
        transllist = [name,descr]
    #fi
    fhtml.write(tablehtml(ptitel=Languagetext.transl('Übersetzungen')
                          , pueberschriften=head
                          , pheadlevel=2
                          , pwerteliste=transllist
                          ,plbc=str(newbarcounter()))
                            )
# printtransl
