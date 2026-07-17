import json
import unittest
from pathlib import Path
import pytest
import tempfile

from IM_STANDARD import JsonSchema,standardmodeljson as smjs

from INTERFACES.DATASPOT.imstandard_dataspot import DataspotElements,ElementId, ds2dmstandard as d2j, json2dataspot as j2d


class Testjson2dataspot(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temppath = Path(tmp_path)

    def setUp(self) -> None:
        self.testjsonpath=Path(__file__).parent.parent.parent/ "IM_STANDARD"/\
                          "im-schema-json" /"test-models" / \
                          "DM" / "valid" / "standarddatamodel.json"
        self.mydebugpath=(Path.home() / "Downloads") if  (Path.home() / "Downloads").exists() else self.temppath
        return

    def dumptodebug(self,filename,jsonstruct):
        debugpath=Path(Path.home(), "Downloads")
        if debugpath.exists():
            with open (debugpath / filename,'w') as outfile:
                json.dump(jsonstruct, outfile, indent=2)
                print('\n', debugpath / filename, " written")
        return


    def test_fullDS2SSOD(self):
        self.skipTest(f"to be cleared")
        path = Path("/testdata/localtestmodels/dataspotforyoumodels")
        path = Path("/Users/stb/Documents/Projekte/FYAYC_intern/webapp/api/chem-x")
        #path = Path("/Users/stb/Documents/Projekte/FYAYC_intern/webapp/api/basf-agriculture")
        with tempfile.TemporaryDirectory() as tempdir:
            dsschema = d2j.Dataspot2Jsonbase(standardjson=JsonSchema(),indirec=path)
            jsonstruct = dsschema.generatejson(targetenv=path.__str__().split("/")[-1])
            self.dumptodebug(filename="dataspotstandard.json",jsonstruct=jsonstruct)
            with open(Path(tempdir) / "dataspotstandard.json", "w") as outfile:
                json.dump(jsonstruct, outfile, indent=2)
            smjs.validateschema(instance=jsonstruct, schemafile=Path(tempdir) / "dataspotstandard.json",
                                verbose=True,schemaonly=True)
            return
            j2d.json2dataspot(injson=Path(tempdir) / "dataspotstandard.json",
                              outpath=Path(tempdir))

            j2d.json2dataspot(injson=Path(tempdir) / "dataspotstandard.json",
                              outpath=Path.home() / "Downloads")

        return

    def testswipsyroundtrip(self):
        self.skipTest(f"to be cleared")
        path1 = Path("dataspottestfiles/Schwipsti")
        with tempfile.TemporaryDirectory() as tempdir:
            dsschema = d2j.Dataspot2IMJsonschema(path1)
            jsonstruct = dsschema.generatejson(modelname=path1.name)
            self.dumptodebug(filename="dataspotstandard.json",jsonstruct=jsonstruct)
            with open(Path(tempdir) / "dataspotstandard.json", "w") as outfile:
                json.dump(jsonstruct, outfile, indent=2)
                smjs.validateschema(instance=jsonstruct, schemafile=Path(tempdir) / "dataspotstandard.json",
                                    verbose=True,schemaonly=True)

            j2d.json2dataspot(injson=Path(tempdir) / "dataspotstandard.json",
                              outpath=Path(tempdir))

            j2d.json2dataspot(injson=Path(tempdir) / "dataspotstandard.json",
                              outpath=Path.home() / "Downloads")

        return

    def test_dataspot2dm(self):
        self.skipTest(f"dm not yet handled")
        file4 = Path("dataspottestfiles/Datamodels/destination datamodel.json")
        dsschema = d2j.Dataspot2DMJsonschema()
        dsschema.dsmodels.readmodels(file4)
        self.assertTrue(len(dsschema.dsmodels.tables)>0)


        path1 = Path("dataspottestfiles/Schwipsti")
        ElementId.reset()
        dsschema = d2j.Dataspot2DMJsonschema()
        dsschema.dsmodels.readmodels(path1)
        self.assertTrue(len(dsschema.dsmodels.tables)>0)

        jsonstructdm = dsschema.generatejson(modelname="MyModelname")
        purejson=jsonstructdm.getjsonmodel()
        self.dumptodebug(filename=f"{purejson.get('ModelInfo').get('modelName')}.json", jsonstruct=purejson)
        with tempfile.TemporaryDirectory() as tempdir:
            with open(Path(tempdir) / f"{purejson.get('ModelInfo').get('modelName')}.json", "w") as outfile:
                json.dump(purejson, outfile, indent=2)

            if not smjs.validateschema(instance=purejson,
                                       schemafile=smjs.ValidateJsonModel.DMschemajson,
                                       verbose=False):
                errors=self.caplog.messages
                assert len(errors)==1

        return

    def test_dataspotelements(self):
        locpath="/Users/stb/Library/CloudStorage/GoogleDrive-stb@foryouandyourcustomers.com/Geteilte Ablagen/C/HD/BASF/BASFAPM - BASF Agricultural ADAM/04_Docs fyayc/dataspot/"
        file1 = Path(locpath+"MDM Attribute (step) references.json")
        file2 = Path(locpath+"MDM Attribute (step) domains.json")
        file3 = Path(locpath+"MDM Attribute (step) datamodel.json")
        dsmodels = DataspotElements()
        dsmodels.readmodels(file1)
        dsmodels.readmodels(file2)
        self.assertTrue(len(dsmodels.LOVvalues)==0)
        self.assertTrue(len(dsmodels.categories)>0)
        self.assertTrue(len(dsmodels.domains)>0)

        dsmodels = DataspotElements(file3)
        self.assertTrue(len(dsmodels.domains) == 0)
        self.assertTrue(len(dsmodels.deployments) > 0)
        self.assertTrue(len(dsmodels.tables) > 0)
        self.assertEqual(file3.stem ,
                         dsmodels.tables[next(iter(dsmodels.tables))].get("DSMODEL"))
        self.assertTrue(next(iter(dsmodels.tables)).startswith (file3.stem+"/"))

        path1 = Path("dataspottestfiles/Schwipsti")
        dsmodels = DataspotElements(path1)
        self.assertTrue(len(dsmodels.LOVvalues)>0)
        self.assertTrue(len(dsmodels.entities)>0)
        return

    def test_localds2json(self):
        #locpath="/Users/stb/Library/CloudStorage/GoogleDrive-stb@foryouandyourcustomers.com/Geteilte Ablagen/C/HD/BASF/BASFAPM - BASF Agricultural ADAM/04_Docs fyayc/dataspot/"
        locpath="/Users/stb/Library/CloudStorage/GoogleDrive-stb@foryouandyourcustomers.com/Geteilte Ablagen/C/HD/BASF/BASFDMP - CHEM-X/Docs fyayc/datraspot exports/tooltest/"
        if not Path(locpath).exists():
            self.skipTest("local test not done remotely")
        file1 = Path(locpath+"Information reference model.json")
        file2 = Path(locpath+"Information domain model.json")
        file3 = Path(locpath+"DMP Definition.json")
        dsschema = d2j.Dataspot2DMJsonschema()
        dsschema.dsmodels.readmodels(file1)
        dsschema.dsmodels.readmodels(file2)
        dsschema.dsmodels.readmodels(file3)
        self.assertTrue(len(dsschema.dsmodels.tables)>0)
        self.assertTrue(len(dsschema.dsmodels.columns)>0)
        jsonstructim = dsschema.generatejson(modelname="mdmtestdataspot",targetenv="CHEM-X")

        self.dumptodebug(filename="mdmtestdataspot.json", jsonstruct=jsonstructim)

        for k,v in jsonstructim.items():
            print (k,len(v))
            if k=="Tables":
                print ("Attributes",sum(len(t.get("columns")) for t in v))

        #if not smjs.validateschema(instance=jsonstructim, verbose=True):
        #    errors=self.caplog.messages
        #    assert len(errors)==1

        return


if __name__ == '__main__':
    unittest.main()
