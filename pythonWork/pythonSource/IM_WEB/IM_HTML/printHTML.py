import html
import os
import re
import logging
import shutil
from distutils.dir_util import copy_tree
from pathlib import Path

from SSOT_db.IM_JSON import JSModel
from SSOT_db.IM_OBJECTS import Modelelemtype, Domain
from SSOT_infra import parameters, nvl2, nvl, transl


def no_hyperlink(element: dict) -> (str or None):
    return None


class HTMLExport:

    def __init__(self):
        self.outputDirectory: str = None
        self.webDirectory: str = ""
        self.webFileName: str = ""
        self.webFileNamePath: str = ""
        self.libSourceDirec: str = ""
        self.imagedirec: str = ""
        self.cssdirec: str = ""
        self.icondirec: str = ""
        self.jsdirec: str = ""
        self.jinadirec: str = ""
        self.htmlfilelist = {}
        self.model: JSModel = None

        """zum Zählen der lokalen Ziele für collapse"""
        self.barcounter = 0
        self.fhtml = None
        self.custom_hyperlink_extractor = no_hyperlink

    def getelement(self, js_element_id: str):
        return self.model.getbyid(js_element_id)

    def setmodel(self, pmodel: JSModel):
        self.model = pmodel

    def getmodel(self):
        return self.model

    def filehref(self, pref, panz, plang, pself=False, pimg=None):
        img = nvl2(pimg, '', '<img class="icon-check" src="icons/{}">'.format(pimg))
        return """<a href="{}{}" target="_{}" >{}{}</a>""" \
            .format(self.webFileName + '_' + plang.lower() + '.html', nvl2(pref, "", "#"), 'self' if pself else 'blank',
                    panz,
                    img)

    def custom_hyperlink(self, element: dict) -> None or str:
        result = self.custom_hyperlink_extractor(element)
        if result is not None:
            logging.warning(f"Using {result} for element {element}")
        return result

    def href(self, ref, anz, htmlfile='', pself=False):

        # if there is a custom hyperlink, use it with priority
        element = self.getelement(ref)
        custom_hyperlink_value = self.custom_hyperlink(element)
        if custom_hyperlink_value is not None and len(custom_hyperlink_value) > 0:
            logging.debug(f"Applying custom hyperlink on element {ref} '{anz}' {custom_hyperlink_value}")
            return f"""<a href="{html.escape(custom_hyperlink_value)}">{html.escape(anz)}</a>"""

        if anz is None:
            return ''
        sep = '#' if nvl(ref) != '' else ''
        return """<a href="{}{}{}" target="{}">{}</a>""".format(htmlfile, sep, ref,
                                                                '_self' if ((htmlfile == '') or pself) else '_blank',
                                                                html.escape(anz))

    def isIconstr(self, w):
        if (w is None) or (type(w) != str):
            return False
        elif (w.startswith('class="')):
            return True
        else:
            return False

    def iconsrc(self, pjsenti, pdefaultlang):
        icon = pjsenti["icon"]
        if icon['type'] == 'FYAYCICON':
            filename = ''  # to be resolved
        elif icon['type'] == 'URL':
            return icon['reference']
        elif icon['type'] == 'FILE':
            filename = icon['reference']
        else:
            """look for entityname in defaultlanguage"""
            filename = pjsenti["name"][pdefaultlang]
            filename = re.sub(r'[^a-zäöüñéàè0-9_-]+', '', filename.lower())
        # fi
        # filename found search in image
        filepath = os.path.join(parameters.webDirec(), 'image', filename)
        if os.path.isfile(filepath):
            # absolute path, return it
            return filepath

        # search for filename with extensions in image directory
        for ext in ('png', 'jpg', 'jpeg', 'gif'):
            fullfilepath = "{}.{}".format(filepath, ext).lower()
            if os.path.isfile(fullfilepath):
                return fullfilepath
        return ''

    def origindomains(self, pintfid):
        # dict of domain with origin DOMAIN and defined in interface intfid (or im if None)
        return {key: value for key, value in self.getmodel().jsmodel['domains'].items()
                if (value['origin'] == Domain.DOMAIN
                    and value['interface-id'] == pintfid)}

    def type2name(self, ptyp, plang=None):
        if ptyp == Modelelemtype.ENTI:
            return transl('Entität', plang)
        elif ptyp == Modelelemtype.ATTR:
            return transl('Attribut', plang)
        elif ptyp == Modelelemtype.DOMA:
            return transl('Wertebereich', plang)
        elif ptyp == Modelelemtype.DIAG:
            return transl('Diagramm', plang)
        elif ptyp == Modelelemtype.TABL:
            return transl('Tabelle', plang)
        elif ptyp == Modelelemtype.DOCU:
            return transl('Dokument', plang)
        elif ptyp == Modelelemtype.ORGU:
            return transl('Organisatioseinheit', plang)
        elif ptyp == Modelelemtype.INTF:
            return transl('System', plang)
        elif ptyp == Modelelemtype.COLU:
            return transl('Column', plang)
        else:
            return ptyp
        # fi

    def searchlogo(self, p_imagedirec):
        retval = ''
        for ext in ('png', 'jpg', 'svg'):
            if os.path.isfile(os.path.join (p_imagedirec , 'logo.' + ext)):
                retval = 'logo.' + ext
        return retval

    def setWebDirec(self, p_webdirec):

        self.webDirectory = Path(nvl(p_webdirec, parameters.webDirec()))
        self.webFileName = parameters.modelName()
        self.imagedirec = os.path.join(self.webDirectory, 'image')
        self.cssdirec = os.path.join(self.webDirectory, 'css')
        self.icondirec = os.path.join(self.webDirectory, 'icons')
        self.jsdirec = os.path.join(self.webDirectory, 'js')
        self.jinadirec = os.path.join(self.webDirectory, 'jinjatemplates')

        this_file = Path(__file__)
        lib_path_tokens = this_file.parts[:-2]
        self.libSourceDirec = os.path.join(*lib_path_tokens, 'html-lib')
        assert os.path.exists(self.libSourceDirec), f"Unable to find {self.libSourceDirec}"
        if (parameters.logoFileName() is None):
            parameters.logoFileName(self.searchlogo(self.imagedirec))

    def createlib(self):
        if not os.path.exists(self.cssdirec):
            shutil.copytree(os.path.join(self.libSourceDirec, 'css'), self.cssdirec)
        if not os.path.exists(self.jsdirec):
            shutil.copytree(os.path.join(self.libSourceDirec, 'js'), self.jsdirec)
        if not os.path.exists(self.icondirec):
            shutil.copytree(os.path.join(self.libSourceDirec, 'icons'), self.icondirec)
        if not os.path.exists(self.imagedirec):
            shutil.copytree(os.path.join(self.libSourceDirec, 'image'), self.imagedirec)
        if not os.path.exists(self.jinadirec):
            shutil.copytree(os.path.join(self.libSourceDirec, 'jinjatemplates'), self.jinadirec)
        return

    def copyimages(self):
        """copy all file from the modeler-image directory into the web-image directory"""
        image_src = parameters.odmFilesDirec() + 'images'
        if os.path.exists(image_src):
            copy_tree(image_src, self.imagedirec)

    def createFile(self, pfilename: Path):
        webfile = os.path.join(self.webDirectory, pfilename)
        if os.path.exists(webfile):
            os.remove(webfile)
        self.fhtml = open(webfile, 'w')
        return self.fhtml

    def closefile(self):
        self.fhtml.close()
