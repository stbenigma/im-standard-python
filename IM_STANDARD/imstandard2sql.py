import logging
import re
from datetime import datetime
from pathlib import Path

from IM_STANDARD import nvl, JsonElement, StandardJsonModel, \
    Sql2IMJsonschema, Sql2IMJson,StandardSchema,json2timestamp
from IM_STANDARD.SQL import dbval, SqliteDb, StandardModelDb


class Standardmodel2SQLdatabase():
    """
    takes a standard model json  and creates a sql database script
    """

    MODELTYPESREV = {val: key for key, val in StandardSchema.MODELTYPES.items()}

    def __init__(self, jsonmodel, mydb: StandardModelDb):

        self.jsonmodel = jsonmodel
        self.sqldb = mydb
        self.language = "en"
        self.languages = [self.language]
        self.entitycatgstranslate = {}
        self.entitytranslate = {}
        self.domaintranslate = {}
        self.attributetranslate = {}
        self.relationtranslate = {}

        return

    @property
    def ismultilingual(self):
        return len(self.languages) > 1

    @staticmethod
    def _bool2sql(val: bool) -> str:
        """ returns TRUE or FALSE
            Noe is FALSE
            """
        return None if val is None else "TRUE" if val else "FALSE"

    def _sql2bool(val: str) -> bool:
        """ returns True or False
            """
        return val.uppper in ("TRUE", "T")

    def _getprop(self, struct: dict, name: str, default=None):
        """
        reads a property from the struct
        if not found, tries additionalProps in the struct
        :param struct: structure to read from
        :param name:  name of the property
        :param default: default, if name does not exist
        :return: property found or default
        """
        if name in struct:
            return struct.get(name)
        return struct.get("additionalProps", dict()).get(name, default)

    def _insertmlvalue(self, mlvalue: str, lang, attrname, modeid):
        if attrname is None or modeid is None or lang is None: return
        langid = self.sqldb.lookupvalue(tablename="languages", colname="lang_id",
                                        lang_iso_code2=lang.lower()
                                        )
        self.sqldb.rowinsert(tablename="lang_texts",
                             lgtx_lang_id=langid,
                             lgtx_attrname=attrname,
                             lgtx_mode_id=modeid,
                             lgtx_text=mlvalue)
        return

    def mlvalue(self, struct):
        if type(struct) == str:
            return struct
        elif type(struct) == dict:
            return struct.get(self.language)
        elif struct is None:
            return None
        else:
            return f"??{type(struct)}??"

    def _insertmultilang(self, elem, modeid, mapfields: dict):
        for fieldname, attrname in mapfields.items():
            val = elem.get(fieldname)
            if isinstance(val, str) or val is None:
                continue  # can't be multilingual
            elif isinstance(val, dict):
                for lang, langval in val.items():
                    if langval not in (None, ""):
                        self._insertmlvalue(mlvalue=langval,
                                            modeid=modeid,
                                            attrname=attrname,
                                            lang=lang
                                            )
            else:
                assert False, f"value must be string or dict"
        return

    def _insertudpvs(self, elem, modeid, specialkeys=[]):
        additionalprops = {key: val for key, val in elem.get("additionalProps", dict()).items()
                           if key not in specialkeys}
        for prop, val in additionalprops.items():
            if re.match(".*:[a-z]{2}$", prop): continue  # skip multilang entries
            self.sqldb.rowinsert(tablename="user_defined_props",
                                 udpv_name=prop,
                                 udpv_mode_id=modeid,
                                 udpv_value=val if type(val) is not list else ", ".join(val)
                                 )
        return

    def _insertexpls(self, expls: list, modeid: int):
        for expl in expls:
            self.sqldb.rowinsert(tablename="examples",
                                 expl_value=expl,
                                 expl_mode_id=modeid)

    def generatebusinessmodel(self):
        self.generateentities()
        self.generateattributes()
        self.generaterelations()
        self.generatekeys()
        self.generatebusinessrules()
        return

    def generatekeys(self):
        """ get all keys from attributes and relations and fill the entities keys property
            assume attributes and relationships are already done"""

        entities = self.jsonmodel.get("Entities", list())

        for enti in entities:
            keys = enti.get("keys", dict())
            keys = {idx: [key for key in idxkeys] for idx, idxkeys in enumerate(enti.get("keys", list()), start=1)}
            for keynum, keyelems in keys.items():
                for key in keyelems:
                    attrid = self.attributetranslate.get(key)
                    relaid = self.relationtranslate.get(key)

                    self.sqldb.rowinsert(tablename="keys",
                                         keys_name=f"{str(keynum)}",
                                         keys_enti_id=self.entitytranslate[enti.get("elementId")],
                                         keys_attr_id=attrid,
                                         keys_rela_id=relaid
                                         )

        return

    def entityjson(self, element):
        additionalprops = self.additionalprops(elem=element,
                                               specialkeys=["subtypeOf"])
        # for dataspot mark entites as favorites
        additionalprops["favorite"] = element.get("favorite")
        additionalprops["SOURCE-HREF"] = self.dsmodels.sourcehref(element)
        elementi = JsonElement().entityjson(elementId=element.get("ID"),
                                            name=self.mutlilangvalue(fieldname="label",
                                                                     value=self._deref(element.get("label")),
                                                                     addprops=additionalprops),
                                            categoryId=self.findelementid(elems=self.dsmodels.categories,
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
                                            shortDescr=self.mutlilangvalue(fieldname="title",
                                                                           value=self._deref(
                                                                               element.get("title")),
                                                                           addprops=additionalprops),
                                            examples=element.get("examples"),
                                            additionalProps=additionalprops
                                            )
        # attributes and keys are added later
        return elementi

    def generateentities(self):

        entities = [enti for enti in self.jsonmodel.get("Entities", list())]
        tablename = "entities"
        for enti in entities:
            modeid = self.sqldb.rowinsert(tablename="modelelements",
                                          mode_type="ENTI",
                                          mode_modl_id=self.model_id,
                                          mode_dc=self._getprop(struct=enti, name="dc", default=self.now),
                                          mode_uc=self._getprop(struct=enti, name="uc", default="loadedfromjson")
                                          )

            try:
                entiname = self.mlvalue(enti.get("name"))
                self.sqldb.rowinsert(tablename=tablename,
                                     enti_id=modeid,
                                     enti_name=entiname,
                                     enti_descr=self.mlvalue(enti.get("description")),
                                     enti_short_name=enti.get("shortName"),
                                     enti_tooltip=self.mlvalue(enti.get("title")),
                                     enti_enca_id=self.entitycatgstranslate[enti.get("categoryId")],
                                     enti_prefix=None
                                     )
            except  SqliteDb.UK_VIOLATED as nd:
                logging.error(f"Duplicate entity name {entiname} in {enti.get('FULLPATH')}.")
                entiname = f"{enti.get('FULLPATH')}"
                self.sqldb.rowinsert(tablename=tablename,
                                     enti_id=modeid,
                                     enti_name=entiname,
                                     enti_descr=self.mlvalue(enti.get("description")),
                                     enti_short_name=enti.get("shortName"),
                                     enti_tooltip=self.mlvalue(enti.get("shortDescr")),
                                     enti_enca_id=self.entitycatgstranslate[enti.get("categoryId")],
                                     enti_prefix=None
                                     )
            except KeyError as e:
                raise KeyError(f"entity '{entiname}': parent not found in categories '{enti.get('categoryId')}'")

            self.entitytranslate[enti.get("elementId")] = modeid
            self._insertmultilang(elem=enti,
                                  modeid=modeid,
                                  mapfields={"name": "enti_name",
                                             "description": "enti_descr",
                                             "shortDescr": "enti_tooltip"}
                                  )
            self._insertudpvs(elem=enti, modeid=modeid)

            self._insertexpls(expls=enti.get("examples", []), modeid=modeid)

            for syno in enti.get("synonyms", []):
                self.sqldb.rowinsert(tablename="synonyms",
                                     syno_name=syno,
                                     syno_enti_id=modeid)

        # for enti in entities.values():
        #     if enti.get("subtypeOf") is None: continue
        #     entiid = self.entitytranslate[enti.get("label")]  # TODO doppelte FullpathNamen siehe oben
        #     entiidsup = self.entitytranslate[enti.get("subtypeOf")]  # TODO doppelte FullpathNamen siehe oben
        #     sql = """update entities set enti_superenti_id =:enti_superenti_id
        #              where enti_id = :enti_id
        #              """
        #     self.sqldb.execsql(sql=sql, enti_id=entiid, enti_superenti_id=entiidsup)

        # TODO add relation
        # self.standardjson.addelementinstance \
        #     (name="Relations",
        #      val=self.relationjsonbase(relationtype="SUBTYPE",
        #                                entityid1=entityid1,
        #                                entityid2=element.get("ID"),
        #                                element={
        #                                    "hasDomain": element.get(
        #                                        "subtypeOf"),
        #                                    "name": self.standardjson.multilangstring_is(),
        #                                    "hasRange": element.get("label"),
        #                                    "inverseName": self.standardjson.multilangstring_is(),
        #                                    "domainMultiplicity": "1",
        #                                    "rangeMultiplicity": "1",
        #                                    "ARC-12": None,
        #                                    "ARC-21": 0,
        #                                    "ID": ElementId.nextid("RELA"),
        #                                    "href": self.dsmodels.sourcehref(element)
        #
        #                                }))

        return

    def generaterelations(self, ):
        tablename = "relations"
        for rela in self.jsonmodel.get("Relations", list()):
            modeid = self.sqldb.rowinsert(tablename="modelelements",
                                          mode_type="RELA",
                                          mode_modl_id=self.model_id,
                                          mode_dc=self._getprop(struct=rela, name="dc", default=self.now),
                                          mode_uc=self._getprop(struct=rela, name="uc", default="loadedfromds")
                                          )
            fwd, bwd = rela.get("fwd"), rela.get("bwd")
            self.sqldb.rowinsert(tablename=tablename,
                                 rela_id=modeid,
                                 rela_name=f'{fwd.get("entityId")}->{self.mlvalue(fwd.get("assocText"))}->{bwd.get("entityId")}',
                                 rela_type=rela.get("relationType"),
                                 rela_arc_no_from=fwd.get("arcNumber"),
                                 rela_arc_no_to=bwd.get("arcNumber"),
                                 rela_assoc_from_to=self.mlvalue(fwd.get("assocText")),
                                 rela_assoc_to_from=self.mlvalue(bwd.get("assocText")),
                                 rela_enti_id_from=self.entitytranslate[fwd.get("entityId")],
                                 rela_enti_id_to=self.entitytranslate[bwd.get("entityId")],
                                 rela_hist_from_to=self._bool2sql(fwd.get("historicised")),
                                 rela_hist_to_from=self._bool2sql(bwd.get("historicised")),
                                 rela_mandatory_from_to=self._bool2sql(fwd.get("mandatory")),
                                 rela_mandatory_to_from=self._bool2sql(bwd.get("mandatory")),
                                 rela_maptype_from_to=fwd.get("cardinality"),
                                 rela_maptype_to_from=bwd.get("cardinality")
                                 )

            self.relationtranslate[rela.get("elementId")] = modeid

            self._insertmultilang(elem=fwd,
                                  modeid=modeid,
                                  mapfields={"assocText": "rela_assoc_from_to"}
                                  )
            self._insertmultilang(elem=bwd,
                                  modeid=modeid,
                                  mapfields={"assocText": "rela_assoc_to_from"}
                                  )

            self._insertudpvs(elem=rela, modeid=modeid)

            self._insertexpls(expls=rela.get("examples", []), modeid=modeid)

        return

    def generate1attribute(self, attr, modeid):
        tablename = "attributes"
        parent = attr.get("parentId")
        if parent in self.entitytranslate:
            entiid, grpdomaid = self.entitytranslate[parent], None
        elif parent in self.domaintranslate:
            entiid, grpdomaid = None, self.domaintranslate[parent]
        else:
            assert False, f"Attribute {parent} is neither entity nor domain"

        domaid = self.domaintranslate.get(attr.get("domainId"))

        self.sqldb.rowinsert(tablename=tablename,
                             attr_id=modeid,
                             attr_tech_name=self.mlvalue(attr.get("name")),
                             attr_displ_name=self.mlvalue(attr.get("name")),
                             attr_descr=self.mlvalue(attr.get("description")),
                             attr_tooltip=self.mlvalue(attr.get("tooltip")),
                             attr_enti_id=entiid,
                             attr_doma_id=domaid,
                             attr_doma_group_id=grpdomaid,
                             attr_displ_seq=attr.get("displaySeq"),
                             attr_is_mandatory=self._bool2sql(attr.get("mandatory")),
                             attr_is_encrypted=self._bool2sql(attr.get("encrypted")),
                             attr_is_historicised=self._bool2sql(attr.get("historicised")),
                             attr_is_repeated=self._bool2sql(attr.get("cardinality") == "MANY"),
                             attr_is_translated=self._bool2sql(attr.get("translated")),
                             attr_is_descriptive=self._bool2sql(attr.get("descriptive") == True)
                             )
        self.attributetranslate[attr.get("elementId")] = modeid
        self._insertmultilang(elem=attr,
                              modeid=modeid,
                              mapfields={"name": "attr_displ_name",
                                         "description": "attr_descr",
                                         "tooltip": "attr_tooltip"}
                              )
        self._insertudpvs(elem=attr, modeid=modeid)

        self._insertexpls(expls=attr.get("examples", []), modeid=modeid)

        # elemattr = JsonElement().attributejson(elementId=attr.get("ID"),
        #                                        name=self.mutlilangvalue(fieldname="label",
        #                                                                 value=self._deref(attr.get("label")),
        #                                                                 addprops=additionalprops),
        #                                        mandatory=attr.get("required") == "MANDATORY",
        #                                        #domainid,
        #                                        parentid=parentid,
        #                                        displaySeq=attr.get("order"),
        #                                        description=self.mutlilangvalue(fieldname="description",
        #                                                                        value=self._deref(
        #                                                                            attr.get("description")),
        #                                                                        addprops=additionalprops),
        #                                        shortDescr=self.mutlilangvalue(fieldname="title",
        #                                                                       value=self._deref(
        #                                                                           attr.get("title")),
        #                                                                       addprops=additionalprops),
        #                                        examples=attr.get("examples"),
        #                                        descriptive=attr.get("favorite"),
        #                                        historicised=attr.get("temporal"),
        #                                        repeated=True if attr.get("cardinality") == "MANY" else None,
        #                                        translated=attr.get("MULTILINGUAL"),
        #                                        additionalProps=additionalprops
        #                                        )
        # try:
        #     attrname = attr.get("label")
        #     self.sqldb.rowinsert(tablename=tablename,
        #                          attr_id=modeid,
        #                          attr_name=attrname,
        #                          attr_descr=attr.get("description"),
        #                          attr_tooltip=attr.get("title"),
        #                          attr_enti_id=self.entitycatgstranslate[attr.get("inCollection")]
        #                          )

        return

    def generateattributes(self):
        for attr in self.jsonmodel.get("Attributes", list()):
            modeid = self.sqldb.rowinsert(tablename="modelelements",
                                          mode_type="ATTR",
                                          mode_modl_id=self.model_id,
                                          mode_dc=self._getprop(struct=attr, name="dc", default=self.now),
                                          mode_uc=self._getprop(struct=attr, name="uc", default="loadedfromds")
                                          )

            self.generate1attribute(attr=attr,
                                    modeid=modeid)
        return

    def generatebusinessrules(self):
        tablename = "business_rules"
        burus = self.jsonmodel.get("BusinessRules",list())
        for buru in burus:
            modeid = self.sqldb.rowinsert(tablename="modelelements",
                                          mode_type="BURU",
                                          mode_modl_id=self.model_id,
                                          mode_dc=self._getprop(struct=buru, name="dc", default=self.now),
                                          mode_uc=self._getprop(struct=buru, name="uc", default="loadedfromds")
                                          )
            self.sqldb.rowinsert(tablename=tablename,
                                 buru_id=modeid,
                                 buru_name=buru.get("name"),
                                 buru_descr=buru.get("description"),
                                 buru_rule=buru.get("rule", buru.get("description")),
                                 buru_type=buru.get("type"),
                                 buru_level=buru.get("level")
                                 )
            for refelem in buru.get("restrictedElements",list()):
                elemid=self.entitytranslate.get(refelem)
                if elemid is None:
                    elemid=self.attributetranslate.get(refelem)
                if elemid is None:
                    elemid = self.relationtranslate.get(refelem)
                if elemid is None:
                    elemid = self.domaintranslate.get(refelem)
                if elemid is None:
                    assert False, f"{refelem} is neither  entity nor attribute nore relation"


                self.sqldb.rowinsert(tablename="businessrule_elements",
                                 bure_buru_id=modeid,
                                 bure_mode_id=elemid
                                 )

        return

    def _diagusage(self, elems):
        usages = []
        for elem in elems:
            sourcepath = self.addmodeltonamedreference(namedref=elem.get("usageOf"),
                                                       modelname=elem.get("DSMODEL"))

            sourceElement = self.findqualielement(fullpath=sourcepath)
            if sourceElement is None:
                sourceElementid = sourcepath
            else:
                sourceElementid = sourceElement.getid()
            usages.append(sourceElementid)
        return usages

    def generatediagrams(self, status=None):
        """ read all transformations and add them to the element
        """
        for diagkey, diag, in self.dsmodels.diagrams.items():
            if not self.checkstatus(diag, status): continue
            additionalprops = self.additionalprops(elem=diag,
                                                   specialkeys=[])
            elems = [r for r in self.dsmodels.diagelements.values() if r.get("usedBy") == diag.get("label")]
            self.standardjson.addelementinstance(name="Diagrams",
                                                 val=JsonElement().diagramjson(elementId=diag.get("ID"),
                                                                               name=diag.get("label"),
                                                                               # position=dict()=,
                                                                               # size=,
                                                                               elements=self._diagusage(elems),
                                                                               additionalProps=additionalprops))
        return

    def valuemappings(self, rules):
        retval = [[rule.get("translatesFrom"), rule.get("translatesTo")] for rule in rules]
        return retval

    def generatemappings(self, status=None):
        """ read all mappings and add them to the element
        """
        for mapkey, mapping, in self.dsmodels.mappings.items():
            if not self.checkstatus(mapping, status): continue
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
                sourceElementid = mapping.get("derivedFrom")
            else:
                sourceElementid = sourcedomain.getid()

            additionalprops = self.additionalprops(elem=mapping,
                                                   specialkeys=["mapsTo",
                                                                "mapsFrom"
                                                                ])

            self.standardjson.addelementinstance(name="Mappings",
                                                 val=JsonElement().mappingjson
                                                 (derivationType=mapping.get("qualifier"),
                                                  targetdomain=targetdomain.getid(),
                                                  sourcedomain=sourceElementid,
                                                  valuemappings=self.valuemappings
                                                  (rules=[r for r in self.dsmodels.translations.values()
                                                          if r.get('translationIn') == mapping.get("label")]),
                                                  additionalProps=additionalprops
                                                  )
                                                 )

        return

    def _inserttotalcategory(self, catg: dict, tablename: str, categoryId: int = None):
        # assert self._modpk(catg.get("elementId")) in \
        #        [mi[0] for mi in self.sqldb.select(sql="select mode_id from modelelements",
        #                                                            aslist=True)]:

        modeid = self.sqldb.rowinsert(tablename="modelelements",
                                      mode_type="ECAT",
                                      mode_modl_id=self.model_id,
                                      mode_dc=json2timestamp(catg.get("dateCreated", self.now)),
                                      mode_uc=catg.get("createdBy", "loadfromjson"))
        self.entitycatgstranslate[catg.get("elementId")] = modeid
        enca = {"enca_id": modeid,
                "enca_name": self.mlvalue(catg.get("name")),
                "enca_descr": self.mlvalue(nvl(catg.get("description"), catg.get("title"))),
                "enca_enca_id": categoryId
                }
        self.sqldb.rowinsert(tablename=tablename, **enca)
        self._insertmultilang(elem=catg,
                              modeid=modeid,
                              mapfields={"name": "enca_name",
                                         "description": "enca_descr",
                                         "title": None}
                              )
        self._insertudpvs(elem=catg, modeid=modeid)
        return modeid

    def generatecategories(self, catgtype: str):
        def _levelcatgs(parent):
            for catg in [catg for catg in self.jsonmodel.get("Categories", list())
                         if catg.get("categoryType") == catgtype and
                            catg.get("categoryId") == parent]:
                catgid = self._inserttotalcategory(catg=catg, tablename=tablename,
                                                   categoryId=(None if parent is None \
                                                                   else self.entitycatgstranslate[parent])
                                                   )
                _levelcatgs(parent=catg.get("elementId"))
            return

        tablename = "entity_categories" if catgtype == "ENTITY" \
            else "domain_categories" if catgtype == "DOMAIN" \
            else ""

        _levelcatgs(parent=None)

        return

    def generatedomains(self):
        domains = [doma for doma in self.jsonmodel.get("Domains", list())]
        for doma in domains:
            modeid = self.sqldb.rowinsert(tablename="modelelements",
                                          mode_type="DOMA",
                                          mode_modl_id=self.model_id,
                                          mode_dc=self._getprop(struct=doma, name="dc", default=self.now),
                                          mode_uc=self._getprop(struct=doma, name="uc", default="loadfromjson"))
            self.domaintranslate[doma.get("elementId")] = modeid
            values = doma.get("values", list())
            self.generate1domain(doma=doma,
                                 modeid=modeid,
                                 values=values)
        return

    def _dt2sql(self, val: str) -> str:
        dt2sql = {"TextDomain": "TXT",
                  "GroupDomain": "GRP",
                  "LOVDomain": "LOV",
                  "NumericDomain": "NUM",
                  "DatetimeDomain": "DAT",
                  "BinaryDomain": "BIN",
                  "BooleanDomain": "BOO"
                  }
        return dt2sql[val]

    @staticmethod
    def _filldomaproperties(element, subtypeproperties):

        domaintype = Sql2IMJson.DOMATYPESREV[element.get("domainType")]

        subtypeproperties["domainType"] = domaintype
        if domaintype == "TXT":
            subtypeproperties["maxLength"] = element.get("maxLength")
            subtypeproperties["syntaxRule"] = element.get("pattern")
            subtypeproperties["minLength"] = element.get("minLength")
        elif domaintype == "NUM":
            JsonElement.optionalprop(subtypeproperties, "minValue",
                                     element.get("minInclusive"), floatvalue=True)
            JsonElement.optionalprop(subtypeproperties, "maxValue",
                                     element.get("maxInclusive"), floatvalue=True)
            if element.get("integerDigits") is not None or element.get("fractionDigits") is not None:
                subtypeproperties["totalDigits"] = element.get("integerDigits", 0) + element.get("fractionDigits", 0)
            JsonElement.optionalprop(subtypeproperties, "fractDigits", element.get("fractionDigits"),
                                     intvalue=True)
            JsonElement.optionalprop(subtypeproperties, "unit", element.get("Unit"))
        elif domaintype == "GRP":
            pass
        elif domaintype == "DAT":
            subtypeproperties["granularity"] = "MINUTE"
        elif domaintype == "DATE":
            subtypeproperties["granularity"] = "DAY"
        elif domaintype == "TIME":
            subtypeproperties["syntaxRule"] = "^[0-1][0-9]:[0-5][0-9]$"

        return

    def generate1domain(self, doma: dict, modeid: int, values: list):
        tablename = "domains"

        subtypeprops = dict()
        self._filldomaproperties(element=doma,
                                 subtypeproperties=subtypeprops)

        domaname = self.mlvalue(doma.get("name"))
        self.domaintranslate[doma.get("elementId")] = modeid
        try:
            self.sqldb.rowinsert(tablename=tablename,
                                 doma_id=modeid,
                                 doma_name=domaname,
                                 doma_descr=self.mlvalue(doma.get("description")),
                                 doma_type=subtypeprops.get("domainType"),
                                 doma_bin_contenttype=subtypeprops.get("contentType"),
                                 doma_bin_storageformat=subtypeprops.get("storageformat"),
                                 doma_dat_granularity=subtypeprops.get("granularity"),
                                 doma_dat_minvalue=None if subtypeprops.get(
                                     "domainType") != 'DAT' else subtypeprops.get("minValue"),
                                 doma_dat_maxvalue=None if subtypeprops.get(
                                     "domainType") != 'DAT' else subtypeprops.get("maxValue"),
                                 doma_num_fract_digits=subtypeprops.get("fractDigits"),
                                 doma_num_minvalue=None if subtypeprops.get(
                                     "domainType") != 'NUM' else subtypeprops.get("minValue"),
                                 doma_num_maxvalue=None if subtypeprops.get(
                                     "domainType") != 'NUM' else subtypeprops.get("maxValue"),
                                 doma_num_physunit=subtypeprops.get("unit"),
                                 doma_num_round_value=subtypeprops.get("round"),
                                 doma_num_total_digits=subtypeprops.get("totalDigits"),
                                 doma_txt_minlng=subtypeprops.get("minlng"),
                                 doma_txt_maxlng=subtypeprops.get("maxlng"),
                                 doma_txt_syntaxrule=subtypeprops.get("syntaxRule")
                                 )
        except Exception as e:
            pass

        self._insertmultilang(elem=doma,
                              modeid=modeid,
                              mapfields={"name": "doma_name",
                                         "description": "doma_descr"}
                              )
        self._insertudpvs(elem=doma, modeid=modeid, specialkeys=['Unit'])  # exclude from udp

        self._insertexpls(expls=doma.get("examples", []), modeid=modeid)

        for idx, value in enumerate(values, 1):
            shortt = value.get("displayValue")
            if isinstance(shortt, dict): logging.warning(f"multilingual lov value  not handled :{shortt}")
            self.sqldb.rowinsert(tablename="lov_values",
                                 lovv_value=value.get("value"),
                                 lovv_displ=None if shortt in ("", None) else self.mlvalue(shortt),
                                 # lovv_descr=firstval.get("longText"),
                                 lovv_sort_order=idx,
                                 lovv_doma_id=modeid)

        return

    def checkconsistency(self):
        """
        checks additional consistency rules, not modelled in sql
        - translated names must also be unique

        :return: True if check is ok
        """
        uniquemultilangs = ",".join(["'enti_name'", "'enti_prefix'", "'enti_short_name'",
                                     "'buru_name'",
                                     "'lang_iso_code2'", "'lang_iso_code3'", "'lang_iso_name'",
                                     "'doma_name'",
                                     "'modl_name'"
                                     ])
        # TODO handle multicolumn multilang uk
        #       like enca_name, enca_enca_id
        uniquetranslationsql = f"""select lang_id,
                            lang_iso_code2 lang,
                            lgtx_attrname attrname,
                            defaultvalue,
                   count(*)
            from translatedvalues
            where lgtx_attrname in ({uniquemultilangs})
            group by lang_id,lang_iso_code2,lgtx_attrname,defaultvalue
            having count(*) > 1
        """
        multilanguks = self.sqldb.select(sql=uniquetranslationsql)
        for mluk in multilanguks:
            logging.error(
                f"ERROR: translated value not unique: Attribute {mluk.get('attrname')}, value={mluk.get('defaultvalue')}")
        return len(multilanguks) == 0

    def _modpk(self, value):
        if value is None:
            return None
        elif re.match("^[A-Z]{4}[0-9]*$", value):
            typeoffset = {"MODL": 0,
                          "ENTI": 100,
                          "CATG": 2000,
                          "RELA": 3000,
                          "DOMA": 4000,
                          "ATTR": 9000}[value[:4]]
            return int(value[4:]) + typeoffset
        else:
            try:
                return int(value)
            except:
                return value

    def filldatabase(self, ):

        self.now = datetime.now().replace(microsecond=0).isoformat()
        modelinfo = self.jsonmodel.get("ModelInfo")
        self.model_id = self.sqldb.rowinsert(tablename="modelelements",
                                             mode_type="MODL",
                                             mode_id=self._modpk(self._getprop(struct=modelinfo, name="elementId")),
                                             mode_dc=self._getprop(struct=modelinfo, name="dc", default=self.now),
                                             mode_uc=self._getprop(struct=modelinfo, name="uc",
                                                                   default="loadedfromjson")
                                             )

        self.sqldb.rowinsert(tablename="models",
                             modl_name=self._getprop(struct=modelinfo, name="modelName"),
                             modl_targetenvironment=self._getprop(struct=modelinfo, name="targetEnvironment"),
                             modl_type=self.MODELTYPESREV[self._getprop(struct=modelinfo, name="modelType")]
                             # ,modl_version=self._getprop(struct=modelinfo,name="modelVersion")
                             )

        self._insertudpvs(elem=modelinfo,
                          modeid=self.model_id,
                          specialkeys=["uc", "dc"])
        modelversion = self._getprop(struct=modelinfo, name="modelVersion")
        if modelversion not in ("", None):
            self.sqldb.rowinsert(tablename="user_defined_props",
                                 udpv_name="modelVersion",
                                 udpv_mode_id=self.model_id,
                                 udpv_value=modelversion
                                 )

        self.language = self._getprop(struct=modelinfo, name="mainLanguage")
        baselangid = self.sqldb.rowinsert(tablename="languages",
                                          lang_iso_code2=self.language,
                                          lang_is_base_lang=dbval(True)
                                          )

        # make sure the baselanguage is in the set of all languages
        self.languages = self._getprop(struct=modelinfo, name="languages")
        self.languages = list(set(self.languages).union(set([self.language])))
        for lang in self.languages:
            if lang == self.language:
                langid = baselangid
            else:
                langid = self.sqldb.rowinsert(tablename="languages",
                                              lang_iso_code2=lang,
                                              lang_lang_id=baselangid)
            self.sqldb.rowinsert(tablename="model_languages",
                                 mola_lang_id=langid,
                                 mola_modl_id=self.model_id,
                                 mola_mainlanguage=dbval(lang == self.language)
                                 )

        # self.generatecategories(catgtype="DOMAIN",status=status)
        self.generatecategories(catgtype="ENTITY")
        self.generatedomains()
        self.generatebusinessmodel()

        self.checkconsistency()
        return
        self.generatederivations(status=status)
        self.generatemappings(status=status)
        self.generatetransformations(status=status)
        self.generatediagrams(status=status)
        self.generatediagrams(status=status)

        return


def exportIM2sqlstandard(inpath, outpath, modelname=None, modelversion='0.0',
                         targetenv=None,
                         language='en', languages=[],
                         server="https://myserver.io",
                         status=None,
                         withdbexport=True):
    indirec: Path = Path(inpath)
    if Path(outpath).is_dir():
        outjsonfilepath = Path(outpath) / (modelname + ".json")
    else:
        outjsonfilepath = Path(outpath)
    outdbfilepath = outjsonfilepath.with_suffix(".db")
    mydb = StandardModelDb(sqlitedb=SqliteDb(), withsqlmodel=True)
    # db = Dataspot2SQLdatabase(indirec=indirec, mydb=mydb)
    # db.filldatabase(modelname=modelname,
    #               languages=languages, language=language,
    #               )

    if withdbexport:
        mydb.writedbtofile(filepath=outdbfilepath)
        print(f'{outdbfilepath} written')

    sql2json = Sql2IMJsonschema(mydb=mydb)
    bmodel = sql2json.generatejson(status=status)

    StandardJsonModel.dumpjsonfile(path=Path(outjsonfilepath),
                                   struct=bmodel, verbose=True)

    return


if __name__ == '__main__':
    pass
