import shutil
import tempfile
import unittest
import pytest
import os

from LOAD_MODELS.LOAD_DATASPOT import *
from LOAD_MODELS.LOAD_INFRA import mergedbs
from SSOT_db import createDB
from tools.excel.datamapping import listmapping
from IM_WEB import listWebdoku
from LOAD_MODELS.LOAD_MIRO import diagram2miro


class DataspotTesting(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temp_folder = Path(tmp_path)
        self.debugpath = Path.home() / "Downloads"  # try local debug path
        if not self.debugpath.is_dir():
            # write to tempfolder
            self.debugpath = self.temp_folder / "debug"
            self.debugpath.mkdir(exist_ok=True)
        logging.warning(f"Using {self.debugpath.resolve()} as temporary folder")

    def setUp(self) -> None:
        self.fyaycrepo = 'https://partner.dataspot.io'
        self.fyaycrepodb = "foryouandyourcustomers"
        self.fyayctenantname = "foryouandyourcustomers"
        self.dstenantname = "Basis - Schwipsti GmbH"
        self.username = ""
        self.password = ''

    def test_elements(self):
        cat = DSCategory(tenant=DSTenant(lang="de", tenantname="irgendwer"),
                         catg={
                             "_type": "Collection",
                             "id": "38dd379c-19ad-4684-a4a4-d64a1b1c0ca0",
                             "href": "/web/foryouandyourcustomers-ch/collections/38dd379c-19ad-4684-a4a4-d64a1b1c0ca0",
                             "label": "Allg. Informationen",
                             "stereotype": "category",
                             "favorite": "true",
                             "status": "WORKING",
                             "createdBy": "sberner",
                             "dateCreated": 1683899027202,
                         })
        return

    def test_good_access(self):
        if not Path.exists(dsrequests.DSAccess.DEFAULT_CREDENTIALS):
            self.skipTest("\nno credentials found skip test with real credentials")

        # check default access with credentialfile
        try:
            dsaccess = dsrequests.DSAccess(repository=self.fyaycrepo,
                                           repoowner=self.fyaycrepodb,
                                           viaazure=True)
        except Exception as e:
            self.skipTest("No access to dataspot-repository")
        dsaccess = dsrequests.DSAccess(repository=self.fyaycrepo, repoowner=self.fyaycrepodb,
                                       tenantname=self.fyayctenantname, viaazure=True)
        with self.assertRaises(Exception) as exp:
            # unknown tenant
            dsaccess = dsrequests.DSAccess(repository=self.fyaycrepo, repoowner=self.fyaycrepodb,
                                           tenantname="blabla")

        # my copy of credential file
        with tempfile.TemporaryDirectory() as td:
            shutil.copyfile(dsrequests.DSAccess.DEFAULT_CREDENTIALS, td + "/credfile")
            dsaccess = dsrequests.DSAccess(repository=self.fyaycrepo, repoowner=self.fyaycrepodb,
                                           credentialfile=td + "/credfile", viaazure=True)

        # illegal opwner
        # with self.assertRaises(Exception) as exp:
        #    dsaccess = dsrequests.DSAccess(repository=self.fyaycrepo, repoowner="blabla")

    def test_no_access(self):
        # illegal credential file
        with self.assertRaises(Exception) as exp:
            dsaccess = dsrequests.DSAccess(credentialfile="blalba.bla", repository=None, repoowner=None, username="a",
                                           password="b")

        # illegal yaml file content
        with tempfile.TemporaryDirectory() as td:
            with open(td + "/cred.yaml", "w") as cred:
                cred.write("foryouandyourcustomers: {user: xxx, password: yyy}")
                cred.close()
            with self.assertRaises(Exception) as exp:
                dsaccess = dsrequests.DSAccess(repository=self.fyaycrepo, repoowner=self.fyaycrepodb,
                                               credentialfile=td + "/cred.yaml")

        # illegal password
        with self.assertRaises(Exception) as exp:
            dsaccess = dsrequests.DSAccess(repository=self.fyaycrepo, repoowner=self.fyaycrepodb,
                                           username="sberner", password="b")

        # illegal username
        with self.assertRaises(Exception) as exp:
            dsaccess = dsrequests.DSAccess(repository=self.fyaycrepo, repoowner=self.fyaycrepodb,
                                           username="xxx", password="b")

    @pytest.mark.integration
    def test_models(self):
        if not Path.exists(dsrequests.DSAccess.DEFAULT_CREDENTIALS):
            self.skipTest("\nno credentials found skip test with real credentials")
        # check default access with credentialfile
        try:
            dsaccess = dsrequests.DSAccess(repository=self.fyaycrepo, repoowner=self.fyaycrepodb,
                                           tenantname=self.dstenantname, viaazure=True)
        except:
            self.skipTest("No access to dataspot-repository")

        self.assertEqual(21, len(dsaccess._getelements(elemtype="schemes")))
        elements = dsaccess._getelements(elemtype="schemes",
                                         filtercondition=lambda x: x.get("_type") in [dsaccess.BusinessDataModel])
        self.assertEqual(1, len(elements))
        schemes = dsaccess.getschemes()
        self.assertEqual(21, len(schemes))
        self.assertEqual(1, len(dsaccess.getschemes(schemetypes=[dsaccess.BusinessDataModel])))
        self.assertEqual(2, len(dsaccess.getschemes(schemetypes=[dsaccess.ReferenceDataModel])))
        self.assertEqual(3, len(dsaccess.getschemes(
            schemetypes=[dsaccess.ReferenceDataModel, dsaccess.BusinessDataModel])))
        schema = dsaccess.getscheme(modelname="Fachdatenmodell")
        self.assertEqual(dsaccess.BusinessDataModel, schema["_type"])
        colts = dsaccess.getcollections()
        bdmcolts = dsaccess.getcollections(parentid=schema["id"])
        self.assertEqual(6, len(bdmcolts))
        bdmobjs = dsaccess.getbusinessobjects()
        self.assertTrue(len(bdmobjs) > 10)
        someobjs = dsaccess.getbusinessobjects(collectionid=bdmcolts[0]["id"])
        self.assertTrue(len(someobjs) > 1)
        someobjs = dsaccess.getbusinessobjects(collectionid=bdmcolts[0]["id"])
        self.assertTrue(len(someobjs) == 3)
        self.assertEqual(someobjs, dsaccess.getbusinessobjects(filtercondition=
                                                               lambda elem: elem["inCollection"] == bdmcolts[0]["id"]))
        someobjs = dsaccess.getbusinessobjects(modelid=bdmcolts[0]["modelId"][5:],
                                               collectionid=bdmcolts[0]["id"])
        self.assertTrue(len(someobjs) == 0)

        someobjs = dsaccess.getbusinessobjects(modelid=bdmcolts[0]["modelId"])
        self.assertTrue(len(someobjs) > 20)
        someobjs = dsaccess.getbusinessobjects(modelid=bdmcolts[0]["modelId"],
                                               collectionid=bdmcolts[0]["id"])
        self.assertTrue(len(someobjs) == 3)
        oneobj = dsaccess.getbusinessobject(modelid=someobjs[0]["modelId"],
                                            objname=someobjs[0]["label"])
        self.assertEqual(someobjs[0]["label"], oneobj["label"])
        attrs = dsaccess.getattributes()
        self.assertTrue(10 < len(attrs))
        relas = dsaccess.getrelations()
        p = dsaccess.getbusinessobject(modelid=relas[0]["modelId"], objname="Produkt")  # hasDomain
        b = dsaccess.getbusinessobject(modelid=relas[0]["modelId"], objname="Bestellposition")  # hasRange
        return

    @pytest.mark.integration
    def test_imelements(self):
        if not Path.exists(dsrequests.DSAccess.DEFAULT_CREDENTIALS):
            self.skipTest("\nno credentials found skip test with real credentials")

        try:
            dsaccess = dsrequests.DSAccess(repository=self.fyaycrepo, repoowner=self.fyaycrepodb,
                                           tenantname=self.dstenantname, viaazure=True)
        except:
            self.skipTest("No access to dataspot-repository")

        tenant = DSTenant(lang="de", dsaccess=dsaccess)
        dscat = {'label': 'Einkauf',
                 'description': 'Sämtliche Daten'
                 }
        catg = dselements.DSCategory(catg=dscat, dateCreated=datetime.now(),
                                     createdBy="teststb",
                                     tenant=tenant)
        self.assertEqual("Einkauf", catg.name)
        self.assertEqual("Sämtliche Daten", catg.descr)

        return

    @pytest.mark.integration
    def test_singlelements(self):
        if not Path.exists(dsrequests.DSAccess.DEFAULT_CREDENTIALS):
            self.skipTest("\nno credentials found skip test with real credentials")
        dsaccess = dsrequests.DSAccess(repository=self.fyaycrepo, repoowner=self.fyaycrepodb,
                                       tenantname=self.fyayctenantname, viaazure=True)
        testtenant = DSTenant(lang="de", tenantname="test")
        mappings = dsaccess.getmappings()
        jsmapping = [DSMapping(mapng=elem, tenant=testtenant).spodjson() for elem in mappings]

        return

    @pytest.mark.integration
    def test_customermodel(self):
        if not Path.exists(dsrequests.DSAccess.DEFAULT_CREDENTIALS):
            self.skipTest("\nno credentials found skip test with real credentials")

        self.skipTest("\ntakes too long")
        try:
            dsaccess = dsrequests.DSAccess(repository=self.fyaycrepo, repoowner=self.fyaycrepodb,
                                           tenantname='komax', viaazure=True)
        except Exception as exp:
            self.skipTest("No access to dataspot-repository")

        tenant = dstenant.DSTenant(lang="de", dsaccess=dsaccess)
        readjson = JSModel(pmodel=tenant.spodjson(), pwithversioncheck=False)
        readjson.write_json(self.debugpath / "readfromdataspot.json")
        return

    @pytest.mark.integration
    def test_immodel(self):
        if not Path.exists(dsrequests.DSAccess.DEFAULT_CREDENTIALS):
            self.skipTest("\nno credentials found skip test with real credentials")

        try:
            dsaccess = dsrequests.DSAccess(repository=self.fyaycrepo, repoowner=self.fyaycrepodb,
                                           tenantname=self.fyayctenantname,
                                           # tenantname="komax",
                                           viaazure=True)
        except Exception as exp:
            self.skipTest("No access to dataspot-repository")

        tenant = dstenant.DSTenant(lang="de", dsaccess=dsaccess)
        # domavals = tenant._domains[1].values
        # mappings = tenant._mappings[0].translations
        # rules = tenant._transformations[0].rules

        readjson = JSModel(pmodel=tenant.spodjson(), pwithversioncheck=False)
        readjson.write_json(self.debugpath / "readfromdataspot.json")

        if tenant.name != self.fyayctenantname: return  # debug with different tenant

        immodel = tenant.getmodelbyname(name="CRM-Beispiel")
        self.assertEqual("CRM-Beispiel", immodel.dsstruct["label"])

        self.assertTrue(1 < len(tenant.categories()) < 10)

        cats = tenant.categories()
        self.assertIn("Kunden", [cat.name for cat in cats])
        einkaufcat = tenant.getcategorybyname(modelid=immodel.elemid, name="Kunden")
        self.assertEqual(einkaufcat, tenant.getitembyid(einkaufcat.elemid))
        self.assertEqual(einkaufcat, tenant.getcategorybyname(name="Kunden"))
        self.assertEqual("Kunden", einkaufcat.name)
        self.assertEqual(tenant.getcategorybyname(modelid=immodel.elemid, name="Kunden"),
                         tenant.getitembyid(einkaufcat.elemid))
        self.assertTrue(10 < len(tenant.entities()))
        self.assertTrue(10 < len(tenant.entities(collectionid=einkaufcat.elemid)))
        self.assertTrue(-1 < len(tenant.relations()))
        self.assertListEqual([], tenant.entities(collectionid="gugus"))
        self.assertIsNone(tenant.getcategorybyname(name="gugus"))

        immiet: dselements.DSEntity = tenant.getentitybyname("Mieter")
        imverk: dselements.DSEntity = tenant.getentitybyname("Vertriebskunde")
        self.assertEqual(immiet.supertypeid(), imverk.elemid)
        self.assertEqual(["Syno"], tenant.getentitybyname("Käufer").synonyms())
        self.assertTrue(3 < len(tenant.attributes(entityid=tenant.getentitybyname("Adresse").elemid)) < 20)

        return

    @pytest.mark.integration
    def test_ds2spod(self):
        self.skipTest("\ndataspot migration into existing SPOD not yet properly tested")
        if not Path.exists(dsrequests.DSAccess.DEFAULT_CREDENTIALS):
            self.skipTest("\nno credentials found skip test with real credentials")
        if not Path.exists(self.debugpath / "readfromdataspot.json"):
            self.test_immodel()
        if os.path.isfile(self.debugpath / 'newdb.db'):
            os.remove(self.debugpath / 'newdb.db')
        with self.caplog.at_level(logging.INFO):
            self.assertTrue(mergedbs.checkjsonfile(pjsonfilepath=self.debugpath / "readfromdataspot.json",
                                                   pverbose=True))
        originaljson = JSModel.readfromfile(self.debugpath / "readfromdataspot.json")
        newjson = JSModel(pmodel=mergedbs.jsonviadbtojson(pmodel=originaljson,
                                                          psrcname=dselements.DATASPOTSRCNAME,
                                                          pcheckonly=False,
                                                          pverbose=True
                                                          )
                          )
        newjson.write_json(self.debugpath / "spoddataspotjson.json")
        print(f"spod json for project written to {self.debugpath / 'spoddataspotjson.json'}")

        createDB(pdestination=self.debugpath / "newdb.db",
                 pmodelname=originaljson.modelname())
        mergedbs.mergejs2db(pdbfile=self.debugpath / "newdb.db", pmodel=originaljson,
                            psrcname=dselements.DATASPOTSRCNAME)
        print(f"spod db for project written to {self.debugpath / 'newdb.db'}")

        listmapping.writedatmxls(pfilename=self.debugpath / "dataspotmapping.xlsx", pmodel=newjson,
                                 plang=newjson.modellanguage())

        return

    @pytest.mark.integration
    def test_ds2miroandlistwebexports(self):
        curpath = os.getcwd()
        mypath = self.debugpath
        assert mypath.is_dir(), f"Debugpath {mypath} is not a folder"

        mirocredentialfile = Path.home() / ".miro" / "credentials-mirobaar.yaml"
        testboardname = "Miro API Test"
        os.chdir(mypath)

        if not os.path.exists("spoddataspotjson.json"):
            self.skipTest("Test file 'spoddataspotjson.json' not found.")

        jsonmodel = JSModel.readfromfile("spoddataspotjson.json")
        adddsdiagram(jsonmodel, "FULL")
        catgid = jsonmodel.getbyfield(ptype="categories", pvalue="Kunden")[0][0]
        adddsdiagram(jsonmodel, "Kunden", categoryid=catgid)
        jsonmodel.write_json("spoddataspotjson_withdiag.json")

        diagram2miro(credentialfile=mirocredentialfile, jsonfile="spoddataspotjson_withdiag.json",
                     diagramname="Kunden", diagx=4000, diagy=0,
                     updatejsonfile=True, boardname=testboardname,
                     lang="de")

        # now create a webdoku of the read model from miro
        listWebdoku.webmain(pjsonfilepath=str("spoddataspotjson_withdiag.json"),
                            pwebdirec=".",
                            pmodelname="dsmodel", pfiletype="html", singlefile=True)

        os.chdir(curpath)
        return


if __name__ == '__main__':
    unittest.main()
