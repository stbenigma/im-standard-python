import json
import logging
import re
import unicodedata
from collections import Counter

from IM_STANDARD import nvl, StandardJsonModel, StandardSchema

JSON_MASTER_SCHEMA = "https://json-schema.org/draft/2020-12/schema"
SCHEMA_FILENAME_END = "{name}.schema.json"
DOMAIN_SIMPLETYPE_MAP = {"integer": "integer",
                         "decimal": "number",
                         "number": "number",
                         "text": "string",
                         "string": "string",
                         "boolean": "boolean",
                         "date": "string",
                         "datetime": "string"}

"""
    generate a json-schema and a json-sample file out of a standard model json file
    assume jsonstruct is validated against the standard IM schema
"""


def initLower(text):
    return None if text is None else text[:1].lower() + text[1:]


def normalizestring(text):
    normalized = unicodedata.normalize('NFKD', text)
    # Filtert alle Zeichen heraus, die keine reinen Buchstaben sind (die "Pünktchen")
    return "".join([c for c in normalized if not unicodedata.combining(c)])


class Json2JsonSchema:
    # TODO für alle "x-samm-aspect-model-urn": "urn:samm:BatteryPass:1.0.0#Circularity",

    def __init__(self, jsonstruct):
        self.jsstruct = StandardSchema(jsonstruct)
        self.language = self.jsstruct.schema.get("ModelInfo",dict()).get("mainLanguage")
        self.mainlanguage = self.jsstruct.schema.get("ModelInfo",dict()).get("mainLanguage")

        return

    @staticmethod
    def getadditionalprop(struct, propname, defval=None):
        """
        returns a property of the object "additionanProps" in struct or defval if it is None
        """
        return StandardSchema.getadditionalprop(struct=struct,
                                               propname=propname,
                                               defval=defval)

    def getelemuuid(self, struct):
        """
            construct an UUID for the element
            constructed from the schema's nid + the UUID of the source element
        """
        return f'{self.nid}:{nvl(self.getadditionalprop(struct=struct, propname="SOURCE-ID"))}'

    @staticmethod
    def urn(nid, localid):
        """build an urn as urn:nid:localid"""
        return f"urn:{nid}:{localid}"

    @staticmethod
    def urnid(model, name, version=None):
        lversion = f":{version}" if version is not None else ""
        return f"{model}{lversion}#{name}"

    @staticmethod
    def _startdash(value: str):
        """
        replaces a leading _ to a $
            or to nothing for _type
        """
        if value == "_type":
            return value[1:]
        elif value.startswith('_'):
            return '$' + value[1:]
        else:
            return value

    @staticmethod
    def _fulldict(**kwargs):
        """returns a dictionry of all kwargs.
            if a key is starts with _ it is changed into $..
            if a key equals _type it is changed into type
        """
        return Json2JsonSchema._conddict(**kwargs)

    @staticmethod
    def _conddict(condition=lambda x: True, **kwargs):
        """returns a dictionry with all kwargs. for which condition (val) holds true
            if a key is starts with _ it is changed into $..
            if a key equals _type it is changed into type
        """
        return {Json2JsonSchema._startdash(key): val for key, val in kwargs.items() if condition(val)}

    @staticmethod
    def _notnulldict(**kwargs):
        """returns a dictionry with all kwargs with a value which is neiter None,"" ,[],{}
            if a key is starts with _ it is changed into $..
            if a key equals _type it is changed into type
        """
        notnullval = lambda val: (val or val == 0 or isinstance(val, bool))  # val not in [None,"",[],{}]
        return Json2JsonSchema._conddict(condition=notnullval, **kwargs)

    def addobject(self, entry, subcat, **kwargs):
        defs = self.jsschemastruct["components"][subcat]
        if entry in defs: return
        defs[entry] = self._notnulldict(**kwargs)
        return f"#/components/{subcat}/{entry}"

    # def setdefsobject(self, entry, **kwargs):
    #    return self.addobject(entry=entry, subcat="$defs", **kwargs)

    def addproperty(self, entry, subcat, **kwargs):
        defs = self.jsschemastruct["components"][subcat]
        assert entry in defs, f"object {entry} does not exist"
        defs[entry].update(self._notnulldict(**kwargs))
        return

    def addschemaproperty(self, entry, **kwargs):
        self.addproperty(entry=entry, subcat="schemas", **kwargs)

    def adddefsproperty(self, entry, **kwargs):
        self.addproperty(entry=entry, subcat="$defs", **kwargs)

    def setschemaobject(self, entry, **kwargs):
        return self.addobject(entry=entry, subcat="schemas", **kwargs)

    def getobject(self, objid):
        """ returns the object identified by objid, None and an error log if not found
        """
        if objid is None:
            return None
        obj = self.jsstruct.getbyid(elemid=objid)
        if obj is None:
            logging.error(f"Object (id={objid}) not found.")
        return obj

    @property
    def isassetmodel(self):
        return self.jsstruct.elements("ModelInfo").get("modelType") == "Artefact model"

    def getmlvalue(self, struct):
        """
        returns lang-value in struct
        :param struct: of form {"de":"abc", "en":"aby" }
        :return: None if struct is None or empty dict or neither self.language nor self.mailanguage are in struct
                struct if is of type "str"
                struct[self.language] if self.language in struct
                struct[self.mainlanguage] if self.mainlanguage in struct
                struct[first entry]
        """
        if struct is None or struct == {}:
            return None
        elif isinstance(struct, str):
            return struct
        elif isinstance(struct, dict):
            return StandardSchema._mlvalue(value=struct,
                                           lang=self.language,
                                           defaultlang=self.mainlanguage)
        else:
            assert False, f"multilingual of ??{type(struct)}??"

    def fillmodel(self, catgs):
        self.toplevelname = self.modelname
        children = dict()
        for catg in catgs:
            self.addcategory(dest=children, catg=catg)

        self.jsschemastruct.update(
            self._notnulldict(
                description=self.jsstruct.schema.elements("ModelInfo").get("description",
                                                                           "Group of elements")),
            type="object",
            properties=children,
            required=list(children.keys())
        )
        self.jsschemastruct["urn"] = self.urn(nid=self.nid,
                                              localid=self.urnid(
                                                  model=self.toplevelname,
                                                  name=self.toplevelname,
                                                  version=self.modelversion)
                                              )
        return


    def addcategory(self, dest, catg):
        objname = self.getname(catg)
        refobj = self.setschemaobject(entry=objname,
                                      description=catg.get("description", "Grouping elements"),
                                      type="object"
                                      )
        children = self.categorychildren(catg)
        self.addschemaproperty(entry=objname
                               , properties=children,
                               required=list(children.keys()))

        dest[objname] = self._notnulldict(description=catg.get("description", "Group of elements"),
                                          _ref=refobj)
        return refobj

    def builddomain(self, doma):
        domaname = self.getname(doma)
        pattern = doma.get("pattern")
        minLength = doma.get("minLength")
        maxLength = doma.get("maxLength")
        unit = doma.get("unit")
        minimum = doma.get("minimum",doma.get("minValue"))
        maximum = doma.get("maximum",doma.get("maxValue"))
        totalDigits = doma.get("totalDigits")
        fractDigits = doma.get("fractDigits")
        lformat = None
        enum = None
        properties = None
        mandatory = None
        if doma.get("domainType") == "TextDomain":
            objtype = "string"
        elif doma.get("domainType") == "GroupDomain":
            objtype = "object"
            properties, mandatory = self.getattributes(doma)
        elif doma.get("domainType") == "BooleanDomain":
            objtype = "boolean"
        elif doma.get("domainType") == "LOVDomain":
            objtype = "string"
            enum = [v.get("value") for v in doma.get("values", list())]
        elif doma.get("domainType") == "NumericDomain":
            if nvl(fractDigits, 0) == 0:
                objtype = "integer"
            else:
                objtype = "decimal"
                if nvl(fractDigits,0)>0:
                    pattern=f"\d*\.\d{{0:{str(fractDigits)}}}"
        elif doma.get("domainType") == "DatetimeDomain":
            objtype = "string"
            if doma.get("granularity") in ("DAY"):
                lformat = "date"
            elif doma.get("granularity") in ("HOUR", "MINUTE",
                                             "SECOND", "MILISECOND"):
                lformat = "date-time"
        else:
            objtype = "???"
            logging.warning(f"datatype '{doma.get('domainType')}' not yet handled")
        domaref = self._notnulldict(_type=objtype,
                                    pattern=pattern,
                                    minLength=minLength,
                                    maxLength=maxLength,
                                    format=lformat,
                                    minimum=minimum,
                                    maximum=maximum,
                                    unit=unit,
                                    enum=enum,
                                    properties=properties,
                                    required=mandatory,
                                    examples=doma.get("examples"),
                                    references=self.getderivations(doma)
                                    )
        return domaref

    def _elemschemafilename(self, elem: dict) -> str:
        """
        return link to json-schema-file for this element
        :param elem:
        :return:
        """
        return SCHEMA_FILENAME_END.format(name=self.getname(elem))

    def getattributes(self, enti):
        attributes = dict()
        mandatory = []
        attrs = self.jsstruct.getbyfield(elements=self.jsstruct.elements("Attributes"),
                                         val=enti.get("elementId"),
                                         fieldname="parentId")
        attrs.sort(key=lambda x: x.get("displaySeq", 9999))
        for attr in attrs:
            objname = initLower(self.getname(attr))

            doma = self.getobject(objid=attr.get("domainId"))
            if doma is None:
                typeref = None
            elif doma.get("elementId") in self.multiuseddomains:
                # create reference to domain
                typeref = {"$ref": self.domaref(doma)}
            else:
                # do domain inline in attribute
                typeref = self.getname(doma).lower()
                typeref=self.builddomain(doma=doma)
                #if typeref in DOMAIN_SIMPLETYPE_MAP:
                #    typeref = DOMAIN_SIMPLETYPE_MAP[typeref]
                #else:
                #   do inattribute type definition
                #  typeref = "ein typ zu definiern"  # self._builddomain(doma=doma)
            example = attr.get("examples")
            attrstruct = self._notnulldict(description=self.getmlvalue(attr.get("description")),
                                           title=self.getmlvalue(attr.get("toolTip")),
                                           _id=self.getelemuuid(attr),
                                           examples=example,
                                           references=self.getderivations(attr)
                                           )
            if attr.get("cardinality") in (None, "1", "one"):
                if typeref is not None:
                    attrstruct |= typeref
            else:
                attrstruct["type"] = "array"
                if typeref is not None:
                    attrstruct["items"] = [typeref]
            if attr.get("mandatory"):
                mandatory.append(objname)
            attributes[objname] = attrstruct
        return attributes, mandatory

    def getrelaname(self, assoc, entiname, ):
        return re.sub(r'[^a-zA-Z0-9$_]', '', assoc) + \
               re.sub(r'[^a-zA-Z0-9$_]', '', entiname)

    def getderivations(self, enti):
        refs = []
        for ref in self.jsstruct.getbyfield(elements=self.jsstruct.elements("Derivations"),
                                            val=enti.get("elementId"),
                                            fieldname="targetElement"):
            refs.append(ref.get("sourceElement"))
        return list(set(refs))

    def getroles(self, enti):
        roles = dict()
        # TODO return mandatory as well (similar in getattributes)
        # TODO protect arc with oneOf
        for rela in self.jsstruct.getbyfield(elements=self.jsstruct.elements("Relations"),
                                             val="ROLE",
                                             fieldname="relationType"):
            fwd, bwd = rela.get("fwd"), rela.get("bwd")
            if fwd.get("entityId") == enti.get("elementId") and \
                    fwd.get("mandatory"):
                otherenti = self.getobject(objid=bwd.get("entityId"))
                entiname = self.getmlvalue(otherenti.get('name'))
                roles[entiname] =self._notnulldict(description=f"{self.getmlvalue(fwd.get('assocText'))} " + \
                                                           f"{self.getmlvalue(otherenti.get('name'))} ",
                                               _id=self.getelemuuid(rela),
                                               type={"$ref": self.entiref(enti=otherenti)}
                                               )
            elif bwd.get("entityId") == enti.get("elementId") and \
                    bwd.get("mandatory"):
                otherenti = self.getobject(objid=fwd.get("entityId"))
                entiname = self.getmlvalue(otherenti.get('name'))
                roles[entiname]=self._notnulldict(description=f"{self.getmlvalue(bwd.get('assocText'))} " + \
                                                           f"{self.getmlvalue(otherenti.get('name'))} ",
                                               _id=self.getelemuuid(rela),
                                               type={"$ref": self.entiref(enti=otherenti)}
                                               )

        return roles

    def getsubtypes(self, enti) -> list:
        subtypes = dict()
        # TODO return mandatory as well (similar in getattributes)
        # TODO protect arc with oneOf
        for rela in self.jsstruct.getbyfield(self.jsstruct.elements("Relations"),
                                             val="SUBTYPE",
                                             fieldname="relationType"):
            fwd, bwd = rela.get("fwd"), rela.get("bwd")
            if fwd.get("entityId") == enti.get("elementId") and \
                    fwd.get("arcNumber") is not None:
                otherenti = self.getobject(objid=bwd.get("entityId"))
                entiname = self.getmlvalue(otherenti.get('name'))
                subtypes[entiname] = self._notnulldict(description=f"{self.getmlvalue(fwd.get('assocText'))} " + \
                                                                   f"{entiname} ",
                                                       _id=self.getelemuuid(rela),
                                                       type={"$ref": self.entiref(enti=otherenti)}
                                                       )

            elif bwd.get("entityId") == enti.get("elementId") and \
                    bwd.get("arcNumber") is not None:
                otherenti = self.getobject(objid=fwd.get("entityId"))
                entiname = self.getmlvalue(otherenti.get('name'))
                subtypes[entiname]=self._notnulldict(description=f"{self.getmlvalue(bwd.get('assocText'))} " + \
                                                              f"{self.getmlvalue(otherenti.get('name'))} ",
                                                  _id=self.getelemuuid(rela),
                                                  type={"$ref": self.entiref(enti=otherenti)}
                                                  )

        return subtypes

    def getM2Nrelations(self, enti):
        for rela in self.jsstruct.getbyfield(elements=self.jsstruct.elements(elementname="Relations"),
                                             val="M:N",
                                             fieldname="relationType"):
            logging.warning(f"Relations of type {rela.get('relationType')} not yet implemented")
        return None, None

    def getfunctionalrelations(self, enti):
        """ get all relations
            where this entity is a many-side of a M:1 relationship
            add an fk-attribute
            """
        fkattrs = dict()
        mandatory = []
        # TODO return mandatory as well (similar in getattributes)
        # TODO protect arc with oneOf
        relations = self.jsstruct.elements("Relations")
        for rela in self.jsstruct.getbyfield(elements=relations,
                                             val="M:1",
                                             fieldname="relationType") + \
                    self.jsstruct.getbyfield(elements=relations,
                                             val="1:1",
                                             fieldname="relationType"):
            fwd, bwd = rela.get("fwd"), rela.get("bwd")
            if fwd.get("entityId") == enti.get("elementId") and \
                    fwd.get("cardinality") == '1' and \
                    bwd.get("cardinality") in ('M', '1'):
                otherenti = self.getobject(objid=bwd.get("entityId"))
                relaname = self.getrelaname(assoc=self.getmlvalue(fwd.get('assocText')),
                                            entiname=self.getmlvalue(otherenti.get('name')))
                fkattrs[relaname] = self._notnulldict(description=f"{self.getmlvalue(fwd.get('assocText'))} " + \
                                                                  f"{self.getmlvalue(otherenti.get('name'))} ",
                                                      _id=self.getelemuuid(rela),
                                                      type={"$ref": self.entiref(enti=otherenti)}
                                                      )
                if fwd.get("mandatory"): mandatory.append(relaname)
            elif bwd.get("entityId") == enti.get("elementId") and \
                    bwd.get("cardinality") == '1' and \
                    fwd.get("cardinality") == 'M':
                otherenti = self.getobject(objid=fwd.get("entityId"))
                relaname = self.getrelaname(assoc=self.getmlvalue(bwd.get('assocText')),
                                            entiname=self.getmlvalue(otherenti.get('name')))
                fkattrs[relaname] = self._notnulldict(description=f"{self.getmlvalue(bwd.get('assocText'))} " + \
                                                                  f"{self.getmlvalue(otherenti.get('name'))} ",
                                                      _id=self.getelemuuid(rela),
                                                      type={"$ref": self.entiref(enti=otherenti)}
                                                      )
                if bwd.get("mandatory"): mandatory.append(relaname)

        return fkattrs, mandatory

    def getallrelations(self, enti):
        """ get all relations
            where this entity is a many-side of a M:1 relationship
            add an fk-attribute
            """
        fkattrs = dict()
        mandatory = []
        # TODO return mandatory as well (similar in getattributes)
        # TODO protect arc with oneOf
        for rela in [c for c in self.jsstruct.elements("Relations") if c.get("relationType") in ("M:1", "1:1")]:
            fwd, bwd = rela.get("fwd"), rela.get("bwd")
            if fwd.get("entityId") == enti.get("elementId") and \
                    fwd.get("cardinality") in ('M', '1') and \
                    bwd.get("cardinality") in ('1'):
                otherenti = self.getobject(objid=bwd.get("entityId"))
                relaname = self.getrelaname(assoc="",  # self.getmlvalue(fwd.get('assocText')),
                                            entiname=self.getmlvalue(otherenti.get('name')))
                # TODO resolve property attributes as roles names z.B. assoctext weglassen nächste Zeile
                fkattrs[relaname] = self._notnulldict(description=f"{self.getmlvalue(fwd.get('assocText'))} " + \
                                                                  self.getmlvalue(otherenti.get('name')),
                                                      title=self.getmlvalue(otherenti.get('shortDescr')),
                                                      _id=self.getelemuuid(rela),
                                                      **self.refobject(objref=self.entiref(enti=otherenti),
                                                                       singleobj=fwd.get("cardinality") == '1',
                                                                       minitems=1 if fwd.get("mandatory") else None)
                                                      )
                if fwd.get("mandatory"): mandatory.append(relaname)
            elif bwd.get("entityId") == enti.get("elementId") and \
                    bwd.get("cardinality") == ('M', '1') and \
                    fwd.get("cardinality") == '1':
                otherenti = self.getobject(objid=fwd.get("entityId"))
                relaname = self.getrelaname(assoc="",  # self.getmlvalue(bwd.get('assocText')),
                                            entiname=self.getmlvalue(otherenti.get('name')))
                # TODO resolve property attributes as roles names
                fkattrs[relaname] = self._notnulldict(description=f"{self.getmlvalue(bwd.get('assocText'))} " + \
                                                                  self.getmlvalue(otherenti.get('name')),
                                                      title=self.getmlvalue(otherenti.get('shortDescr')),
                                                      _id=self.getelemuuid(rela),
                                                      **self.refobject(objref=self.entiref(enti=otherenti),
                                                                       singleobj=bwd.get("cardinality") == '1',
                                                                       minitems=1 if bwd.get("mandatory") else None)

                                                      )
                if bwd.get("mandatory"): mandatory.append(relaname)
        return fkattrs, mandatory

    def getname(self, struct):
        return normalizestring(self.getadditionalprop(struct=struct,
                                                      propname="TechnicalName",
                                                      defval=self.getmlvalue(struct.get("name", "???"))
                                                      )).replace(" ", "")

    def entiref(self, enti):
        self.usedentities.add(enti.get("elementId"))
        return self._elemschemafilename(enti)

    def domaref(self, doma):
        self.useddomains.add(doma.get("elementId"))
        return self._elemschemafilename(doma)

    def buildentity(self, enti):

        children, mandatory = self.getattributes(enti)
        if self.isassetmodel:
            fkchildren, fkrelamandatory = self.getallrelations(enti)
        else:
            fkchildren, fkrelamandatory = self.getfunctionalrelations(enti)
            mnchildren, mnrelamandatory = self.getM2Nrelations(enti)

        children.update(fkchildren)
        mandatory.extend(fkrelamandatory)

        # Material component hat subtypes statt rollen
        subtypes = self.getsubtypes(enti)
        rolesof = self.getroles(enti)
        # TODO required abhängig vom mandatory
        entistruct = self._notnulldict(
            _type="object")

        allelements = {"properties": dict(),
                       "required": list()}

        if len(children) > 0:
            allelements["properties"] |= children
            allelements["required"] += mandatory
        if len(rolesof) > 0:
            allelements["properties"] |= rolesof
        if len(subtypes) > 0:
            allelements["properties"] |= subtypes
            allelements["oneOf"] = [{"required": [subt]} for subt in subtypes.keys()]
        # "oneOf": [
        #     {"required": ["substance"]},
        #     {"required": ["mixture"]}
        # ],

        entistruct |= allelements
        entistruct |= self._notnulldict(examples=enti.get("examples"))
        entistruct["references"] = self.getderivations(enti)
        return entistruct

    def adddomain(self, doma):
        objname = self.getname(doma)
        domastruct = self._genschemafiletemplate(descr=self.getmlvalue(doma.get("description")),
                                                 title=self.getmlvalue(doma.get("shortDescr")),
                                                 urn=self.urn(nid=self.nid,
                                                              localid=self.urnid(
                                                                  model=objname,
                                                                  name=objname,
                                                                  version=self.modelversion
                                                              )),
                                                 sourcelink=self.getadditionalprop(struct=doma,
                                                                                   propname="SOURCE_LINK"))
        domastruct |= self.builddomain(doma=doma)
        return domastruct

    def addentity(self, enti):
        objname = self.getname(enti)
        entistruct = self._genschemafiletemplate(descr=self.getmlvalue(enti.get("description")),
                                                 title=self.getmlvalue(enti.get("shortDescr")),
                                                 urn=self.urn(nid=self.nid,
                                                              localid=self.urnid(
                                                                  model=self.toplevelname,
                                                                  name=objname,
                                                                  version=self.modelversion
                                                              )),
                                                 _type="object",
                                                 sourcelink=self.getadditionalprop(struct=enti,
                                                                                   propname="SOURCE_LINK"))
        entistruct |= self.buildentity(enti=enti)
        return entistruct

    def refobject(self, objref, singleobj: bool = False,
                  unique: bool = None,
                  minitems: int = None,
                  maxitems: int = None):
        if singleobj:
            retval = {"_type": {"$ref": objref}}
        else:
            retval = self._notnulldict(_type="array",
                                       items={"$ref": objref},
                                       minItems=None if minitems is None else int(minitems),
                                       maxItems=None if maxitems is None else int(maxitems),
                                       uniqueItems=None if unique is None else unique
                                       )
        return retval

    def categorychildren(self, catg):
        children = dict()
        # catgchildren
        for catgchild in [c for c in self.jsstruct.elements("Categories") \
                          if c.get("categoryType") == "ENTITY" and \
                             c.get("categoryId") == catg.get("elementId")]:
            self.addcategory(dest=children, catg=catgchild)
        # entichildren
        for entichild in self.jsstruct.getbyfield(elements=self.jsstruct.elements("Relations"),
                                                  val=catg.get("elementId"),
                                                  fieldname="categoryId"):
            refenti = self.addentity(enti=entichild)
            refobject = self.refobject(refenti,
                                       singleobj=False,
                                       unique=True)
            assert "type" in refobject, "refobject enthält immer _type"
            children[self.getname(entichild)] = \
                self._notnulldict(description=entichild.get("description"),
                                  **refobject)

        return children

    def _notreferenced(self, entiid) -> bool:
        """
        returns True if the entiid is used in a fwd or bwd relationshipend
        :param entiid:
        :return:
        """
        return 0 == len([rela for rela in self.jsstruct.elements(elementname="Relations")
                         if entiid in (rela.get("fwd", {}).get("entityId"),
                                       rela.get("bwd", {}).get("entityId"))
                         ]
                        )

    def _genschemafiletemplate(self, descr: str,
                               urn: dict,
                               title: str = None,
                               _type:str = None,
                               **kwargs):
        # toplevel schema
        return self._fulldict(
            _schema=self._schema,
            _id=nvl(urn,
                    self.urn(nid=self.nid,
                             localid=self.urnid(
                                 model=self.toplevelname,
                                 name=self.toplevelname,
                                 version=self.modelversion
                             )
                             )
                    ),
            **kwargs) | self._notnulldict(title=title,
                                          description=descr,
                                          _type=_type,
                                          additionalProperties=False if _type =="object" else None
                                          )

    def _unrefentis(self, catgid=None):
        """
        get all entityids  of the input structure
        catgid != None look only or entities in this category
        """
        return [enti.get("elementId") for enti in self.jsstruct.elements(elementname="Entities") \
                if ((catgid is None or enti.get("categoryId") == catgid))
                ]

    def _domainhasrestriction(self, doma: dict) -> bool:
        """
        returns true if the domain has any restriction of length or pattern

        :param doma:
        :return:
        """
        pass
        return set([doma.get(restrict) for restrict in ["minValue", "maxValue",
                                                        "totalDigits",
                                                        "fractDigits", "roundValue", "unit",
                                                        "minLength", "maxLength", "syntaxRule",
                                                        "minDate", "maxDate", "granularity",
                                                        "contentType", "binaryFileType"]]) != set([None])

    def _getownobjectdomains(self) -> list:
        """
        returns list of domainId's which get an own json-schema file
        Domains used in more than one attribute
                unless they are simpletypes (string, integer) without any redstrictions
            or which are group domains
            or are lov domains having more than 5 values
        :return:
        """
        countdomas = Counter([attr.get("domainId") for attr in self.jsstruct.elements("Attributes")
                              if attr.get("domainId") is not None])
        return [doma.get("elementId") for doma in self.jsstruct.elements("Domains") \
                if (doma.get("elementId") in [domaid for domaid, cnt in countdomas.items()
                                              if (cnt > 1 and
                                                  (self._domainhasrestriction(doma)
                                                   or (self.getname(doma).lower() not in DOMAIN_SIMPLETYPE_MAP)
                                                   ) and
                                                  (doma.get("domainType") not in (
                                                      "LOVDomain", "GroupDomain", "Boolean"))
                                                  )]
                    )
                or (doma.get("domainType") == "GroupDomain")
                or (doma.get("domainType") == "LOVDomain" and len(doma.get("values", [])) > 5)
                ]

    def generate(self, _schema=JSON_MASTER_SCHEMA,
                 nid="???",
                 language=None,
                 collection=None,
                 entity=None,
                 singlefile=False,
                 version=None,
                 **kwargs) -> list[tuple[str, dict]]:
        """
        returns a list of tupels (filename, struct) for every file  generated.
        in case of singlefile, the list contains one entry only
        entity is not None: entity is top level jsonfile
        collection is not None: collection is top level jsonfile containing all entities of this collection which are referenced by no other
        both None: model is top level jsonfile, containing all entities referenced by no others.
        domains are resolved inline, if they are referenced by only one attribute.
        otherwise they are resolved as sepearte json-schema
         
        :param _schema: json-schema master file, default "https://json-schema.org/draft/2020-12/schema"
        :param nid: prefix for $id
        :param language: iso code of language for texts. default model main language
        :param collection: name of collection where the hierarchiy starts 
        :param entity: name of entity where the  hierarchiy starts
        :param singlefile: True, genrate one single json-schema-file, False create a file for every element
        :param version: version of the schema to be generated. Default taken from modelinfo of jsonstruct
        :param kwargs: 
        :return: 
        """
        # HEADER
        assert not singlefile,f"singlefile not yet handled"
        self.nid = nid
        self._schema = _schema
        modelinfo = self.jsstruct.elements("ModelInfo")

        if modelinfo is None:
            logging.error(f"'ModelInfo' not found in structure")
            modelinfo = dict()

        self.modelname = modelinfo.get("modelName", '???')
        self.modelversion = nvl(version, modelinfo.get("modelVersion", '0.0'))
        sourcelink = self.getadditionalprop(struct=modelinfo,
                                            propname="SOURCE-HREF")
        self.language = language if (language is not None and language in modelinfo.get("languages")) \
                            else modelinfo.get("mainLanguage")

        self.multiuseddomains = self._getownobjectdomains()
        genschemata = []  # schemata (filename, struct tuples) generated so far
        self.usedentities = set()  # entities referenced so far, to be added
        self.useddomains = set()  # domains referenced so far, to be added
        self.doneentities = set()  # entities generated so far
        self.donedomains = set()  # domains generated so far
        self.toplevelname=""
        schemastruct={}

        # if domain is not None:
        #    assert False, "domains export not yet implemented"
        #    for doma in [c for c in self.jsstruct.get("Domains", list()) \
        #                 if self.getmlvalue(c.get("name")) == domain]:
        #        self.adddomain(dest=self.jsschemastruct, enti=enti)
        # elif
        if entity is not None:
            for enti in [c for c in self.jsstruct.elements("Entities") \
                         if self.getmlvalue(c.get("name")) == entity]:
                self.toplevelname = self.getmlvalue(enti.get("name"))
                schemastruct |= self._genschemafiletemplate(descr=self.getmlvalue(enti.get("description")),
                                                           title=self.getmlvalue(enti.get("shortDescr")),
                                                           urn=kwargs.get("urn"),
                                                           _type="object",
                                                           sourcelink=sourcelink
                                                           )
                schemastruct |= self.buildentity(enti=enti)
                self.usedentities.add(enti.get("elementId"))
                self.doneentities.add(enti.get("elementId")) ## added to genschemata at end of if
        elif collection is not None:
            assert False, f"collection no yet implemented"
            for catg in [catg for catg in self.jsstruct.elements("Categories") \
                         if catg.get("categoryType") == "ENTITY" and
                            collection == self.getname(catg)
                         ]:
                self.usedentities = set(self._unrefentis(catgid=catg.get("elementId")))
                self.toplevelname=self.getname(catg)
                schemastruct|=self._genschemafiletemplate(descr=self.getmlvalue(catg.get("description")),
                                            urn=kwargs.get("urn",
                                                           self.urn(nid=self.nid,
                                                                    localid=self.urnid(
                                                                        model=self.toplevelname,
                                                                        name=self.toplevelname,
                                                                        version=self.modelversion
                                                                    )
                                                                    )
                                                           ),
                                            _type="object",
                                            sourcelink=self.getadditionalprop(struct=catg,
                                                                              propname="SOURCE-HREF")
                                            )
                children = self.categorychildren(catg)
                schemastruct |= self._notnulldict(description=self.getmlvalue(catg.get("description")),
                        type = "object",
                        properties = children,
                        required = list(children.keys())
                )
        else:
            assert False,f"full model not yet implemented"
            # no restriction, fill all entities from model
            # start with a model schema-file
            self.toplevelname = self.modelname
            #components = {"schemas": {},
            #              "$defs": {}} if singlefile \
            #                else {}
            schemastruct |= self._genschemafiletemplate(descr=self.getmlvalue(modelinfo.get("description")),
                                                       urn=kwargs.get("urn",
                                                                      self.urn(nid=self.nid,
                                                                               localid=self.urnid(
                                                                                   model=self.toplevelname,
                                                                                   name=self.toplevelname,
                                                                                   version=self.modelversion
                                                                               )
                                                                               )
                                                                      ),
                                                       _type="object",
                                                       sourcelink=self.getadditionalprop(struct=modelinfo,
                                                                                         propname="SOURCE-HREF"),
                                                       components=components,
                                                       )
            self.usedentities = set(self._unrefentis(catgid=None))
            self.fillmodel(catgs=[catg for catg in self.jsstruct.elements("Categories") \
                                  if catg.get("categoryType") == "ENTITY" and
                                  catg.get("categoryId") is None
                                  ])

        filename = SCHEMA_FILENAME_END.format(name=self.toplevelname)
        genschemata.append((filename, schemastruct))

        while len(self.doneentities) < len(self.usedentities):
            # create more entries for entities used so far
            entiid = (self.usedentities - self.doneentities).pop()
            enti = self.jsstruct.getbyid(entiid)
            genschemata.append((SCHEMA_FILENAME_END.format(name=self.getname(enti)),
                                self.addentity(enti)
                                )
                               )
            self.doneentities.add(entiid)

        while len(self.donedomains) < len(self.useddomains):
            # create all domains used so far
            domaid = (self.useddomains - self.donedomains).pop()
            doma = self.jsstruct.getbyid(domaid)
            genschemata.append((SCHEMA_FILENAME_END.format(name=self.getname(doma)),
                                self.adddomain(doma)
                                )
                               )
            self.donedomains.add(domaid)

        return genschemata


class JsonExample:
    def __init__(self, jsschema):
        self.jsschema = jsschema
        return

    def generateexamples(self) -> dict:
        jsexample = dict()

        def doallprops(deststruct, lobject):
            doprops(deststruct, lobject.get("properties", dict()))
            for allprops in lobject.get("allOf", []):
                doprops(deststruct, allprops.get("properties", dict()))

        def doprops(deststruct, props: dict):
            for propname, propdef in props.items():
                proptype = propdef.get("type")
                if proptype == "array":
                    refobjname = propdef.get("items").get("$ref", ['/???']).split("/")[-1]
                    refobj = self.jsschema.get("components", dict()).get("schemas", dict()).get(refobjname, dict())
                    if refobj.get("type") == "object":
                        res = dict()
                        doallprops(res, refobj)
                        deststruct[propname] = [res]
                elif proptype is not None and "$ref" in proptype and \
                        proptype.get("$ref") is not None and \
                        proptype.get("$ref", "").startswith("#/components/schemas"):
                    refobjname = proptype.get("$ref", ['/???']).split("/")[-1]
                    refobj = self.jsschema.get("components", dict()).get("schemas", dict()).get(refobjname, dict())
                    if refobj.get("type") == "object":
                        deststruct[refobjname] = dict()
                        doallprops(deststruct[refobjname], refobj)
                elif "examples" in propdef and len(propdef.get("examples")) > 0:
                    deststruct[propname] = propdef.get("examples")[0]
                elif proptype is not None and "$ref" in proptype and \
                        proptype.get("$ref") is not None and \
                        proptype.get("$ref", "").startswith("#/components/$defs"):
                    refdomaname = proptype.get("$ref", ['/???']).split("/")[-1]
                    refdoma = self.jsschema.get("components", dict()).get("$defs", dict()).get(refdomaname, dict())
                    if "examples" in refdoma and len(refdoma.get("examples")) > 0:
                        deststruct[propname] = refdoma.get("examples")[0]
                    elif refdoma.get("type") == "object":
                        groupname = proptype.get("$ref", ['/???']).split("/")[-1]
                        attrgrp = dict()
                        doallprops(attrgrp, refdoma)
                        deststruct[propname] = attrgrp
                    else:
                        deststruct[propname] = "???"
                else:
                    deststruct[propname] = "???"
            return

        doallprops(jsexample, self.jsschema)

        return jsexample


def generatejsonschema(jsonfilepath=None,
                       jsonstruct=None,
                       _schema=None,
                       nid="???",
                       collection=None,
                       entity=None,
                       outfilepath=None,
                       singlefile=False,
                       samplespath=None,
                       **kwargs) -> (dict, dict):
    if jsonstruct is not None:
        jsstruct = jsonstruct
    elif jsonfilepath is not None:
        with open(jsonfilepath) as infile:
            jsstruct = json.load(infile)
    else:
        logging.error("No input given")
        return None
    # returns list of tupels (filename,schema)
    jsschemas = Json2JsonSchema(jsonstruct=jsstruct).generate(nid=nid,
                                                              _schema=_schema,
                                                              collection=collection,
                                                              entity=entity,
                                                              singlefile=singlefile,
                                                              **kwargs)
    if outfilepath is not None:
        for jsschema in jsschemas:
            StandardJsonModel.dumpjsonfile(struct=jsschema[1],
                                           outpath=outfilepath / jsschema[0],
                                           verbose=True,
                                           ensure_ascii=True)
    jsexamples = []
    if samplespath is not None:
        for jsschema in jsschemas:
            jsexample = JsonExample(jsschema[1]).generateexamples()
            explfilename = jsschema[0].replace("schema", "example")
            jsexamples.append((explfilename, jsexample))
            StandardJsonModel.dumpjsonfile(struct=jsexample,
                                           outpath=samplespath / explfilename,
                                           verbose=True,
                                           ensure_ascii=True)

    return jsschemas, jsexamples
