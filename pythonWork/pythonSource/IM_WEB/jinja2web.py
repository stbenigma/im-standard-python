import os
import re
import logging
from datetime import datetime
from pathlib import Path

from jinja2 import FileSystemLoader, Environment
from markdown import markdown

from IM_WEB.IM_HTML import entityenviron, HTMLExport
from SSOT_db.IM_JSON import JSModel, jsguid2type
from SSOT_infra import logmessages,nvl
from SSOT_infra.translateprompt import transl


class Webmodel:

    def __init__(self, export: HTMLExport, pcurlang: str, pdatmid):
        self.curlanguage = pcurlang
        self.jsmodel:JSModel = export.model
        self.datmid = pdatmid
        self.htmlfilelist = export.htmlfilelist
        self.export = export
        self._basedirec = ''

    @property
    def startdiagram(self):
        return self.export.startdiagram


    @property
    def basedirec(self):
        return self._basedirec

    @basedirec.setter
    def basedirec(self, value):
        self._basedirec = value
        return

    def setbasedirec(self,value):
        self.basedirec=value
        return

    def getdatmid(self):
        return self.datmid

    def getmodelname(self):
        return self.jsmodel.jsmodel['model']['name']

    def getsubentyids(self, attrid):
        """get all subentity-ids from subentities inheriting this attribute"""
        entiids = [entikey for entikey, entival in self.jsmodel.getelements("entities").items()
                   if (attrid in entival["inheritedattributes+"])]
        return entiids

    def gethref(self,destid,basedirec,destlang,desttype):
        filename = self.export.getreffilename(destid=destid,desttype=desttype,basedirec=basedirec,destlang=destlang)
        return filename

    def getreflink(self, name, destid,
                   curdatmid=0, destdatmid=0,
                   curlang=None, destlang=None,
                   desttype=None, basedirec=''):
        if curlang is None:
            curlang = self.curlanguage
        retval = self.export.getreflink(name=name, destid=destid,
                                        curdatmid=nvl(curdatmid,self.getdatmid()),
                                        destdatmid=nvl(destdatmid,self.getelemdatmid(destid)),
                                        curlang=curlang, destlang=destlang,
                                        desttype=nvl(desttype,self.elemtype(destid)),
                                        basedirec=basedirec)
        return retval

    def getsubentyrefs(self, attrid, basedirec=''):
        """get all subentity-referencestrings from subentities inheriting this attribute"""
        entiids = self.getsubentyids(attrid)
        entirefs = [self.getreflink(name=self.getlangstr(self.getelem(elemid)["name"]),
                                    destid=elemid, desttype="entities", curlang=self._curlanguage,
                                    basedirec=basedirec)
                    for elemid in entiids]
        return entirefs

    def getelemdatmid(self,elemid):
        elem = self.getelem(elemid)
        retval = 0 #assume IM if no datm is found
        if elem is not None:
            if jsguid2type(elemid) in ["TABL","DOMA"]:
                retval = nvl(elem["datamodel-id"],0)
            elif jsguid2type(elemid) in ["DATM","COLU"]:
                retval = elem["datamodel-id+"]
        #fi
        return retval

    @property
    def curlanguage(self):
        return self._curlanguage

    @curlanguage.setter
    def curlanguage(self, newval):
        self._curlanguage = newval

    def getdeflanguage(self):
        return self.jsmodel.getdefaultlang()

    def getlanguages(self, all=True):
        langs = list(self.jsmodel.jsmodel[JSModel.elemtype2label(JSModel.ELEMTYPE_LANG)].keys())
        if not all:
            langs.remove(self.curlanguage)
        return langs

    def setelements(self, **kwargs):
        for key, val in kwargs.items():
            self.__setattr__(key.lower(), val)

    def gettransltext(self, instr):
        retval = transl(instr)
        return retval

    def getlangstr(self, instr, default=None):
        if type(instr) == dict:
            """assumes instr = {'de':"xxx",'en':"xxy",...}"""
            try:
                retval = instr[default if default is not None else self.curlanguage]
            except:  # chosen language chosen does not exist, take default language
                retval = instr[default if default is not None else self.getdeflanguage()]
        else:
            retval = instr
        # fi
        return retval

    def displelemtype(self, typ):
        return self.export.type2name(ptyp=jsguid2type(typ), plang=self.curlanguage)

    def elemtype(self, elemid):
        return self.export.type2elemtype(ptyp=jsguid2type(elemid))

    def getelem(self, id):
        if self.elemtype(id) == 'diagrams':
            # diagrams have a prerendered svg/pdf structure
            diags = {diag['id']: diag for diag in self.diagrams}
            retval = diags[id]
            #replace lang and filestructure dependent hrefs in svg
            retval["svg"] = self.export.replacesvghrefs(svg=retval["svg"], curlang=self.curlanguage,
                                                        basedirec=self.basedirec+"../../")
        else:
            retval = self.jsmodel.getbyid(id)
        return retval

    def collecttablemappings(self, pelem):
        # name, list of entries mit {webanker:'name'}
        entities = {e: self.getelem(e)['name'][self.curlanguage] for e in pelem['entitiesmapped']}
        relations = {r: self.getelem(r)['name'] for r in pelem['relationsmapped']}
        entities.update(relations)
        allmappings = {"Information Model": ', '.join(self.getreflink(name=name, destid=anker
                                                                      , curdatmid=self.getdatmid(),
                                                                      basedirec=self.basedirec)
                                                      for anker, name in entities.items())}

        for datmanker, datmelem in filter(lambda e : e[0] != pelem['datamodel-id'],
                                          self.jsmodel.getelements(pelemtype='datamodels').items()):
            #replaced with filter if datmanker == pelem['datamodel-id']: continue
            tablist = []
            for enti in pelem['entitiesmapped'] + pelem['relationsmapped']:
                elem = self.getelem(enti)['tablesmapped+']
                if datmanker in elem:
                    tablist += elem[datmanker]
            if len(tablist) == 0: continue
            tablist = list(set(tablist))
            allmappings[datmelem["name"]] = ', '.join(
                self.getreflink(name="({} ({}))".format(self.getelem(tabanker)['name']
                                                        , self.getelem(tabanker)['CRUD']),
                                destid=tabanker,
                                curdatmid=self.getdatmid(),
                                destdatmid=datmanker,
                                basedirec=self.basedirec)
                for tabanker in tablist)
        # for
        return allmappings

    def collectcolmappings(self, pelem):
        # [[attrkey,attr,subentikey],...]
        attrs = [[attr[0]
                     , self.getelem(attr[0])
                     , attr[1]] for attr in pelem['attributesmapped']]
        # append string to be displayed
        for attr in attrs:
            if attr[1]['entity'] is None:
                attr.append("{}.{}".format(self.getelem(attr[1]['relation'])['name']
                                           , attr[1]['name'][self.curlanguage])
                            )
            else:
                enti = self.getelem(attr[2])
                entistr = "" if enti is None else f" ({enti['name'][self.curlanguage]})"
                attr.append("{}{}.{}".format(self.getelem(attr[1]['entity'])['name'][self.curlanguage]
                                             , entistr
                                             , attr[1]['name'][self.curlanguage])
                            )
            # fi
        # for
        allmappings = {"Information Model": ', '.join (self.getreflink(name=attr[3],destid=attr[0],
                                                                       curdatmid=self.getdatmid(),
                                                                      basedirec=self.basedirec
                                                                       ) for attr  in attrs)}

        for datmanker, datmelem in filter(lambda e : e[0] != pelem['datamodel-id+'],
                                          self.jsmodel.getelements(pelemtype='datamodels').items()):
            #replaced by filter if datmanker == pelem['datamodel-id+']: continue
            collist = []
            for attr in pelem['attributesmapped']:
                mapcolus = self.getelem(attr[0])['columnsmapped+']
                if datmanker in mapcolus:
                    collist += mapcolus[datmanker]
            if len(collist) == 0: continue
            collist = list(set(collist))
            allmappings[datmelem["name"]] = ', '.join(
                self.getreflink(name="({}.{} ({}))".format(self.getelem(colanker)['table-name+']
                                                           , self.getelem(colanker)['name']
                                                           , self.getelem(colanker)['R/W']),
                                 destid=colanker,
                                 curdatmid=self.getdatmid(),
                                 destdatmid=datmanker,
                                basedirec=self.basedirec) for colanker in collist)
        # for
        return allmappings

    def getmaplist(self, id, curdatmid=None):
        elem = self.jsmodel.getbyid(id)
        if jsguid2type(id) in ('TABL', 'RELA'):
            retval = self.collecttablemappings(pelem=elem)

        elif jsguid2type(id) == 'COLU':
            retval = self.collectcolmappings(pelem=elem)
        elif jsguid2type(id) == 'ENTI':
            retval = {}
        elif jsguid2type(id) == 'ATTR':
            retval = {}
        else:
            retval = {}
        return retval

    def getentiicon(self, entielem):
        return self.export.iconsrc(pjsenti=entielem, pdefaultlang=self.getdeflanguage())


    def getentienviron(self, entiid):
        entienviron = entityenviron.entienviro2svg(pentiid=entiid
                                                   , penviron=entityenviron.createentienvironment(pentiid=entiid
                                                                                                  , pjson=self.jsmodel
                                                                                                  ,pmodellang=self.curlanguage)
                                                   )
        retval = self.export.replacesvghrefs(svg=entienviron,curlang=self.curlanguage,basedirec=self.basedirec)
        return retval


def getnvl(val, default=""):
    return default if val is None else val


def formattext(pstr):
    MARKDOWN: str = '<text/markdown>'
    # check wether we have markdown in the string
    if type(pstr) != str:
        return pstr
    if pstr.startswith(MARKDOWN):
        try:
            htmltext = markdown(pstr[len(MARKDOWN):])
            """ mark html tags with a special class to allow css for markdown content"""
            htmltext = re.sub(r'<(h1|h2|h3|h4|p|li|ul|ol)>', r'<\g<1> class="md">', htmltext)
            return htmltext
        except:
            return pstr
    else:  # assume plain text
        try:  # replace cr with <br>cr
            return re.sub(r"\n", r"<br>\n", pstr)
        except:
            return pstr
    # fi


"""
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "template.html"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render()  # this is where to put args to the template renderer
"""


def model2html(pwebmodel: Webmodel):
    template_folder = pwebmodel.export.jinjaDirec
    assert os.path.isdir(template_folder), f"Missing jinja templates folder {template_folder}"
    t = Environment(loader=FileSystemLoader(searchpath=template_folder),autoescape=True)
    if pwebmodel.getdatmid() is not None:
        templatename = "datamodel.jinja.html"
    else:
        templatename = "informationmodel.jinja.html"
    # fi
    try:
        templ = t.get_template(templatename)
    except:
        logmessages.writelog(f"jinja template {templatename} in {pwebmodel.export.jinjaDirec} not found")
        raise
    # try

    templ.globals['getnvl'] = getnvl
    t.filters['formattext'] = formattext
    t.filters['nvl'] = getnvl
    try:
        retval = templ.render(timestamp=datetime.now(), webmodel=pwebmodel)
    except Exception as e:
        logmessages.writelog(f"Error in jinja template {pwebmodel.export.jinjaDirec}/{templatename}")
        logmessages.writelog(str(e))
        raise Exception(f"Cannot render template {Path(template_folder, templatename)}: " + str(e)) from e
    # try
    return retval


def element2html(pwebmodel: Webmodel, pelemtype: str, pelemid: str):
    template_folder = pwebmodel.export.jinjaDirec
    assert os.path.isdir(template_folder), f"Missing jinja templates folder {template_folder}"
    t = Environment(loader=FileSystemLoader(searchpath=template_folder), autoescape=True)
    if pelemtype=="maindview":
        templatename = "mainview.jinja.html"
    elif pwebmodel.getdatmid() is not None:
        templatename = "datamodel.jinja.html"
    else:
        templatename = "im_pagewise.jinja.html"
    # fi
    try:
        templ = t.get_template(templatename)
    except:
        logmessages.writelog(f"jinja template {templatename} in {pwebmodel.export.jinjaDirec} not found")
        raise
    # try

    templ.globals['getnvl'] = getnvl
    t.filters['formattext'] = formattext
    t.filters['nvl'] = getnvl
    try:
        retval = templ.render(timestamp=datetime.now(), webmodel=pwebmodel,
                              elemtype=pelemtype, elemid=pelemid)
    except Exception as e:
        logmessages.writelog(f"Error in jinja template {pwebmodel.export.jinjaDirec}/{templatename}")
        logmessages.writelog(str(e))
        raise Exception(f"Cannot render template {Path(template_folder, templatename)}: " + str(e)) from e
    # try
    return retval
