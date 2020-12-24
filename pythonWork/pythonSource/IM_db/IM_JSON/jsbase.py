import json
import sqlite3

"""creates a unique ID as reference in the json file
   <telemtype><elemid> """
jsguid = lambda type, id: None if id is None else type + str(id)

"""returns the id part of a jsguid by removing the 4 leading characters (type) from a jsguid"""
jsguid2id = lambda guid: None if guid is None else int(guid[4:])

"""returns the type part of a jsguid = 4 leading characters (type) from a jsguid"""
jsguid2type = lambda guid: None if guid is None else guid[:4]

def optionalvalue(pelem,pkey):
    try:
        retval = pelem[pkey]
    except KeyError as err:
        retval = None
    return retval

def jsonfilename(pfilename):
    return pfilename + '.json'

def printJSON(pmodel, pfilepath, pfilename):
    jsonfile = open(pfilepath + jsonfilename(pfilename), 'w')
    jsonfile.write(json.dumps(pmodel, indent=3, sort_keys=False))
    jsonfile.close()

class JSModel:
    def __init__(self,pmodel={}):
        self.jsmodel = pmodel
        self._checked = False
        self._errorcnt = 0
        self._warningcnt = 0
        self._errors = []
        self._warnings = []
        self._modellanguage = None
        self.languages = {}  # langid:iso2

    staticmethod
    def readfromfile(pfilename):
        with open(pfilename, 'r') as handle:
            model = json.load(handle)
        return JSModel(pmodel=model)

    def checked(self):
        return self._checked
    def setchecked(self,pvalue):
        self._checked = pvalue
    def modellanguage(self):
        return self._modellanguage
    def setmodellanguage(self,pvalue):
        self._modellanguage = pvalue

    def incerrcnt(self):
        self._errorcnt += 1
    def errcnt(self):
        return self._errorcnt

    def incwrncnt(self):
        self._warningcnt += 1
    def wrncnt(self):
        return self._warningcnt

    def errors(self):
        return self._errors
    def warnings(self):
        return self._warnings

    def markerror(self,pmsg,pelemstr=''):
        if type(pmsg) in (sqlite3.IntegrityError, sqlite3.DatabaseError, sqlite3.DataError, sqlite3.Error):
            errtype = 'DB-'
        else:
            errtype = ''
        #fi

        self._errors.append("***{}ERROR: {}".format(errtype, pmsg))
        self._errors.append("     " + pmsg.__str__())
        if pelemstr != '': self._errors.append(pelemstr)
        self.incerrcnt()
    # markerror
    def markwarning(self,pmsg):
        self._warnings.append("WARNING: {}".format(pmsg))
        self.incwrncnt()
    # markwarning


