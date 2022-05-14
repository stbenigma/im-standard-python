from SSOT_infra.parameters import SUPPORTEDLANGUAGES
from SSOT_infra import nvlkey
import logging

class Metainfo():
    def __init__(self,**kwargs):
        self._gitrevision = nvlkey(kwargs,"gitrevision")
        self._dbmodelversion = nvlkey(kwargs,"dbmodelversion")
        self._lastupdate = nvlkey(kwargs,"lastupdate")
        self._jsonfile = nvlkey(kwargs,"jsonfile")
        self._modellang = nvlkey(kwargs,"modellang")
        self._modelname = nvlkey(kwargs,"modelname")

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
        return

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

    def analyzeheader(self, prow):
        if not (self.KEY in prow and len(prow) > 1):
            raise AssertionError("***** Header must contain 'Key' and at least one language-code")
        self._header = dict()
        for idx, title in enumerate(prow, start=1):
            self._header[idx] = title

    def analyzecomment(self,pcomment):
        self._metainfo = Metainfo().str2metainfo(pcomment)
        return

    def getmetainfo(self):
        return self._metainfo

    @staticmethod
    def strislang(l: str) -> bool:
        return l.lower() in SUPPORTEDLANGUAGES.keys()
