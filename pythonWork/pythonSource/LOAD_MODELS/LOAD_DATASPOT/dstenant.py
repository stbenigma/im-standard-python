from LOAD_MODELS.LOAD_DATASPOT.dselements import *
from SSOT_db.IM_JSON import *
from SSOT_infra import parameters


class DSTenant(DSIMElement):
    """ contains the model and all its interpreted forms.
        if dsaccess is None, create empty tenant to be filled from files
    """

    def __init__(self, lang, tenantname=None, dsaccess=None):
        self._dsaccess: DSAccess = dsaccess
        self._tenantlang = lang
        assert lang in Parameter.SUPPORTEDLANGUAGES.keys()

        self._mappings = []
        self._rules = []
        self._transformations = []
        self._translations = []
        self._udps = []

        if self._dsaccess is None:
            assert tenantname is not None, f"tenant name must be given"
            super().__init__(source=DSIMElement.FILESOURCE,
                             imelement={"_type": "Tenant",
                                        "id": tenantname,
                                        "tenantName": tenantname,
                                        "label": tenantname
                                        },
                             tenant=tenantname
                             )
        else:
            assert tenantname is None or dsaccess.tenantname is not None, f"no tenant name given"
            self._dsaccess.tenantname = nvl(tenantname, self._dsaccess.tenantname)
            super().__init__(source=DSIMElement.APISOURCE,
                             imelement=self._dsaccess.gettenant(),
                             tenant=None)
        # fi

        self._getmodels()
        self._getcollections()
        self._getrelations()
        self._getentities()
        self._getdomainvalues()
        self._getdomains()
        self._getattributes()
        self._gettables()
        self._getcolumns()
        self._fillarcs()
        self._getrules()
        self._gettranslations()
        self._gettransformations()
        self._getmappings()
        return

    @property
    def lang(self):
        return self._tenantlang

    @property
    def name(self):
        return self.dsstruct.get("tenantName")

    def loadfile(self, filepath, modeltype, modelname=None, modelid=None):
        """loads a json file into my model
            filepath full path of file containing a dataspot export
            modelname = None: use filename as modelname
        """
        with open(filepath, "r") as infile:
            modeljson = json.load(infile)
            infile.close()
        locmodelname = nvl(modelname, Path(filepath).stem)
        model = self.getmodelbyid(modelid=modelid)
        if model is None:
            # now try by modelname
            model = self.getmodelbyname(name=locmodelname)
        if model is None:
            # create a new model
            self._models.append(DSModel(tenant=self, filepath=filepath, tenantid=self.tenantid,
                                        modeltype=modeltype, modelid=modelid, modelname=locmodelname)
                                )
        else:
            # model found, add the file we'll load
            model.addfilepath(filepath)

        self._loadelements(modeljson)
        return

    def getmodelbyname(self, name):
        if nvl(name) == "":
            return None
        else:
            locname = name.strip("\"")  # remove "" escape protection codes
        for elem in self._models:
            if elem.name == locname:
                return elem
        return None

    def getmodelbyid(self, modelid):
        for elem in self.models():
            if elem.elemid == modelid:
                return elem
        return None

    def _returnonlyoneelem(self, elems: list(), name, elemtype, **kwargs):
        if len(elems) == 1:
            return elems[0]
        elif len(elems) == 0:
            return None
        else:
            instr = "".join(f": {arg}={val}" for arg, val in kwargs.items())
            raise Exception(f"{elemtype} name is not uniqe {name} ({instr})")

    def getentityidbyname(self, name, modelid=None, collectionid=None):
        enti = self.getentitybyname(name=name, modelid=modelid, collectionid=collectionid)
        return enti if enti is None else enti.elemid

    def getentitybyname(self, name, modelid=None, collectionid=None):
        if nvl(name) == "":
            return None
        else:
            locname = name.strip("\"")  # remove "" escape protection codes
        return self._returnonlyoneelem(elems=[elem for elem in self._entities
                                              if (modelid is None or elem.modelid == modelid) and
                                              (collectionid is None or elem.parentid == collectionid) and
                                              elem.name == locname
                                              ],
                                       name=locname,
                                       elemtype=DSAccess.BusinessObject,
                                       model=modelid,
                                       collection=collectionid)

    def getdomainbyname(self, name, modelid=None, collectionid=None):
        if nvl(name) == "":
            return None
        else:
            locname = name.strip("\"")  # remove "" escape protection codes
        names = locname.split('/')
        domaname = names[len(names) - 1]
        if collectionid is not None:
            coll = collectionid
        elif len(names) > 1:
            modl = self.getmodelbyname(name=names[len(names) - 2])
            modelid = modl if modl is None else modl.elemid
            coll = None
        else:
            coll = None
        return self._returnonlyoneelem(elems=[elem for elem in self._domains
                                              if (modelid is None or elem.modelid == modelid) and
                                              (coll is None or elem.parentid == coll) and
                                              elem.name == domaname
                                              ],
                                       name=locname,
                                       elemtype="Domain",
                                       model=modelid,
                                       collection=collectionid)

    def getdomainidbyname(self, name, modelid=None, collectionid=None):
        doma = self.getdomainbyname(name=name, modelid=modelid, collectionid=collectionid)
        return doma if doma is None else doma.elemid

    def getmodelbyname(self, name):
        return self._returnonlyoneelem(elems=[elem for elem in self._models
                                              if elem.name == name],
                                       name=name,
                                       elemtype='Model')

    def getcategorybyname(self, name, modelid=None):
        if nvl(name) == "":
            return None
        else:
            locname = name.strip("\"")  # remove "" escape protection codes
        collectionnames = locname.split('/')
        if len(collectionnames) > 0:
            # get last name in Sequence of collections
            lastname = collectionnames[len(collectionnames) - 1].strip('"')
        else:
            lastname = None
        return self._returnonlyoneelem(elems=[elem for elem in self.categories(modelid=modelid)
                                              if (modelid is None or elem.modelid == modelid) and elem.name == lastname
                                              ],
                                       name=locname, elemtype="category",
                                       model=modelid)

    def getitembyid(self, itemid):
        for elem in self.collections():
            if elem.elemid == itemid: return elem
        for elem in self.relations():
            if elem.elemid == itemid: return elem
        for elem in self.entities():
            if elem.elemid == itemid: return elem
        for elem in self.attributes():
            if elem.elemid == itemid: return elem
        for elem in self.arcs():
            if elem.elemid == itemid: return elem
        for elem in self.tables():
            if elem.elemid == itemid: return elem
        for elem in self.columns():
            if elem.elemid == itemid: return elem
        for elem in self.domains():
            if elem.elemid == itemid: return elem
        for elem in self.mappings():
            if elem.elemid == itemid: return elem
        for elem in self.transformations():
            if elem.elemid == itemid: return elem
        for elem in self.rules():
            if elem.elemid == itemid: return elem
        for elem in self.translations():
            if elem.elemid == itemid: return elem
        return None

    def models(self):
        return self._models

    def categories(self, modelid=None):
        retval = [c for c in self.collections(modelid=modelid)
                  if c.stereotype == DSCategory.CATG_STEREOTYPE
                  ]
        return retval

    def collections(self, modelid=None):
        return [c for c in self._collections
                if modelid is None or c.modelid == modelid]

    def entities(self, modelid=None, collectionid=None):
        if collectionid is None:
            entis = [e for e in self._entities
                     if modelid is None or e.modelid == modelid]
        else:
            entis = [enti for enti in self._entities
                     if collectionid is None or collectionid == enti.parentid]
        return entis

    def arcs(self):
        return self._arcs

    def domains(self, modelid=None, collectionid=None):
        if collectionid is None:
            domas = [d for d in self._domains
                     if modelid is None or d.modelid == modelid]
        else:
            domas = [d for d in self._domains
                     if collectionid is None or collectionid == d.parentid]
        return domas

    def domainvalues(self, domaid=None):

        domas = [d for d in self._domvalues
                 if domaid is None or d.parentid == domaid]
        return domas

    def tables(self, modelid=None, collectionid=None):
        if collectionid is None:
            tabls = [d for d in self._tables
                     if modelid is None or d.modelid == modelid]
        else:
            tabls = [d for d in self._tables
                     if collectionid is None or collectionid == d.parentid]
        return tabls

    def attributes(self, entityid=None):
        attrs = [attr for attr in self._attributes
                 if (entityid is None or entityid == attr.parentid)
                 ]
        return attrs

    def columns(self, parentid=None):
        cols = [col for col in self._columns
                if (parentid is None or parentid == col.parentid)
                ]
        return cols

    def mappings(self, mapstoid=None, mapsfromid=None):
        mapngs = [mapng for mapng in self._mappings
                  if (mapstoid is None or mapstoid == mapng.mapstoid) and
                  (mapsfromid is None or mapsfromid == mapng.mapsfromid)
                  ]
        return mapngs

    def rules(self, elemid=None, parentid=None):
        rules = [rule for rule in self._rules
                 if (elemid is None or elemid in (rule.transformfromids + rule.transformtoids)) and
                 (parentid is None or parentid == rule.parentid)
                 ]
        return rules

    def datamodels(self):
        dms = [m for m in self._models
               if m.jsonmodeltype() == DSModel.DMType]
        return dms

    def transformations(self, maptoid=None, mapfromid=None):
        trfms = [trfm for trfm in self._transformations
                 if (maptoid is None or maptoid in trfm.maptoids) and
                 (mapfromid is None or mapfromid in trfm.mapfromids)
                 ]
        return trfms

    def translations(self, mapid=None):
        trnls = [trnl for trnl in self._translations
                 if (mapid is None or mapid in trnl.mappingid)
                 ]
        return trnls

    def relations(self, modelid=None, entiid=None):
        return [r for r in self._relations
                if (modelid is None or modelid == r.modelid) and
                (entiid is None or r["hasDomain"] == entiid or r["hasRange"] == entiid)
                ]

    def _getmodels(self):
        """read all models for tenant"""
        if self.source == DSIMElement.FILESOURCE:
            schms = []
        else:
            schms = self._dsaccess.getschemes()

        elems = [DSModel(model=schm, tenant=self) for schm in schms]
        self._models = elems
        return

    def _getcollections(self):
        """read all collections """
        self._collections = []
        if self.source == DSIMElement.FILESOURCE:
            pass
        else:
            colls = self._dsaccess.getcollections()
            for coll in colls:
                if coll.get("stereotype") == DSCategory.CATG_STEREOTYPE:
                    self._collections.append(DSCategory(tenant=self, catg=coll))
                else:
                    self._collections.append(DSCollection(tenant=self, coll=coll))
        return

    def _getentities(self):
        """read all entities (BusinessObjects) """
        self._entities = []
        if self.source == DSIMElement.FILESOURCE:
            pass
        else:
            busobjs = self._dsaccess.getbusinessobjects()
            for enti in busobjs:
                self._entities.append(DSEntity(enti=enti, tenant=self))
            self._udps.append(DSEntity.udptypes(entis=self._entities))
            self._handlesuperentities()
        return

    def _gettables(self):
        """read all tables (umlobjects) """
        if self.source == DSIMElement.FILESOURCE:
            self_tables = []
        else:
            dstabls = self._dsaccess.gettables()
            self._tables = [DSTable(tabl=tabl, tenant=self) for tabl in dstabls]
            self._udps.append(DSTable.udptypes(tabs=self._tables))
        return

    def _getcolumns(self):
        """read all Columns (umlelements) """
        if self.source == DSIMElement.FILESOURCE:
            self._columns = []
        else:
            dscols = self._dsaccess.getcolumns()
            self._columns = [DSColumn(col=col, tenant=self) for col in dscols]
            self._udps.append(DSColumn.udptypes(cols=self._columns))
        return

    def _getdomains(self, modelid=None):
        """read all domains  DataDomain, ReferenceObject """
        self._domains = []
        if self.source == DSIMElement.FILESOURCE:
            pass
        else:
            for doma in filter (lambda d : d.get("_type") != "UmlEnumeration",
                        self._dsaccess.getenumerations(
                    modelid=modelid)):  # for loops for check of duplicates after every append
                #replaced by filter if doma.get("_type") == "UmlEnumeration": continue  # TODO wollen wir die auch? dann in DSDomain handlen
                self._domains.append(DSDomain(domatype=Domain.LOV, doma=doma,
                                              tenant=self,
                                              values=self.domainvalues(domaid=doma.get("id"))
                                              )
                                     )
            for doma in self._dsaccess.getdatatypes(modelid=modelid):
                self._domains.append(DSDomain(domatype=DSDomain.dstype2spodtype(doma.get("baseType")),
                                              doma=doma,
                                              tenant=self)
                                     )
            if "Unknwon" not in [d.name for d in self._domains]:
                self._domains.append(DSDomain(domatype=Domain.TXT,
                                              doma={"_type": DSAccess.DataDomain,
                                                    "label": "Unknown",
                                                    "id": "Unknown",
                                                    "descr": "Dummy domain to manage NO-Domain"},
                                              tenant=self))
            self._udps.append(DSDomain.udptypes(domas=self._domains))
        # fi

        return

    def _getdomainvalues(self, parent=None):
        if self.source == DSIMElement.FILESOURCE:
            self._domvalues = []
        else:
            self._domvalues = [DSDomainValue(domaval=dsval, tenant=self, parent=parent)
                               for dsval in self._dsaccess.getliterals(enumid=None if parent is None else parent.elemid)
                               ]
        return

    def _gettranslations(self):
        if self.source == DSIMElement.FILESOURCE:
            self._translations = []
        else:
            self._translations = [DSTranslation(trnsl=trnsl, tenant=self)
                                  for trnsl in self._dsaccess.gettranslations()
                                  ]
        return

    def _getmappings(self, modelid=None):
        if self.source == DSIMElement.FILESOURCE:
            self._mappings = []
        else:
            self._mappings = [DSMapping(mapng=dsmap,
                                        tenant=self)
                              for dsmap in self._dsaccess.getmappings(modelid=modelid)
                              ]
        return

    def _getrules(self):
        if self.source == DSIMElement.FILESOURCE:
            self._rules = []
        else:
            self._rules = [DSRule(rule=rule, tenant=self)
                           for rule in self._dsaccess.getrules()
                           ]
        return

    def _gettransformations(self, modelid=None):
        if self.source == DSIMElement.FILESOURCE:
            self._transformations = []
        else:
            self._transformations = [DSTransformation(trnsf=dstrn,
                                                      tenant=self,
                                                      rules=self.rules(parentid=dstrn.get("id"))
                                                      )
                                     for dstrn in self._dsaccess.gettransformations(modelid=modelid)
                                     if self.getitembyid(dstrn.get("transformationOf")) is not None
                                     # get rid of ENUMS mappings inDMs
                                     ]

        return

    def _getattributes(self, modelid=None):
        """read all attributes (BusinessObjects) """
        self._attributes = []
        if self.source == DSIMElement.FILESOURCE:
            pass
        else:
            dsattrs = self._dsaccess.getattributes(modelid=modelid)
            self._attributes = [DSAttribute(attr=attr, tenant=self) for attr in dsattrs]
            self._udps.append(DSAttribute.udptypes(attrs=self._attributes))
        return

    def _getrelations(self, modelid=None):
        """read all relations  """
        self._relations = []
        if self.source == DSIMElement.FILESOURCE:
            pass
        else:
            dsrelas = self._dsaccess.getrelations(modelid=modelid)
            self._relations = [DSRelation(rela=rela, tenant=self) for rela in dsrelas
                               if rela.get("_type") == DSAccess.Relationship
                               ]
            self._udps.append(DSRelation.udptypes(relas=self._relations))

        return

    def _addarc(self, arcno, entiid, relaid):
        if arcno is None:
            return
        arcname = DSArc.arcname(arcno=arcno, entiid=entiid)
        if arcname not in [arc.elemid for arc in self.arcs()]:
            self._arcs.append(DSArc(tenant=self, no=arcno, entiid=entiid,
                                    relations=[relaid],
                                    uc=self.uc, dc=datetime.today()
                                    )
                              )
        else:
            arc = self.getitembyid(arcname)
            arc.relations.append(relaid)
        return

    def _fillarcs(self):
        self._arcs = []
        for rela in self.relations():
            self._addarc(arcno=rela.fromarc, entiid=rela.fromentityid, relaid=rela.elemid)
            self._addarc(arcno=rela.toarc, entiid=rela.toentityid, relaid=rela.elemid)

    def _createsubtyperelation(self, enti):
        """create a ISA-relationship for this sup/subentity
            """
        self._relations.append(DSRelation(rela={"_type": DSAccess.Relationship,
                                                "id": f"RISA-{enti.elemid}-{enti.supertypeid()}",
                                                "label": f"ISA-{enti.name}-{enti.supertypeid()}",
                                                "status": "WORKING",
                                                "stereotype": "one2one",
                                                "identifying": "false",
                                                "name": "is",
                                                "required": "MANDATORY",
                                                "cardinality": "ONE",
                                                "navigable": "RANGE",
                                                "inverseName": "is",
                                                "domainMultiplicity": "1",
                                                "rangeMultiplicity": "1",
                                                "temporal": "false",
                                                "hasDomain": enti.elemid,
                                                "hasRange": enti.supertypeid(),
                                                "customProperties": {
                                                    "ARC": None,
                                                    "BCKWARC": 9,
                                                    "BCKWCARDINALITY": "ONE",
                                                    "BCKWOPTIONALITY": "MANDATORYY",
                                                    "BCKWTEXT": "is"
                                                }
                                                },
                                          tenant=self, uc=enti.uc, dc=enti.dc))
        return

    def _handlesuperentities(self):
        for enti in [e for e in self._entities if e.supertypeid() is not None]:
            self._createsubtyperelation(enti=enti)

    def _loadelements(self, modeljson):
        for elem in modeljson:
            if elem.get("_type") == DSAccess.Collection:
                if elem.get("stereotype") == DSCategory.CATG_STEREOTYPE:
                    self._collections.append(DSCategory(tenant=self, catg=elem, dc=self.dc, uc=self.uc))
                else:
                    self._collections.append(DSCollection(tenant=self, coll=elem, dc=self.dc, uc=self.uc))
            else:
                logging.warning(f"unhandled dataspot object type {elem.get('_type')}")
        return

    def spodjson(self) -> dict:

        jsmodel = dict()
        for key, value in JSModel._elemtype2label.items():
            jsmodel[value] = dict()

        jsmodel["model"] = jsonproject(name=self.name,
                                       modeltype="logical",
                                       language=self._tenantlang,
                                       uc=self.uc, dc=self.dc)

        jsmodel["languages"] = {self._tenantlang: jsonlanguage(isoname=Parameter.SUPPORTEDLANGUAGES[self._tenantlang][0]
                                                               , iso3=Parameter.SUPPORTEDLANGUAGES[self._tenantlang][1],
                                                               modellanguage='de' == self._tenantlang)}
        jsmodel["categories"] = {cat.elemid: cat.spodjson() for cat in self.categories()}
        jsmodel["entities"] = {elem.elemid: elem.spodjson() for elem in self.entities()}
        jsmodel["relations"] = {elem.elemid: elem.spodjson() for elem in self.relations()}
        jsmodel["domains"] = {elem.elemid: elem.spodjson() for elem in self.domains()}
        jsmodel["attributes"] = {elem.elemid: elem.spodjson() for elem in self.attributes()}
        jsmodel["arcs"] = {elem.elemid: elem.spodjson() for elem in self.arcs()}
        jsmodel["tables"] = {elem.elemid: elem.spodjson() for elem in self.tables()}
        jsmodel["columns"] = {elem.elemid: elem.spodjson() for elem in self.columns()}
        jsmodel["datamodels"] = {elem.elemid: elem.spodjson() for elem in self.datamodels()}
        # jsmodel["mappings"] = {elem.elemid: elem.spodjson() for elem in self.mappings()+self.transformations()}
        # simple solution tables are mapped to entities or tables. no complex relationshipts with rules etc.
        jsmodel["diagrams"] = dict()
        jsmodel["_imprint_"] = jsonimprint(dbname="",
                                           created=str(datetime.today()),
                                           modelversion=parameters.expecteddbversion(),
                                           jsonversion=str(parameters.jsonversion()),
                                           hashvalue=None,
                                           gitrevision="0")

        return jsmodel
