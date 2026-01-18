import copy
import logging
from datetime import datetime

from INTERFACES.DATASPOT.imstandard_dataspot.dselements import DataspotElements
from INTERFACES.DATASPOT.imstandard_dataspot.json2dataspot import Json2dataspot as j2d
from IM_STANDARD import ElementId,alwayslist,nvl,JsonSchema,JsonElement


def mseconds2date(seconds):
    return datetime.utcfromtimestamp(seconds / 1000)


def date2mseconds(date):
    # todo timezone
    return int(date.timestamp() * 1000)


class Dataspot2Jsonbase(DataspotElements):
    ORIGINTOOL = "dataspot"

    def __init__(self, standardjson: JsonSchema, indirec=None, **kwargs):
        super().__init__(indirec=indirec, **kwargs)
        self.standardjson: JsonSchema = standardjson
        return

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
            retval = {} if value is None else {self.standardjson.mainlang: value}
            for otherlang in self.standardjson.languages:
                if otherlang == self.standardjson.mainlang: continue
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

    def createmultimodelcategories(self):
        def typemulticatg(models, catgtype):
            if len(models) > 1:
                descr = "Dataspot-Modell in eine oberste Kategorie im Standardmodell übersetzt" \
                    if self.standardjson.mainlang == 'de' \
                    else "dataspot model translated into a top level category in standard model"
                for model in models:
                    replacedkeys = []
                    for key, catg in self.categories.items():
                        if catg.get("TYPE") == catgtype and catg.get("DSMODEL") == model:
                            if catg.get("PARENT") is None:
                                catg["PARENT"] = model
                                catg["inCollection"] = model
                            replacedkeys.append(key)
                    for key in replacedkeys:
                        self.categories[f"{model}/{key}"] = self.categories[key]
                        del self.categories[key]

                    nextid = ElementId.nextid("CATG")

                    self.categories[f"{model}/{model}"] = {'_type': 'Collection',
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
        diffimmodels = set(c.get("DSMODEL") for c in self.categories.values() if c.get("TYPE") == "ENTITY")
        typemulticatg(models=diffimmodels, catgtype='ENTITY')
        diffdomainmodels = set(c.get("DSMODEL") for c in self.categories.values() if c.get("TYPE") == "DOMAIN")
        typemulticatg(models=diffdomainmodels, catgtype='DOMAIN')
        diffsystemmodels = set(c.get("DSMODEL") for c in self.categories.values() if c.get("TYPE") == "SYSTEM")
        typemulticatg(models=diffsystemmodels, catgtype='SYSTEM')
        diffsystemmodels = set(c.get("DSMODEL") for c in self.categories.values() if c.get("TYPE") == "DATAMODEL")
        typemulticatg(models=diffsystemmodels, catgtype='DATAMODEL')

        return

    def generatecategories(self, catgtype):
        categories = {key: val for key, val in self.categories.items() if val.get("TYPE") == catgtype}
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
                    newcategories.append(self.catgjson(element=catg
                                                       , categorytype=catgtype)
                                         )
                    donecatgs[catg.get("label")] = catg.get("ID")
                    del restcatgs[key]
                else:
                    fullname = parentname + "/" + catg.get("label")
                    if parentname not in restcatgs:  # parent was alredy processed
                        newcategories.append(self.catgjson(element=catg
                                                           , categorytype=catgtype)
                                             )
                        donecatgs[fullname] = catg.get("ID")
                        del restcatgs[key]
                    else:
                        pass
        #self.modelcategories[catgtype] = doxnecatgs
        self.standardjson.addelementinstance(name="Categories", val=newcategories)
        return

    def getelementbyid(self, elements, id):
        elem = [e for e in elements.values() if e.get("ID") == id]
        if len(elem) == 0:
            return None
        elif len(elem) == 1:
            return elem[0]
        assert False, f"element id {id} found more than once"

    def getelementid(self, elementtype, elementname):
        """ beware of translated names with mlvalue() """
        elements = {self.standardjson.mlvalue(elem["name"]): elem.getid()
                    for elem in self.standardjson.jsonschemamodel.get(elementtype, [])}
        return elements.get(self._deref(elementname)) if elements else None

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
                 [val for key,val in attr.getadditionalprops().items() if key == "SOURCE-MODEL"]
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

    def categoryid(self, modeltype, categoryname):
        modelcatg = self.modelcategories.get(modeltype)
        if modelcatg is None:
            return None
        else:
            return modelcatg.get(categoryname)

    def catgjson(self, element, categorytype):
        parentname = element.get("PARENT")
        parentid = None if parentname is None \
            else self.findelementid(elems=self.categories,
                                    modelname=element.get("DSMODEL"),
                                    name=parentname, fullname=True)

        additionalprops = self.additionalprops(elem=element, specialkeys=["parentid"])
        jsonstruct = JsonElement().categoryjson(elementid=element.get("ID"),
                                                    name=self.mutlilangvalue(fieldname="label",
                                                                             value=element.get("label"),
                                                                             addprops=additionalprops),
                                                    description=self.mutlilangvalue(fieldname="description",
                                                                                    value=element.get("description"),
                                                                                    addprops=additionalprops),
                                                    categorytype=categorytype,
                                                    categoryid=parentid,
                                                    additionalProps=additionalprops)
        return jsonstruct

    @staticmethod
    def namedreference2struct(namedref:str):
        """ separates a refrence to an object into its components
            [/<modelname>]:[<elementpath>/]*<elementname>
            alle Namen die ein "/" oder ein Spezialzeichen enthalten sind in ""
            return
            modelname: None or firstname after /
            elementpath : list of names between

        """
        if namedref is None: return (None,None,None)
        if ":" in namedref:
            parts = j2d.custom_split(input_string=namedref, delimiter=":")
            modelname=parts[0]
            parts = [parts[1]]
        else:
            parts = j2d.custom_split(input_string=namedref, delimiter="/")
            if namedref.startswith("/"):
                modelname=parts[1]
                parts = parts[2:]  # remove modelnam
            else:
                modelname=None
        elementname=parts[-1]
        elementpath=parts[0:-1]
        return modelname,elementpath,elementname

    @staticmethod
    def addmodeltonamedreference(namedref:str,modelname:str):
        """ if namedreference starts with / do nothing (it starts with a model)
            if not, create a new namedreference, starting with /modelname/
        """
        #if namedref.startswith("/"): return namedref
        modelname2,elementpath,elementname=Dataspot2Jsonbase.namedreference2struct(namedref)
        return Dataspot2Jsonbase.refparts2namedreference(modelname=nvl(modelname2,modelname),
                                                         elementpath=elementpath,elementname=elementname)

    @staticmethod
    def refparts2namedreference(elementname:str,modelname:str=None,elementpath:list=None):
        """ combines the element-path-parts into a single string
            [<modelname>]:[<elementpath>/]*<elementname>
            all names containing "/" or . are enclosed in ""
        """
        retval = ""
        if modelname is not None:
            retval += j2d.fullescapestr(modelname) + ":"
        if len(alwayslist(elementpath))>0:
            retval += "/".join([j2d.fullescapestr(ep) for ep in elementpath]) + "/"
        retval += nvl(j2d.fullescapestr(elementname))
        return retval

    @staticmethod
    def getadditionalprop(elem: JsonElement, propname: str):
        return elem.getadditionalprop(propname)

    def findelement(self, elems, modelname, name, fullname=False):
        if name is None:
            return None
        elif name.startswith("/"):
            # name is in other model
            namepath = j2d.custom_split(name, "/")
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

    def findelementid(self, elems, modelname, name, notnull=False, fullname=False):
        elem = self.findelement(elems=elems, modelname=modelname,
                                name=name, fullname=fullname)
        assert not (elem is None and notnull), f"{modelname}-{name} not found"
        return None if elem is None else elem.get("ID")

    @classmethod
    def additionalprops(cls, elem, specialkeys)->dict:
        defaultfields = ["_type", "label",
                         "id", "href",
                         "examples", "synonyms", "favorite",
                         "description", "title", "inCollection",
                         "status", "createdBy", "dateCreated",
                         "hasDomain", "hasRange", "stereotype",
                         "ID", "TYPE", "DSMODEL", "PARENT", "PARENT2"]
        retval = {key: val for key, val in elem.items() if key not in (defaultfields + specialkeys)}
        if "id" in elem: retval["SOURCE-ID"]= elem.get("id")
        if "DSMODEL" in elem: retval["SOURCE-MODEL"]= elem.get("DSMODEL")
        return retval

    @staticmethod
    def _cardinality(multiplicity):
        """translate 0..*,1,0..1,* into 1 or M"""
        return "1" if multiplicity is None else "1" if "1" in multiplicity else "M"

    @staticmethod
    def _mandatory(multiplicity):
        """translate 0..*,1,0..1,* into true or false"""
        return multiplicity in ("1", "*")

    def _relationtype(self, element):
        """ get the relationship type from the elementdefinition"""
        frommany = self._cardinality(element.get("rangeMultiplicity")) == 'M'
        tomany = self._cardinality(element.get("domainMultiplicity")) == 'M'
        frommand = self._mandatory(element.get("rangeMultiplicity"))
        tomand = self._mandatory(element.get("domainMultiplicity"))
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
                                                    fwd=fwdend,
                                                    bwd=bwdend,
                                                    examples=element.get("examples"),
                                                    additionalProps=additionalprops
                                                    )

        # TODO  examples in relationships (generate them?)
        return elemrela

    def relationjson(self, modelname, relationtype, element):
        entityid1 = self.findelementid(elems=self.entities,
                                       modelname=modelname,
                                       name=self._deref(element.get("PARENT")))
        dataobjectid1 = self.findelementid(elems=self.tables,
                                      modelname=modelname,
                                      name=self._deref(element.get("PARENT")))
        entityid2 = self.findelementid(elems=self.entities,
                                       modelname=modelname,
                                       name=self._deref(element.get("PARENT2")))
        dataobjectid2 = self.findelementid(elems=self.tables,
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
                                                             key=ElementId.nextid("RELA"),
                                                             relationtype=self._relationtype(rela),
                                                             element=rela)
                                       )

        return

    def domasubattrs(self, element):
        domattrs = [da for da in self.attributes.values()
                    if element.get("ID") == self.findelementid(elems=self.domains,
                                                               modelname=da.get("DSMODEL"),
                                                               name=da.get("hasDomain")
                                                               )]
        return domattrs

    def setdomainsubtype(self, element, subtypeproperties):
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
        subattrs = self.domasubattrs(element=element)
        if element.get("_type") == "ReferenceObject":
            domaintype = "LOV"
        elif len(subattrs) > 0:
            domaintype = "GROUP"
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
            # NO group domains have sometimes a string rep and therefore a pattern
            # JsonElement.optionalprop(subtypeproperties, "maxlength", element.get("maxLength"), intvalue=True)
            # JsonElement.optionalprop(subtypeproperties, "syntaxrule", element.get("pattern"))
            # JsonElement.optionalprop(subtypeproperties, "minlength", element.get("minlength"), intvalue=True)
            # subtypeproperties["elements"] = [
            #    self.attributejson(modelname=element.get("DSMODEL"),
            #                       element=elem)
            #    for elem in subattrs]
            pass
        elif domaintype == "DATETIME":
            subtypeproperties["granularity"] = "MINUTE"
        elif domaintype == "DATE":
            subtypeproperties["granularity"] = "DAY"
        elif domaintype == "TIME":
            subtypeproperties["syntaxrule"] = "^[0-1][0-9]:[0-5][0-9]$"
        elif domaintype == "BOOLEAN":
            pass
        elif domaintype == "LOV":
            domaname = element.get("label")
            refvalues = [val for val in self.LOVvalues.values() \
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
        restricted = j2d.custom_split(element.get("constraintOn"), "/")
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

    def generatedomains(self):
        for element in self.domains.values():
            self.standardjson.addelementinstance(name="Domains",
                                                 val=self.generate1domain(doma=element))
        return

    def generate1domain(self, doma):

        catgid = self.findelementid(elems=self.categories,
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

    def findanyid(self, modelname, name, notnull=False):
        retval = self.findelementid(elems=self.attributes,
                                    modelname=modelname,
                                    name=name)
        if retval is None:
            retval = self.findelementid(elems=self.entities,
                                        modelname=modelname,
                                        name=name)
        if retval is None:
            retval = self.findelementid(elems=self.tables,
                                        modelname=modelname,
                                        name=name)
        if retval is None:
            retval = self.findelementid(elems=self.columns,
                                        modelname=modelname,
                                        name=name)
        if retval is None:
            retval = self.findelementid(elems=self.categories,
                                        modelname=modelname,
                                        name=name)
        if retval is None:
            retval = self.findelementid(elems=self.relationships,
                                        modelname=modelname,
                                        name=name)
        if retval is None:
            retval = self.findelementid(elems=self.domains,
                                        modelname=modelname,
                                        name=name)
        if retval is None:
            retval = self.findelementid(elems=self.systems,
                                        modelname=modelname,
                                        name=name)
        if retval is None:
            retval = self.findelementid(elems=self.transformations,
                                        modelname=modelname,
                                        name=name)

        assert not (retval is None and notnull), f"{name} in {modelname} not found"
        return retval

    @staticmethod
    def _deref(name: str):
        return name if type(name) is not str else name.strip('"')

    def __str__(self):
        return self.model
