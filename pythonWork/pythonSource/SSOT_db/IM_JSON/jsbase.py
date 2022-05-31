import json
import logging
from datetime import datetime
from pathlib import Path
from threading import local

from SSOT_db.IM_OBJECTS import Modelelemtype, Boolean
from SSOT_infra import nvl

context = local()


def jsguid(mtype, guid):
    """creates a unique ID as reference in the json file
   <telemtype><elemid> """
    context.ctx = dict()
    context.ctx[mtype] = guid
    return None if guid is None else mtype + (guid if type(guid) == str else str(guid))


def jsguid2id(guid):
    """returns the id part of a jsguid by removing the 4 leading characters (type) from a jsguid"""
    return None if guid is None else int(guid[4:])


def jsguid2type(guid):
    """returns the type part of a jsguid = 4 leading characters (type) from a jsguid"""
    return None if guid is None else guid[:4]


def optionalvalue(pelem, pkey):
    try:
        retval = pelem[pkey]
    except KeyError:
        retval = None
    return retval


def jsonfilename(pfilename):
    return pfilename + ('' if pfilename[-5:] == '.json' else '.json')


class JSModel:
    ELEMTYPE_LANG = 'LANG'
    ELEMTYPE_PROJ = 'PROJ'
    ELEMTYPE_CATG = 'CATG'
    _elemtype2label = {
        Modelelemtype.ENTI: 'entities',
        Modelelemtype.BURU: 'businessrules',
        Modelelemtype.RELA: 'relations',
        Modelelemtype.ATTR: 'attributes',
        Modelelemtype.ACTR: 'actorroles',
        Modelelemtype.DOMA: 'domains',
        Modelelemtype.ORGU: 'orgunits',
        Modelelemtype.TABL: 'tables',
        Modelelemtype.INTF: 'systems',
        Modelelemtype.COLU: 'columns',
        Modelelemtype.ARCS: 'arcs',
        Modelelemtype.DOCU: 'documents',
        Modelelemtype.KEYS: 'keys',
        Modelelemtype.DATY: 'datatypes',
        Modelelemtype.DIAG: 'diagrams',
        Modelelemtype.PHYU: 'physicalunits',
        Modelelemtype.STFO: 'storageformats',
        Modelelemtype.UDPR: 'userdefprops',
        ELEMTYPE_CATG: 'categories',
        ELEMTYPE_LANG: 'languages',
        ELEMTYPE_PROJ: 'model'
    }

    def __init__(self, pmodel=None):
        self.jsmodel = {} if pmodel is None else pmodel
        self.languages = {}  # langid:iso2

    def getelements(self, pelemtype):
        """returns dict of top level Elements filtered by statusfilter"""
        if pelemtype in self.jsmodel:
            elemtypekey = pelemtype
        else:
            elemtypekey = JSModel.elemtype2label(pelemtype=pelemtype)
            if elemtypekey is None:
                return None
            # fi
        # fi
        assert (elemtypekey in self.jsmodel), "key {} not found in json-model".format(elemtypekey)
        return self.jsmodel[elemtypekey]

    @staticmethod
    def readfromfile(pfilename):
        try:
            with open(pfilename, 'r') as handle:
                model = json.load(handle)
        except ValueError as e:
            raise ValueError(f"Invalid JSON in {pfilename}. {e}") from e

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
            lab = {val: key for key, val in JSModel._elemtype2label.items()}
            return lab[plabel]
        except:
            return plabel

    def getentitycolor(self, pentiid, pcolortype):
        enti = self.getbyid(pentiid)
        if enti is None:
            return None
        catg = self.getbyid(enti["category"])
        if catg is None or len(catg["ui"]) == 0:
            return None
        return catg["ui"][pcolortype]

    def getdefaultlang(self):
        return self.jsmodel["model"]["language"]

    """return the element identified by the jsid (<type><id>) from the current jsmodel"""

    def getbyid(self, pjsid):
        try:
            return self.jsmodel[JSModel.elemtype2label(jsguid2type(pjsid))][pjsid]
        except:
            return None

    def checked(self):
        return self._checked

    def setchecked(self, pvalue):
        self._checked = pvalue

    def modellanguage(self):
        return self.jsmodel["model"]["language"]

    def modelname(self):
        return self.jsmodel["model"]["name"]

    def printmodel(self, pfilepath, pfilename):
        return printJSON(pmodel=self.jsmodel, pfilepath=pfilepath, pfilename=pfilename)

    def printSPOD(self, destination: Path):
        return storeSPOD(self.jsmodel, destination)

    def _repr_json_(self):
        return {
            'model': self.jsmodel['model'],
            'imprint': self.jsmodel['_imprint_'],
            'entities': len(self.jsmodel['entities']),
            'attributes': len(self.jsmodel['attributes']),
            'systems': len(self.jsmodel['systems']),
            'tables': len(self.jsmodel['tables']),
            'columns': len(self.jsmodel['columns']),
        }


# JSModel


def check_json_serialisable(structure: dict):
    def nest(element, path: str):
        if isinstance(element, dict):
            for key, value in element.items():
                full_path = path + '."' + key + '"'
                nest(value, full_path)
        elif isinstance(element, list):
            index = 0
            for item in element:
                full_path = path + f'[{index}]'
                nest(item, full_path)
                index += 1
        else:
            check_value(element, path)

    def check_value(value, path: str):
        if isinstance(value, datetime):
            raise ValueError(f"Value {value} of type {type(value)} in {path} cannot be serialised")

    nest(structure, '')


def printJSON(pmodel, pfilepath, pfilename, psorted=False):
    destination = Path(pfilepath, jsonfilename(pfilename))
    return storeSPOD(pmodel, destination)


def storeSPOD(pmodel, destination, psorted=False) -> Path:
    check_json_serialisable(pmodel)
    with open(destination, 'w') as jsonfile:
        jsonfile.write(json.dumps(pmodel, indent=3))
    return destination


def fillmodel(pmodel, pentries):
    """
    :param pmodel: ["name"...]
    :param pentries: [value...]
    :return: dictionary with position in list matching name-value pairs
    """
    if not pmodel or not pentries or (len(pmodel) != len(pentries)):
        raise Exception("parameter mismatch (model: {}, entries: {})".format(len(pmodel), len(pentries)))
    return {pmodel[idx]: val for idx, val in enumerate(pentries)}


def warn_missing_translation(din: dict, dout: dict) -> None:
    diff = set(dout.values()).difference(set(din.values()))
    if len(diff) > 0:
        languages = dict(filter(lambda i: i[1] is None, din.items()))
        logging.warning(f"Patching missing translation for {languages.keys()} in {context.ctx}")
    return


def multilangtext(ptext: dict = {'en': ''}):
    assert ptext is not None
    result = {k: nvl(v) for k, v in ptext.items()}
    ### Multilang-Texte werden im select behandelt.
    # warn_missing_translation(ptext, result)
    return result


def reflist(plist: list = None):
    """ None = emptymodel"""
    if plist is None:
        return []
    else:
        return [e for e in plist]


def tabreflist(plist: dict = None):
    """ None = emptymodel"""
    """ """
    if plist is None:
        return {'INTF000': ['TABL000']}
    else:
        return plist


def colureflist(plist: dict = None):
    """ None = emptymodel"""
    """ """
    if plist is None:
        return {'INTF000': ['COLU000']}
    else:
        return plist


def sourceref(pvalues: dict = None):
    """ None = emptymodel"""
    if pvalues is None:
        return {"ODM": ["", ""]}
    else:
        return pvalues


def userdefprops(pprops: dict = None):
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
        return {'Theme': {"Group": {"UDPR000": {"name": '', "value": ''}}}}
    else:
        return pprops


def rwstr(pread=True, pwrite=False):
    return ''.join(rw(pread=pread, pwrite=pwrite))


def rw(pread=True, pwrite=False):
    if type(pread) == str:
        pread = Boolean.str2bool(pread)
    if type(pwrite) == str:
        pwrite = Boolean.str2bool(pwrite)
    retval = []
    if pread:
        retval.append('R')
    if pwrite:
        retval.append('W')
    return retval


def crudstr(pread=True, pupdate=False, pdelete=False, pcreate=False):
    return ''.join(crud(pread=pread, pupdate=pupdate, pdelete=pdelete, pcreate=pcreate))


def crud(pread=True, pupdate=False, pdelete=False, pcreate=False):
    if type(pread) == str:
        pread = Boolean.str2bool(pread)
    if type(pcreate) == str:
        pcreate = Boolean.str2bool(pcreate)
    if type(pupdate) == str:
        pupdate = Boolean.str2bool(pupdate)
    if type(pdelete) == str:
        pdelete = Boolean.str2bool(pdelete)
    retval = []
    if pcreate:
        retval.append('C')
    if pread:
        retval.append('R')
    if pupdate:
        retval.append('U')
    if pdelete:
        retval.append('D')
    return retval
