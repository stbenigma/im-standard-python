from IM_STANDARD import JsonSchema, nvl
from INTERFACES.DATASPOT import Json2dataspot

TYPETRANSLATE={"Number":"Decimal",
               "Text":"Text",
               "String":"String",
               "Boolean":"Boolean",
               "Date":"Date",
               "DateTime":"Timestamp",
               "Time":"Time of day"
               }
def _sourcedef(props: dict) -> str:
    retval = None if (props is None or len(props)==0)\
                 else ("\n\nadditional Properties:\n" + "\n" + \
             "\n".join([f"- {key}: {val}" for key, val in props.items()]))
    return retval


def _examples(examples: list) -> str:
    retval = None if examples is None or all(examples)==None \
        else [(expl if type(expl) in (int,float,bool) else str(expl)[:100]) for expl in examples if expl is not None]
    return retval

def _datatyperef(domainmodel:str,basetype:str)->str:
    retval = domainmodel.rstrip("/")+"/"+TYPETRANSLATE[basetype]
    return retval

def generatedatasetjson(jsonschema: JsonSchema,
                        domainmodel:str) -> list:
    """

    :param jsonschema: read jsonschema from excel
    :param domainmodel: path of the domain model in my target dataspot repository
    :return: a json ready to import into dataspot
    """
    datasetjson = []
    collectionname = "Excels"
    datasetjson.append(Json2dataspot.fillstruct(elementtype="Collection",
                                                label=collectionname,
                                                description="Generated from Excel"
                                                ))

    modelinfo = jsonschema.jsonschemamodel.get("ModelInfo")
    datasetjson.append(Json2dataspot.fillstruct(elementtype="Dataset",
                                                label=jsonschema.modelname,
                                                inCollection=collectionname,
                                                description=nvl(modelinfo.get("description")) + \
                                                            nvl(_sourcedef(modelinfo.get("additionalProps")))
                                                ))
    for datobj in jsonschema.jsonschemamodel.get("DataObjects"):
        objname = datobj.get("name")
        objid = datobj.get("elementid")
        datasetjson.append(Json2dataspot.fillstruct(elementtype="Dataset",
                                                    label=objname,
                                                    subsetOf=jsonschema.modelname,
                                                    description=nvl(datobj.get("description")) + \
                                                                nvl(_sourcedef(datobj.get("additionalProps"))),
                                                    mand=datobj.get("mandatory"),
                                                    exmpls=nvl(_examples(datobj.get("examples")))
                                                    ))
        for dataattr in jsonschema.jsonschemamodel.get("DataAttributes"):
            if dataattr.get("dataobjectid")!= objid: continue
            datasetjson.append(Json2dataspot.fillstruct(elementtype="Composition",
                                                        label=dataattr.get("name"),
                                                        componentOf=objname,
                                                        composedOf=_datatyperef(domainmodel=domainmodel,
                                                                                basetype=dataattr.get("basedatatype")),
                                                        description=nvl(dataattr.get("description")) + \
                                                                    nvl(_sourcedef(dataattr.get("additionalProps"))),
                                                        mand=dataattr.get("mandatory"),
                                                        exmpls=nvl(_examples(dataattr.get("examples")))
                                                        ))

    return datasetjson

