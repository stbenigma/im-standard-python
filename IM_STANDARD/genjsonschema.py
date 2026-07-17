import json
import logging
import re
import unicodedata

from IM_STANDARD import nvl,StandardJsonModel

"""
    generate a json-schema and a json-sample file out of a standard model json file
    assume jsonstruct is validated against the standard IM schema
"""


def initLower(text):
    return text[:1].lower() + text[1:]


def normalizestring(text):
    normalized = unicodedata.normalize('NFKD', text)
    # Filtert alle Zeichen heraus, die keine reinen Buchstaben sind (die "Pünktchen")
    return "".join([c for c in normalized if not unicodedata.combining(c)])


class Json2JsonSchema:
    # TODO für alle "x-samm-aspect-model-urn": "urn:samm:BatteryPass:1.0.0#Circularity",

    def __init__(self, jsonstruct):
        self.jsstruct = jsonstruct
        return

    def getadditionalprop(self, struct, propname, defval=None):
        return struct.get("additionalProps", dict()).get(propname, defval)

    def getid(self, struct):
        """ construct an ID for the element"""
        return self.nid + ":" + nvl(self.getadditionalprop(struct=struct, propname="SOURCE-ID"))

    def urn(self, nid, localid):
        return f"urn:{nid}:{localid}"

    def urnid(self, model, name, version=None):
        lversion = f":{version}" if version is not None else ""
        return f"{model}{lversion}#{name}"

    def startdash(self, value: str):
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

    def notnulldict(self, **kwargs):
        return {self.startdash(key): val for key, val in kwargs.items()
                if not (val is None or
                        val == "" or
                        val == list() or
                        val == dict())}

    def addobject(self, entry, subcat, **kwargs):
        defs = self.jsschemastruct["components"][subcat]
        if entry in defs: return
        defs[entry] = self.notnulldict(**kwargs)
        return f"#/components/{subcat}/{entry}"

    def setdefsobject(self, entry, **kwargs):
        return self.addobject(entry=entry, subcat="$defs", **kwargs)

    def addproperty(self, entry, subcat, **kwargs):
        defs = self.jsschemastruct["components"][subcat]
        assert entry in defs, f"object {entry} does not exist"
        defs[entry].update(self.notnulldict(**kwargs))
        return

    def addschemaproperty(self, entry, **kwargs):
        self.addproperty(entry=entry, subcat="schemas", **kwargs)

    def adddefsproperty(self, entry, **kwargs):
        self.addproperty(entry=entry, subcat="$defs", **kwargs)

    def setschemaobject(self, entry, **kwargs):
        return self.addobject(entry=entry, subcat="schemas", **kwargs)

    def getobject(self, objtype, objid):
        objs = [o for o in self.jsstruct.get(objtype) if o.get("elementId") == objid]
        if len(objs) == 1:
            return objs[0]
        else:
            # logging.error(f"Object (id={objid}) not found in {objtype}")
            return None

    def getmainlang(self):
        return self.jsstruct.get("ModelInfo").get("mainLanguage", "en")

    @property
    def isassetmodel(self):
        return self.jsstruct.get("ModelInfo").get("modelType")=="Asset model"

    def getmlvalue(self, struct):
        if type(struct) == str:
            return struct
        elif type(struct) == dict:
            return struct.get(self.getmainlang())
        else:
            return f"??{type(struct)}??"

    def fillmodel(self, catgs):
        self.toplevelobject = self.modelname
        children = dict()
        for catg in catgs:
            self.addcategory(dest=children, catg=catg)

        self.jsschemastruct.update(
            self.notnulldict(
                description=self.jsstruct.get("ModelInfo", dict()).get("description",
                                                                       "Group of elements")),
            type="object",
            properties=children,
            required=list(children.keys())
        )
        self.jsschemastruct["urn"] = self.urn(nid=self.nid,
                                              localid=self.urnid(
                                                  model=self.toplevelobject,
                                                  name=self.toplevelobject,
                                                  version=self.modelversion)
                                              )
        return

    def fillcategory(self, catg):
        objname = self.getname(catg)
        self.toplevelobject = objname
        children = self.categorychildren(catg)
        self.jsschemastruct.update(self.notnulldict(description=catg.get("description",
                                                                         "Group of elements")),
                                   type="object",
                                   properties=children,
                                   required=list(children.keys())
                                   )
        self.jsschemastruct["urn"] = self.urn(nid=self.nid,
                                              localid=self.urnid(
                                                  model=self.toplevelobject,
                                                  name=objname,
                                                  version=self.modelversion)
                                              )

        return objname

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

        dest[objname] = self.notnulldict(description=catg.get("description", "Group of elements"),
                                         _ref=refobj)
        return refobj

    def adddomain(self, doma):
        domaname = self.getname(doma)
        pattern = doma.get("pattern")
        minLength = doma.get("minLength")
        maxLength = doma.get("maxLength")
        unit = doma.get("unit")
        minimum = doma.get("minimum")
        maximum = doma.get("maximum")
        lformat = None
        enum = None
        properties = None
        required = None
        if doma.get("domainType") == "TextDomain":
            objtype = "string"
        elif doma.get("domainType") == "GroupDomain":
            objtype = "object"
            properties, mandatory = self.getattributes(doma)
            required = []
        elif doma.get("domainType") == "BooleanDomain":
            objtype = "boolean"
        elif doma.get("domainType") == "LOVDomain":
            objtype = "string"
            enum = [v.get("value") for v in doma.get("values", list())]
        elif doma.get("domainType") == "NumericDomain":
            if doma.get("fractDigits", 0) == 0:
                objtype = "integer"
            else:
                objtype = "decimal"
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
        domaref = self.setdefsobject(entry=domaname,
                                     description=doma.get("description"),
                                     _id=self.getid(doma),
                                     urn=self.urn(nid=self.nid,
                                                  localid=self.urnid(
                                                      model=self.toplevelobject,
                                                      name=domaname,
                                                      version=self.modelversion)
                                                  ),
                                     _type=objtype,
                                     pattern=pattern,
                                     minLength=minLength,
                                     maxLength=maxLength,
                                     format=lformat,
                                     minimum=minimum,
                                     maximum=maximum,
                                     unit=unit,
                                     enum=enum,
                                     properties=properties,
                                     required=required,
                                     examples=doma.get("examples"),
                                     references=self.getderivations(doma)
                                     )
        return domaref

    def getattributes(self, enti):
        attributes = dict()
        mandatory = []
        attrs=[c for c in self.jsstruct.get("Attributes", list()) \
                     if c.get("parentId") == enti.get("elementId")]
        attrs.sort(key=lambda x:x.get("displaySeq",9999))
        for attr in attrs:
            objname = initLower(self.getname(attr))

            doma = self.getobject(objtype="Domains", objid=attr.get("domainid"))
            if doma is None:
                typeref = None
            else:
                typeref = self.getname(doma).lower()
                typemap={"integer": "integer",
                 "decimal": "number",
                 "number": "number",
                 "text": "string",
                 "string": "string",
                 "boolean": "boolean"}
                if typeref in typemap:
                    typeref = typemap[typeref]
                else:
                    domaref = self.adddomain(doma=doma)
                    typeref = {"$ref": domaref}
            example=attr.get("examples")
            attrstruct = self.notnulldict(description=attr.get("description"),
                                          _id=self.getid(attr),
                                          examples=example,
                                          references=self.getderivations(attr)
                                          )
            if attr.get("cardinality") in (None, "1", "one"):
                if typeref is not None:
                    attrstruct["type"] = typeref
            else:
                attrstruct["type"] = "array"
                if typeref is not None:
                    attrstruct["items"] = [{"type": typeref}]
            if attr.get("mandatory"):
                mandatory.append(objname)
            attributes[objname] = attrstruct
        return attributes, mandatory

    def getrelaname(self, assoc, entiname, ):
        return re.sub(r'[^a-zA-Z0-9$_]', '', assoc) + \
               re.sub(r'[^a-zA-Z0-9$_]', '', entiname)

    def getderivations(self, enti):
        refs = []
        for ref in [c for c in self.jsstruct.get("Derivations", list())
                    if c.get("targetElement") == enti.get("elementId")]:
            refs.append(ref.get("sourceElement"))
        return list(set(refs))

    def getroles(self, enti):
        roles = list()
        # TODO return mandatory as well (similar in getattributes)
        # TODO protect arc with oneOf
        for rela in [c for c in self.jsstruct.get("Relations", list())
                     if c.get("relationType") == "ROLE"]:
            fwd, bwd = rela.get("fwd"), rela.get("bwd")
            if fwd.get("entityId") == enti.get("elementId") and \
                    fwd.get("mandatory"):
                otherenti = self.getobject(objtype="Entities", objid=bwd.get("entityId"))
                roles.append(self.notnulldict(description=f"{self.getmlvalue(fwd.get('assocText'))} " + \
                                                          f"{self.getmlvalue(otherenti.get('name'))} ",
                                              _id=self.getid(rela),
                                              type={"$ref": self.entiref(enti=otherenti)}
                                              )
                             )
            elif bwd.get("entityId") == enti.get("elementId") and \
                    bwd.get("mandatory"):
                otherenti = self.getobject(objtype="Entities", objid=fwd.get("entityId"))
                roles.append(self.notnulldict(description=f"{self.getmlvalue(bwd.get('assocText'))} " + \
                                                          f"{self.getmlvalue(otherenti.get('name'))} ",
                                              _id=self.getid(rela),
                                              type={"$ref": self.entiref(enti=otherenti)}
                                              )
                             )

        return roles

    def getsubtypes(self, enti) -> list:
        subtypes = list()
        # TODO return mandatory as well (similar in getattributes)
        # TODO protect arc with oneOf
        for rela in [c for c in self.jsstruct.get("Relations", list())
                     if c.get("relationType") == "SUBTYPE"]:
            fwd, bwd = rela.get("fwd"), rela.get("bwd")
            if fwd.get("entityId") == enti.get("elementId") and \
                    bwd.get("arcNumber") is not None:
                otherenti = self.getobject(objtype="Entities", objid=bwd.get("entityId"))
                subtypes.append(self.notnulldict(description=f"{self.getmlvalue(fwd.get('assocText'))} " + \
                                                             f"{self.getmlvalue(otherenti.get('name'))} ",
                                                 _id=self.getid(rela),
                                                 type={"$ref": self.entiref(enti=otherenti)}
                                                 )
                                )
            elif bwd.get("entityId") == enti.get("elementId") and \
                    fwd.get("arcNumber") is not None:
                otherenti = self.getobject(objtype="Entities", objid=fwd.get("entityId"))
                subtypes.append(self.notnulldict(description=f"{self.getmlvalue(bwd.get('assocText'))} " + \
                                                             f"{self.getmlvalue(otherenti.get('name'))} ",
                                                 _id=self.getid(rela),
                                                 type={"$ref": self.entiref(enti=otherenti)}
                                                 )
                                )
        return subtypes

    def getM2Nrelations(self,enti):
        for rela in [c for c in self.jsstruct.get("Relations", list()) if c.get("relationType") in ("M:N")]:

            logging.warning(f"Relations of type {rela.get('relationType')} not yet implemented")
        return None,None

    def getfunctionalrelations(self, enti):
        """ get all relations
            where this entity is a many-side of a M:1 relationship
            add an fk-attribute
            """
        fkattrs = dict()
        mandatory = []
        # TODO return mandatory as well (similar in getattributes)
        # TODO protect arc with oneOf
        for rela in [c for c in self.jsstruct.get("Relations", list()) if c.get("relationType") in ("M:1","1:1")]:
            fwd, bwd = rela.get("fwd"), rela.get("bwd")
            if fwd.get("entityId") == enti.get("elementId") and \
                    fwd.get("cardinality") == '1' and \
                    bwd.get("cardinality") in ('M','1'):
                otherenti = self.getobject(objtype="Entities", objid=bwd.get("entityId"))
                relaname=self.getrelaname(assoc=self.getmlvalue(fwd.get('assocText')),
                                         entiname=self.getmlvalue(otherenti.get('name')))
                fkattrs[relaname] = self.notnulldict(description=f"{self.getmlvalue(fwd.get('assocText'))} " + \
                                                 f"{self.getmlvalue(otherenti.get('name'))} ",
                                     _id=self.getid(rela),
                                     type={"$ref": self.entiref(enti=otherenti)}
                                     )
                if fwd.get("mandatory") : mandatory.append(relaname)
            elif bwd.get("entityId") == enti.get("elementId") and \
                    bwd.get("cardinality") == '1' and \
                    fwd.get("cardinality") == 'M':
                otherenti = self.getobject(objtype="Entities", objid=fwd.get("entityId"))
                relaname=self.getrelaname(assoc=self.getmlvalue(bwd.get('assocText')),
                                         entiname=self.getmlvalue(otherenti.get('name')))
                fkattrs[relaname] = self.notnulldict(description=f"{self.getmlvalue(bwd.get('assocText'))} " + \
                                                 f"{self.getmlvalue(otherenti.get('name'))} ",
                                     _id=self.getid(rela),
                                     type={"$ref": self.entiref(enti=otherenti)}
                                     )
                if bwd.get("mandatory") : mandatory.append(relaname)

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
        for rela in [c for c in self.jsstruct.get("Relations", list()) if c.get("relationType") in ("M:1","1:1")]:
            fwd, bwd = rela.get("fwd"), rela.get("bwd")
            if fwd.get("entityId") == enti.get("elementId") and \
                    fwd.get("cardinality") in ('M','1') and \
                    bwd.get("cardinality") in ('1'):
                otherenti = self.getobject(objtype="Entities", objid=bwd.get("entityId"))
                relaname=self.getrelaname(assoc=self.getmlvalue(fwd.get('assocText')),
                                         entiname=self.getmlvalue(otherenti.get('name')))
                fkattrs[relaname] = self.notnulldict(description=f"{self.getmlvalue(fwd.get('assocText'))} " + \
                                                 f"{self.getmlvalue(otherenti.get('name'))} ",
                                     _id=self.getid(rela),
                                     **self.refobject(objref=self.entiref(enti=otherenti),
                                                          singleobj=fwd.get("cardinality") =='1',
                                                          minitems=1 if fwd.get("mandatory") else None)
                                     )
                if fwd.get("mandatory") : mandatory.append(relaname)
            elif bwd.get("entityId") == enti.get("elementId") and \
                    bwd.get("cardinality") == ('M','1') and \
                    fwd.get("cardinality") == '1':
                otherenti = self.getobject(objtype="Entities", objid=fwd.get("entityId"))
                relaname=self.getrelaname(assoc=self.getmlvalue(bwd.get('assocText')),
                                         entiname=self.getmlvalue(otherenti.get('name')))
                fkattrs[relaname] = self.notnulldict(description=f"{self.getmlvalue(bwd.get('assocText'))} " + \
                                                 f"{self.getmlvalue(otherenti.get('name'))} ",
                                     _id=self.getid(rela),
                                     **self.refobject(objref=self.entiref(enti=otherenti),
                                                          singleobj=bwd.get("cardinality") =='1',
                                                          minitems=1 if bwd.get("mandatory") else None)

                                     )
                if bwd.get("mandatory") : mandatory.append(relaname)
        return fkattrs, mandatory

    def getname(self, struct):
        return normalizestring(self.getadditionalprop(struct=struct,
                                                      propname="TechnicalName",
                                                      defval=self.getmlvalue(struct.get("name", "???"))
                                                      )).replace(" ", "")

    def entiref(self, enti):
        self.usedentities.append(self.getmlvalue(enti.get("name")))
        return f"#/components/schemas/{self.getname(enti)}"

    def buildentity(self, entiname, enti):
        children, mandatory = self.getattributes(enti)
        if self.isassetmodel:
            fkchildren, fkrelamandatory = self.getallrelations(enti)
        else:
            fkchildren, fkrelamandatory = self.getfunctionalrelations(enti)
            mnchildren,mnrelamandatory=self.getM2Nrelations(enti)

        children.update(fkchildren)
        mandatory.extend(fkrelamandatory)

        subtypes = self.getsubtypes(enti)
        rolesof = self.getroles(enti)
        # TODO required abhängig vom mandatory
        entistruct = self.notnulldict(
            description=enti.get("description"),
            _id=self.getid(enti),
            urn=self.urn(nid=self.nid,
                         localid=self.urnid(
                             model=self.toplevelobject,
                             name=entiname,
                             version=self.modelversion)
                         ),
            sourcelink=enti.get("additionalProps",{}).get("SOURCE-HREF"),
            _type="object",
            examples=enti.get("examples"),
            references=self.getderivations(enti))

        allelements = []
        if len(rolesof) > 0:
            allelements.append({"allOf": rolesof})

        if len(children) > 0:
            allelements.append(self.notnulldict(properties=children,
                                                required=mandatory
                                                ))
        if len(subtypes) > 0:
            allelements.append({"oneOf": subtypes})

        entistruct["allOf"] = allelements
        return entistruct

    def addentity(self, enti):
        objname = self.getname(enti)
        entistruct = self.buildentity(entiname=objname, enti=enti)
        refobjname = self.setschemaobject(entry=objname,
                                          **entistruct)
        # TODO required abhängig vom mandatory
        return refobjname

    def fillentity(self, enti):
        objname = self.getname(enti)
        entistruct = self.buildentity(entiname=objname, enti=enti)
        self.jsschemastruct.update(entistruct)

        return objname

    def refobject(self,objref,singleobj:bool=False,
                      unique:bool=None,
                      minitems:int= None,
                      maxitems:int=None):
        if singleobj:
            retval= {"_type":{"$ref": objref}}
        else:
            retval= self.notnulldict(_type= "array",
                                    items= {"$ref": objref},
                                     minItems=None if minitems is None else int(minitems),
                                    maxItems=None if maxitems is None else int(maxitems),
                                    uniqueItems=None if unique is None else unique
                                     )
        return retval

    def categorychildren(self, catg):
        children = dict()
        # catgchildren
        for catgchild in [c for c in self.jsstruct.get("Categories", list()) \
                          if c.get("categoryType") == "ENTITY" and \
                             c.get("categoryId") == catg.get("elementId")]:
            self.addcategory(dest=children, catg=catgchild)
        # entichildren
        for entichild in [c for c in self.jsstruct.get("Entities", list()) \
                          if c.get("categoryId") == catg.get("elementId")]:
            refenti = self.addentity(enti=entichild)
            refobject= self.refobject(refenti,
                                      singleobj=False,
                                      unique=True)
            assert "type" in refobject,"refobject enthält immer _type"
            children[self.getname(entichild)] = \
                self.notnulldict(description=entichild.get("description"),
                                    **refobject)

        return children

    def generate(self, _schema=None,
                 nid="???",
                 collection=None,
                 entity=None,
                 domain=None,
                 **kwargs):
        # HEADER
        self.nid = nid
        self._schema = _schema
        modelinfo = self.jsstruct.get("ModelInfo")

        if modelinfo is None:
            logging.error(f"'ModelInfo' not found in structure")
            modelinfo = dict()

        self.modelname = modelinfo.get("modelName", '???')
        self.modelversion = modelinfo.get("modelVersion", '0.0')

        self.explstruct=dict()
        self.jsschemastruct = self.notnulldict(
            _schema=_schema,
            urn=kwargs.get("urn",
                           self.urn(nid=self.nid,
                                    localid=self.urnid(
                                        model=self.modelname,
                                        name=self.modelname,
                                        version=self.modelversion
                                    )
                                    )
                           ),
            sourcelink=modelinfo.get("additionalProps",{}).get("SOURCE-HREF"),
            description=modelinfo.get("description"),
            _type="object",
            components={
                "schemas": {},
                "$defs": {}
            },
        )
        self.usedentities = []
        # properties, start with categories
        if domain is not None:
            assert False, "domains export not yet implemented"
            for doma in [c for c in self.jsstruct.get("Domains", list()) \
                         if self.getmlvalue(c.get("name")) == domain]:
                self.adddomain(dest=self.jsschemastruct, enti=enti)
        elif entity is not None:
            for enti in [c for c in self.jsstruct.get("Entities", list()) \
                         if self.getmlvalue(c.get("name")) == entity]:
                self.toplevelobject = self.getname(enti)
                self.fillentity(enti=enti)
        elif collection is not None:
            for catg in [catg for catg in self.jsstruct.get("Categories", list()) \
                         if catg.get("categoryType") == "ENTITY" and
                            collection in (self.getname(catg),
                                           self.getmlvalue(catg.get("name")
                                                           )
                                           )
                         ]:
                self.fillcategory(catg=catg)
        else:
            # no restriction, fill all elements from model
            # they start with collections
            self.fillmodel(catgs=[catg for catg in self.jsstruct.get("Categories", list()) \
                                  if catg.get("categoryType") == "ENTITY" and
                                  catg.get("categoryId") is None
                                  ])

        for enti in [c for c in self.jsstruct.get("Entities", list()) \
                     if self.getmlvalue(c.get("name")) in self.usedentities]:
            self.addentity(enti=enti)

        return self.jsschemastruct

class JsonExample:
    def __init__(self,jsschema):
        self.jsschema=jsschema
        return

    def generateexamples(self)->dict:
        jsexample=dict()

        def doallprops(deststruct, lobject):
            doprops(deststruct, lobject.get("properties", dict()))
            for allprops in lobject.get("allOf", []):
                doprops(deststruct,allprops.get("properties",dict()))

        def doprops(deststruct,props:dict):
            for propname,propdef in props.items():
                proptype=propdef.get("type")
                if proptype == "array":
                    refobjname=propdef.get("items").get("$ref",['/???']).split("/")[-1]
                    refobj=self.jsschema.get("components",dict()).get("schemas",dict()).get(refobjname,dict())
                    if refobj.get("type")=="object":
                        res=dict()
                        doallprops(res,refobj)
                        deststruct[propname] = [res]
                elif proptype is not None and "$ref" in proptype and \
                        proptype.get("$ref") is not None and \
                        proptype.get("$ref","").startswith("#/components/schemas"):
                    refobjname = proptype.get("$ref", ['/???']).split("/")[-1]
                    refobj=self.jsschema.get("components",dict()).get("schemas",dict()).get(refobjname,dict())
                    if refobj.get("type")=="object":
                        deststruct[refobjname] = dict()
                        doallprops(deststruct[refobjname],refobj)
                elif "examples" in propdef and len(propdef.get("examples")) > 0:
                    deststruct[propname] = propdef.get("examples")[0]
                elif proptype is not None and "$ref" in proptype and \
                        proptype.get("$ref") is not None and \
                        proptype.get("$ref", "").startswith("#/components/$defs"):
                    refdomaname = proptype.get("$ref", ['/???']).split("/")[-1]
                    refdoma=self.jsschema.get("components",dict()).get("$defs",dict()).get(refdomaname,dict())
                    if "examples" in refdoma and len(refdoma.get("examples")) > 0:
                        deststruct[propname] = refdoma.get("examples")[0]
                    elif refdoma.get("type")=="object":
                        groupname = proptype.get("$ref", ['/???']).split("/")[-1]
                        attrgrp=dict()
                        doallprops(attrgrp,refdoma)
                        deststruct[propname] = attrgrp
                    else:
                        deststruct[propname] = "???"
                else:
                    deststruct[propname]="???"
            return

        doallprops(jsexample,self.jsschema)

        return jsexample


def generatejsonschema(jsonfilepath=None,
                       jsonstruct=None,
                       _schema=None,
                       nid="???",
                       collection=None,
                       entity=None,
                       domain=None,
                       outfilepath=None,
                       examplepath=None,
                       **kwargs) -> (dict,dict):
    if jsonstruct is not None:
        jsstruct = jsonstruct
    elif jsonfilepath is not None:
        with open(jsonfilepath) as infile:
            jsstruct = json.load(infile)
    else:
        logging.error("No input given")
        return None
    jsschema = Json2JsonSchema(jsonstruct=jsstruct).generate(nid=nid,
                                                             _schema=_schema,
                                                             collection=collection,
                                                             entity=entity,
                                                             domain=domain,
                                                             **kwargs)

    jsexample=JsonExample(jsschema).generateexamples()
    if outfilepath is not None:
        StandardJsonModel.dumpjsonfile(struct=jsschema,
                                       path=outfilepath,
                                       verbose=True)
    if examplepath is not None:
        StandardJsonModel.dumpjsonfile(struct=jsexample,
                                       path=examplepath,
                                       verbose=True)


    return jsschema,jsexample
