import logging
from copy import deepcopy

from INTERFACES.DATASPOT.dsrequests import *

DATASPOTSRCNAME = "imstandard_dataspot"

def dsstatus2spodstatus(status):
    if status in ["Veröffentlicht", "Published"]:
        return "PUBL"
    elif status in ["Abgenommen", "Accepted"]:
        return "GTOP"
    else:
        """ "In Arbeit", "Working"
            "Abgestimmt", "Submitted"
            "Finalisiert", "Final"
        """
        return "DRAFT"


class DSIMElement():
    FILESOURCE = "FILE"
    APISOURCE = "API"
    baseproperties = {
        "_type": "Collection",
        "id": "38dd379c-19ad-4684-a4a4-d64a1b1c0ca0",
        "href": "/web/foryouandyourcustomers-ch/collections/38dd379c-19ad-4684-a4a4-d64a1b1c0ca0",
        "favorite": "true",
        "status": "WORKING",
        "createdBy": "sberner",
        "dateCreated": 1683899027202,
        "stereotype": "category",
        "label": "Allg. Informationen",
        "title": "Name translated",
        "description": "Fläche eines Gebiets als geo-Information",
        "order": 1,
        "synonyms": [],
        "examples": [],
        "subtypeOf": "198ed59d-3d5e-4639-9571-5c578bc010ba",  # API
        # "subtypeOf" : "Gebiet",#FILEBASED
        "required": "MANDATORY",
        "cardinality": "ONE",
        "identifying": "true",
        "temporal": "true",
        "hasDomain": "Land",  # FILEBASED
        "hasRange": "/<modelname>/ISO-Land",  # FILEBASED
        # "hasDomain": "1233454576", #API
        # "hasRange": "123456658", #API
        "name": "unterteilt",
        # "inCollection" : "Produkte", #FILEBASED   escaped "\"Allg. Informationen\""
        "inCollection": "d350afbe-f97c-4291-b644-77222bf59d4c",  # API
        "customProperties": {},  # API
        "_version": 1,  # API
        "tenantId": "bb3f40af-7831-4f55-b058-f39b8ec03be5",  # API
        "modelId": "d350afbe-f97c-4291-b644-77222bf59d4c",  # API
        "parentId": "189c99d5-6f9b-4047-b455-20ebcefd24ae",  # API
        "db": "foryouandyourcustomers-ch",  # API
        "_links": {}  # API
    }

    def __init__(self, tenant, imelement=dict(), **kwargs):
        self._imelement = imelement
        self._uc = kwargs.get("createdBy")
        self._dc = kwargs.get("dateCreated")
        self._um = None  # not yet found
        self._dm = None  # not yet found
        self._tenant = tenant
        assert self._tenant is not None or self.elemtype == "Tenant"
        self._modelid = kwargs.get("modelid")
        self._parentid = kwargs.get("childid")
        self._source = kwargs.get("source")
        if self._source is None and self._tenant is not None:
            self._source = self._tenant.source
        assert self._source in (self.FILESOURCE, self.APISOURCE), "illegal source given for element \"{source}\""

        return

    def __str__(self):
        return str(f"{type(self)}: {self._imelement}")

    def _sourcedivide(self, filebased, apibased, otherbase=None):
        if self.source == self.FILESOURCE:
            return filebased
        elif self.source == self.APISOURCE:
            return apibased
        else:
            return otherbase

    @property
    def dsstruct(self):
        return self._imelement

    @property
    def source(self):
        return self._source

    @property
    def elemtype(self):
        return self.dsstruct.get("_type")

    @elemtype.setter
    def elemtype(self, val):
        self.dsstruct["_type"] = val
        return

    @property
    def stereotype(self):
        return self.dsstruct.get("stereotype")

    @stereotype.setter
    def stereotype(self, val):
        self.dsstruct["stereotype"] = val
        return

    @property
    def elemid(self):
        return self.dsstruct.get("id")

    @property
    def name(self):
        return self.dsstruct.get("label")

    @name.setter
    def name(self, val):
        self.dsstruct["label"] = val
        return

    @property
    def descr(self):
        return self.dsstruct.get("description")

    @property
    def tooltip(self):
        return self.dsstruct.get("title")

    def examples(self):
        return nvl(self.dsstruct.get("examples"), [])

    def synonyms(self):
        return nvl(self.dsstruct.get("synonyms"), [])

    @property
    def tenantid(self):
        if self.elemtype == "Tenant":
            return None
        tenantid = self.dsstruct.get("tenantId")
        if tenantid is None:
            return self._tenant.elemid
        else:
            return tenantid

    @property
    def parentid(self):
        parentid = self.dsstruct.get("parentId")
        if parentid is None:
            return self._parentid
        else:
            return parentid

    @property
    def parent(self):
        return self._tenant.getitembyid(self.parentid)

    @property
    def schemeid(self):
        return self.dsstruct.get("inScheme")

    @property
    def collectionid(self):
        return self.dsstruct.get("inCollection")

    @property
    def status(self):
        return self.dsstruct.get("status")

    @property
    def modelid(self):
        modelid = self.dsstruct.get("modelId")
        if modelid is None:
            return self._modelid
        else:
            return modelid

    @property
    def title(self):
        return self.dsstruct.get("title")

    @property
    def uc(self):
        return self._uc if self._uc is not None else self.dsstruct.get("createdBy")

    @property
    def um(self):
        return self._um if self._um is not None else self.dsstruct.get("modifiedBy")

    @property
    def dc(self):
        return self._dc if self._dc is not None else self.dsstruct.get("dateCreated")

    @property
    def dm(self):
        return self._dm if self._dm is not None else self.dsstruct.get("modifiedAt")

    def getudp(self, propertyname):
        props = self.dsstruct.get("customProperties")
        return self._sourcedivide(self.dsstruct.get(propertyname),
                                  props if props is None else props.get(propertyname)
                                  )

    def udpvalues(self):
        # dummy
        return dict()

    def _udpvalues(self, spodproperties):
        """ get all name,value pairs of user defined properties for this element
            get all properties and subtract basepropeties and spod-properties
        """
        # TODO first fill in userdefpros in TENANT
        return dict()
        if self.source == self.APISOURCE:
            custprops = nvl(self.dsstruct.get("customProperties"), dict())
            realudp = deepcopy(custprops)
            # remove proper SPOD properties which are handled as normal properties (not in spodproperties)
            for u in list(custprops.keys()):
                if u in spodproperties:
                    del realudp[u]
            return realudp
        if self.source == self.FILESOURCE:
            return {udpname: self.dsstruct.get(udpname) for udpname in spodproperties}

    def spodjson(self):
        retval = dict()
        return retval

    @classmethod
    def _udptypes(cls, elements, udptheme, udpgroup):
        """ returns list of all types (theme, group, name) of user defined properties of all elements."""
        udpnames = set()
        for e in elements:
            udpnames.update(set((e.udpvalues().keys())))
        return {udptheme: {udpgroup: list(udpnames)}}


class DSModel(DSIMElement):
    IMType = "IM"
    DMType = "DM"
    REFType = "REF"
    OTHERType = "UNKWN"

    spodproperties = {
    }

    def __init__(self, tenant, model=None,
                 tenantid=None, modelid=None, modelname=None, modeltype=None,
                 filepath=None, **kwargs):
        self._modelname = None
        self._modeltype = None
        self._filepaths = set()

        if model is None:
            # file models must deliver a tenantid to the init-call
            assert modelname is not None, "missing modelname"
            assert modeltype in DSAccess.KnownModelTypes, f"unknown model type \"{modeltype}\""
            super().__init__(tenant=tenant, modelid=nvl(modelid, modelname), tenantid=tenantid,
                             parentid=tenantid, **kwargs)
            self._modelname = modelname
            self._modeltype = modeltype
            self._filepaths = set((filepath,))
        else:
            # online models have a tenantId
            assert model.get("_type") in DSAccess.KnownModelTypes, f"unknown model type \"{model.get('_type')}\""
            super().__init__(tenant=tenant, imelement=model, parentid=model.get("tenantId"), **kwargs)

        return

    @property
    def filepaths(self):
        return self._filepaths

    def addfilepath(self, filepath):
        self._filepaths.add(filepath)

    def delfilepath(self, filepath):
        self._filepaths.discard(filepath)

    @property
    def name(self):
        return nvl(super().name, self._modelname)

    @property
    def elemtype(self):
        return nvl(super().elemtype, self._modeltype)

    def jsonmodeltype(self):
        if self.elemtype == DSAccess.BusinessDataModel:
            return self.IMType
        if self.elemtype == DSAccess.UmlModel:
            return self.DMType
        if self.elemtype == DSAccess.ReferenceDataModel:
            return self.REFType
        else:
            return self.OTHERType

    def spodjson(self):
        return jsondatamodel(name=self.name, descr=self.descr,
                             uc=self.uc, dc=self.dc,
                             sourceref={DATASPOTSRCNAME: [self.elemid, str(datetime.today())]},
                             tables=[t.elemid for t in self._tenant.tables(modelid=self.elemid)],
                             domains=[d.elemid for d in self._tenant.domains(modelid=self.elemid)]
                             )


class DSCollection(DSIMElement):
    spodproperties = {
    }

    def __init__(self, tenant, coll, **kwargs):
        if "_type" not in coll:
            coll["_type"] = DSAccess.Collection
        super().__init__(tenant=tenant, imelement=coll, **kwargs)
        return

    @property
    def fillcolor(self):
        return None

    def spodjson(self):
        return None

    def udpvalues(self):
        """ getall name,value pairs of user defined properties for this attribute """
        return super()._udpvalues(spodproperties=[])

    @classmethod
    def udptypes(cls, colls):
        """ returns list of all types (theme, group, name) of user defined properties of all collections."""
        return super()._udptypes(elements=colls, udptheme="IM", udpgroup=DSAccess.Collection)


class DSCategory(DSCollection):
    CATG_STEREOTYPE = "category"
    spodproperties = {
        "backgroundColor": "#FF9900"  # API
    }

    def __init__(self, tenant, catg, **kwargs):
        super().__init__(tenant=tenant, coll=catg, **kwargs)
        self._checkandresolveduplicatenames()
        return

    @property
    def fillcolor(self):
        return colorhex(self.getudp("backgroundColor"))

    def _checkandresolveduplicatenames(self):
        twin = self._tenant.getcategorybyname(name=self.name)
        if twin is not None:
            modelname = self._tenant.getmodelbyid(self.modelid).name
            logging.warning(f"duplicate category-name {self.name} in model {modelname}. " + \
                            f" Prefixed with \"{modelname}\"")
            self.name = modelname + "_" + self.name
        return

    def spodjson(self):
        color = self.fillcolor
        if color is not None:
            color = color[1:]  # json does not need leading #
        return jsoncategory(name=self.name,
                            uc=self.uc,
                            dc=self.dc,
                            ui=UIElement(color=color).js())


class DSEntity(DSIMElement):
    """entity baseproperties={
    "synonyms" : [ "Syno" ],
    "examples" : [ "examp", "abcd" ],
    "subtypeOf": "198ed59d-3d5e-4639-9571-5c578bc010ba", #API
    "subtypeOf" : "Gebiet",#FILEBASED
    }"""
    spodproperties = {}

    def __init__(self, tenant, enti, **kwargs):
        if "_type" not in enti:
            enti["_type"] = DSAccess.BusinessObject
        super().__init__(tenant=tenant, imelement=enti, **kwargs)
        self._checkandresolvecategory()
        self._checkandresolveduplicatenames()
        return

    def supertypeid(self):
        return self._sourcedivide(self._tenant.getentityidbyname(name=self.dsstruct.get("subtypeOf")),
                                  self.dsstruct.get("subtypeOf"))

    def _checkandresolvecategory(self):
        # check wether parent collection is category
        self.categoryid = None
        catg: DSCategory = self._tenant.getitembyid(self.parentid)
        if catg is None:
            logging.error(f"collection \"{self.self.parentid}\" does not exist")
        elif catg.stereotype == DSCategory.CATG_STEREOTYPE:
            self.categoryid = catg.elemid
        else:
            logging.warning(f"Entity \"{self.name}\" has collection instead of category \"{catg.name}\"")
        return

    def _checkandresolveduplicatenames(self):
        twin = self._tenant.getentityidbyname(name=self.name)
        if twin is not None:
            modelname = self._tenant.getmodelbyid(self.modelid).name
            logging.warning(f"duplicate entity-name \"{self.name}\" in model \"{modelname}\". " + \
                            f" Prefixed with \"{modelname}\"")
            self.name = modelname + "_" + self.name
        return

    def attributes(self):
        return self._tenant.attributes(parentid=self.elemid)

    def spodjson(self):
        catg = self._tenant.getcategorybyname(name=self.dsstruct.get('inCollection'))
        catgid = self._sourcedivide(catg if catg is None else catg.elemid,
                                    self.categoryid)

        retval = jsonentity(
            name=multilangstring(string=self.name, lang=self._tenant.lang),
            shortname=self.name,
            uc=self.uc, dc=self.dc,
            publstatus=dsstatus2spodstatus(self.status),
            descr=multilangstring(string=self.descr, lang=self._tenant.lang),
            tooltip=multilangstring(string=self.tooltip, lang=self._tenant.lang),
            category=catgid,
            supertypeentity=self.supertypeid(),
            icon=dict(),
            synonyms=[multilangstring(string=s, lang=self._tenant.lang)
                      for s in self.synonyms()],
            examples=[multilangstring(string=s, lang=self._tenant.lang) for s in
                      self.examples()],
            sourceref={DATASPOTSRCNAME: [self.elemid, str(datetime.today())]},
            tablesmapped=[],
            referencedby=[],
            userdefprops=jsonudptheme(theme="IM", group="ENTITIES", values=self.udpvalues())
        )
        return retval

    def udpvalues(self):
        """ getall name,value pairs of user defined properties for this entity """
        return super()._udpvalues(spodproperties=self.spodproperties)

    @classmethod
    def udptypes(cls, entis):
        """ returns list of all types (theme, group, name) of user defined properties of all entities."""
        return super()._udptypes(elements=entis, udptheme="IM", udpgroup=DSAccess.BusinessObject)


class DSAttribute(DSIMElement):
    """attribute baseproperties={
        "synonyms" : [ "Syno" ],
     "examples" : [ "examp", "abcd" ],
        "required": "MANDATORY",
        "cardinality": "ONE",
        "identifying": true
        "temporal": true
        "hasDomain": "Land", #FILEBASED
        "hasRange": "/<modelname>/ISO-Land", #FILEBASED
        #"hasDomain": "1233454576", #API
        #"hasRange": "123456658", #API
    }"""
    spodproperties = {
        "multilingual": "true"
    }

    def __init__(self, tenant, attr, **kwargs):
        if "_type" not in attr:
            attr["_type"] = DSAccess.BusinessAttribute
        super().__init__(tenant=tenant, imelement=attr, **kwargs)
        return

    @property
    def mandatory(self):
        return True if self.dsstruct.get("required") == "OPTIONAL" else False

    @property
    def repeated(self):
        return True if self.dsstruct.get("cardinality") == "MANY" else False

    @property
    def multilingual(self):
        return self.getudp("multilingual")

    @property
    def temporal(self):
        return self.dsstruct.get("temporal")

    @property
    def entityid(self):
        return self._sourcedivide(self._tenant.getentityidbyname(name=self.dsstruct.get("hasDomain")),
                                  self.dsstruct.get("hasDomain"))

    @property
    def domainid(self):
        return self._sourcedivide(self._tenant.getdomainidbyname(name=self.dsstruct.get("hasRange")),
                                  self.dsstruct.get("hasRange"))

    def udpvalues(self):
        """ get all name,value pairs of user defined properties for this attribute """
        return super()._udpvalues(spodproperties=self.spodproperties)

    @classmethod
    def udptypes(cls, attrs):
        """ returns list of all types (theme, group, name) of user defined properties of all attributes."""
        return super()._udptypes(elements=attrs, udptheme="IM", udpgroup=DSAccess.BusinessAttribute)

    def spodjson(self):
        if self.source == self.FILESOURCE:
            pass
        elif self.source == self.APISOURCE:
            pass
        else:
            pass

        retval = jsonattribute(
            name=multilangstring(string=nvl(self.name), lang=self._tenant.lang),
            techname=self.name,
            uc=self.uc, dc=self.dc,
            publstatus=dsstatus2spodstatus(self.status),
            descr=multilangstring(string=self.descr, lang=self._tenant.lang),
            tooltip=multilangstring(string=nvl(self.tooltip), lang=self._tenant.lang),
            examples=[multilangstring(string=s, lang=self._tenant.lang)
                      for s in self.examples()],
            seq=self.dsstruct.get("order"),
            entity=self.entityid,
            domain=nvl(self.domainid, self._tenant.getdomainidbyname("Unknown")),
            # descriptive= attr.get("") ,
            mandatory=self.mandatory,
            historicised=self.temporal,
            repeated=self.repeated,
            translated=self.multilingual,
            columnsmapped=[],
            # encrypted= attr.get("") ,
            # minzoomlevel= attr.get("") ,
            # maxzoomlevel= attr.get("") ,
            sourceref={DATASPOTSRCNAME: [self.elemid, str(datetime.today())]},
            userdefprops=jsonudptheme(theme="IM", group="ATTRIBUTES", values=self.udpvalues())
        )
        return retval


class DSRelation(DSIMElement):
    """ relation baseproperties={
      "stereotype" : "many2many",
        "name" : "unterteilt",
        "required" : "OPTIONAL",
        "cardinality" : "MANY",
        "navigable":"RANGE"   "DOMAIN",  "BOTH", "NONE"
        "inverseName":"ist"
        "domainMultiplicity":"1"   "0..1"
        "rangeMultiplicity":"0..*"  "*"
        "hasDomain":"b769ef16-8225-4187-8abf-d80b64aff1db"
        "hasRange":"668c98b7-f2eb-444b-8e4e-ccec8bffcede"
    }"""
    spodproperties = {
        "ARC": 1,
        "BCKWARC": 2,
    }

    def __init__(self, tenant, rela, **kwargs):
        if "_type" not in rela:
            rela["_type"] = DSAccess.Relationship
        super().__init__(tenant=tenant, imelement=rela, **kwargs)
        self.checkrelation()
        return

    @property
    def name(self):
        return self.dsstruct.get("name")

    def fromend(self):
        return {"entity": self.fromentityid,
                "mandatory": self.frommandatory,
                "cardinality": self.fromcardinality,
                "verb": self.fromtext}

    @classmethod
    def cardinality(cls,multiplicity):
        return None if multiplicity is None else \
                 "ONE" if multiplicity in ("1","0..1") \
                    else "MANY"

    @property
    def frommandatory(self):
        if nvl(self.dsstruct.get("required")).strip() == '':
            return False
        else:
            return not (self.dsstruct.get("required") == "OPTIONAL")

    @property
    def tomandatory(self):
        if nvl(self.dsstruct.get("domainMultiplicity")).strip() == '':
            return False
        else:
            return not (self.dsstruct.get("domainMultiplicity") in ("1","*"))

    @property
    def fromtext(self):
        return "????" if nvl(self.name).strip() == '' else self.name

    @property
    def totext(self):
        return "????" if nvl(self.dsstruct.get("inverseName")).strip() == '' else self.dsstruct.get("inverseName")

    @property
    def fromarc(self):
        return self.getudp("ARC")

    @property
    def toarc(self):
        return self.getudp("BCKWARC")

    @property
    def fromcardinality(self):
        if nvl(self.dsstruct.get("domainMultiplicity")).strip() == '':
            return self.cardinality("0..*")
        else:
            return self.cardinality(self.dsstruct.get("domainMultiplicity"))

    @property
    def tocardinality(self):
        if nvl(self.dsstruct.get("rangeMultiplicity")).strip() == '':
            return self.cardinality("0..*")
        else:
            return self.cardinality(self.dsstruct.get("rangeMultiplicity"))

    @property
    def fromentityid(self):
        return self._sourcedivide(self._tenant.getentityidbyname(name=self.dsstruct.get("hasDomain")),
                                  self.dsstruct.get("hasDomain"))

    @property
    def toentityid(self):
        return self._sourcedivide(self._tenant.getentityidbyname(name=self.dsstruct.get("hasRange")),
                                  self.dsstruct.get("hasRange"))

    @property
    def temporal(self):
        return self.dsstruct.get("temporal")

    def udpvalues(self):
        """ get all name,value pairs of user defined properties for this element """
        return super()._udpvalues(spodproperties=self.spodproperties)

    def checkrelation(self):
        if nvl(self.dsstruct.get("name")).strip() == '':
            logging.error(f"Relation \"{self.dsstruct.get('label')}\" has no forward text. Defaulted to '????'")
        if nvl(self.dsstruct.get("inverseName")).strip() == '':
            logging.error(f"Relation \"{self.dsstruct.get('label')}\" has no backward text. Defaulted to '????'")
        if nvl(self.dsstruct.get("inverseName")).strip() == '':
            logging.error(f"Relation \"{self.dsstruct.get('label')}\" has no backward text. Defaulted to '????'")
        if nvl(self.dsstruct.get("domainMultiplicity")).strip() == '':
            logging.error(f"Relation \"{self.dsstruct.get('label')}\" has no forward cardinalty. Defaulted to \"0..*\"")
        if nvl(self.dsstruct.get("rangeMultiplicity")).strip() == '':
            logging.error(f"Relation \"{self.dsstruct.get('label')}\" has no backward cardinalty. Defaulted to \"0..*\"")
        return

    @classmethod
    def udptypes(cls, relas):
        """ returns list of all types (theme, group, name) of user defined properties of all attributes."""
        return super()._udptypes(elements=relas, udptheme="IM", udpgroup=DSAccess.Relationship)

    def relaend(self, many, name, mand, entiid, arcid):
        return jsonrelationend(enti=entiid,
                               arc=arcid,
                               assoc=multilangstring(string=name, lang=self._tenant.lang),
                               maptype="M" if many == "MANY" else "1",
                               hist=False,
                               mandatory=mand)

    def spodjson(self):
        retval = jsonrelation(name=self.name,
                              relatype=self.calculaterelatype(),
                              relafrom=self.relaend(many=self.tocardinality,
                                                    name=self.fromtext,
                                                    mand=self.frommandatory,
                                                    entiid=self.fromentityid,
                                                    arcid=DSArc.arcname(arcno=self.getudp("ARC"),
                                                                        entiid=self.fromentityid
                                                                        )
                                                    ),
                              relato=self.relaend(many=self.fromcardinality,
                                                  name=self.totext,
                                                  mand=self.tomandatory,
                                                  entiid=self.toentityid,
                                                  arcid=DSArc.arcname(arcno=self.getudp("BCKWARC"),
                                                                      entiid=self.toentityid
                                                                      )
                                                  ),
                              sourceref={DATASPOTSRCNAME: [self.elemid, str(datetime.today())]},
                              uc=self.uc, dc=self.dc,
                              tablesmapped=[],
                              publstatus=dsstatus2spodstatus(self.status)
                              )

        return retval


    def dstype2jsontype(self, dstype):
        #no longer stored but calcualtes
        return self.calculaterelatype()
        # if dstype == "many2many":
        #     return "M:N"
        # elif dstype == "one2one":
        #     return "1:1"
        # elif dstype == "role":
        #     return "ISAR"
        # elif dstype == "subtype":
        #     return "ISAS"
        # elif dstype == "one2many":
        #     return "M:1"
        # else:
        #     logging.warning(f"illegal sterotype for relation: \"{dstype}\"")
        #     return None

    def calculaterelatype(self):
        if (self.tocardinality == 'ONE' == self.fromcardinality):
            if (self.frommandatory != self.tomandatory):
                retval = "ISAR"
            elif self.tomandatory and self.frommandatory and \
                    (self.fromarc is not None or self.toarc is not None):
                retval = "ISAS"
            else:
                retval = "1:1"
        elif self.tocardinality != self.fromcardinality:
            retval = "M:1"
        elif self.fromcardinality == 'MANY' == self.tocardinality:
            retval = "M:N"
        else:
            raise Exception(f"illegal relation end combination for relation: \"{self.name}\"")
        return retval


class DSTable(DSIMElement):
    """{"_type":"UmlClass",
    }"""
    spodproperties = {}

    def __init__(self, tenant, tabl, **kwargs):
        if "_type" not in tabl:
            tabl["_type"] = DSAccess.UmlClass
        super().__init__(tenant=tenant, imelement=tabl, **kwargs)
        return

    def columns(self):
        return self._tenant.columns(parentid=self.elemid)

    def transformationsto(self):
        # looking from myself, give me all mappings, mapping me to somebody (I am the from )
        # get all transformations in which I am from
        return self._tenant.transformations(mapfromid=self.elemid)

    def transformationsfrom(self):
        # looking from myself, give me all mappings, mapping somebody to me (I am the to )
        # get all transformations in which I am to
        return self._tenant.transformations(maptoid=self.elemid)

    def udpvalues(self):
        """ getall name,value pairs of user defined properties for this entity """
        return super()._udpvalues(spodproperties=self.spodproperties)

    @classmethod
    def udptypes(cls, tabs):
        """ returns list of all types (theme, group, name) of user defined properties of all entities."""
        return super()._udptypes(elements=tabs, udptheme="DM", udpgroup=DSAccess.UmlClass)

    def spodjson(self):
        mappings = {DSAccess.BusinessObject: set(),
                    DSAccess.UmlClass: set(),
                    DSAccess.Relationship: set()
                    }
        for e in self.transformationsto():
            for i in e.maptoids:
                mapelem = self._tenant.getitembyid(i)
                if mapelem is None:
                    logging.error(f"mapping element not found for id {i}")
                else:
                    mappings[mapelem.elemtype].add(mapelem.elemid)
        for e in self.transformationsfrom():
            for i in e.mapfromids:
                mapelem = self._tenant.getitembyid(i)
                if mapelem is None:
                    logging.error(f"mapping element not found for id {i}")
                else:
                    mappings[mapelem.elemtype].add(mapelem.elemid)
        return jsontable(
            name=self.name,
            datamodelid=self.modelid,
            uc=self.uc, dc=self.dc,
            # publstatus=dsstatus2spodstatus(self.status),
            descr=self.descr,
            sourceref={DATASPOTSRCNAME: [self.elemid, str(datetime.today())]},
            referencedby=[],
            entitiesmapped=list(mappings.get(DSAccess.BusinessObject)),
            tablesmapped=list(mappings.get(DSAccess.UmlClass)),
            relationsmapped=list(mappings.get(DSAccess.Relationship)),
            userdefprops=jsonudptheme(theme="DM", group="TABLES", values=self.udpvalues())
        )


class DSColumn(DSIMElement):
    """{
    {"_type":"UmlAttribute",,
    "required":"OPTIONAL",
    "hasDomain":"d4039b33-b3b1-4df0-b06a-7edc54bb5d48",
    "cardinality":"ONE","maxCardinality":1,"minCardinality":0,
    "hasRange":"2be369d5-e4e7-4ace-838c-0eacc92e0f74",
    }"""
    spodproperties = {}

    def __init__(self, tenant, col, **kwargs):
        if "_type" not in col:
            col["_type"] = DSAccess.UmlAttribute
        super().__init__(tenant=tenant, imelement=col, **kwargs)
        return

    @property
    def domainid(self):
        return self._sourcedivide(self._tenant.getdomainidbyname(name=self.dsstruct.get("hasRange")),
                                  self.dsstruct.get("hasRange"))

    @property
    def mandatory(self):
        return False if self.dsstruct.get("required") == "OPTIONAL" else True

    @property
    def repeated(self):
        return True if self.dsstruct.get("cardinality") == "MANY" else False

    def mappedto(self):
        # looking from myself, give me all rules, mapping me to somebody (I am the from )
        # get all rules in which I am from
        retval = []
        trfns = self.parent.transformationsto()
        for tr in trfns:
            for r in tr.rules:
                if self.elemid in r.transformfromids:
                    retval.append(r)
        return retval

    def mappedfrom(self):
        # looking from myself, give me all rules, mapping somebody to me (I am the to )
        # get all rules in which I am to
        retval = []
        trfns = self.parent.transformationsfrom()
        for tr in trfns:
            for r in tr.rules:
                if self.elemid in r.transformtoids:
                    retval.append(r)
        return retval

    def udpvalues(self):
        """ getall name,value pairs of user defined properties for this entity """
        return super()._udpvalues(spodproperties=self.spodproperties)

    @classmethod
    def udptypes(cls, cols):
        """ returns list of all types (theme, group, name) of user defined properties of all entities."""
        return super()._udptypes(elements=cols, udptheme="DM", udpgroup=DSAccess.UmlAttribute)

    def _onlynewentries(self, maplist, newentry):
        if newentry not in maplist:
            maplist.append(newentry)
        return

    def spodjson(self):
        mappings = {DSAccess.BusinessAttribute: [],
                    DSAccess.UmlAttribute: [],
                    DSAccess.Relationship: []
                    }
        for r in self.mappedto():
            for i in r.transformtoids:
                mapelem = self._tenant.getitembyid(i)
                if mapelem is None:
                    logging.error(f"mapping element not found for id {i}")
                else:
                    # attribute mapping can contain the entity in which the attribute was inherited
                    # in ds: if the same attribute is mapped to an attribute and to an entity which
                    # is in the children hierarchiy of the current entity, use the entity as child (which
                    # inherited the attribute
                    if mapelem.elemtype in mappings.keys():
                        self._onlynewentries(maplist=mappings[mapelem.elemtype],
                                             newentry=mapelem.elemid if mapelem.elemtype == DSAccess.UmlAttribute \
                                                 else jsoncolumapentry(mapid=mapelem.elemid,
                                                                       childid=None))
                    else:
                        logging.warning(
                            f"Element {mapelem.name} is of wrong type {mapelem.elemtyper}to be mapped to element {self.name} ")

        for r in self.mappedfrom():
            for i in r.transformfromids:
                mapelem = self._tenant.getitembyid(i)
                if mapelem is None:
                    logging.error(f"mapping element not found for id {i}")
                else:
                    if mapelem.elemtype in mappings.keys():
                        # attribute mapping can contain the entity in which the attribute was inherited
                        self._onlynewentries(maplist=mappings[mapelem.elemtype],
                                             newentry=mapelem.elemid if mapelem.elemtype == DSAccess.UmlAttribute \
                                                 else jsoncolumapentry(mapid=mapelem.elemid,
                                                                       childid=None))
                    else:
                        logging.warning(
                            f"Element {mapelem.name} is of wrong type {mapelem.elemtype} to be mapped from element {self.name} of type {self.elemtype} ")

        return jsoncolumn(
            name=self.name,
            tableid=self.parentid,
            domain=nvl(self.domainid, self._tenant.getdomainidbyname("Unknown")),
            uc=self.uc, dc=self.dc,
            publstatus=dsstatus2spodstatus(self.status),
            descr=self.descr,
            sourceref={DATASPOTSRCNAME: [self.elemid, str(datetime.today())]},
            referencedby=[],
            attributesmapped=mappings.get(DSAccess.BusinessAttribute),
            columnsmapped=mappings.get(DSAccess.UmlAttribute),
            relationsmapped=mappings.get(DSAccess.Relationship),
            userdefprops=jsonudptheme(theme="DM", group="COLUMNS", values=self.udpvalues())
        )


class DSDomain(DSIMElement):
    """  baseproperties = {"_type": "ReferenceObject",
        "subordinateOf": "19c3995a-9825-407a-94e9-a6d8e3bc0242",
        "inCollection": "f4224577-05c7-47ee-be73-0fcbf4922455",
        }

        OR

        "_type": "DataDomain",
        "_type": "UmlDatatype",
        "baseType": "DECIMAL",
            "fractionDigits": 2,
            "integerDigits": 8,
            "maxInclusive":1000.0,
            "minInclusive":1.0
        "baseType": "STRING",
            "length": "0-250",
            "pattern": "Zeichen",
            "minLength": 0,
            "maxLength": 250,
        "baseType": "BOOLEAN",
        "baseType": "DATETIME",

        OR

    """
    spodproperties = {}

    @classmethod
    def dstype2spodtype(cls, dstype):
        if dstype == "DECIMAL":
            return Domain.NUM
        elif dstype == "BOOLEAN":
            return Domain.LOV
        elif dstype == "STRING":
            return Domain.TXT
        elif dstype == "DATETIME":
            return Domain.DAT
        elif dstype == "DATE":
            return Domain.DAT
        elif dstype == "TIME":
            return Domain.DAT
        else:
            return Domain.TXT

    def __init__(self, tenant, doma, domatype, **kwargs):
        assert doma["_type"] in \
               [DSAccess.ReferenceObject, DSAccess.DataDomain,
                DSAccess.UmlDatatype], f"_type is {doma['_type']} but should be in\"{[DSAccess.ReferenceObject, DSAccess.DataDomain, DSAccess.UmlDatatype]}\""
        super().__init__(tenant=tenant, imelement=doma, **kwargs)
        self._domatype = domatype
        self._origin = Domain.DOMAIN
        self._checkandresolveduplicatenames()

        if kwargs.get("values") is not None:
            self._values = kwargs.get("values")
        elif domatype == Domain.LOV:
            if self.dsstruct.get("baseType") == "BOOLEAN":
                self._values = [DSDomainValue(tenant=tenant, parent=self, domaval=domaval)
                                for domaval in [{"code": "TRUE", "shortText": "True"},
                                                {"code": "FALSE", "shortText": "False"}]
                                ]
            else:
                self._values = []

        # set parent in all values
        for dval in self.values:
            dval.parent = self

        return

    def udpvalues(self):
        """ get all name,value pairs of user defined properties for this attribute """
        return super()._udpvalues(spodproperties=self.spodproperties)

    def _checkandresolveduplicatenames(self):
        twin = self._tenant.getdomainidbyname(name=self.name)
        if twin is not None:
            modelname = self._tenant.getmodelbyid(self.modelid).name
            logging.warning(f"duplicate domain-name \"{self.name}\" in model \"{modelname}\". " + \
                            f" Prefixed with \"{modelname}\"")
            self.name = modelname + "_" + self.name
        return

    @property
    def minlength(self):
        return self.dsstruct.get("minLength")

    @property
    def maxlength(self):
        return self.dsstruct.get("maxLength")

    @property
    def pattern(self):
        return self.dsstruct.get("pattern")

    @property
    def fractdigits(self):
        return self.dsstruct.get("fractionDigits")

    @property
    def intdigits(self):
        return self.dsstruct.get("integerDigits")

    @property
    def minval(self):
        return self.dsstruct.get("minInclusive")

    @property
    def maxval(self):
        return self.dsstruct.get("maxInclusive")

    @property
    def values(self):
        if self._domatype == Domain.LOV:
            return self._values
        else:
            return []

    def getdomainvalue(self, domavalueid):
        for dv in self.values:
            if dv.elemid == domavalueid: return dv
        return None

    def mappedtodomains(self):
        # looking from myself, give me all mappings, mapping me to somebody (I am the from )
        return self._tenant.mappings(mapsfromid=self.elemid)

    def mappedfromdomains(self):
        # looking from myself, give me all mappings, mapping somebody to me (I am the to )
        return self._tenant.mappings(mapstoid=self.elemid)

    @classmethod
    def udptypes(cls, domas):
        """ returns list of all types (theme, group, name) of user defined properties of all domains."""
        return super()._udptypes(elements=domas, udptheme="IM", udpgroup=DSAccess.ReferenceObject)

    # TODO system-domains vs IM domains
    # TODO duplicate Names
    def spodjson(self):
        retval = jsondomain(name=multilangstring(string=self.name, lang=self._tenant.lang),
                            domtype=self._domatype,
                            domorigin=self._origin,
                            datamodelid=None if self.dsstruct.get("_type") != DSAccess.UmlDatatype \
                                else self.modelid,
                            descr=multilangstring(string=self.descr, lang=self._tenant.lang),
                            values=[domval.spodjson() for domval in self.values],
                            sourceref={DATASPOTSRCNAME: [self.elemid, str(datetime.today())]},
                            uc=self.uc, dc=self.dc,
                            minvalue=self.minval, maxvalue=self.maxval,
                            totaldigits=None if self._domatype != Domain.NUM
                            else nvl(self.intdigits, 0) + nvl(self.fractdigits, 0),
                            fractdigits=None if self._domatype != Domain.NUM
                            else nvl(self.fractdigits, 0),
                            granularity=None if self._domatype != Domain.DAT
                            else Domain.SECOND if self.dsstruct.get("baseType") == "TIME"
                            else Domain.MINUTE if self.dsstruct.get("baseType") == "DATETIME"
                            else Domain.DAY,
                            # roundvalue=,unit=, unitid=,
                            maxlng=self.maxlength, syntaxrule=self.pattern,
                            mappedto=[m.mapstoid for m in self.mappedtodomains()],
                            mappedfrom=[m.mapsfromid for m in self.mappedfromdomains()]
                            )

        return retval


class DSArc(DSIMElement):
    @classmethod
    def arcname(cls, arcno, entiid):
        return None if arcno is None else f"{str(entiid)}-{str(arcno)}"

    def __init__(self, tenant, no, entiid, relations=[], **kwargs):
        super().__init__(tenant=tenant, imelement={}, **kwargs)
        self._arcno = no
        self._name = self.arcname(entiid=entiid, arcno=self._arcno)
        self._relations = relations
        self._entiid = entiid
        return

    @property
    def name(self):
        return "????" if nvl(self._name).strip() == '' else self._name

    @property
    def elemid(self):
        return self._name

    @property
    def elemtype(self):
        return DSArc.__name__

    @property
    def relations(self):
        return self._relations

    @property
    def entiid(self):
        return self._entiid

    def spodjson(self):
        retval = jsonarc(name=self.name,
                         entity=self.entiid,
                         relations=self.relations,
                         uc=self.uc, dc=self.dc,
                         sourceref={DATASPOTSRCNAME: [self.elemid, str(datetime.today())]}
                         )
        return retval


class DSDomainValue(DSIMElement):
    """baseproperties {
    {
  "literalOf" : "ISO-Land",
  "timeSeries" : [ {
    "validFrom" : -2208988800000,
    "validTo" : 32503593600000,
    "code" : "AD",
    "shortText" : "Andorra"
  }
    }"""

    spodproperties = {}

    def __init__(self, tenant, domaval, parent, **kwargs):
        if "_type" not in domaval:
            domaval["_type"] = DSAccess.ReferenceValue
        super().__init__(tenant=tenant, imelement=domaval, **kwargs)
        self._parent = parent
        return

    @property
    def code(self):
        return self.dsstruct.get("code")

    @property
    def shorttext(self):
        return self.dsstruct.get("shortText")

    @property
    def parent(self):
        if self._parent is None:
            self._tenant.getitembyid(self.dsstruct.get("literalOf"))
        else:
            return self._parent

    @parent.setter
    def parent(self, val):
        self._parent = val

    @property
    def parentid(self):
        if self._parent is None:
            return self.dsstruct.get("literalOf")
        else:
            return self._parent.elemid

    def spodjson(self):
        # in mapsfrom I am the translationtoid
        mapsfrom = [[self._tenant.getitembyid(mf.mapsfromid), mf.translations] for mf in
                    self.parent.mappedfromdomains()]
        # in mapsto I am the translationfromid
        mapsto = [[self._tenant.getitembyid(mf.mapstoid), mf.translations] for mf in self.parent.mappedtodomains()]

        mapvalto = [[jsondomainvaluemap(domainid=trs[0].elemid,
                                        value=trs[0].getdomainvalue(tr.translatetoid).code)
                     for tr in trs[1]
                     if tr.translatefromid == self.elemid
                     ]
                    for trs in mapsto
                    ]
        while [] in mapvalto:  # remove missing translatione
            mapvalto.remove([])
        mapvalfrom = [[jsondomainvaluemap(domainid=trs[0].elemid,
                                          value=trs[0].getdomainvalue(
                                              tr.translatefromid).code)
                       for tr in trs[1]
                       if tr.translatetoid == self.elemid
                       ]
                      for trs in mapsfrom
                      ]
        while [] in mapvalfrom:  # remove missing translatione
            mapvalfrom.remove([])
        retval = jsondomainvalue(value=self.code, sort=None,
                                 descr=self.title, displ=self.shorttext,
                                 uc=self.uc, dc=self.dc,
                                 mappedto=mapvalto,
                                 mappedfrom=mapvalfrom
                                 )
        return retval


class DSTransformation(DSIMElement):
    """{"_type":"Transformation",  -> always to one entity/table
    "transformationOf":"2f305c23-d9a6-46c7-95ff-ef14c7c64b07",
    "label":"AccountId-bez"
    "parentId":"2f305c23-d9a6-46c7-95ff-ef14c7c64b07",

    """

    spodproperties = {}

    def __init__(self, tenant, trnsf, rules=None, **kwargs):
        if "_type" not in trnsf:
            trnsf["_type"] = DSAccess.Transformation
        super().__init__(tenant=tenant, imelement=trnsf, **kwargs)
        self._rules = rules
        return

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, rules):
        self._rules = rules

    @property
    def rulefrwd(self):
        return None

    @property
    def rulebckw(self):
        return None

    @property
    def mapfromids(self):
        # get all parents of all elements mapped in rules
        fromelements = []
        for r in self.rules:
            for elemid in r.transformfromids:
                elem = self._tenant.getitembyid(elemid)
                if elem is None:
                    # assume it is a enumeration and forget it
                    # TODO resolve erarlier
                    logging.error(f"no element found for mapping entry {elemid}")
                elif elem.parent is None:
                    logging.error(f"no parent element found for mapping entry {elemid}:{elem.name}")
                else:
                    # for values, attributes and columns the transformation is defined for their resp. parents
                    # for parent-elements it is the element itself
                    if elem.elemtype in (DSAccess.UmlAttribute, DSAccess.ReferenceValue, DSAccess.BusinessAttribute):
                        fromelements.append(elem.parent.elemid)
                    else:
                        fromelements.append(elem.elemid)
        return list(set(fromelements))  # remove duplicates

    @property
    def maptoids(self):
        return [self.dsstruct.get("transformationOf")]

    @classmethod
    def maptype(cls, fromelemtype, toelemtype):
        if fromelemtype == DSAccess.UmlClass == toelemtype:
            return Mapping.MAPTYPE_DATM_DATM
        elif (fromelemtype == DSAccess.UmlClass and \
              toelemtype == DSAccess.BusinessObject) or \
                (fromelemtype == DSAccess.BusinessObject and \
                 toelemtype == DSAccess.UmlClass):
            return Mapping.MAPTYPE_DATM_IM
        elif (fromelemtype == DSAccess.UmlClass and \
              toelemtype == DSAccess.Relationship) or \
                (fromelemtype == DSAccess.Relationship and \
                 toelemtype == DSAccess.UmlClass):
            return Mapping.MAPTYPE_DATM_IM
        elif fromelemtype == DSAccess.UmlClass and toelemtype == '????':
            return Mapping.MAPTYPE_DATM_SYST
        assert False, f"illegal combination of mappints \"{fromelemtype}\" - \"{toelemtype}\""
        return

    def spodjson(self):
        mapsfrom = self._tenant.getitembyid(self.mapfromids[0])
        mapsto = self._tenant.getitembyid(self.maptoids[0])
        retval = jsonmapping(name=self.name,
                             maptype=self.maptype(fromelemtype=mapsfrom.elemtype,
                                                  toelemtype=mapsto.elemtype),
                             descr=self.descr,
                             fromelemids=self.mapfromids,
                             toelemids=self.maptoids,
                             rulefrwd=self.rulefrwd,
                             rulebckw=self.rulebckw,
                             sourceref={DATASPOTSRCNAME: [self.elemid, str(datetime.today())]},
                             uc=self.uc, dc=self.dc
                             )
        return retval


class DSRule(DSIMElement):
    """
    {"_type":"Rule",
    ,"ruleOf":"3fe7d0e2-74e1-4b5f-8b5e-28d87486ae93",
    "transformsFrom":["74028795-6ec7-422a-bd11-ae2aea4cc3bc"],
    "transformsTo":["b5727aa0-fd1d-4f73-add4-7eca254e3e53"],
    "label":"167",
    "stereotype":"ONE2ONE",
    "parentId":"3fe7d0e2-74e1-4b5f-8b5e-28d87486ae93",
    """
    spodproperties = {}

    def __init__(self, tenant, rule, **kwargs):
        if "_type" not in rule:
            rule["_type"] = DSAccess.Rule
        super().__init__(tenant=tenant, imelement=rule, **kwargs)
        return

    @property
    def parent(self):
        return self._tenant.getitembyid(self.parentid)

    @property
    def parentid(self):
        return self.dsstruct.get("ruleOf")

    @property
    def transformfromids(self) -> list:
        return self.dsstruct.get("transformsFrom")

    @property
    def transformtoids(self) -> list:
        return self.dsstruct.get("transformsTo")


class DSMapping(DSIMElement):
    """baseproperties {
    "mapsTo": "941ba7f7-1d65-4ae5-9236-6e9e3ae4df14",
    "mapsFrom": "317183b4-5ab2-48f7-9c7a-f62b6c11adc5",
    }"""

    spodproperties = {}

    def __init__(self, tenant, mapng, translations=None, **kwargs):
        if "_type" not in mapng:
            mapng["_type"] = DSAccess.ReferenceValue
        super().__init__(tenant=tenant, imelement=mapng, **kwargs)
        self._translations = translations
        return

    @property
    def mapsfromid(self):
        return self.dsstruct.get("mapsFrom")

    @property
    def mapstoid(self):
        return self.dsstruct.get("mapsTo")

    @property
    def translations(self):
        if self._translations is None:
            self._translations = self._tenant.translations(mapid=self.elemid)
        return self._translations

    @translations.setter
    def translations(self, translations):
        self._translations = translations

    @property
    def rulefrwd(self):
        return None

    @property
    def rulebckw(self):
        return None

    def spodjson(self):
        retval = jsonmapping(name=self.name,
                             maptype=Mapping.MAPTYPE_DOMA_DOMA,
                             descr=self.descr,
                             fromelemids=[self.mapsfromid],
                             toelemids=[self.mapstoid],
                             rulefrwd=self.rulefrwd,
                             rulebckw=self.rulebckw,
                             sourceref={DATASPOTSRCNAME: [self.elemid, str(datetime.today())]},
                             uc=self.uc, dc=self.dc
                             )

        return retval


class DSTranslation(DSIMElement):
    """baseproperties {
    "translationIn" : "testboolean",
    "translatesFrom" : "1",
    "translatesTo" : "TRUE",
      "validFrom" : -2208988800000,
  "validTo" : 32503593600000,
    }"""

    spodproperties = {}

    def __init__(self, tenant, trnsl, **kwargs):
        if "_type" not in trnsl:
            trnsl["_type"] = DSAccess.ReferenceValue
        super().__init__(tenant=tenant, imelement=trnsl, **kwargs)
        return

    @property
    def mappingid(self):
        return self.dsstruct.get("translationIn")

    @property
    def parentid(self):
        return self.mappingid

    @property
    def parent(self):
        return self._tenant.getitembyid(self.parentid)

    @property
    def translatefromid(self):
        return self.dsstruct.get("translatesFrom")

    @property
    def translatetoid(self):
        return self.dsstruct.get("translatesTo")
