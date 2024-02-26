import html
import logging
import os
import re
import shutil
from distutils.dir_util import copy_tree
from pathlib import Path

from IM_WEB.htmlparameters import HTMLParameter
from SSOT_db.IM_JSON import JSModel
from SSOT_db.IM_OBJECTS import Modelelemtype, Domain
from SSOT_infra import nvl2, nvl, transl


def no_hyperlink(element: dict) -> (str or None):
    return None


class HTMLExport(HTMLParameter):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.outputDirectory: str = None
        self._htmlfilelist = nvl(kwargs.get("htmlfilelist"), dict())
        self._model: JSModel = None
        self._startdiagram = kwargs.get("startdiagram")

        """zum Zählen der lokalen Ziele für collapse"""
        self.barcounter = 0
        self.fhtml = None
        self.custom_hyperlink_extractor = no_hyperlink

    @classmethod
    def safe_filename(cls, path: str) -> str:
        return path.replace('/', '-').replace(' - ', '-')

    @property
    def htmlfilelist(self):
        return self._htmlfilelist

    @htmlfilelist.setter
    def htmlfilelist(self, newval):
        self._htmlfilelist = newval

    @property
    def startdiagram(self):
        return self._startdiagram

    @startdiagram.setter
    def startdiagram(self, value):
        self._startdiagram = value

    def getelement(self, js_element_id: str):
        return self.model.getbyid(js_element_id)

    def getmodel(self):
        return(self.model)

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model: JSModel):
        self._model = model

    def _langpart(self, lang):
        return '' if ((nvl(lang, '') == '') or (len(self.languages()) == 1)) \
            else f"_{lang.lower()}"

    def _webfileend(self, lang) -> str:
        return f"{self._langpart(lang)}.{self.webFileExtension}"

    def modellangs(self):
        if self.model == None:
            retval = []
        else:
            retval = list(self.model.jsmodel["languages"].keys())
        return retval

    def fullwebfilename(self, pfilename, plang=None):
        if pfilename == '':
            return pfilename  # empty filename needs no appendix
        else:
            return pfilename + self._webfileend(plang)

    def ataghref(self, phref, pdispl, ptarget='', pimg=None):
        img = nvl2(pimg, '', f'<img class="icon-check" src="icons/{pimg}">')

        return f"""<a href="{phref}" {ptarget}>{pdispl}{img}</a>"""

    def custom_hyperlink(self, element: dict) -> None or str:
        result = self.custom_hyperlink_extractor(element)
        if result is not None:
            result = result.strip()
            logging.debug(f"Using UDP value {result} for jselement {element} hyperlink")
        return result

    def href(self, filename, destid=None):
        anker = lambda destid: '' if destid is None else f"#{destid}"
        return f"{filename}{anker(destid)}"

    # def elementhref(self, elementid, displ, htmlfile='', pself=False):
    #     # if there is a custom hyperlink, use it with priority
    #     jselement = self.getelement(elementid)
    #     custom_hyperlink_value = self.custom_hyperlink(jselement)
    #     if custom_hyperlink_value is not None and len(custom_hyperlink_value) > 0:
    #         logging.debug(f"Applying custom hyperlink on jselement {jselement} '{displ}' {custom_hyperlink_value}")
    #         return self.ataghref(phref=html.escape(custom_hyperlink_value),
    #                              pdispl=displ)
    #
    #     if displ is None:
    #         return ''
    #     return self.ataghref(phref=self.href(filename=htmlfile,destid=elementid),
    #                          ptarget='target="{}"'.format('_self' if ((htmlfile == '') or pself) else '_blank'),
    #                          pdispl=html.escape(displ))


    def getreffilename(self, destid,
                       curdatmid=0, destdatmid=0,
                       desttype=None, destlang=None,
                       basedirec='', curlang=''):
        destfilename = self.fullwebfilename(self.htmlfilelist[destdatmid])
        # fi

        if self.singlefile:
            retval = ''
            if desttype in ('model',):
                if not (curdatmid == destdatmid and destlang in (curlang, '',None)):
                  retval = f"{basedirec}{destlang}/{destfilename}"
            elif desttype in ('datamodels', 'tables', 'columns'):
                if not (curdatmid == destdatmid):
                    retval = basedirec  + destfilename
            else:
                if not (curdatmid == destdatmid and destlang in (curlang, '',None)) :
                    retval = f"{basedirec}{destlang}/{destfilename}"
            # fi
            #append destid to jump within index or current file
            retval = retval + ("" if destid is None else f"#{destid}")
        else:
            # multiplefile framework
            if desttype in ('model',):
                retval = f"{basedirec}{destlang}/{destfilename}"
            elif desttype in ('datamodels', 'tables', 'columns'):
                if curdatmid == destdatmid :
                    retval = ''
                else:
                    retval= basedirec + destfilename
                retval = retval + ("" if destid is None else f"#{destid}")
            else:
                retval = f"{basedirec}{nvl(destlang,curlang)}/elements/{desttype}/{self.fullwebfilename(destid)}"
            # fi
        # fi
        return retval

    def gettarget(self,desttype,curdatmid=0,destdatmid=0):
        if self.singlefile:
            if (curdatmid != destdatmid):
                # different datamodels: new tab in browser
                target = '_blank'
            else:
                target = '_self'  # same tab
        else:
            if desttype in ("model","datamodels","tables","columns"):
                target = '_self'  # same tab
            else:
                target = 'contentIframe'  # use my contentframe
        return f'target="{target}"'

    def getreflink(self, name, destid,
                   curdatmid=0, destdatmid=0,
                   curlang='', destlang=None,
                   desttype=None, basedirec=''):
        #assert destdatmid is not None, "destdatmid must be set"
        if destdatmid == 0:
            # go to information model page
            destlang = nvl(destlang, curlang)
        else:
            # go to datamodels pages
            destlang = ''  # datamodels files are not language dependent
            if desttype == 'datamodels':
                destid = None  # no anker for datamodelfiles
        # fi

        filename= self.getreffilename(destid=destid,
                                      curdatmid=curdatmid, destdatmid=destdatmid,
                                      desttype=desttype, destlang=destlang,
                                      basedirec=basedirec, curlang=curlang)
        try:
            retval = self.ataghref(phref=filename, pdispl=name,
                                   ptarget=self.gettarget(curdatmid=curdatmid,
                                                          destdatmid=destdatmid,
                                                          desttype=desttype))
        except Exception as err:
            logging.warning(f"Cannot format link to {destid}")
            raise err
            retval = ""

        return retval

    def isIconstr(self, w):
        if (w is None) or (type(w) != str):
            return False
        elif (w.startswith('class="')):
            return True
        else:
            return False

    def iconsrc(self, pjsenti, pdefaultlang):
        if pjsenti is None: return ''
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
        filepath = os.path.join(self.imageDirec, filename)
        if os.path.isfile(filepath):
            # absolute path, return it
            return filepath

        # search for filename with extensions in image directory
        for ext in ('png', 'jpg', 'jpeg', 'gif'):
            fullfilepath = "{}.{}".format(filepath, ext).lower()
            if os.path.isfile(fullfilepath):
                return fullfilepath
        return ''

    def origindomains(self, pdatmid):
        # dict of domain with origin DOMAIN and defined in datamodel datmid (or im if None)
        return {key: value for key, value in self.getmodel().jsmodel['domains'].items()
                if (value['origin'] == Domain.DOMAIN
                    and value['datamodel-id'] == pdatmid)}

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
        elif ptyp == Modelelemtype.RELA:
            return transl('Beziehung', plang)
        elif ptyp == Modelelemtype.BURU:
            return transl('Business Rule', plang)
        elif ptyp == Modelelemtype.ORGU:
            return transl('Organisatioseinheit', plang)
        elif ptyp == Modelelemtype.DATM:
            return transl('Datenmodell', plang)
        elif ptyp == Modelelemtype.COLU:
            return transl('Column', plang)
        elif ptyp == Modelelemtype.ACTR:
            return transl('Rolle', plang)
        else:
            return ptyp
        # fi

    def type2elemtype(self, ptyp):
        if ptyp == Modelelemtype.ENTI:
            return 'entities'
        elif ptyp == Modelelemtype.ATTR:
            return 'attributes'
        elif ptyp == Modelelemtype.DOMA:
            return 'domains'
        elif ptyp == Modelelemtype.DIAG:
            return 'diagrams'
        elif ptyp == Modelelemtype.TABL:
            return 'tables'
        elif ptyp == Modelelemtype.DOCU:
            return 'documents'
        elif ptyp == Modelelemtype.RELA:
            return 'relations'
        elif ptyp == Modelelemtype.BURU:
            return 'businessrules'
        elif ptyp == Modelelemtype.ORGU:
            return 'orgunits'
        elif ptyp == Modelelemtype.DATM:
            return 'datamodels'
        elif ptyp == Modelelemtype.COLU:
            return 'columns'
        elif ptyp == Modelelemtype.ACTR:
            return 'actorroles'
        else:
            return ptyp
        # fi

    def replacesvghrefs(self, svg,curlang,basedirec):
        replacetypes = ["ENTI","ATTR"] # needs dest-datm-id but where does it come from,"TABL","COLU"]

        # replace href to entity #ENTInnnn by relative href
        for idtype in replacetypes:
            href = self.getreffilename(curlang=curlang,destlang=curlang,
                                              destid="\\1",
                                              desttype=self.type2elemtype(idtype),
                                              basedirec=basedirec)
            svg = re.sub(r'href="#({idtype}[0-9]+)"'.format(idtype=idtype),
                            r'href="{ref}" {target}'.format(ref=href,
                                                                target=self.gettarget(desttype=self.type2elemtype(idtype))),
                            svg)
        return svg

    def createlib(self):
        if not os.path.exists(self.cssDirec):
            shutil.copytree(os.path.join(self.libSourceDirec, 'css'), self.cssDirec)
        if not os.path.exists(self.jsDirec):
            shutil.copytree(os.path.join(self.libSourceDirec, 'js'), self.jsDirec)
        if not os.path.exists(self.imageDirec):
            shutil.copytree(os.path.join(self.libSourceDirec, 'image'), self.imageDirec)
        if not os.path.exists(self.jinjaDirec):
            shutil.copytree(os.path.join(self.libSourceDirec, 'jinjatemplates'), self.jinjaDirec)
        return

    def copyimages(self):
        """copy all file from the modeler-image directory into the web-image directory"""
        # currently no separate impage directory for originals
        return
        image_src = self.imageDirec
        if os.path.exists(image_src):
            copy_tree(image_src, self.imageDirec)

    def createFile(self, pfilename: Path):
        webfile = os.path.join(self.webDirec, pfilename)
        if os.path.exists(webfile):
            os.remove(webfile)
        self.fhtml = open(webfile, 'w')
        return self.fhtml
