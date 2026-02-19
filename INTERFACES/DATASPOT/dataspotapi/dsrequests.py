import json
import logging
from pathlib import Path

import requests as req
from requests.auth import HTTPBasicAuth, AuthBase

from IM_STANDARD import nvl
from INTERFACES import authentification


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

    def _basehttprequest(self, reqtype="rest"):
        return self._repository + f"/{reqtype}/" + self._repoowner

    def _getcredentials(self, credentialfile, username, password, viaazure):
        self.__un=None,
        self.__pw=None
        self.__accesskey=None
        self.__token=None
        lclientid = None
        if username is None:
            if credentialfile is None:
                credentialfile = self.DEFAULT_CREDENTIALS
            try:
                credentials = authentification.getcredentials(credentialfile=credentialfile)
                if credentials is not None:
                    self.__un = credentials[1].get('username')
                    self.__pw = credentials[1].get('password')
                    lclientid = credentials[1].get('clientid')
                    self.__accesskey = credentials[1].get('accesskey')
                if self.__un is None and self.__accesskey is None:
                    raise Exception(f"no proper credentials found in file {credentialfile}")
            except Exception as exp:
                logging.error(exp)
                raise exp
        else:
            self.__un = username
            self.__pw = password
            self.__accesskey = None

        if viaazure:
            self._auth = TokenAuth(
                token=authentification.getazuretoken(clientid=lclientid, username=self.__un, password=self.__pw))
        else:
            self._auth = HTTPBasicAuth(username=self.__un, password=self.__pw)
        return

    def _buildheader(self, postheader=False, accesskey=None):
        header = {
            'accept': "application/json",
        }
        if accesskey is not None:
            header["dataspot-access-key"] = accesskey
        if self._tenantname is not None:
            header["dataspot-tenant"] = self._tenantname
        if postheader:
            header["content-type"] = 'application/json'
        return header

    def doread(self, url,
               params,
               outpath):
        url = "https://www.dataspot.io/api/chem-x/schemes/Business%20Partners%20and%20Identity/download?format=json&v=3"

        #from invoke import task
        #@task
        #def download(c, filename="data.json"):
        # Use the -o flag just like you wanted
        # -L follows redirects, -s is silent mode
        # c.run(f"curl -L -s '{url}' -o {filename}")
        # print(f"File saved to {filename}")
        locrequest = self._basehttprequest(reqtype='api') + url
        with req.get(url, params=params,
                     headers=self._buildheader(accesskey=self.accesskey),
                     stream=True) as r:
            r.raise_for_status()  # Check for HTTP errors (404, 500, etc.)

            # 2. Open the local file for writing in 'binary' mode
            with open(outpath, 'wb') as f:
                # 3. Write the file in chunks (e.g., 8KB at a time)
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)

        return

    def _doget(self, request, reqtype="rest", params=None):
        locrequest = self._basehttprequest(reqtype=reqtype) + request
        # response = req.get(locrequest, auth=self._auth, headers=self._buildheader(accesskey=self.accesskey))
        try:
            response = req.get(locrequest, headers=self._buildheader(accesskey=self.accesskey),
                               params=params)
        except Exception as e:
            raise e
        if response.status_code != 200:
            raise Exception(f"api access error {response.reason}")
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
    DataAttribute = "DataAttribute"
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
        self._tenantname = None
        self._tenants = self.gettenants()
        if tenantname is not None:
            assert tenantname in [tname.get("tenantName") for tname in
                                  self._tenants], f"tenant {tenantname} not found in repository {repository}"
            self._tenantname = tenantname
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

    def _getelements(self, elemtype, modelname=None, subtypes: list = None,
                     filtercondition=lambda x: True):
        modelpart = "" if modelname is None else f"/schemes/{modelname}"
        answer = self._doget(request=f"{modelpart}/{elemtype}/")
        if "_embedded" in answer:
            elems = answer["_embedded"][elemtype]
        else:
            elems = []
        retval = [elem for elem in elems if (nvl(subtypes, []) == [] or elem["_type"] in subtypes) and \
                  filtercondition(elem)
                  ]
        return retval

    def getschemes(self, schemetypes: list = None, filtercondition=None):
        schemes = self._getelements(elemtype="schemes"
                                    , subtypes=schemetypes
                                    , filtercondition=nvl(filtercondition, truelambda))
        return schemes

    def getscheme(self, modelname):
        scheme = self.getschemes(filtercondition=lambda x: x["label"] == modelname)
        if len(scheme) == 0:
            return None
        elif len(scheme) == 1:
            return scheme[0]
        else:
            raise Exception(f"more than one scheme found for {modelname}")

    def getcollections(self, parentid=None, modelname=None):
        """parentId is either scheme/model-ID or (parent-)collection-ID"""
        cols = self._getelements(elemtype="collections", modelname=modelname)
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

    def getbusinessobjects(self, modelid=None, modelname=None, collectionid=None, filtercondition=truelambda):
        return self._getelements(elemtype="classifiers",
                                 modelname=modelname,
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

    def getenumerations(self, modelname=None, modelid=None):
        enums = self._getelements(elemtype="enumerations",
                                  modelname=modelname,
                                  filtercondition=lambda elem: (modelid is None or elem.get("modelId") == modelid))
        return enums

    def getdatatypes(self, modelname=None, modelid=None):
        datys = self._getelements(elemtype="datatypes",
                                  modelname=modelname,
                                  filtercondition=lambda elem: (modelid is None or elem.get("modelId") == modelid))
        return datys

    def getliterals(self, modelname=None, enumid=None):
        literals = self._getelements(elemtype="literals",
                                     modelname=modelname,
                                     filtercondition=lambda elem: (enumid is None or elem.get("literalOf") == enumid))
        return literals

    def gettranslations(self, modelname=None, mapid=None):
        translations = self._getelements(elemtype="translations",
                                         modelname=modelname,
                                         filtercondition=lambda elem: (
                                                 mapid is None or elem.get("translationIn") == mapid))
        return translations

    def getmappings(self, modelname=None, modelid=None):
        mappings = self._getelements(elemtype="mappings",
                                     modelname=modelname,
                                     filtercondition=lambda elem: (
                                             modelid is None or elem.get("modelId") == modelid))
        return mappings

    def getrules(self,
                 modelname=None, trfmid=None):
        rules = self._getelements(elemtype="rules",
                                  modelname=modelname,
                                  filtercondition=lambda elem: (trfmid is None or elem.get("ruleOf") == trfmid))
        return rules

    def gettransformations(self,
                           modelname=None, modelid=None):
        transformations = self._getelements(elemtype="transformations",
                                            modelname=modelname,
                                            filtercondition=lambda elem: (
                                                    modelid is None or elem.get("modelId") == modelid))
        return transformations

    def getmodelattributes(self, modelname, entities: list):
        """ read all attributes of all entities in this model"""
        attrs = []
        for enti in entities:
            # misuse of modelname parameter
            try:
                attrs += self._getelements(elemtype="attributes",
                                           modelname=modelname + "/classifiers/" + enti,
                                           filtercondition=lambda elem: elem.get("_type") == self.BusinessAttribute)
            except Exception as e:
                if e.__str__().endswith("Not Found"):
                    pass
                else:
                    raise e
        return attrs

    def getdataattributes(self, modelid=None):
        attrs = self._getelements(elemtype="attributes",
                                  filtercondition=lambda elem: elem.get("_type") == self.DataAttribute and \
                                                               (modelid is None or modelid == elem.get("modelId")))
        return attrs

    def getattributes(self, modelid=None):
        attrs = self._getelements(elemtype="attributes",
                                  filtercondition=lambda elem: elem.get("_type") == self.BusinessAttribute and \
                                                               (modelid is None or modelid == elem.get("modelId")))
        return attrs

    def getrelations(self,
                     modelname=None, modelid=None):
        relas = self._getelements(elemtype="associations",
                                  modelname=modelname,
                                  filtercondition=lambda elem: modelid is None or elem.get("modelId") == modelid)
        return relas

    def gettables(self,
                  modelname=None, modelid=None):
        tables = self._getelements(elemtype="classifiers",
                                   modelname=modelname,
                                   filtercondition=lambda elem: (modelid is None or elem.get("modelId") == modelid) and
                                                                elem.get("_type") == self.UmlClass)
        return tables

    def getcolumns(self,
                   modelname=None, modelid=None):
        cols = self._getelements(elemtype="attributes",
                                 modelname=modelname,
                                 filtercondition=lambda elem: (modelid is None or elem.get("modelId") == modelid) and
                                                              elem.get("_type") == self.UmlAttribute)
        return cols
