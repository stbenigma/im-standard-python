import re
import logging

attrmatchkey2js= {'name':'name',
            'descr':'descr',
            'tooltip':'tooltip',
            'synonyms':'synonyms',
            'examples':'examples',
            'errormsg':'errormsg',
            'fromto':'from-to'
            ,'tofrom':'to-from'}
attrmatchjs2key={val:key for key,val in attrmatchkey2js.items()}
def attrjs2key(pstr):
    return None if not pstr in attrmatchjs2key else attrmatchjs2key[pstr]

def attrkey2js(pstr):
    return None if not pstr in attrmatchkey2js else attrmatchkey2js[pstr]



def strislang(l: str) -> bool:
    return type(l) is str and re.match("[a-z]{2}",l)

class Metainfo():
    def __init__(self,**kwargs):
        self._gitrevision = kwargs.get("gitrevision")
        self._dbmodelversion = kwargs.get("dbmodelversion")
        self._lastupdate = kwargs.get("lastupdate")
        self._jsonfile = kwargs.get("jsonfile")
        self._modellang = kwargs.get("modellang")
        self._modelname = kwargs.get("modelname")

    def getgitrevision(self):
        return self._gitrevision

    def getdbmodelversion(self):
        return self._dbmodelversion

    def getlastupdate(self):
        return self._lastupdate

    def getmodelname(self):
        return self._modelname

    def getmodellang(self):
        return self._modellang

    def getjsonfile(self):
        return self._jsonfile

    def str2metainfo(self,pstr):
        lines = pstr.split('\n')
        for line in lines:
            vals = line.split('=')
            if len(vals) == 2:
                if vals[0].strip()=="model":
                    self._modelname=vals[1].strip()
                if vals[0].strip() == "lastmodified":
                    self._lastupdate = vals[1].strip()
                if vals[0].strip() == "modellanguage":
                    self._modellang = vals[1].strip()
                if vals[0].strip() == "git-revision":
                    self._gitrevision = vals[1].strip()
                if vals[0].strip() == "jsonfile":
                    self._jsonfile = vals[1].strip()
                if vals[0].strip() == "dbmodelversion":
                    self._dbmodelversion = vals[1].strip()
            else:
                logging.warning(f"Excelimport: invalid metainformation from comment: {vals}")
        return self

    def __str__(self):
        return '\n'.join(s for s in [f"model={self.getmodelname()}",
                                    f"lastmodified={self.getlastupdate()}",
                                    f"modellanguage={self.getmodellang()}",
                                    f"git-revision={self.getgitrevision()}",
                                    f"jsonfile={self.getjsonfile()}"
                                    ])

class Langexceldata:
    KEY = 'Key'
    def __init__(self):
        self._headerwidthws = []
        self._header = dict()
        self._metainfo = None

    def getheader(self):
        return self._header

    def setheader(self, plangs):
        self._header = dict()
        self._header[1] = self.KEY
        for idx, l in enumerate(plangs, start=2):
            self._header[idx] = l
        self._header[len(plangs) + 2] = 'Description'
        self._header[len(plangs) + 3] = 'Comments'

    def setheaderwidth(self,pdimensions:list):
        self._headerwidthws = pdimensions

    def getheaderwidth(self):
        return self._headerwidthws

    def getheader(self):
        return self._header

    def setheader(self, plangs):
        self._header = dict()
        self._header[1] = self.KEY
        for idx, l in enumerate(plangs, start=2):
            self._header[idx] = l
        else:
            self._header[len(plangs) + 2] = 'Description'
            self._header[len(plangs) + 3] = 'Comments'

    def getheaderlist(self):
        retval = [self._header[k] for k in sorted(self._header.keys())]
        return retval

    def getheaderidx(self,ptitle):
        for i, v in self._header.items():
            if v == ptitle:
                return i

    def keyrowidx(self):
        return self.getheaderidx(self.KEY)

    def getlanguages(self):
        assert len(self._header)>1
        return [val for idx,val in self._header.items() if strislang(val)]

    def analyzeheader(self, prow):
        headervals = [cell.value for cell in prow]
        if not (self.KEY in headervals and len(headervals) > 1):
            raise AssertionError("***** Header must contain 'Key' and at least one language-code")
        self._header = dict()
        for idx, title in enumerate(headervals, start=1):
            self._header[idx] = title
        langs =self.getlanguages()
        if len(langs) != len(set(langs)):
            raise AssertionError("***** Header must not contain duplicated languages {langs}")

    @staticmethod
    def decodekey(pkey):
        """returns id,attr,idx for from a keyvalue
            ENTI119-Name[-nnn]
        """
        key,attr,idx = None,None,None
        if re.match("^[A-Z]{4}\d+\-[a-z]+\-?\d*$",pkey):
            vals = pkey.split('-')
            key =vals[0]
            attr = vals[1]
            idx = None if len(vals)<3 else int(vals[2])
        else:
            raise Exception(ValueError)
        return key,attr,idx


    def analyzecomment(self,pcomment):
        self._metainfo = Metainfo().str2metainfo(pcomment)
        return

    def getmetainfo(self)->Metainfo:
        return self._metainfo


