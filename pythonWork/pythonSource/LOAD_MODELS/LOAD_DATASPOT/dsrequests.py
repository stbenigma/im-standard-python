import json
from pathlib import Path

import requests as req
from requests.auth import HTTPBasicAuth, AuthBase

from SSOT_infra import authentification


class TokenAuth(AuthBase):
    def __init__(self, token, auth_scheme='Bearer'):
        self.token = token
        self.auth_scheme = auth_scheme

    def __call__(self, request):
        request.headers['Authorization'] = f'{self.auth_scheme} {self.token}'
        return request


class DSRequest:
    DEFAULT_CREDENTIALS = Path.home() / ".dataspot" / "credentials-fyayc.yaml"

    def __init__(self, repository, repoowner,
                 credentialfile=None, username=None, password=None,
                 viaazure=False):
        self._repoowner = repoowner
        self._repository = repository
        self._getcredentials(credentialfile=credentialfile,
                             username=username, password=password, viaazure=viaazure)
        return

    def _basehttprequest(self):
        return self._repository + "/rest/" + self._repoowner

    def _getcredentials(self, credentialfile, username, password, viaazure):
        if username is None:
            if credentialfile is None:
                credentialfile = self.DEFAULT_CREDENTIALS
            try:
                credentials = authentification.getcredentials(credentialfile=credentialfile)
                if credentials is not None:
                    lusername = credentials[1].get('username')
                    lpassword = credentials[1].get('password')
                    lclientid = credentials[1].get('clientid')
                if lusername is None:
                    raise Exception(f"no proper credentials found in file {credentialfile}")
            except Exception as exp:
                raise exp

        else:
            lusername = username
            lpassword = password
            lclientid = None

        if viaazure:
            self._auth = TokenAuth(
                token=authentification.getazuretoken(clientid=lclientid, username=lusername, password=lpassword))
        else:
            self._auth = HTTPBasicAuth(username=lusername, password=lpassword)
        return

    def _buildheader(self, postheader=False):
        header = {
            'accept': "application/json",
        }
        if self._tenantname is not None:
            header["dataspot-tenant"] = self._tenantname
        if postheader:
            header["content-type"] = 'application/json'
        return header

    def _doget(self, request):
        locrequest = self._basehttprequest() + request
        response = req.get(locrequest, auth=self._auth, headers=self._buildheader())
        if response.status_code != 200:
            raise Exception(f"api access error {response.text}")
        jsonresp = json.loads(response.content)
        return jsonresp

    def _postheader(self):
        return self._buildheader(postheader=True)

    # def _dopatch(self,request,data):
    #     locrequest=urllib.parse.quote(request)
    #     response = req.patch(url=locrequest,json=data, headers=self._postheader())
    #     if response.status_code not in (200,201):
    #         raise Exception(f"miro api access error {response.text}"+
    #                         f"\ndata={data}")
    #     jsonresp = json.loads(response.content)
    #     return jsonresp
    #
    # def _dodelete(self,request):
    #     locrequest = urllib.parse.quote(request)
    #     response = req.delete(url=locrequest, headers=self._postheader())
    #     if response.status_code not in (201, 200,204):
    #         raise Exception(f"miro api access error {response.text}")
    #
    # def _dopost(self,request,data):
    #     # add http if missing
    #     locrequest=urllib.parse.quote(request)
    #     response = req.post(url=locrequest,json=data, headers=self._postheader())
    #     if response.status_code not in (201,200):
    #         raise Exception(f"miro api access error {response.text}"+
    #                         f"\ndata={data}")
    #     jsonresp = json.loads(response.content)
    #     return jsonresp
    #


truelambda = lambda x: True


class DSAccess(DSRequest):
    # Elementtypes
    BusinessAttribute = "BusinessAttribute"
    BusinessDataModel = "BusinessDataModel"
    BusinessObject = "BusinessObject"
    Collection = "Collection"
    DataCatalog = "DataCatalog"
    DataDomain = "DataDomain"
    DataDomainModel = "DataDomainModel"
    MeasuresCatalog = "MeasuresCatalog"
    ProcessingRecords = "ProcessingRecords"
    ProjectDirectory = "ProjectDirectory"
    QualityModel = "QualityModel"
    Mapping = "Mapping"
    ReferenceDataModel = "ReferenceDataModel"
    ReferenceObject = "ReferenceObject"
    ReferenceValue = "ReferenceValue"
    Relationship = "Relationship"
    Rule = "Rule"
    SystemCatalog = "SystemCatalog"
    Transformation = "Transformation"
    Translation = "Translation"
    UmlAttribute = "UmlAttribute"
    UmlClass = "UmlClass"
    UmlDatatype = "UmlDatatype"
    UmlModel = "UmlModel"

    KnownModelTypes = [BusinessAttribute,
                       BusinessDataModel,
                       BusinessObject,
                       Collection,
                       DataCatalog,
                       DataDomain,
                       DataDomainModel,
                       MeasuresCatalog,
                       ProcessingRecords,
                       ProjectDirectory,
                       QualityModel,
                       Mapping,
                       ReferenceDataModel,
                       ReferenceObject,
                       ReferenceValue,
                       Relationship,
                       Rule,
                       SystemCatalog,
                       Transformation,
                       Translation,
                       UmlAttribute,
                       UmlClass,
                       UmlDatatype,
                       UmlModel
                       ]

    def __init__(self, repository, repoowner, tenantname=None,
                 credentialfile=None, username=None, password=None,
                 viaazure=False
                 ):
        super().__init__(repository=repository, repoowner=repoowner,
                         credentialfile=credentialfile, username=username, password=password,
                         viaazure=viaazure
                         )
        self._tenantname=tenantname
        self._tenants = self.gettenants()
        if tenantname is not None:
            assert tenantname in [tname.get("tenantName") for tname in self._tenants], f"tenant {tenantname} not found in repository {repository}"
        return

    @property
    def tenantname(self):
        return self._tenantname

    @tenantname.setter
    def tenantname(self, val):
        self._tenantname = val


    def gettenants(self):
        return self._doget(request="/tenants/")["_embedded"]["tenants"]

    def gettenant(self):
        for tenant in self._tenants:
            if tenant["tenantName"] == self.tenantname:
                return tenant
        return None

    def _getelements(self, elemtype, subtypes: list = None,
                     filtercondition=lambda x: True):
        answer = self._doget(request=f"/{elemtype}/")
        if "_embedded" in answer:
            elems = answer["_embedded"][elemtype]
        else:
            elems = []
        retval = [elem for elem in elems if (subtypes is None or elem["_type"] in subtypes) and \
                  filtercondition(elem)
                  ]
        return retval

    def getschemes(self, schemetypes: list = None, filtercondition=truelambda):
        schemes = self._getelements(elemtype="schemes"
                                    , subtypes=schemetypes
                                    , filtercondition=filtercondition)
        return schemes

    def getscheme(self, modelname):
        scheme = self.getschemes(filtercondition=lambda x: x["label"] == modelname)
        if len(scheme) == 0:
            return None
        elif len(scheme) == 1:
            return scheme[0]
        else:
            raise Exception(f"more than one scheme found for {modelname}")

    def getcollections(self, parentid=None):
        """parentId is either scheme/model-ID or (parent-)collection-ID"""
        cols = self._getelements(elemtype="collections")
        if parentid is None:
            return cols  # no restriction
        else:
            """find all (grand-)children below this parent"""
            retval = []
            parentids = []
            # start with top: collections in models (=schemes)
            for col in cols:
                if col.get("inScheme") == parentid:
                    retval.append(col)
                    parentids.append(col["id"])
                    cols.remove(col)
            lastlen = len(cols) + 1  # make sure look runs at least once
            # while we still find children in the tree, we keep going
            while len(cols) < lastlen:
                lastlen = len(cols)
                for col in cols:
                    if col.get("inCollection") in parentids:
                        retval.append(col)
                        parentids.append(col["id"])
                        cols.remove(col)
            return retval

    def getbusinessobjects(self, modelid=None, collectionid=None, filtercondition=truelambda):
        return self._getelements(elemtype="classifiers",
                                 subtypes=[self.BusinessObject],
                                 filtercondition=lambda elem: (modelid is None or
                                                               elem["modelId"] == modelid) \
                                                              and (collectionid is None or
                                                                   elem["inCollection"] == collectionid) \
                                                              and filtercondition(elem)
                                 )

    def getbusinessobject(self, modelid, objname):
        busobjs = self.getbusinessobjects(modelid=modelid,
                                          filtercondition=lambda elem: elem["label"] == objname)
        if len(busobjs) == 0:
            return None
        elif len(busobjs) == 1:
            return busobjs[0]
        else:
            raise Exception(f"more than one businesobject found in model {modelid} for name {objname}")

    def getenumerations(self, modelid=None):
        enums = self._getelements(elemtype="enumerations",
                                  filtercondition=lambda elem: (modelid is None or elem.get("modelId") == modelid))
        return enums

    def getdatatypes(self, modelid=None):
        datys = self._getelements(elemtype="datatypes",
                                  filtercondition=lambda elem: (modelid is None or elem.get("modelId") == modelid))
        return datys

    def getliterals(self, enumid=None):
        literals = self._getelements(elemtype="literals",
                                     filtercondition=lambda elem: (enumid is None or elem.get("literalOf") == enumid))
        return literals

    def gettranslations(self, mapid=None):
        translations = self._getelements(elemtype="translations",
                                         filtercondition=lambda elem: (
                                                     mapid is None or elem.get("translationIn") == mapid))
        return translations

    def getmappings(self, modelid=None):
        mappings = self._getelements(elemtype="mappings",
                                         filtercondition=lambda elem: (
                                                     modelid is None or elem.get("modelId") == modelid))
        return mappings

    def getrules(self, trfmid=None):
        rules = self._getelements(elemtype="rules",
                                  filtercondition=lambda elem: (trfmid is None or elem.get("ruleOf") == trfmid))
        return rules

    def gettransformations(self, modelid=None):
        transformations = self._getelements(elemtype="transformations",
                                            filtercondition=lambda elem: (
                                                        modelid is None or elem.get("modelId") == modelid))
        return transformations

    def getattributes(self, modelid=None):
        attrs = self._getelements(elemtype="attributes",
                                  filtercondition=lambda elem: (modelid is None or elem.get("modelId") == modelid) and
                                                               elem.get("_type") == self.BusinessAttribute)
        return attrs

    def getrelations(self, modelid=None):
        relas = self._getelements(elemtype="associations",
                                  filtercondition=lambda elem: modelid is None or elem.get("modelId") == modelid)
        return relas

    def gettables(self, modelid=None):
        tables = self._getelements(elemtype="classifiers",
                                   filtercondition=lambda elem: (modelid is None or elem.get("modelId") == modelid) and
                                                                elem.get("_type") == self.UmlClass)
        return tables

    def getcolumns(self, modelid=None):
        cols = self._getelements(elemtype="attributes",
                                 filtercondition=lambda elem: (modelid is None or elem.get("modelId") == modelid) and
                                                              elem.get("_type") == self.UmlAttribute)
        return cols
