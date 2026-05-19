import json
import os
import unittest
from pathlib import Path

import pytest

from INTERFACES.DATASPOT import exportIM2standard,Dataspot2IMJsonschema
from IM_STANDARD import remove_key_from_json, IMStandardJsonModel

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

    def getelement(self,instance,elemtype,name):
        element=[e for e in instance.get(elemtype, []) if e["name"].get('de')==name]
        return None if len(element)==0 else element[0]

    def test_ds2im_astronomie_load(self):
        inpath = Path(__file__).parent / "dataspottestfiles" / "astronomie"
        dsschema = Dataspot2IMJsonschema(indirec=inpath)
        self.assertTrue(len(dsschema.dsmodels.categories)>3)
        domacatg=[c for c in dsschema.dsmodels.categories.values() if c.get("TYPE")=="DOMAIN"]
        self.assertTrue(len(domacatg)>3)
        self.assertEqual(1,len([d for d in domacatg if d.get("label")=='Astronomische Referenzwerte']))
        self.assertTrue(len([a for a in dsschema.dsmodels.attributes.values() if a.get("_type")=="DataAttribute"])>3)
        self.assertTrue(len([a for a in dsschema.dsmodels.attributes.values() if a.get("_type")=="BusinessAttribute"])>3)
        self.assertEqual(1,len([a for a in dsschema.dsmodels.attributes.values() if a.get("label")=="Dauer"]))

        jsonstruct=dsschema.generatejson(modelname=inpath.name,
                                       modelversion="0.0",
                                       targetenv="Test",
                                       language="de",
                                       languages=["en"])
        self.assertTrue(len([a for a in jsonstruct.get("Attributes") if a["parentid"].startswith("ENTI")])>5)
        self.assertTrue(len([a for a in jsonstruct.get("Attributes") if a["parentid"].startswith("DOMA")])>5)
        self.assertEqual(0,len([a for a in jsonstruct.get("Domains") if not a["elementid"].startswith("DOMA")]))

        attr=self.getelement(jsonstruct,"Attributes","Aphel")
        self.assertFalse(attr.get("descriptive"))
        attr=self.getelement(jsonstruct,"Attributes","Umlaufdauer")
        self.assertTrue(attr.get("descriptive"))

        dauer=self.getelement(jsonstruct,"Attributes","Dauer")
        doma= self.getelement(jsonstruct,"Domains","Dezimalzahl")
        self.assertEqual(dauer["domainid"],doma.get("elementid"))
        return

    def test_ds2im_astro(self):
        inpath = Path(__file__).parent / "dataspottestfiles" / "astronomie"
        instance = exportIM2standard(inpath=inpath,
                                     outpath=self.mydebugpath / "astronomie-standard.json",
                                     modelname="Astronomie Beispiel",
                                     modelversion='0.9',
                                     targetenv="Astronomie Beispiel",
                                     language='de', languages=['en']
                                     )

        self.assertNotEqual(0, len(instance.get("Categories", [])))
        self.assertEqual("GroupDomain", self.getelement(instance, "Domains", "Umlaufdauer")["domaintype"])
        dauer = self.getelement(instance, "Attributes", "Dauer")
        self.assertIsNotNone(dauer)
        dauer = self.getelement(instance, "Attributes", "Dauer")
        doma = self.getelement(instance, "Domains", "Dezimalzahl")
        self.assertEqual(dauer.get("domainid"), doma.get("elementid"))
        self.assertEqual("NumericDomain", doma["domaintype"])

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

    def test_ds2im_astro_assets(self):
        inpath = Path(__file__).parent / "dataspottestfiles" / "astronomie-assets"
        instance = exportIM2standard(inpath=inpath,
                                     outpath=self.mydebugpath,
                                     modelname="Astronomie Assets",
                                     modelversion='0.1',
                                     targetenv="Astronomie Assets",
                                     language='de', languages=['en']
                                     )

        self.dumptodebug(filename=self.mydebugpath / "astronomie-asset-purejson.json",
                         jsonstruct=remove_key_from_json(obj=instance,
                                                         key_to_remove="additionalProps"
                                                         ))
        return

    def test_ds2im_astro_full(self):
        inpath = Path(__file__).parent / "dataspottestfiles" / "astronomie-full"
        instance = exportIM2standard(inpath=inpath,
                                     outpath=self.mydebugpath,
                                     modelname="Astronomie full",
                                     modelversion='0.1',
                                     targetenv="Astronomie full",
                                     language='de', languages=['en']
                                     )

        self.dumptodebug(filename=self.mydebugpath / "astronomie-full-purejson.json",
                         jsonstruct=remove_key_from_json(obj=instance,
                                                         key_to_remove="additionalProps"
                                                         ))
        return

    def test_ds2im_schwipsti_load(self):
        inpath = Path(__file__).parent / "dataspottestfiles" / "Schwipsti"
        dsschema = Dataspot2IMJsonschema(indirec=inpath)

        categories = [c for c in dsschema.dsmodels.categories.values() if c.get("PARENT") is not None]
        self.assertTrue(len(categories)>0)
        derivations = [c for c in dsschema.dsmodels.derivations.values()]
        self.assertTrue(len(derivations)>0)
        transformations = [c for c in dsschema.dsmodels.transformations.values()]
        self.assertTrue(len(transformations)>0)
        rules = [c for c in dsschema.dsmodels.rules.values()]
        self.assertTrue(len(rules)>0)
        mappings = [c for c in dsschema.dsmodels.mappings.values()]
        self.assertTrue(len(mappings)>0)
        translations = [c for c in dsschema.dsmodels.translations.values()]
        self.assertTrue(len(translations)>0)

        jsonstruct=dsschema.generatejson(modelname=inpath.name,
                                       modelversion="0.0",
                                       targetenv="Test",
                                       language="de",
                                       languages=["en"])
        categories2=[c for c in jsonstruct.get("Categories") if c.get("elementid") is not None]
        self.assertTrue(len(categories2)>0)
        derivations2=[c for c in jsonstruct.get("Derivations",[]) ]
        self.assertTrue(len(derivations2)>0)
        mappings2=[c for c in jsonstruct.get("Mappings",[]) ]
        self.assertEqual(len(mappings),len(mappings2))
        self.assertTrue(len(mappings2[0].get("valuemappings",[]))>0)
        transformations2= [t for t in jsonstruct.get("Transformations",[]) if not t.get("is1to1")]
        for t in transformations2:
            self.assertTrue(len(t.get("sourceelements"))!=1 or len(t.get("targetelements"))!=1)
        return

    def test_ds2im_modelmodel(self):
        inpath = Path(__file__).parent / "dataspottestfiles" / "Informationsmodell-modell"
        instance = exportIM2standard(inpath=inpath,
                                     outpath=self.mydebugpath/ "IM-standard.json",
                                     modelversion='0.9',
                                     targetenv="Informationmodel-model",
                                     language='en', languages=['de']
                                     )

        #self.assertNotEqual(0, len(instance.get("Categories", [])))

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

    def test_ds2im_status(self):
        inpath = Path(__file__).parent / "dataspottestfiles" / "Informationsmodell-modell"
        dsschema = Dataspot2IMJsonschema(indirec=inpath)

        with self.assertRaises(Exception):
            jsonstruct = dsschema.generatejson(modelname=inpath.name,
                                               modelversion="0.0",
                                               targetenv="Test",
                                               language="de",
                                               languages=["en"],
                                               status="XXL")

        jsonstructall=dsschema.generatejson(modelname=inpath.name,
                                       modelversion="0.0",
                                       targetenv="Test",
                                       language="de",
                                       languages=["en"])
        self.assertEqual(27,len(jsonstructall.get("Entities",[])))
        jsonstructall2=dsschema.generatejson(modelname=inpath.name,
                                       modelversion="0.0",
                                       targetenv="Test",
                                       language="de",
                                       languages=["en"],
                                         status="ALL")
        self.assertDictEqual(jsonstructall2,jsonstructall2)
        dsschema.dsmodels.entities['Informationsmodell/Kernmodell/Beziehungen/Beziehung']["status"]="SUBMITTED"
        dsschema.dsmodels.entities['Informationsmodell/Kernmodell/Entitäten/Attribut']["status"]="ACCEPTED"
        dsschema.dsmodels.entities['Informationsmodell/Kernmodell/Entitäten/Entität']["status"]="PUBLISHED"
        jsonstructallgtop=dsschema.generatejson(modelname=inpath.name,
                                       modelversion="0.0",
                                       targetenv="Test",
                                       language="de",
                                       languages=["en"],
                                         status="GTOP")
        self.assertEqual(2,len(jsonstructallgtop.get("Entities",[])))
        jsonstructallpubl=dsschema.generatejson(modelname=inpath.name,
                                       modelversion="0.0",
                                       targetenv="Test",
                                       language="de",
                                       languages=["en"],
                                         status="PUBL")

        self.assertEqual(1,len(jsonstructallpubl.get("Entities",[])))
        #self.dumptodebug(filename=self.mydebugpath / "informationmodel-schema-published.json",
        #                 jsonstruct=jsonstruct)
        return

    def test_ds2im_schwipsti(self):
        inpath = Path(__file__).parent / "dataspottestfiles" / "Schwipsti"
        instance = exportIM2standard(inpath=inpath,
                                     outpath=self.mydebugpath/ "Schwipsti-standard.json",
                                     modelversion='0.9',
                                     targetenv="Sandbox",
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
                                     outpath=self.mydebugpath/(modeldir.name +".json"),
                                     modelversion='0.9',
                                     targetenv=f"local test for {modeldir.name}",
                                     language='en'
                                     )

                    self.assertTrue(len(instance)<3 or len(instance.get("Categories", []))>0)

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

    def test_ds2systemlandscape(self):
        inpath = Path(__file__).parent / "dataspottestfiles" / "systemlandscape"
        if not inpath.is_dir(): self.skipTest("no localtestmodels found")
        instance = exportIM2standard(inpath=inpath,
                                     outpath=self.mydebugpath/ "sydstemlandscape.json",
                                     modelversion='0.9',
                                     targetenv="systemlandscape",
                                     language='en', languages=['de']
                                     )
        return

if __name__ == '__main__':
    unittest.main()
