import copy
import logging
from datetime import datetime

from IM_STANDARD import ElementId, alwayslist, nvl, JsonSchema, JsonElement
from INTERFACES.DATASPOT.imstandard_dataspot.dselements import DataspotElements
from .dslib import fullescapestr, custom_split


def mseconds2date(seconds):
    return datetime.utcfromtimestamp(seconds / 1000)


def date2mseconds(date):
    # todo timezone
    return int(date.timestamp() * 1000)


class Dataspot2Jsonbase:
    ORIGINTOOL = "dataspot"

    def __init__(self, standardjson: JsonSchema, dsmodels=None, indirec=None, **kwargs):
        # super().__init__(indirec=indirec, **kwargs)
        self.dsmodels = dsmodels if dsmodels is not None else DataspotElements(indirec=indirec, **kwargs)
        self.standardjson: JsonSchema = standardjson
        return

    @staticmethod
    def _multilangvalue(value,
                        mainlang: str,
                        langs: list,
                        fieldname: str,
                        addprops: dict):
        retval = {} if value is None else {mainlang: value}
        for otherlang in langs:
            if otherlang == mainlang: continue
            translkey = f"{fieldname}:{otherlang}"
            othervalue = addprops.get(translkey)
            if othervalue is not None:
                retval[otherlang] = othervalue
                # remove this property from this additionalproperties
                del addprops[translkey]
            else:
                capitalize = lambda s: s[0].upper() + s[1:]
                translkey = f"{capitalize(fieldname)}:{otherlang}"
                othervalue = addprops.get(translkey)
                if othervalue is not None:
                    retval[otherlang] = othervalue
                    # remove this property from this additionalproperties
                    del addprops[translkey]
        # if allvalues in all languages are none, return None
        if len([val for val in retval.values() if val not in (None, "")]) == 0:
            retval = None
        return retval

    def mutlilangvalue(self, fieldname, value, addprops):
        """
        get the value in otherlanguages  (fieldname with ":xx" at end)
        build a dictionary with all existing languages
        If the value is already a dictionary, assume, it is already translated
        and return it as is
        @param fieldname: name of the field in dataspotstructure
        @param value: value for this field
        @param :*addprops: list of additional properties of field
        @return:
            value if value is dict
            else
            {"<mainlang>": "value",
              <otherlang>: "<value of addprop, starting with fieldname, ending in ':<otherlang>'"
               .... }
        """
        if type(value) is dict:
            return value
        elif not self.standardjson.modelismultilingual():
            return value
        else:
            return self._multilangvalue(value=value,
                                        mainlang=self.standardjson.mainlang,
                                        langs=self.standardjson.languages,
                                        fieldname=fieldname,
                                        addprops=addprops)

    def createmultimodelcategories(self):
        def typemulticatg(models, catgtype):
            if len(models) > 1:
                descr = "Dataspot-Modell in eine oberste Kategorie im Standardmodell übersetzt" \
                    if self.standardjson.mainlang == 'de' \
                    else "dataspot model translated into a top level category in standard model"
                for model in models:
                    replacedkeys = []
                    for key, catg in self.dsmodels.categories.items():
                        if catg.get("TYPE") == catgtype and catg.get("DSMODEL") == model:
                            if catg.get("PARENT") is None:
                                catg["PARENT"] = model
                                catg["inCollection"] = model
                            replacedkeys.append(key)
                    for key in replacedkeys:
                        self.dsmodels.categories[f"{model}/{key}"] = self.dsmodels.categories[key]
                        del self.dsmodels.categories[key]

                    nextid = ElementId.nextid("CATG")

                    self.dsmodels.categories[f"{model}/{model}"] = {'_type': 'Collection',
                                                                    'label': model,
                                                                    'description': descr,
                                                                    'DSMODEL': model,
                                                                    'ID': nextid,
                                                                    'TYPE': catgtype,
                                                                    'PARENT': None}
            return

        """ dataspot allows several models of the same type (Information model, domainid model, referencemodel)
            which are combined in standard model.
            Create top level categories for the models (if  there is more than one) above all top level models
        """
        diffimmodels = set(c.get("DSMODEL") for c in self.dsmodels.categories.values() if c.get("TYPE") == "ENTITY")
        typemulticatg(models=diffimmodels, catgtype='ENTITY')
        diffdomainmodels = set(c.get("DSMODEL") for c in self.dsmodels.categories.values() if c.get("TYPE") == "DOMAIN")
        typemulticatg(models=diffdomainmodels, catgtype='DOMAIN')
        diffsystemmodels = set(c.get("DSMODEL") for c in self.dsmodels.categories.values() if c.get("TYPE") == "SYSTEM")
        typemulticatg(models=diffsystemmodels, catgtype='SYSTEM')
        diffsystemmodels = set(
            c.get("DSMODEL") for c in self.dsmodels.categories.values() if c.get("TYPE") == "DATAMODEL")
        typemulticatg(models=diffsystemmodels, catgtype='DATAMODEL')

        return

    def generatecategories(self, catgtype, status=None):
        categories = {key: val for key, val in self.dsmodels.categories.items()
                      if val.get("TYPE") == catgtype \
                      and DataspotElements.checkstatus(val, status)}
        donecatgs = dict()
        newcategories = []
        cnt = 0
        restcatgs = copy.deepcopy(categories)
        while len(restcatgs) > 0:
            cnt += 1
            assert cnt < 30
            todocatgs = list(restcatgs.keys())
            for key in todocatgs:
                catg = restcatgs[key]
                parentname = catg.get("inCollection")
                if parentname is None:
                    newcategories.append(JsonElement().categoryjson(elementid=catg.get("ID"),
                                                                    name=catg.get("label"),
                                                                    categorytype=catgtype)
                                         )
                    donecatgs[catg.get("label")] = catg.get("ID")
                    del restcatgs[key]
                else:
                    fullname = parentname + "/" + catg.get("label")
                    if parentname not in restcatgs:  # parent was alredy processed
                        newcategories.append(JsonElement().categoryjson(elementid=catg.get("ID"),
                                                                        name=catg.get("label"),
                                                                        categorytype=catgtype))
                        donecatgs[fullname] = catg.get("ID")
                        del restcatgs[key]
                    else:
                        pass
        # self.modelcategories[catgtype] = doxnecatgs
        self.standardjson.addelementinstance(name="Categories", val=newcategories)
        return

    def getelementbyid(self, elements, elemid):
        elem = [e for e in elements.values() if e.get("ID") == elemid]
        if len(elem) == 0:
            return None
        elif len(elem) == 1:
            return elem[0]
        assert False, f"element id {elemid} found more than once"

    def getelementid(self, elementtype, elementname):
        """ beware of translated names with mlvalue() """
        elements = {self.standardjson.mlvalue(elem["name"]): elem.getid()
                    for elem in self.standardjson.jsonschemamodel.get(elementtype, [])}
        return elements.get(self._deref(elementname)) if elements else None

    def getrelationid(self, **kwargs):
        return None

    def getentityid(self, entiname):
        return self.getelementid(elementtype="Entities", elementname=entiname)

    def getdomainid(self, domaname):
        return self.getelementid(elementtype="Domains", elementname=domaname)

    def getdataobjectid(self, datoname):
        return self.getelementid(elementtype="DataObjects", elementname=datoname)

    def getattributeid(self, parentname, attrname, modelname=None):
        entiparent = self.standardjson.getbyid(self.getentityid(parentname))
        domaparent = self.standardjson.getbyid(self.getdomainid(parentname))
        if entiparent is None and domaparent is None:
            return None  # no attribute found
        # check identical attribute in domain and entity with same name, separate by modelname
        entiid = None if entiparent is None else entiparent.getid()
        domaid = None if domaparent is None else domaparent.getid()
        attrs = {self.standardjson.mlvalue(attr["name"]): attr.getid()
                 for attr in self.standardjson.getelementinstances(elementname="Attributes")
                 if attr["parentid"] in (entiid, domaid) and
                 modelname in
                 [val for key, val in attr.getadditionalprops().items() if key == "SOURCE-MODEL"]
                 }
        return attrs.get(self._deref(attrname))

    def getcolumnid(self, datoname, coluname):
        parent = self.standardjson.getbyid(self.getdataobjectid(datoname))
        subelementsname = "columns"
        if parent is None:
            logging.error(f"DataObject '{datoname}' not found")
            return None
        colus = {self.standardjson.mlvalue(colu["name"]): colu.getid()
                 for colu in parent[subelementsname]}
        return colus.get(self._deref(coluname))

    @staticmethod
    def namedreference2struct(namedref: str):
        """ separates a refrence to an object into its components
            [/<modelname>]:[<elementpath>/]*<elementname>
            alle Namen die ein "/" oder ein Spezialzeichen enthalten sind in ""
            return
            modelname: None or firstname after /
            elementpath : list of names between

        """
        if namedref is None: return (None, None, None)
        if ":" in namedref:
            parts = custom_split(input_string=namedref, delimiter=":")
            modelname = parts[0]
            restpath = parts[1]
        else:
            modelname = None
            restpath = namedref

        parts = custom_split(input_string=restpath, delimiter="/")
        if restpath.startswith("/"):
            modelname = parts[1]
            parts = parts[2:]  # remove modelname

        elementname = parts[-1]
        elementpath = parts[0:-1]
        return modelname, elementpath, elementname

    @staticmethod
    def addmodeltonamedreference(namedref: str, modelname: str):
        """ if namedreference starts with / do nothing (it starts with a model)
            if not, create a new namedreference, starting with /modelname/
        """
        # if namedref.startswith("/"): return namedref
        modelname2, elementpath, elementname = Dataspot2Jsonbase.namedreference2struct(namedref)
        return Dataspot2Jsonbase.refparts2namedreference(modelname=nvl(modelname2, modelname),
                                                         elementpath=elementpath, elementname=elementname)

    @staticmethod
    def refparts2namedreference(elementname: str, modelname: str = None, elementpath: list = None):
        """ combines the element-path-parts into a single string
            [<modelname>]:[<elementpath>/]*<elementname>
            all names containing "/" or . are enclosed in ""
        """
        retval = ""
        if modelname is not None:
            retval += fullescapestr(modelname) + ":"
        if len(alwayslist(elementpath)) > 0:
            retval += "/".join([fullescapestr(ep) for ep in elementpath]) + "/"
        retval += nvl(fullescapestr(elementname))
        return retval

    @staticmethod
    def getadditionalprop(elem: JsonElement, propname: str):
        return elem.getadditionalprop(propname)

    @staticmethod
    def findelement(elems, modelname, name, fullname=False):
        if name is None:
            return None
        elif name.startswith("/"):
            # name is in other model
            namepath = custom_split(name, "/")
            elem = [val for key, val in elems.items() if
                    key.startswith(namepath[1]) and key.endswith("/" + "/".join(namepath[2:]))]
        else:
            elem = [val for key, val in elems.items() if
                    key.startswith(modelname + "/")
                    and ((fullname and key[len(modelname) + 1:] == name.strip(r"[\"\']"))
                         or (not fullname and key.endswith("/" + name.strip(r"[\"\']"))))]
        if elem is None or len(elem) != 1:
            return None
        else:
            return elem[0]

    @staticmethod
    def findelementid(elems, modelname, name, notnull=False, fullname=False):
        elem = Dataspot2Jsonbase.findelement(elems=elems, modelname=modelname,
                                             name=name, fullname=fullname)
        assert not (elem is None and notnull), f"{modelname}-{name} not found"
        return None if elem is None else elem.get("ID")

    @classmethod
    def additionalprops(cls, elem, specialkeys) -> dict:
        defaultfields = ["_type", "label",
                         "id", "href", "subtypeOf",
                         "examples", "synonyms", "favorite",
                         "description", "title", "inCollection",
                         "status", "createdBy", "dateCreated",
                         "hasDomain", "hasRange", "stereotype", "name", "inverseName", "navigable",
                         "domainMultiplicity","rangeMultiplicity",
                         "identifying","baseType","maxLength","pattern",
                         "minInclusive","maxInclusive",
                         "integerDigits","fractionDigits",
                         "required","cardinality","ARC-21","ARC-12"
                         "ID", "TYPE", "DSMODEL", "PARENT", "PARENT2"]
        retval = {key: val for key, val in elem.items() if key not in (defaultfields + specialkeys)}
        if "id" in elem: retval["SOURCE-ID"] = elem.get("id")
        if "DSMODEL" in elem: retval["SOURCE-MODEL"] = elem.get("DSMODEL")
        return retval

    @staticmethod
    def _cardinality(multiplicity):
        """translate 0..*,1,0..1,* into 1 or M"""
        return "1" if multiplicity is None else "1" if "1" in multiplicity else "M"

    @staticmethod
    def _mandatory(multiplicity):
        """translate 0..*,1,0..1,* into true or false"""
        return multiplicity in ("1", "*")

    @staticmethod
    def _relationtype(element):
        """ get the relationship type from the elementdefinition"""
        frommany = Dataspot2Jsonbase._cardinality(element.get("rangeMultiplicity")) == 'M'
        tomany = Dataspot2Jsonbase._cardinality(element.get("domainMultiplicity")) == 'M'
        frommand = Dataspot2Jsonbase._mandatory(element.get("rangeMultiplicity"))
        tomand = Dataspot2Jsonbase._mandatory(element.get("domainMultiplicity"))
        fromarc = element.get("ARC-12") is not None
        toarc = element.get("ARC-21") is not None
        if frommany and tomany:
            return "M:N"
        elif frommany != tomany:
            return "M:1"
        elif not frommany and not tomany and (frommand != tomand):
            return "ROLE"  # 1:1 1opt 1mand
        elif not frommany and not tomany and frommand and tomand and (fromarc or toarc):
            return "SUBTYPE"  # 1:1 2mand 1 in arc
        else:
            return "1:1"  # 1:1 not subtype not role

    def relationjsonbase(self, relationtype,
                         element,
                         entityid1=None, dataobjectid1=None,
                         entityid2=None, dataobjectid2=None
                         ):
        additionalprops = self.additionalprops(elem=element,
                                               specialkeys=["name",
                                                            "inverseName",
                                                            "domainMultiplicity",
                                                            "rangeMultiplicity",
                                                            "arcno", "required",
                                                            "cardinality",
                                                            "navigable",
                                                            "ARC-21", "ARC-12"])
        additionalprops["SOURCE-HREF"] = self.dsmodels.sourcehref(element)
        intval = lambda x: None if element.get(x) is None else int(element.get(x))
        fwdend = JsonElement().relationendjson(entityid=entityid1,
                                               dataobjectid=dataobjectid1,
                                               assoctext=self.mutlilangvalue(
                                                   fieldname="name",
                                                   value=self._deref(element.get("name")),
                                                   addprops=additionalprops),
                                               cardinality=self._cardinality(
                                                   element.get("rangeMultiplicity")),
                                               mandatory=self._mandatory(
                                                   element.get("rangeMultiplicity")),
                                               historicised=element.get("temporal"),
                                               arcnumber=intval("ARC-12")
                                               )
        bwdend = JsonElement().relationendjson(entityid=entityid2,
                                               dataobjectid=dataobjectid2,
                                               assoctext=self.mutlilangvalue(
                                                   fieldname="inverseName",
                                                   value=self._deref(
                                                       element.get("inverseName")),
                                                   addprops=additionalprops),
                                               cardinality=self._cardinality(
                                                   element.get("domainMultiplicity")),
                                               mandatory=self._mandatory(
                                                   element.get("domainMultiplicity")),
                                               historicised=None,
                                               arcnumber=intval("ARC-21"))
        elemrela = JsonElement().relationjson(elementid=element.get("ID"),
                                              relationtype=relationtype,
                                              # relaname=self._relationname(entiid1=entityid1,
                                              #                             assoc=fwdend.data.get("assoctext"),
                                              #                             entiid2=entityid2
                                              #                             ),
                                              fwd=fwdend,
                                              bwd=bwdend,
                                              examples=element.get("examples"),
                                              additionalProps=additionalprops
                                              )

        # TODO  examples in relationships (generate them?)
        return elemrela

    def relationjson(self, modelname, relationtype, element):
        entityid1 = self.findelementid(elems=self.dsmodels.entities,
                                       modelname=modelname,
                                       name=self._deref(element.get("PARENT")))
        dataobjectid1 = self.findelementid(elems=self.dsmodels.tables,
                                           modelname=modelname,
                                           name=self._deref(element.get("PARENT")))
        entityid2 = self.findelementid(elems=self.dsmodels.entities,
                                       modelname=modelname,
                                       name=self._deref(element.get("PARENT2")))
        dataobjectid2 = self.findelementid(elems=self.dsmodels.tables,
                                           modelname=modelname,
                                           name=self._deref(element.get("PARENT2")))
        assert entityid1 is not None or dataobjectid1 is not None, f"Missing entity/table parent {element.get('PARENT')}->{element.get('PARENT2')}"
        assert entityid2 is not None or dataobjectid2 is not None, f"Missing entity/table parent {element.get('PARENT2')}->{element.get('PARENT')}"

        return self.relationjsonbase(relationtype=relationtype,
                                     entityid1=entityid1, dataobjectid1=dataobjectid1,
                                     entityid2=entityid2, dataobjectid2=dataobjectid2,
                                     element=element)

    def fillrelation(self, modelname, rela):
        self.imjson.addelementinstance(name="Relations",
                                       val=self.relationjson(modelname=modelname,
                                                             # key=ElementId.nextid("RELA"),
                                                             relationtype=self._relationtype(rela),
                                                             element=rela)
                                       )

        return

    def domasubattrs(self, element):
        domattrs = [da for da in self.dsmodels.attributes.values()
                    if element.get("ID") == self.findelementid(elems=self.dsmodels.domains,
                                                               modelname=da.get("DSMODEL"),
                                                               name=da.get("hasDomain")
                                                               )]
        return domattrs

    @staticmethod
    def _filldomaproperties(element, subtypeproperties):
        domaintypes = {"STRING": "TextDomain",
                       "TEXT": "TextDomain",
                       "ID": "TextDomain",
                       "GROUP": "GroupDomain",
                       "LOV": "LOVDomain",
                       "INTEGER": "NumericDomain",
                       "DECIMAL": "NumericDomain",
                       "DATETIME": "DatetimeDomain",
                       "DATE": "DatetimeDomain",
                       "TIME": "TextDomain",
                       "BINARY": "BinaryDomain",
                       "BOOLEAN": "BooleanDomain"
                       }
        if element.get("_type") == "ReferenceObject":
            domaintype = "LOV"
        else:
            domaintype = element.get("baseType", "STRING")

        subtypeproperties["domaintype"] = domaintypes[domaintype]
        if domaintype in ("STRING", "TEXT"):
            JsonElement.optionalprop(subtypeproperties, "maxlength", element.get("maxLength"), intvalue=True)
            JsonElement.optionalprop(subtypeproperties, "syntaxrule", element.get("pattern"))
            JsonElement.optionalprop(subtypeproperties, "minlength", element.get("minlength"), intvalue=True)
        elif domaintype in ("DECIMAL", "INTEGER"):
            JsonElement.optionalprop(subtypeproperties, "minvalue", element.get("minInclusive"), intvalue=True)
            JsonElement.optionalprop(subtypeproperties, "maxvalue", element.get("maxInclusive"), intvalue=True)
            if element.get("integerDigits") is not None or element.get("fractionDigits") is not None:
                subtypeproperties["totaldigits"] = element.get("integerDigits", 0) + element.get("fractionDigits", 0)
            JsonElement.optionalprop(subtypeproperties, "fractdigits", element.get("fractionDigits"),
                                     intvalue=True)
            JsonElement.optionalprop(subtypeproperties, "unit", element.get("Unit"))
        elif domaintype == "GROUP":
            pass
        elif domaintype == "DATETIME":
            subtypeproperties["granularity"] = "MINUTE"
        elif domaintype == "DATE":
            subtypeproperties["granularity"] = "DAY"
        elif domaintype == "TIME":
            subtypeproperties["syntaxrule"] = "^[0-1][0-9]:[0-5][0-9]$"

        return

    def setdomainsubtype(self, element, subtypeproperties):
        self._filldomaproperties(element=element,
                                 subtypeproperties=subtypeproperties)

        if len(self.domasubattrs(element=element)) > 0:
            subtypeproperties["domaintype"] = "GroupDomain"

        if subtypeproperties["domaintype"] == "LOVDomain":
            domaname = element.get("label")
            refvalues = [val for val in self.dsmodels.LOVvalues.values() \
                         if val.get("_type") == "ReferenceValue" and \
                         val.get("literalOf") == domaname]
            values = []
            for val in refvalues:
                if val.get("timeSeries") in (None, []):
                    logging.warning(f"no timeseries in value {val.get('id')} of reference type {val.get('literalOf')} ")
                    val["code"] = "??? missing ???"
                    val["shortText"] = None
                    val["longText"] = None
                else:
                    youngesttimerserie = val.get("timeSeries")[-1]
                    # TODO time series > 0
                    # workaround, add timeseries attributes to valuestrucuture
                    val["code"] = youngesttimerserie.get("code")
                    val["shortText"] = youngesttimerserie.get("shortText")
                    val["longText"] = youngesttimerserie.get("longText")

                valadditionalprops = self.additionalprops(elem=val, specialkeys=["literalOf", "timeSeries",
                                                                                 "code",
                                                                                 "shortText", "longText"])
                newvalue = JsonElement().refvaluejson(value=val.get("code"),
                                                      displayvalue=self.mutlilangvalue(fieldname="shortText",
                                                                                       value=val.get("shortText"),
                                                                                       addprops=valadditionalprops),
                                                      description=self.mutlilangvalue(fieldname="longText",
                                                                                      value=val.get("longText"),
                                                                                      addprops=valadditionalprops),
                                                      additionalProps=valadditionalprops
                                                      )
                # TODO subvalues unter values auch beim Domain!
                newvalue.addoptionalprop(propname="additionalProps",
                                         value=valadditionalprops)
                values.append(newvalue.data)

            subtypeproperties["values"] = values
        return

    def businessrulejson(self, key, element):
        restricted = custom_split(element.get("constraintOn"), "/")
        if len(restricted) == 1:
            # assume entitiy or domainid or dataobject
            restrid = self.getentityid(entiname=restricted[0])
            if restrid is None:
                restrid = self.getdomainid(domaname=restricted[0])
            if restrid is None:
                restrid = self.getdataobjectid(datoname=restricted[0])
        else:
            # assume attribute or relation
            if ">" in restricted[1]:
                # relation
                restrid = self.getrelationid(entiname=restricted[0],
                                             rela=restricted[1])
            else:  # attribute
                restrid = self.getattributeid(parentname=restricted[0],
                                              attrname=restricted[1],
                                              modelname=element.get("DSMODEL"))
                if restrid is None:
                    # try column
                    restrid = self.getcolumnid(datoname=restricted[0],
                                               coluname=restricted[1])

        jsonstruct = JsonElement().businessrulejson(elementid=key,
                                                    restrictedelems=[restrid],
                                                    description=element.get("description"),
                                                    rule=element.get("computation")
                                                    )

        return jsonstruct

    def generatebusinessrules(self, elementname, elements):
        for element in elements:
            self.standardjson.addelementinstance(name=elementname,
                                                 val=self.businessrulejson(key=ElementId.nextid("BURU"),
                                                                           element=element)
                                                 )
        return

    def generatedomains(self, status=None):
        for element in self.dsmodels.domains.values():
            if DataspotElements.checkstatus(element, status):
                self.standardjson.addelementinstance(name="Domains",
                                                     val=self.generate1domain(doma=element))
        return

    def generate1domain(self, doma):

        catgid = self.findelementid(elems=self.dsmodels.categories,
                                    modelname=doma.get("DSMODEL"),
                                    name=doma.get("inCollection"), notnull=True)
        additionalprops = self.additionalprops(elem=doma,
                                               specialkeys=["minInclusive",
                                                            "maxInclusive",
                                                            "minLength", "maxLength",
                                                            "integerDigits",
                                                            "fractionDigits",
                                                            "baseType",
                                                            "Unit", "pattern"
                                                            ])
        additionalprops["SOURCE-HREF"] = self.dsmodels.sourcehref(doma)

        JsonElement.optionalprop(destobject=additionalprops,
                                 propname="SOURCE-DATATYPE",
                                 value=doma.get("baseType"))
        subtypeproperties = {"description": self.mutlilangvalue(fieldname="description",
                                                                value=doma.get("description"),
                                                                addprops=additionalprops)
                             }
        self.setdomainsubtype(element=doma, subtypeproperties=subtypeproperties)

        subtypeproperties["additionalProps"] = additionalprops
        elemdoma = JsonElement().domainjson(elementid=doma.get("ID"),
                                            name=self.mutlilangvalue(fieldname="label",
                                                                     value=doma.get("label"),
                                                                     addprops=additionalprops),
                                            categoryid=catgid,
                                            **subtypeproperties
                                            )
        return elemdoma

    def generatederivations(self, status=None):
        """ read all derivations and add them to the derivations of the model, if the target is in this model
        """
        for keyderiv, deriv in self.dsmodels.derivations.items():
            if not DataspotElements.checkstatus(deriv, status): continue
            sourcepath = self.addmodeltonamedreference(namedref=deriv.get("derivedFrom"),
                                                       modelname=deriv.get("DSMODEL"))
            sourceelement = self.findqualielement(fullpath=sourcepath)
            targetpath = self.addmodeltonamedreference(namedref=deriv.get("derivedTo"),
                                                       modelname=deriv.get("DSMODEL"))
            targetelement = self.findqualielement(fullpath=targetpath)
            if targetelement is None:
                # target not found, is not part of the current model
                continue

            # add derivation to found element
            if sourceelement is None:
                sourceelementid = sourcepath
            else:
                sourceelementid = sourceelement.getid()

            additionalprops = self.additionalprops(elem=deriv,
                                                   specialkeys=["derivedTo",
                                                                "derivedFrom",
                                                                "qualifier"
                                                                ])

            self.standardjson.addelementinstance(name="Derivations",
                                                 val=JsonElement().derivationjson
                                                 (derivationtype=deriv.get("qualifier"),
                                                  sourceelement=sourceelementid,
                                                  targetelement=targetelement.getid(),
                                                  additionalProps=additionalprops
                                                  )
                                                 )

        return

    def generatetransformations(self, status=None):
        """ read all transformations and add them to the element
        """
        for trakey, transf, in self.dsmodels.transformations.items():
            if not DataspotElements.checkstatus(transf, status): continue
            transpath = transf.get("transformationOf") + "/" + transf.get("label")

            additionalprops = self.additionalprops(elem=transf,
                                                   specialkeys=["transformationOf"])
            transfname = self.mutlilangvalue(fieldname="label",
                                             value=transf.get("label"),
                                             addprops=additionalprops)
            rules = [r for r in self.dsmodels.rules.values() if r.get("ruleOf") == transpath]
            for rule in rules:
                sourceelements = [nvl(self.findqualielement(
                    fullpath=self.addmodeltonamedreference(namedref=t, modelname=rule.get("DSMODEL"))), t)
                    for t in rule.get("transformsFrom", [])]
                sourceelements = [se.getid() if isinstance(se, JsonElement) else se for se in sourceelements]
                targetelements = [nvl(self.findqualielement(
                    fullpath=self.addmodeltonamedreference(namedref=t, modelname=rule.get("DSMODEL"))), t)
                    for t in rule.get("transformsTo", [])]
                targetelements = [se.getid() if isinstance(se, JsonElement) else se for se in targetelements]
                self.standardjson.addelementinstance(name="Transformations",
                                                     val=JsonElement().transformationjson
                                                     (name=transf.get("label"),
                                                      targetelements=targetelements,
                                                      sourceelements=sourceelements,
                                                      fwd=JsonElement().transformationrulejson(rule=rule.get("code"),
                                                                                               condition=rule.get(
                                                                                                   "condition")),
                                                      bwd=JsonElement().transformationrulejson(rule=None,
                                                                                               condition=None),
                                                      additionalProps=additionalprops
                                                      )
                                                     )
        return

    def findanyid(self, modelname, name, notnull=False):
        retval = self.findelementid(elems=self.dsmodels.attributes,
                                    modelname=modelname,
                                    name=name)
        if retval is None:
            retval = self.findelementid(elems=self.dsmodels.entities,
                                        modelname=modelname,
                                        name=name)
        if retval is None:
            retval = self.findelementid(elems=self.dsmodels.tables,
                                        modelname=modelname,
                                        name=name)
        if retval is None:
            retval = self.findelementid(elems=self.dsmodels.columns,
                                        modelname=modelname,
                                        name=name)
        if retval is None:
            retval = self.findelementid(elems=self.dsmodels.categories,
                                        modelname=modelname,
                                        name=name)
        if retval is None:
            retval = self.findelementid(elems=self.dsmodels.relationships,
                                        modelname=modelname,
                                        name=name)
        if retval is None:
            retval = self.findelementid(elems=self.dsmodels.domains,
                                        modelname=modelname,
                                        name=name)
        if retval is None:
            retval = self.findelementid(elems=self.dsmodels.systems,
                                        modelname=modelname,
                                        name=name)
        if retval is None:
            retval = self.findelementid(elems=self.dsmodels.transformations,
                                        modelname=modelname,
                                        name=name)

        assert not (retval is None and notnull), f"{name} in {modelname} not found"
        return retval

    def findqualielement(self, fullpath: str,
                         elemtype: str = None):
        """ find element fully qualified by fullpathj"""
        frommodel, frompath, fromelement = self.namedreference2struct(fullpath)
        elements = self.standardjson.getanyelementsbyfield(name=fromelement,
                                                           field="name") + \
                   self.standardjson.getelementinstances("Relations")

        retval = []
        for elem in elements:
            # if FULLPATH ist defined, use it
            if elem.getname() == fullpath:  # getadditionalprop("FULLPATH")
                retval.append(elem)
            else:
                elemmodel, elempath, elemname = self.namedreference2struct(
                    namedref=self.standardjson.getfullpath(elem=elem))
                # assert len(frompath) <= 1, "mehrfach path muss noch gemacht werden"
                if (frommodel == elemmodel) and \
                        (fromelement == elemname) and \
                        (len(frompath) <= len(
                            elempath) and  # both paths are equal from the end to the beginning of the frompath
                         (frompath == [] or frompath[-len(frompath):] == elempath[-len(frompath):])) and \
                        (elemtype is None or
                         (elemtype == elem.elemtype)):
                    retval.append(elem)
        if len(retval) == 1:
            return retval[0]
        else:
            return None

    @staticmethod
    def _deref(name: str):
        return name if type(name) is not str else name.strip('"')

    def __str__(self):
        return self.model
