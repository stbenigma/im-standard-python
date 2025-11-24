import json
import os
import unittest
from pathlib import Path

import pytest

from IM_STANDARD import remove_key_from_json, IMStandardJsonModel
from INTERFACES.DATASPOT import exportIM2standard

class Test_dataspot2im(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temppath = Path(tmp_path)

    def setUp(self) -> None:
        self.mydebugpath = (Path.home() / "Downloads") if (Path.home() / "Downloads").exists() else self.temppath
        return

    def dumpjson(self, filepath: Path, jsonstruct):
        with open(filepath, 'w') as outfile:
            json.dump(jsonstruct, outfile, indent=2)
            print('\n', filepath, " written")
        return

    def dumptodebug(self, filename, jsonstruct):
        if self.mydebugpath.exists():
            self.dumpjson(filepath=self.mydebugpath / filename,
                          jsonstruct=jsonstruct)
        return

    def test_ds2im_astronomie(self):
        inpath = Path(__file__).parent / "dataspottestfiles" / "astronomie"
        instance = exportIM2standard(inpath=inpath,
                                     outpath=self.mydebugpath,
                                     modelname="Astronomie Beispiel",
                                     modelversion='0.9',
                                     targetenv="Astronomie Beispiel",
                                     language='de', languages=['en']
                                     )

        self.assertNotEqual(0, len(instance.get("Categories", [])))

        # check generated json
        from IM_STANDARD import validateschema
        errors = validateschema(instance=instance,
                                schemafile=IMStandardJsonModel.IMDEFINITIONFILEPATH,
                                verbose=True)
        if len(errors) > 0:
            print("\n".join(errors))
            self.assertTrue(False)

        self.dumptodebug(filename=self.mydebugpath / "astronomie-schema-purejson.json",
                         jsonstruct=remove_key_from_json(obj=instance,
                                                         key_to_remove="additionalProps"
                                                         ))
        return

    def test_ds2im_modelmodel(self):
        inpath = Path(__file__).parent / "dataspottestfiles" / "Informationsmodell-modell"
        instance = exportIM2standard(inpath=inpath,
                                     outpath=self.mydebugpath,
                                     modelversion='0.9',
                                     targetenv="Informationmodel-model",
                                     language='en', languages=['de']
                                     )

        self.assertNotEqual(0, len(instance.get("Categories", [])))

        # check generated json
        from IM_STANDARD import validateschema
        errors = validateschema(instance=instance,
                                schemafile=IMStandardJsonModel.IMDEFINITIONFILEPATH,
                                verbose=True)
        if len(errors) > 0:
            print("\n".join(errors))
            self.assertTrue(False)

        self.dumptodebug(filename=self.mydebugpath / "informationmodel-schema-purejson.json",
                         jsonstruct=remove_key_from_json(obj=instance,
                                                         key_to_remove="additionalProps"
                                                         ))
        return

    def test_ds2im_schwipsy(self):
        inpath = Path(__file__).parent / "dataspottestfiles" / "Schwipsti"
        instance = exportIM2standard(inpath=inpath,
                                     outpath=self.mydebugpath,
                                     modelversion='0.9',
                                     targetenv="Standard example of dataspot environment",
                                     language='de'
                                     )

        self.assertNotEqual(0, len(instance.get("Categories", [])))

        # check generated json
        from IM_STANDARD import validateschema
        errors = validateschema(instance=instance,
                                schemafile=IMStandardJsonModel.IMDEFINITIONFILEPATH,
                                verbose=True)
        if len(errors) > 0:
            print("\n".join(errors))
            self.assertTrue(False)

        return

    def test_ds2im_localtestmodels(self):
        inpath = Path(__file__).parent.parent.parent.parent.parent / "localtestmodels"
        if not inpath.is_dir(): self.skipTest("no localtestmodels found")
        with os.scandir(inpath) as testmodels:
            for modeldir in testmodels:
                if modeldir.is_dir():
                    instance = exportIM2standard(inpath=Path(modeldir.path),
                                     outpath=self.mydebugpath,
                                     modelversion='0.9',
                                     targetenv=f"local test for {modeldir.name}",
                                     language='en'
                                     )

                    self.assertNotEqual(0, len(instance.get("Categories", [])))

                    # check generated json
                    from IM_STANDARD import validateschema
                    errors = validateschema(instance=instance,
                                            schemafile=IMStandardJsonModel.IMDEFINITIONFILEPATH,
                                            verbose=True)
                    if len(errors) > 0:
                        print (f"ERROR in {modeldir.name}")
                        print("\n".join(errors))
                        self.assertTrue(False)

        return

if __name__ == '__main__':
    unittest.main()
