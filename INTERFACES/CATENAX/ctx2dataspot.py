import json
import logging
import re

from CATENAX import CatenaxFiles
from DATASPOT.imstandard_dataspot.json2dataspot import Json2dataspot


def nvl(a, b=""): return a if a is not None else b


class CTXInfra():

    @staticmethod
    def alwayslist(elem):
        return [] if elem is None \
            else elem if type(elem) is list \
            else [elem]


class UrnInfra():
    def __init__(self, sammobj):
        if type(sammobj) == str:
            objurn = sammobj
        elif type(sammobj) == dict:
            objurn = sammobj.get("x-samm-aspect-model-urn")
        else:
            raise Exception(f"{type(sammobj)}")
        if objurn is None:
            raise Exception()
        else:
            self._name = objurn.split("#")[-1]
            self._version = objurn.split(':')[-1].split("#")[0]
            self._direc = ':'.join(objurn.split(':')[:-1])
            self._direcversion = self._direc + ":" + self._version
            self._full = objurn
        return

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def direc(self):
        return self._direc

    @property
    def direcversion(self):
        return self._direcversion

    @property
    def full(self):
        return self._full


class CTXLoadJson():

    def __init__(self,
                 basepath,
                 allfiles):
        self.basepath = basepath
        self.allfiles = allfiles

        self.models = dict()
        self.readmodels()
        return

    def readmodels(self):
        donefiles = []

        while len(self.allfiles) > 0:
            filepath = self.allfiles[0]
            if filepath not in donefiles:
                self.models[filepath] = CatenaxFiles.read1file(filepath=filepath)
                self.allfiles += self.findchildren(self.models[filepath])
                self.allfiles = list(set(self.allfiles))
                donefiles.append(filepath)
            self.allfiles.remove(filepath)
        return

    def modelname(self, direcname):
        parts = direcname.split(".")
        modelname = "".join([p.capitalize() for p in parts[-1].split("_")])
        return modelname

    def findchildren(self, rootjson):
        jsonstring = json.dumps(rootjson)
        children = re.findall('"x-samm-aspect-model-urn" ?: ?"urn:samm:(io.catenax\.[^:]*):([\d.]+)#([^"]+)"',
                              jsonstring)
        childpathes = [self.basepath+"/"+c[0] + "/" + c[1] + "/gen/" + self.modelname(c[0]) + "-schema.json" for c
                       in children]
        return list(set(childpathes))


class CTXAnalyzeJson():
    def __init__(self, models, grpattrlist=[]):
        self.models = models
        self.elements = {"collections": {"objects": dict(),
                                         "lovs": dict(),
                                         "domains": dict()
                                         },
                         "lovs": dict(),
                         "domains": dict(),
                         "objects": dict(),
                         "synonyms": dict(),  # realobject:[synonyms]
                         "properties": dict(),
                         "groupattributes": dict(),
                         "arrays": dict()
                         }
        self.analyze(grpattrlist)
        return

    def _replacelocalref(self, refstruct):
        """ replace in the refstructure the local $ref by a global ref link """
        ref = refstruct["$ref"]
        if ref.startswith("#"):
            if ref not in self.translatelocals:
                # not yet found, do later
                return False
            refstruct["$ref"] = self.translatelocals[ref]
        return True

    def analyzarray(self, parentfull, objname, arrayobj):
        objref = UrnInfra(arrayobj)
        if "items" in arrayobj:
            items = arrayobj.get("items")
            if "$ref" in items:
                if not self._replacelocalref(refstruct=items):
                    # if replacement of  local ref "#/components/schema..." by real definition did not work, try later
                    self.postponeschema[objname] = arrayobj
                    return
                self.elements["arrays"][objref.full] = (items["$ref"], parentfull, arrayobj)
            elif "type" in items:
                self.elements["arrays"][objref.full] = (items.get("type"), parentfull, arrayobj)
            else:
                raise Exception("no ref or type in item)")
        else:
            raise Exception("no Items in array")

        self.translatelocals[f"#/components/schemas/{objref.name}"] = objref.full
        return

    def analyzeschema(self, parent: UrnInfra, objname: str,
                      obj: dict, grpattrlist: list):
        objref = UrnInfra(obj)
        if objref.direcversion == parent.direcversion:
            # Originally defined here
            if obj.get("type") in ("string", 'boolean', 'number'):
                target = "lovs" if "enum" in obj else "domains"
                self.elements["collections"][target][parent.full] = (None, parent)
                self.elements[target][objref.full] = (None, parent.full, obj)
                self.translatelocals[f"#/components/schemas/{objname}"] = objref.full
            elif obj.get("type") in ("object"):
                # if objectname is in list of objects to be treated as group attributes
                # handle it
                if len(grpattrlist) > 0 and re.search('|'.join(grpattrlist), objref.name):
                    # get detail of group attr and create collection + object
                    self.elements["collections"]["domains"][parent.full] = (None, parent)
                    self.elements["groupattributes"][objref.full] = (None, parent.full, obj)
                    self.translatelocals[f"#/components/schemas/{objname}"] = objref.full
                else:
                    # get detail and create collection + object
                    self.elements["collections"]["objects"][parent.full] = (None, parent)
                    self.elements["objects"][objref.full] = ('object', parent.full, obj)
                    self.translatelocals[f"#/components/schemas/{objname}"] = objref.full
                if "properties" in obj:
                    for propname, prop in obj.get("properties").items():
                        self.analyzeproperty(parentfull=objref.full, propname=propname, prop=prop)
                elif "allOf" in obj:
                    allof = obj.get("allOf")
                    if len(allof) == 1 and "$ref" in allof[0]:
                        # allOf with only one ref as substitute for $ref is ok as synonym
                        # mark object as synonym

                        self.elements["objects"][objref.full] = ('synonym', parent.full, obj)

                        if not self._replacelocalref(refstruct=obj.get("allOf")[0]):
                            raise Exception(f'replacement not found for allOf-ref {obj.get("allOf")[0]}')
                            # if replacement of  local ref "#/components/schema..." by real definition did not work, try later
                            # self.postponeschema[objname] = arrayobj
                        # mark is as a synonym for the referenced object
                        self.elements["synonyms"][objref.full] = allof[0]["$ref"]
                    else:
                        raise Exception(f'object with unhandled allOf {objref.full}')
                else:
                    raise Exception(f'object without properties {objref.full}')
            elif obj.get("type") == "array":
                self.analyzarray(parentfull=parent.full, objname=objname, arrayobj=obj)
            else:
                raise Exception(f"NOT YET ASSIGNED {obj.get('type')}: {objref.name}")
        else:
            # not defined in this file, add local translation
            if "urn:samm:org.eclipse.esmf" in objref.full and objref.full not in self.elements["domains"]:
                eclipsesubstitute = UrnInfra(objref.direcversion + "#eclipsesubstitute")
                self.elements["collections"]["domains"][eclipsesubstitute.full] = (None, eclipsesubstitute)
                self.elements["domains"][objref.full] = (None, eclipsesubstitute.full, obj)
                self.translatelocals[f"#/components/schemas/{objname}"] = objref.full
                logging.warning(f"eclipse not yet included {objref.full}")

            self.translatelocals[f"#/components/schemas/{objname}"] = objref.full
        return

    def analyzeproperty(self, parentfull, propname, prop):

        propref = UrnInfra(prop)
        ref = prop.get("$ref")
        self.elements["properties"].setdefault(parentfull, dict())
        if ref is None:
            # analyze type
            raise Exception("no ref in property")
        else:
            if not self._replacelocalref(refstruct=prop):
                #
                self.postponeproperty[propname] = prop
                return
            self.elements["properties"][parentfull][propref.name] = (propname, parentfull, prop)

        return

    def analyze(self, grpattrlist):
        for modelfilename, model in self.models.items():
            self.translatelocals = dict()  # store local references within this modelfile
            self.postponeschema = dict()
            self.postponeproperty = dict()
            if model.get("type") != "object":
                raise Exception(f'top level no object  {model.get("type")} : {modelfilename}')
            else:
                modelref = UrnInfra(model)
                schemas = model.get("components").get("schemas")
                properties = model.get("properties")
                self.elements["collections"]["objects"][modelref.full] = (None, modelref)
                self.elements["objects"][modelref.full] = (None, modelref.full, model)

                for objname, obj in schemas.items():
                    self.analyzeschema(parent=modelref, objname=objname,
                                       obj=obj, grpattrlist=grpattrlist)

                # loop for all later defined ref objects
                doneschemas = []
                while len(set(self.postponeschema).difference(set(doneschemas))) > 0:
                    for objname, obj in self.postponeschema.items():
                        if objname in doneschemas: continue
                        doneschemas.append(objname)
                        self.analyzeschema(parent=modelref, objname=objname,
                                           obj=obj, grpattrlist=grpattrlist)

                for propname, prop in properties.items():
                    self.analyzeproperty(parentfull=modelref.full, propname=propname, prop=prop)

                # loop for all later defined ref objects
                doneprops = []
                while len(set(self.postponeproperty).difference(set(doneprops))) > 0:
                    for propname, prop in self.postponeproperty.items():
                        if propname in doneprops: continue
                        doneprops.append(propname)
                        self.analyzeproperty(parentfull=modelref.full, propname=propname, prop=prop)
        return


class CTXGenerateDSJson:

    def __init__(self,
                 models,
                 analyzedelements: dict(),
                 datamodelname,
                 outfilebase,
                 intermediateoutputfile=None):
        self.models = models
        self.analyzedelements = analyzedelements
        self.datamodelname = datamodelname
        self.intermediateoutputfile = intermediateoutputfile
        self.outfilebase = nvl(outfilebase, datamodelname)
        self.referencemodelname = self.datamodelname + " referencemodel"
        self.domainmodelname = self.datamodelname + " domainmodel"
        self.datamodelfullname = self.datamodelname + " datamodel"
        self.defaultdmcollectionname = "BatteryPass"

        return

    def generatereference(self, jsonstruct, lovobject, lovname, collectionname):
        reference = dict()

        return reference

    def generaterefmodel(self):
        referencemodel = list()
        usedlovcollections = set([UrnInfra(p[1]).name for p in self.analyzedelements["lovs"].values()])
        for reflink, coll in self.analyzedelements["collections"]["lovs"].items():
            if coll[1].name not in usedlovcollections: continue
            collectionname = coll[1].name + "_coll"
            collectionref = coll[1].full
            referencemodel.append(Json2dataspot.fillstruct(elementtype="Collection",
                                                           label=collectionname,
                                                           title=collectionref,
                                                           description=None
                                                           ))
        lovcontrol = []
        for reflink, (_, parent, lov) in self.analyzedelements["lovs"].items():
            lovname = UrnInfra(lov).name
            if lovname in lovcontrol:
                logging.warning(f"LOV {lovname} {UrnInfra(lov).full} more than once.")
                continue
            lovcontrol.append(lovname)
            parentname = UrnInfra(parent).name + "_coll"
            lovjson = Json2dataspot.fillstruct("ReferenceObject",
                                               label=lovname,
                                               description=Json2dataspot.escapestr(lov.get("description")),
                                               title=UrnInfra(lov).full
                                               )
            Json2dataspot.optionalprop(lovjson, "inCollection", parentname)
            # Json2dataspot.optionalprop(lovjson, "subordinateOf", None)
            referencemodel.append(lovjson)
            for lovval in lov.get("enum"):
                valuejson = Json2dataspot.fillstruct(elementtype="ReferenceValue",
                                                     literalOf=lovname,
                                                     timeSeries=[{
                                                         "validFrom": -2208988800000,
                                                         "validTo": 32503593600000,
                                                         "code": Json2dataspot.escapestr(lovval)
                                                     }])
                referencemodel.append(valuejson)

        return referencemodel

    def generatedomainmodel(self):
        domainmodel = list()
        domainmodel.append(Json2dataspot.fillstruct(elementtype="Collection",
                                                    label="Basic datatypes",
                                                    title="json types without proper definition"
                                                    ))
        for name, basetype in [("string", "STRING")]:
            domainmodel.append(Json2dataspot.fillstruct(elementtype="DataDomain",
                                                        label=name,
                                                        title="Basic json type",
                                                        inCollection="Basic datatypes",
                                                        baseType=basetype
                                                        ))

        useddomcollections = set([UrnInfra(p[1]).name for p in self.analyzedelements["domains"].values()])
        for reflink, coll in self.analyzedelements["collections"]["domains"].items():
            if coll[1].name not in useddomcollections: continue
            collectionname = coll[1].name + "_coll"
            collectionref = coll[1].full
            domainmodel.append(Json2dataspot.fillstruct(elementtype="Collection",
                                                        label=collectionname,
                                                        title=collectionref,
                                                        description=None
                                                        ))
        domcontrol = []
        for reflink, (_, parent, dom) in self.analyzedelements["domains"].items():
            domname = UrnInfra(dom).name
            if domname in domcontrol:
                logging.warning(f"Domain {domname} {UrnInfra(dom).full} more than once.")
                continue
            domcontrol.append(domname)
            parentname = UrnInfra(parent).name + "_coll"
            domtype = dom.get("type")
            domainjson = Json2dataspot.fillstruct(elementtype="DataDomain",
                                                  label=domname,
                                                  title=UrnInfra(dom).full,
                                                  description=Json2dataspot.escapestr(dom.get("description")),
                                                  inCollection=parentname
                                                  )
            domainjson["minInclusive"] = None
            domainjson["maxInclusive"] = None
            domainjson["minExclusive"] = None
            domainjson["maxExclusive"] = None
            domainjson["integerDigits"] = None
            domainjson["fractionDigits"] = None
            if domtype == "boolean":
                domainjson["baseType"] = "BOOLEAN"
            elif domtype == "number":
                domainjson["baseType"] = "DECIMAL"
                Json2dataspot.optionalprop(destobject=domainjson, propname="minInclusive", value=dom.get("minimum"))
                Json2dataspot.optionalprop(destobject=domainjson, propname="maxInclusive", value=dom.get("maximum"))
            else:
                domainjson["baseType"] = "STRING"
                Json2dataspot.optionalprop(destobject=domainjson, propname="pattern", value=dom.get("pattern"))
                Json2dataspot.optionalprop(destobject=domainjson, propname="maxLength", value=dom.get("maxLength"))
                Json2dataspot.optionalprop(destobject=domainjson, propname="minLength", value=dom.get("minLength"))

            domainmodel.append(domainjson)
        for reflink, (_, parent, dom) in self.analyzedelements["groupattributes"].items():
            domname = UrnInfra(dom).name
            if domname in domcontrol:
                logging.warning(f"Domain {domname} {UrnInfra(dom).full} more than once.")
                continue
            domcontrol.append(domname)
            parentcoll = UrnInfra(parent).name + "_coll"
            domtype = dom.get("type")
            if domtype != "object":
                raise Exception(f'Groupdomain is not object {UrnInfra(dom).full}')
            domainjson = Json2dataspot.fillstruct(elementtype="DataDomain",
                                                  label=domname,
                                                  title=UrnInfra(dom).full,
                                                  description=Json2dataspot.escapestr(dom.get("description")),
                                                  inCollection=parentcoll
                                                  )
            domainmodel.append(domainjson)

            reqproperties = CTXInfra.alwayslist(dom.get("required"))
            idx = 0
            for propurn, (propname, propparenturn, prop) in self.analyzedelements["properties"][
                UrnInfra(dom).full].items():
                if "$ref" in prop:
                    # property references a schema, which I see as range (domain, second entity)
                    range = prop.get("$ref")

                    cardinality = "ONE"
                    if range in self.analyzedelements["lovs"]:
                        rangemodel = self.referencemodelname
                    elif range in self.analyzedelements["domains"]:
                        rangemodel = self.domainmodelname
                    elif range in self.analyzedelements["groupattributes"]:
                        rangemodel = self.domainmodelname
                    elif range in self.analyzedelements["arrays"]:
                        rangemodel = self.domainmodelname
                        cardinality = "MANY"
                        range = self.analyzedelements["arrays"][range][0]
                    else:
                        raise Exception(
                            f"no range type found {range}, probably object referenced in groupattribute {propurn}")
                    rangeref = UrnInfra(range)

                    self.generateattribute(jsonstruct=domainmodel,
                                           attrkey=propname,
                                           attribute=prop,
                                           objectname=f'{Json2dataspot.fullescapestr(parentcoll)}/{Json2dataspot.fullescapestr(UrnInfra(propparenturn).name)}',
                                           range=f'/{rangemodel}/{Json2dataspot.fullescapestr(rangeref.name)}',
                                           derived=False,
                                           mandatory=propname in reqproperties,
                                           cardinality=cardinality,
                                           favorite=idx < 3)
                    idx += 1
                else:
                    logging.error(f'datadomaimn prop has no ref: {prop}')

        return domainmodel

    def generateattribute(self, jsonstruct, attrkey, attribute, objectname, range=None,
                          derived=False, mandatory="OPTIONAL", cardinality="ONE",
                          favorite=False):
        self.generateelement(elementtype="DataAttribute",
                             jsonstruct=jsonstruct,
                             key=attrkey, elem=attribute,
                             objectname=objectname,
                             range=range,
                             derived=derived,
                             mandatory=mandatory, cardinality=cardinality,
                             favorite=favorite)
        return

    def generatecolumn(self,
                       jsonstruct, colkey, column, objectname, range=None,
                       derived=False, mandatory="OPTIONAL", cardinality="ONE",
                       favorite=False):
        self.generateelement(elementtype="UmlAttribute",
                             jsonstruct=jsonstruct,
                             key=colkey, elem=column,
                             objectname=objectname,
                             range=range,
                             derived=derived,
                             mandatory=mandatory, cardinality=cardinality,
                             favorite=favorite)
        return

    def generateelement(self, elementtype, jsonstruct, key, elem, objectname, range=None,
                        derived=False, mandatory="OPTIONAL", cardinality="ONE",
                        favorite=False):
        jsonstruct.append(Json2dataspot.fillstruct(elementtype=elementtype,
                                                   label=key,
                                                   title=elem.get("x-samm-aspect-model-urn"),
                                                   description=Json2dataspot.escapestr(
                                                       elem.get("description")),
                                                   hasDomain=objectname,
                                                   hasRange=range,
                                                   favorite=favorite,
                                                   derived=derived,
                                                   required="MANDATORY" if mandatory else "OPTIONAL",
                                                   cardinality=cardinality
                                                   ))
        return

    def generatecolumns(self, jsonstruct, columns, objectname):
        idx = 0
        for colkey, col in columns.items():
            if "$ref" in col:
                refobjname = col.get("$ref").rpartition("/")[2]
                column = self.schemas.get(refobjname)
                if column.get("type") == 'array':
                    # hier noch die Refs des Arrays suchen
                    print(f'Columns array: {colkey}')

                else:
                    idx += 1
                    # simple datatype, add reference to domain
                    self.generatecolumn(jsonstruct=jsonstruct, colkey=colkey,
                                        column=column,
                                        objectname=objectname,
                                        favorite=idx <= 3)
            else:
                print(f'Columns no ref: {colkey}')

        return

    def _defaultrelation(self, startobj, endobj, title, name, required, cardinality, description=None):
        rela = Json2dataspot.fillstruct(elementtype="UmlAssociation",
                                        title=title,
                                        hasDomain=startobj,
                                        name=name,
                                        hasRange=endobj,
                                        description=description,
                                        domainMultiplicity="1",
                                        rangeMultiplicity=f"{'1' if required else '0'}{'..*' if cardinality == 'MANY' else '' if required else '..1'}",
                                        required="MANDATORY" if required else "OPTIONAL",
                                        cardinality="MANY"
                                        )
        return rela

    def generaterelation(self,
                         jsonstruct,
                         rangeobj,
                         rangename,
                         attrname,
                         description,
                         rangeurn,
                         parentcoll,
                         parentkey,
                         required, cardinality
                         ):
        # logging.warning(f"relationship to object {key} {range}")
        endobjcoll = self.analyzedelements["collections"]["objects"] \
            [rangeobj[1]][1].name
        jsonstruct.append(self._defaultrelation(
            startobj=f'{Json2dataspot.fullescapestr(parentcoll)}/{Json2dataspot.fullescapestr(parentkey)}',
            endobj=f'{Json2dataspot.fullescapestr(endobjcoll + "_coll")}/{Json2dataspot.fullescapestr(rangename)}',
            title=rangeurn,
            name=attrname,
            description=description,
            required=required,
            cardinality=cardinality
        )
        )
        return

    def generateproperties(self,
                           jsonstruct,
                           myproperties,
                           parentcoll,
                           parentkey,
                           reqproperties
                           ):
        idx = 1
        for propurn, (propname, propparenturn, prop) in myproperties:
            if "$ref" in prop:
                # property references a schema, which I see as range (domain, second entity)
                rangeurn = prop.get("$ref")
                multivalue = False
                if rangeurn in self.analyzedelements["arrays"]:
                    multivalue = True

                    """ make it a multivalue element and get the new range (= the array-items -content)"""
                    rangeobj = self.analyzedelements["arrays"][rangeurn]
                    if "type" in rangeobj[2].get("items"):
                        # type is not reference but simple type, generate a multivalue column of the basic type
                        proptype = rangeobj[0]
                        if proptype != "string":
                            logging.error(f'datatpyes other than string in item {UrnInfra(rangeurn).name} {proptype}')
                        self.generatecolumn(jsonstruct=jsonstruct,
                                            colkey=propname,
                                            column=prop,
                                            objectname=f'{Json2dataspot.fullescapestr(parentcoll)}/{Json2dataspot.fullescapestr(UrnInfra(propparenturn).name)}',
                                            range=f'/{self.domainmodelname}/{proptype}',
                                            derived=False,
                                            mandatory=propname in reqproperties,
                                            cardinality="MANY",
                                            favorite=idx < 3)
                        idx += 1
                        # this property is finished
                        continue
                    elif "$ref" in rangeobj[2].get("items"):
                        # the destination is multiobject, generate a Many relation
                        desturn = rangeobj[0]
                        destobj = self.analyzedelements["objects"].get(desturn)
                        rangeurn, rangeobj = desturn, destobj
                        if destobj is None:
                            destobj = self.analyzedelements["domains"].get(desturn)
                            rangeurn, rangeobj = desturn, destobj
                        if destobj is None:
                            destobj = self.analyzedelements["lovs"].get(desturn)
                            rangeurn, rangeobj = desturn, destobj
                        if destobj is None:
                            destobj = self.analyzedelements["groupattributes"].get(desturn)
                            rangeurn, rangeobj = desturn, destobj
                        if destobj is None:
                            raise Exception(f'destination object not found {desturn}')
                    else:
                        logging.error(f"array with unknown type {rangeobj[2].get('items')}")

                rangename = UrnInfra(rangeurn).name
                if rangeurn in self.analyzedelements["objects"]:
                    # property references an object -> make relationship
                    if rangeurn in self.analyzedelements["synonyms"]:
                        rangeurn = self.analyzedelements["synonyms"][rangeurn]
                        rangename = UrnInfra(rangeurn).name
                    self.generaterelation(jsonstruct=jsonstruct,
                                          rangeobj=self.analyzedelements["objects"][rangeurn],
                                          rangename=Json2dataspot.fullescapestr(rangename),
                                          attrname=propname,
                                          rangeurn=rangeurn,
                                          parentcoll=parentcoll,
                                          parentkey=parentkey,
                                          description=prop.get("description"),
                                          required=propname in reqproperties,
                                          cardinality="ONE"
                                          )

                else:
                    if rangeurn in self.analyzedelements["lovs"]:
                        rangemodel = self.referencemodelname
                    elif rangeurn in self.analyzedelements["domains"]:
                        rangemodel = self.domainmodelname
                    elif rangeurn in self.analyzedelements["groupattributes"]:
                        rangemodel = self.domainmodelname
                    else:
                        raise Exception(f"no range type found {rangeurn}")
                    self.generatecolumn(jsonstruct=jsonstruct,
                                        colkey=propname,
                                        column=prop,
                                        objectname=f'{Json2dataspot.fullescapestr(parentcoll)}/{Json2dataspot.fullescapestr(UrnInfra(propparenturn).name)}',
                                        range=f'/{rangemodel}/{Json2dataspot.fullescapestr(UrnInfra(rangeurn).name)}',
                                        derived=False,
                                        mandatory=propname in reqproperties,
                                        cardinality="MANY" if multivalue else "ONE",
                                        favorite=idx < 3)
                    idx += 1
            else:
                proptype = prop.get("type")
                if proptype != "string":
                    logging.error(f'datatpyes other than string in item {UrnInfra(rangeurn).name} {proptype}')

                self.generatecolumn(jsonstruct=jsonstruct,
                                    colkey=propname,
                                    column=prop,
                                    objectname=f'{Json2dataspot.fullescapestr(parentcoll)}/{parentkey}',
                                    range=f'/{self.domainmodelname}/{proptype}',
                                    derived=False,
                                    mandatory=propname in reqproperties,
                                    cardinality="ONE",
                                    favorite=idx < 3)
                idx += 1
        return

    def generatedataboject(self, jsonstruct, dataobject, key, collectionname):
        dataref = UrnInfra(dataobject)
        jsonstruct.append(Json2dataspot.fillstruct(elementtype="UmlClass",
                                                   label=key,
                                                   title=dataref.full,
                                                   description=Json2dataspot.escapestr(
                                                       nvl(dataobject.get("description"))),
                                                   # examples=refobj.get("examples"),
                                                   inCollection=collectionname,
                                                   favorite=False))
        # 'urn:samm:io.BatteryPass.GeneralProductInformation:1.2.0#PostalAddress'
        if dataref.full in self.analyzedelements["properties"]:
            self.generateproperties(jsonstruct=jsonstruct,
                                    myproperties=self.analyzedelements["properties"][dataref.full].items(),
                                    parentcoll=collectionname,
                                    parentkey=key,
                                    reqproperties=CTXInfra.alwayslist(dataobject.get("required"))
                                    )
        else:
            if "allOf" in dataobject and len(dataobject["allOf"]) == 1 and "$ref" in dataobject["allOf"][0]:
                raise Exception("Object without properties and single allOf not yet handled")
            else:
                raise Exception("Object without properties and single allOfnot yet handled")
        return

    def generatedatamodel(self):
        datamodel = list()
        for reflink, coll in self.analyzedelements["collections"]["objects"].items():
            collectionname = coll[1].name + "_coll"
            collectionref = coll[1].full
            datamodel.append(Json2dataspot.fillstruct(elementtype="Collection",
                                                      label=collectionname,
                                                      title=collectionref,
                                                      description=None
                                                      ))
        for reflink, (entrytype, parent, dataobj) in self.analyzedelements["objects"].items():
            if entrytype == "synonym": continue
            dataobjname = UrnInfra(dataobj).name
            parentname = UrnInfra(parent).name + "_coll"
            self.generatedataboject(jsonstruct=datamodel,
                                    dataobject=dataobj, key=dataobjname, collectionname=parentname)

        return datamodel

    def generateDSmodels(self):
        outfilepath = self.outfilebase / (self.referencemodelname + ".json")
        with open(outfilepath, 'w') as outfile:
            json.dump(self.generaterefmodel(), outfile, indent=2)
            logging.info(f"Referencemodel generated into file {str(outfilepath)}")
            print(f"Referencemodel generated into file {str(outfilepath)}")

        outfilepath = self.outfilebase / (self.domainmodelname + ".json")
        with open(outfilepath, 'w') as outfile:
            json.dump(self.generatedomainmodel(), outfile, indent=2)
            logging.info(f"Domainmodel generated into file {str(outfilepath)}")
            print(f"Domainmodel generated into file {str(outfilepath)}")

        outfilepath = self.outfilebase / (self.datamodelfullname + ".json")
        with open(outfilepath, 'w') as outfile:
            json.dump(self.generatedatamodel(), outfile, indent=2)
            logging.info(f"Datamodel generated into file {str(outfilepath)}")
            print(f"Datamodel generated into file {str(outfilepath)}")

        return
