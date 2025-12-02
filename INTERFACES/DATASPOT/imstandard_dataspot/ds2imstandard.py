import json
from datetime import datetime
from pathlib import Path

from IM_STANDARD import JsonSchema, ElementId, nvl
from INTERFACES.DATASPOT.imstandard_dataspot.ds2standardbase import Dataspot2Jsonbase
from INTERFACES.DATASPOT.imstandard_dataspot.json2dataspot import Json2dataspot as j2d


class Dataspot2IMJsonschema(Dataspot2Jsonbase):
    """
    extract all elements from the dataspot json exports and create a standardjson-schema
    file
    The json-schem contains Entities (with attributes, keys), relationships, domains, busines rules
    and categories (to group entities and domains)
    """

    def __init__(self, indirec=None, **kwargs):
        super().__init__(standardjson=JsonSchema(),
                         indirec=indirec, **kwargs)
        return

    def generatebusinessmodel(self):
        self.generateentities(elementname="Entities",
                              elements=[elem for elem in self.entities.values()])
        self.generaterelations(elementname="Relations",
                               elements=[elem for elem in self.relationships.values()
                                         if elem.get("_type") == "Relationship"]
                               )
        self.generateattributes(elements=[elem for elem in self.attributes.values()
                                          if elem.get("_type") == "BusinessAttribute"])
        self.generateattributes(elements=[elem for elem in self.attributes.values()
                                          if elem.get("_type") == "DataAttribute"])
        self.generatebusinessrules(elementname="BusinessRules",
                                   elements=[elem for elem in self.businessrules.values()
                                             if elem.get("_type") == "BusinessConstraint"]
                                   )
        self.generatekeys()

        self.generatederivations()
        return

    # def lookupid(self, elemtype, name):
    #     elems = {e.get("name"): e.get("elementid") for e in self.model.get(elemtype)}
    #     return elems.get(name)
    #
    # def catgid(self, catgname):
    #     return self.lookupid(elemtype="Categories", name=catgname)
    #
    def generatekeys(self):
        """ get all keys from attributes and relations and fill the entities keys property
            assume attributes and relationships are already done"""
        for enti in self.standardjson.getelementinstances("Entities"):
            entiid = enti.get("elementid")
            keyelements = []
            for attr in enti.get('attributes', []):
                origattr = self.getelementbyid(elements=self.attributes,
                                               id=attr.get("elementid"))
                if origattr.get("identifying"):
                    keyelements.append(attr.get("elementid"))
            # find relationships with keys
            for rela in self.standardjson.getelementinstances("Relations"):
                if ((entiid == rela.get("fwd").get("entityid") and rela.get("fwd").get("cardinality") == "1")
                        or (entiid == rela.get("bwd").get("entityid") and rela.get("bwd").get("cardinality") == "1")):
                    origrela = self.getelementbyid(elements=self.relationships,
                                                   id=rela.get("elementid"))
                    # generated relations (subtypes) have no original
                    if origrela is not None and origrela.get("identifying"):
                        keyelements.append(rela.get("elementid"))
                    # TODO inherited keys (Mond erbt von Begleiter den Key)
                    # TODO different keys if relationships are in arc

            if len(keyelements) > 0:
                # standard keys are a list of keyelementlists
                enti["keys"] = self.standardjson.keysjson(keys=[keyelements])
        return

    def entityjson(self, element):
        additionalprops = self.additionalprops(elem=element,
                                               specialkeys=["subtypeOf"])
        # for dataspot mark entites as favorites
        additionalprops["favorite"]= element.get("favorite")
        jsonstruct = self.standardjson.entityjson(elementid=element.get("ID"),
                                                  name=self.mutlilangvalue(fieldname="label",
                                                                           value=self._deref(element.get("label")),
                                                                           addprops=additionalprops),
                                                  categoryid=self.findelementid(elems=self.categories,
                                                                                modelname=element.get("DSMODEL"),
                                                                                name=self._deref(
                                                                                    element.get("inCollection")),
                                                                                notnull=True
                                                                                ),
                                                  synonyms=element.get("synonyms"),
                                                  description=self.mutlilangvalue(fieldname="description",
                                                                                  value=self._deref(
                                                                                      element.get("description")),
                                                                                  addprops=additionalprops),
                                                  shortdescr=self.mutlilangvalue(fieldname="title",
                                                                                 value=self._deref(
                                                                                     element.get("title")),
                                                                                 addprops=additionalprops),
                                                  examples=element.get("examples"),
                                                  additionalProps=additionalprops
                                                  )
        # attributes and keys are added later
        return jsonstruct

    def generateentities(self, elementname, elements):
        for element in nvl(elements, []):
            self.standardjson.addelementinstance(name=elementname, val=self.entityjson(element))
        for element in nvl(elements, []):
            if element.get("subtypeOf") is not None:
                entityid1 = self.findelementid(elems=self.entities,
                                               modelname=element.get("DSMODEL"),
                                               name=element.get("subtypeOf"),
                                               notnull=True)
                self.standardjson.addelementinstance(name="Relations",
                                                     val=self.relationjsonbase(relationtype="SUBTYPE",
                                                                               entityid1=entityid1,
                                                                               entityid2=element.get("ID"),
                                                                               element={
                                                                                   "hasDomain": element.get(
                                                                                       "subtypeOf"),
                                                                                   "name": self.standardjson.multilangstring_is(),
                                                                                   "hasRange": element.get("label"),
                                                                                   "inverseName": self.standardjson.multilangstring_is(),
                                                                                   "domainMultiplicity": "1",
                                                                                   "rangeMultiplicity": "1",
                                                                                   "ARC-12": None,
                                                                                   "ARC-21": 0,
                                                                                   "ID": ElementId.nextid("RELA")
                                                                               }))

        return

    def relationtype(self, element):
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

    def generaterelations(self, elementname, elements):
        for element in elements:
            self.standardjson.addelementinstance(name=elementname,
                                                 val=self.relationjson(relationtype=self._relationtype(element),
                                                                       modelname=element.get("DSMODEL"),
                                                                       element=element)
                                                 )
        return

    def generate1attribute(self, element):
        parentid = self.getentityid(element.get("hasDomain"))
        if parentid is None:
            parentid = self.getdomainid(element.get("hasDomain"))
        domainname = element.get("hasRange")
        domainid = None if type(domainname) is not str else self.getdomainid(
            domaname=j2d.custom_split(domainname, "/")[-1])
        additionalprops = self.additionalprops(elem=element,
                                               specialkeys=["order", "cardinality", "required",
                                                            "temporal", "MULTILINGUAL", "identifying"])
        # "computation",
        jsonstruct = self.standardjson.attributejson(elementid=element.get("ID"),
                                                     name=self.mutlilangvalue(fieldname="label",
                                                                              value=self._deref(element.get("label")),
                                                                              addprops=additionalprops),
                                                     mandatory=element.get("required") == "MANDATORY",
                                                     domainid=domainid,
                                                     parentid=parentid,
                                                     displayseq=element.get("order"),
                                                     description=self.mutlilangvalue(fieldname="description",
                                                                                     value=self._deref(
                                                                                         element.get("description")),
                                                                                     addprops=additionalprops),
                                                     shortdescr=self.mutlilangvalue(fieldname="title",
                                                                                    value=self._deref(
                                                                                        element.get("title")),
                                                                                    addprops=additionalprops),
                                                     examples=element.get("examples"),
                                                     descriptive=element.get("favorite"),
                                                     historicised=element.get("temporal"),
                                                     repeated=True if element.get("cardinality") == "MANY" else None,
                                                     translated=element.get("MULTILINGUAL"),
                                                     additionalProps=additionalprops
                                                     )

        return jsonstruct

    def generateattributes(self, elements):
        for element in nvl(elements, []):
            self.standardjson.addelementinstance(name="Attributes",
                                                 val=self.generate1attribute(element=element))
        return

    def generatedomains(self):
        for element in self.domains.values():
            self.standardjson.addelementinstance(name="Domains",
                                                 val=self.generate1domain(doma=element))
        return

    def generate1domain(self, doma):
        jsonstruct = []
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
        jsonstruct.append(self.standardjson.domainjson(elementid=doma.get("ID"),
                                                       name=self.mutlilangvalue(fieldname="label",
                                                                                value=doma.get("label"),
                                                                                addprops=additionalprops),
                                                       categoryid=catgid,
                                                       **subtypeproperties
                                                       ))
        return jsonstruct
    def getadditionalprop(self,elem:dict,propname:str):
        addprops=elem.get("additionalProps",[])

        return
    def findqualielement(self,fullpath:str):
        frommodel, frompath, fromelement = self.namedreference2struct(fullpath)
        elements = self.standardjson.getanyelementsbyfield(name=fromelement,
                                                                field="name")
        retval = []
        for elem in elements:
            pass
        return None

    def generatederivations(self):
        """ read all derivations and add them to the element mentioned in the TO part of the derivation
        """
        for keyderiv, deriv, in self.derivations.items():
            sourceelement=self.findqualielement(fullpath=deriv.get("derivedFrom"))
            targetelement = self.findqualielement(fullpath=deriv.get("derivedTo"))
            if sourceelement is not None:
                newelem:dict()=self.standardjson.getbyid(sourceelement)
                #add drivation to this element

                newelem.setdefault("derivations",[])
                newelem["derivations"].append(self.standardjson.derivationjson
                                              (derivationtype=deriv.get("qualifier"),
                                               sourceelementname=deriv.get("derivedFrom")
                                              )
                                              )

        return

    def generatejson(self, modelname,
                     modelversion="0.0",
                     targetenv=None,
                     language="en",
                     languages=[]):
        now = datetime.now().replace(microsecond=0).isoformat()
        self.standardjson.setschemaelement(name="ModelInfo",
                                           val=self.standardjson.modelinfojson(
                                               modelname=modelname,
                                               modeltype="Information model",
                                               mainlanguage=language,
                                               languages=languages,
                                               dc=now,
                                               modelversion=modelversion,
                                               targetenvironment=targetenv,
                                               origintool=self.ORIGINTOOL))

        self.generatecategories(catgtype="DOMAIN")
        self.generatecategories(catgtype="ENTITY")
        self.generatedomains()
        self.generatebusinessmodel()

        return self.standardjson.jsonschemamodel


def exportIM2standard(inpath, outpath, modelname=None, modelversion='0.0',
                      targetenv=None,
                      language='en', languages=[]):
    indirec = Path(inpath)
    dsschema = Dataspot2IMJsonschema(indirec=indirec)
    jsonstruct = dsschema.generatejson(modelname=nvl(modelname, indirec.name),
                                       modelversion=modelversion,
                                       targetenv=targetenv,
                                       language=language,
                                       languages=languages)

    outfilepath = Path(outpath) / (indirec.name + ".json")
    with open(outfilepath, 'w') as outfile:
        json.dump(jsonstruct, outfile, indent=2)
        print('\n', outfilepath, " written")

    return jsonstruct


if __name__ == '__main__':
    import sys

    # mainpath="/Users/stb/Library/Mobile Documents/com~apple~CloudDocs/Arbeit/dataspot addons/access/chem-x"
    exportIM2standard(inpath=sys.argv[1],
                      outpath=sys.argv[2])
    # (inpath=mainpath+"/download",outpath= mainpath)
