import json
import logging

"""
    generate a json-schema of a standard im json
    assume jsonstruct is validated against the standard IM schema
"""


def initLower(text):
    return text[:1].lower() + text[1:]


class Json2JsonSchema:
    ENUMTEMPLATE = {
        "type": "string",
        "enum": [
            "BillOfMaterial",
            "Model3D",
            "DismantlingManual",
            "RemovalManual",
            "OtherManual",
            "Drawing"
        ]
    }

    DATATYPETEMPLATE = {
        "type": "string",
        "description": None
    }

    ATTRGROUPTEMPLATE = {
        "description": None,
        "type": "object",
        "properties": {}
    }

    LISTTEMPLATE = {
        "description": None,
        "type": "array",
        "items": {
            "$ref": "#/components/schemas/DismantlingandRemovalDocumentation"
        }
    }

    REFTEMPLATE = {
        "description": None,
        "$ref": "#/components/schemas/SetOfDocumentation"
    }
    # "x-samm-aspect-model-urn": "urn:samm:BatteryPass:1.0.0#Circularity",
    JSONSCHEMATEMPLATE = {"$schema": None,
                          "urn": None,
                          "description": None,
                          "type": "object",
                          "components": {
                              "schemas": {}
                          },
                          "properties": {},
                          "required": []
                          }

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

    def setdefsobject(self, entry, **kwargs):
        schemas = self.jsschemastruct["components"]["$defs"]
        if entry in schemas: return
        schemas[entry] = self.notnulldict(**kwargs)
        return

    def setschemaobject(self, entry, **kwargs):
        schemas = self.jsschemastruct["components"]["schemas"]
        if entry in schemas: return
        schemas[entry] = self.notnulldict(**kwargs)
        return

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

    def fillcategory(self, dest, catg):
        objname = initLower(
            catg.get("additionalProps", dict()).get("TechnicalName", self.getmlvalue(catg.get("name", "???"))))
        refobjname = f"{objname}"
        dest[objname] = self.notnulldict(description=catg.get("description", None),
                                         _ref=f"#/components/schemas/{refobjname}")
        descr = catg.get("description")
        self.setschemaobject(entry=refobjname,
                             description=f"{objname} group" if descr is None else descr,
                             type="object",
                             properties=self.categorychildren(catg))
        return

    def adddomain(self, doma):
        domaname = initLower(doma.get("additionalProps",
                                      dict()).get("TechnicalName",
                                                  self.getmlvalue(doma.get("name", "???"))
                                                  ))
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
        self.setdefsobject(entry=domaname,
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
        return domaname

    def getattributes(self, enti):
        attributes = dict()
        for attr in [c for c in self.jsstruct.get("Attributes", list()) \
                     if c.get("parentid") == enti.get("elementid")]:
            objname = initLower(attr.get("additionalProps",
                                         dict()).get("TechnicalName",
                                                     self.getmlvalue(attr.get("name", "???"))
                                                     ))

            doma = self.getobject(objtype="Domains", objid=attr.get("domainid"))
            if doma is None:
                domainref = None
            else:
                domaname = self.adddomain(doma=doma)
                domainref = {"$ref": f"#/components/$defs/{domaname}"}
            attrstruct = self.notnulldict(description=attr.get("description"),
                                          type=domainref,
                                          examples=attr.get("examples")
                                          )
            if attr.get("cardinality") in (None, "1", "one"):
                if domainref is not None:
                    attrstruct["type"] = domainref
            else:
                attrstruct["type"] = "array"
                attrstruct["items"] = [{"type": domainref}]
            attributes[objname] = attrstruct
        return attributes

    def fillentity(self, dest, enti):
        objname = initLower(enti.get("additionalProps",
                                     dict()).get("TechnicalName",
                                                 self.getmlvalue(enti.get("name", "???"))
                                                 ))
        refobjname = f"{objname}"
        dest[objname] = self.notnulldict(description=enti.get("description", None),
                                         _ref=f"#/components/schemas/{refobjname}")
        self.setschemaobject(entry=refobjname,
                             description=enti.get("description"),
                             type="object",
                             examples=enti.get("examples"),
                             properties=self.getattributes(enti),
                             required=[]
                             )
        return

    def categorychildren(self, catg):
        children = dict()
        # catgchildren
        for catgchild in [c for c in self.jsstruct.get("Categories", list()) \
                          if c.get("categorytype") == "ENTITY" and \
                             c.get("categoryid") == catg.get("elementid")]:
            self.fillcategory(dest=children, catg=catgchild)
        # entichildren
        for entichild in [c for c in self.jsstruct.get("Entities", list()) \
                          if c.get("categoryid") == catg.get("elementid")]:
            self.fillentity(dest=children, enti=entichild)
        return children

    def generate(self, collections=list(),
                 entities=list(),
                 domains=list(),
                 **kwargs):
        self.jsschemastruct = self.JSONSCHEMATEMPLATE
        # HEADER
        modelinfo = self.jsstruct.get("ModelInfo")
        if modelinfo is None:
            logging.error(f"'ModelInfo' not found in structure")
            modelinfo = dict()
        self.jsschemastruct = self.notnulldict(
            _schema=kwargs.get("_schema",
                               "http://json-schema.org/draft-04/schema"),
            urn=kwargs.get("urn",
                           self.urn(nid=kwargs.get("nid", "???"),
                                    localid=self.urnid(
                                        model=modelinfo.get("modelname", "????"),
                                        name=modelinfo.get("modelname", "????"),
                                        version=modelinfo.get("modelversion",
                                                              "????"))
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
            for enti in [c for c in self.jsstruct.get("Entities", list()) \
                         if self.getmlvalue(c.get("name")) in entities]:
                assert False
                self.adddomain(dest=self.jsschemastruct, enti=enti)
        elif len(entities) > 0:
            for enti in [c for c in self.jsstruct.get("Entities", list()) \
                         if self.getmlvalue(c.get("name")) in entities]:
                self.fillentity(dest=self.jsschemastruct, enti=enti)
        else:
            for catg in [catg for catg in self.jsstruct.get("Categories", list()) \
                         if catg.get("categorytype") == "ENTITY"
                         ]:
                # either in list or list is empty and I am top collection
                if (self.getmlvalue(catg.get("name")) in collections) or \
                        (len(collections) == 0 and catg.get("categoryid") is None):
                    self.fillcategory(dest=self.jsschemastruct["properties"],
                                      catg=catg)

        return self.jsschemastruct


def generatejsonschema(jsonfilepath=None,
                       jsonstruct=None,
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

    jsschema = Json2JsonSchema(jsonstruct=jsstruct).generate(collections=collections,
                                                             entities=entities,
                                                             domains=domains,
                                                             **kwargs)

    if outfilepath is not None:
        with open(outfilepath, "w") as outfile:
            json.dump(jsschema, outfile, indent=2)

    return jsschema
