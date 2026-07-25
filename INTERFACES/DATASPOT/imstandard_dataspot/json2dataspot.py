import json
from pathlib import Path

from IM_STANDARD import JsonSchema, JsonElement, nvl,StandardJsonModel
from .dslib import escapestr,fullescapestr


class Json2dataspot():
    DUMMYCOLLECTION = "DEFAULTCOLLECTION"
    # Translation of standardmodel properties into additional properties in dataspot
    MULTILANGADDPROPS = {"name": "Name",
                         "description": "Description",
                         "shortDescr": "Title",
                         "assocText": "assocText"  # separation in fwd,bwd is done in code
                         }
    ADDITIONALPROPS={"label:en","title:en","description:en",
                     "label:de","title:de","description:de",
                     "inverseName:en","inverseName:de",
                     "Unit","multilingual","defaultValue",
                     "exclusiv-1-2","exclusiv-2-1",
                     "physicalName"
                     }
    def __init__(self, standardjson,
                 imname=None,
                 dmname=None,
                 refdomainsname=None,
                 domainsname=None,
                 systemsname=None):
        self.model = JsonSchema(standardjson)
        self.datoneeddummycatg = False
        self.lovneeddummycatg = False
        self.domaneeddummycatg = False
        self.entineeddummycatg = False
        self.imname = imname
        self.dmname = dmname
        self.domainsname = domainsname
        self.systemsname = systemsname
        self.refdomainsname = refdomainsname
        self.curlang = self.model.mainlang
        return

    @staticmethod
    def _multiplicity(card, mand):
        """translate cardinality (1,M) and mandatory bool) into 0..*,1,0..1,* into 1 or M"""
        return ("0.." if not mand else "1.." if card == "M" else "") + ("*" if card == "M" else "1")

    @staticmethod
    def fillstruct(elementtype, **kwargs):
        jsonstruct = {"_type": elementtype}
        if elementtype not in ("Derivation"):
            # elements without a status
            jsonstruct.setdefault("status", "WORKING")

        for key, val in kwargs.items():
            if key in ("_type", "_status"): continue
            if key == "additionalProps" and val is not None:
                for apkey, apval in val.items():
                    if apkey in Json2dataspot.ADDITIONALPROPS:
                        JsonElement.optionalprop(jsonstruct, apkey, apval)
            elif key.startswith("ARC_"):
                JsonElement.optionalprop(jsonstruct, key.replace('_', '-'), val)
            else:
                JsonElement.optionalprop(jsonstruct, key, val)
        return jsonstruct

    def getelembyid(self, elemid, elemtype):
        for e in self.model.jsonschemamodel[elemtype]:
            if e.get("elementId") == elemid:
                return e
        assert False, f"Id {elemid} not found in elementtype {elemtype}"

    def getfieldbyid(self, elemid, elemtype, field="name"):
        elem = self.getelembyid(elemid=elemid, elemtype=elemtype)
        retval = elem.get(field)
        if field in ("name", "shortDescr", "description"):
            return self.model.mlvalue(retval)
        else:
            return retval

    def getcategoryname(self, catgid):
        if catgid is None: return ""  # stop recursion
        catg = self.getelembyid(elemid=catgid, elemtype="Categories")
        retval = fullescapestr(self.model.mlvalue(catg.get("name")))
        if catg.get("parent") is not None:
            retval = self.getcategoryname(catgid=catg.get("parent")) + "/" + retval
        else:
            retval = retval  # + "_COLLECTION"  # TODO resolve unique collections (d.h. keine BO ) sind ok
        return retval

    def getdomainname(self, domaid):
        if domaid is None: return None
        return self.getfieldbyid(domaid, "Domains")

    def mlvalues(self, *fields, elem, default=True):
        """ return dict of values for non-mainlanguages,
            *fields list of field names to return from element
            elem json element with properties
            default True: replace nonexisting languageentry by mainlanguage entry
                    False return what you find
        """
        langs = set(self.model.languages).difference({self.model.mainlang})
        retval = dict()
        for lang in langs:
            for fname in fields:
                if fname not in elem: continue
                retval[f"{self.MULTILANGADDPROPS[fname]}:{lang}"] = self.model.mlvalue(value=elem.get(fname), lang=lang,
                                                                                       default=default)
        return retval

    def extractadditionalprops(self, element, props):
        """

        @param element: structure to transform
        @param props: list of names in element to transform to language props
        @return:
            additional propierties, language transformed if applicable, pure otherwise
        """
        additionalprops = element.get("additionalProps", dict())
        additionalprops.update(self.mlvalues(*props, elem=element, default=False))
        retval = dict()
        for aps, val in additionalprops.items():
            # translate the props into ds-keywords
            if aps.upper().startswith("NAME:"):
                retval["label:" + aps[len("NAME:"):]] = val
            elif aps.upper().startswith("DESCRIPTION:"):
                retval["description:" + aps[len("DESCRIPTION:"):]] = val
            elif aps.upper().startswith("TITLE:"):
                retval["title:" + aps[len("TITLE:"):]] = val
            elif aps.upper().startswith("SHORTDESCR:"):
                retval["title:" + aps[len("SHORTDESCR:"):]] = val
            else:
                retval[aps] = val
        return retval

    def categories(self, catgtype, catglist=None) -> list:
        categories = self.model.jsonschemamodel.get("Categories", [])
        retval = []
        for catg in categories:
            if catg.get("categoryType") != catgtype: continue
            if catglist is not None and catg.get("elementId") not in catglist: continue

            catgname = escapestr(self.model.mlvalue(catg.get("name")))
            additionalprops = self.extractadditionalprops(element=catg,
                                                          props=["name", "description"])

            retval.append(self.fillstruct(elementtype="Collection",
                                          label=catgname,
                                          # TODO nur doppelte werden ergänzt um Postfix d.h. Toplevel die entitäten sind oder lowlevel die Entitäten mit gleichem Namen in sich haben
                                          description=escapestr(self.model.mlvalue(catg.get("description", ""))),
                                          inCollection=self.getcategoryname(catgid=catg.get("parent")),
                                          favorite=False,
                                          additionalProps=additionalprops
                                          ))
        return retval

    def getentikeys(self, enti):
        retval = []
        keys = enti.get("keys")
        if keys is None:
            return retval
        else:
            keyelems = set(elem for sublist in keys for elem in sublist)
            retval = list(keyelems)
        return retval

    def datareferences(self, dataobject):
        retval = []
        for dataref in dataobject.get("references", []):
            additionalprops = self.extractadditionalprops(element=dataref,
                                                          props=["name", "mandatory",
                                                                 "maxcardinality",
                                                                 "refdataobjectid",
                                                                 "attributeref"])
            todato = self.getelembyid(elemid=dataref.get("refdataobjectid"),
                                      elemtype="DataObjects")
            retval.append(self.fillstruct(elementtype="UmlAssociation",
                                          hasDomain=self.dataobjecteref(catgid=dataobject.get('categoryId'),
                                                                        dataobjectname=dataobject.get("name")),
                                          name=f"{dataobject.get('name')} - {todato.get('name')}",
                                          domainMultiplicity=self._multiplicity(card="M",
                                                                               mand=False
                                                                               ),
                                          hasRange=self.dataobjecteref(catgid=todato.get('categoryId'),
                                                                        dataobjectname=todato.get("name")),
                                          inverseName=None,
                                          rangeMultiplicity=self._multiplicity(
                                              card="1" if dataref.get("maxcardinality", 1) == 1 else "M",
                                              mand=dataref.get("mandatory", False)
                                              ),
                                          identifying=False,
                                          navigable="NONE",
                                          temporal=False,
                                          ARC_12=None,  # verkehrte Welt
                                          ARC_21=None,  # verkehrte Welt
                                          additionalProps=additionalprops,
                                          linksDomain=None,  # ["Organisation/Company/Company name"],
                                          linksRange=None,  # ["Organisation/General/Comment"],
                                          onDelete=None,  # "RESTRICT",
                                          onUpdate=None,  # "CASCADE" SET_NULL
                                          )
                          )
        return retval

    def relations(self, modeltype):
        relas = self.model.jsonschemamodel.get("Relations", [])
        retval = []
        for rela in relas:
            relamult12 = self._multiplicity(card=rela["fwd"].get("cardinality"), mand=rela["fwd"].get("mandatory"))
            assoc12 = self.model.mlvalue(rela["fwd"].get("assocText"))
            assoc12 = "is" if nvl(assoc12) == "" else assoc12.strip()
            arc_12 = rela["fwd"].get("arcNumber")
            rangeobj = self.getelembyid(elemid=rela["fwd"].get("entityId"), elemtype="Entities") if modeltype == "IM" \
                else self.getelembyid(elemid=rela["fwd"].get("dataObjectId"), elemtype="DataObjects")

            relamult21 = self._multiplicity(card=rela["bwd"].get("cardinality"), mand=rela["bwd"].get("mandatory"))
            assoc21 = self.model.mlvalue(rela["bwd"].get("assocText"))
            assoc21 = "is" if nvl(assoc21) == "" else assoc21.strip()
            arc_21 = rela["bwd"].get("arcNumber")
            domainobj = self.getelembyid(elemid=rela["bwd"].get("entityId"), elemtype="Entities") if modeltype == "IM" \
                else self.getelembyid(elemid=rela["bwd"].get("dataObjectId"), elemtype="DataObjects")

            """ define the direction of the relationship in dataspot
                1->M  1 ist first (domainid) direction RANGE
                M->M  arbitrary direction BOTH  
                1->1  the one with an arc is first direction RANGE
                1->1  arbitrary if no arc direction NONE
                """
            if "*" in relamult12 and "*" in relamult21:
                navigable = "BOTH"
            elif "*" in relamult12:
                navigable = "RANGE"
                domainobj, relamult12, assoc12, arc_12, rangeobj, relamult21, assoc21, arc_21 = rangeobj, relamult21, assoc21, arc_21, domainobj, relamult12, assoc12, arc_12
            elif "*" in relamult21:
                navigable = "RANGE"
            elif relamult12 == "1" and relamult21 == "1":
                if arc_12 is not None:
                    navigable = "RANGE"
                elif arc_21 is not None:
                    navigable = "RANGE"
                    relamult12, assoc12, arc_12, relamult21, assoc21, arc_21 = relamult21, assoc21, arc_21, relamult12, assoc12, arc_12
                else:
                    navigable = "NONE"
            elif relamult12 == "1":
                navigable = "RANGE"
                relamult12, assoc12, arc_12, relamult21, assoc21, arc_21 = relamult21, assoc21, arc_21, relamult12, assoc12, arc_12
            elif relamult21 == "1":
                navigable = "RANGE"
            else:
                navigable = "NONE"

            temporal = rela["bwd"].get("historicised") or rela["fwd"].get("historicised")
            identifying = rela.get("elementId") in self.getentikeys(enti=rangeobj) or \
                          rela.get("elementId") in self.getentikeys(enti=domainobj)
            multilangassoc = {f"name:{key[-2:]}": val for key, val in
                              self.mlvalues("assocText", elem=rela["bwd"], default=False).items()}
            multilangassoc.update({f"inverseName:{key[-2:]}": val for key, val in
                                   self.mlvalues("assocText", elem=rela["fwd"], default=False).items()})

            additionalprops = rela.get("additionalProps", dict())
            additionalprops.update(multilangassoc)
            destinationtype = "UmlAssociation" if modeltype == "DM" else "Relationship"
            retval.append(self.fillstruct(elementtype=destinationtype,
                                          hasDomain=self.dataobjecteref(catgid=domainobj.get('categoryId'),
                                                                        dataobjectname=self.model.mlvalue(
                                                                            domainobj.get("name"))),
                                          name=assoc21,
                                          domainMultiplicity=relamult12,
                                          hasRange=self.dataobjecteref(catgid=rangeobj.get('categoryId'),
                                                                       dataobjectname=self.model.mlvalue(
                                                                           rangeobj.get("name"))),
                                          inverseName=assoc12,
                                          rangeMultiplicity=relamult21,
                                          identifying=identifying,
                                          navigable=navigable,
                                          temporal=temporal,
                                          ARC_12=arc_21,  # verkehrte Welt
                                          ARC_21=arc_12,  # verkehrte Welt
                                          additionalProps=additionalprops,
                                          linksDomain=None,  # ["Organisation/Company/Company name"],
                                          linksRange=None,  # ["Organisation/General/Comment"],
                                          onDelete=None,  # "RESTRICT",
                                          onUpdate=None,  # "CASCADE" SET_NULL
                                          )
                          )
        return retval

    def domainrange(self, domainid):
        """

        @param domainid:
                either DOMAxxx
                or {"domainId": "DOMAxxx",
                    "modelName": "yyyyy"
                }
        @return: domainrange for dataspot
        """
        if domainid is None: return None
        if type(domainid) == dict:
            modelname = domainid.get("modelName", self.imname)
            domaid = domainid.get("domainId")
        else:
            modelname = self.imname
            domaid = domainid
        if modelname == self.imname:
            doma = self.getelembyid(domaid, "Domains")
            if doma.get("domainType") == "LOVDomain":
                modelname = self.refdomainsname
            else:
                modelname = self.domainsname
        else:
            assert False, "woher weiss ich den Namen des domains bei fremden Modellen"

        return f"/{modelname}/{self.model.mlvalue(doma.get('name'))}"

    def attrlist(self, parentobj: dict) -> list:
        # TODO add ranges
        attributes = [a for a in self.model.jsonschemamodel.get("Attributes", []) if
                      a.get("parentId") == parentobj.get("elementId")]
        entiref = fullescapestr(self.model.mlvalue(parentobj.get("name")))
        attrtype = "BusinessAttribute" if parentobj.get("elementId").startswith("ENTI") else "DataAttribute"
        retval = []
        for attr in attributes:
            additionalprops = self.extractadditionalprops(element=attr,
                                                          props=["name", "description", "shortDescr"])
            retval.append(self.fillstruct(elementtype=attrtype,
                                          hasDomain=entiref,
                                          label=escapestr(self.model.mlvalue(attr.get("name"))),
                                          title=escapestr(self.model.mlvalue(attr.get("shortDescr"))),
                                          description=escapestr(self.model.mlvalue(attr.get("description"))),
                                          favorite=attr.get("descriptive"),
                                          hasRange=self.domainrange(attr.get("domainId")),
                                          examples=attr.get("examples"),
                                          required="MANDATORY" if attr.get("mandatory") else "OPTIONAL",
                                          cardinality="MANY" if attr.get("repeated") else "ONE",
                                          temporal=attr.get("historicised"),
                                          order=attr.get("displaySeq"),
                                          additionalProps=additionalprops
                                          ))
        return retval

    def path(self, catgid):
        if catgid is None: return None
        catg = self.getelembyid(elemid=catgid, elemtype="Categories")  # self.jsonschemamodel["Categories"].get(catgid)
        retval = None
        if catg is not None:
            if catg.get("parent") is None:
                retval = fullescapestr(self.model.mlvalue(value=catg.get("name")))
            else:
                retval = self.getcategoryname(catg.get("parent")) + \
                         "/" + fullescapestr(self.model.mlvalue(value=catg.get("name")))
        return retval

    def dataobjecteref(self, catgid, dataobjectname):
        return f"{nvl(self.path(catgid), self.DUMMYCOLLECTION)}/{fullescapestr(dataobjectname)}"

    def dataattributelist(self) -> list:
        # TODO add ranges
        # if dataobject.get('name') in ("PPH_CCGLT_MTLS", "PPH_MLGT", "PPH_MARD", "PPH_MAT_STEP",
        #                          "PPH_MAT_R3", "PPH_CCGLT_MTLV",
        #                          "Shopspezifische Marketingangaben [lumimart.ch]"):
        #     logging.warning(f"umlclass not handled yet {dataobject.get('name')}")
        #     return []  # TODO special cases

        # TODO mit Vater dazu
        donedatanames = []

        datalist = self.model.jsonschemamodel.get("DataAttributes", [])
        retval = []
        for data in datalist:
            dataobject = self.getelembyid(elemid=data.get("dataObjectId"), elemtype="DataObjects")
            additionalprops = data.get("additionalProps", dict())
            additionalprops.update(self.mlvalues("name", "description", "shortDescr",
                                                 elem=data, default=False))


            dataname = self.makeunique(name=escapestr(data.get("name")),
                                       donenames=[datnam.split(":")[1] for datnam in donedatanames if
                                                  datnam.startswith(f"{dataobject.get('name')}:")])
            donedatanames.append(f"{dataobject.get('name')}:{dataname}")
            retval.append(self.fillstruct(elementtype="UmlAttribute",
                                          hasDomain=self.dataobjecteref(catgid=dataobject.get('categoryId'),
                                                                        dataobjectname=dataobject.get('name')),
                                          label=dataname,
                                          title=escapestr(data.get("shortDescr")),
                                          description=escapestr(nvl(data.get("description"))),
                                          favorite=data.get("descriptive"),
                                          hasRange=self.domainrange(data.get("domainId")),
                                          displaySeq=data.get("displaySeq"),
                                          examples=data.get("examples"),
                                          required="MANDATORY" if data.get("mandatory") else "OPTIONAL",
                                          cardinality="MANY" if data.get("repeated") else "ONE",
                                          temporal=data.get("historicised"),
                                          order=data.get("displaySeq"),
                                          physicalName=data.get("technicalName"),
                                          additionalProps=additionalprops
                                          ))
        return retval

    def systemname(self, systid):
        if systid is None:
            systemname = None
        else:
            systemname = self.getelembyid(systid, "Systems").get("name")
        return systemname

    def collectionname(self, catgid):
        if catgid is None:
            collectionname = self.DUMMYCOLLECTION
        else:
            collectionname = self.getcategoryname(catgid=catgid)
        return collectionname

    def entitylist(self) -> list:
        # TODO resolve subcategories, requiring a parent categoriy as reference
        entities = self.model.jsonschemamodel.get("Entities", [])
        doneentitynames = []
        retval = []
        for enti in entities:
            additionalprops = self.extractadditionalprops(element=enti,
                                                          props=["name", "description", "shortDescr"])
            self.entineeddummycatg = self.entineeddummycatg or enti.get("categoryId") is None
            entityname = self.makeunique(name=escapestr(self.model.mlvalue(enti.get("name"))),
                                         donenames=doneentitynames)

            # make sure name is not also used as category for entities
            catgs = self.model.jsonschemamodel.get("Categories")
            if entityname in [self.model.mlvalue(elem.get("name")) for elem in catgs if
                              elem.get("categoryType") == "ENTITY"]:
                entityname += " (business object)"

            doneentitynames.append(entityname)
            retval.append(self.fillstruct(elementtype="BusinessObject",
                                          label=entityname,
                                          title=self.model.mlvalue(enti.get("shortDescr")),
                                          description=escapestr(nvl(self.model.mlvalue(enti.get("description")))),
                                          examples=enti.get("examples"),
                                          synonyms=[self.model.mlvalue(e) for e in enti.get("synonyms", [])],
                                          inCollection=self.collectionname(catgid=enti.get("categoryId")),
                                          favorite=False,
                                          additionalProps=additionalprops
                                          ))
            retval += self.attrlist(parentobj=enti)
        return retval

    def lovdomains(self):
        domains = self.model.jsonschemamodel.get("Domains", [])
        donedomainnames = []
        retval = []
        for idx, doma in enumerate(domains):
            if idx > 10000: break
            if doma.get("domainType") != "LOVDomain": continue

            self.lovneeddummycatg = self.lovneeddummycatg or doma.get("categoryId") is None
            domainname = self.makeunique(name=escapestr(self.model.mlvalue(doma.get("name"))),
                                         donenames=donedomainnames)
            # make sure name is not also used as category for entities
            catgs = self.model.jsonschemamodel.get("Categories")
            if domainname in [self.model.mlvalue(elem.get("name")) for elem in catgs if
                              elem.get("categoryType") == "DOMAIN"]:
                domainname += " (LOV domainid)"

            additionalprops = self.extractadditionalprops(element=doma, props=["name", "description"])
            donedomainnames.append(domainname)

            retval.append(self.fillstruct(elementtype="ReferenceObject",
                                          label=domainname,
                                          description=escapestr(nvl(self.model.mlvalue(doma.get("description")))),
                                          inCollection=self.collectionname(catgid=doma.get("categoryId")),
                                          examples=doma.get("examples"),
                                          additionalProps=additionalprops
                                          )
                          )
            for idx2, val in enumerate(doma.get("values", [])):
                retval.append(self.fillstruct(elementtype="ReferenceValue",
                                              favorite=idx2 < 3,
                                              literalOf=fullescapestr(
                                                  self.model.mlvalue(doma.get("name"), lang=self.model.mainlang)),
                                              timeSeries=[{
                                                  "validFrom": -2208988800000,
                                                  "validTo": 32503593600000,
                                                  "code": val.get("value"),
                                                  "shortText": escapestr(
                                                      self.model.mlvalue(val.get("displayValue"))),
                                                  "longText": escapestr(self.model.mlvalue(val.get("description")))
                                              }
                                              ]
                                              )
                              )

        return retval

    @staticmethod
    def toint(val):
        return None if val is None else int(val)

    def domainlist(self) -> list:
        domains = self.model.jsonschemamodel.get("Domains", [])
        donedomainnames = []
        retval = []
        for doma in domains:
            if doma.get("domainType") == "LOVDomain": continue
            additionalprops = self.extractadditionalprops(element=doma, props=["name", "description"])

            self.domaneeddummycatg = self.domaneeddummycatg or doma.get("categoryId") is None
            domainname = self.makeunique(name=escapestr(self.model.mlvalue(doma.get("name"))),
                                         donenames=donedomainnames)
            # make sure name is not also used as category for domains
            catgs = self.model.jsonschemamodel.get("Categories")
            if domainname in [self.model.mlvalue(elem.get("name")) for elem in catgs if
                              elem.get("categoryType") == "DOMAIN"]:
                domainname += " (domainid)"
            donedomainnames.append(domainname)
            domain = {"elementtype": "DataDomain",
                      "label": domainname,
                      # "title":doma.get("name"),
                      "description": escapestr(nvl(self.model.mlvalue(doma.get("description")))),
                      "inCollection": self.collectionname(catgid=doma.get("categoryId")),
                      "examples": doma.get("examples"),
                      "additionalProps": additionalprops
                      }
            if doma.get("domainType") == "TextDomain":
                domain["pattern"] = doma.get("syntaxRule")
                domain["baseType"] = "STRING"
                domain["minLength"] = doma.get("minLength")
                domain["maxLength"] = doma.get("maxLength")
            elif doma.get("domainType") == "NumericDomain":
                domain["minInclusive"] = doma.get("minValue")
                domain["maxInclusive"] = doma.get("maxValue")
                domain["integerDigits"] = None if doma.get("totalDigits") is None \
                    else (self.toint(doma.get("totalDigits"))
                          - nvl(self.toint(doma.get("fractDigits")), 0))
                domain["fractionDigits"] = self.toint(doma.get("fractDigits"))
                # domainid["roundValue"]=
                # domainid["unit"]=
            retval.append(self.fillstruct(**domain))
            """  "_type" : "DataDomain",
  "title" : "wahr / falsch",
  "inCollection" : "Basis Datentypen",
  "status" : "WORKING",
  "createdBy" : "dataspot.",
  "dateCreated" : 1737640210995,
  "baseType" : "BOOLEAN",
"""
        return retval

    def systemlist(self) -> list:
        systems = self.model.jsonschemamodel.get("Systems", [])
        donenames = []
        retval = []
        for syst in systems:
            self.domaneeddummycatg = self.domaneeddummycatg or syst.get("categoryId") is None
            systname = self.makeunique(name=escapestr(syst.get("name")),
                                       donenames=donenames)
            # make sure name is not also used as category for domains
            catgs = self.model.jsonschemamodel.get("Categories")
            if systname in [self.model.mlvalue(elem.get("name")) for elem in catgs if
                            elem.get("categoryType") == "SYSTEM"]:
                systname += " (system)"
            donenames.append(systname)
            system = {"elementtype": "System",
                      "label": systname,
                      "title": None,
                      "description": escapestr(nvl(self.model.mlvalue(syst.get("description"))))
                      }
            if syst.get("categoryId") is not None:
                system["inCollection"] = self.collectionname(catgid=syst.get("categoryId"))
            if syst.get("parent") is not None:
                system["subsystemOf"] = self.systemname(systid=syst.get("parent"))
            retval.append(self.fillstruct(**system))
        return retval

    def dsentityjson(self) -> list:
        """create from a standardjson a dataspot load-json"""
        retval = list()
        if self.model.modeltype not in ("Information model","Artefact model"): return retval
        retval += self.entitylist()
        if len(retval) > 0:
            retval += self.categories(catgtype="ENTITY")
            retval.append(self.fillstruct(elementtype="Collection",
                                          label=self.DUMMYCOLLECTION,
                                          description="REPLACE BY PROPER collection"
                                          ))

            retval += self.relations(modeltype="IM")
            if not self.entineeddummycatg:
                retval = [d for d in retval if not (d['_type'] == "Collection" and d["label"] == self.DUMMYCOLLECTION)]
        return retval

    def getusedcategories(self, withparents=True):
        return [doma.get("elementId")
                for doma in self.model.jsonschemamodel["Domains"]
                if doma.get("domainType") == "Domain"]

    def getmycategoryIdtree(self, categoryIds, withparents=False):
        retval = categoryIds
        mycategories = [catg for catg in self.model.jsonschemamodel["Categories"] if
                        catg.get("elementId") in categoryIds]
        # TODO MANY in jsonschema
        parents = []
        for catg in mycategories:
            if withparents and catg.get("parent") is not None \
                    and catg.get("parent") not in retval + parents:
                parents.extend(self.getmycategoryIdtree(categoryIds=[catg.get("parent")], withparents=True))
        retval.extend(parents)
        return retval

    def dsreferencejson(self):
        retval = list()
        retval += self.lovdomains()
        if len(retval) > 0:
            refdomains = [doma for doma in self.model.jsonschemamodel.get("Domains", []) if
                          doma.get("domainType") == "LOVDomain"]
            retval += self.categories(catgtype="DOMAIN",
                                      catglist=self.getmycategoryIdtree(
                                          categoryIds=list(set(d.get("categoryId") for d in refdomains)),
                                          withparents=True)
                                      )

            retval.append(self.fillstruct(elementtype="Collection",
                                          label=self.DUMMYCOLLECTION,
                                          description="REPLACE BY PROPER collection"
                                          ))
        if not self.lovneeddummycatg:
            retval = [d for d in retval if not (d['_type'] == "Collection" and d["label"]) == self.DUMMYCOLLECTION]
        return retval

    def dsdomainjson(self):
        retval = list()
        retval += self.domainlist()
        if len(retval) > 0:
            domains = [doma for doma in self.model.jsonschemamodel.get("Domains", []) if
                       doma.get("domainType") != "LOVDomain"]
            for doma in domains:
                retval += self.attrlist(parentobj=doma)

            retval += self.categories(catgtype="DOMAIN",
                                      catglist=self.getmycategoryIdtree(
                                          categoryIds=list(set(d.get("categoryId") for d in domains)),
                                          withparents=True)
                                      )

            retval.append(self.fillstruct(elementtype="Collection",
                                          label=self.DUMMYCOLLECTION,
                                          description="REPLACE BY PROPER collection"
                                          ))

            if not self.domaneeddummycatg:
                retval = [d for d in retval if not (d['_type'] == "Collection" and d["label"]) == self.DUMMYCOLLECTION]
        return retval

    def dssystemjson(self):
        retval = list()
        retval += self.systemlist()
        if len(retval) > 0:
            retval += self.categories(catgtype="SYSTEM")
            return retval
            retval.append(self.fillstruct(elementtype="Collection",
                                          label=self.DUMMYCOLLECTION,
                                          description="REPLACE BY PROPER collection"
                                          ))

            if not self.domaneeddummycatg:
                retval = [d for d in retval if not (d['_type'] == "Collection" and d["label"]) == self.DUMMYCOLLECTION]
        return retval

    def makeunique(self, name: str, donenames: list) -> str:
        idx = 1
        secondtablename = name
        while secondtablename in donenames:
            secondtablename = f"{name} -{str(idx)}"
            idx += 1
            assert idx < 1000, f" more than 1000 duplicates {name}"
        return secondtablename

    def dataobjectlist(self):
        dataobjects = self.model.jsonschemamodel.get("DataObjects", [])
        donedatonames = []
        retval = []
        retval += self.categories(catgtype="DATAOBJECT")
        for dato in dataobjects:
            additionalprops = dato.get("additionalProps", dict())

            self.datoneeddummycatg = self.datoneeddummycatg or dato.get("categoryId") is None
            datoname = self.makeunique(name=escapestr(dato.get("name")),
                                       donenames=donedatonames)
            donedatonames.append(datoname)
            retval.append(self.fillstruct(elementtype="UmlClass",
                                          label=datoname,
                                          title=dato.get("shortDescr"),
                                          description=escapestr(nvl(dato.get("description"))),
                                          examples=dato.get("examples"),
                                          synonyms=[e for e in dato.get("synonyms", [])],
                                          inCollection=self.collectionname(catgid=dato.get("categoryId")),
                                          favorite=False,
                                          physicalName= dato.get("technicalName"),
                                          additionalProps=additionalprops
                                          ))
        return retval

    def dsdmjson(self) -> list:
        """create from a datamodel standardjson a dataspot load-json"""
        retval = list()
        if self.model.modeltype != "Artefact model": return retval
        retval += self.dataobjectlist()
        if len(retval) > 0:
            retval += self.categories(catgtype="DATAOBJECT")
            retval.append(self.fillstruct(elementtype="Collection",
                                          label=self.DUMMYCOLLECTION,
                                          description="REPLACE BY PROPER collection"
                                          ))

            retval += self.dataattributelist()
            for dato in self.model.jsonschemamodel.get("DataObjects", []):
                retval += self.datareferences(dataobject=dato)

            if not self.datoneeddummycatg:
                retval = [d for d in retval if not (d['_type'] == "Collection" and d["label"] == self.DUMMYCOLLECTION)]
        return retval


def dumpmodel(outpath, modelname, elements):
    if modelname is not None and len(elements) > 0:
        StandardJsonModel.dumpjsonfile(path=Path(outpath) / f"{modelname}.json",
                                       struct=elements,
                                       verbose=True)


def json2dataspot(injson, outpath,
                  imname=None,
                  dmname=None,
                  refdomainsname="Reference_model",
                  domainsname="Domain_model",
                  systemsname="Systems_model"):
    # hack for the moment
    locimname = nvl(imname, "Business_data_model")

    if type(injson) == dict:
        jsfile = injson
    else:
        with open(injson) as infile:
            jsfile = json.load(infile)
    dsjson = Json2dataspot(standardjson=jsfile,
                           imname=locimname,
                           dmname=dmname,
                           refdomainsname=refdomainsname,
                           domainsname=domainsname,
                           systemsname=systemsname)
    print(f"\nFrom file {injson} generated:")
    dumpmodel(outpath=outpath, modelname=imname, elements=dsjson.dsentityjson())
    dumpmodel(outpath=outpath, modelname=domainsname, elements=dsjson.dsdomainjson())
    dumpmodel(outpath=outpath, modelname=refdomainsname, elements=dsjson.dsreferencejson())
    dumpmodel(outpath=outpath, modelname=dmname, elements=dsjson.dsdmjson())
    dumpmodel(outpath=outpath, modelname=systemsname, elements=dsjson.dssystemjson())
    dumpmodel(outpath=outpath, modelname=dmname, elements=dsjson.dsdmjson())
    return


if __name__ == '__main__':
    import sys

    json2dataspot(injson=sys.argv[1],
                  outpath=sys.argv[2])
