import json
import logging
from pathlib import Path

from INTERFACES.DATASPOT import Json2dataspot

TYPETRANSLATE = {"<class 'int'>": "Integer",
                 "<class 'str'>": "String",
                 "<class 'bool'>": "Boolean",
                 "<class 'float'>": "Decimal",
                 "<class 'NoneType'>": "String",
                 "<class 'list'>": "List",
                 "<class 'dict'>": "Dict",
                 }


class Json2Dataset:
    idx = 0

    def __init__(self, modelpath, modelname, domainmodel):
        self.modelpath = modelpath
        self.modelname = modelname
        self.domainmodel = domainmodel
        self.collectionname = None
        self.topcollection = ""
        self._duplicates = {}

        return

    def _duplnames(self, name):
        if name in self._duplicates:
            self.idx += 1
            return name + (str(self.idx))
        return name

    def _unduplname(self, name, parentname):
        newname = self._duplnames(name=name)
        self._duplicates[newname] = (parentname, name)
        return newname

    def _translduplname(self, name, parentname):
        def _key(parent, child):
            return f"{parent}-{child}"

        transl = {_key(val[0], val[1]): key for key, val in self._duplicates.items()}
        if _key(parentname, name) in transl:
            return transl[_key(parentname, name)]
        else:
            return name

    @staticmethod
    def _examples(value) -> str:
        retval = None if value is None \
            else [value if type(value) in (int,float,bool) else str(value)[:100]]
        return retval

    @staticmethod
    def _datatyperef(domainmodel: str, basetype: str) -> str:
        retval = domainmodel.rstrip("/") + "/" + basetype
        return retval

    @staticmethod
    def _cardinality(valtype):
        if valtype == list:
            dstype = "MANY"
        elif valtype == dict:
            dstype = "ONE"
        else:
            raise Exception(f"jsonschema must be list or dict, not {valtype}")
        return dstype

    def _genelement(self, objname: str,
                    obj: dict,
                    dslevel: str,
                    parentname: str = None) -> list:
        """
        generate an element of a dataset.
        for dict and list, create a subset dslevel=MASTER or a new dataset dslevel=SUB

        :param objname: name of the obj I am currently in
        :param obj: json object of the element
        :param dslevel: The level I am in calling this function
                        SUB sub dataset
                        MASTER dataset
        @param: parentname: name of the parentelement in case of duplicate subdatasets naes
        :return: list of json-import entries generated in this function
        """
        dataset = []
        for key, val in obj.items():
            if type(val) == list:
                newval = val[0] if len(val) > 0 else None
                valcard = "MANY"
                logging.warning(f"only first list element used for {objname}.{key}")
            else:
                newval = val
                valcard = "ONE"
            valtype = TYPETRANSLATE[str(type(newval))]
            if valtype not in ("List", "Dict"):
                composed = self._datatyperef(domainmodel=self.domainmodel,
                                             basetype=valtype)

                dataset.append(Json2dataspot.fillstruct(elementtype="Composition",
                                                        label=key,
                                                        componentOf=(f"{parentname}/" if parentname else "") + objname,
                                                        composedOf=composed,
                                                        description=None,
                                                        card=valcard,
                                                        exmpls=self._examples(newval)
                                                        ))
            elif valtype == "Dict":
                """ create a new subset if master, or a dataset and reference it in here if  subste"""
                if dslevel == "MASTER":
                    # As a master I can create subsets
                    dataset.extend(self._gensubset(setname=key,
                                                   parentname=objname,
                                                   schema=newval,
                                                   card=valcard
                                                   )
                                   )
                else:
                    """ create new masterset and add an element to reference it"""
                    dataset.extend(self._genmasterset(setname=key,
                                                      schema=newval,
                                                      parentname=objname)
                                   )
                    composed = self._datatyperef(domainmodel=self.modelpath + "/" + self.collectionname,
                                                 basetype=self._translduplname(parentname=objname,
                                                                               name=key))
                    dataset.append(Json2dataspot.fillstruct(elementtype="Composition",
                                                            label=key,
                                                            componentOf=objname,
                                                            composedOf=composed,
                                                            description=None,
                                                            card="ONE",
                                                            exmpls=self._examples(newval)
                                                            ))
            elif valtype == "List":
                assert False, f"sollte nicht hier sein"
                """  create an element with the first element of the list, but provide a warning"""
                dataset.extend(self._genelement(objname=key,
                                                obj=None if len(val) == 0 else val[0],
                                                dslevel=dslevel
                                                )
                               )
                logging.warning(f"only first list element used for {objname}")

        return dataset

    def _gensubset(self,
                   setname: str,
                   parentname: str,
                   schema,
                   card: str) -> list:
        dataset = []
        assert type(schema) in [list, dict]

        # cardinality = self._cardinality(type(schema))
        if type(schema) == dict:
            pass
        elif type(schema) == list:
            pass

        # setname= self._unduplname(name=setname,parentname=parentname)
        dataset.append(Json2dataspot.fillstruct(elementtype="Dataset",
                                                label=setname,
                                                subsetOf=parentname,
                                                card=card)
                       )
        if type(schema) == dict:
            dataset.extend(self._genelement(objname=setname,
                                            obj=schema,
                                            dslevel="SUB",
                                            parentname=parentname)
                           )
        elif type(schema) == list:
            dataset.extend(self._genelement(objname=setname,
                                            obj=schema,
                                            dslevel="SUB")
                           )

        return dataset

    def _genmasterset(self, setname: str,
                      schema, parentname: str = None) -> list:
        dataset = []
        cardinality = self._cardinality(type(schema))

        # setname = self._duplnames(name=setname)
        # self._duplicates.append(setname)
        setname = self._unduplname(name=setname, parentname=parentname)
        dataset.append(Json2dataspot.fillstruct(elementtype="Dataset",
                                                label=setname,
                                                inCollection=self.modelpath + "/" +
                                                             self.collectionname,
                                                card=cardinality)
                       )

        if cardinality == "ONE":
            newmaster = schema
        else:
            """ take first element of list an fill and ignore the rest"""
            newmaster = schema[0] if len(schema) > 0 else {}
            if len(schema) > 1:
                logging.warning(f"only first list element used for {setname}")

        dataset.extend(self._genelement(objname=setname,
                                        obj=newmaster, dslevel="MASTER")
                       )

        return dataset

    def generatedatasetjson(self, jsonschema) -> list:
        """
        generates a dataset json for dataspot out of a json file with values

        :param jsonschema: json schema to be analyzed
        :return: a json ready to import into dataspot
        """
        datasetjson = list()
        self._duplicates = {}

        self.collectionname = self.modelname + "_coll"
        modelpathes = self.modelpath.split("/")
        self.topcollection = modelpathes[-1] if len(modelpathes) > 2 else None

        datasetjson.append(Json2dataspot.fillstruct(elementtype="Collection",
                                                    label=self.collectionname,
                                                    inCollection=self.topcollection,
                                                    description="Generated from json"
                                                    ))
        datasetjson.extend(self._genmasterset(setname=self.modelname,
                                              schema=jsonschema))

        return datasetjson


def jsondata2dataset(jsonschema,
                     datasetmodelpath: str,
                     modelname: str,
                     domainmodelpath: str):
    """
    converts jsonschema into a json  ready to be imported into dataspot as a dataset.

    :param jsonschema: jsonschema  containing data-json to be conververted
    :param datasetmodelpath: dataspot modelpath for the collection receiving the new dataset
    :param modelname: name of the model. will be the collection containing all sub datasets
    :param domainmodelpath: dataspot modelpath for the collection containing the standard datatypes
                            (Integer, Decimal, Boolean, String, Text)
    :return: json ready to be imported into dataspot as a dataset
    """
    json2ds = Json2Dataset(modelpath=datasetmodelpath,
                           modelname=modelname,
                           domainmodel=domainmodelpath
                           )
    outjson = json2ds.generatedatasetjson(jsonschema=jsonschema)
    return outjson


def jsondata2dataset_files(infilepath: str,
                           datasetmodelpath: str,
                           modelname: str,
                           domainmodelpath: str,
                           outfilepath: str=None):
    """
    loads a data-jsonfile and converts it into a jsonfile ready to be imported into dataspot as a dataset.

    :param infilepath: jsonfile containing data-json to be conververted
    :param outfilepath: jsonfile ready to be imported into dataspot as a dataset.
                        Default: infilepath with -dataset added to the stem
    :param datasetmodelpath: dataspot modelpath for the collection receiving the new dataset
    :param modelname: name of the model. will be the collection containing all sub datasets
    :param domainmodelpath: dataspot modelpath for the collection containing the standard datatypes
                            (Integer, Decimal, Boolean, String, Text)
    :return: file written and message printed
    """
    with open(infilepath, 'r', encoding='utf-8') as infile:
        model = json.load(infile)

    outjson = jsondata2dataset(jsonschema=model,
                               datasetmodelpath=datasetmodelpath,
                               modelname=modelname,
                               domainmodelpath=domainmodelpath
                               )

    outfilepath = Path(outfilepath) if outfilepath is not None \
        else Path(infilepath).with_stem(Path(infilepath).stem + "-dataset")
    with open(outfilepath, "w", encoding='utf-8') as outfile:
        json.dump(outjson, outfile, indent=2)
        print(f"dataspot import json for dataset written to {str(outfilepath)}")
    return
