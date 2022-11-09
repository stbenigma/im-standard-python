import json
import logging
from datetime import datetime
from pathlib import Path
from threading import local
from packaging import version

from SSOT_db.IM_OBJECTS import Modelelemtype, Boolean
from SSOT_infra import nvl,parameters

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

    def __init__(self, pmodel=None,pwithversioncheck=True,**kwargs):
        if pmodel is None:
            self.jsmodel = {}
        else:
            self.jsmodel = pmodel
            if pwithversioncheck:
                #check against version in tools-version file
                self.assertversion()

        self.languages = {}  # langid:iso2
        self._jsfile=kwargs.get('jsonfile')

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
    def readfromfile(pfilename,pwithcheck=True):
        try:
            with open(pfilename, 'r') as handle:
                model = json.load(handle)
        except ValueError as e:
            raise ValueError(f"Invalid JSON in {pfilename}. {e}") from e

        return JSModel(pmodel=model,pwithversioncheck=pwithcheck,jsonfile=pfilename)

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

    @property
    def jsfile(self):
        return self._jsfile

    def getdefaultlang(self):
        return self.jsmodel["model"]["language"]


    def getlangtext(self,pelem,plang,pidx=None,preplacement=True):
        """ get the value of a translated field
            pelem language-text-element
                {
                    "de": "Gugus",
                    "en": "*de* Gugus",
                    "fr": ""
                },
            pidx  None for dict, non None for lists (like synonyms or examples
            plang language for text to choose
            preplacement if text is empty of special coded (see en above) return text of default language

            if the value of a translation (=entry of none-default language)
            is of the form *<ll>* <value of default language>) (see en in example)
            the replacement language text (or "" if not wanted) is returned, as this is a replacement for an empty language

            """
        assert ((type(pelem) is dict and (set(pelem.keys())==set(self.jsmodel["languages"].keys())))
                or (type(pelem) is list and pidx is not None and  (set(pelem[pidx].keys())==set(self.jsmodel["languages"].keys())))
                )
        if type(pelem) is list:
            elem = pelem[pidx]
        else:
            elem = pelem

        lang = plang.lower()
        deflang=self.getdefaultlang()

        val = nvl(elem.get(lang))
        if lang == deflang:
            return val #default language is not handled

        if val == f"*{deflang}* {elem.get(deflang)}":
            val = ""

        #if val is empty, choose the replacement language text if chosen
        if val == "" and preplacement:
            replang = self.jsmodel["languages"].get(lang)["replacementlang"]
            if replang is not None:
                val = elem.get(replang)

        return val


    def getbyid(self, pjsid):
        """return the element identified by the jsid (<type><id>) from the current jsmodel"""
        try:
            return self.jsmodel[JSModel.elemtype2label(jsguid2type(pjsid))][pjsid]
        except:
            return None

    def getbyfield(self, ptype, pvalue, pfield='name', plang=None):
        """return tupels of (ID,element) of all elements containing the field pfield
            with a content of pvalue from the type of element current jsmodel
            returns empty list if nothing was found
        """
        retval = []
        for k, v in self.jsmodel[ptype].items():
            if (plang is None and v[pfield] == pvalue) or \
                    (plang is not None and v[pfield][plang] == pvalue):
                retval.append((k, v))
        # raise Exception(f"{ptype} : {pfield} : {pvalue}({plang}) not found ")
        return retval

    def getbysrcref(self,psrcname,psrcid)->(str,dict):
        """ return the id and the structure of the element, identified by
        the external sourceref-id for the source called psrcname
        return None,None if not found
        """
        for elemtype in self.jsmodel.values():
            for key,elem in elemtype.items():
                if type(elem) is not dict: continue
                sourceref = elem.get("sourceref")
                if sourceref is None: continue
                odmref = sourceref.get(psrcname)
                if odmref and (odmref[0] == psrcid):
                    return key, elem
        return None, None

    def isrecursive(self,pentiid):
        """ True, if the entitiy has a direct recursive relation
        """
        retval = False
        if pentiid in self.getelements("entities").keys():
            enti = self.getbyid(pentiid)
            if enti is not None :
                for relaid in enti["relations+"]:
                    #if one relation points to itself, set retval TRUE
                    rela = self.getbyid(relaid)
                    retval = retval or (rela["from-to"]["enti"] == pentiid == rela["to-from"]["enti"])
        return retval

    def issupertype(self,psupid,psubid):
        """
        True, if psupid is a supertypeentitiy on any level of psubid
        False otherwise
        """
        if psupid is None or psubid is None:
            return False
        retval = False
        subenti = self.getbyid(psubid)
        for newsubid in subenti["supertypes+"]:
            if (newsubid == psupid) or self.issupertype(psupid,newsubid):
                retval = True
                break

        return retval

    @property
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

    def write_json(self, destination: Path):
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


    def getjsversion(self)->version.Version:
        if "_imprint_"  not in self.jsmodel:
            jsversionstr ="0.0"
        else:
            jsversionstr = self.jsmodel["_imprint_"].get("JSONversion")
            if jsversionstr is None:
                jsversionstr= "0.0"

        jsversion = version.parse(jsversionstr)
        return jsversion

    def checkversion(self,pcheckversion:str=None)->Boolean:
        """
        json version are compatible  if major version is equal
        """
        if pcheckversion is None:
            checkv = parameters.jsonversion()
        else:
            checkv=version.parse(pcheckversion)
        return checkv.major == self.getjsversion().major

    def assertversion(self,pcheckversion:str=None):
        """
            breaks if jsonversion is not suitable
        """
        assert self.checkversion(pcheckversion),\
        f"loaded json-Version {self.getjsversion().base_version} not covered by current json-version {parameters.jsonversion()}"
        return

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
