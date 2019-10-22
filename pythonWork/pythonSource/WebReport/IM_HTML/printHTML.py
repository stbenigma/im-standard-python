from IM_ODM import odmParam
import os,shutil

outputDirectory:str = None
webDirectory:str = "";
webFileName:str = "";
detailDirectory:str = "";
webFileNameSpec:str = "";
tocFileName:str = "";
contFileName:str = "";
indexFileName:str = "";
libSourceDirec:str = "";

headIndex:str ="""<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>{}</title>
</head>
<frameset cols="20%,80%">
<frame name="toc" src="{}.html">
<frame name="details" src="{}.html"></frameset>
</html>
"""
headToc:str ="""<html xmlns="http://www.w3.org/1999/xhtml">
	<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/></head>
	<link rel="stylesheet" type="text/css" href="./css/osddm_main.css">
	<link rel="stylesheet" type="text/css" href="./css/osddm_vs.css">
	<link rel="stylesheet" type="text/css" href="./css/osddm_toc_tree.css">

	<script src="./js/toc_filter.js"></script>
	<body>
				<div class="t_item">
		<div id="toc_list">
		<table id="toc_table" width="100%" style="empty-cells:show; font-family:Tahoma; font-size:small; text-align:left; vertical-align:top; word-wrap:break-word;">
<tr><td style="color:navy; font-family:Tahoma; font-size:small; font-style:italic; font-weight:bold;"><input type="text" style="width: 180px; margin-top: 5px;" onkeyup="$d_Find('toc_list',this.value,'a')"/></td></tr>
<tr><td>&nbsp;</td></tr>
</table>
"""
headCont:str ="""<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> 
<html>
<head>
	<META http-equiv="Content-Type" content="text/html; charset=UTF-8"> <title></title>
		<meta name="generator" content="Altova StyleVision Enterprise Edition 2 014 (x64) (http://www.altova.com)">
		<meta http-equiv="X-UA-Compatible" content="IE=7">
		<link rel="stylesheet" type="text/css" href="css/osddm_main.css">
		<link rel="stylesheet" type="text/css" href="css/osddm_vs.css">
<!--[if IE]><STYLE type="text/css">.altova-rotate-left-textbox{{filter: progid:DXImageTransform.Microsoft.BasicImage(rotation=3)}}.altova-rotate-right-textbox{{filter: progid:DXImageTransform.Microsoft.BasicImage(rotation=1)}}</STYLE><![endif]--><!--[if !IE]><!-->
<style type="text/css">.altova-rotate-left-textbox{{-webkit-transform: rotate(-90deg) translate(-100%, 0%); -webkit-transform-origin: 0% 0%;-moz-transform: rotate(-90deg)
translate(-100%, 0%); -moz-transform-origin: 0% 0%;-ms-transform: rotate(-90deg) translate(-100%, 0%); -ms-transform-origin: 0%
0%;}}.altova-rotate-right-textbox{{-webkit-transform: rotate(90deg) translate(0%, -100%); -webkit-transform-origin: 0% 0%;-moz-transform: rotate(90deg) translate(0%,
-100%); -moz-transform-origin: 0% 0%;-ms-transform: rotate(90deg) translate(0%, -100%); -ms-transform-origin: 0% 0%;}}</style><!--<![endif]--><style
type="text/css">@page {{ margin-left:2cm; margin-right:2cm; margin-top:2cm; margin-bottom:2cm }}@media print {{ br.altova-page-break {{ page-break-before: always; }}
</style>
</head>
<body style="font-family:Tahoma; font-size:xx-small; ">
	<br><center><span class="caption">{}</span></center>
	<p></p>
"""
ftoc = None
fcont = None


def setWebDirec(pwebDirec, pbaseDirec):
    global webDirectory ,webFileName,detailDirectory,webFileNameSpec,tocFileName
    global contFileName, indexFileName
    global libSourceDirec

    if (pwebDirec is None):
        if (not os.path.exists(pbaseDirec+"Web")):
            os.mkdir(pbaseDirec+"Web");
        #fi
        webDirectory = pbaseDirec+"Web/";
    else:
        webDirectory = webDirec;
    #fi
    webFileName = odmParam.imModelName;
    detailDirectory = webDirectory + webFileName + "/";
    webFileNameSpec = webFileName + '.html';
    tocFileName = webFileName + '_toc';
    contFileName = webFileName + '_cont';
    indexFileName = webDirectory + webFileNameSpec;
    libSourceDirec = os.path.dirname(os.path.abspath(__file__))+'/../';
# setWebDirec


def createIndex(title):
    global ftoc,fcont

    if os.path.exists(indexFileName):
        os.remove(indexFileName)
    if os.path.exists(detailDirectory):
        shutil.rmtree(detailDirectory)

    os.mkdir(detailDirectory)
    for loc in ['js','css','img']:
        shutil.copytree(libSourceDirec+'html-lib/'+loc,detailDirectory+loc)

    f = open(indexFileName,'w')
    f.write(headIndex .format(title,webFileName+'/'+tocFileName,webFileName+'/'+contFileName))
    f.close()

    ftoc = open(detailDirectory+tocFileName+'.html','w')
    ftoc.write(headToc)

    fcont = open(detailDirectory+contFileName+'.html','w')
    fcont.write(headCont .format(title))

#createIndex

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
