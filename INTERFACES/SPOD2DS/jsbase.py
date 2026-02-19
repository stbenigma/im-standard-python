from datetime import datetime
from pathlib import Path
import json
#from threading import local

from IM_STANDARD import nvl
from packaging import version

#context = local()


def readjsonfile(pfilename):
    try:
        with open(pfilename, 'r') as handle:
            retval = json.load(handle)
    except ValueError as e:
        raise ValueError(f"Invalid JSON in {pfilename}. {e}") from e
    return retval


# def jsguid(mtype, guid):
#     """creates a unique ID as reference in the json file
#    <telemtype><elemid> """
#     context.ctx = dict()
#     context.ctx[mtype] = guid
#     return None if guid is None else mtype + (guid if type(guid) == str else str(guid))
#

def jsguid2id(guid):
    """returns the id part of a jsguid by removing the 4 leading characters (type) from a jsguid"""
    if guid is None:
        retval = None
    elif guid[4:].isdigit():
        retval = int(guid[4:])
    else:
        retval = None
    return retval


def jsguid2type(guid):
    """returns the type part of a jsguid = 4 leading characters (type) from a jsguid"""
    return None if guid is None else guid[:4]


# def optionalvalue(pelem, pkey):
#     try:
#         retval = pelem[pkey]
#     except KeyError:
#         retval = None
#     return retval


def jsonfilename(pfilename):
    return pfilename + ('' if pfilename[-5:] == '.json' else '.json')


class JSModel:
    _elemtype2label = {
        "ENTI": 'entities',
        "BURU": 'businessrules',
        "RELA": 'relations',
        "ATTR": 'attributes',
        "ACTR": 'actorroles',
        "DOMA": 'domains',
        "ORGU": 'orgunits',
        "TABL": 'tables',
        "DATM": 'datamodels',
        "COLU": 'columns',
        "ARCS": 'arcs',
        "DOCU": 'documents',
        "KEYS": 'keys',
        "DATY": 'datatypes',
        "DIAG": 'diagrams',
        "PHYU": 'physicalunits',
        "STFO": 'storageformats',
        "UDPR": 'userdefprops',
        "CATG": 'categories',
        "LANG": 'languages',
        "PROJ": 'model',
        "EXST": 'examples'
    }

    def __init__(self, pmodel=None, pwithversioncheck=True, **kwargs):
        if pmodel is None:
            self.jsmodel = {}
        else:
            self.jsmodel = pmodel
            if pwithversioncheck:
                # check against version in tools-version file
                self.assertversion()

        self.languages = {}  # langid:iso2
        self._jsfile = kwargs.get('jsonfile')
        self._checked = None

    @property
    def git_revision(self):
        imprint=self.jsmodel['_imprint_']
        if imprint is not None:
            return imprint.get('git-revision')
        else:
            return None
    @git_revision.setter
    def git_revision(self,git_revision):
        imprint = self.jsmodel['_imprint_']
        if imprint is not None:
            imprint['git-revision'] = git_revision
        return

    @classmethod
    def jsonimprint(cls,dbname, created, modelversion, jsonversion, hashvalue, gitrevision):
        return {"database": dbname,
                "created": created,
                "Modelversion": modelversion,
                "JSONversion": jsonversion,
                "hashvalue": hashvalue,
                "git-revision": gitrevision,
                "comment": "Entries ending with + represent denormalized data and are not checked for consistency while reading back"
                }

    @classmethod
    def emptyjsonmodel(cls):
        retval={val: {} for val in JSModel._elemtype2label.values()}
        retval["_imprint_"] = cls.jsonimprint(dbname="",
                                   created=str(datetime.now()),
                                   modelversion="0.0",#parameters.expecteddbversion(),
                                   jsonversion="0.0",#str(parameters.jsonversion()),
                                   hashvalue=None,
                                   gitrevision='xxx')

        return retval

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
    def readfromfile(pfilename, pwithcheck=True):
        model = readjsonfile(pfilename=pfilename)

        return JSModel(pmodel=model, pwithversioncheck=pwithcheck, jsonfile=pfilename)

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

    def getentitycolor(self, pentiid, pcolortype="color"):
        enti = self.getbyid(pjsid=pentiid, ptype="entities")
        if enti is None:
            return None
        catg = self.getbyid(pjsid=enti["category"], ptype="categories")
        if catg is None or len(catg["ui"]) == 0:
            return None
        return catg["ui"][pcolortype]

    @property
    def jsfile(self):
        return self._jsfile

    def getdefaultlang(self):
        return self.jsmodel["model"]["language"]

    def getlangtext(self, pelem, plang, pidx=None, preplacement=True):
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
        assert ((type(pelem) is dict and (set(pelem.keys()) == set(self.jsmodel["languages"].keys())))
                or (type(pelem) is list and pidx is not None and (
                        set(pelem[pidx].keys()) == set(self.jsmodel["languages"].keys())))
                )
        if type(pelem) is list:
            elem = pelem[pidx]
        else:
            elem = pelem

        lang = plang.lower()
        deflang = self.getdefaultlang()

        val = nvl(elem.get(lang))
        if lang == deflang:
            return val  # default language is not handled

        if val == f"*{deflang}* {elem.get(deflang)}":
            val = ""

        # if val is empty, choose the replacement language text if chosen
        if val == "" and preplacement:
            replang = self.jsmodel["languages"].get(lang)["replacementlang"]
            if replang is not None:
                val = elem.get(replang)

        return val

    def getelemdescr(self, pjsid, ptype=None, plang=None):
        """returns a string describing an element found by id """
        elem = self.getbyid(pjsid=pjsid, ptype=ptype)
        if elem is None: return None
        lang = plang if plang is not None else self.getdefaultlang()
        if ptype == "relations":
            """rela-type, from-entiname, from-to assoc, to-entiname"""
            fromenti = self.getbyid(pjsid=elem["from-to"]["enti"], ptype="entities")
            toenti = self.getbyid(pjsid=elem["to-from"]["enti"], ptype="entities")
            return f"{elem['type']} {fromenti['name'][lang]} " + \
                   f"- {elem['from-to']['assoc'][lang]} - {toenti['name'][lang]}"

        else:
            return f"no description for element {ptype}:{pjsid}"


    def getbyid(self, pjsid, ptype=None):
        """return the element identified by the jsid (<type><id>) from the current mirojsmodel"""
        # check for id's which are not of the internal type (e.g. from external tools)
        if ptype is not None:
            for k, v in self.jsmodel[ptype].items():
                if k == pjsid:
                    return v
        try:
            return self.jsmodel[JSModel.elemtype2label(jsguid2type(pjsid))][pjsid]
        except:
            return None


    def getbyfield(self, ptype, pvalue, pfield='name', plang=None):
        """return tupels of (ID,element) of all elements containing the field pfield
            with a content of pvalue from the type of element current mirojsmodel
            returns empty list if nothing was found
        """
        retval = []
        for k, v in self.jsmodel[ptype].items():
            if (plang is None and v[pfield] == pvalue) or \
                    (plang is not None and v[pfield][plang] == pvalue):
                retval.append((k, v))
        # raise Exception(f"{ptype} : {pfield} : {pvalue}({plang}) not found ")
        return retval


    def elementui(self, diagid, elemtype, elemid):
        try:
            diag = self.jsmodel["diagrams"][diagid]
            if elemtype == "relationships":
                retval = diag[elemtype][elemid]
            else:
                uielement = [elem for elem in diag["elements"][elemtype] if elem["element"] == elemid]
                retval = uielement[0]
        except:
            retval = None
        return retval


    def getbysrcref(self, psrcname, psrcid) -> (str, dict):
        """ return the id and the structure of the element, identified by
        the external sourceref-id for the source called psrcname
        return None,None if not found
        """
        for elemtype in self.jsmodel.values():
            for key, elem in filter (lambda e : type(e[1]) is dict,
                                     elemtype.items()):
                #replaced by filter if type(elem) is not dict: continue
                sourceref = elem.get("sourceref")
                if sourceref is None: continue
                odmref = sourceref.get(psrcname)
                if odmref and (odmref[0] == psrcid):
                    return key, elem
        return None, None


    def isrecursive(self, pentiid):
        """ True, if the entitiy has a direct recursive relation
        """
        retval = False
        if pentiid in self.getelements("entities").keys():
            enti = self.getbyid(pentiid)
            if enti is not None:
                for relaid in enti["relations+"]:
                    # if one relation points to itself, set retval TRUE
                    rela = self.getbyid(relaid)
                    retval = retval or (rela["from-to"]["enti"] == pentiid == rela["to-from"]["enti"])
        return retval


    def issupertype(self, psupid, psubid):
        """
        True, if psupid is a supertypeentitiy on any level of psubid
        False otherwise
        """
        if psupid is None or psubid is None:
            return False
        retval = False
        subenti = self.getbyid(psubid)
        if subenti is None:
            # If the other entity is unavailable
            return False
        for newsubid in subenti["supertypes+"]:
            if (newsubid == psupid) or self.issupertype(psupid, newsubid):
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
            'datamodels': len(self.jsmodel['datamodels']),
            'tables': len(self.jsmodel['tables']),
            'columns': len(self.jsmodel['columns']),
        }


    def getjsversion(self) -> version.Version:
        if "_imprint_" not in self.jsmodel:
            jsversionstr = "0.0"
        else:
            jsversionstr = self.jsmodel["_imprint_"].get("JSONversion")
            if jsversionstr is None:
                jsversionstr = "0.0"

        jsversion = version.parse(jsversionstr)
        return jsversion

    def getdbfilepath(self) -> str:
        if "_imprint_" not in self.jsmodel:
            dbfilepath = None
        else:
            dbfilepath = self.jsmodel["_imprint_"].get("database")

        return dbfilepath


    # def equalversions(self, pcheckversion: str = None) -> bool:
    #     if pcheckversion is None:
    #         checkv = parameters.jsonversion()
    #     else:
    #         checkv = version.parse(pcheckversion)
    #     return checkv == self.getjsversion()


    # def compatibleversions(self, pcheckversion: str = None) -> bool:
    #     """
    #     json version are compatible  if major version is equal
    #     """
    #     if pcheckversion is None:
    #         checkv = parameters.jsonversion()
    #     else:
    #         checkv = version.parse(pcheckversion)
    #     return checkv.major == self.getjsversion().major


    def assertversion(self, pcheckversion: str = None):
        """
            breaks if jsonversion is not suitable
        """
        #assert self.compatibleversions(pcheckversion), \
        #    f"loaded json-Version {self.getjsversion().base_version} not covered by current json-version {parameters.jsonversion()}"
        return


    def upgradejson(self):
        """
            upgrades read json version step by step to json version given in parameters
            if no ugradefunction exists, raises Exception
        """

        def upgr00_10():
            print("upgrade 0.0 to 1.0")

        JSONVERSIONS = {"0.0": lambda x: None,
                        "1.0": upgr00_10}
        destversion = "0.0"#parameters.jsonversion()
        curversion = self.getjsversion()
        while curversion.__str__ < destversion:
            if curversion.major < destversion.major and curversion.minor < 99:
                curversion = version.Version(f"{curversion.major}.{curversion.minor + 1}")
            else:
                curversion = version.Version(f"{curversion.major + 1}.{0}")
            if str(curversion) in JSONVERSIONS.keys():
                JSONVERSIONS[str(curversion)]()

        return


def check_json_serialisable(structure: dict):
    def nest(element, path: str):
        if isinstance(element, dict):
            for key, value in element.items():
                full_path = path + '."' + str(key) + '"'
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
    return


def printJSON(pmodel, pfilepath, pfilename, psorted=False):
    destination = Path(pfilepath, jsonfilename(pfilename))
    return storeSPOD(pmodel, destination)

#
def storeSPOD(pmodel, destination, psorted=False) -> Path:
    check_json_serialisable(pmodel)
    with open(destination, 'w') as jsonfile:
        jsonfile.write(json.dumps(pmodel, indent=3))
    return destination

#
# def fillmodel(pmodel, pentries):
#     """
#     :param pmodel: ["name"...]
#     :param pentries: [value...]
#     :return: dictionary with position in list matching name-value pairs
#     """
#     if not pmodel or not pentries or (len(pmodel) != len(pentries)):
#         raise Exception("parameter mismatch (model: {}, entries: {})".format(len(pmodel), len(pentries)))
#     return {pmodel[idx]: val for idx, val in enumerate(pentries)}
#
#
# def initjselement(model, refmodel):
#     for key in refmodel:
#         if not key.endswith("+"):
#             model[key] = None
#     return model
#
#
# def fillargs(model, refmodel: list, **kwargs):
#     for arg, val in kwargs.items():
#         if arg in refmodel:
#             model[arg] = val
#         elif arg + "+" in refmodel:
#             model[arg + "+"] = val
#         elif arg + "#" in refmodel:
#             model[arg + "#"] = val
#         else:
#             #print(f"in function {callers_name()}: unknown attribute for jsonobject {arg}\n'{instr(refmodel)}")
#             logging.warning(f"in function {callers_name()}: unknown attribute for jsonobject: {arg}\n'{str(refmodel)}")
#     return model
#
#
# def warn_missing_translation(din: dict, dout: dict) -> None:
#     diff = set(dout.values()).difference(set(din.values()))
#     if len(diff) > 0:
#         languages = dict(filter(lambda i: i[1] is None, din.items()))
#         logging.warning(f"Patching missing translation for {languages.keys()} in {context.ctx}")
#     return
#
#
# def reflist(plist: list = None):
#     """ None = emptymodel"""
#     if plist is None:
#         return []
#     else:
#         return [e for e in plist]
#
#
# def tabreflist(plist: dict = None):
#     """ None = emptymodel"""
#     """ """
#     if plist is None:
#         return {'DATM000': ['TABL000']}
#     else:
#         return plist
#
#
# def colureflist(plist: dict = None):
#     """ None = emptymodel"""
#     """ """
#     if plist is None:
#         return {'DATM000': ['COLU000']}
#     else:
#         return plist
#
#
# def sourceref(pvalues: dict = None):
#     """ None = emptymodel"""
#     if pvalues is None:
#         return {"ODM": ["", ""]}
#     else:
#         return pvalues
#
#
#
# def userdefprops(pprops: dict = None):
#     """ None = emptymodel"""
#     """
#             "datamapping": {
#                "PENTA": {
#                   "UDPR206": {
#                      "name": "PENTA TabName",
#                      "value": null
#                   }
#                },
#                "PIM": {
#                   "UDPR201": {
#                      "name": "PIM TabName",
#                      "value": null
#                   }
#                }
#             },
#         """
#     if pprops is None:
#         return {'Theme': {"Group": {"UDPR000": {"name": '', "value": ''}}}}
#     else:
#         return pprops
#
#
# def rwstr(pread=True, pwrite=False):
#     return ''.join(rw(pread=pread, pwrite=pwrite))
#
#
# def rw(pread=True, pwrite=False):
#     if type(pread) == str:
#         pread = Boolean.str2bool(pread)
#     if type(pwrite) == str:
#         pwrite = Boolean.str2bool(pwrite)
#     retval = []
#     if pread:
#         retval.append('R')
#     if pwrite:
#         retval.append('W')
#     return retval
#
#
# def crudstr(pread=True, pupdate=False, pdelete=False, pcreate=False):
#     return ''.join(crud(pread=pread, pupdate=pupdate, pdelete=pdelete, pcreate=pcreate))
#
#
# def crud(pread=True, pupdate=False, pdelete=False, pcreate=False):
#     if type(pread) == str:
#         pread = Boolean.str2bool(pread)
#     if type(pcreate) == str:
#         pcreate = Boolean.str2bool(pcreate)
#     if type(pupdate) == str:
#         pupdate = Boolean.str2bool(pupdate)
#     if type(pdelete) == str:
#         pdelete = Boolean.str2bool(pdelete)
#     retval = []
#     if pcreate:
#         retval.append('C')
#     if pread:
#         retval.append('R')
#     if pupdate:
#         retval.append('U')
#     if pdelete:
#         retval.append('D')
#     return retval
