import json
import sqlite3
from IM_OBJECTS import Modelelemtype,Boolean



"""creates a unique ID as reference in the json file
   <telemtype><elemid> """
jsguid = lambda mtype, id: None if id is None else mtype + (id if type(id)==str else str(id))

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


class JSModel:
    ELEMTYPE_LANG = 'LANG'
    ELEMTYPE_PROJ = 'PROJ'
    ELEMTYPE_CATG = 'CATG'
    _elemtype2label = {
        Modelelemtype.ENTI: 'entities'
      ,Modelelemtype.BURU: 'businessrules2js'
      ,Modelelemtype.RELA: 'relations'
      ,Modelelemtype.ATTR: 'attributes'
      ,Modelelemtype.DOMA: 'domains'
      ,Modelelemtype.ORGU: 'orgunits'
      ,Modelelemtype.TABL: 'tables'
      ,Modelelemtype.INTF: 'systems'
      ,Modelelemtype.COLU: 'columns'
      ,Modelelemtype.ARCS: 'arcs'
      ,Modelelemtype.DOCU: 'documents'
      ,Modelelemtype.KEYS: 'keys'
      ,Modelelemtype.DATY: 'datatypes'
      ,Modelelemtype.DIAG: 'diagrams'
      ,Modelelemtype.PHYU: 'physicalunits'
      ,Modelelemtype.STFO: 'storageformats'
      , Modelelemtype.UDPR: 'userdefprops'
      ,ELEMTYPE_CATG: 'categories'
        , ELEMTYPE_LANG: 'languages'
        , ELEMTYPE_PROJ: 'model'
    }

    def __init__(self,pmodel={}):
        self.jsmodel = pmodel
        self._checked = False
        self._errorcnt = 0
        self._warningcnt = 0
        self._errors = []
        self._warnings = []
        self.languages = {}  # langid:iso2
        self._statusfilter = (None,'DEV','TEST','REL')

    def getelements(self,pelemtype,pfiltered=True):
        """returns dict of top level Elements filtered by statusfilter"""
        elemkey = JSModel.elemtype2label(pelemtype=pelemtype)
        if elemkey is None:
            """ not found, check wether pelem is already a key"""
            if pelemtype in self.jsmodel:
                elemkey = pelemtype
            else:
                return None
            #fi
        #fi
        assert (elemkey in self.jsmodel),"key {} not found in json-model".format(elemkey)
        """get all elements, if filtered make sure it is a) not a dict, b) has no devstatus or c) its devstatus is in my statusfilter"""
        elems = {key : value for key,value in self.jsmodel[elemkey].items()
                   if (not pfiltered or type(value) != dict or 'devstatus' not in value or value['devstatus'] in self._statusfilter) }
        return elems

    def setstatusfilter(self,pfilter):
        self._statusfilter = pfilter

    def getstatusfilter(self,pfilter):
        return self._statusfilter

    @staticmethod
    def readfromfile(pfilename):
        with open(pfilename, 'r') as handle:
            model = json.load(handle)
        return JSModel(pmodel=model)

    @staticmethod
    def elemtype2label(pelemtype):
        try:
            return JSModel._elemtype2label[pelemtype]
        except:
            return None

    @staticmethod
    def label2elemtype(plabel):
        try:
            lab = {val:key for key,val in JSModel._elemtype2label.items()}
            return lab[plabel]
        except:
            return plabel

    def getdefaultlang(self):
        return self.jsmodel["model"]["language"]

    """return the element identified by the jsid (<type><id>) from the current jsmodel"""
    def getbyid(self,pjsid):
        try:
            return self.jsmodel[JSModel.elemtype2label(jsguid2type(pjsid))][pjsid]
        except:
            return None

    def checked(self):
        return self._checked

    def setchecked(self,pvalue):
        self._checked = pvalue

    def modellanguage(self):
        return self.jsmodel["model"]["language"]

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

    def printmodel(self,pfilepath, pfilename):
        return printJSON(pmodel=self.jsmodel,pfilepath=pfilepath,pfilename=pfilename)
#JSModel


def printJSON(pmodel, pfilepath, pfilename):
    destination = pfilepath + jsonfilename(pfilename)
    with open(destination, 'w') as jsonfile:
        jsonfile.write(json.dumps(pmodel, indent=3, sort_keys=False))
    return destination

def fillmodel(pmodel, pentries):
    """
    :param pmodel: ["name"...]
    :param pentries: [value...]
    :return: dictionary with position in list matching name-value pairs
    """
    if not pmodel or not pentries or (len(pmodel)!= len(pentries)):
        raise Exception("parameter mismatch (model: {}, entries: {})".format(len(pmodel),len(pentries)))
    retval = {pmodel[idx]: val for idx, val in enumerate(pentries)}
    return retval

def multilangtext(ptext:list=None):
    """ None = emptymodel"""
    if ptext is None:
        return {'en':''}
    else:
        return ptext

def reflist(plist:list=None):
    """ None = emptymodel"""
    if plist is None:
        return []
    else:
        return [e for e in plist]

def tabreflist(plist:dict=None):
    """ None = emptymodel"""
    """ """
    if plist is None:
        return {'INTF000':['TABL000']}
    else:
        return plist
def colureflist(plist:dict=None):
    """ None = emptymodel"""
    """ """
    if plist is None:
        return {'INTF000':['COLU000']}
    else:
        return plist

def sourceref(pvalues:dict=None):
    """ None = emptymodel"""
    if pvalues is None:
        return {"ODM": ["",""]}
    else:
        return pvalues

def userdefprops (pprops:dict=None):
    """ None = emptymodel"""
    """
            "datamapping": {
               "PENTA": {
                  "UDPR206": {
                     "name": "PENTA TabName",
                     "value": null
                  }
               },
               "PIM": {
                  "UDPR201": {
                     "name": "PIM TabName",
                     "value": null
                  }
               }
            },
        """
    if pprops is None:
        return {'Theme': {"Group": {"UDPR000": {"name":'', "value":''}}}}
    else:
        return pprops

def rwstr(pread=True,pwrite=False):
    return ''.join(rw(pread=pread,pwrite=pwrite))
def rw(pread=True,pwrite=False):
    if type(pread)== str:pread = Boolean.str2bool(pread)
    if type(pwrite)== str:pwrite = Boolean.str2bool(pwrite)
    retval = []
    if pread: retval.append('R')
    if pwrite:
        retval.append('W')
    return retval

def crudstr(pread=True,pupdate=False,pdelete=False,pcreate=False):
    return ''.join(crud(pread=pread,pupdate=pupdate,pdelete=pdelete,pcreate=pcreate))

def crud(pread=True,pupdate=False,pdelete=False,pcreate=False):
    if type(pread)== str:pread = Boolean.str2bool(pread)
    if type(pcreate)== str:pcreate = Boolean.str2bool(pcreate)
    if type(pupdate)== str:pupdate = Boolean.str2bool(pupdate)
    if type(pdelete)== str:pdelete = Boolean.str2bool(pdelete)
    retval = []
    if pcreate: retval.append('C')
    if pread: retval.append('R')
    if pupdate: retval.append('U')
    if pdelete: retval.append('D')
    return retval
