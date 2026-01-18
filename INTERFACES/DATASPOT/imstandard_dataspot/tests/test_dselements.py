import json
import unittest
from pathlib import Path
import pytest

from INTERFACES.DATASPOT.imstandard_dataspot import dselements as dse,Dataspot2Jsonbase


class Testjson2dataspot(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys

    def setUp(self) -> None:
        return

    def dumptodebug(self,filename,jsonstruct):
        debugpath=Path(Path.home(), "Downloads")
        if debugpath.exists():
            with open (debugpath / filename,'w') as outfile:
                json.dump(jsonstruct, outfile, indent=2)
                print('\n', debugpath / filename, " written")
        return

    def test_dataspotelements(self):

        path1 = Path("dataspottestfiles/schwipsti")
        dsschema = dse.DataspotElements(path1)
        self.assertTrue(len(dsschema.LOVvalues)>0)
        self.assertTrue(len(dsschema.entities)>0)
        return

    def test_named_paths(self):
        self.assertTupleEqual((None,None,None),Dataspot2Jsonbase.namedreference2struct(None))
        self.assertTupleEqual((None,[],""),Dataspot2Jsonbase.namedreference2struct(""))
        self.assertTupleEqual((None,[],"abcd"),Dataspot2Jsonbase.namedreference2struct("abcd"))
        self.assertTupleEqual((None,[],"ab/cd"),Dataspot2Jsonbase.namedreference2struct('"ab/cd"'))
        self.assertTupleEqual((None,["path1"],"ab/cd"),Dataspot2Jsonbase.namedreference2struct('path1/"ab/cd"'))
        self.assertTupleEqual((None,["path1","path/2"],"ab/cd"),Dataspot2Jsonbase.namedreference2struct('path1/"path/2"/"ab/cd"'))
        self.assertTupleEqual(("model",["path1","path/2"],"ab/cd"),Dataspot2Jsonbase.namedreference2struct('/model/path1/"path/2"/"ab/cd"'))
        self.assertTupleEqual(("model",[],"ab/cd"),Dataspot2Jsonbase.namedreference2struct('/model/"ab/cd"'))
        self.assertTupleEqual(("",[],"ab/cd"),Dataspot2Jsonbase.namedreference2struct('//"ab/cd"'))

        self.assertEqual("",Dataspot2Jsonbase.refparts2namedreference(modelname=None,elementpath=None,elementname=None))
        self.assertEqual("abcd",Dataspot2Jsonbase.refparts2namedreference(modelname=None,elementpath=None,elementname="abcd"))
        self.assertEqual("abcd",Dataspot2Jsonbase.refparts2namedreference(elementname="abcd"))
        self.assertEqual('"ab.cd"',Dataspot2Jsonbase.refparts2namedreference(modelname=None,elementpath=None,elementname="ab.cd"))
        self.assertEqual('"ab/.cd"',Dataspot2Jsonbase.refparts2namedreference(modelname=None,elementpath=None,elementname="ab/.cd"))
        self.assertEqual('model:abcd',Dataspot2Jsonbase.refparts2namedreference(modelname="model",elementpath=None,elementname="abcd"))
        self.assertEqual('model:abcd',Dataspot2Jsonbase.refparts2namedreference(modelname="model",elementpath=[],elementname="abcd"))
        self.assertEqual('model:x/abcd',Dataspot2Jsonbase.refparts2namedreference(modelname="model",elementpath=["x"],elementname="abcd"))
        self.assertEqual('model:x/"mit/ und \\"und . "/abcd',Dataspot2Jsonbase.refparts2namedreference(modelname="model",elementpath=["x","mit/ und \"und . "],elementname="abcd"))
        self.assertEqual(':x/abcd',Dataspot2Jsonbase.refparts2namedreference(modelname="",elementpath=["x"],elementname="abcd"))
        self.assertEqual('x/abcd',Dataspot2Jsonbase.refparts2namedreference(modelname=None,elementpath=["x"],elementname="abcd"))
        self.assertEqual('x/abcd',Dataspot2Jsonbase.refparts2namedreference(elementpath=["x"],elementname="abcd"))

        self.assertEqual('Y:x/abcd',Dataspot2Jsonbase.addmodeltonamedreference(namedref="x/abcd",modelname="Y"))
        self.assertEqual('Y:x/abcd', Dataspot2Jsonbase.addmodeltonamedreference(namedref="/Y/x/abcd", modelname="Z"))
        self.assertEqual('Y:abcd', Dataspot2Jsonbase.addmodeltonamedreference(namedref="/Y/abcd", modelname="Z"))
        self.assertEqual('Z:abcd', Dataspot2Jsonbase.addmodeltonamedreference(namedref="abcd", modelname="Z"))

if __name__ == '__main__':
    unittest.main()
