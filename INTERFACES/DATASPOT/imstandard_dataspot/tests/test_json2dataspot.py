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
        self.testjsonpath=Path(__file__).parent.parent.parent.parent/ "IM_STANDARD"/\
                          "im-schema-json" /"test-models" / \
                          "IM" / "valid" / "astronomie-1.json"
        with open(self.testjsonpath) as infile:
            self.testjson = json.load(fp=infile)

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
        self.assertEqual("1",Json2dataspot._multiplicity(card=1,mand=True))
        self.assertEqual("0..1",Json2dataspot._multiplicity(card="1",mand=False))
        self.assertEqual("1..*",Json2dataspot._multiplicity(card="M",mand=True))
        self.assertEqual("0..*",Json2dataspot._multiplicity(card="M",mand=False))

        return

    def test_astronomie(self):
        dsclass = Json2dataspot(standardjson=self.testjson,
                                    imname="Informationmodel",
                  refdomainsname="Referencemodell",
                  domainsname="Domainmodel")
        dsjson = dsclass.dsentityjson()
        self.dumptodebug(filename="dsentityjson.json", jsonstruct=dsjson)
        print('\n', self.mydebugpath / "dsentityjons.json", " created")

        json2dataspot(injson=self.testjsonpath,
                      outpath=self.mydebugpath,
                      imname="Business object model")
        return

    def test_divfiles(self):
        self.caplog.set_level(logging.INFO)
        testfilepath=Path(__file__).parent / "dataspottestfiles" / "standardjsons"
        testfile=testfilepath/"astronomie-ohneaddprops.json"
        json2dataspot(injson=testfile,
                      outpath=self.mydebugpath,
                      imname="IM",
                      refdomainsname="references",
                      domainsname="domains")
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
