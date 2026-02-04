import json
import unittest
import pytest
from pathlib import Path


from INTERFACES.DATASPOT import dataspotAPI

class MyTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temp_folder = Path(tmp_path)
        self.debugpath = Path.home() / "Downloads"  # try local debug path
        if not self.debugpath.is_dir():
            # write to tempfolder
            self.debugpath = self.temp_folder / "debug"
            self.debugpath.mkdir(exist_ok=True)

    def setUp(self) -> None:
        self.reponame = "https://www.dataspot.io"
        self.repoowner = "chem-x"
        self.tenantname = "Mandant"
        self.credentialfile = Path.home() / ".dataspot" / "credentials-chemx.yaml"

    def test_loadim(self):

        if not Path.exists(self.credentialfile):
            self.skipTest("\nno credentials found skip test with real credentials")

        # check default access with credentialfile
        repo=dataspotAPI(credentialfile=self.credentialfile,
                         reponame=self.reponame,
                         repoowner=self.repoowner)


        models=repo.getmodels()
        mymodel=[m for m in models if m.get("label")=="Information domain model"][0]
        #test= repo.dsaccess._doget(request="/schemes/Information model/uml")
        #test=repo.dsaccess.getcollections(modelname="Information model")
        test=repo.dsaccess._getelements(elemtype="attributes")
        #test= repo.dsaccess._doget(request="/schemes/Information model/classifiers/attributes")
        #entities= repo.dsaccess.getbusinessobjects(modelname="Information model")
        #attributesfiltered=repo.dsaccess.getmodelattributes(modelname="Information model",
        #            entities=[e.get("label") for e in entities])
        #attributesbymodel=repo.dsaccess.getattributes(modelid=mymodel.get("modelId"))
        repo.loadmodels(modelnamepattern="^Information.*model$")
        return

    def writejson(self,js,name):
        outfilepath=self.debugpath/f"{name}.json"
        with open(outfilepath,"w") as outfile:
            json.dump(js,outfile,indent=2)

    def test_loadmodelfiles(self):
        if not Path.exists(self.credentialfile):
            self.skipTest("\nno credentials found skip test with real credentials")

        # check default access with credentialfile
        repo=dataspotAPI(credentialfile=self.credentialfile,
                         reponame=self.reponame,
                         repoowner=self.repoowner)


        tenant=repo.gettenant()
        if tenant is not None: repo.tenantname=tenant.get("tenantName")
        models=repo.getmodels(filtercondition=lambda x: x.get("tenantId")==tenant.get("tenantId"))
        self.writejson(js=tenant,name=f"{self.repoowner}-tenant")
        self.writejson(js=models,name=f"{self.repoowner}-models")

        starturl=repo.dsaccess._basehttprequest(reqtype='api')
        for model in models:
            url=starturl + \
                f"/schemes/{model.get('id')}/download?format=json&v=3"
            # -L follows redirects, -s is silent mode
            filename=self.debugpath/f"{repo.tenantname}-{model.get('label')}.json"
            c.run(f"curl -L -s '{url}' -u '{repo.dsaccess.__un}:{repo.dsaccess.__pw}' -o {filename}")
            print(f"model saved to {filename}")

            #modelcont = repo.get1model(modelname=model.get("id"), outpath="test.json")
            #self.writejson(js=modelcont, name=f"{self.repoowner}-{model.get('label')}")




if __name__ == '__main__':
    unittest.main()
