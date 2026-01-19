import json
import logging

"""
    generate a json-schema of a standard im json
    assume jsonstruct is validated against the standard IM schema
"""


def initLower(text):
    return text[:1].lower() + text[1:]


class Json2JsonSchema:
    # TODO für alle "x-samm-aspect-model-urn": "urn:samm:BatteryPass:1.0.0#Circularity",

    def __init__(self, jsonstruct):
        self.jsstruct = jsonstruct
        return

    def urn(self, nid, localid):
        return f"urn:{nid}:{localid}"

    def urnid(self, model, name, version=None):
        lversion = f":{version}" if version is not None else ""
        return f"{model}{lversion}#{name}"

    def startdollar(self, value: str):
        """
        replaces a leading _ into a $
        """
        if value.startswith('_'):
            return '$' + value[1:]
        else:
            return value

    def notnulldict(self, **kwargs):
        return {self.startdollar(key): val for key, val in kwargs.items()
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

    def setschemaobject(self, entry, **kwargs):
        return self.addobject(entry=entry, subcat="schemas", **kwargs)

    def getobject(self, objtype, objid):
        objs = [o for o in self.jsstruct.get(objtype) if o.get("elementid") == objid]
        if len(objs) == 1:
            return objs[0]
        else:
            # logging.error(f"Object (id={objid}) not found in {objtype}")
            return None

    def getmainlang(self):
        return self.jsstruct.get("ModelInfo").get("mainlanguage", "en")

    def getmlvalue(self, struct):
        if type(struct) == str:
            return struct
        elif type(struct) == dict:
            return struct.get(self.getmainlang())
        else:
            return f"??{type(struct)}??"

    def fillcategory(self, catg):
        objname = initLower(self.getname(catg))
        children = self.categorychildren(catg)
        self.jsschemastruct.update(self.notnulldict(description=catg.get("description",
                                                                         "Group of elements")),
                                   type="object",
                                   properties=children,
                                   required=list(children.keys())
                                   )
        self.jsschemastruct["urn"] = self.urn(nid=self.nid,
                                              localid=self.urnid(
                                                  model=objname,
                                                  name=objname,
                                                  version=self.modelversion)
                                              )

        return objname

    def addcategory(self, dest, catg):
        objname = initLower(self.getname(catg))
        refobj = self.setschemaobject(entry=objname,
                                      description=catg.get("description", "Grouping elements"),
                                      type="object",
                                      properties=self.categorychildren(catg),
                                      required=[]
                                      )

        dest[objname] = self.notnulldict(description=catg.get("description", "Group of elements"),
                                         _ref=refobj)
        descr = catg.get("description")
        return refobj

    def adddomain(self, doma):
        domaname = initLower(self.getname(doma))
        pattern = doma.get("pattern")
        minLength = doma.get("minLength")
        maxLength = doma.get("maxLength")
        unit = doma.get("unit")
        minimum = doma.get("minimum")
        maximum = doma.get("maximum")
        format = None
        enum = None
        properties = None
        required = None
        if doma.get("domaintype") == "TextDomain":
            objtype = "string"
        elif doma.get("domaintype") == "GroupDomain":
            objtype = "object"
            properties = self.getattributes(doma)
            required = []
        elif doma.get("domaintype") == "BooleanDomain":
            objtype = "boolean"
        elif doma.get("domaintype") == "LOVDomain":
            objtype = "string"
            enum = [v.get("value") for v in doma.get("values", list())]
        elif doma.get("domaintype") == "NumericDomain":
            if doma.get("fractdigits", 0) == 0:
                objtype = "integer"
            else:
                objtype = "decimal"
        elif doma.get("domaintype") == "DatetimeDomain":
            objtype = "string"
            if doma.get("granularity") in ("DAY"):
                format = "date"
            elif doma.get("granularity") in ("HOUR", "MINUTE",
                                             "SECOND", "MILISECOND"):
                format = "date-time"
        else:
            objtype = "???"
            logging.warning(f"datatype '{doma.get('domaintype')}' not yet handled")
        domaref = self.setdefsobject(entry=domaname,
                                     description=doma.get("description"),
                                     type=objtype,
                                     pattern=pattern,
                                     minLength=minLength,
                                     maxLength=maxLength,
                                     format=format,
                                     minimum=minimum,
                                     maximum=maximum,
                                     unit=unit,
                                     enum=enum,
                                     properties=properties,
                                     required=required,
                                     examples=doma.get("examples")
                                     )
        return domaref

    def getattributes(self, enti):
        attributes = dict()
        for attr in [c for c in self.jsstruct.get("Attributes", list()) \
                     if c.get("parentid") == enti.get("elementid")]:
            objname = initLower(self.getname(attr))

            doma = self.getobject(objtype="Domains", objid=attr.get("domainid"))
            if doma is None:
                typeref = None
            else:
                typeref = self.getname(doma).lower()
                if typeref in ("integer", "decimal", "number","text", "string", "boolean"):
                    typeref = {"integer": "integer",
                               "decimal": "number",
                               "number": "number",
                               "text": "string",
                               "string": "string",
                               "boolean": "boolean"}[typeref]
                else:
                    domaref = self.adddomain(doma=doma)
                    typeref = {"$ref": domaref}
            attrstruct = self.notnulldict(description=attr.get("description"),
                                          examples=attr.get("examples")
                                          )
            if attr.get("cardinality") in (None, "1", "one"):
                if typeref is not None:
                    attrstruct["type"] = typeref
            else:
                attrstruct["type"] = "array"
                if typeref is not None:
                    attrstruct["items"] = [{"type": typeref}]
            attributes[objname] = attrstruct
        return attributes

    def getrelations(self, enti):
        relations = dict()
        return relations

    def getname(self, struct):
        return struct.get("additionalProps",
                          dict()).get("TechnicalName",
                                      self.getmlvalue(struct.get("name", "???"))
                                      )

    def addentity(self, dest, enti):
        objname = initLower(self.getname(enti))
        children = self.getattributes(enti) | self.getrelations(enti)
        refobjname = self.setschemaobject(entry=objname,
                                          description=enti.get("description"),
                                          type="object",
                                          examples=enti.get("examples"),
                                          properties=children,
                                          required=list(children.keys())
                                          )
        dest[objname] = self.notnulldict(description=enti.get("description", None),
                                         _ref=refobjname)
        return

    def fillentity(self, enti):
        objname = initLower(self.getname(enti))
        refobjname = f"{objname}"
        self.jsschemastruct[objname] = self.notnulldict(description=enti.get("description",
                                                                             None),
                                                        _ref=f"#/components/schemas/{refobjname}")
        self.setschemaobject(entry=refobjname,
                             description=enti.get("description"),
                             type="object",
                             examples=enti.get("examples")
                             )
        properties = self.getattributes(enti) | self.getrelations(enti)
        required = []

        return

    def categorychildren(self, catg):
        children = dict()
        # catgchildren
        for catgchild in [c for c in self.jsstruct.get("Categories", list()) \
                          if c.get("categorytype") == "ENTITY" and \
                             c.get("categoryid") == catg.get("elementid")]:
            self.addcategory(dest=children, catg=catgchild)
        # entichildren
        for entichild in [c for c in self.jsstruct.get("Entities", list()) \
                          if c.get("categoryid") == catg.get("elementid")]:
            self.addentity(dest=children, enti=entichild)
        return children

    def generate(self, _schema=None,
                 nid=None,
                 collections=list(),
                 entities=list(),
                 domains=list(),
                 **kwargs):
        # HEADER
        self.nid = nid
        self._schema = _schema
        modelinfo = self.jsstruct.get("ModelInfo")

        if modelinfo is None:
            logging.error(f"'ModelInfo' not found in structure")
            modelinfo = dict()

        self.modelname = modelinfo.get("modelname", '???')
        self.modelversion = modelinfo.get("modelversion", '0.0')

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
            description=modelinfo.get("description"),
            type="object",
            components={
                "schemas": {},
                "$defs": {}
            },
        )
        # add empty elements
        self.jsschemastruct["properties"] = {}
        self.jsschemastruct["required"] = []

        # properties, start with categories
        if len(domains) > 0:
            if len(entities) > 1:
                logging.error(f"restriction: only one domain can be exported: {domains}")
            else:
                for doma in [c for c in self.jsstruct.get("Domains", list()) \
                             if self.getmlvalue(c.get("name")) in entities]:
                    assert False
                    self.adddomain(dest=self.jsschemastruct, enti=enti)
        elif len(entities) > 0:
            if len(entities) > 1:
                logging.error(f"restriction: only one entity can be exported: {entities}")
            else:
                for enti in [c for c in self.jsstruct.get("Entities", list()) \
                             if self.getmlvalue(c.get("name")) in entities]:
                    assert False
                    self.fillentity(enti=enti)
        else:
            for catg in [catg for catg in self.jsstruct.get("Categories", list()) \
                         if catg.get("categorytype") == "ENTITY"
                         ]:
                # either in list or list is empty and I am top collection
                cnt = 0
                catgname = self.getname(catg)
                if (catgname in collections) or (self.getmlvalue(catg.get("name")) in collections) or \
                        (len(collections) == 0 and catg.get("categoryid") is None):
                    if cnt > 0:
                        logging.error(f"restriction: only one collection can be exported.")
                    else:
                        cnt += 1
                        self.fillcategory(catg=catg)

        return self.jsschemastruct


def generatejsonschema(jsonfilepath=None,
                       jsonstruct=None,
                       _schema=None,
                       nid=None,
                       collections=[],
                       entities=[],
                       domains=[],
                       outfilepath=None,
                       **kwargs) -> dict:
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
                                                             collections=collections,
                                                             entities=entities,
                                                             domains=domains,
                                                             **kwargs)

    if outfilepath is not None:
        with open(outfilepath, "w") as outfile:
            json.dump(jsschema, outfile, indent=2)

    return jsschema
