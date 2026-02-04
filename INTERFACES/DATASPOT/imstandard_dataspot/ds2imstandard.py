import json
import logging
from datetime import datetime
from pathlib import Path

from IM_STANDARD import JsonSchema, ElementId, nvl, JsonElement, model2json
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
        self.generatemappings()
        self.generatetransformations()
        return

    def generatekeys(self):
        """ get all keys from attributes and relations and fill the entities keys property
            assume attributes and relationships are already done"""
        for enti in self.standardjson.getelementinstances("Entities"):
            entiid = enti.getid()
            keyelements = []
            for attr in self.standardjson.getelementinstances("Attributes"):
                if attr["parentid"] == entiid:
                    origattr = self.getelementbyid(elements=self.attributes,
                                                   id=attr.getid())
                    if origattr.get("identifying"):
                        keyelements.append(attr.getid())
            # find relationships with keys
            for rela in self.standardjson.getelementinstances("Relations"):
                if ((entiid == rela["fwd"].get("entityid") and rela["fwd"].get("cardinality") == "1")
                        or (entiid == rela["bwd"].get("entityid") and rela["bwd"].get("cardinality") == "1")):
                    origrela = self.getelementbyid(elements=self.relationships,
                                                   id=rela.getid())
                    # generated relations (subtypes) have no original
                    if origrela is not None and origrela.get("identifying"):
                        keyelements.append(rela.getid())
                    # TODO inherited keys (Mond erbt von Begleiter den Key)
                    # TODO different keys if relationships are in arc

            if len(keyelements) > 0:
                # standard keys are a list of keyelementlists
                enti.setproperty("keys", [keyelements])
        return

    def entityjson(self, element):
        additionalprops = self.additionalprops(elem=element,
                                               specialkeys=["subtypeOf"])
        # for dataspot mark entites as favorites
        additionalprops["favorite"] = element.get("favorite")
        elementi = JsonElement().entityjson(elementid=element.get("ID"),
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
        return elementi

    def generateentities(self, elementname, elements):
        for element in nvl(elements, []):
            self.standardjson.addelementinstance(name=elementname,
                                                 val=self.entityjson(element))
        for element in nvl(elements, []):
            if element.get("subtypeOf") is not None:
                entityid1 = self.findelementid(elems=self.entities,
                                               modelname=element.get("DSMODEL"),
                                               name=element.get("subtypeOf"),
                                               notnull=True)
                self.standardjson.addelementinstance \
                    (name="Relations",
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
        elemattr = JsonElement().attributejson(elementid=element.get("ID"),
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

        return elemattr

    def generateattributes(self, elements):
        for element in nvl(elements, []):
            self.standardjson.addelementinstance(name="Attributes",
                                                 val=self.generate1attribute(element=element))
        return

    def findqualielement(self, fullpath: str,
                         elemtype: str = None):
        frommodel, frompath, fromelement = self.namedreference2struct(fullpath)
        elements = self.standardjson.getanyelementsbyfield(name=fromelement,
                                                           field="name")
        retval = []
        for elem in elements:
            elemmodel, elempath, elemname = self.namedreference2struct(
                namedref=self.standardjson.getfullpath(elem=elem))
            # assert len(frompath) <= 1, "mehrfach path muss noch gemacht werden"
            if (frommodel == elemmodel) and \
                    ((len(frompath) <= len(
                        elempath)) and  # both paths are equal from the end to the beginning of the frompath
                     ((frompath == []) or (frompath[-len(frompath):] == elempath[-len(frompath):]))) and \
                    (elemtype is None or
                     (elemtype == elem.elemtype)):
                retval.append(elem)
        if len(retval) == 1:
            return retval[0]
        else:
            return None

    def generatederivations(self):
        """ read all derivations and add them to the derivations of the model, if the target is in this model
        """
        for keyderiv, deriv, in self.derivations.items():
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

    def generatetransformations(self):
        """ read all transformations and add them to the element
        """
        for trakey, transf, in self.transformations.items():
            transpath = transf.get("transformationOf") + "/" + transf.get("label")

            additionalprops = self.additionalprops(elem=transf,
                                                   specialkeys=["transformationOf"])
            rules = [r for r in self.rules.values() if r.get("ruleOf") == transpath]
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
                                                     (targetelements=targetelements,
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

    def valuemappings(self, rules):
        retval = [[rule.get("translatesFrom"), rule.get("translatesTo")] for rule in rules]
        return retval

    def generatemappings(self):
        """ read all mappings and add them to the element
        """
        for mapkey, mapping, in self.mappings.items():
            sourcedomain = self.findqualielement(
                fullpath=self.addmodeltonamedreference(namedref=mapping.get("mapsFrom"),
                                                       modelname=mapping.get("DSMODEL")),
                elemtype="Domain")
            targetdomain = self.findqualielement(fullpath=self.addmodeltonamedreference(namedref=mapping.get("mapsTo"),
                                                                                        modelname=mapping.get(
                                                                                            "DSMODEL")),
                                                 elemtype="Domain")
            if targetdomain is None:
                # target not found, is not part of the current model
                continue

            # add derivation to found element
            if sourcedomain is None:
                sourceelementid = mapping.get("derivedFrom")
            else:
                sourceelementid = sourcedomain.getid()

            additionalprops = self.additionalprops(elem=mapping,
                                                   specialkeys=["mapsTo",
                                                                "mapsFrom"
                                                                ])

            self.standardjson.addelementinstance(name="Mappings",
                                                 val=JsonElement().mappingjson
                                                 (derivationtype=mapping.get("qualifier"),
                                                  targetdomain=targetdomain.getid(),
                                                  sourcedomain=sourceelementid,
                                                  valuemappings=self.valuemappings
                                                  (rules=[r for r in self.translations.values()
                                                          if r.get('translationIn') == mapping.get("label")]),
                                                  additionalProps=additionalprops
                                                  )
                                                 )

        return

    def generatejson(self, modelname,
                     modelversion="0.0",
                     targetenv=None,
                     language="en",
                     languages=[]):
        now = datetime.now().replace(microsecond=0).isoformat()
        modeltype = "Information model"

        additionalprops = {"FULLPATH": f"{nvl(targetenv,self.tenant.get('name',''))}:{modeltype}:{modelname}",
                           "SOURCE-SERVER": self.tenant.get('server'),  # "https://partner.dataspot.io/rest/"
                           "SOURCE-DB": self.tenant.get('db'),  # foryouandyourcustomers
                           "SOURCE-TENANT": self.tenant.get("name"),  # Sandbox"
                           "SOURCE-HREF": f"{self.tenant.get('server')}{self.tenant.get('db')}/schemes/a54fed8f-8fed-39a0-a192-92310c56cfd6"
                           }
        self.standardjson.setschemaelement(name="ModelInfo",
                                           val=JsonElement().modelinfojson(
                                               modelname=modelname,
                                               modeltype=modeltype,
                                               mainlanguage=language,
                                               languages=languages,
                                               dc=now,
                                               modelversion=modelversion,
                                               targetenvironment=targetenv,
                                               origintool=self.ORIGINTOOL,
                                               originuri=None,
                                               additionalProps=additionalprops
                                           )
                                           )

        self.generatecategories(catgtype="DOMAIN")
        self.generatecategories(catgtype="ENTITY")
        self.generatedomains()
        self.generatebusinessmodel()

        return model2json(self.standardjson.jsonschemamodel)


def exportIM2standard(inpath, outpath, modelname=None, modelversion='0.0',
                      targetenv=None,
                      language='en', languages=[]):
    indirec = Path(inpath)
    dsschema = Dataspot2IMJsonschema(indirec=indirec, tenant={"name": targetenv,
                                                              "id": None,
                                                              "uri": None,
                                                              "db": "foryouandyourcustomers",
                                                              "server": "https://partner.dataspot.io/rest/"}
                                     )
    jsonstruct = dsschema.generatejson(modelname=nvl(modelname, indirec.name),
                                       modelversion=modelversion,
                                       targetenv=dsschema.tenant.get("name"),
                                       language=language,
                                       languages=languages)

    outfilepath = Path(outpath)
    with open(outfilepath, 'w') as outfile:
        json.dump(jsonstruct, outfile, indent=2)

    return jsonstruct


if __name__ == '__main__':
    import sys

    # mainpath="/Users/stb/Library/Mobile Documents/com~apple~CloudDocs/Arbeit/dataspot addons/access/chem-x"
    exportIM2standard(inpath=sys.argv[1],
                      outpath=sys.argv[2])
    # (inpath=mainpath+"/download",outpath= mainpath)
