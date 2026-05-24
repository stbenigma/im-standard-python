import json
import logging
from pathlib import Path

from IM_STANDARD import nvl, ElementId
from .dslib import custom_split


class DataspotElements():
    def __init__(self, indirec:Path=None, **kwargs):
        # models
        tenant = kwargs.get("tenant")
        if type(tenant) is str:
            self.tenant = {"name": tenant}
        elif type(tenant) is dict:
            self.tenant = tenant
        else:
            self.tenant = dict()

        self.dsmodels = dict()
        self.modelname = kwargs.get("modelname")

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
        self.usages = dict()
        self.mappings = dict()
        self.rules = dict()
        self.translations = dict()
        self.deployments = dict()
        self.dependencies = dict()
        self.derivations = dict()
        self.diagrams = dict()
        self.diagelements = dict()
        self.businessrules = dict()
        self.dataobjects = dict()
        self.dataattributes = dict()

        if indirec is not None:
            self.readmodels(indirec)
        return

    def sourcehref(self, element):
        return f"{self.tenant.get('server')}{element.get('href').replace('/web/', '/rest/')}"

    def modeltype(self, struct):
        if type(struct) == list:
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
                logging.warning(f"inputfiletype not yet handled for {set([elem.get('_type') for elem in struct])}")
                return None
        else:
            raise Exception(f"no list in file but '{type(struct)}'")

    def entryid(self, entry, name):
        model = entry.get('DSMODEL')
        parent = entry.get('PARENT')
        return f"""{model}/{"" if parent is None else (parent + '/')}{nvl(name)}"""

    def elementname(self, entry):
        """
        depending on elemtype construct  a name for the element
        :param entry: json-structure from dataspot
        :return: unique name of the element
        """

        if entry.get("_type") in ('UmlAssociation', 'Relationship'):
            retval = entry.get("name") + "->" + \
                     custom_split(entry.get('hasRange'), "/")[-1]
        elif entry.get("_type") == 'ReferenceValue':
            retval = entry.get("timeSeries")[0]["code"]
        elif entry.get("_type") == 'Translation':
            retval = entry.get("translationIn") + \
                     "/" + \
                     custom_split(entry.get("translatesFrom"), '/')[-1] + \
                     custom_split(entry.get("translatesTo"), '/')[-1]
        elif entry.get("_type") == 'Derivation':
            retval = nvl(entry.get("PARENT2")) + ("" if entry.get("qualifier") is None \
                                                      else (">" + entry.get("qualifier")))
        elif entry.get("_type") == 'Dependency':
            retval = entry.get("stereotype", "") + ">" + \
                     nvl(entry.get('dependsOn'))
        elif entry.get("_type") == 'Usage':
            retval = entry.get('usedBy') + ("" if entry.get("usageOf") is None
                                            else (">" + entry.get("usageOf")))
        else:
            retval = entry.get('label')
        return retval

    def elementfullpath(self, modelname, entry):
        if entry.get("_type") in ('UmlAssociation', 'Relationship'):
            pathstart = entry.get('hasDomain') + "->"
        elif entry.get("_type") in ('Dependency',):
            pathstart = entry.get('PARENT') + ">"
        else:
            pathstart = nvl(entry.get('PARENT')) + "/"
        return f"{modelname}:{pathstart}{self.elementname(entry)}"

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

    @staticmethod
    def checkstatus(elem, filterstatus):
        """

        :param elem: element to be checked
        :param filterstatus: PUBL,GTOP,ALL,None
        :return:
        true, if elem.get("status") is empty or fullfils the filterstatus
        false else
        """
        if filterstatus in ("ALL", None):
            return True
        status = elem.get("status")
        if status is None:
            return True
        if filterstatus == "PUBL" and status in ("PUBLISHED",):
            return True
        if filterstatus == "GTOP" and status in ("PUBLISHED",
                                                 "ACCEPTED",
                                                 "FINAL"):
            return True
        return False

    @staticmethod
    def filterelements(element: dict,
                       elemtype: str = None,
                       status: str = None) -> dict:
        """
        returns the dictionary filtered by type and status.

        :param element: dictionnary of dataspot elements
        :param elemtype: "TYPE" attribute in dictionnary
        :param status:  status attribute ("PUBL", "GTOP", "ALL",None)
        :return: dictionnary of filtered entries
        """
        return {key: val for key, val in element.items()
                if (elemtype is None or val.get("TYPE") == elemtype) \
                and (status is None or DataspotElements.checkstatus(val, status))}

    def metainfo(self, struct: dict):
        """
        :param struct: put the struct-info in its appropriate container
        :return: nothing
        """
        if struct.get("_type") == "Tenant":
            self.tenant["name"] = struct.get("tenantName")
            self.tenant["id"] = struct.get("id")
            self.tenant["db"] = struct.get("db")
            self.tenant["uri"] = struct.get("_links", dict()).get("self", dict()).get("href")

        elif struct.get("_type") in ("BusinessDataModel",
                                     "UmlModel",
                                     "SystemCatalog",
                                     "ProjectDirectory"):
            self.dsmodels[struct.get('label')] = {"name": struct.get('label'),
                                                  "id": struct.get("id"),
                                                  "parentid": struct.get("tenantId"),
                                                  "description": struct.get("description"),
                                                  "title": struct.get("title")
                                                  }
        else:
            others = ["ReferenceDataModel",
                      "DataDomainModel",
                      ]
            logging.warning(f"not yet handled modeltype {struct.get('_type')}")
        return

    def fillids(self, modelname, struct: list):
        """create spod id for every element and add element by natural name to its proper list.
           the name of the file is used as the model name in which the element was found
        """
        modeltype = self.modeltype(struct)
        if modeltype is None:
            return
        for entry in struct:
            entry["DSMODEL"] = modelname
            name = self.elementname(entry=entry)
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
                                                name=name
                                                )] = entry
            elif entry.get("_type") == "Relationship":
                entry["ID"] = ElementId.nextid("RELA")
                entry["TYPE"] = "IM"
                entry["PARENT"] = entry.get('hasDomain')
                entry["PARENT2"] = entry.get('hasRange')
                self.relationships[self.entryid(entry=entry,
                                                name=name)] = entry
            elif entry.get("_type") == "ReferenceObject":
                entry["ID"] = ElementId.nextid("DOMA")
                entry["TYPE"] = "LOV"
                entry["PARENT"] = entry.get('inCollection')
                self.domains[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "ReferenceValue":
                entry["ID"] = None
                entry["PARENT"] = entry.get('literalOf')
                # TODO values with timeseries, Code type of lov code
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
                self.derivations[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "Mapping":
                entry["ID"] = ElementId.nextid("MAPP")
                entry["TYPE"] = "VALUES"
                entry["PARENT"] = entry.get('inCollection')
                self.mappings[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "Translation":
                entry["TYPE"] = "VALUES"
                entry["PARENT"] = entry.get('translationIn')
                self.translations[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "Project":
                entry["ID"] = ElementId.nextid("DIAG")
                entry["PARENT"] = entry.get('inCollection')
                self.diagrams[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "Usage":
                entry["ID"] = None
                entry["PARENT"] = entry.get('usedBy')
                self.diagelements[self.entryid(entry=entry, name=name)] = entry
            elif entry.get("_type") == "BusinessConstraint":
                entry["ID"] = ElementId.nextid("BURU")
                entry["PARENT"] = entry.get('constraintOn')
                entry.get('label')
                self.businessrules[self.entryid(entry=entry, name=name)] = entry
            else:
                logging.warning(f"dataspot type '{entry.get('_type')}' is not yet handled from output")
            entry["FULLPATH"] = self.elementfullpath(modelname=modelname, entry=entry)
        return

    def readmodels(self, path: Path):
        def readjson(lpath, modelname=None):
            with open(lpath) as f:
                struct = json.load(f)

                if type(struct) == dict and "_type" in struct:
                    self.metainfo(struct)
                elif type(struct) == list and len(struct) > 0 and "_type" in struct[0]:
                    self.fillids(modelname=modelname, struct=struct)
            return

        if path.is_file():
            self.modelname = nvl(self.modelname, path.stem)
            readjson(lpath=path, modelname=self.modelname)
        elif path.is_dir():
            for onepath in path.iterdir():
                if onepath.suffix == '.json':
                    self.modelname = onepath.stem
                    readjson(lpath=onepath, modelname=self.modelname)
        else:
            raise Exception(f"path must be file or directory {path.__str__()}")
        return
