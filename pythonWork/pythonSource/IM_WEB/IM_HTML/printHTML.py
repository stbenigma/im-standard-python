import os
import re
import shutil
from distutils.dir_util import copy_tree

from SSOT_infra import parameters
from IM_OBJECTS import *
import html
from IM_JSON import JSModel

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

fhtml = None


def filehref(pref, panz, plang, pself=False,pimg=None):
    img =  parameters.nvl2(pimg, '', '<img class="icon-check" src="icons/{}">'.format(pimg))
    return """<a href="{}{}" target="_{}" >{}{}</a>""" \
        .format(webFileName + '_' + plang.lower() + '.html', parameters.nvl2(pref, "", "#"), 'self' if pself else 'blank', panz, img)


def href(ref, anz, htmlfile='',pself=False):
    if anz is None: return ''
    sep = '#' if parameters.nvl(ref) != '' else ''
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

def iconsrc(pjsenti,pdefaultlang):
    icon = pjsenti["icon"]
    if icon['type']== 'FYAYCICON':
        filename = ''  #to be resolved
    elif icon['type']== 'URL':
        return icon['reference']
    elif icon['type']== 'FILE':
        filename = icon['reference']
    else:
        """look for entityname in defaultlanguage"""
        filename = pjsenti["name"][pdefaultlang]
        filename = re.sub(r'[^a-zäöüñéàè0-9_-]+', '', filename.lower())
    #fi
    #filename found search in image
    if os.path.isfile(filename):
        #absolute path, return it
        return filename

    #search for filename with extensions in image directory
    for ext in ('png','jpg','jpeg','gif'):
        fullfilename = "{}/{}.{}".format('image',filename,ext).lower()
        if os.path.isfile(parameters.webDirec() + fullfilename):
            return fullfilename
    return ''

def origindomains(pintfid):
    #dict of domain with origin DOMAIN and defined in interface intfid (or im if None)
    return {key: value for key, value in getmodel().jsmodel['domains'].items()
                                                if (value['origin'] == Domain.DOMAIN
                                                and value['interface-id'] == pintfid)}


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

def searchlogo(p_imagedirec):
    retval = ''
    for ext in ('png', 'jpg', 'svg'):
        if os.path.isfile(p_imagedirec + 'logo.' + ext): retval = 'logo.' + ext
    return retval

def setWebDirec(p_webdirec):
    global webDirectory, webFileName, webFileNamePath
    global libSourceDirec, imagedirec, cssdirec, icondirec,jsdirec,jinadirec

    webDirectory = parameters.nvl(p_webdirec, parameters.webDirec());
    webFileName = parameters.modelName();
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
    return

def copyimages():
    global imagedirec
    """copy all file from the modeler-image directory into the web-image directory"""
    if os.path.exists(parameters.odmFilesDirec() + 'images'):
        copy_tree(parameters.odmFilesDirec() + 'images', imagedirec)
    return

def createFile(pfilename):
    global fhtml
    webfile = webDirectory + pfilename
    if os.path.exists(webfile):
        os.remove(webfile)
    fhtml = open(webfile, 'w')
    return


# createFile
def closefile():
    global fhtml
    fhtml.close()
    return

