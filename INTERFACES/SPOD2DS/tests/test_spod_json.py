import json
import tempfile
import unittest
from pathlib import Path

import openapi_schema_validator as osv
import pytest

from INTERFACES.SPOD2DS  import JSModel
from INTERFACES.SPOD2DS import Spod2Jsonschema
from IM_STANDARD import standardmodeljson as smjs, remove_key_from_json,validateschema,IMStandardJsonModel,model2json
from INTERFACES.DATASPOT.imstandard_dataspot.json2dataspot import Json2dataspot, json2dataspot


class TestModelSchema(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temppath = Path(tmp_path)

    def setUp(self) -> None:
        myroot=Path(__file__).parent.parent.parent.parent.parent
        self.basepath =  myroot / "Information-model-standard"
        self.schemadefpath =  self.basepath / "im-standard"
        self.imdeffilename="InformationModel-schema.json"

        self.myschemafile = IMStandardJsonModel.IMDEFINITIONFILEPATH
        with open(self.myschemafile) as infile:
            self.myschemajs = json.load(fp=infile)
        self.mydebugpath = (Path.home() / "Downloads") \
            if (Path.home() / "Downloads").exists() \
            else self.temppath
        return

    def spodsetup(self):
        #self.tm1 = integration.ModelHelper(integration.TESTMODEL1)
        #self.tm1jsmodel = JSModel.readfromfile(self.tm1.jsonfile)
        #self.crm = integration.ModelHelper(integration.CRMTEST)
        #self.crmjsmodel = JSModel.readfromfile(self.crm.jsonfile)
        return

    def test_standardIMmodel(self):
        imstandardmodelfilepath = Path("/Users/stb/Documents/Projekte/IM-Standard/ODM/DB/IM-standard.json")
        if not imstandardmodelfilepath.is_file():
            self.skipTest(f"local im {imstandardmodelfilepath.stem} standardfile not found")
        imstandardmodel = JSModel.readfromfile(imstandardmodelfilepath)
        spodschema = Spod2Jsonschema(jsmodel=imstandardmodel)
        instance = spodschema.generatestandardjson(modeltype="Information model",
                                                   targetenv="Standard IM",
                                                   description=None)
        puremodel=model2json(instance.jsonschemamodel)
        self.assertTrue(len(validateschema(instance=puremodel,
                                                schemafile=self.myschemafile,
                                                verbose=True,
                                                schemaonly=True))==0
                         )
        self.assertTrue(0==len(validateschema(instance=puremodel,
                                            schemafile=self.myschemafile,
                                            verbose=True,
                                            schemaonly=False))
                        )
        if self.mydebugpath.exists():
            debugfile = self.mydebugpath / 'imstandardstandardjson.json'
            with open(debugfile, 'w') as outfile:
                json.dump(puremodel, outfile, indent=2)
                print('\n', debugfile, " written")
        debugfile = self.mydebugpath / 'imstandardstandardjson-pure.json'
        with open(debugfile, 'w') as outfile:
            json.dump(remove_key_from_json(obj=puremodel,
                                           key_to_remove="additionalProps"
                                           )
                      , outfile, indent=2)
            print('\n', debugfile, " written")
        return

    def test_oevIMmodel(self):
        imstandardmodelfilepath = Path(
            "/Users/stb/Documents/Projekte/FYAYC_intern/fyyccim-refmodels/OeV/DB/vdv-oev.json")
        if not imstandardmodelfilepath.is_file():
            self.skipTest(f"local im {imstandardmodelfilepath.stem} standardfile not found")
        imstandardmodel = JSModel.readfromfile(imstandardmodelfilepath)
        imstandardmodel.jsmodel["domains"]["DOMA999"] = \
            {"name": "Test Group",
             "type": "GRP",
             "elements": [{"elementid": "ATTR999",
                           "name": "DomainAttr1",
                           "mandatory": True,
                           "descr": "descr des 1. Attributes",
                           "domainid": "DOMA10"},
                          {"elementid": "ATTR998",
                           "name": "DomainAttr2",
                           "mandatory": True,
                           "descr": {"en": "descr of second Attribute",
                                           "de": "descr des zweiten Attr."},
                           "domainid": "DOMA13"
                           }
                          ]
             }
        spodschema = Spod2Jsonschema(jsmodel=imstandardmodel)
        instance = spodschema.generatestandardjson(modeltype="Information model",
                                                   targetenv="Standard IM",
                                                   description=None)
        puremodel=model2json(instance.jsonschemamodel)
        self.assertTrue(validateschema(instance=puremodel,
                                                schemafile=IMStandardJsonModel.IMDEFINITIONFILEPATH,
                                                verbose=True,
                                                schemaonly=True))

        self.assertTrue(validateschema(instance=puremodel,
                                            schemafile=IMStandardJsonModel.IMDEFINITIONFILEPATH,
                                            verbose=True,
                                            schemaonly=False))

        if self.mydebugpath.exists():
            debugfile = self.mydebugpath / 'vdv-oev-standardim.json'
            with open(debugfile, 'w') as outfile:
                json.dump(puremodel, outfile, indent=2)
                print('\n', debugfile, " written")

            debugfile = self.mydebugpath / 'vdv-oev-standardim-pure.json'
            with open(debugfile, 'w') as outfile:
                json.dump(remove_key_from_json(obj=puremodel,
                                               key_to_remove="additionalProps"
                                               ), outfile, indent=2)
                print('\n', debugfile, " written")
        return

    def test_myMmodels(self):
        for imstandardmodelfilepath in [#Path("/Users/stb/Documents/Projekte/BOBTDCC/DB/BOSCH_BT_ENG.json"),
                    # Path("/Users/stb/Documents/Projekte/GEBININF/DB/IM_GEBERIT.json")
            #Path("/Users/stb/Documents/Projekte/FYAYC_intern/FYAIM/DB/FYAYC_intern_GTOP.json"),
            #Path("/Users/stb/Documents/Projekte/FYAYC_intern/fyyccim-ModellModell/gitHub/DB/ModellModell_neu.json")
            Path("/Users/stb/Documents/Projekte/BASF/gitHub/DB/BASFMDM.json")
        ]:
            if not imstandardmodelfilepath.is_file():
                print (f"local im {imstandardmodelfilepath.stem} standardfile not found")
                continue
            imstandardmodel = JSModel.readfromfile(imstandardmodelfilepath)
            spodschema = Spod2Jsonschema(jsmodel=imstandardmodel)
            instance = spodschema.generatestandardjson(modeltype="Information model",
                                                       targetenv="Standard IM",
                                                       description=None)

            purejson=model2json(instance.jsonschemamodel)
            if self.mydebugpath.exists():
                debugfile = self.mydebugpath / (imstandardmodelfilepath.stem + '-standard.json')
                with open(debugfile, 'w') as outfile:
                    json.dump(purejson, outfile, indent=2)
                    print('\n', debugfile, " written")

                json2dataspot(injson=debugfile,
                              outpath=self.mydebugpath,
                              imname=imstandardmodelfilepath.stem,
                              refdomainsname=imstandardmodelfilepath.stem + " reference",
                              domainsname=imstandardmodelfilepath.stem + " domain",
                              systemsname=imstandardmodelfilepath.stem + " system"
                              )

                debugfile = self.mydebugpath / (imstandardmodelfilepath.stem +'-standard-pure.json')
                with open(debugfile, 'w') as outfile:
                    json.dump(remove_key_from_json(obj=purejson,
                                                   key_to_remove="additionalProps"
                                                   ), outfile, indent=2)
                    print('\n', debugfile, " written")

                json2dataspot(injson=debugfile,
                              outpath=self.mydebugpath,
                              imname=imstandardmodelfilepath.stem,
                              refdomainsname=imstandardmodelfilepath.stem + " reference",
                              domainsname=imstandardmodelfilepath.stem + " domain",
                              systemsname=imstandardmodelfilepath.stem + " system"
                              )

            self.assertTrue(validateschema(instance=purejson,
                                                    schemafile=IMStandardJsonModel.IMDEFINITIONFILEPATH,
                                                    verbose=True,
                                                        schemaonly=True)

                             )
            self.assertTrue(validateschema(instance=purejson,
                                                schemafile=IMStandardJsonModel.IMDEFINITIONFILEPATH,
                                                verbose=True,
                                                schemaonly=False)
                            )
        return


if __name__ == '__main__':
    unittest.main()
