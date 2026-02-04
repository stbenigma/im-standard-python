import re

from .dsrequests import DSAccess

class dataspotAPI:
    def __init__(self, reponame, repoowner,
                 tenantname=None,
                 credentialfile=None,
                 username=None,
                 password=None):
        self.dsaccess = DSAccess(credentialfile=credentialfile,
                                 username=username,
                                 password=password,
                                 repository=reponame,
                                 repoowner=repoowner,
                                 tenantname=tenantname,
                                 viaazure=False)
        return

    def getmodels(self, schemetypes=list(), filtercondition=None):
        models = self.dsaccess.getschemes(filtercondition=filtercondition,
                                          schemetypes=schemetypes)
        return models

    def get1model(self, modelname):
        model = self.dsaccess._doget(request=f"/schemes/{modelname}/download",
                                 reqtype="api",
                                 params={'format': 'json',
                                         'v': "3"})
        return model

    @property
    def tenantname(self):
        return self.dsaccess.tenantname

    @tenantname.setter
    def tenantname(self, val):
        self.dsaccess.tenantname = val

    def gettenant(self, tenantname=None):
        tenants = self.gettenants()
        if tenantname is None and len(tenants) == 1:
            return tenants[0]
        else:
            tenant = [ten for ten in tenants if ten.get("tenantName") == tenantname]
            if len(tenant) == 1:
                return tenant[0]
            else:
                return None

    def gettenants(self, ):
        return self.dsaccess.gettenants()

    def getmodelnames(self, models):
        return [m.get("label") for m in models]

    def loadmodels(self, modelnamepattern: str):
        """
        returns all modelnames matching the regexp which are in the repository
        :param modelnames:
        :return:
        """
        self.metamodel = {
            "models": self.getmodels(),
            "categories": [],
            "systems": [],
            "entities": [],
            "attributes": [],
            "domains": [],
            "LOVvalues": [],
            "tables": [],
            "columns": [],
            "relationships": [],
            "transformations": [],
            "mappings": [],
            "rules": [],
            "translations": [],
            "deployments": [],
            "dependencies": [],
            "derivations": [],
            "diagrams": [],
            "diagelements": [],
            "businessrules": []
        }
        # TODO read all attributes as this takes a long time and is repeated
        for model in self.metamodel["models"]:
            if re.match(modelnamepattern, model.get("label")):
                self.loadjson(model)
        return

    def loadjson(self, model):
        modelname = model.get("label")
        if model.get("_type") == "BusinessDataModel":
            self.metamodel["categories"] += self.dsaccess.getcollections(modelname=modelname)
            self.metamodel["entities"] += self.dsaccess.getbusinessobjects(modelname=modelname)
            self.metamodel["attributes"] += self.dsaccess.getattributes(modelid=model.get("id"))
            self.metamodel["relationships"] += []
            self.metamodel["transformations"] += []
            self.metamodel["rules"] += []
            self.metamodel["translations"] += []
            self.metamodel["deployments"] += []
            self.metamodel["derivations"] += []
            self.metamodel["businessrules"] += []
        elif model.get("_type") == "DataDomainModel":
            self.metamodel["categories"] += self.dsaccess.getcollections(modelname=modelname)
            self.metamodel["domains"] += self.dsaccess.getdatatypes(modelname=modelname),
            self.metamodel["attributes"] += self.dsaccess.getdataattributes(modelid=model.get("id"))
            self.metamodel["transformations"] += []
            self.metamodel["rules"] += []
            self.metamodel["translations"] += []
            self.metamodel["deployments"] += []
            self.metamodel["derivations"] += []
            self.metamodel["businessrules"] += []
        elif model.get("_type") == "ReferenceDataModel":
            self.metamodel["categories"] += self.dsaccess.getcollections(modelname=modelname)
            self.metamodel["domains"] += self.dsaccess.getenumerations(modelname=modelname),
            self.metamodel["LOVvalues"] += []
            self.metamodel["transformations"] += []
            self.metamodel["mappings"] += []
            self.metamodel["rules"] += []
            self.metamodel["translations"] += []
            self.metamodel["deployments"] += []
            self.metamodel["derivations"] += []
            self.metamodel["businessrules"] += []
        else:
            print("NOT YET HANDLED", model.get("_type"))
        return

