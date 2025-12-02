import json
import logging
import unittest
from pathlib import Path
import pytest


from INTERFACES.DATASPOT.imstandard_dataspot.json2dataspot import Json2dataspot,json2dataspot

class Testjson2dataspot(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temppath = Path(tmp_path)

    def setUp(self) -> None:
        self.imstandardbasedirec=Path(__file__).parent.parent.parent.parent.parent.parent/ "Information-model-standard"
        self.astronomietestjsonpath =self.imstandardbasedirec / "Example models" /"Astronomie" /  "astronomie-schema.json"

        self.mydebugpath=(Path.home() / "Downloads") if  (Path.home() / "Downloads").exists() else self.temppath
        return

    def dumptodebug(self,filename,jsonstruct):
        debugpath=Path(Path.home(), "Downloads")
        if debugpath.exists():
            with open (debugpath / filename,'w') as outfile:
                json.dump(jsonstruct, outfile, indent=2)
                print('\n', debugpath / filename, " written")
        return


    def test_diverse(self):
        self.assertEqual('"abc/d"', Json2dataspot.fullescapestr("abc/d"))
        self.assertEqual('a\\"b\\"cd', Json2dataspot.escapestr('a"b"cd'))
        self.assertEqual([],Json2dataspot.custom_split(input_string=None,delimiter="/",quote='"'))
        self.assertEqual([""],Json2dataspot.custom_split(input_string="",delimiter="/",quote='"'))
        self.assertEqual(["","abc","def"],Json2dataspot.custom_split(input_string="/abc/def",delimiter="/",quote='"'))
        self.assertEqual(["ab/c","def"],Json2dataspot.custom_split(input_string="\"ab/c\"/def",delimiter="/",quote='"'))
        self.assertEqual(["","ab.c","","def"],Json2dataspot.custom_split(input_string="/ab.c//def",delimiter="/",quote='"'))
        self.assertEqual(["","abc","","def",""],Json2dataspot.custom_split(input_string="/abc/""/def/",delimiter="/",quote='"'))
        self.assertEqual("1",Json2dataspot._multiplicity(card=1,mand=True))
        self.assertEqual("0..1",Json2dataspot._multiplicity(card="1",mand=False))
        self.assertEqual("1..*",Json2dataspot._multiplicity(card="M",mand=True))
        self.assertEqual("0..*",Json2dataspot._multiplicity(card="M",mand=False))

        Json2dataspot
        return



    def test_astronomiesingle(self):
        with open(self.astronomietestjsonpath) as infile:
            testjson = json.load(fp=infile)

        json2dataspot(injson=self.astronomietestjsonpath,
                      outpath=self.mydebugpath,
                      imname="Astronomie model",
                      refdomainsname="TestReference",
                      domainsname="testdomain",
                      systemsname="Systems_model"
                      )
        return


    def test_astronomie_generated(self):
        with open(self.astronomietestjsonpath.with_stem("astronomie-schema-generated")) as infile:
            testjson = json.load(fp=infile)

        dsclass = Json2dataspot(standardjson=testjson,
                                    imname="Informationmodel",
                  refdomainsname="TestReference",
                  domainsname="testdomain")
        dsjson = dsclass.dsentityjson()
        self.assertTrue(len([elem for elem in dsjson if elem.get("_type")=="Collection"])>2)
        self.assertTrue(len([elem for elem in dsjson if elem.get("_type")=="BusinessObject"])>5)
        self.assertTrue(len([elem for elem in dsjson if elem.get("_type")=="Relationship"])>5)
        self.assertTrue(len([elem for elem in dsjson if elem.get("_type")=="BusinessObject" and elem.get("label")=="Zwergplanet"])==1)
        self.assertFalse([elem for elem in dsjson if elem.get("_type")=="BusinessAttribute" and elem.get("label")=="Aphel"][0].get("favorite"))

        dsjson=dsclass.dsdomainjson()
        self.assertTrue(len([elem for elem in dsjson if elem.get("_type")=="Collection"])>3)
        self.assertTrue(len([elem for elem in dsjson if elem.get("_type")=="DataDomain"])>6)
        self.assertTrue(len([elem for elem in dsjson if elem.get("_type")=="DataAttribute"])>6)
        self.assertFalse('Standard Referenzwerte' in [elem.get("label") for elem in dsjson if elem.get("_type")=="Collection"])

        dsjson=dsclass.dsreferencejson()
        self.assertEqual(2,len([elem for elem in dsjson if elem.get("_type")=="Collection"]))
        all_collection_names=[elem.get("label") for elem in dsjson if elem.get("_type")=="Collection"]
        self.assertEqual(len(all_collection_names),len(set(all_collection_names)))
        self.assertFalse ('Astronomie Wertebereiche' in all_collection_names)
        self.assertTrue(len([elem for elem in dsjson if elem.get("_type")=="ReferenceObject"])>3)
        self.assertTrue(len([elem for elem in dsjson if elem.get("_type")=="ReferenceValue"])>6)

        #self.dumptodebug(filename="dsentityjson.json", jsonstruct=dsjson)
        #print('\n', self.mydebugpath / "dsentityjons.json", " created")

        json2dataspot(injson=self.astronomietestjsonpath,
                      outpath=self.mydebugpath,
                      imname="Astronomie model",
                      refdomainsname="TestReference",
                      domainsname="testdomain",
                      systemsname="Systems_model"
                      )

        return

    def test_divfiles(self):
        self.caplog.set_level(logging.INFO)
        testfile=self.imstandardbasedirec/"im-model-model"/"im-model-model.json"
        if not testfile.exists():
            self.skipTest(f"file does not exist {str(testfile)}")

        json2dataspot(injson=testfile,
                      outpath=self.mydebugpath,
                      imname="IMmodelmodel",
                      refdomainsname="IMmodelmodel reference model",
                      domainsname="IMmodelmodel domain model")
        print ("\n".join(self.caplog.messages))
        return

    def test_systems(self):
        self.caplog.set_level(logging.INFO)

        testfile=self.mydebugpath / "SystemStandard-pure.json"
        if not testfile.exists():
            self.skipTest(f"file does not exist {str(testfile)}")
        json2dataspot(injson=testfile,
                      outpath=self.mydebugpath,
                      imname="IM",
                      refdomainsname="references",
                      domainsname="domains",
                      systemsname="systems")
        print ("\n".join(self.caplog.messages))
        return


if __name__ == '__main__':
    unittest.main()
