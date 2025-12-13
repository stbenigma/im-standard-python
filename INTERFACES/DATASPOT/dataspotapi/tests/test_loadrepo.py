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



if __name__ == '__main__':
    unittest.main()
