import copy
import re
from datetime import datetime

from IM_STANDARD import nvl, JsonElement
from IM_STANDARD.SQL.SQL_INFRA import DbDML, dbval
from INTERFACES.DATASPOT.imstandard_dataspot.ds2standardbase import DataspotElements, Dataspot2Jsonbase
from INTERFACES.DATASPOT.imstandard_dataspot.dslib import ds2timestamp

class Dataspot2SQLdatabase():

    """
    extract all elements from the dataspot json exports and create a
    sql database script
    """

    def __init__(self, indirec, mydb: DbDML):

        self.dsmodel = DataspotElements(indirec=indirec)
        self.sqldb = mydb
        self.language = "en"
        self.languages = [self.language]
        self.entitycatgstranslate = {}
        self.entitytranslate = {}
        self.domaintranslate = {}
        self.attributetranslate = {}
        self.relationtranslate = {}

        return

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

    def _insertmultilang(self, elem, modeid, mapfields: dict):
        additionalprops = Dataspot2Jsonbase.additionalprops(elem=elem, specialkeys=[])
        # additionalprops["SOURCE-HREF"] = self.dsmodels.sourcehref(catg)
        for lang in self.languages:
            for prop, val in additionalprops.items():
                propname = prop[:prop.find(":")]
                if prop.endswith(f":{lang}") and propname in mapfields:
                    self._insertmlvalue(mlvalue=val,
                                        modeid=modeid,
                                        attrname=mapfields[propname],
                                        lang=lang
                                        )

    def _insertudpvs(self, elem, modeid):
        additionalprops = Dataspot2Jsonbase.additionalprops(elem=elem, specialkeys=[])
        # additionalprops["SOURCE-HREF"] = self.dsmodels.sourcehref(catg)
        for prop, val in additionalprops.items():
            if re.match(".*:[a-z]{2}$", prop): continue  # skip multilang entries
            self.sqldb.rowinsert(tablename="user_defined_props",
                                 udpv_name=prop,
                                 udpv_mode_id=modeid,
                                 udpv_value=val if type(val) is not list else ", ".join(val)
                                 )
        return

    def _insertexpls(self,expls:list,modeid:int):
        for expl in expls:
            self.sqldb.rowinsert(tablename="examples",
                             expl_value=expl,
                             expl_mode_id=modeid)

    def generatebusinessmodel(self, status=None):
        self.generateentities(status=status)
        self.generateattributes(status=status)
        self.generaterelations(status=status)
        self.generatekeys()
        self.generatebusinessrules(status=status)
        return

    def generatekeys(self):
        """ get all keys from attributes and relations and fill the entities keys property
            assume attributes and relationships are already done"""

        entities = {key: val for key, val in DataspotElements.filterelements(
            element=self.dsmodel.entities).items()
                    if val.get("label") in self.entitytranslate}

        for entikey, enti in entities.items():
            entiname = enti.get("label")
            entiid = self.entitytranslate[entiname]
            attrkeyelements = []
            attrs = [val for key, val in DataspotElements.filterelements(
                element=self.dsmodel.attributes).items()
                     if val.get("hasDomain") == entiname
                     ]
            for attr in attrs:
                if attr.get("identifying"):
                    attrkeyelements.append(self.attributetranslate[f"{entiid}:{attr.get('label')}"])

            # find relationships with keys
            # for rela in self.standardjson.getelementinstances("Relations"):
            #     if ((entiid == rela["fwd"].get("entityid") and rela["fwd"].get("cardinality") == "1")
            #             or (entiid == rela["bwd"].get("entityid") and rela["bwd"].get("cardinality") == "1")):
            #         origrela = self.getelementbyid(elements=self.dsmodels.relationships,
            #                                        elemid=rela.getid())
            #         # generated relations (subtypes) have no original
            #         if origrela is not None and origrela.get("identifying"):
            #             attrkeyelements.append(rela.getid())
            #         # TODO inherited keys (Mond erbt von Begleiter den Key)
            #         # TODO different keys if relationships are in arc

            keynum = 1
            for key in attrkeyelements:
                self.sqldb.rowinsert(tablename="keys",
                                     keys_name=f"{entiname}_{str(keynum)}",
                                     keys_enti_id=entiid,
                                     keys_attr_id=key)

        return

    def entityjson(self, element):
        additionalprops = self.additionalprops(elem=element,
                                               specialkeys=["subtypeOf"])
        # for dataspot mark entites as favorites
        additionalprops["favorite"] = element.get("favorite")
        additionalprops["SOURCE-HREF"] = self.dsmodels.sourcehref(element)
        elementi = JsonElement().entityjson(elementid=element.get("ID"),
                                            name=self.mutlilangvalue(fieldname="label",
                                                                     value=self._deref(element.get("label")),
                                                                     addprops=additionalprops),
                                            categoryid=self.findelementid(elems=self.dsmodels.categories,
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
                                            shortdescr=self.mutlilangvalue(fieldname="title",
                                                                           value=self._deref(
                                                                               element.get("title")),
                                                                           addprops=additionalprops),
                                            examples=element.get("examples"),
                                            additionalProps=additionalprops
                                            )
        # attributes and keys are added later
        return elementi


    def generateentities(self, status: str = None):

        entities = {key: val for key, val in DataspotElements.filterelements(element=self.dsmodel.entities,
                                                                             status=status).items()}
        tablename = "entities"
        for enti in entities.values():
            modeid = self.sqldb.rowinsert(tablename="modelelements",
                                           mode_type="ENTI",
                                          mode_modl_id=self.model_id,
                                          mode_dc=ds2timestamp(enti.get("dateCreated")).isoformat(),
                                           mode_uc=enti.get("createdBy", "loadedfromds"))

            try:
                entiname = enti.get("label")
                self.sqldb.rowinsert(tablename=tablename,
                                     enti_id=modeid,
                                     enti_name=entiname,
                                     enti_descr=enti.get("description"),
                                     enti_short_name=None,
                                     enti_tooltip=enti.get("title"),
                                     enti_enca_id=self.entitycatgstranslate[enti.get("inCollection")],
                                     enti_prefix=None)
            except  DbDML.UK_VIOLATED as nd:
                entiname = f"{enti.get('FULLPATH')}-{enti.get('label')}"
                self.sqldb.rowinsert(tablename=tablename,
                                     enti_id=modeid,
                                     enti_name=entiname,
                                     enti_descr=enti.get("description"),
                                     enti_short_name=None,
                                     enti_tooltip=enti.get("title"),
                                     enti_enca_id=self.entitycatgstranslate[enti.get("inCollection")],
                                     enti_prefix=None)

            self.entitytranslate[entiname] = modeid
            self._insertmultilang(elem=enti,
                                  modeid=modeid,
                                  mapfields={"Label": "enti_name",
                                             "Description": "enti_descr",
                                             "Title": "enti_descr"}
                                  )
            self._insertudpvs(elem=enti, modeid=modeid)

            self._insertexpls(expls=enti.get("examples", []),modeid=modeid)

            for syno in enti.get("synonyms", []):
                self.sqldb.rowinsert(tablename="synonyms",
                                     syno_name=syno,
                                     syno_enti_id=modeid)

        for enti in entities.values():
            if enti.get("subtypeOf") is None: continue
            entiid = self.entitytranslate[enti.get("label")]  # TODO doppelte FullpathNamen siehe oben
            entiidsup = self.entitytranslate[enti.get("subtypeOf")]  # TODO doppelte FullpathNamen siehe oben
            sql = """update entities set enti_superenti_id =:enti_superenti_id
                     where enti_id = :enti_id
                     """
            self.sqldb.execsql(sql=sql, enti_id=entiid, enti_superenti_id=entiidsup)

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

    def generaterelations(self, status: str = None):
        tablename = "relations"
        relas = {'/'.join(key.split('/')[1:]): val for key, val in
                 DataspotElements.filterelements(element=self.dsmodel.relationships,
                                                 status=status).items()}
        for relaname, rela in relas.items():
            modeid = self.sqldb.rowinsert(tablename="modelelements",
                                           mode_type="RELA",
                                          mode_modl_id=self.model_id,
                                          mode_dc=ds2timestamp(rela.get("dateCreated")).isoformat(),
                                           mode_uc=rela.get("createdBy", "loadedfromds"))

            self.sqldb.rowinsert(tablename=tablename,
                                 rela_id=modeid,
                                 rela_name=relaname,
                                 rela_type=Dataspot2Jsonbase._relationtype(element=rela),
                                 rela_arc_no_from=None if rela.get("ARC-12") is None else int(rela.get("ARC-12")),
                                 rela_arc_no_to=None if rela.get("ARC-21") is None else int(rela.get("ARC-21")),
                                 rela_assoc_from_to=rela.get("name"),
                                 rela_assoc_to_from=rela.get("inverseName"),
                                 rela_enti_id_from=self.entitytranslate[rela.get("hasDomain")],
                                 rela_enti_id_to=self.entitytranslate[rela.get("hasRange")],
                                 rela_hist_from_to=self._bool2sql(rela.get("temporal", False)),
                                 rela_hist_to_from='FALSE',
                                 rela_mandatory_from_to=self._bool2sql('0' in rela.get("domainMultiplicity", "")),
                                 rela_mandatory_to_from=self._bool2sql('0' in rela.get("rangeMultiplicity", "")),
                                 rela_maptype_from_to=Dataspot2Jsonbase._cardinality(rela.get("rangeMultiplicity")),
                                 rela_maptype_to_from=Dataspot2Jsonbase._cardinality(rela.get("domainMultiplicity"))
                                 )

            self.relationtranslate[relaname] = modeid

            self._insertmultilang(elem=rela,
                                  modeid=modeid,
                                  mapfields={"name": "rela_assoc_from_to",
                                             "inverseName": "rela_assoc_to_from"}
                                  )

            self._insertudpvs(elem=rela, modeid=modeid)

            self._insertexpls(expls=rela.get("examples", []),modeid=modeid)

        return

    def generate1attribute(self, attr, modeid):
        tablename = "attributes"
        parent = attr.get("hasDomain")
        if parent in self.entitytranslate:
            entiid, grpdomaid = self.entitytranslate[parent], None
        elif parent in self.domaintranslate:
            entiid, grpdomaid = None, self.domaintranslate[parent]
        else:
            assert False, f"{parent} is weder entity noch domain"
        domaref = attr.get("hasRange")
        if domaref is None:
            domaid = None
        else:
            domaid = self.domaintranslate[domaref.split("/")[-1]]
        # additionalprops = self.additionalprops(elem=attr,
        #                                       specialkeys=["order", "cardinality", "required",
        #                                                    "temporal", "MULTILINGUAL", "identifying"])
        # "computation",
        # additionalprops["SOURCE-HREF"] = self.dsmodels.sourcehref(attr)
        self.sqldb.rowinsert(tablename=tablename,
                             attr_id=modeid,
                             attr_tech_name=attr.get("label"),
                             attr_displ_name=attr.get("label"),
                             attr_descr=attr.get("description"),
                             attr_tooltip=attr.get("title"),
                             attr_enti_id=entiid,
                             attr_doma_id=domaid,
                             attr_doma_group_id=grpdomaid,
                             attr_displ_seq=attr.get("order"),
                             attr_is_mandatory=self._bool2sql(attr.get("required") == "MANDATORY"),
                             attr_is_encrypted=self._bool2sql(attr.get("encrypted")),
                             attr_is_historicised=self._bool2sql(attr.get("temporal")),
                             attr_is_repeated=self._bool2sql(attr.get("cardinality") == "MANY"),
                             attr_is_translated=self._bool2sql(attr.get("MULTILANG")),
                             attr_is_descriptive=self._bool2sql(attr.get("favorite")==True)
                             )
        self.attributetranslate[f"{str(entiid if entiid is not None else grpdomaid)}:{attr.get('label')}"] = modeid
        self._insertmultilang(elem=attr,
                              modeid=modeid,
                              mapfields={"Label": "attr_displ_name",
                                         "Description": "attr_descr",
                                         "Title": "attr_tooltip"}
                              )
        self._insertudpvs(elem=attr, modeid=modeid)

        self._insertexpls(expls=attr.get("examples", []), modeid=modeid)

        # elemattr = JsonElement().attributejson(elementid=attr.get("ID"),
        #                                        name=self.mutlilangvalue(fieldname="label",
        #                                                                 value=self._deref(attr.get("label")),
        #                                                                 addprops=additionalprops),
        #                                        mandatory=attr.get("required") == "MANDATORY",
        #                                        #domainid=domainid,
        #                                        parentid=parentid,
        #                                        displayseq=attr.get("order"),
        #                                        description=self.mutlilangvalue(fieldname="description",
        #                                                                        value=self._deref(
        #                                                                            attr.get("description")),
        #                                                                        addprops=additionalprops),
        #                                        shortdescr=self.mutlilangvalue(fieldname="title",
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

    def generateattributes(self, status):
        attributes = {key: val for key, val in DataspotElements.filterelements(element=self.dsmodel.attributes,
                                                                               status=status).items()
                      if val.get("hasDomain") in self.entitytranslate
                      or val.get("hasDomain") in self.domaintranslate}
        for attr in attributes.values():
            modeid = self.sqldb.rowinsert(tablename="modelelements",
                                           mode_type="ATTR",
                                          mode_modl_id=self.model_id,
                                          mode_dc=ds2timestamp(attr.get("dateCreated")).isoformat(),
                                           mode_uc=attr.get("createdBy", "loadedfromds"))

            self.generate1attribute(attr=attr,
                                    modeid=modeid)
        return

    def generatebusinessrules(self, status: str):
        tablename = "business_rules"
        burus = [val for key, val in DataspotElements.filterelements(element=self.dsmodel.businessrules,
                                                                     status=status).items()
                 ]
        for buru in burus:
            modeid = self.sqldb.rowinsert(tablename="modelelements",
                                           mode_type="BURU",
                                          mode_modl_id=self.model_id,
                                          mode_dc=ds2timestamp(buru.get("dateCreated")).isoformat(),
                                           mode_uc=buru.get("createdBy", "loadedfromds"))
            # dereference constraintOn (Master) of busienss rule
            refelem = buru.get("constraintOn").split('/')  # one enti/domain element or enti/domain + attrielement
            if len(refelem) == 1 and refelem[0] in self.entitytranslate:
                elemrefid, level = self.entitytranslate[refelem[0]], "ENTI"
            elif len(refelem) == 1 and refelem[0] in self.domaintranslate:
                elemrefid, level = self.domaintranslate[refelem[0]], "TUPL"
            elif refelem[0] in self.entitytranslate:
                elemrefid = self.attributetranslate[f"{str(self.entitytranslate[refelem[0]])}:{refelem[1]}"]
                level = "ATTR"
            elif refelem[0] in self.domaintranslate:
                elemrefid = self.attributetranslate[f"{str(self.domaintranslate[refelem[0]])}:{refelem[1]}"]
                level = "ATTR"
            else:
                assert False, f"{refelem} is weder entity noch domain noch attribut noch Groupdomain oder relation"

            self.sqldb.rowinsert(tablename=tablename,
                                 buru_id=modeid,
                                 buru_name=buru.get("label"),
                                 buru_descr=buru.get("description"),
                                 buru_rule=buru.get("rule", buru.get("description")),
                                 buru_type="CHECK",
                                 buru_level=level
                                 )
            self.sqldb.rowinsert(tablename="businessrule_elements",
                                 bure_buru_id=modeid,
                                 bure_mode_id=elemrefid
                                 )

        return

    def _diagusage(self, elems):
        usages = []
        for elem in elems:
            sourcepath = self.addmodeltonamedreference(namedref=elem.get("usageOf"),
                                                       modelname=elem.get("DSMODEL"))

            sourceelement = self.findqualielement(fullpath=sourcepath)
            if sourceelement is None:
                sourceelementid = sourcepath
            else:
                sourceelementid = sourceelement.getid()
            usages.append(sourceelementid)
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
                                                 val=JsonElement().diagramjson(elementid=diag.get("ID"),
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
                sourceelementid = mapping.get("derivedFrom")
            else:
                sourceelementid = sourcedomain.getid()

            additionalprops = self.additionalprops(elem=mapping,
                                                   specialkeys=["mapsTo",
                                                                "mapsFrom"
                                                                ])

            self.standardjson.addelementinstance(name="Mappings",
                                                 val=JsonElement().mappingjson
                                                 (derivationtype=mapping.get("qualifier"),
                                                  targetdomain=targetdomain.getid(),
                                                  sourcedomain=sourceelementid,
                                                  valuemappings=self.valuemappings
                                                  (rules=[r for r in self.dsmodels.translations.values()
                                                          if r.get('translationIn') == mapping.get("label")]),
                                                  additionalProps=additionalprops
                                                  )
                                                 )

        return

    def _inserttotalcategory(self, catg: dict, tablename: str, parentid: int = None):
        modeid = self.sqldb.rowinsert(tablename="modelelements",
                                       mode_type="ECAT",
                                      mode_modl_id=self.model_id,
                                       mode_dc=ds2timestamp(catg.get("dateCreated")).isoformat(),
                                       mode_uc=catg.get("createdBy", "loadfromds"))

        enca = {"enca_id": modeid,
                "enca_name": catg.get("label"),
                "enca_descr": nvl(catg.get("description"), catg.get("title"))
                }
        if parentid is not None:
            enca["enca_enca_id"] = parentid

        self.sqldb.rowinsert(tablename=tablename, **enca)
        self._insertmultilang(elem=catg,
                              modeid=modeid,
                              mapfields={"Label": "enca_name",
                                         "Description": "enca_descr",
                                         "Title": None}
                              )
        self._insertudpvs(elem=catg, modeid=modeid)
        return modeid

    def generatecategories(self, catgtype: str, status: str):

        categories = DataspotElements.filterelements(element=self.dsmodel.categories,
                                                     elemtype=catgtype,
                                                     status=status)
        tablename = "entity_categories" if catgtype == "ENTITY" \
            else "domain_categories" if catgtype == "DOMAIN" \
            else ""

        donecatgs = dict()
        newcategories = []
        cnt = 0
        restcatgs = copy.deepcopy(categories)
        while len(restcatgs) > 0:
            cnt += 1
            assert cnt < 30
            todocatgs = list(restcatgs.keys())
            for key in todocatgs:
                catg = restcatgs[key]
                parentname = catg.get("inCollection")
                if parentname is None:
                    modeid = self._inserttotalcategory(catg=catg,
                                                        tablename=tablename)
                    # elementi = JsonElement().entityjson(elementid=element.get("ID"),
                    #                                     name=self.mutlilangvalue(fieldname="label",
                    #                                                              value=self._deref(
                    #                                                                  element.get("label")),
                    #                                                              addprops=additionalprops),
                    #
                    donecatgs[catg.get("label")] = modeid
                    del restcatgs[key]
                else:
                    fullname = parentname + "/" + catg.get("label")
                    if parentname not in restcatgs:  # parent was alredy processed
                        modeid = self._inserttotalcategory(catg=catg, tablename=tablename,
                                                            parentid=donecatgs[parentname])

                        donecatgs[fullname] = modeid
                        del restcatgs[key]
                    else:
                        pass

        return donecatgs

    def generatedomains(self, status):
        domains = {key: val for key, val in DataspotElements.filterelements(element=self.dsmodel.domains,
                                                                            status=status).items()
                   }
        for doma in domains.values():
            modeid = self.sqldb.rowinsert(tablename="modelelements",
                                           mode_type="DOMA",
                                          mode_modl_id=self.model_id,
                                          mode_dc=ds2timestamp(doma.get("dateCreated")).isoformat(),
                                           mode_uc=doma.get("createdBy", "loadedfromds"))

            values = [val for key, val in self.dsmodel.LOVvalues.items()
                      if val["literalOf"] == doma["label"]
                      ]
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

    def generate1domain(self, doma: dict, modeid: int, values: list):
        tablename = "domains"

        subtypeprops = dict()
        Dataspot2Jsonbase._filldomaproperties(element=doma,
                                              subtypeproperties=subtypeprops)
        domaname = doma.get("label")
        self.domaintranslate[domaname] = modeid
        domatype=self._dt2sql(subtypeprops.get("domaintype"))
        self.sqldb.rowinsert(tablename=tablename,
                             doma_id=modeid,
                             doma_name=domaname,
                             doma_descr=doma.get("description"),
                             doma_type=domatype,
                             doma_bin_contenttype=subtypeprops.get("contenttype"),
                             doma_bin_storageformat=subtypeprops.get("storageformat"),
                             doma_dat_granularity=subtypeprops.get("granularity"),
                             doma_dat_minvalue=None if domatype != 'DAT' else subtypeprops.get("minvalue"),
                             doma_dat_maxvalue=None if domatype != 'DAT' else subtypeprops.get("maxvalue"),
                             doma_num_fract_digits=subtypeprops.get("fractdigits"),
                             doma_num_maxvalue=None if domatype != 'NUM' else subtypeprops.get("maxvalue"),
                             doma_num_minvalue=None if domatype != 'NUM' else subtypeprops.get("minvalue"),
                             doma_num_physunit=subtypeprops.get("unit"),
                             doma_num_round_value=subtypeprops.get("round"),
                             doma_num_total_digits=subtypeprops.get("totaldigits"),
                             doma_txt_minlng=subtypeprops.get("minlng"),
                             doma_txt_maxlng=subtypeprops.get("maxlng"),
                             doma_txt_syntaxrule=subtypeprops.get("syntaxrule")
                             )

        self._insertmultilang(elem=doma,
                              modeid=modeid,
                              mapfields={"Label": "doma_name",
                                         "Description": "doma_descr"}
                              )
        self._insertudpvs(elem=doma, modeid=modeid)

        self._insertexpls(expls=doma.get("examples", []),modeid=modeid)

        for idx, value in enumerate(values, 1):
            firstval = value.get("timeSeries")[0]
            shortt = firstval.get("shortText")
            self.sqldb.rowinsert(tablename="lov_values",
                                 lovv_value=firstval.get("code"),
                                 lovv_displ=None if shortt == "" else shortt,
                                 lovv_descr=firstval.get("longText"),
                                 lovv_sort_order=idx,
                                 lovv_doma_id=modeid)

        return

    def filldatabase(self, modelname,
                     modelversion="0.0",
                     targetenv=None,
                     language="en",
                     languages=["en"],
                     status=None):
        assert status in ("PUBL", "GTOP", "ALL", None), "status  must be PUBL, GTOP or ALL"

        now = datetime.now().replace(microsecond=0).isoformat()
        modeltype = "Information model"
        self.model_id = self.sqldb.rowinsert(tablename="modelelements",
                                      mode_type="MODL",
                                      mode_dc=datetime.now().isoformat(),
                                        #       ds2timestamp(enti.get("dateCreated")).isoformat(),
                                        mode_uc = "ich")  # enti.get("createdBy", "loadedfromds"))

        self.sqldb.rowinsert(tablename="models",
                             modl_id=self.model_id,
                             modl_name="Test",
                            modl_type="IM")

        self.language = language
        baselangid = self.sqldb.rowinsert(tablename="languages",
                                      lang_iso_code2=language)

        self.languages = languages
        for lang in languages:
            if lang ==language :
                langid=baselangid
            else:
                langid=self.sqldb.rowinsert(tablename="languages",
                                 lang_iso_code2=lang,
                                 lang_lang_id=baselangid)
            self.sqldb.rowinsert(tablename="model_languages",
                                 mola_lang_id=langid,
                                 mola_modl_id=self.model_id,
                                 mola_mainlanguage=dbval(lang==language)
                                 )


                                          # self.standardjson.setschemaelement(name="ModelInfo",
        #                                    val=JsonElement().modelinfojson(
        #                                        modelname=modelname,
        #                                        modeltype=modeltype,
        #                                        mainlanguage=language,
        #                                        languages=languages,
        #                                        dc=now,
        #                                        modelversion=modelversion,
        #                                        targetenvironment=targetenv,
        #                                        origintool=self.ORIGINTOOL,
        #                                        originuri=None,
        #                                        additionalProps=additionalprops
        #                                    )
        #                                    )

        # self.generatecategories(catgtype="DOMAIN",status=status)
        self.entitycatgstranslate = self.generatecategories(catgtype="ENTITY", status=status)
        self.generatedomains(status=status)
        self.generatebusinessmodel(status=status)
        return
        self.generatederivations(status=status)
        self.generatemappings(status=status)
        self.generatetransformations(status=status)
        self.generatediagrams(status=status)
        self.generatediagrams(status=status)

        return


if __name__ == '__main__':
    pass
