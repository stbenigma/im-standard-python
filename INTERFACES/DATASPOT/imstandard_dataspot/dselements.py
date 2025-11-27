import json
import logging
from pathlib import Path


from INTERFACES.DATASPOT.imstandard_dataspot.json2dataspot import Json2dataspot as j2d
from IM_STANDARD.myjsonschema import ElementId
from IM_STANDARD import nvl


class DataspotElements():
    def __init__(self, indirec=None,**kwargs):
        # models
        # self._dsmodels = dict()

        # all elements grouped by modeltype
        #self._modeltypeelements = dict()
        self.modelcategories = dict()

        self.modelname=kwargs.get("modelname")

        # elements from dataspot according to their type
        self.categories = dict()
        self.systems = dict()
        self.entities = dict()
        self.attributes = dict()
        self.domains = dict()
        self.LOVvalues = dict()
        self.tables = dict()
        self.columns = dict()
        self.relationships = dict()
        self.transformations = dict()
        self.rules = dict()
        self.deployments = dict()
        self.dependencies = dict()
        self.derivations = dict()
        self.diagrams = dict()
        self.diagelements = dict()
        self.businessrules = dict()

        if indirec is not None:
            self.readmodels(indirec)
        return

    def modeltype(self, struct):
        keyset = set([elem.get("_type") for elem in struct])
        if keyset.intersection({"Collection",
                                "BusinessObject"}) == {"Collection",
                                                       "BusinessObject"}:
            return "BUSINESSMODEL"
        elif keyset.intersection({"Collection",
                                  "ReferenceObject"}) == {"Collection",
                                                          "ReferenceObject"}:
            return "REFERENCE"
        elif keyset.intersection({"Collection",
                                  "DataDomain"}) == {"Collection",
                                                     "DataDomain"}:
            return "DATATYPE"
        elif keyset.intersection({"Collection",
                                  "UmlClass"}) \
                == {"Collection",
                    "UmlClass"}:
            return "DATAMODEL"
        elif keyset.intersection({"Collection",
                                  "System"}) \
                == {"Collection",
                    "System"}:
            return "SYSTEMS"
        elif keyset.intersection({"Collection",
                                  "Project"}) \
                == {"Collection",
                    "Project"}:
            return "PROJECT"
        else:
            print(set([elem.get("_type") for elem in struct]))
            return None

    def entryid(self, entry, name):
        model = entry.get('DSMODEL')
        parent = entry.get('PARENT')
        return f"""{model}/{"" if parent is None else (parent + '/')}{nvl(name)}"""

    def _categorytype(self, modeltype):
        if modeltype == "BUSINESSMODEL":
            return "ENTITY"
        elif modeltype in ("DATATYPE", "REFERENCE"):
            return "DOMAIN"
        elif modeltype in ("DATAMODEL",):
            return "DATAOBJECT"
        elif modeltype in ("SYSTEMS",):
            return "SYSTEM"
        elif modeltype in ("PROJECT",):
            return "PROJECT"
        else:
            logging.warning(f"{modeltype} not known")

    def fillids(self, modelname, struct):
        """create spod id for every element and add element by natural name to its proper list.
           the name of the file is used as the model name in which the element was found
        """
        modeltype = self.modeltype(struct)
        if modeltype is None:
            return
        for entry in struct:
            entry["DSMODEL"] = modelname
            name = entry.get('label')
            if entry.get("_type") == "Collection":
                entry["ID"] = ElementId.nextid("CATG")
                entry["TYPE"] = self._categorytype(modeltype)
                entry["PARENT"] = entry.get('inCollection')
                self.categories[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "BusinessObject":
                entry["ID"] = ElementId.nextid("ENTI")
                entry["PARENT"] = entry.get('inCollection')
                self.entities[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "BusinessAttribute":
                entry["ID"] = ElementId.nextid("ATTR")
                entry["PARENT"] = entry.get('hasDomain')
                self.attributes[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "Dependency":
                entry["PARENT"] = nvl(entry.get('dependentOf'))
                entry["PARENT2"] = nvl(entry.get('dependsOn'))
                self.dependencies[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "System":
                entry["ID"] = ElementId.nextid("SYST")
                entry["PARENT"] = nvl(entry.get('subsystemOf'), entry.get('inCollection'))
                self.systems[self.entryid(entry=entry, name=name)] = entry
                # TODO
                """
                
                --nicht system aber fast alle 
                "_type" : "Derivation",
              "derivedTo" : "reference_data_hub_dev/dsap_geographic_region_test/country",
            "derivedFrom" : "manual_reference_data/reporting_region/country"
            "type??
                } 
                +
                  "_type" : "Dependency",
                     "dependentOf" : "mite",
                    "dependsOn" : "hubSpot",
                    "dependencyType": ??
                    } ]
                    {
                  "_type" : "Attribution",
                  "attributionFor" : "APDP-Loading sources",
                  "attributedTo" : "Barrientos, Greta",
                  "attributedAs" : "Data source manager role"
                } """
            elif entry.get("_type") == "UmlClass":
                entry["ID"] = ElementId.nextid("DATO")
                entry["PARENT"] = entry.get('inCollection')
                self.tables[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "UmlAttribute":
                entry["ID"] = ElementId.nextid("COLU")
                entry["PARENT"] = entry.get('hasDomain')
                self.columns[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "Transformation":
                entry["ID"] = ElementId.nextid("TRAF")
                entry["TYPE"] = "DATA"
                entry["PARENT"] = entry.get('transformationOf')
                self.transformations[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "Rule":
                entry["ID"] = None
                entry["TYPE"] = "DATA"
                entry["PARENT"] = entry.get('ruleOf')
                self.rules[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "Deployment":
                entry["ID"] = None
                entry["PARENT"] = entry.get('deploymentOf')
                entry["PARENT2"] = entry.get('deployedIn')
                self.deployments[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "UmlAssociation":
                entry["ID"] = ElementId.nextid("RELA")
                entry["TYPE"] = "DATA"
                entry["PARENT"] = entry.get('hasDomain')
                entry["PARENT2"] = entry.get('hasRange')
                self.relationships[self.entryid(entry=entry,
                                                name=entry.get("name") + ">" + \
                                                     j2d.custom_split(entry.get('hasRange'), "/")[-1]
                                                )
                ] = entry
            elif entry.get("_type") == "Relationship":
                entry["ID"] = ElementId.nextid("RELA")
                entry["TYPE"] = "IM"
                entry["PARENT"] = entry.get('hasDomain')
                entry["PARENT2"] = entry.get('hasRange')
                self.relationships[self.entryid(entry=entry,
                                                name=entry.get("name") + ">" + \
                                                     j2d.custom_split(entry.get('hasRange'), "/")[-1])] = entry
            elif entry.get("_type") == "ReferenceObject":
                entry["ID"] = ElementId.nextid("DOMA")
                entry["TYPE"] = "LOV"
                entry["PARENT"] = entry.get('inCollection')
                self.domains[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "ReferenceValue":
                entry["ID"] = None
                entry["PARENT"] = entry.get('literalOf')
                # TODO values with timeseries, Code type of lov code
                name = entry.get("timeSeries")[0]["code"]
                self.LOVvalues[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "DataDomain":
                entry["ID"] = ElementId.nextid("DOMA")
                entry["TYPE"] = "NORMAL"
                entry["PARENT"] = entry.get('inCollection')
                self.domains[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "DataAttribute":
                entry["ID"] = ElementId.nextid("ATTR")
                entry["PARENT"] = entry.get('hasDomain')
                self.attributes[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "Derivation":
                entry["PARENT"] = entry.get('derivedFrom')
                entry["PARENT2"] = entry.get('derivedTo')
                name = nvl(entry["PARENT2"]) + ">" + nvl(entry.get("qualifier"))
                self.derivations[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "Mapping":
                entry["ID"] = ElementId.nextid("TRAF")
                entry["TYPE"] = "VALUES"
                entry["PARENT"] = entry.get('inCollection')
                self.transformations[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "Translation":
                entry["TYPE"] = "VALUES"
                entry["PARENT"] = entry.get('translationIn')
                self.rules[self.entryid(entry=entry, name=entry.get("id"))] = entry
                # TODO
                """{
                "_type" : "Mapping",
                "id" : "5547bef9-170d-4247-a7f6-973dcf0b4dac",
                "href" : "/web/basf-agriculture/mappings/5547bef9-170d-4247-a7f6-973dcf0b4dac",
                "label" : "xxxtest",
                "mapsFrom" : "Portfolio life cycle status",
                "mapsTo" : "Country status",
                "inCollection" : "Vegetables",
                "status" : "WORKING",
                "createdBy" : "stb@foryouandyourcustomers.com",
                "dateCreated" : 1746430127105
                }, {
                "_type" : "Translation",
                "id" : "770a74ea-ee89-4a02-bc64-c99ef04c65dd",
                "href" : "/web/basf-agriculture/translations/770a74ea-ee89-4a02-bc64-c99ef04c65dd",
                "translationIn" : "xxxtest",
                "translatesFrom" : "DUMP DISC",
                "translatesTo" : "Inactive",
                "validFrom" : -2208988800000,
                "validTo" : 32503593600000,
                "status" : "WORKING",
                "createdBy" : "stb@foryouandyourcustomers.com",
                "dateCreated" : 1746430138521
                }"""
            elif entry.get("_type") == "Project":
                entry["ID"] = ElementId.nextid("DIAG")
                entry["PARENT"] = entry.get('inCollection')
                self.diagrams[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "Usage":
                entry["ID"] = ElementId.nextid("DIAE")
                entry["PARENT"] = entry.get('usedBy')
                self.diagelements[self.entryid(entry=entry, name=entry.get('usedBy') + ">" +
                                                                 entry.get('usageOf'))] = entry
            elif entry.get("_type") == "BusinessConstraint":
                entry["ID"] = ElementId.nextid("BURU")
                entry["PARENT"] = entry.get('constraintOn')
                self.businessrules[self.entryid(entry=entry, name=entry.get('label'))] = entry
            else:
                pass
                # logging.warning(f"dataspot type '{entry.get('_type')}' is not yet handled from output")
        return

    def readmodels(self, path: Path):
        def readjson(path, modelname=None):
            with open(path) as f:
                struct = json.load(f)
                if type(struct) == dict or len(struct)==0 or "_type" not in struct[0]:
                    return  # non modelfiles
                self.fillids(modelname=modelname, struct=struct)
            return

        if path.is_file():
            self.modelname=nvl(self.modelname, path.stem)
            readjson(path=path, modelname=self.modelname)
        elif path.is_dir():
            for onepath in path.iterdir():
                if onepath.suffix == '.json':
                    self.modelname=onepath.stem
                    readjson(path=onepath, modelname=self.modelname)
        else:
            raise Exception(f"path must be file or directory {path.__str__()}")
        return

