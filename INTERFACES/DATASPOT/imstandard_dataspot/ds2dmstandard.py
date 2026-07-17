from INTERFACES.DATASPOT.imstandard_dataspot.ds2standardbase import Dataspot2Jsonbase
from .dslib import custom_split
from IM_STANDARD.myjsonschema import ElementId, JsonSchema,JsonElement


class Dataspot2DMJsonschema(Dataspot2Jsonbase):

    def __init__(self, indirec=None, **kwargs):
        super().__init__(standardjson=JsonSchema(),
                         indirec=indirec, **kwargs)

        return

    def getdatoid(self, datoname):
        return self.getelementid(elementtype="DataObjects", elementname=datoname)

    def getdomainid(self, domaname):
        return self.getelementid(elementtype="Domains", elementname=domaname)

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

    def generaterelations(self, elementname, elements):
        for element in elements:
            self.standardjson.addelementinstance(name=elementname,
                                                 val=self.relationjson(relationtype=self._relationtype(element),
                                                                 modelname=element.get("DSMODEL"),
                                                                 element=element)
                                                 )
        return

    def generatedataobjects(self, elementname, elements):
        for element in elements:
            self.standardjson.addelementinstance(name=elementname,
                                                 val=JsonElement().dataobjectjson(elementId=element.get("ID"),
                                                                                name=element.get("label"),
                                                                                columns=[],
                                                                                description=element.get("description"),
                                                                                #categoryid=self.categoryid(
                                                                                #    modeltype="DATAOBJECT",
                                                                                #    categoryname=self._deref(
                                                                                #        element.get("inCollection"))),
                                                                                additionalProps=self.additionalprops(
                                                                                    elem=element,
                                                                                    specialkeys=[])
                                                                                ))
        return

    def generatecolumns(self, elements):
        for subelem in elements:
            datoid = self.getdatoid(custom_split(subelem.get("hasDomain"), "/")[-1])
            domainname = subelem.get("hasRange")
            domainid = None if type(domainname) is not str else self.getdomainid(
                domaname=custom_split(domainname, "/")[-1])
            jsonstruct = JsonElement().dataattributejson(elementId=ElementId.nextid("COLU"),
                                                      dataobjectid=datoid,
                                                      name=subelem.get("label"),
                                                      domainid=domainid,
                                                      mandatory=subelem.get("required") == "MANDATORY",
                                                      techname=subelem.get("label").upper(),
                                                      description=subelem.get("description"),
                                                      tooltip=subelem.get("title"),
                                                      additionalProps={"SOURCE-ID": subelem.get("id")}
                                                      )
            self.standardjson.addelementinstance(name="DataAttributes",val=jsonstruct)
        return

    def fillrules(self, transformation):
        rules = []
        models = [{"modelName": self.jsonschemamodel["ModelInfo"].get("modelName"),
                   "sourcemodelurl": None}]
        for types in [elem for elem in self.modeltypeelements.values()]:
            sources = []
            for rule in [entry for entry in types if entry.get("_type") == "Rule" and
                                                     custom_split(entry.get("ruleOf"), "/")[
                                                         -1] == transformation.get(
                "label")]:
                sources.extend([custom_split(tf, "/")[1] for tf in rule.get("transformsFrom", [])])
                rules.append({"sequenceno": rule.get("label"),
                              "description": None,
                              "rule": rule.get("label")})
                # models.extend(list({tf.split("/")[0] for tf in rule.get("transformsTo", [])}))
            models.extend([{"modelName": s,
                            "sourcemodelurl": None} for s in list(set(sources))])
        return models, rules

    def filltransformations(self, elementname, elements):
        for element in elements:
            models, rules = self.fillrules(transformation=element)
            self.add_property(name=elementname,
                              val=self.mappingjson(
                                  name=element.get("label"),
                                  models=models,
                                  rules=rules,
                                  description=element.get("description"),
                                  additionalProps={"SOURCE-ID": element.get("id")}
                              )
                              )
        return

    def generatedatamodel(self,status:str):
        self.generatedataobjects(elementname="DataObjects",
                                 elements=[elem for elem in self.dsmodels.tables.values()])
        self.generatecolumns(elements=[elem for elem in self.columns.values()
                                       if elem.get("_type") == "UmlAttribute"])
        self.generaterelations(elementname="Relations",
                               elements=[elem for elem in self.relationships.values()
                                         if elem.get("_type") == "UmlAssociation"]
                               )
        self.generatebusinessrules(elementname="BusinessRules",
                                   elements=[elem for elem in self.businessrules.values()
                                             if (elem.get("_type") == "BusinessConstraint" and
                                                 elem.get("DSMODEL") == self.modelname)]
                                   )
        # self.generatekeys()
        return

    def generatejson(self, modelname, targetenv=None, **kwargs):
        status=kwargs.get("status")
        self.standardjson.setschemaelement(name="ModelInfo",
                                           val=JsonElement().modelinfojson(
                                           modelname=modelname,
                                           modeltype="Information Model",
                                           mainlanguage=kwargs.get("language", "en"),
                                           languages=kwargs.get("languages"),
                                           dc=None,
                                           modelversion=kwargs.get("modelVersion"),
                                           targetenvironment=targetenv,
                                           origintool=self.ORIGINTOOL))

        self.generatecategories(catgtype="DOMAIN",status=status)
        self.generatecategories(catgtype="DATAOBJECT",status=status)
        self.generatedomains(status=status)
        self.generatedatamodel(status=status)
        self.generatedatamodel(status=status)

        return self.standardjson


if __name__ == '__main__':
    pass

    # mainpath="/Users/stb/Library/Mobile Documents/com~apple~CloudDocs/Arbeit/dataspot addons/access/chem-x"
    # (inpath=mainpath+"/download",outpath= mainpath)
