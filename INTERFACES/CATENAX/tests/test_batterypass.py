import unittest

import pytest

from CATENAX import *


class MyTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        caplog.set_level(logging.WARNING)
        self.capsys = capsys

    def setUp(self) -> None:

        self.githubpath = Path.home() / Path("Documents/Projekte/BatteryPassDataModel/gitHubmodels/")
        self.tractusx_schemapath = self.githubpath / "tractus-x sldt-semantic-models"
        self.din_schemapath = self.githubpath / "DIN BatteryPassDataModel" /"BatteryPass"

        self.debugpath = Path.home() / "Downloads"

    def test_filestruct(self):
        with os.scandir(self.tractusx_schemapath) as direcs:
            for iodirec in direcs:
                # print(iodirec.name)
                if iodirec.name == "io.catenax.battery.battery_pass":
                    with os.scandir(self.tractusx_schemapath / iodirec.name) as localdirec:
                        latest = max([locdirec.name for locdirec in localdirec
                                      if (not locdirec.is_file() and \
                                          re.match(r"^\d+\.\d+\.\d+$", locdirec.name))])
                    with os.scandir(self.tractusx_schemapath / iodirec.name / (latest + "/gen")) as myversion:
                        for model in myversion:
                            if re.match(r"^[a-zA-Z]+-schema.json$", model.name):
                                self.assertEqual("BatteryPass-schema.json", model.name)

        file = CatenaxFiles.findfile(basepath=self.tractusx_schemapath / "io.catenax.battery.battery_pass",
                                     modelname="BatteryPass")
        self.assertEqual("BatteryPass-schema.json", file[0].name)
        file = CatenaxFiles.findfile(basepath=self.tractusx_schemapath / "io.catenax.battery.battery_pass",
                                     modelname="BatteryPass", version="6.0.0")
        self.assertEqual(
            self.tractusx_schemapath / "io.catenax.battery.battery_pass" / "6.0.0" / "gen" / "BatteryPass-schema.json",
            file[0])
        file = CatenaxFiles.findfile(basepath=self.tractusx_schemapath / "io.catenax.battery.battery_pass",
                                     modelname="BatteryPass", version="6.x.1")
        self.assertEqual([], file)
        file = CatenaxFiles.findfile(basepath=self.tractusx_schemapath / "io.catenax.battery.battery_passXXX",
                                     modelname="BatteryPass")
        self.assertEqual([], file)
        return

    def test_onefile(self):
        rootfile = CatenaxFiles.findfile(basepath=self.tractusx_schemapath / "io.catenax.battery.battery_pass")
        myjson = CatenaxFiles.read1file(filepath=rootfile)

        return

    def test_tractus_batterypass(self):
        grpattrlist = ["^KeyValueList$",
                       "^RecordCharacteristic$",
                       "^lifespanEntity$",
                       "^CapacityCharacteristic$",
                       "^EnergyCharacteristic$",
                       "^RemainingPowerCharacteristic$",
                       "^RemainingResistanceCharacteristicRecord$",
                       "^FullCycleCharacteristic$",
                       "^DocumentationEntity$",
                       "^DocumentEntity$",
                       "^TimeCharacteristic$",
                       "^WarrantyCharacteristic$",
                       "^AreaCharacteristic$",
                       "^CountQuantityCharacteristic$",
                       "^ItemQuantityCharacteristic$",
                       "^LinearCharacteristic$",
                       "^MassCharacteristic$",
                       "^MiscQuantityCharacteristic$",
                       # "^SitesEntity$",
                       # "^ManufacturingCharacteristic$",
                       "^RangeEntity$",
                       "^LifespanEntity$",
                       "^PhysicalDimensionCharacteristic$",
                       "^PerformanceTemperatureCharacteristic$",
                       "^CodeEntity$",
                       "^RatedEnergyCharacteristic$",
                       "^VoltageCharacteristic$",
                       "^VolumeCharacteristic$"
                       ]
        rootfile = CatenaxFiles.findfile(basepath=self.tractusx_schemapath / "io.catenax.battery.battery_pass")
        ctxload = CTXLoadJson(basepath=str(self.tractusx_schemapath),
                              allfiles=[str(rootfile)])

        ctxanalyzed = CTXAnalyzeJson(models=ctxload.models,grpattrlist=[])
        #ctxanalyzed = CTXAnalyzeJson(models=ctxload.models,grpattrlist=grpattrlist)

        ctxgen = CTXGenerateDSJson(models=ctxload.models,
                                   analyzedelements=ctxanalyzed.elements,
                                   datamodelname="BatteryPass",
                                   outfilebase=self.debugpath,
                                   intermediateoutputfile="intermediate.json"
                                   )

        ctxgen.generateDSmodels()

        return

    def test_din_batterypass(self):
        grpattrlist = ["^KeyValueList$",
                       "^RecordCharacteristic$",
                       "^lifespanEntity$",
                       "^CapacityCharacteristic$",
                       "^EnergyCharacteristic$",
                       "^RemainingPowerCharacteristic$",
                       "^RemainingResistanceCharacteristicRecord$",
                       "^FullCycleCharacteristic$",
                       "^DocumentationEntity$",
                       "^DocumentEntity$",
                       "^TimeCharacteristic$",
                       "^WarrantyCharacteristic$",
                       "^AreaCharacteristic$",
                       "^CountQuantityCharacteristic$",
                       "^ItemQuantityCharacteristic$",
                       "^LinearCharacteristic$",
                       "^MassCharacteristic$",
                       "^MiscQuantityCharacteristic$",
                       # "^SitesEntity$",
                       # "^ManufacturingCharacteristic$",
                       "^RangeEntity$",
                       "^LifespanEntity$",
                       "^PhysicalDimensionCharacteristic$",
                       "^PerformanceTemperatureCharacteristic$",
                       "^CodeEntity$",
                       "^RatedEnergyCharacteristic$",
                       "^VoltageCharacteristic$",
                       "^VolumeCharacteristic$"
                       ]
        grpattrlist=["TemperatureRangeIdleState"]
        allfiles = CatenaxFiles.findfiles(basepath=self.din_schemapath,
                                         elementregexp="^io\.BatteryPass\.[a-zA-Z0-9]+$")
        #allfiles.remove(Path('/Users/stb/Documents/Projekte/BatteryPassDataModel/gitHubmodels/DIN BatteryPassDataModel/BatteryPass/io.BatteryPass.SupplyChainDueDiligence/1.2.0/gen/SupplyChainDueDiligence-schema.json'))
        #allfiles.remove(Path('/Users/stb/Documents/Projekte/BatteryPassDataModel/gitHubmodels/DIN BatteryPassDataModel/BatteryPass/io.BatteryPass.CarbonFootprint/1.2.0/gen/CarbonFootprintForBatteries-schema.json'))
        #allfiles.remove(Path("/Users/stb/Documents/Projekte/BatteryPassDataModel/gitHubmodels/DIN BatteryPassDataModel/BatteryPass/io.BatteryPass.Labels/1.2.0/gen/Labeling-schema.json"))
        #allfiles.remove(Path("/Users/stb/Documents/Projekte/BatteryPassDataModel/gitHubmodels/DIN BatteryPassDataModel/BatteryPass/io.BatteryPass.Circularity/1.2.0/gen/Circularity-schema.json"))
        #allfiles=[Path('/Users/stb/Documents/Projekte/BatteryPassDataModel/gitHubmodels/DIN BatteryPassDataModel/BatteryPass/io.BatteryPass.SupplyChainDueDiligence/1.2.0/gen/SupplyChainDueDiligence2-schema.json')]
        #allfiles=[Path('/Users/stb/Documents/Projekte/BatteryPassDataModel/gitHubmodels/DIN BatteryPassDataModel/BatteryPass/io.BatteryPass.GeneralProductInformation/1.2.0/gen/GeneralProductInformation-schema.json')]
        #allfiles = CatenaxFiles.findfile(basepath=self.din_schemapath / "io.BatteryPass.GeneralProductInformation",
        #                                 modelname="GeneralProductInformation")
        ctxload = CTXLoadJson(basepath=str(self.din_schemapath),
                              allfiles=allfiles)

        ctxanalyzed = CTXAnalyzeJson(models=ctxload.models,grpattrlist=[])
        #ctxanalyzed = CTXAnalyzeJson(models=ctxload.models,grpattrlist=grpattrlist)

        ctxgen = CTXGenerateDSJson(models=ctxload.models,
                                   analyzedelements=ctxanalyzed.elements,
                                   datamodelname="Battery Model (DIN, samm)",
                                   outfilebase=self.debugpath,
                                   intermediateoutputfile="intermediate.json"
                                   )

        ctxgen.generateDSmodels()

        return

    def test_batterypassanalyze(self):
        rootfile = CatenaxFiles.findfile(basepath=self.tractusx_schemapath / "io.catenax.battery.battery_pass")
        ctxload = CTXLoadJson(basepath=str(self.tractusx_schemapath),
                              allfiles=[rootfile])

        ctxanalyzed = CTXAnalyzeJson(models=ctxload.models)
        self.assertTrue(len(ctxanalyzed.elements["collections"]) == 3)

        grpattrlist = ["^KeyValueList$",
                       "^RecordCharacteristic$",
                       "^lifespanEntity$",
                       "^CapacityCharacteristic$",
                       "^EnergyCharacteristic$",
                       "^RemainingPowerCharacteristic$",
                       "^RemainingResistanceCharacteristicRecord$",
                       "^FullCycleCharacteristic$",
                       "^DocumentationEntity$",
                       "^TimeCharacteristic$"
                       ]

        ctxanalyzednew = CTXAnalyzeJson(models=ctxload.models,
                                        grpattrlist=["^KeyValueList",
                                                     "^RecordCharacteristic",
                                                     "^lifespanEntity"
                                                     ]
                                        )
        self.assertTrue(len(ctxanalyzednew.elements["groupattributes"]) > 0)

        return


if __name__ == '__main__':
    unittest.main()
