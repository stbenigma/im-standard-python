import json
from datetime import datetime
from pathlib import Path

from IM_STANDARD import JsonSchema, ElementId, nvl, JsonElement, model2json
from INTERFACES.DATASPOT.imstandard_dataspot.ds2standardbase import Dataspot2Jsonbase,DataspotElements
from .dslib import custom_split


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

    def generatebusinessmodel(self,status=None):
        self.generateentities(elementname="Entities",
                              elements=[elem for elem in self.dsmodels.entities.values()
                                        if DataspotElements.checkstatus(elem,status)])
        self.generaterelations(elementname="Relations",
                               elements=[elem for elem in self.dsmodels.relationships.values()
                                         if elem.get("_type") == "Relationship" and
                                            self.dsmodels.checkstatus(elem, status)
                                         ]
                               )
        self.generateattributes(elements=[elem for elem in self.dsmodels.attributes.values()
                                          if elem.get("_type") == "BusinessAttribute" and
                                            self.dsmodels.checkstatus(elem, status)
                                          ])
        self.generateattributes(elements=[elem for elem in self.dsmodels.attributes.values()
                                          if elem.get("_type") == "DataAttribute" and
                                            self.dsmodels.checkstatus(elem, status)
                                          ])
        self.generatebusinessrules(elementname="BusinessRules",
                                   elements=[elem for elem in self.dsmodels.businessrules.values()
                                             if elem.get("_type") == "BusinessConstraint" and
                                            self.dsmodels.checkstatus(elem, status)
                                             ]
                                   )
        self.generatekeys()

        return

    def generatekeys(self):
        """ get all keys from attributes and relations and fill the entities keys property
            assume attributes and relationships are already done"""
        for enti in self.standardjson.getelementinstances("Entities"):
            entiid = enti.getid()
            keyelements = []
            for attr in self.standardjson.getelementinstances("Attributes"):
                if attr["parentid"] == entiid:
                    origattr = self.getelementbyid(elements=self.dsmodels.attributes,
                                                   elemid=attr.getid())
                    if origattr.get("identifying"):
                        keyelements.append(attr.getid())
            # find relationships with keys
            for rela in self.standardjson.getelementinstances("Relations"):
                if ((entiid == rela["fwd"].get("entityid") and rela["fwd"].get("cardinality") == "1")
                        or (entiid == rela["bwd"].get("entityid") and rela["bwd"].get("cardinality") == "1")):
                    origrela = self.getelementbyid(elements=self.dsmodels.relationships,
                                                   elemid=rela.getid())
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
        additionalprops["SOURCE-HREF"] = self.dsmodels.sourcehref(element)
        elementi = JsonElement().entityjson(elementid=element.get("ID"),
                                            name=self.mutlilangvalue(fieldname="label",
                                                                     value=self._deref(element.get("label")),
                                                                     addprops=additionalprops),
                                            categoryid=self.findelementid(elems=self.dsmodels.categories,
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
                entityid1 = self.findelementid(elems=self.dsmodels.entities,
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
                                                   "ID": ElementId.nextid("RELA"),
                                                   "href":  self.dsmodels.sourcehref(element)

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
            domaname=custom_split(domainname, "/")[-1])
        additionalprops = self.additionalprops(elem=element,
                                               specialkeys=["order", "cardinality", "required",
                                                            "temporal", "MULTILINGUAL", "identifying"])
        # "computation",
        additionalprops["SOURCE-HREF"] = self.dsmodels.sourcehref(element)
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

    def _diagusage(self, elems):
        usages = []
        for elem in elems:
            sourcepath = self.addmodeltonamedreference(namedref=elem.get("usageOf"),
                                                       modelname=elem.get("DSMODEL"))

            sourceelement = self.findqualielement(fullpath=sourcepath)
            if sourceelement is None:
                sourceelementid = sourcepath
            else:
                sourceelementid = sourceelement.getid()
            usages.append(sourceelementid)
        return usages

    def generatediagrams(self,status=None):
        """ read all transformations and add them to the element
        """
        for diagkey, diag, in self.dsmodels.diagrams.items():
            if not self.dsmodels.checkstatus(diag, status): continue
            additionalprops = self.additionalprops(elem=diag,
                                                   specialkeys=[])
            elems = [r for r in self.dsmodels.diagelements.values() if r.get("usedBy") == diag.get("label")]
            self.standardjson.addelementinstance(name="Diagrams",
                                                 val=JsonElement().diagramjson(elementid=diag.get("ID"),
                                                                               name=diag.get("label"),
                                                                               # position=dict()=,
                                                                               # size=,
                                                                               elements=self._diagusage(elems),
                                                                               additionalProps=additionalprops))
        return

    def valuemappings(self, rules):
        retval = [[rule.get("translatesFrom"), rule.get("translatesTo")] for rule in rules]
        return retval

    def generatemappings(self,status=None):
        """ read all mappings and add them to the element
        """
        for mapkey, mapping, in self.dsmodels.mappings.items():
            if not self.dsmodels.checkstatus(mapping, status): continue
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
                                                  (rules=[r for r in self.dsmodels.translations.values()
                                                          if r.get('translationIn') == mapping.get("label")]),
                                                  additionalProps=additionalprops
                                                  )
                                                 )

        return

    def generatejson(self, modelname,
                     modelversion="0.0",
                     targetenv=None,
                     language="en",
                     languages=[],
                     status=None):
        self.standardjson = JsonSchema()
        assert status in ("PUBL", "GTOP", "ALL", None), "status  must be PUBL, GTOP or ALL"

        now = datetime.now().replace(microsecond=0).isoformat()
        modeltype = "Information model"

        additionalprops = {"FULLPATH": f"{nvl(targetenv, self.dsmodels.tenant.get('name', ''))}:{modeltype}:{modelname}",
                           "SOURCE-SERVER": self.dsmodels.tenant.get('server'),  # "https://partner.dataspot.io/rest/"
                           "SOURCE-TENANT": self.dsmodels.tenant.get("name"),  # Sandbox"
                           "SOURCE-HREF": f"{self.dsmodels.tenant.get('server')}{self.dsmodels.tenant.get('uri')}"
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

        self.generatecategories(catgtype="DOMAIN",status=status)
        self.generatecategories(catgtype="ENTITY",status=status)
        self.generatedomains(status=status)
        self.generatebusinessmodel(status=status)
        self.generatederivations(status=status)
        self.generatemappings(status=status)
        self.generatetransformations(status=status)
        self.generatediagrams(status=status)
        self.generatediagrams(status=status)

        return model2json(self.standardjson.jsonschemamodel)


def exportIM2standard(inpath, outpath, modelname=None, modelversion='0.0',
                      targetenv=None,
                      language='en', languages=[],
                      server="https://myserver.io",
                      status=None):
    indirec = Path(inpath)
    dsschema = Dataspot2IMJsonschema(indirec=indirec, tenant={"name": targetenv,
                                                              "id": None,
                                                              "uri": None,
                                                              "db": None,
                                                              "server": server}
                                     )
    jsonstruct = dsschema.generatejson(modelname=nvl(modelname, indirec.name),
                                       modelversion=modelversion,
                                       targetenv=nvl(targetenv, dsschema.dsmodels.tenant.get("name")),
                                       language=language,
                                       languages=languages,
                                     status=status)

    outfilepath = Path(outpath)
    if outfilepath.is_dir():
        # add filename
        outfilepath = outfilepath / (
                    jsonstruct.get("ModelInfo", dict()).get("modelname", "whatever") + "-standard.json")
    with open(outfilepath, 'w') as outfile:
        json.dump(jsonstruct, outfile, indent=2)

    return jsonstruct


if __name__ == '__main__':
    import sys

    # mainpath="/Users/stb/Library/Mobile Documents/com~apple~CloudDocs/Arbeit/dataspot addons/access/chem-x"
    exportIM2standard(inpath=sys.argv[1],
                      outpath=sys.argv[2])
    # (inpath=mainpath+"/download",outpath= mainpath)
