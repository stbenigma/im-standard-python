import logging
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
                "MAPP": "Mappings",
                "TRAF": "Transformations"
                }
    idmax = {key: 0 for key in OBJNAMES.keys()}

    @staticmethod
    def reset():
        ElementId.idmax = {key: 0 for key in ElementId.OBJNAMES.keys()}

    @staticmethod
    def setnextid(objtype, objid):
        if objtype in ElementId.idmax:
            ElementId.idmax[objtype] = objid
        return

    @staticmethod
    def nextid(objtype):
        if objtype in ElementId.idmax:
            ElementId.idmax[objtype] += 1
            return objtype + str(ElementId.idmax[objtype])
        else:
            return '????0'

    @staticmethod
    def separateid(elementId):
        """
        :param elementId: ZZZZnn
        :return: ZZZZ,nn
        """
        return (elementId[0:4], elementId[4:])

    @staticmethod
    def idtype(elementId):
        """
        :param elementId: ZZZZnn
        :return: ZZZZ
        """
        return ElementId.separateid(elementId)[0]

    @staticmethod
    def idnumber(elementId):
        """
        :param elementId: ZZZZnn
        :return: nn
        """
        return ElementId.separateid(elementId)[1]

    @staticmethod
    def short2long(objname):
        return ElementId.OBJNAMES.get(objname)

    @staticmethod
    def long2short(objname):
        return {val: key for key, val in ElementId.OBJNAMES.items()}.get(objname)


class StandardSchema:
    MODELTYPES = {"IM": "Information model",
                  "DM": "Data model",
                  "AM": "Artefact model"}


    """
    contains basic functions to manage a json standard schema
    """

    def __init__(self, schema: dict):
        self._schema = schema
        return

    @property
    def schema(self):
        return self._schema

    def elements(self, elementname: str):
        """
        the list of elements in the standard structure
        (in case of ModelInfo, a dictionary)
        :param elementname:
        :return:
        """
        return self.schema.get(elementname,
                               dict() if elementname == "ModelInfo" else list()
                               )

    @staticmethod
    def getadditionalprop(struct, propname, defval=None):
        """
        returns a property of the additionalProps dictionary
        :param self:
        :param struct: strcture containing additionalProps
        :param propname: name of proerty in additionalProps
        :param defval: default value if not found
        :return:
        """
        return struct.get("additionalProps", dict()).get(propname, defval)

    @staticmethod
    def _mlvalue(value: dict, lang=None, defaultlang=None):
        """Multilanguage value
            returns
                None if value is None or empty dict
                value if value is not dict
                value[lang] if lang is not None and lang in dict
                value[default]lang] if lang is None and defaultlang in dict
                else return value of first element in value-list
            """
        if value is None:
            return None
        elif type(value) is dict:
            if len(value) == 0:
                return None
            else:
                if lang is not None and lang in value.keys():
                    return value.get(lang)
                if defaultlang is not None and defaultlang in value.keys():
                    return value.get(defaultlang)
                #language not found issue warning
                logging.warning(f"Languages '{lang}' and '{defaultlang}' not found in {value}")
                return list(value.values())[0]
        else:
            return value


    def getbyid(self, elemid: str):
        """
        returns an element with the given ID
        :param elemid:
        :return: None if not found, the element if found
        """
        for elemtype in ElementId.OBJNAMES.values():
            elem = self.getbyfield(elements=self._schema.get(elemtype, []),
                                   val=elemid,
                                   fieldname="elementId",
                                   unique=True)
            if elem is not None:
                return elem
        return None

    def getbyfield(self, elements: list,
                   val: str,
                   fieldname: str = "name",
                   fieldname2: str = None,
                   unique=False):
        """
        returns all elements with the given field-value
        :param: elements: list of elements-dicts to search
        :param val: value to search for
        :param fieldname: fieldname containing value
        :param fieldname2: name of a property in the property fieldname
        :prarm: unique: true, assumes unique, false assumes
        :return: None if not found and unique
                [] if not found and not unique
                 one element if 1 found and unique
                 a list of elements if found several times and not unique
                 an exception if found several and unique
        """
        retval = [elem for elem in elements
                  if val == (elem.get(fieldname)if fieldname2 is None
                             else elem.get(fieldname, dict()).get(fieldname2)
                             )
                  ]
        if unique and len(retval) == 1:
            return retval[0]
        elif unique and len(retval) == 0:
            return None
        elif unique and len(retval) > 1:
            raise Exception(f"more than 1 value for {fieldname}={val}")
        else:
            return retval


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
    def sourcehref(self):
        return self.jsonschemamodel.get("ModelInfo", dict()).get("additionalProps", {}).get('SOURCE-HREF')

    @property
    def targetenvironment(self):
        return self.jsonschemamodel.get("ModelInfo", dict())["targetEnvironment"]

    @property
    def modelname(self):
        return self.jsonschemamodel.get("ModelInfo", dict())["modelName"]

    @property
    def curlang(self):
        return self._curlang

    @curlang.setter
    def curlang(self, val):
        self._curlang = val

    @property
    def modelversion(self):
        return self.jsonschemamodel["ModelInfo"].get("modelVersion")

    @property
    def modeldescr(self):
        return self.jsonschemamodel["ModelInfo"].get("description")

    @property
    def modeltype(self):
        return self.jsonschemamodel["ModelInfo"]["modelType"]

    @property
    def mainlang(self):
        return self.jsonschemamodel["ModelInfo"]["mainLanguage"]

    @property
    def languages(self):
        """"
            return additional languages for model empty if nonexistent
        """
        if type(self.jsonschemamodel["ModelInfo"]) == dict:
            return alwayslist(self.jsonschemamodel["ModelInfo"].get("languages"))
        else:
            return alwayslist(self.jsonschemamodel["ModelInfo"]["languages"])

    @property
    def alllanguages(self):
        """"
            return additional languages for model
        """
        return self.languages + [self.mainlang]

    def modelismultilingual(self):
        return len(self.languages) > 0

    @staticmethod
    def _mlvalue(value: dict, lang=None, defaultlang=None):
        """Multilanguage value
            returns
                None if value is None or empty dict
                value if value is not dict
                value[lang] if lang is not None and lang in dict
                value[default]lang] if lang is None and defaultlang in dict
                else return value of first element in value-list
            """
        if value is None:
            return None
        elif type(value) is dict:
            if len(value) == 0:
                return None
            else:
                if lang is not None and lang in value.keys():
                    return value.get(lang)
                if defaultlang is not None and defaultlang in value.keys():
                    return value.get(defaultlang)
                return list(value.values())[0]
        else:
            return value

    def mlvalue(self, value, lang=None, default=True):
        """Multilanguage value
            returns
                "" if value is None
                value if it is no dict
                if value is dict:
                    value[lang] if lang is not None and lang in dict
                    value[self.curlang] if lang is None and curlang in dict
                    value[self.mainlanguage] if default = True
                    else return value of first element in value-list
            """
        return nvl(self._mlvalue(value=value,
                                 lang=lang if lang is not None else self.curlang,
                                 defaultlang=None if not default else self.mainlang
                                 ))

    def multilangstring_is(self, stdstr="is"):
        """ "is" translated into a multilingual string """
        IS_TRANSL = {"de": "ist",
                     "en": "is",
                     "fr": "est",
                     "it": "e",
                     "es": "es"}
        CONTAINS_TRANSL = {"de": "enthält",
                           "en": "contains",
                           "fr": "contien",
                           "it": "contiene",
                           "es": "contiene"}

        def _istransl(lang):
            if lang in translstr:
                return translstr[lang]
            else:
                return translstr["en"]

        assert stdstr in ("is", "contains")
        if stdstr == 'is':
            translstr = IS_TRANSL
        elif stdstr == "contains":
            translstr = CONTAINS_TRANSL

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
            parent1 = self.getbyid(elem["fwd"].get("entityId"))
            parent2 = self.getbyid(elem["bwd"].get("entityId"))
            elem.setproperty("$id",
                             f'{parent1["$id"]}:{parent2.getname()}->{self.mlvalue(value=elem["fwd"]["assocText"])}')
        elif elem.elemtype == "System":
            elem.setproperty("$id", f'{self.targetenvironment}:{elem.getname()}')
        return

    @staticmethod
    def parentidfieldname(elem: JsonElement):
        """ returns the parentid or whatever a parent is called in this element
            None if there is no parentprop or there is no partentid """
        if elem.elemtype in ("Entity", "DataObject", "Domain", "Category"):
            parentprop = "categoryId"
        elif elem.elemtype in ("Attribute"):
            parentprop = "parentId"
        elif elem.elemtype == "BusinessRule":
            parentprop = None
        elif elem.elemtype == "DataAttribute":
            parentprop = "dataObjectId"
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

        parentelem: JsonElement = self.getbyid(elem[JsonSchema.parentidfieldname(elem)])
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

    def getbyid(self, elementId):
        """get any element of any type with the given ID"
            as ID's contain elementtype (ENTI..., DOMA...)
            any ID iw unique over all type of elements
            """
        retval = []
        for elemtype in self.MAINELEMENTS:
            retval.extend([elem for elem in self.getelementinstances(elementname=elemtype)
                           if elem.getid() == elementId])

        assert len(retval) < 2, f"id {elementId} found twice"
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
        return elem.get("technicalName",
                        self.maketechnicalname(self.mlvalue(
                            elem["name"])))  # TODO generate technical names in domainstechname=elem["technicalName""]

    def getjsonmodel(self, withids=True):
        """
        :parameter: withids add $id to every element read
        :return: the model in pure json (JsonElement replaced)
        """

        return model2json(model=self.jsonschemamodel, idfunc=self.fillparentid)
