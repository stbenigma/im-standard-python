import json
import logging
import unittest
from pathlib import Path

import pytest

from STIBO import LoadStep, Step2Dataspot, GenerateReferences, \
    GenerateDomains, GenerateDatamodel, generatemodels


class MyTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        caplog.set_level(logging.WARNING)
        self.capsys = capsys
        self.temppath = tmp_path

    def setUp(self) -> None:
        self.debugpath = Path.home() / "Downloads"
        if not self.debugpath.is_dir():
            self.debugpath=self.temppath

        self.mytestxml = Path(__file__).parent / "testfiles" / "simpletest.xml"
        if not self.mytestxml.is_file():
            self.skipTest("Testpath does not exist")
        return

    def test_simplestep(self):
        getobjs = lambda t,prop,l: [rm for rm in dsjson if rm.get("_type")== t and rm.get(prop)==l]
        getobj = lambda t,prop,l: getobjs(t,prop,l)[0]


        loadstep = LoadStep(
            stepfilepath=self.mytestxml,
            rootusertypes="^(product_usertype_root|packaging_root)$"
        )

        stepmodel=GenerateReferences(loadedstep=loadstep,
                                dsmodelname="BatteryPass")
        dsjson=stepmodel.generatedsjson()
        self.assertEqual("List Of Values group root/lovs_2",
                         getobj("ReferenceObject",
                                "label","batteryStatus").get("inCollection")
                         )
        outfilepath = Path(self.debugpath,
                           stepmodel.referencemodelname + ".json")
        with open(outfilepath, 'w') as outfile:
            json.dump(dsjson, outfile, indent=2)
            logging.info(f"Referencemodel generated into file {str(outfilepath)}")
            print(f"Referencemodel generated into file {str(outfilepath)}")

        stepmodelviasupertyp=Step2Dataspot(loadedstep=loadstep,
                                dsmodelname="BatteryPass")
        dsjsonvia=stepmodelviasupertyp.generatereferences()
        self.assertListEqual(dsjson,dsjsonvia)

        stepmodel=GenerateDomains(loadedstep=loadstep,
                                dsmodelname="BatteryPass")
        dsjson=stepmodel.generatedomains()
        outfilepath = Path(self.debugpath,
                           stepmodel.domainmodelname + ".json")
        with open(outfilepath, 'w') as outfile:
            json.dump(dsjson, outfile, indent=2)
            logging.info(f"Domainmodel generated into file {str(outfilepath)}")
            print(f"Domainmodel generated into file {str(outfilepath)}")
        dsjsonvia=stepmodelviasupertyp.generatedomains()
        self.assertListEqual(dsjson,dsjsonvia)


        stepmodel=GenerateDatamodel(loadedstep=loadstep,
                                dsmodelname="BatteryPass")
        dsjson=stepmodel.generatedsjson()
        outfilepath = Path(self.debugpath,
                           stepmodel.datamodelfullname + ".json")
        with open(outfilepath, 'w') as outfile:
            json.dump(dsjson, outfile, indent=2)
            logging.info(f"Datamodel generated into file {str(outfilepath)}")
            print(f"Datamodel generated into file {str(outfilepath)}")
        return

    def test_localstep1(self):
        testfile = Path(__file__).parent.parent.parent.parent.parent.parent \
                   / "testdata" /"localtestmodels" /"coop" \
                   / "testfile-PIM-exported-2025-03-17_10.14.09.xml"
        if not testfile.is_file():
            self.skipTest("Testpath does not exist")

        loadstep = LoadStep(
            stepfilepath=testfile,
            rootusertypes=r"^(Product user-type root|General user-type root)$"
        )

        self.assertTrue(len(loadstep.myusertypes)>0)
        generatemodels(outpath=self.debugpath,
                       dsmodelname="testfile PIMcoop",
                       loadedstep=loadstep)

        return

    def test_localstep2(self):
        testfile = Path(
            "/Users/stb/Documents/Projekte/BASF/dataspot/multifile") / "all_ots.xmlx"
        if not testfile.is_file():
            self.skipTest(f"Testfile {testfile} does not exist")

        loadstep = LoadStep(
            stepfilepath=testfile,
            rootusertypes=r"^(.*)$"
        )

        self.assertTrue(len(loadstep.myusertypes)>0)
        generatemodels(outpath=self.debugpath,
                       dsmodelname="MDM Attribute (step)",
                       loadedstep=loadstep)

        return

    def test_localstep3(self):
        testpath = Path(
                "/Users/stb/Documents/Projekte/BASF/dataspot") / "multifile"
        if not testpath.is_dir():
            self.skipTest("Testpath does not exist")

        loadstep = LoadStep(
            stepfilepath=testpath,
            rootusertypes=r"^(.*)$"
        )

        self.assertTrue(len(loadstep.myusertypes) > 0)
        generatemodels(outpath=self.debugpath,
                       dsmodelname="MDM Attribute (step)",
                       loadedstep=loadstep)
        return

    def test_localstep4(self):
        testpath = Path(
                    "/Users/stb/Documents/Projekte/BOBTDCC/dataspot") / "stepfiles"
        if not testpath.is_dir():
            self.skipTest("Testpath does not exist")

        loadstep = LoadStep(
            stepfilepath=testpath,
            rootusertypes="^(Product user-type root)$",
            debugpath=self.debugpath
        )

        generatemodels(testpath,
                       dsmodelname="BT step",loadedstep=loadstep)
        #stepmodel=GenerateReferences(loadedstep=loadstep,
        #                        dsmodelname="BT step")
        #loadstep = LoadStep(
        #    stepfilepath=testpath,
        #    datamodelname="BT step",
        #    outpath="/Users/stb/Documents/Projekte/BOBTDCC/dataspot",
            # outpath=Path.home() / "Downloads",
            #outfilebase="MDM Attribute (step)",
            #rootusertypes="^Product user-type root$"""
            # "Product hierarchy root" #"Product user-type root" #oder Product hierarchy root
        #)

        #refmodel=loadstep.generatereferences()
        #domainmodel=loadstep.generatedomains()
        #datamodel=loadstep.generatedatamodel()
        return

    def test_localstep5(self):

        testpath = Path(
            "/Users/stb/Documents/Projekte/BatteryPassDataModel/DPP/Battery/Stibo")
        testfile = testpath / "Battery DPP stibo exported-2025-09-22_13.34.06.xml"
        if not testfile.is_file():
            self.skipTest("Testfile does not exist")
            return

        loadstep = LoadStep(
            stepfilepath=testfile,
            rootusertypes="^(obj_persher_dpp_product_ingredients_root"+\
                          "|obj_ent_persher_supplier"+\
                          "|obj_ent_persher_country"+\
                            "|obj_persher_dpp_demo_root"+\
                            "|obj_persher_dpp_passport_root"+\
                          "|obj_persher_product_hierarchy_root)$",
            debugpath=self.debugpath
        )

        generatemodels(outpath=testpath,
                       dsmodelname="DIN Battery PIM",loadedstep=loadstep)

        return

if __name__ == '__main__':
    unittest.main()
