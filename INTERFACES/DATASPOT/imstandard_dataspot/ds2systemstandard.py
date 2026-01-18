import json
from pathlib import Path

from IM_STANDARD import JsonSchema,nvl
from INTERFACES.DATASPOT.imstandard_dataspot.ds2standardbase import Dataspot2Jsonbase

class Dataspot2SYSTJsonschema(Dataspot2Jsonbase):
    """
    extract all elements from the dataspot json exports and create a standardjson-schema
    file
    The json-schem contains systems and categories (to group systems)
    """

    def __init__(self, indirec=None, **kwargs):
        super().__init__(standardjson=JsonSchema(),
                         indirec=indirec, **kwargs)
        return


    def systemjson(self, element):
        additionalprops = self.additionalprops(elem=element,
                                               specialkeys=["subsystemOf"])
        additionalprops["shortDescr"]=element.get("title")
        jsonstruct = self.standardjson.systemjson(elementid=element.get("ID"),
                                                  name=self.mutlilangvalue(fieldname="label",
                                                                           value=self._deref(element.get("label")),
                                                                           addprops=additionalprops),
                                                  categoryid=self.findelementid(elems=self.categories,
                                                                                modelname=element.get("DSMODEL"),
                                                                                name=self._deref(
                                                                                    element.get("inCollection")),
                                                                                fullname=True
                                                                                ),
                                                  parent=self.findelementid(elems=self.systems,
                                                                                modelname=element.get("DSMODEL"),
                                                                                name=self._deref(
                                                                                    element.get("subsystemOf"))),
                                                  synonyms=element.get("synonyms"),
                                                  description=self.mutlilangvalue(fieldname="description",
                                                                                  value=self._deref(
                                                                                      element.get("description")),
                                                                                  addprops=additionalprops),
                                                  additionalProps=additionalprops
                                                  )
        return jsonstruct

    def generatesystems(self, elementname, elements):
        for element in nvl(elements, []):
            self.standardjson.addelementinstance(name=elementname, val=self.systemjson(element))
        return

    def generatejson(self,
                     modelname=None,
                     modelversion='0.0',
                     targetenv=None,
                     language='en',
                     languages=['en']):
        self.standardjson.setschemaelement(name="ModelInfo",
                                           val=self.standardjson.modelinfojson(
                                           modelname=nvl(modelname,self.modelname),
                                           modeltype="System model",
                                           mainlanguage=language,
                                           languages=languages,
                                           modelversion=modelversion,
                                           targetenvironment=targetenv,
                                           origintool=self.ORIGINTOOL))
        self.generatecategories(catgtype="SYSTEM")
        self.generatesystems(elementname="Systems",
                             elements=[elem for elem in self.systems.values()])

        return self.standardjson.jsonschemamodel


def exportSYST2standard(inpath, outpath,
                      targetenv=None,
                      language='en', languages=[]):
    indirec = Path(inpath)
    systschema = Dataspot2SYSTJsonschema(indirec=indirec)
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
