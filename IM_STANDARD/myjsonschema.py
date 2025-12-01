
import re

from IM_STANDARD import JsonElements,alwayslist

class ElementId:
    """ give unique new id with every call"""
    OBJNAMES = {"ENTI": "Entities",
                "CATG": "Categories",
                "ATTR": "Attributes",
                "RELA": "Relations",
                "DOCU": "Documents",
                "DOMA": "Domains",
                "BURU": "BusinessRules",
                "DATO": "Dataobjects",
                "COLU": "Columns",
                "SYST": "Systems",
                "DIAG": "Diagrams",
                "DIAE": "Diagram elements",
                "TRAF": "Transformations"
                }
    idmax = {key: 0 for key in OBJNAMES.keys()}

    @staticmethod
    def reset():
        ElementId.idmax == {key: 0 for key in ElementId.OBJNAMES.keys()}

    @staticmethod
    def setnextid(objtype, id):
        if objtype in ElementId.idmax:
            ElementId.idmax[objtype] = id
        return

    @staticmethod
    def nextid(objtype):
        if objtype in ElementId.idmax:
            ElementId.idmax[objtype] += 1
            return objtype + str(ElementId.idmax[objtype])
        else:
            return '????0'

    @staticmethod
    def separateid(elementid):
        """
        :param elementid: ZZZZnn
        :return: ZZZZ,nn
        """
        return (elementid[0:4], elementid[4:])

    @staticmethod
    def idtype(elementid):
        """
        :param elementid: ZZZZnn
        :return: ZZZZ
        """
        return ElementId.separateid(elementid)[0]

    @staticmethod
    def idnumber(elementid):
        """
        :param elementid: ZZZZnn
        :return: nn
        """
        return ElementId.separateid(elementid)[1]

    @staticmethod
    def short2long(objname):
        return ElementId.OBJNAMES.get(objname)

    @staticmethod
    def long2short(objname):
        return {val: key for key, val in ElementId.OBJNAMES.items()}.get(objname)


class JsonSchema(JsonElements):
    """
    common functions and jsonstructures to be used in  jsonSchemas organized according to the standard
    """

    def __init__(self, model=None, **kwargs):
        self._model = model if model is not None else \
            {"ModelInfo": dict()} #create legal json-schema
        self._curlang = None
        return

    @property
    def jsonschemamodel(self):
        return self._model

    @jsonschemamodel.setter
    def jsonschemamodel(self, value):
        self._model = value
        return

    @property
    def modelname(self):
        return self.jsonschemamodel["ModelInfo"].get("modelname")

    @property
    def curlang(self):
        return self._curlang

    @curlang.setter
    def curlang(self, val):
        self._curlang = val

    @property
    def modeldescr(self):
        return self.jsonschemamodel["ModelInfo"].get("description")

    @property
    def modeltype(self):
        return self.jsonschemamodel["ModelInfo"].get("modeltype")

    @property
    def mainlang(self):
        return self.jsonschemamodel["ModelInfo"].get("mainlanguage")

    @property
    def languages(self):
        """"
            return additional languages for model empty if nonexistent
        """
        return self.jsonschemamodel["ModelInfo"].get("languages",[])

    @property
    def alllanguages(self):
        """"
            return additional languages for model
        """
        return self.languages+[self.mainlang]

    def modelismultilingual(self):
        return len(self.languages) > 0

    def mlvalue(self, value, lang=None, default=True):
        """Multilanguage value
            returns
                "" if value is None
                value if it is string
                if value ist dict:
                    value[lang] if lang is not None and lang in dict
                    value[curlang] if lang is None and curlang in dict
                    value[mainlanguage] if default = True
                    else return value of first element in value-list
            """
        if value is None:
            return ""
        elif type(value) is str:
            return value
        elif type(value) is dict:
            #is whish language in the dict
            if lang is not None and lang in value.keys():
                return value.get(lang)
            #is the current language of the generation in the dict
            if self.curlang is not None and self.curlang in value.keys():
                return value.get(self.curlang)
            #do we accept defaults and is the mainlanguage (=defaultlanguage) in the dict
            if default and self.mainlang in value.keys():
                return value.get(self.mainlang)
            # do we accept defaults and is their any language in the dict
            if default and len(value.keys())>0:
                return value.get(list(value.keys())[0])
        return value

    def multilangstring_is(self):
        """ "is" translated into a multilingual string """
        IS_TRANSL = {"de": "ist",
                     "en": "is",
                     "fr": "est",
                     "it": "e",
                     "es": "es"}

        def _istransl(lang):
            if lang in IS_TRANSL:
                return IS_TRANSL[lang]
            else:
                return self.IS_TRANSL["en"]

        if self.modelismultilingual():
            return {lang: _istransl(lang) for lang in self.alllanguages}
        else:
            return _istransl(self.mainlang)

    def setschemaelement(self, name, val):
        self.jsonschemamodel[name] = val
        return

    def addelementinstance(self, name, val):
        """ add an instance to the element 'name'
        """
        #create element if not present
        self.jsonschemamodel.setdefault(name, [])
        if type(val) == list:
            self.jsonschemamodel[name].extend(val)
        elif type(val) == dict:
            self.jsonschemamodel[name].append(val)
        else:
            raise Exception(f"illegal type of value '{type(val)}'")
        return

    def getelementsbyfield(self, elementtype,
                           name,
                           field="name"):
        """
            get the elements of a certain type (Entities, Tables, Domains...)
            where the field is present and its value equals to name

        """
        elements = self.jsonschemamodel[elementtype]
        retval = [elem for elem in elements if elem.get(field) == name]
        return retval

    def getelementbyfield(self,
                          elementtype,
                          name,
                          field="name"):
        """

        @param elementtype:  Dntities, Relations, Attributes, Domains...
        @param name: value to search for
        @param field: field in element containing the valu
        @return: the element , if exactly one was found
                    None, if none was found
                    an (assertion) error, if more than one was found
        """
        retval = self.getelementsbyfield(elementtype=elementtype,
                                         name=name,
                                         field=field)
        if len(retval) == 1:
            return retval[0]
        elif len(retval) == 0:
            return None
        else:
            assert False, f"more than 1 record found in {elementtype}.{field} {name}  "

    def getelementinstances(self, elementname):
        """
        @param elementname: name of the elementtype ("Entities, Attributes, Domains...)
        @return: [] if no elements exists or if type does not exist
                list of elements of the type.
                    for subelements like keys, columns
                        all instances from all father-elements are collected
                            and returned
        """

        def subelements(fathername, elementname):
            """
            @param fathername: name of the father element
            @param elementname: name of the elements in father strcuture
            @return: list of all elements of all fahterelemets
            """
            retval = []
            for father in self.getelementinstances(elementname=fathername):
                if elementname in father:
                    retval.extend(father[elementname])
            return retval

        if elementname in ("Entities", "Domains", "Categories",
                           "Attributes", "DataObjects",
                           "Relations", 'BusinessRules','Systems'
                           ):
            retval = self.jsonschemamodel.get(elementname, [])
        elif elementname in ("Keys"):
            retval = subelements(fathername="Entities",
                                 elementname=elementname.lower())
        elif elementname == "Columns":
            retval = subelements(fathername="DataObjects",
                                 elementname=elementname)
        else:
            retval = []
        return retval

    def getbyid(self, elementid):
        """get any element of any type with the given ID"
            as ID's contain elementtype (ENTI..., DOMA...)
            any ID iw unique over all type of elements
            """
        retval = []
        for elemtype in ("Entities", "Domains", "Categories",
                         "DataObjects", "Attributes", "Columns",
                         "Relations", "Columns", 'BusinessRules',
                         'Systems'
                         ):
            retval.extend([elem for elem in self.getelementinstances(elementname=elemtype)
                           if elem["elementid"] == elementid])

        assert len(retval) < 2, f"id {elementid} found twice"
        return retval[0] if len(retval) == 1 else None

    def categorytree(self, catgid):
        """ give a list from the top category (first element)
            along the parent id of the children
            down to the category identified by catgid
        """
        if catgid is None: return []
        catgtree = []
        for catg in alwayslist(self.getelementinstances(elementname="Categories")):
            if catg.get("elementid") == catgid:
                catgtree.append(self.mlvalue(catg.get("name")))
                catgtree = self.categorytree(catg.get("parent")) + catgtree
        return catgtree

    def maketechnicalname(self, name):
        return re.sub(r'[^a-zA-Z0-9_$]', '', name)

    def _gettechnicalname(self, elem):
        return elem.get("technicalname",
                   self.maketechnicalname(self.mlvalue(
                       elem.get("name"))))  # TODO generate technical names in domainstechname=elem.get("technicalname")

