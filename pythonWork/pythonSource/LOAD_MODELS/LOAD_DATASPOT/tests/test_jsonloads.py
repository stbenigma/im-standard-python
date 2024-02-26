import unittest
from pathlib import Path
import os,pytest
from SSOT_infra.tests import integration as testsrc
from LOAD_MODELS.LOAD_DATASPOT import analyze_dataspot
from SSOT_db.IM_JSON import JSModel
from LOAD_MODELS.LOAD_INFRA import mergedbs


class TestDSMIRO(unittest.TestCase):

    @pytest.mark.integration
    def test_manualexports(self):
        curpath =  os.getcwd()
        mypath = testsrc.testmodels_dir() / testsrc.DATASPOT
        mirocredentialfile = Path.home() / ".miro" / "credentials-mirobaar.yaml"
        testboardname = "Miro API Test"
        os.chdir(mypath)
        try:
            spodjsonfile = analyze_dataspot.main(argv=[__file__,"CRM-Beispiel.json","IM-Domaenen.json",
                               "CRM-Masterdata.json","CRM-Referenzobjekte.json"])
        except:
            self.skipTest("analyzing dataspot-json-files is currently not active")

        jsonmodel=JSModel.readfromfile(spodjsonfile)
        adddsdiagram(jsonmodel,"FULL")
        jsonmodel.jsmodel = mergedbs.jsonviadbtojson(pmodel=jsonmodel, psrcname=analyze_dataspot.DATASPOTSRCNAME)
        jsonmodel.write_json("CRM-Beispiel_spod2.json")


        os.chdir(curpath)
        return

if __name__ == '__main__':
    unittest.main()
