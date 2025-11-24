import copy
import logging
from datetime import datetime

from INTERFACES.DATASPOT.imstandard_dataspot.dselements import DataspotElements
from INTERFACES.DATASPOT.imstandard_dataspot.json2dataspot import Json2dataspot as j2d
from IM_STANDARD.myjsonschema import ElementId, JsonSchema


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
                translkey=f"{fieldname}:{otherlang}"
                othervalue = {key:val for ap in addprops for key,val in ap.items()}.get(translkey)
                if othervalue is not None:
                    retval[otherlang] = othervalue
                    # remove this property from this additionalproperties
                    addprops.remove({translkey: othervalue})
                else:
                    capitalize = lambda s: s[0].upper() + s[1:]
                    translkey = f"{capitalize(fieldname)}:{otherlang}"
                    othervalue = {key:val for ap in addprops for key,val in ap.items()}.get(translkey)
                    if othervalue is not None:
                        retval[otherlang] = othervalue
                        # remove this property from this additionalproperties
                        addprops.remove({translkey: othervalue})
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
        self.modelcategories[catgtype] = donecatgs
        self.standardjson.addelementinstance(name="Categories", val=newcategories)
        return

    def generatedomains(self):
        for element in self.domains.values():
            self.standardjson.addelementinstance(name="Domains",
                                                 val=self.generate1domain(doma=element))
        return

    def _notnullentries(self, **kwargs):
        return {key: val for key, val in kwargs.items() if val is not None}

    def getelementbyid(self, elements, id):
        elem = [e for e in elements.values() if e.get("ID") == id]
        if len(elem) == 0:
            return None
        elif len(elem) == 1:
            return elem[0]
        assert False, f"element id {id} found more than once"

    def getelementid(self, elementtype, elementname):
        """ beware of translated names with mlvalue() """
        elements = {self.standardjson.mlvalue(elem.get("name")): elem.get("elementid")
                    for elem in self.standardjson.jsonschemamodel.get(elementtype,[])}
        return elements.get(self._deref(elementname)) if elements else None

    def getentityid(self, entiname):
        return self.getelementid(elementtype="Entities", elementname=entiname)

    def getdomainid(self, domaname):
        return self.getelementid(elementtype="Domains", elementname=domaname)

    def getdataobjectid(self, datoname):
        return self.getelementid(elementtype="DataObjects", elementname=datoname)

    def getattributeid(self, parentname, attrname,modelname=None):
        entiparent = self.standardjson.getbyid(self.getentityid(parentname))
        domaparent = self.standardjson.getbyid(self.getdomainid(parentname))
        if entiparent is None and domaparent is None:
            return None #no attribute found
        #check identical attribute in domain and entity with same name, separate by modelname
        entiid=None if entiparent is None else entiparent.get("elementid")
        domaid=None if domaparent is None else domaparent.get("elementid")
        attrs = {self.standardjson.mlvalue(attr.get("name")): attr.get("elementid")
                 for attr in self.standardjson.getelementinstances(elementname="Attributes")
                if attr.get("parentid") in (entiid,domaid) and
                 modelname in
                    [v for ap in attr.get("additionalProps",[])
                    for k, v in ap.items() if k == "SOURCE-MODEL"]
                 }
        return attrs.get(self._deref(attrname))

    def getcolumnid(self, datoname, coluname):
        parent = self.standardjson.getbyid(self.getdataobjectid(datoname))
        subelementsname = "columns"
        if parent is None:
            logging.error(f"DataObject '{datoname}' not found")
            return None
        colus = {self.standardjson.mlvalue(colu.get("name")): colu.get("elementid")
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

        additionalprops = self.additionalprops(elem=element, specialkeys=[])
        jsonstruct = self.standardjson.categoryjson(elementid=element.get("ID"),
                                                    name=self.mutlilangvalue(fieldname="label",
                                                                             value=element.get("label"),
                                                                             addprops=additionalprops),
                                                    description=self.mutlilangvalue(fieldname="description",
                                                                                    value=element.get("description"),
                                                                                    addprops=additionalprops),
                                                    categorytype=categorytype,
                                                    parent=parentid,
                                                    additionalProps=additionalprops)
        return jsonstruct

    def fillcategory(self, catg, catgtype):
        self.standardjson.addelementinstance(name="Categories"
                                             , val=self.catgjson(element=catg
                                                           , categorytype=catgtype)
                                             )

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
    def additionalprops(cls, elem, specialkeys):
        defaultfields = ["_type", "label",
                         "id", "href",
                         "examples", "synonyms", "favorite",
                         "description", "title", "inCollection",
                         "status", "createdBy", "dateCreated",
                         "hasDomain", "hasRange", "stereotype",
                         "ID", "TYPE", "DSMODEL", "PARENT", "PARENT2"]
        retval = [{key: val} for key, val in elem.items() if key not in (defaultfields + specialkeys)]
        if "id" in elem: retval.append({"SOURCE-ID": elem.get("id")})
        if "DSMODEL" in elem: retval.append({"SOURCE-MODEL": elem.get("DSMODEL")})
        return retval

    def systemids(self, modelname, elemid, searchelements):

        retval = [self.findelementid(elems=self.systems,
                                     modelname=modelname,
                                     name=depl.get("deployedIn"))
                  for depl in self.deployments.values()
                  if elemid == self.findelementid(elems=searchelements,
                                                  modelname=modelname,
                                                  name=depl.get("deploymentOf"))
                  ]
        return retval

    def fillcolumns(self, modelname, tableid):
        retval = []

        for elem in self.columns.values():
            if self.findelementid(elems=self.tables,
                                  modelname=modelname, name=elem.get("PARENT")) \
                    == tableid:
                retval.append(self.imjson.columnjson(
                    key=elem.get("ID"),
                    name=elem.get("label"),
                    domainid=self.findelementid(elems=self.domains,
                                                modelname=modelname,
                                                name=elem.get("hasRange")
                                                ),
                    mandatory=elem.get("required") == "MANDATORY",
                    order=elem.get("order"),
                    techname=elem.get("label").upper(),
                    description=elem.get("description"),
                    tooltip=elem.get("title"),
                    inSystems=self.systemids(modelname=modelname,
                                             elemid=elem.get("ID"),
                                             searchelements=self.columns),
                    additionalProps=self.additionalprops(elem=elem,
                                                         specialkeys=["required",
                                                                      "cardinality",
                                                                      "order"])
                ))
                return retval

    def attributejson(self, modelname, element):

        domainid = self.findelementid(elems=self.domains,
                                      modelname=modelname,
                                      name=element.get("hasRange"))

        additionalprops = self.additionalprops(elem=element,
                                               specialkeys=["required",
                                                            "temporal",
                                                            "MULTILINGUAL",
                                                            "cardinality",
                                                            "order",
                                                            "minInclusive",
                                                            "maxInclusive"
                                                            ])
        jsonstruct = self._notnullentries(elementid=element.get("ID"),
                                          name=self.mutlilangvalue(fieldname="label", value=element.get("label"),
                                                                   addprops=additionalprops),
                                          mandatory=element.get("required") == "MANDATORY",
                                          domainid=domainid,
                                          displayseq=element.get("order"),
                                          description=self.mutlilangvalue(fieldname="description",
                                                                          value=self._deref(element.get("description")),
                                                                          addprops=additionalprops),
                                          shortdescr=self.mutlilangvalue(fieldname="title",
                                                                         value=self._deref(element.get("title")),
                                                                         addprops=additionalprops),
                                          examples=element.get("examples"),
                                          descriptive=element.get("favorite"),
                                          historicised=element.get("temporal"),
                                          repeated=element.get("cardinality") == "MANY",
                                          translated=element.get("MULTILINGUAL"),
                                          # minvalue=element.get("minInclusive"),
                                          # maxvalue=element.get("maxInclusive"),
                                          additionalProps=additionalprops
                                          )
        return jsonstruct

    def fillattributes(self, modelname, entiname):
        retval = []
        for elem in self.attributes.values():
            if elem.get("DSMODEL") == modelname and \
                    elem.get("PARENT") == entiname:
                retval.append(self.attributejson(modelname=modelname,
                                                 element=elem))
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
                         entityid1=None, tableid1=None,
                         entityid2=None, tableid2=None
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
        fwdend = self.standardjson.relationendjson(entityid=entityid1,
                                                   tableid=tableid1,
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
        bwdend = self.standardjson.relationendjson(entityid=entityid2,
                                                   tableid=tableid2,
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
        jsonstruct = self.standardjson.relationjson(elementid=element.get("ID"),
                                                    relationtype=relationtype,
                                                    fwd=fwdend,
                                                    bwd=bwdend,
                                                    examples=element.get("examples"),
                                                    additionalProps=additionalprops
                                                    )

        # TODO  examples in relationships (generate them?)
        return jsonstruct

    def relationjson(self, modelname, relationtype, element):
        entityid1 = self.findelementid(elems=self.entities,
                                       modelname=modelname,
                                       name=self._deref(element.get("PARENT")))
        tableid1 = self.findelementid(elems=self.tables,
                                      modelname=modelname,
                                      name=self._deref(element.get("PARENT")))
        entityid2 = self.findelementid(elems=self.entities,
                                       modelname=modelname,
                                       name=self._deref(element.get("PARENT2")))
        tableid2 = self.findelementid(elems=self.tables,
                                      modelname=modelname,
                                      name=self._deref(element.get("PARENT2")))
        assert entityid1 is not None or tableid1 is not None, f"Missing entity/table parent {element.get('PARENT')}->{element.get('PARENT2')}"
        assert entityid2 is not None or tableid2 is not None, f"Missing entity/table parent {element.get('PARENT2')}->{element.get('PARENT')}"

        return self.relationjsonbase(relationtype=relationtype,
                                     entityid1=entityid1, tableid1=tableid1,
                                     entityid2=entityid2, tableid2=tableid2,
                                     element=element)

    def fillrelation(self, modelname, rela):
        self.imjson.addelementinstance(name="Relations",
                                       val=self.relationjson(modelname=modelname,
                                                       key=ElementId.nextid("RELA"),
                                                       relationtype=self._relationtype(rela),
                                                       element=rela)
                                       )

        return

    def fillentity(self, modelname, enti):
        self.imjson.addelementinstance(name="Entities",
                                       val=self.entityjson(element=enti)
                                       )
        self.imjson.jsonschemamodel["Entities"][-1]["attributes"] = self.fillattributes(modelname=modelname,
                                                                                        entiname=enti.get("label"))
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
            self.standardjson.optionalprop(subtypeproperties, "maxlength", element.get("maxLength"), intvalue=True)
            self.standardjson.optionalprop(subtypeproperties, "syntaxrule", element.get("pattern"))
            self.standardjson.optionalprop(subtypeproperties, "minlength", element.get("minlength"), intvalue=True)
        elif domaintype in ("DECIMAL", "INTEGER"):
            self.standardjson.optionalprop(subtypeproperties, "minvalue", element.get("minInclusive"), intvalue=True)
            self.standardjson.optionalprop(subtypeproperties, "maxvalue", element.get("maxInclusive"), intvalue=True)
            if element.get("integerDigits") is not None or element.get("fractionDigits") is not None:
                subtypeproperties["totaldigits"] = element.get("integerDigits", 0) + element.get("fractionDigits", 0)
            self.standardjson.optionalprop(subtypeproperties, "fractdigits", element.get("fractionDigits"),
                                           intvalue=True)
            self.standardjson.optionalprop(subtypeproperties, "unit", element.get("Unit"))
        elif domaintype == "GROUP":
            # group domains have sometimes a string rep and therefore a pattern
            self.standardjson.optionalprop(subtypeproperties, "maxlength", element.get("maxLength"), intvalue=True)
            self.standardjson.optionalprop(subtypeproperties, "syntaxrule", element.get("pattern"))
            self.standardjson.optionalprop(subtypeproperties, "minlength", element.get("minlength"), intvalue=True)
            #subtypeproperties["elements"] = [
            #    self.attributejson(modelname=element.get("DSMODEL"),
            #                       element=elem)
            #    for elem in subattrs]
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
                newvalue = self.standardjson.refvaluejson(value=val.get("code"),
                                                          displayvalue=self.mutlilangvalue(fieldname="shortText",
                                                                                           value=val.get("shortText"),
                                                                                           addprops=valadditionalprops),
                                                          description=self.mutlilangvalue(fieldname="longText",
                                                                                          value=val.get("longText"),
                                                                                          addprops=valadditionalprops),
                                                          additionalProps=valadditionalprops
                                                          )
                # TODO subvalues unter values auch beim Domain!
                self.standardjson.optionalprop(destobject=newvalue, propname="additionalProps",
                                               value=valadditionalprops)
                values.append(newvalue)

            subtypeproperties["values"] = values
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

        self.standardjson.optionalprop(destobject=additionalprops,
                                       propname="SOURCE-DATATYPE",
                                       value=doma.get("baseType"))
        subtypeproperties = {"description": self.mutlilangvalue(fieldname="description",
                                                                value=doma.get("description"),
                                                                addprops=additionalprops)
                             }
        self.setdomainsubtype(element=doma, subtypeproperties=subtypeproperties)

        subtypeproperties["additionalProps"] = additionalprops
        jsonstruct = self.standardjson.domainjson(elementid=doma.get("ID"),
                                                  name=self.mutlilangvalue(fieldname="label",
                                                                           value=doma.get("label"),
                                                                           addprops=additionalprops),
                                                  categoryid=catgid,
                                                  **subtypeproperties
                                                  )

        return jsonstruct

    def fillsystem(self, modelname, syst):
        dependson = [self.findelementid(elems=self.systems,
                                        modelname=modelname,
                                        name=dept.get("PARENT2"),
                                        notnull=True)
                     for dept in self.dependencies.values()
                     if syst.get("ID") == self.findelementid(elems=self.systems,
                                                             modelname=modelname,
                                                             name=dept.get("PARENT"),
                                                             notnull=True)]
        if len(dependson) == 0: dependson = None
        if syst.get('subsystemOf') is not None:
            # subsystem found
            parentid = self.findelementid(elems=self.systems,
                                          modelname=modelname,
                                          name=syst.get("subsystemOf"),
                                          notnull=True)
            jsonstruct = self._notnullentries(elementid=syst.get("ID"),
                                              name=syst.get("label"),
                                              parentid=parentid,
                                              dependsOn=dependson,
                                              additionalProps=self.additionalprops(elem=syst,
                                                                                   specialkeys=["subsystemOf"]
                                                                                   )
                                              )
        else:
            catgid = self.findelementid(elems=self.categories,
                                        modelname=modelname,
                                        name=syst.get("inCollection"),
                                        notnull=True)
            jsonstruct = self._notnullentries(elementid=syst.get("ID"),
                                              name=syst.get("label"),
                                              categoryid=catgid,
                                              dependsOn=dependson,
                                              additionalProps=self.additionalprops(elem=syst,
                                                                                   specialkeys=[]
                                                                                   ))

        self.imjson.addelementinstance(name="Systems",
                                       val=jsonstruct
                                       )

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
                    #try column
                    restrid = self.getcolumnid(datoname=restricted[0],
                                               coluname=restricted[1])

        jsonstruct = self.standardjson.businessrulejson(elementid=key,
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

    def fillbusinessrule(self, modelname, buru):
        appliedfor = [self.findanyid(modelname=buru.get("DSMODEL")
                                     , name=buru.get("PARENT"),
                                     notnull=True)]
        jsonstruct = self._notnullentries(elementid=buru.get("ID"),
                                          name=buru.get("label"),
                                          title=buru.get("title"),
                                          description=buru.get("description"),
                                          appliedfor=appliedfor,
                                          additionalProps=self.additionalprops(elem=buru,
                                                                               specialkeys=["constraintOn"]
                                                                               )
                                          )
        self.imjson.addelementinstance(name="BusinessRules",
                                       val=jsonstruct
                                       )

        return

    def filldiagram(self, modelname, diag):
        catgid = self.findelementid(elems=self.categories,
                                    modelname=modelname,
                                    name=diag.get("inCollection"),
                                    notnull=True)
        elements = [self.findanyid(modelname=val.get("usageOf").split("/")[1],
                                   name=val.get("usageOf"),
                                   notnull=True)
                    for val in self.diagelements.values()
                    if val.get("PARENT") == diag.get("label")]

        jsonstruct = self._notnullentries(elementid=diag.get("ID"),
                                          name=diag.get("label"),
                                          categoryid=catgid,
                                          elements=elements,
                                          additionalProps=self.additionalprops(elem=diag,
                                                                               specialkeys=[]
                                                                               ))

        self.imjson.addelementinstance(name="Diagrams",
                                       val=jsonstruct
                                       )

        return

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

    def fillrules(self, tfrmid):
        retval = dict()
        ruleno = 0
        for rule in self.rules.values():
            if rule.get("TYPE") == "DATA":
                if tfrmid == self.findelementid(self.transformations,
                                                modelname=rule.get("DSMODEL"),
                                                name=rule.get("ruleOf"),
                                                notnull=True):
                    retval[rule.get("label")] = \
                        self._notnullentries(inputs=[self.findanyid(modelname=rule.get("DSMODEL"),
                                                                    name=inp)
                                                     for inp in rule.get("transformsFrom", [])],
                                             outputs=[self.findanyid(modelname=rule.get("DSMODEL"),
                                                                     name=inp)
                                                      for inp in rule.get("transformsTo", [])],
                                             shortrule=rule.get("title"),
                                             rule=rule.get("description"),
                                             additionalProps=self.additionalprops(elem=rule,
                                                                                  specialkeys=[
                                                                                      "ruleOf",
                                                                                      "transformsFrom",
                                                                                      "transformsTo"]
                                                                                  )
                                             )
            elif rule.get("TYPE") == "VALUES":
                if tfrmid == self.findelementid(self.transformations,
                                                modelname=rule.get("DSMODEL"),
                                                name=rule.get("translationIn"),
                                                notnull=True):
                    ruleno += 1
                    retval[str(ruleno)] = \
                        self._notnullentries(inputs=[rule.get("translatesFrom")],
                                             outputs=[rule.get("translatesTo")],
                                             shortrule=rule.get("title"),
                                             rule=rule.get("description"),
                                             additionalProps=self.additionalprops(elem=rule,
                                                                                  specialkeys=[
                                                                                      "translatesFrom",
                                                                                      "translatesTo",
                                                                                      "translationIn"]
                                                                                  )
                                             )
            else:
                assert False, f"unknown rule type {rule.get('TYPE')}"
        return retval

    def filltransformation(self, tfrm):
        if tfrm.get("TYPE") == "DATA":
            jsonstruct = self._notnullentries(name=tfrm.get("label"),
                                              fromModels=[],
                                              toModels=[],
                                              rules=self.fillrules(
                                                  tfrmid=self.findelementid(self.transformations,
                                                                            modelname=tfrm.get("DSMODEL"),
                                                                            name=f"{tfrm.get('transformationOf')}/{tfrm.get('label')}",
                                                                            notnull=True)
                                              ),
                                              additionalProps=self.additionalprops(
                                                  elem=tfrm,
                                                  specialkeys=["TYPE",
                                                               "transformationOf"]
                                              ))
            rules = []
            for r in self.rules.values():
                if r.get("TYPE") not in ("DATA") or r.get("transformsFrom") is None: continue
                rules.append({m.split("/")[1] if m.startswith("/") else tfrm.get("DSMODEL")
                              for m in r.get("transformsFrom")})
            rset = set()
            for r in rules:
                rset = rset.union(r)
            jsonstruct["fromModels"] = list(rset)
            jsonstruct["toModels"] = [tfrm.get("DSMODEL")]  # in dataspot there is only one target for a transfomration
        elif tfrm.get("TYPE") == "VALUES":
            jsonstruct = self._notnullentries(name=tfrm.get("label"),
                                              fromDomain=self.findelementid(self.domains,
                                                                            modelname=tfrm.get("DSMODEL"),
                                                                            name=tfrm.get('mapsFrom'),
                                                                            notnull=True),
                                              toDomain=self.findelementid(self.domains,
                                                                          modelname=tfrm.get("DSMODEL"),
                                                                          name=tfrm.get('mapsTo'),
                                                                          notnull=True),
                                              rules=self.fillrules(
                                                  tfrmid=self.findelementid(self.transformations,
                                                                            modelname=tfrm.get("DSMODEL"),
                                                                            name=f"{tfrm.get('inCollection')}/{tfrm.get('label')}",
                                                                            notnull=True)
                                              ),
                                              additionalProps=self.additionalprops(
                                                  elem=tfrm,
                                                  specialkeys=["TYPE",
                                                               "mapsFrom",
                                                               "mapsTo"]
                                              ))
        else:
            assert False, f"unknow transformationtype {tfrm.get('TYPE')}"
        return jsonstruct

    def generateDOMAjson(self, modelname, targetenv):
        self.imjson = JsonSchema()

        self.imjson.setschemaelement(name="ModelInfo",
                                     val=self.imjson.modelinfojson(modelname=modelname,
                                                               modeltype="Domain model",
                                                               mainlanguage='en',
                                                               languages=None,  # TODO falls es mehrsprachiges hat,...
                                                               dc=str(datetime.now()),
                                                               modelversion="0.0",
                                                               targetenvironment=targetenv,
                                                               origintool=self.ORIGINTOOL))

        for elem in self.categories.values():
            if elem.get("DSMODEL") == modelname:
                self.fillcategory(catg=elem, catgtype="DOMAIN")
        for elem in self.domains.values():
            if elem.get("DSMODEL") == modelname:
                self.imjson.addelementinstance(name="Domains",
                                               val=self.generate1domain(doma=elem)
                                               )
        return self.imjson.jsonschemamodel

    def generateSYSTjson(self, modelname, targetenv):
        self.imjson = JsonSchema()
        self.imjson.setschemaelement(name="ModelInfo",
                                     val=self.imjson.modelinfojson(modelname=modelname,
                                                               modeltype="System model",
                                                               mainlanguage='en',
                                                               languages=None,  # TODO falls es mehrsprachiges hat,...
                                                               dc=str(datetime.now()),
                                                               modelversion="0.0",
                                                               targetenvironment=targetenv,
                                                               origintool=self.ORIGINTOOL))

        for elem in self.categories.values():
            if elem.get("DSMODEL") == modelname:
                self.fillcategory(catg=elem, catgtype="SYSTEM")
        for elem in self.systems.values():
            if elem.get("DSMODEL") == modelname:
                self.fillsystem(modelname=modelname, syst=elem)
        return self.imjson.jsonschemamodel

    def generateDIAGjson(self, modelname, targetenv):
        self.imjson = JsonSchema()
        self.imjson.modelinfojson(modelname=modelname,
                                  modeltype="Diagram",
                                  mainlanguage='en',
                                  languages=None,  # TODO falls es mehrsprachiges hat,...
                                  dc=str(datetime.now()),
                                  modelversion="0.0",
                                  targetenvironment=targetenv,
                                  origintool=self.ORIGINTOOL)

        for elem in self.categories.values():
            if elem.get("DSMODEL") == modelname:
                self.fillcategory(catg=elem, catgtype="PROJECT")
        for elem in self.diagrams.values():
            if elem.get("DSMODEL") == modelname:
                self.filldiagram(modelname=modelname, diag=elem)
        return self.imjson.jsonschemamodel

    def fillderivation(self, deriv):
        toid = self.findanyid(modelname=deriv.get("DSMODEL"),
                              name=deriv.get("derivedTo")
                              )
        if toid is None:
            logging.warning(f"missing to ID in {deriv.get('derivedFrom')}>{deriv.get('derivedTo')}")
            toid = f'{"" if deriv.get("derivedTo").startswith("/") else ("/" + deriv.get("DSMODEL") + "/")}{deriv.get("derivedTo")}'

        fromid = self.findanyid(modelname=deriv.get("DSMODEL"),
                                name=deriv.get("derivedFrom")
                                )
        if fromid is None:
            logging.warning(f"missing from ID in {deriv.get('derivedFrom')}>{deriv.get('derivedTo')}")
            fromid = f'{"" if deriv.get("derivedFrom").startswith("/") else ("/" + deriv.get("DSMODEL") + "/")}{deriv.get("derivedFrom")}'

        jsonstruct = self._notnullentries(  # name=f"{fromid}>{toid} {deriv.get('qualifier')}"
            derivedfrom=fromid,
            derivedto=toid,
            qualifier=deriv.get('qualifier'))
        return jsonstruct

    def generateDERIVjson(self):
        self.imjson = JsonSchema()
        self.imjson.jsonschemamodel.setdefault("derivations", [])
        for deriv in self.derivations.values():
            self.imjson.jsonschemamodel["derivations"].append(self.fillderivation(deriv=deriv))
        return self.imjson.jsonschemamodel["derivations"]

    def generateTFRMjson(self, tfrmtype):
        return
        # self.imjson = TFRMJsonSchema()
        # self.imjson.jsonschemamodel.setdefault(tfrmtype, [])
        # for tfrm in self.transformations.values():
        #     if tfrm.get("TYPE") == tfrmtype:
        #         self.imjson.jsonschemamodel[tfrmtype].append(self.filltransformation(tfrm=tfrm))
        # return self.imjson.jsonschemamodel[tfrmtype]

    def generateIMjson(self, modelname, targetenv):
        self.imjson = JsonSchema()
        self.imjson.setschemaelement(name="ModelInfo",
                                     val=self.imjson.modelinfojson(modelname=modelname,
                                                               modeltype="Information model",
                                                               mainlanguage='en',
                                                               languages=None,  # TODO falls es mehrsprachiges hat,...
                                                               dc=str(datetime.now()),
                                                               modelversion="0.0",
                                                               targetenvironment=targetenv,
                                                               origintool=self.ORIGINTOOL))

        for elem in self.categories.values():
            if elem.get("DSMODEL") == modelname:
                self.fillcategory(catg=elem, catgtype="ENTITY")
        for elem in self.entities.values():
            if elem.get("DSMODEL") == modelname:
                self.fillentity(modelname=modelname, enti=elem)
        for elem in self.relationships.values():
            if elem.get("DSMODEL") == modelname:
                self.fillrelation(modelname=modelname, rela=elem)
        for elem in self.businessrules.values():
            if elem.get("DSMODEL") == modelname:
                self.fillbusinessrule(modelname=modelname, buru=elem)

        return self.imjson.jsonschemamodel

    def generateDMjson(self, modelname, targetenv):
        self.imjson = JsonSchema()
        self.imjson.setschemaelement(name="ModelInfo",
                                     val=self.imjson.modelinfojson(modelname=modelname,
                                                               modeltype="Data model",
                                                               mainlanguage='en',
                                                               languages=None,  # TODO falls es mehrsprachiges hat,...
                                                               dc=str(datetime.now()),
                                                               modelversion="0.0",
                                                               targetenvironment=targetenv,
                                                               origintool=self.ORIGINTOOL))

        for elem in self.categories.values():
            if elem.get("DSMODEL") == modelname:
                self.fillcategory(catg=elem, catgtype="DATAOBJECT")
        for elem in self.tables.values():
            if elem.get("DSMODEL") == modelname:
                self.filltable(modelname=modelname, tabl=elem)
        for elem in self.relationships.values():
            if elem.get("DSMODEL") == modelname:
                self.fillrelation(modelname=modelname, rela=elem)
        for elem in self.businessrules.values():
            if elem.get("DSMODEL") == modelname:
                self.fillbusinessrule(modelname=modelname, buru=elem)

        return self.imjson.jsonschemamodel

    def generatefulljson(self, targetenv):
        dataspotjson = {"environment": targetenv,
                        "createdAt": str(datetime.now())}

        # do all information models
        ims = set([e["DSMODEL"] for e in self.entities.values()])
        for im in ims:
            dataspotjson.setdefault("InformationModels", [])
            dataspotjson["InformationModels"].append(self.generateIMjson(modelname=im,
                                                                         targetenv=targetenv)
                                                     )
        domas = set([e["DSMODEL"] for e in self.domains.values()])
        for doma in domas:
            dataspotjson.setdefault("DomainModels", [])
            dataspotjson["DomainModels"].append(self.generateDOMAjson(modelname=doma,
                                                                      targetenv=targetenv)
                                                )
        tabs = set([e["DSMODEL"] for e in self.tables.values()])
        for tab in tabs:
            dataspotjson.setdefault("Datamodels", [])
            dataspotjson["Datamodels"].append(self.generateDMjson(modelname=tab,
                                                                  targetenv=targetenv)
                                              )
        dataspotjson["Mappings"] = dict()
        dataspotjson["Mappings"]["DATA"] = self.generateTFRMjson(tfrmtype="DATA")
        dataspotjson["Mappings"]["VALUES"] = self.generateTFRMjson(tfrmtype="VALUES")
        dataspotjson["Mappings"]["DERIVATIONS"] = self.generateDERIVjson()

        syst = set([e["DSMODEL"] for e in self.systems.values()])
        for sy in syst:
            dataspotjson.setdefault("Systems", [])
            dataspotjson["Systems"].append(self.generateSYSTjson(modelname=sy,
                                                                 targetenv=targetenv)
                                           )

        diags = set([e["DSMODEL"] for e in self.diagrams.values()])
        for diag in diags:
            dataspotjson.setdefault("Diagrams", [])
            dataspotjson["Diagrams"].append(self.generateDIAGjson(modelname=diag,
                                                                  targetenv=targetenv)
                                            )

        return dataspotjson

        # self.modelinfojson(modelname=modelname, modeltype="Information model",
        #                    mainlanguage='en',
        #                    languages=None,  # TODO falls es mehrsprachiges hat,...
        #                    dc=None,
        #                    modelversion="0.0",
        #                    targetenvironment=targetenv,
        #                    origintool=self.ORIGINTOOL)
        #
        #
        # for modeltype, struct in self.modeltypeelements.items():
        #     if modeltype == "REFERENCE":
        #         self.generatelovs(struct)
        #     elif modeltype == "DATATYPE":
        #         self.generatedomains(struct)
        #     elif modeltype == "BUSINESSMODEL":
        #         self.generatebusinessmodel(struct)
        #     elif modeltype == "DATAMODEL":
        #         self.generatedatamodel(struct)

        return self.jsonschemamodel

    @staticmethod
    def _deref(name: str):
        return name if type(name) is not str else name.strip('"')

    def __str__(self):
        return self.model
