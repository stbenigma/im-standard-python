import json
from pathlib import Path

from IM_STANDARD import JsonSchema,JsonElement,nvl

class Json2dataspot():
    DUMMYCOLLECTION = "DEFAULTCOLLECTION"
    # Translation of standardmodel properties into additional properties in dataspot
    MULTILANGADDPROPS = {"name": "Name",
                         "description": "Description",
                         "shortdescr": "Title",
                         "assoctext": "assoctext"  # separation in fwd,bwd is done in code
                         }

    def __init__(self, standardjson,
                 imname=None,
                 dmname=None,
                 refdomainsname=None,
                 domainsname=None,
                 systemsname=None):
        super().__init__(model=standardjson)
        self.tableneeddummycatg = False
        self.lovneeddummycatg = False
        self.domaneeddummycatg = False
        self.entineeddummycatg = False
        self.imname = imname
        self.dmname = dmname
        self.domainsname = domainsname
        self.systemsname = systemsname
        self.refdomainsname = refdomainsname
        self.curlang=self.mainlang
        return

    @staticmethod
    def _multiplicity(card, mand):
        """translate cardinality (1,M) and mandatory bool) into 0..*,1,0..1,* into 1 or M"""
        return ("0.." if not mand else "1.." if card == "M" else "") + ("*" if card == "M" else "1")

    @staticmethod
    def fillstruct(elementtype, **kwargs):
        jsonstruct = {"_type": elementtype
                      # "createdBy": None,
                      # "dateCreated": None
                      }
        if elementtype not in ("Derivation"):
            #elements without a status
            jsonstruct.setdefault("status","WORKING")
        for key, val in kwargs.items():
            if key in ("_type", "_status"): continue
            if key == "additionalProps" and val is not None:
                for apkey, apval in val.items():
                    JsonElement.optionalprop(jsonstruct, apkey, apval)
            elif key.startswith("ARC_"):
                JsonElement.optionalprop(jsonstruct, key.replace('_', '-'), val)
            else:
                JsonElement.optionalprop(jsonstruct, key, val)
        return jsonstruct

    @staticmethod
    def escapestr(instr):
        """
        escape all characters in a string not suitable for dataspot
        :param instr:
        :return:
        """
        if instr is None: return instr
        retval = instr.replace('"', '\\"').\
                    replace("\n", " ").\
                    replace("\u00a0", " ").\
                    replace("\u0013", "-").\
                    replace("\u0014", "-")
        return retval

    @staticmethod
    def fullescapestr(instr):
        """ escape string and then enclose string in "" if it contains / or . """
        retval = Json2dataspot.escapestr(instr)
        if retval is not None and (("/" in instr) or ('.' in instr)):
            retval = f'"{retval}"'
        return retval

    @staticmethod
    def custom_split(input_string, delimiter,quote='"'):
        result = []
        current_segment = []
        in_quotes = False
        if input_string is None: return result

        for char in input_string:
            if char == quote:
                in_quotes = not in_quotes
            elif char == delimiter and not in_quotes:
                result.append(Json2dataspot.escapestr(''.join(current_segment)))
                current_segment = []
            else:
                current_segment.append(char)

        result.append(Json2dataspot.escapestr(''.join(current_segment)))
        return result

    def getelembyid(self, id, elemtype):
        for e in self.jsonschemamodel[elemtype]:
            if e.get("elementid") == id:
                return e
        assert False, f"Id {id} not found in elementtype {elemtype}"

    def getfieldbyid(self, id, elemtype, field="name"):
        elem = self.getelembyid(id=id, elemtype=elemtype)
        retval = elem.get(field)
        if field in ("name", "shortdescr", "description"):
            return self.mlvalue(retval)
        else:
            return retval

    def getcategoryname(self, catgid):
        if catgid is None: return ""  # stop recursion
        catg = self.getelembyid(id=catgid, elemtype="Categories")
        retval = self.fullescapestr(self.mlvalue(catg.get("name")))
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
        langs = set(self.languages).difference({self.mainlang})
        retval = dict()
        for lang in langs:
            for fname in fields:
                if fname not in elem: continue
                retval[f"{self.MULTILANGADDPROPS[fname]}:{lang}"] = self.mlvalue(value=elem.get(fname), lang=lang,
                                                                                 default=default)
        return retval

    def extractadditionalprops(self,element,props):
        """

        @param element: structure to transform
        @param props: list of names in element to transform to language props
        @return:
            additional propierties, language transformed if applicable, pure otherwise
        """
        additionalprops = element.get("additionalProps", dict())
        additionalprops.update(self.mlvalues(*props, elem=element, default=False))
        retval=dict()
        for aps, val in additionalprops.items():
            #translate the props into ds-keywords
            if aps.upper().startswith("NAME:"):
                retval["Label:" + aps[len("NAME:"):]] = val
            elif aps.upper().startswith("DESCRIPTION:"):
                retval["Description:" + aps[len("DESCRIPTION:"):]] = val
            elif aps.upper().startswith("TITLE:"):
                retval["Title:" + aps[len("TITLE:"):]] = val
            elif aps.upper().startswith("SHORTDESCR:"):
                retval["Title:" + aps[len("SHORTDESCR:"):]] = val
            else:
                retval[aps]=val
        return retval

    def categories(self, catgtype, catglist=None) -> list:
        categories = self.jsonschemamodel["Categories"]
        retval = []
        for catg in categories:
            if catg.get("categorytype") != catgtype: continue
            if catglist is not None and catg.get("elementid") not in catglist: continue

            catgname = self.escapestr(self.mlvalue(catg.get("name")))
            additionalprops=self.extractadditionalprops(element=catg,
                                                        props=["name","description"])

            retval.append(self.fillstruct(elementtype="Collection",
                                          label=catgname,
                                          # TODO nur doppelte werden ergänzt um Postfix d.h. Toplevel die entitäten sind oder lowlevel die Entitäten mit gleichem Namen in sich haben
                                          description=self.escapestr(self.mlvalue(catg.get("description",""))),
                                          inCollection=self.getcategoryname(catgid=catg.get("parent")),
                                          favorite=False,
                                          additionalProps=additionalprops
                                          ))
        return retval

    def getentikeys(self,enti):
        retval=[]
        keys= enti.get("keys")
        if keys is None:
            return retval
        else:
            keyelems=set(elem for sublist in keys for elem in sublist)
            retval=list(keyelems)
        return retval

    def relations(self, modeltype):
        relas = self.jsonschemamodel.get("Relations",[])
        retval = []
        for rela in relas:
            relamult12 = self._multiplicity(card=rela["fwd"].get("cardinality"), mand=rela["fwd"].get("mandatory"))
            assoc12 = self.mlvalue(rela["fwd"].get("assoctext"))
            assoc12 = "is" if nvl(assoc12) == "" else assoc12.strip()
            arc_12=rela["fwd"].get("arcnumber")
            rangeobj = self.getelembyid(id=rela["fwd"].get("entityid"), elemtype="Entities") if modeltype == "IM" \
                else self.getelembyid(id=rela["fwd"].get("tableid"), elemtype="Tables")

            relamult21 = self._multiplicity(card=rela["bwd"].get("cardinality"), mand=rela["bwd"].get("mandatory"))
            assoc21 = self.mlvalue(rela["bwd"].get("assoctext"))
            assoc21 = "is" if nvl(assoc21) == "" else assoc21.strip()
            arc_21=rela["bwd"].get("arcnumber")
            domainobj = self.getelembyid(id=rela["bwd"].get("entityid"), elemtype="Entities") if modeltype == "IM" \
                else self.getelembyid(id=rela["bwd"].get("tableid"), elemtype="Tables")

            """ define the direction of the relationship in dataspot
                1->M  1 ist first (domainid) direction RANGE
                M->M  arbitrary direction BOTH  
                1->1  the one with an arc is first direction RANGE
                1->1  arbitrary if no arc direction NONE
                """
            if "*" in relamult12 and "*" in relamult21:
                navigable="BOTH"
            elif "*" in relamult12:
                navigable = "RANGE"
                domainobj,relamult12, assoc12, arc_12,rangeobj,relamult21, assoc21, arc_21 = rangeobj,relamult21, assoc21, arc_21,domainobj,relamult12, assoc12, arc_12
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
            elif relamult12 == "1" :
                navigable = "RANGE"
                relamult12, assoc12, arc_12,relamult21, assoc21, arc_21 = relamult21, assoc21, arc_21,relamult12, assoc12, arc_12
            elif relamult21 =="1":
                navigable = "RANGE"
            else:
                navigable = "NONE"

            temporal=rela["bwd"].get("historicised") or rela["fwd"].get("historicised")
            identifying = rela.get("elementid") in self.getentikeys(enti=rangeobj) or \
                          rela.get("elementid") in self.getentikeys(enti=domainobj)
            multilangassoc = {f"Label:{key[-2:]}": val for key, val in
                              self.mlvalues("assoctext", elem=rela["bwd"], default=False).items()}
            multilangassoc.update({f"Reversedname:{key[-2:]}": val for key, val in
                                   self.mlvalues("assoctext", elem=rela["fwd"], default=False).items()})

            additionalprops = rela.get("additionalProps", dict())
            additionalprops.update(multilangassoc)
            destinationtype = "UmlAssociation" if modeltype == "DM" else "Relationship"
            retval.append(self.fillstruct(elementtype=destinationtype,
                                          hasDomain=self.tableref(catgid=domainobj.get('categoryid'),
                                                                  tablename=self.mlvalue(domainobj.get("name"))),
                                          name=assoc21,
                                          domainMultiplicity=relamult12,
                                          hasRange=self.tableref(catgid=rangeobj.get('categoryid'),
                                                                 tablename=self.mlvalue(rangeobj.get("name"))),
                                          inverseName=assoc12,
                                          rangeMultiplicity=relamult21,
                                          identifying=identifying,
                                          navigable=navigable,
                                          temporal=temporal,
                                          ARC_12=arc_21, #verkehrte Welt
                                          ARC_21=arc_12, #verkehrte Welt
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
                or {"domainid": "DOMAxxx",
                    "modelname": "yyyyy"
                }
        @return: domainrange for dataspot
        """
        if domainid is None: return None
        if type(domainid)==dict:
            modelname=domainid.get("modelname", self.imname)
            domaid=domainid.get("domainid")
        else:
            modelname=self.imname
            domaid = domainid
        if modelname == self.imname:
            doma = self.getelembyid(domaid, "Domains")
            if doma.get("domaintype") == "LOVDomain":
                modelname = self.refdomainsname
            else:
                modelname = self.domainsname
        else:
            assert False,"woher weiss ich den Namen des domains bei fremden Modellen"

        return f"/{modelname}/{self.mlvalue(doma.get('name'))}"

    def attrlist(self, parentobj: dict) -> list:
        # TODO add ranges
        attributes=[a for a in self.jsonschemamodel.get("Attributes",[]) if a.get("parentid")==parentobj.get("elementid")]
        entiref = self.fullescapestr(self.mlvalue(parentobj.get("name")))
        attrtype = "BusinessAttribute" if parentobj.get("elementid").startswith("ENTI") else "DataAttribute"
        retval = []
        for attr in attributes:
            additionalprops = self.extractadditionalprops(element=attr,
                                                          props=["name", "description", "shortdescr"])
            retval.append(self.fillstruct(elementtype=attrtype,
                                          hasDomain=entiref,
                                          label=self.escapestr(self.mlvalue(attr.get("name"))),
                                          title=self.escapestr(self.mlvalue(attr.get("shortdescr"))),
                                          description=self.escapestr(self.mlvalue(attr.get("description"))),
                                          favorite=attr.get("descriptive"),
                                          hasRange=self.domainrange(attr.get("domainid")),
                                          examples=attr.get("examples"),
                                          required="MANDATORY" if attr.get("mandatory") else "OPTIONAL",
                                          cardinality="MANY" if attr.get("repeated") else "ONE",
                                          temporal=attr.get("historicised"),
                                          order=attr.get("displayseq"),
                                          additionalProps=additionalprops
                                          ))
        return retval

    def path(self, catgid):
        if catgid is None: return None
        catg = self.getelembyid(id=catgid, elemtype="Categories")  # self.jsonschemamodel["Categories"].get(catgid)
        retval = None
        if catg is not None:
            if catg.get("parent") is None:
                retval = self.fullescapestr(self.mlvalue(value=catg.get("name")))
            else:
                retval = self.getcategoryname(catg.get("parent")) + \
                         "/" + self.fullescapestr(self.mlvalue(value=catg.get("name")))
        return retval

    def tableref(self, catgid, tablename):
        return f"{nvl(self.path(catgid), self.DUMMYCOLLECTION)}/{self.fullescapestr(tablename)}"

    def columnlist(self, table: dict) -> list:
        # TODO add ranges

        if table.get('name') in ("PPH_CCGLT_MTLS", "PPH_MLGT", "PPH_MARD", "PPH_MAT_STEP",
                                 "PPH_MAT_R3", "PPH_CCGLT_MTLV",
                                 "Shopspezifische Marketingangaben [lumimart.ch]"):
            return []  # TODO special cases

        # TODO mit Vater dazu
        donecolunames = []

        colulist = table.get("columns", [])
        retval = []
        for colu in colulist:
            additionalprops = colu.get("additionalProps", dict())
            # additionalprops.update(self.mlvalues("name", "description", "shortdescr",
            #                                     elem=attr, default=False))
            coluname = self.makeunique(name=self.escapestr(colu.get("name")),
                                       donenames=donecolunames)
            donecolunames.append(coluname)
            retval.append(self.fillstruct(elementtype="UmlAttribute",
                                          hasDomain=self.tableref(catgid=table.get('categoryid'),
                                                                  tablename=table.get('name')),
                                          label=coluname,
                                          title=self.escapestr(colu.get("shortdescr")),
                                          favorite=colu.get("descriptive"),
                                          hasRange=self.domainrange(colu.get("domainid")),
                                          examples=colu.get("examples"),
                                          required="MANDATORY" if colu.get("mandatory") else "OPTIONAL",
                                          cardinality="MANY" if colu.get("repeated") else "ONE",
                                          temporal=colu.get("historicised"),
                                          order=colu.get("displayseq"),
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

    def collectionfullname(self, catgid):
        if catgid is None:
            collpath = self.DUMMYCOLLECTION
        else:
            collectionname = self.getcategoryname(catgid=catgid)
        return collpath

    def entitylist(self) -> list:
        # TODO resolve subcategories, requiring a parent categoriy as reference
        entities = self.jsonschemamodel.get("Entities",[])
        doneentitynames = []
        retval = []
        for enti in entities:
            additionalprops = self.extractadditionalprops(element=enti,
                                                          props=["name", "description", "shortdescr"])
            self.entineeddummycatg = self.entineeddummycatg or enti.get("categoryid") is None
            entityname = self.makeunique(name=self.escapestr(self.mlvalue(enti.get("name"))),
                                         donenames=doneentitynames)

            #make sure name is not also used as category for entities
            catgs=self.jsonschemamodel.get("Categories")
            if entityname in [self.mlvalue(elem.get("name")) for elem in catgs if elem.get("categorytype")== "ENTITY"]:
                entityname += " (business object)"

            doneentitynames.append(entityname)
            retval.append(self.fillstruct(elementtype="BusinessObject",
                                          label=entityname,
                                          title=self.mlvalue(enti.get("shortdescr")),
                                          description=self.escapestr(nvl(self.mlvalue(enti.get("description")))),
                                          examples=enti.get("examples"),
                                          synonyms=[self.mlvalue(e) for e in enti.get("synonyms", [])],
                                          inCollection=self.collectionname(catgid=enti.get("categoryid")),
                                          favorite=False,
                                          additionalProps=additionalprops
                                          ))
            retval += self.attrlist(parentobj=enti)
        return retval

    def lovdomains(self):
        domains = self.jsonschemamodel.get("Domains",[])
        donedomainnames = []
        retval = []
        for idx, doma in enumerate(domains):
            if idx > 10000: break
            if doma.get("domaintype") != "LOVDomain": continue

            self.lovneeddummycatg = self.lovneeddummycatg or doma.get("categoryid") is None
            domainname = self.makeunique(name=self.escapestr(self.mlvalue(doma.get("name"))),
                                         donenames=donedomainnames)
            #make sure name is not also used as category for entities
            catgs=self.jsonschemamodel.get("Categories")
            if domainname in [self.mlvalue(elem.get("name")) for elem in catgs if elem.get("categorytype")== "DOMAIN"]:
                domainname += " (LOV domainid)"

            additionalprops = self.extractadditionalprops(element=doma,props=["name", "description"])
            donedomainnames.append(domainname)

            retval.append(self.fillstruct(elementtype="ReferenceObject",
                                          label=domainname,
                                          description=self.escapestr(nvl(self.mlvalue(doma.get("description")))),
                                          inCollection=self.collectionname(catgid=doma.get("categoryid")),
                                          examples=doma.get("examples"),
                                          additionalProps=additionalprops
                                          )
                          )
            for idx,val in enumerate(doma.get("values", [])):
                retval.append(self.fillstruct(elementtype="ReferenceValue",
                                              favorite=idx <3,
                                              literalOf=self.fullescapestr(
                                                  self.mlvalue(doma.get("name"), lang=self.mainlang)),
                                              timeSeries=[{
                                                  "validFrom": -2208988800000,
                                                  "validTo": 32503593600000,
                                                  "code": val.get("value"),
                                                  "shortText": self.escapestr(self.mlvalue(val.get("displayvalue"))),
                                                  "longText": self.escapestr(self.mlvalue(val.get("description")))
                                              }
                                              ]
                                              )
                              )

        return retval

    @staticmethod
    def toint(val):
        return None if val is None else int(val)

    def domainlist(self) -> list:
        domains = self.jsonschemamodel.get("Domains",[])
        donedomainnames = []
        retval = []
        for doma in domains:
            if doma.get("domaintype") == "LOVDomain": continue
            additionalprops = self.extractadditionalprops(element=doma,props=["name", "description"])

            self.domaneeddummycatg = self.domaneeddummycatg or doma.get("categoryid") is None
            domainname = self.makeunique(name=self.escapestr(self.mlvalue(doma.get("name"))),
                                         donenames=donedomainnames)
            #make sure name is not also used as category for domains
            catgs=self.jsonschemamodel.get("Categories")
            if domainname in [self.mlvalue(elem.get("name")) for elem in catgs if elem.get("categorytype")== "DOMAIN"]:
                domainname += " (domainid)"
            donedomainnames.append(domainname)
            domain = {"elementtype": "DataDomain",
                      "label": domainname,
                      # "title":doma.get("name"),
                      "description": self.escapestr(nvl(self.mlvalue(doma.get("description")))),
                      "inCollection": self.collectionname(catgid=doma.get("categoryid")),
                      "examples": doma.get("examples"),
                      "additionalProps": additionalprops
                      }
            if doma.get("domaintype") == "TextDomain":
                domain["pattern"] = doma.get("syntaxrule")
                domain["baseType"] = "STRING"
                domain["minLength"] = doma.get("minlength")
                domain["maxLength"] = doma.get("maxlength")
            elif doma.get("domaintype") == "NumericDomain":
                domain["minInclusive"] = doma.get("minvalue")
                domain["maxInclusive"] = doma.get("maxvalue")
                domain["integerDigits"] = None if doma.get("totaldigits") is None \
                    else (self.toint(doma.get("totaldigits"))
                          - nvl(self.toint(doma.get("fractdigits")), 0))
                domain["fractionDigits"] = self.toint(doma.get("fractdigits"))
                # domainid["roundvalue"]=
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
        systems = self.jsonschemamodel.get("Systems", [])
        donenames = []
        retval = []
        for syst in systems:
            self.domaneeddummycatg = self.domaneeddummycatg or syst.get("categoryid") is None
            systname = self.makeunique(name=self.escapestr(syst.get("name")),
                                         donenames=donenames)
            # make sure name is not also used as category for domains
            catgs = self.jsonschemamodel.get("Categories")
            if systname in [self.mlvalue(elem.get("name")) for elem in catgs if
                              elem.get("categorytype") == "SYSTEM"]:
                systname += " (system)"
            donenames.append(systname)
            system = {"elementtype": "System",
                      "label": systname,
                      "title":None,
                      "description": self.escapestr(nvl(self.mlvalue(syst.get("description"))))
                      }
            if syst.get("categoryid") is not None:
                system["inCollection"]= self.collectionname(catgid=syst.get("categoryid"))
            if syst.get("parent") is not None:
                system["subsystemOf"]= self.systemname(systid=syst.get("parent"))
            retval.append(self.fillstruct(**system))
        return retval

    def dsentityjson(self) -> list:
        """create from a standardjson a dataspot load-json"""
        retval = list()
        retval += self.entitylist()
        if len(retval)>0:
            retval += self.categories(catgtype="ENTITY")
            retval.append(self.fillstruct(elementtype="Collection",
                                      label=self.DUMMYCOLLECTION,
                                      description="REPLACE BY PROPER collection"
                                      ))

            retval += self.relations(modeltype="IM")
            if not self.entineeddummycatg:
                retval = [d for d in retval if not (d['_type'] == "Collection" and d["label"]) == self.DUMMYCOLLECTION]
        return retval

    def getusedcategories(self, withparents=True):
        return [doma.get("elementid")
                for doma in self.jsonschemamodel["Domains"]
                if doma.get("domaintype") == "Domain"]

    def getmycategoryidtree(self, categoryids, withparents=False):
        retval = categoryids
        mycategories=[catg for catg in self.jsonschemamodel["Categories"] if catg.get("elementid")in categoryids]
        #TODO MANY in jsonschema
        parents=[]
        for catg in mycategories:
            if withparents and catg.get("parent") is not None \
                    and catg.get("parent") not in retval+parents:
                parents.extend(self.getmycategoryidtree(categoryids=[catg.get("parent")], withparents=True))
        retval.extend(parents)
        return retval

    def dsreferencejson(self):
        retval = list()
        retval += self.lovdomains()
        if len(retval) > 0:
            refdomains=[doma for doma in self.jsonschemamodel.get("Domains",[]) if doma.get("domaintype")=="LOVDomain"]
            retval+= self.categories(catgtype="DOMAIN",
                                    catglist=self.getmycategoryidtree(categoryids=list(set(d.get("categoryid") for d in refdomains)),
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
            domains=[doma for doma in self.jsonschemamodel.get("Domains",[]) if doma.get("domaintype")!="LOVDomain"]
            for doma in domains:
                retval += self.attrlist(parentobj=doma)

            retval+= self.categories(catgtype="DOMAIN",
                                    catglist=self.getmycategoryidtree(categoryids=list(set(d.get("categoryid") for d in domains)),
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
        if len(retval)>0:
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

    def tablelist(self):
        tables=self.jsonschemamodel.get("Tables", [])
        donetablenames = []
        retval = []
        retval += self.categories(catgtype="DATAOBJECT")
        for tabl in tables:
            additionalprops = tabl.get("additionalProps", dict())

            self.tableneeddummycatg = self.tableneeddummycatg or tabl.get("categoryid") is None
            tablename = self.makeunique(name=self.escapestr(tabl.get("name")),
                                        donenames=donetablenames)
            donetablenames.append(tablename)
            retval.append(self.fillstruct(elementtype="UmlClass",
                                          label=tablename,
                                          title=tabl.get("shortdescr"),
                                          description=self.escapestr(nvl(tabl.get("description"))),
                                          examples=tabl.get("examples"),
                                          synonyms=[e for e in tabl.get("synonyms", [])],
                                          inCollection=self.collectionname(catgid=tabl.get("categoryid")),
                                          favorite=False,
                                          additionalProps=additionalprops
                                          ))
            retval += self.columnlist(table=tabl)
        return retval

    def dsdmjson(self) -> list:
        """create from a standardjson a dataspot load-json"""
        retval = list()
        retval += self.tablelist()
        if len(retval)>0:
            retval += self.categories(catgtype="DATAOBJECT")
            retval.append(self.fillstruct(elementtype="Collection",
                                          label=self.DUMMYCOLLECTION,
                                          description="REPLACE BY PROPER collection"
                                          ))

            retval += self.relations(modeltype="DM")
            if not self.tableneeddummycatg:
                retval = [d for d in retval if not (d['_type'] == "Collection" and d["label"]) == self.DUMMYCOLLECTION]
        return retval

def dumpmodel(outpath,modelname,elements):
    if modelname is not None and len(elements)>0:
        with open(Path(outpath) / f"{modelname}.json", "w") as modelfile:
            json.dump(elements, modelfile, indent=2, ensure_ascii=False)
            print(f'Model {Path(outpath) / f"{modelname}.json"}')

def json2dataspot(injson, outpath,
                  imname=None,
                  dmname=None,
                  refdomainsname="Reference_model",
                  domainsname="Domain_model",
                  systemsname="Systems_model"):
    # hack for the moment
    locimname = imname
    if locimname is None and dmname is None:
        locimname = "Business_data_model"

    if type(injson) == dict:
        jsfile = injson
    else:
        with open(injson) as infile:
            jsfile = json.load(infile)
    dsjson = Json2dataspot(standardjson=jsfile,
                           imname=locimname,
                           refdomainsname=refdomainsname,
                           domainsname=domainsname,
                           systemsname=systemsname)
    print(f"\nFrom file {injson} generated:")
    dumpmodel(outpath=outpath,modelname=imname,elements=dsjson.dsentityjson())
    dumpmodel(outpath=outpath,modelname=domainsname,elements=dsjson.dsdomainjson())
    dumpmodel(outpath=outpath,modelname=refdomainsname,elements=dsjson.dsreferencejson())
    dumpmodel(outpath=outpath,modelname=dmname,elements=dsjson.dsdmjson())
    dumpmodel(outpath=outpath,modelname=systemsname,elements=dsjson.dssystemjson())
    return

if __name__ == '__main__':
    import sys

    json2dataspot(injson=sys.argv[1],
                  outpath=sys.argv[2])
