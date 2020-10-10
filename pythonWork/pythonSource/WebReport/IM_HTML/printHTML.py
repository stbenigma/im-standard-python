import os
import re
import shutil

from IM_DB import parameters
from IM_HTML import web_sql
from IM_OBJECTS import *
import html

outputDirectory: str = None
webDirectory: str = "";
webFileName: str = "";
webFileNamePath: str = "";
libSourceDirec: str = "";
imagedirec: str = "";
cssdirec: str = "";
icondirec: str = "";
htmlfilelist = {}

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

def nvl(x, default=''):
    return x if (x is not None) else default


# nvl

def filehref(ref, anz, plang, pimg=None):
    img = '' if pimg is None else '<img class="icon-check" src="icons/{}">'.format(pimg)
    return """<a href="{}{}" target="_blank" >{}{}</a>""" \
        .format(webFileName + '_' + plang.lower() + '.html'
                , "#" + ref if ref is not None else "", anz, img)


def href(ref, anz, htmlfile=''):
    if anz is None: return ''
    sep = '' if ((ref is None) or (ref == '')) else '#'
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
#         elem.append(href(ref=
#             web_sql.entiAnker(el1[0]) if ptype == 'ENTI' else
#             web_sql.dokuAnker(el1[0]) if ptype == 'DOKU' else
#             el1[0]
#         , anz=el1[1]))
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


def printhead(p_firma, p_titel, p_info, p_logofilename):
    htmlhead: str = """<!DOCTYPE html>
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
    """.format(p_titel, p_firma, p_titel, p_info, p_logofilename, p_firma)
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
    if len(plist) == 0: return
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
    for l in plist:
        inanker = l[1]
        local = False
        if type(inanker) == Webanker:
            local = re.match(r'/(.+/)*{}'.format(htmlfilelist[inanker.modelid()])
                             , fhtml.name)
            anker = '' if (local) else htmlfilelist[inanker.modelid()]
            if not pfileonly:
                anker += '#' + inanker.anker()
        else:
            anker = '#' + l[1]
        anzeige = l[0]
        fhtml.write(listcontentline.format(anker, '_self' if local else '_blank', anzeige))
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
        str += filehref(ref=None, anz=l + '   ', plang=l, pimg=lang2img(l.lower()))
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

def printcontent(ptype, pname, panker, plbc, pdescr="", pmaster=""):
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

    fhtml.write(contentelementhead.format(panker, ptype, pname
                                          , pmaster
                                          , "" if (pdescr == "") else "<p1>{}</p1>".format(pdescr)
                                          , plbc))


# printcontent

def printflagline(pheaders, pvalues):
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
    alist = penti.getattributes()
    if (len(alist) == 0):
        return

    fhtml.write(starttable(ptitel=Sprachtext.transl('Attribute')
                           , pueberschriften=(
            Sprachtext.transl('Name'), Sprachtext.transl('Domain'), Sprachtext.transl('Typ')
            , Sprachtext.transl('Pflichtattribut'), Sprachtext.transl('Schlüssel'), Sprachtext.transl('Deskriptor'),
            Sprachtext.transl('übersetzt')
            , Sprachtext.transl('historisiert'), Sprachtext.transl('wiederholt'), Sprachtext.transl('verschlüsselt'))))

    for attr in alist:
        domain = attr.getdomain()
        domname = html.escape(domain.getname(Sprachtext.reportLang()))
        domainref = domname if domain.isderived() \
                        else href(ref=domain.webanker().anker(), anz=domname)
        fhtml.write(writetableline(pwerte=(href(ref=attr.webanker().anker(), anz=attr.getname(Sprachtext.reportLang()))
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
    retval.append(tabhead.format(pheadlevel, html.escape(ptitel), pheadlevel
                                 , '' if ptabid is None
                                 else '<a href="#{}" onclick="download_table_as_csv(\'{}\');">download as CSV</a>'.format(
            pselfanker, ptabid)
                                 , '' if ptabid is None
                                 else 'id="{}"'.format(ptabid)))
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


def printentikeys(pentiid):
    keylist = web_sql.keylist(p_entiid=pentiid, p_lang=Sprachtext.reportLang())
    if (len(keylist) == 0):
        return
    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Schlüssel')
                          , pueberschriften=(
            Sprachtext.transl('Nr'), Sprachtext.transl('Name'), Sprachtext.transl('Attribute(e)'),
            Sprachtext.transl('Beziehung(en)'))
                          , pwerteliste=keylist
                          )
                )


# printentikeys

def printmappinthtml(pwerte, ptitel, pueberschriften, pheadlevel=2):
    # pwerte, list of entries mit {'name':webanker}
    if (pwerte is None or len(pwerte) == 0):
        return
    werte = []
    for t in pwerte:
        name, tabs = t[0], t[1]
        commalist = ', '.join([href(ref=value.anker(), anz=key, htmlfile=htmlfilelist[value.modelid()]) \
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
    printmappinthtml(pwerte=werte, ptitel=titel, pueberschriften=ueberschr)


def printentirela(pentiid):
    relalist = web_sql.relalist(p_entiid=pentiid, p_lang=Sprachtext.reportLang())
    if (len(relalist) == 0):
        return
    fhtml.write(starttable(ptitel=Sprachtext.transl('Beziehungen')
                           , pueberschriften=(
            Sprachtext.transl('Name'), Sprachtext.transl('Entität') + '-1', '', Sprachtext.transl('Beziehung'), '',
            Sprachtext.transl('Entität') + '-2'
            , Sprachtext.transl('Arc'), Sprachtext.transl('Schlüssel'),)))
    for r in relalist:
        if (pentiid == r[0]):
            # 'Name','Entität1','','Beziehung','', 'Entität2','Arc','Key'
            fhtml.write(writetableline(pwerte=(html.escape(nvl(r[16])), html.escape(r[1]), '->', html.escape(nvl(r[3], '--'))
                                               , html.escape(nvl(r[4]))
                                               , arrow2icon('down'), nvl(r[14]), bool2icon(r[17]))))
            fhtml.write(writetableline(pwerte=('', arrow2icon('up'), r[9], html.escape(nvl(r[8], '--')), '<-'
                                               , href(ref=web_sql.entiAnker(r[5]), anz=html.escape(r[6])))))
        else:
            fhtml.write(writetableline(pwerte=(html.escape(nvl(r[16])), html.escape(r[6]), '->', html.escape(nvl(r[8], '--'))
                                               , html.escape(nvl(r[9]))
                                               , arrow2icon('down'), '', bool2icon(r[17]))))
            fhtml.write(writetableline(pwerte=('', arrow2icon('up'), r[4], html.escape(nvl(r[3], '--')), '<-'
                                               , href(ref=web_sql.entiAnker(r[0]), anz=html.escape(r[1])))))
        # if
    # for
    fhtml.write(endtable())


# printentirela

def printcontentmapping(plist):
    if len(plist) == 0: return
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
        lthema = m[2]
        lgruppe = m[0]
        lanker = m[1]
        namenliste = [Sprachtext.transl('Attribute')]
        udpnamen = web_sql.udpnamen(pmeltname='ATTR', pthema=lthema, pgruppe=lgruppe)
        # print ('udpnamen=',udpnamen,m[2],m[0])
        if len(udpnamen) == 0: continue
        udpnamen = udpnamen[0][2].split(',')
        udpnamen.sort()  # SQl kann keine sortierte group_concat liefern
        udpnamen = [html.escape(u) for u in udpnamen]

        # print ('udpnamen=',udpnamen)
        namenliste.extend(udpnamen)

        al = web_sql.udpattrlist(pthema=lthema, pgruppe=lgruppe, plang=Sprachtext.reportLang())
        werte = []
        for a in al:
            zeile = [href(ref=a[1], anz=a[0])]
            udpwerte = web_sql.udpwerte(pmeltname='ATTR', pthema=lthema, pgruppe=lgruppe, pid=a[2])
            if udpwerte is None: continue
            zeile.extend(html.escape(w[0]) for w in udpwerte)
            werte.append(zeile)

        lbc = str(newbarcounter())
        fhtml.write(contentelementhead.format(lanker
                                              , Sprachtext.transl('Attribute - Mapping')
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
        fhtml.write(contentelementfoot.format(lbc, Sprachtext.transl('Mehr')))
    # for


def printUDP(p_meltname, p_id, pwithref=False):
    startgeschrieben = False

    udpentries = web_sql.udpnamen(pmeltname=p_meltname)
    for udpentry in udpentries:
        if udpentry[0] == parameters.odmUDPTranslFileName():
            continue
        namenliste = udpentry[2].split(',')
        namenliste.sort()  # SQl kann keine sortierte group_concat liefern
        anzwerte = {udpname: '' for udpname in namenliste}
        werte = web_sql.udpwerte(pmeltname=p_meltname, pthema=udpentry[0], pgruppe=udpentry[1], pid=p_id)
        """werte = [(bdeg_name,bdeg_wert),...]"""
        for l in werte:
            anzwerte[l[0]] = html.escape(l[1])

        if (len(anzwerte) > list(anzwerte.values()).count('')):
            if (not startgeschrieben):
                fhtml.write(startabschnitt(p_titel=Sprachtext.transl('Benutzerdefinerte Eigenschaften')))
                startgeschrieben = True
            # fi

            titel = href(ref=web_sql.udpAnker('{}-{}'.format(udpentry[0], udpentry[1])) \
                         , anz=' {} - {} '.format(udpentry[0], udpentry[1])) \
                if pwithref else ' {} - {} '.format(udpentry[0], udpentry[1])
            fhtml.write(tablehtml(ptitel=titel
                                  , pueberschriften=namenliste
                                  , pheadlevel=3
                                  , pwerteliste=[list(anzwerte.values())])
                        )
    #            fhtml.write(starttable(ptitel=href(ref=web_sql.udpAnker('{}-{}'.format(udpname[0],udpname[1]))
    #                                               ,anz=' {} - {} '.format(udpname[0], udpname[1]))
    #                                   , pueberschriften=namenliste
    #                                   , pheadlevel=3))
    #            fhtml.write(writetableline(pwerte=lw))
    #            fhtml.write(endtable())
    # fi
    # rof
    if (startgeschrieben):
        fhtml.write(endabschnitt())
    # fi


# printUDP

def printentiudp(pentiid):
    printUDP(p_meltname='ENTI', p_id=pentiid)


# printentiudp

def printattrudp(pattrid):
    printUDP(p_meltname='ATTR', p_id=pattrid)


# printattrudp

def entidiag(pentiid):
    doppelanker = "{}-{}"
    diaglist = web_sql.diaglist(pentiid=pentiid)
    if (len(diaglist) == 0):
        return
    diagdict = {dl[0]: dl[1] for dl in diaglist}
    diagstring = ', '.join(href(ref=doppelanker.format(web_sql.diagAnker(id)
                                                       , web_sql.entiAnker(pentiid))
                                , anz=str(name)) for name, id in diagdict.items())
    # print (diagstring)
    return diagstring


# entidiag

def printcontententi():
    printcontentstart('entities')
    infoheaders = (Sprachtext.transl('Synonyme'), Sprachtext.transl('Superentität')
                   , Sprachtext.transl('Subentitäten'), Sprachtext.transl('auf Diagram(en)')
                   , Sprachtext.transl('geändert'))

    for enti in Entity.select(porderby='enti_name'):
        lbc = str(newbarcounter())
        printcontent(ptype=Sprachtext.transl('Entität')
                     , panker=enti.webanker().anker()
                     , pname=enti.getname(Sprachtext.reportLang())
                     , pdescr=lf2htmlbr(nvl(enti.enti_descr))
                     , plbc=lbc)

        """print entity Info"""
        synonyms = ', '.join(s.getname() for s in enti.getsynonyms())
        parent = enti.getparent()
        if (parent is None):
            parentstr = ''
        else:
            parentstr = href(ref=parent.webanker().anker(), anz=enti.getname(Sprachtext.reportLang()))
        children = ', '.join(
            href(ref=c.webanker().anker(), anz=c.getname(Sprachtext.reportLang())) for c in enti.getchildren())
        infovalues = (nvl(synonyms), parentstr, nvl(children)
                      , entidiag(pentiid=enti.enti_id), nvl(enti.enti_uc) + ', ' + nvl(enti.enti_dc))
        printcontentinfo(ptitle=Sprachtext.transl('Informationen'), pheaders=infoheaders, pvalues=infovalues)

        printattrlist(penti=enti)
        printentikeys(pentiid=enti.enti_id)
        printentirela(pentiid=enti.enti_id)
        printreflist(pelemid=enti.enti_id, pelemtype=Modelelemtype.ENTI)
        printtransl(pentiid=enti.enti_id)
        printentiudp(pentiid=enti.enti_id)
        printmapping(pentiid=enti.enti_id)

        printcontentend(lbc)
    # for


# printcontententi

def printcontentattr():
    infoheaders = (
        Sprachtext.transl('Technischer Name'), Sprachtext.transl('Domain'), Sprachtext.transl('Datentyp'),
        Sprachtext.transl('Tooltip')
        , Sprachtext.transl('geändert'))
    flagheaders = (
        Sprachtext.transl('Pflichtattribut'), Sprachtext.transl('Schlüssel'), Sprachtext.transl('Deskriptor'),
        Sprachtext.transl('übersetzt')
        , Sprachtext.transl('historisiert'), Sprachtext.transl('wiederholt'), Sprachtext.transl('verschlüsselt'))

    for attr in Attribute.select(porderby='attr_displ_name'):
        printcontentstart('attributes')
        enti = attr.getparent()
        if enti is not None:
            master = "<p1>{}: {}</p1><br>" \
                .format(Sprachtext.transl('Entität'), href(ref=enti.webanker().anker(), anz=enti.getname()))
        else:
            master = 'Relation tbd'

        lbc = str(newbarcounter())
        printcontent(ptype=Sprachtext.transl('Attribute')
                     , panker=attr.webanker().anker()
                     , pname=attr.attr_displ_name
                     , pmaster=master
                     , pdescr=lf2htmlbr(nvl(attr.attr_descr))
                     , plbc=lbc)
        domain = attr.getdomain()
        domainref = domain.getname(Sprachtext.reportLang()) \
            if domain.isderived() \
            else href(ref=domain.webanker().anker(), anz=domain.getname(Sprachtext.reportLang()))
        infovalues = (nvl(attr.attr_tech_name, ''), domainref, domain.displdatatype()
                      , nvl(attr.attr_tooltip, ''), re.sub(r'^, $', '', nvl(attr.attr_uc) + ', ' + nvl(attr.attr_dc)))
        printcontentinfo(ptitle=Sprachtext.transl('Informationen'), pheaders=infoheaders, pvalues=infovalues)

        flagvalues = (bool2icon(attr.attr_is_mandatory), bool2icon(attr.isinkey()), bool2icon(attr.attr_is_descriptive)
                      , bool2icon(attr.attr_is_translated)
                      , bool2icon(attr.attr_is_historicised), bool2icon(attr.attr_is_repeated),
                      bool2icon(attr.attr_is_encrypted))
        printflagline(pheaders=flagheaders, pvalues=flagvalues)

        printreflist(pelemid=attr.attr_id, pelemtype='ATTR')
        printtransl(pattrid=attr.attr_id)
        printattrudp(pattrid=attr.attr_id)
        printmapping(pattrid=attr.attr_id)
        printcontentend(lbc)
    # for


# printcontentattr

def printreflist(pelemid, pelemtype):
    if (pelemtype == 'DOKU'):
        refentries = web_sql.dokureflist(pid=pelemid, plang=Sprachtext.reportLang())
    elif (pelemtype in ('TABL', 'INTF')):
        # indirekte auch anzeigen.
        refentries = web_sql.refdokulist(pid=pelemid, pelemtype=pelemtype)
    else:
        refentries = web_sql.refdokulist(pid=pelemid, pelemtype=pelemtype)
    # fi
    if (refentries is None or len(refentries) == 0): return

    fhtml.write(starttable(ptitel=Sprachtext.transl('Referenziert von')
                           , pueberschriften=[Sprachtext.transl('Typ'), Sprachtext.transl('Elemente')]))

    curtype = ''  # Annahme: Dokumentenliste ist sortiert nach typ und Name
    kinder = ''
    for refentry in refentries:
        htmlname = ''
        anker = None
        if (pelemtype in ('DOKU', 'ENTI', 'ATTR', 'DOMA')):
            if (refentry.elemtype == 'TABL'):
                # Tabellen sind in schn-file
                tabl = Tabelle().getbyid(refentry.elemid)
                htmlname = htmlfilelist[tabl.tabl_schn_id]
            elif (refentry.elemtype == 'INTF'):
                htmlname = htmlfilelist[refentry.elemid]
                anker = ''  # Schnittstellen haben keinen Anker ausser dem Namen
            # fi
        elif (pelemtype in ('TABL', 'INTF', 'INTF')):  # aus schn-html zurück ins Main
            if (refentry.elemtype in ('ENTI', 'ATTR', 'DOMA', 'DOKU')):
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


def printwrtbattrlist(pwrtbid, wrtgruppe=False):
    alist = web_sql.namelist(ptype='ATTG' if wrtgruppe else 'ATTR'
                             , plang=Sprachtext.reportLang(), pid=pwrtbid)
    if (len(alist) == 0):
        return
    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Verwendet in Attributgruppen' if wrtgruppe
                                                   else 'Verwendet für Attribute')
                          , pueberschriften=[Sprachtext.transl('Attributgruppe' if wrtgruppe
                                                               else 'Attribute')]
                          , pwerteliste=[[href(ref=a[1], anz=a[0])] for a in alist]))


def printwrtbcollist(pwrtbid):
    clist = Schnittstelleattr.select(pwhere='scha_wrtb_id = {}'.format(pwrtbid))
    if (len(clist) == 0):
        return
    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Verwendet für Columns')
                          , pueberschriften=[Sprachtext.transl('Column')]
                          , pwerteliste=[[href(ref=col.webanker().anker()
                                               , anz="{} ({}:{})".format(col.scha_column_name, col.getintfname(),
                                                                         col.gettablname())
                                               , htmlfile=htmlfilelist[col.getintfid()]
                                               )
                                          ] for col in clist
                                         ]))


def printwrtbmembers(pwrtbid):
    elems = web_sql.wbgrelements(wrtbid=pwrtbid)
    if (len(elems) == 0):
        return
    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Elemente')
                          , pueberschriften=
                          [Sprachtext.transl('Element')
                              , Sprachtext.transl('Beschreibung')
                              , Sprachtext.transl('Domain')
                              , Sprachtext.transl('geändert')
                           ]
                          , pwerteliste=[[e[0], e[1]
                                             , href(ref=web_sql.wrtbAnker(e[9])
                                                    , anz=e[2] + ' (' + Domain.anzdatentyp(e[3]) + ')')
                                             , e[5] + ' , ' + e[6]] for e in elems]))


# printwrtbmembers

def printwertelist(pwrtb):
    wlist = Vorgabewert.select(pwhere="vgwt_wrtb_id= {}".format(pwrtb.wrtb_id))
    if (len(wlist) == 0):
        return
    wlist = [(w.vgwt_sortrhfg,w.vgwt_wert,w.vgwt_anzeige,w.vgwt_beschr) for w in wlist]
    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Werteliste')
                          , pueberschriften=(
                            Sprachtext.transl('Nr'), Sprachtext.transl('Wert')
                            , Sprachtext.transl('Anzeige'), Sprachtext.transl('Beschreibung')
                            )
                          , pheadlevel=3
                          , pwerteliste=wlist)
                        )


# printwertelist

def printcontentwrtb(plist):
    printcontentstart('domains')
    for w in plist:
        wrtb_name = w.getname(Sprachtext.reportLang())

        lbc = str(newbarcounter())
        printcontent(ptype=Sprachtext.transl('Domain')
                     , panker=w.webanker().anker()
                     , pname=wrtb_name
                     , pdescr=lf2htmlbr(nvl(w.wrtb_beschr))
                     , plbc=lbc)

        if (w.wrtb_typ in (Domain.TEXT, Domain.LOV)):
            infoheaders = (
                Sprachtext.transl('Datentyp'), Sprachtext.transl('Max. Länge'), Sprachtext.transl('Syntaxregel'),
                Sprachtext.transl('geändert'))
            infovalues = (
                nvl(Domain.anzdatentyp(w.wrtb_typ)), nvl(w.wrtb_text_maxlng), nvl(w.wrtb_text_syntaxregel),
                nvl(w.wrtb_uc) + ',' + nvl(w.wrtb_dc))
        elif (w.wrtb_typ == Domain.BIN):
            infoheaders = (Sprachtext.transl('Datentyp'), Sprachtext.transl('Inhaltstyp'), Sprachtext.transl('Format'),
                           Sprachtext.transl('geändert'))
            infovalues = (
                nvl(Domain.anzdatentyp(w.wrtb_typ)), Domain.displcontenttype(nvl(w.wrtb_bin_inhalttyp)),
                nvl(w.wrtb_bin_spfo_id), nvl(w.wrtb_uc) + ',' + nvl(w.wrtb_dc))
        elif (w.wrtb_typ == Domain.GRP):
            infoheaders = (Sprachtext.transl('Datentyp'), Sprachtext.transl('geändert'))
            infovalues = (Domain.anzdatentyp(w.wrtb_typ), nvl(w.wrtb_uc) + ',' + nvl(w.wrtb_dc))
        elif (w.wrtb_typ == Domain.NUM):
            infoheaders = (
                Sprachtext.transl('Datentyp'), Sprachtext.transl('Vorkommast.'), Sprachtext.transl('Nachkommast.')
                , Sprachtext.transl('Rundungseinh.'), Sprachtext.transl('Einheit'), Sprachtext.transl('Min. Wert'),
                Sprachtext.transl('Max. Wwert')
                , Sprachtext.transl('geändert'))
            infovalues = (
                nvl(Domain.anzdatentyp(w.wrtb_typ)), nvl(w.wrtb_num_vorkstellen), nvl(w.wrtb_num_nachkstellen),
                nvl(w.wrtb_num_rundng_einh), nvl(w.wrtb_num_pheh_id)
                , nvl(w.wrtb_num_minwert), nvl(w.wrtb_num_maxwert)
                , nvl(w.wrtb_uc) + ',' + nvl(w.wrtb_dc))
        elif (w.wrtb_typ == Domain.ZPKT):
            infoheaders = (
                Sprachtext.transl('Datentyp'), Sprachtext.transl('Min. Wert'), Sprachtext.transl('Max. Wwert'),
                Sprachtext.transl('Granularität')
                , Sprachtext.transl('geändert'))
            infovalues = (nvl(Domain.anzdatentyp(w.wrtb_typ)), nvl(w.wrtb_zpkt_minwert), nvl(w.wrtb_zpkt_maxwert),
                          Domain.displgranul(nvl(w.wrtb_zpkt_granularitaet)), nvl(w.wrtb_uc) + ',' + nvl(w.wrtb_dc))
        else:
            infoheaders, infovalues = None, None
        # fi
        if infoheaders is not None: printcontentinfo(ptitle=Sprachtext.transl('Informationen'), pheaders=infoheaders,
                                                     pvalues=infovalues)

        if (w.wrtb_typ == 'LOV'):
            printwertelist(pwrtb=w)

        if (w.wrtb_typ == 'GRP'):
            printwrtbmembers(pwrtbid=w.wrtb_id)

        printwrtbattrlist(pwrtbid=w.wrtb_id, wrtgruppe=False)
        printwrtbattrlist(pwrtbid=w.wrtb_id, wrtgruppe=True)
        printwrtbcollist(pwrtbid=w.wrtb_id)

        printcontentend(lbc)  # for


# printcontentwrtb

def printcontentdoku(plist):
    """
    #            select child.DOKU_ID,child.DOKU_NAME,child.DOKU_FORMAT,child.DOKU_REFERENZ
    #             ,parent.DOKU_ID parent_id ,parent.doku_name parent_name
    #             ,(select group_concat(grandchild.doku_id||':'||grandchild.doku_name, '|') kinder
    #                from DOKUMENTE grandchild
    #                where grandchild.DOKU_DOKU_ID = child.DOKU_ID) kinder
    #            from DOKUMENTE child
    #            left join dokumente parent on parent.DOKU_ID = child.DOKU_DOKU_ID
    #            order by upper(child.doku_name)
    #            """
    printcontentstart('documents')
    infoheaders = (Sprachtext.transl('Format'), Sprachtext.transl('Referenz'), Sprachtext.transl('Vaterdokument')
                   , Sprachtext.transl('Unterdokumente'))
    for doc in plist:
        lbc = str(newbarcounter())
        doku_id = doc.doku_id
        parent = doc.getparent()
        children = doc.getchildren()
        printcontent(ptype=Sprachtext.transl('Document')
                     , panker=doc.webanker().anker()
                     , pname=doc.doku_name
                     , pdescr=""
                     , plbc=lbc)

        """DOKU_ID,DOKU_NAME,DOKU_FORMAT,DOKU_REFERENZ
            ,parent_id, parent_name, kinder"""
        #        kinder = ''
        #        if children is not None:
        #            for child in children:
        #                kinder += href(ref=child.webanker.anker(),anz=child.doku_name) + ', '
        #            #for
        #            kinder = kinder.rstrip(', ')
        #        #fi
        if children is None:
            kinder = ''
        else:
            kinder = ', '.join(href(ref=child.webanker().anker(), anz=child.doku_name) for child in children)
        # fi

        infovalues = (nvl(doc.doku_format), nvl(doc.doku_referenz),
                      '' if parent is None else href(ref=parent.webanker().anker(), anz=nvl(parent.doku_name))
                      , kinder)
        printcontentinfo(ptitle=Sprachtext.transl('Informationen'), pheaders=infoheaders, pvalues=infovalues)

        printreflist(pelemid=doku_id, pelemtype='DOKU')

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

    webDirectory = p_webdirec if (p_webdirec is not None) else parameters.webDirec();
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
    elif pattrname in ['ENTI_SYNONYM']:
        return Sprachtext.transl('Synonym')
    else:
        return pattrname
    # fi


def findtransl(pattr, pmodeid, plangs):
    tl = [attname2element(pattr)]
    for l in plangs:
        eintrag = web_sql.transltext(pattr=pattr, pmodeid=pmodeid, plang=l)
        if (pattr in ('ENTI_NAME', 'ATTR_NAME')):
            id = web_sql.elementid(pmodeid=pmodeid, ptyp=pattr[0:4])
            eintrag = filehref(ref=web_sql.entiAnker(id) if pattr == 'ENTI_NAME'
            else web_sql.attrAnker(id)
                               , anz=eintrag, plang=l)
        # fi
        tl.extend([eintrag])
    return tl


def printtransl(pentiid=None, pattrid=None):
    langs = projekt.projektlangs().split(',')
    try:
        langs.remove(Sprachtext.reportLang())
    except:
        pass
    if len(langs) == 0: return
    head = [Sprachtext.transl('Element')]
    head.extend(langs)
    if (pentiid is not None):
        modeid = Modelelement.getidbyelemid(pentiid=pentiid)
        transllist = [findtransl(pattr='ENTI_NAME', pmodeid=modeid, plangs=langs)
            , findtransl(pattr='ENTI_SYNONYM', pmodeid=modeid, plangs=langs)
            , findtransl(pattr='ENTI_COMMENT', pmodeid=modeid, plangs=langs)]
    elif (pattrid is not None):
        modeid = Modelelement.getidbyelemid(pattrid=pattrid)
        transllist = [findtransl(pattr='ATTR_NAME', pmodeid=modeid, plangs=langs)
            , findtransl(pattr='ATTR_COMMENT', pmodeid=modeid, plangs=langs)]
    # print(transllist)
    fhtml.write(tablehtml(ptitel=Sprachtext.transl('Übersetzungen')
                          , pueberschriften=head
                          , pheadlevel=2
                          , pwerteliste=transllist))
    # fhtml.write(starttable(ptitel=Sprachtext.transl('Übersetzungen')
    #                       , pueberschriften=head
    #                       , pheadlevel= 2))
    # for d in transllist:
    #    fhtml.write(writetableline(pwerte=d))
    # fhtml.write(endtable())
# printtransl
