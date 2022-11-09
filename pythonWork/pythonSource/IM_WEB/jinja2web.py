import re
import os
import logging
from datetime import datetime
from pathlib import Path

from markdown import markdown

from IM_WEB.IM_HTML import entityenviron, HTMLExport
from SSOT_infra import logmessages
from SSOT_db.IM_JSON import  JSModel, jsguid2type
from jinja2 import FileSystemLoader, Environment
from SSOT_infra.translateprompt import transl

class Webmodel:

    def __init__(self, export: HTMLExport, pcurlang: str, pjsmodel: JSModel, pintfid, phtmlfilelist):
        self.curlanguage = pcurlang
        self.jsmodel:JSModel = pjsmodel
        self.intferfaceid = pintfid
        self.htmlfilelist = phtmlfilelist
        self.export = export

    def getintfid(self):
        return self.intferfaceid

    def getmodelname(self):
        return self.jsmodel.jsmodel['model']['name']

    def getsubentyids(self,attrid):
        """get all subentity-ids from subentities inheriting this attribute"""
        entiids = [entikey for entikey,entival in self.jsmodel.getelements("entities").items()
                   if (attrid in entival["inheritedattributes+"])]
        return entiids

    def getsubentyrefs(self,attrid):
        """get all subentity-referencestrings from subentities inheriting this attribute"""
        entiids = self.getsubentyids(attrid)
        entirefs = [self.getreflink(name=self.getlangstr(self.getelem(elemid)["name"]),destid=elemid)
                    for elemid in entiids]
        return entirefs

    def getelemintfid(self,elemid):
        elem = self.getelem(elemid)
        retval = None
        if elem is not None:
            if jsguid2type(elemid) in ["TABL","DOMA"]:
                retval = elem["interface-id"]
            elif jsguid2type(elemid) in ["INTF","COLU"]:
                retval = elem["interface-id+"]
        #fi
        return retval

    def getcurlanguage(self):
        return self.curlanguage

    def getdeflanguage(self):
        return self.jsmodel.getdefaultlang()

    def getlanguages(self,all=True):
        langs = list(self.jsmodel.jsmodel[JSModel.elemtype2label(JSModel.ELEMTYPE_LANG)].keys())
        if not all:
            langs.remove(self.getcurlanguage())
        return langs

    def setelements(self,**kwargs):
        for key,val in kwargs.items():
            self.__setattr__(key.lower(),val)

    def gettransltext(self, str):
        retval = transl(str)
        return retval

    def getlangstr(self,str,default=None):
        if type(str) == dict:
            """assumes str = {'de':"xxx",'en':"xxy",...}"""
            try:
                retval = str[default if default is not None else self.getcurlanguage()]
            except: #chosen language chosen does not exist, take default language
                retval = str[default if default is not None else self.getdeflanguage()]
        else:
            retval = str
        #fi
        return retval

    def displelemtype(self,typ):
        return self.export.type2name(ptyp=typ[:4],plang=self.getcurlanguage())

    def getelem(self,id):
        retval = self.jsmodel.getbyid(id)
        return retval

    def getreflink(self,name,destid,**intfs):
        curintfid,destintfid,destlang = None,None,None
        if "curintfid" in intfs: curintfid = intfs["curintfid"]
        if "destintfid" in intfs: destintfid = intfs["destintfid"]
        if "destlang" in intfs:
            destlang= intfs["destlang"]
        if (curintfid == destintfid and destlang is None):
            destfilename = ''
        else:
            destfilename = self.htmlfilelist[0 if destintfid is None else destintfid]
            if destlang is not None:
                """ language dependent file"""
                destfilename = destfilename[:-7] + destlang + f".{self.export.webFileExtension()}"
            #fi
        #fi

        try:
            retval = """<a href="{}#{}" target="{}">{}</a>""" \
            .format(destfilename
                    ,destid
                    ,'_self' if curintfid == destintfid else '_blank'
                    ,name)
        except Exception as err:
            logging.warning(f"Cannot format link to {destid}")
            return ""

        return retval

    def collecttablemappings(self,pelem):
        # name, list of entries mit {webanker:'name'}
        entities = {e: self.getelem(e)['name'][self.curlanguage] for e in pelem['entitiesmapped']}
        relations = {r: self.getelem(r)['name'] for r in pelem['relationsmapped']}
        entities.update(relations)
        allmappings = {"Information Model": ', '.join (self.getreflink(name=name,destid=anker
                                                                       ,curintfid=self.getintfid()) for anker,name  in entities.items())}

        for intfanker, intfelem in self.jsmodel.getelements(pelemtype='systems').items():
            if intfanker == pelem['interface-id']: continue
            tablist = []
            for enti in pelem['entitiesmapped'] + pelem['relationsmapped']:
                elem = self.getelem(enti)['tablesmapped+']
                if intfanker in elem:
                    tablist += elem[intfanker]
            if len(tablist) == 0: continue
            tablist=list(set(tablist))
            allmappings[intfelem["name"]] = ', '.join(self.getreflink(name="({} ({}))".format(self.getelem(tabanker)['name']
                                                                                                , self.getelem(tabanker)['CRUD'])
                                                , destid=tabanker
                                          , curintfid=self.getintfid()
                                          , destintfid=intfanker)
                                                      for tabanker in tablist)
        # for
        return allmappings

    def collectcolmappings(self,pelem):
        #[[attrkey,attr,subentikey],...]
        attrs = [[attr[0]
                  , self.getelem(attr[0])
                  , attr[1]] for attr in pelem['attributesmapped']]
        #append string to be displayed
        for attr in attrs:
            if attr[1]['entity'] is None:
                attr.append("{}.{}".format(self.getelem(attr[1]['relation'])['name']
                                         , attr[1]['name'][self.curlanguage])
                            )
            else:
                enti = self.getelem(attr[2])
                entistr = "" if enti is None else f" ({enti['name'][self.curlanguage]})"
                attr.append("{}{}.{}".format(self.getelem(attr[1]['entity'])['name'][self.curlanguage]
                                             ,entistr
                                            , attr[1]['name'][self.curlanguage])
                            )
            # fi
        # for
        allmappings = {"Information Model": ', '.join (self.getreflink(name=attr[3],destid=attr[0]
                                                                       ,curintfid=self.getintfid()
                                                                       ) for attr  in attrs)}

        for intfanker, intfelem in self.jsmodel.getelements(pelemtype='systems').items():
            if intfanker == pelem['interface-id+']: continue
            collist = []
            for attr in pelem['attributesmapped']:
                mapcolus = self.getelem(attr[0])['columnsmapped+']
                if intfanker in mapcolus:
                    collist += mapcolus[intfanker]
            if len(collist) == 0: continue
            collist =list(set(collist))
            allmappings[intfelem["name"]] = ', '.join(self.getreflink(name="({}.{} ({}))".format(self.getelem(colanker)['table-name+']
                                                                                    , self.getelem(colanker)['name']
                                                                                    , self.getelem(colanker)['R/W'])
                                                                      , destid=colanker
                                                                      , curintfid=self.getintfid()
                                                                      , destintfid=intfanker) for colanker in collist)
        # for
        return allmappings

    def getmaplist(self,id,curintfid=None,):
        elem = self.jsmodel.getbyid(id)
        if jsguid2type(id) in ('TABL','RELA'):
            retval = self.collecttablemappings(pelem=elem)

        elif jsguid2type(id)=='COLU':
            retval = self.collectcolmappings(pelem=elem)
        elif jsguid2type(id) == 'ENTI':
            retval = {}
        elif jsguid2type(id) == 'ATTR':
            retval = {}
        else:
            retval = {}
        return retval

    def getentiicon(self, entielem):
        return self.export.iconsrc(pjsenti=entielem,pdefaultlang=self.getdeflanguage())

    def getentienviron(self,entiid):
        return entityenviron.entienviro2svg(pentiid=entiid
                                            ,penviron=entityenviron.createentienvironment(pentiid=entiid
                                                                                          ,pjson=self.jsmodel
                                                                                          ,pmodellang=self.getcurlanguage()))
def getnvl(val,default = ""):
    return default if val is None else val


def formattext(pstr):
    MARKDOWN:str = '<text/markdown>'
    #check wether we have markdown in the string
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
    else: #assume plain text
        try: #replace cr with <br>cr
            return re.sub(r"\n", r"<br>\n", pstr)
        except:
            return pstr
    #fi

"""
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "template.html"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render()  # this is where to put args to the template renderer
"""
def model2html(pwebmodel:Webmodel):
    template_folder = pwebmodel.export.jinjaDirec()
    assert os.path.isdir(template_folder), f"Missing jinja templates folder {template_folder}"
    t = Environment(loader=FileSystemLoader(searchpath=template_folder),autoescape=True)
    if pwebmodel.getintfid() is not None:
        templatename = "interface.jinja.html"
    else:
        templatename = "informationmodel.jinja.html"
    #fi
    try:
        templ = t.get_template(templatename)
    except:
        logmessages.writelog("jinja template {} in {} not found".format(templatename, pwebmodel.export.jinadirec))
        raise
    #try


    templ.globals['getnvl'] = getnvl
    t.filters['formattext'] = formattext
    t.filters['nvl'] = getnvl
    try:
        retval = templ.render(timestamp=datetime.now(),webmodel=pwebmodel)
    except Exception as e:
        logmessages.writelog("Error in jinja template {}/{}".format(pwebmodel.export.jinjaDirec(), templatename))
        logmessages.writelog(str(e))
        raise Exception(f"Cannot render template {Path(template_folder, templatename)}: " + str(e)) from e
    #try
    return retval

