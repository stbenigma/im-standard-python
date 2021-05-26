from datetime import datetime
import re
import logmessages
from IM_HTML import printHTML,entityenviron
from IM_DB import parameters
from IM_JSON import JSModel,jsguid2type
from IM_OBJECTS import Languagetext
from jinja2 import FileSystemLoader,Environment

class Webmodel():
    def __init__(self,pcurlang,pjsmodel:JSModel,pintfid,phtmlfilelist):
        self.curlanguage = pcurlang
        self.jsmodel:JSModel = pjsmodel
        self.intferfaceid = pintfid
        self.htmlfilelist = phtmlfilelist

    def getintfid(self):
        return self.intferfaceid

    def getmodelname(self):
        return self.jsmodel.jsmodel['model']['name']

    def getelemintfid(self,elemid):
        elem = self.getelem(elemid)
        if jsguid2type(elemid) in ["TABL","DOMA"]:
            retval = elem["interface-id"]
        elif jsguid2type(elemid) in ["INTF","COLU"]:
            retval = elem["interface-id+"]
        else:
            retval = None
        #fi
        return retval

    def getcurlanguage(self):
        return self.curlanguage

    def getdeflanguage(self):
        return self.jsmodel.getdefaultlang()

    def getlanguages(self,all=True):
        langs = list(self.jsmodel.jsmodel["languages"].keys())
        if not all:
            langs.remove(self.getcurlanguage())
        return langs

    def setelements(self,**kwargs):
        for key,val in kwargs.items():
            self.__setattr__(key.lower(),val)

    def gettransltext(self,str):
        retval = Languagetext.transl(pname=str,plang=self.getcurlanguage())
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
        return printHTML.type2name(ptyp=typ[:4],plang=self.getcurlanguage)

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
                destfilename = destfilename[:-7] + destlang + ".html"
            #fi
        #fi

        try:
            retval = """<a href="{}#{}" target="{}">{}</a>""" \
            .format(destfilename
                    ,destid
                    ,'_self' if curintfid == destintfid else '_blank'
                    ,name)
        except Exception as err:
            pass
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
            for enti in pelem['entitiesmapped']+pelem['relationsmapped']:
                try:
                    tablist += self.getelem(enti)['tablesmapped+'][intfanker]
                except:
                    pass
            if len(tablist) == 0: continue
            allmappings[intfelem["name"]] = ', '.join (self.getreflink(name="({})".format(self.getelem(tabanker)['name'])
                                                                ,destid=tabanker
                                                                ,curintfid=self.getintfid()
                                                                ,destintfid=intfanker) for tabanker in tablist)
        # for
        return allmappings

    def collectcolmappings(self,pelem):
        attrs = {a: self.getelem(a) for a in pelem['attributesmapped']}
        attrlist = []
        for anker, attr in attrs.items():
            if attr['entity'] is None:
                attrlist.append([anker, "{}.{}".format(self.getelem(attr['relation'])['name']
                                                       , attr['name'][self.curlanguage])])
            else:
                attrlist.append([anker, "{}.{}".format(self.getelem(attr['entity'])['name'][self.curlanguage]
                                                       , attr['name'][self.curlanguage])])
            # fi
        # for
        allmappings = {"Information Model": ', '.join (self.getreflink(name=name,destid=anker
                                                                       ,curintfid=self.getintfid()) for anker,name  in attrlist.items())}
        for intfanker, intfelem in self.jsmodel.getelements(pelemtype='systems').items():
            if intfanker == pelem['interface-id+']: continue
            collist = []
            for attr in pelem['attributesmapped']:
                try:
                    collist += self.getelem(attr)['columnsmapped+'][intfanker]
                except:
                    pass
            if len(collist) == 0: continue
            allmappings[intfelem["name"]] = ', '.join(self.getreflink(name="({}.{})".format(self.getelem(colanker)['table-name+']
                                                                                    , self.getelem(colanker)['name'])
                                                                      , destid=colanker
                                                                      , curintfid=self.getintfid()) for colanker in collist)
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

    def getentiicon(self,entielem):
        m = printHTML.getmodel()
        return printHTML.iconsrc(pjsenti=entielem,pdefaultlang=self.getdeflanguage())

    def getentienviron(self,entiid):
        return entityenviron.entienviro2svg(pentiid=entiid
                                            ,penviron=entityenviron.createentienvironment(pentiid=entiid
                                                                                          ,pjson=self.jsmodel
                                                                                          ,pmodellang=self.getcurlanguage()))
def getnvl(val,default = ""):
    return default if val is None else val



def lf2htmlbr(pstr):
    try:
        return re.sub(r"\n", "<br>\n", pstr)
    except:
        return pstr


def model2html(pwebmodel:Webmodel):
    jinjadirec = parameters.webDirec()+"jinjatemplates"
    #jinjadirec = "/Users/stb/Documents/Projekte/FYAYC_intern/fyyccim-tools/pythonWork/pythonSource/IM_WEB/html-lib/jinjatemplates"
    t = Environment(loader=FileSystemLoader(jinjadirec),autoescape=True)
    if pwebmodel.getintfid() is not None:
        templatename = "interface.jinja.html"
    else:
        templatename = "informationmodel.jinja.html"
    #fi

    try:
        templ = t.get_template(templatename)
    except:
        logmessages.writelog("jinja template {} in {} not found".format(templatename,jinjadirec))
        raise
    #try


    templ.globals['getnvl'] = getnvl
    templ.globals['lf2htmlbr'] = lf2htmlbr
    try:
        retval = templ.render(timestamp=datetime.now(),webmodel=pwebmodel)
    except Exception as e:
        logmessages.writelog("Error in jinja template {}/{}".format(jinjadirec,templatename))
        logmessages.writelog(str(e))
        raise e
    #try
    return retval

