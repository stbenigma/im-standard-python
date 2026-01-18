import re

from IM_STANDARD import JsonElement, alwayslist, nvl, model2json


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
                "DATA": "Dataattributes",
                "COLU": "Columns",
                "SYST": "Systems",
                "DIAG": "Diagrams",
                "DIAE": "Diagram elements",
                "MAPP": "Mappings",
                "TRAF": "Transformations"
                }
    idmax = {key: 0 for key in OBJNAMES.keys()}

    @staticmethod
    def reset():
        ElementId.idmax = {key: 0 for key in ElementId.OBJNAMES.keys()}

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


class JsonSchema():
    """
    common functions and jsonstructures to be used in  jsonSchemas organized according to the standard
    """

    MAINELEMENTS = ["Entities", "Domains", "Categories",
                    "Attributes",
                    "Relations", 'BusinessRules'
        , "DataObjects", "DataAttributes", 'Systems']

    def __init__(self, model=None, **kwargs):
        self._model = (model if model is not None else
                       {"ModelInfo": None})  # create legal json-schema
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
    def targetenvironment(self):
        return self.jsonschemamodel["ModelInfo"]["targetenvironment"]

    @property
    def modelname(self):
        return self.jsonschemamodel["ModelInfo"]["modelname"]

    @property
    def curlang(self):
        return self._curlang

    @curlang.setter
    def curlang(self, val):
        self._curlang = val

    @property
    def modeldescr(self):
        return self.jsonschemamodel["ModelInfo"]["description"]

    @property
    def modeltype(self):
        return self.jsonschemamodel["ModelInfo"]["modeltype"]

    @property
    def mainlang(self):
        return self.jsonschemamodel["ModelInfo"]["mainlanguage"]

    @property
    def languages(self):
        """"
            return additional languages for model empty if nonexistent
        """
        if type(self.jsonschemamodel["ModelInfo"]) == dict:
            return alwayslist(self.jsonschemamodel["ModelInfo"].get("languages"))
        else: return alwayslist(self.jsonschemamodel["ModelInfo"]["languages"])

    @property
    def alllanguages(self):
        """"
            return additional languages for model
        """
        return self.languages + [self.mainlang]

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
            # is whish language in the dict
            if lang is not None and lang in value.keys():
                return value.get(lang)
            # is the current language of the generation in the dict
            if self.curlang is not None and self.curlang in value.keys():
                return value.get(self.curlang)
            # do we accept defaults and is the mainlanguage (=defaultlanguage) in the dict
            if default and self.mainlang in value.keys():
                return value.get(self.mainlang)
            # do we accept defaults and is their any language in the dict
            if default and len(value.keys()) > 0:
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

    def fillparentid(self, elem: JsonElement):
        """ fills $id into the element
             """
        if "$id" in elem.data: return
        if elem.elemtype in ("ModelInfo",):
            elem.setproperty("$id", f'{self.targetenvironment}:{self.modelname}')
        if elem.elemtype in ("Entity", "DataObject", "Domain", "BusinessRule"):
            elem.setproperty("$id", f'{self.targetenvironment}:{self.modelname}:{nvl(elem.getname(), elem.getid())}')
        elif elem.elemtype in ("Attribute", "DataAttribute"):
            parent = self.getbyid(elem[self.parentidfieldname(elem)])
            elem.setproperty("$id", f'{parent["$id"]}:{elem.getname()}')
        elif elem.elemtype in ("Category"):
            parentcatg = self.getbyid(elem[self.parentidfieldname(elem)])
            if parentcatg is None:
                parent = f'{self.targetenvironment}:{self.modelname}'
            else:
                if "$id" not in parentcatg.data:
                    self.fillparentid(parentcatg)
                parent = parentcatg["$id"]
            elem.setproperty("$id", f'{parent}:{elem.getname()}')
        elif elem.elemtype == "Relation":
            parent1 = self.getbyid(elem["fwd"].get("entityid"))
            parent2 = self.getbyid(elem["bwd"].get("entityid"))
            elem.setproperty("$id",
                             f'{parent1["$id"]}:{parent2.getname()}->{self.mlvalue(value=elem["fwd"]["assoctext"])}')
        elif elem.elemtype == "System":
            elem.setproperty("$id", f'{self.targetenvironment}:{elem.getname()}')
        return

    @staticmethod
    def parentidfieldname(elem: JsonElement):
        """ returns the parentid or whatever a parent is called in this element
            None if there is no parentprop or there is no partentid """
        if elem.elemtype in ("Entity", "DataObject", "Domain", "Category"):
            parentprop = "categoryid"
        elif elem.elemtype in ("Attribute"):
            parentprop = "parentid"
        elif elem.elemtype == "BusinessRule":
            parentprop = None
        elif elem.elemtype == "DataAttribute":
            parentprop = "dataobjectid"
        elif elem.elemtype == "Relation":
            parentprop = None
        elif elem.elemtype == "System":
            parentprop = None
        else:
            parentprop = None

        return parentprop

    def getpath(self, elem: JsonElement):
        """
        :param elem:
        :return the names of all parents separated by / up to the root.
                "" if object has no parent
                None if elem is None
        """
        if elem is None: return None
        retval = ""
        parentelem: JsonElement = self.getbyid(JsonSchema.parentidfieldname(elem))
        if parentelem is not None:
            retval += self.getpath(parentelem)
            retval += self.mlvalue(parentelem.getname())
            retval += "/"
        return retval

    def getfullpath(self, elem: JsonElement,
                    lang=None):
        """
        get the full path of an element from its name up to the model level, with all parents
        :return: /modelname/{parent.name/}/elementname
        """
        retval = f"{elem.getadditionalprop('SOURCE-MODEL')}:{self.getpath(elem=elem)}{self.mlvalue(value=elem.getname(), lang=lang)}"
        # TODO read all parents and define all names
        return retval

    def setschemaelement(self, name, val):
        self.jsonschemamodel[name] = val
        return

    def addelementinstance(self, name, val):
        """ add an instance to the element 'name'
        """
        # create element if not present
        self.jsonschemamodel.setdefault(name, [])
        if isinstance(val, list):
            self.jsonschemamodel[name].extend(val)
        elif isinstance(val, dict) or isinstance(val, JsonElement):
            self.jsonschemamodel[name].append(val)
        else:
            raise Exception(f"illegal type of value '{type(val)}'")
        return

    def getanyelementsbyfield(self, name,
                              field="name"):
        """
        find the name in the field of any element

        :param name: value to search for (multilingual)
        :param field: name of the field to search
        :return: list of all elements found
        """
        elements = []
        for elemtype in self.MAINELEMENTS:
            elements += self.getelementsbyfield(elementtype=elemtype,
                                                name=name, field=field)
        return elements

    def getanyelementbyfield(self, name,
                             field="name"):
        """
        find the name in the field in any element

        :param name: value to search for (multilingual)
        :param field: name of the field to search
        :return: [] if nothing found
                error if more than one was found
                element if exactly one was found
        """
        elements = self.getanyelementsbyfield(name=name, field=field)
        if len(elements) == 0:
            return []
        elif len(elements) > 1:
            raise Exception("Too many elements with {name} found")
        else:
            return elements[0]

    def getelementsbyfield(self, elementtype,
                           name,
                           field="name"):
        """
            get the elements of a certain type (Entities, Tables, Domains...)
            where the field is present and its value equals to name

        """
        elements = self.jsonschemamodel.get(elementtype, [])
        retval = [elem for elem in elements if self.mlvalue(elem[field]) == name]
        return retval

    def getelementbyfield(self,
                          elementtype,
                          name,
                          field="name"):
        """

        @param elementtype:  Entities, Relations, Attributes, Domains...
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

        if elementname in self.MAINELEMENTS:
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
        for elemtype in self.MAINELEMENTS:
            retval.extend([elem for elem in self.getelementinstances(elementname=elemtype)
                           if elem.getid() == elementid])

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
            if catg.getid() == catgid:
                catgtree.append(self.mlvalue(catg["name"]))
                catgtree = self.categorytree(catg["parent"]) + catgtree
        return catgtree

    def maketechnicalname(self, name):
        return re.sub(r'[^a-zA-Z0-9_$]', '', name)

    def _gettechnicalname(self, elem):
        return elem.get("technicalname",
                        self.maketechnicalname(self.mlvalue(
                            elem["name"])))  # TODO generate technical names in domainstechname=elem["technicalname""]

    def getjsonmodel(self, withids=True):
        """
        :parameter: withids add $id to every element read
        :return: the model in pure json (JsonElement replaced)
        """

        return model2json(model=self.jsonschemamodel, idfunc=self.fillparentid)
