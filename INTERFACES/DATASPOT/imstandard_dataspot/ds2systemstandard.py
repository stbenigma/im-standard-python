import json
from pathlib import Path

from IM_STANDARD import nvl,JsonElement, model2json
from .dselements import DataspotElements
from .ds2standardbase import Dataspot2Jsonbase,JsonSchema

class System2Json():
    """
    extract all elements from the dataspot json exports and create a standardjson-schema
    for systems
    The json-schema contains systems and categories (to group systems)
    Füllt das bestehende Schema
    """

    def __init__(self, dsmodels:DataspotElements,standardjson=None):
        self.dsmodels=dsmodels
        self.standardjson=standardjson if standardjson is not None else JsonSchema()
        return


    def systemjson(self, element):
        additionalprops = self.additionalprops(elem=element,
                                               specialkeys=["subsystemOf"])
        jsonstruct = JsonElement().systemjson(elementId=element.get("ID"),
                                                  name=self.mutlilangvalue(fieldname="label",
                                                                           value=self._deref(element.get("label")),
                                                                           addprops=additionalprops),
                                                    shortDescr=self.mutlilangvalue(fieldname="title",
                                                                           value=self._deref(element.get("title")),
                                                                           addprops=additionalprops),
                                              categoryId=self.findelementid(elems=self.dsmodels.categories,
                                                                                modelname=element.get("DSMODEL"),
                                                                                name=self._deref(
                                                                                    element.get("inCollection")),
                                                                                fullname=True
                                                                                ),
                                                  parent=self.findelementid(elems=self.dsmodels.systems,
                                                                                modelname=element.get("DSMODEL"),
                                                                                name=self._deref(
                                                                                    element.get("subsystemOf"))),
                                                  synonyms=element.get("synonyms"),
                                                  systemtype=element.get("stereotype"),
                                                  description=self.mutlilangvalue(fieldname="description",
                                                                                  value=self._deref(
                                                                                      element.get("description")),
                                                                                  addprops=additionalprops),
                                                  additionalProps=additionalprops
                                                  )
        return jsonstruct

    def generatesystems(self, elementname, elements,status=None):
        for element in nvl(elements, []):
            self.standardjson.addelementinstance(name=elementname, val=self.systemjson(element))

        "add dependencies to systems"
        for syst in self.standardjson.getelementinstances(elementname):
            dependencies=[[dep.get("dependsOn"),
                           dep.get("stereotype")] for dep in self.dsmodels.dependencies.values()
                            if dep.get("dependentOf") == self.standardjson.mlvalue(syst.getname()) \
                            and dep.get("DSMODEL") == syst.getadditionalprop("SOURCE-MODEL")]
            if len(dependencies) > 0:
                deps = {}
                for d in dependencies:
                    key = nvl(d[1], "dependson")
                    deps.setdefault(key, [])
                    deps[key].append(self.getelementid(elementtype="Systems",
                                             elementname=d[0])
                                     )
                syst.setproperty(propname="dependencies",val=deps)


        return

    def generatejson(self,
                     modelname=None,
                     modelversion='0.0',
                     targetenv=None,
                     language='en',
                     languages=['en'],
                     status=None):
        self.standardjson.setschemaelement(name="ModelInfo",
                                           val=JsonElement().modelinfojson(
                                           modelname=nvl(modelname,self.dsmodels.modelname),
                                           modeltype="System model",
                                           mainlanguage=language,
                                           languages=languages,
                                           modelversion=modelversion,
                                           targetEnvironment=targetenv,
                                           origintool=Dataspot2Jsonbase.ORIGINTOOL))
        self.generatecategories(catgtype="SYSTEM",status=status)
        self.generatederivations(status=status)
        self.generatetransformations(status=status)

        self.generatesystems(elementname="Systems",
                             elements=[elem for elem in self.dsmodels.systems.values()],
                     status=None)

        return model2json(self.standardjson.jsonschemamodel)


def exportSYST2standard(inpath, outpath,
                      targetenv=None,
                      language='en', languages=[]):
    indirec = Path(inpath)
    systschema = System2Json(indirec=indirec)
    jsonstruct = systschema.generatejson()

    outfilepath = Path(outpath) / (indirec.name + ".json")
    with open(outfilepath, 'w') as outfile:
        json.dump(jsonstruct, outfile, indent=2)
        print('\n', outfilepath, " written")

    return jsonstruct


if __name__ == '__main__':
    import sys

    # mainpath="/Users/stb/Library/Mobile Documents/com~apple~CloudDocs/Arbeit/dataspot addons/access/chem-x"
    exportSYST2standard(inpath=sys.argv[1],
                      outpath=sys.argv[2])
    # (inpath=mainpath+"/download",outpath= mainpath)
