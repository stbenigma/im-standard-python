import copy
import unittest

from packaging import version

from SSOT_db.IM_JSON import JSModel
from SSOT_infra import parameters
from SSOT_infra.tests import integration


class TestBasejson(unittest.TestCase):
    def setUp(self) -> None:
        self.tm1 = integration.ModelHelper(integration.TESTMODEL1)
        self.crm = integration.ModelHelper(integration.CRMTEST)
        return

    def test_version(self):
        self.assertEqual(version.Version("0.0.0"), JSModel().getjsversion())
        js1 = JSModel.readfromfile(self.tm1.jsonfile,pwithcheck=False)
        impr = js1.getelements("_imprint_")
        if "JSONversion" in impr:
            del impr["JSONversion"]
        self.assertEqual(version.Version("0.0"), js1.getjsversion())

        impr["JSONversion"] = "1.3"
        self.assertEqual("1.3", str(js1.getjsversion()))
        self.assertTrue(js1.equalversions("1.3"))
        self.assertTrue(js1.equalversions("1.3.0"))
        self.assertFalse(js1.equalversions("1.0"))
        self.assertFalse(js1.equalversions("1.3.1"))
        self.assertFalse(js1.compatibleversions("0.1"))
        self.assertTrue(js1.compatibleversions("1.1"))
        self.assertTrue(js1.compatibleversions("1.3"))
        self.assertTrue(js1.compatibleversions("1.2.1"))
        self.assertFalse(js1.compatibleversions("2.0"))
        with self.assertRaises(AssertionError) as r:
            js1.assertversion("2.0")


        jsversion = parameters.jsonversion()
        impr["JSONversion"] = str(jsversion)
        self.assertTrue(js1.compatibleversions())
        js1.assertversion()  # should not raise asserterror
        jsmodel = JSModel(js1.jsmodel, pwithversioncheck=True)  # should not raise exception

        impr["JSONversion"] = "0.0"
        self.assertFalse(js1.compatibleversions())
        with self.assertRaises(AssertionError) as r:
            js1.assertversion()
        js1.upgradejson()


        model = copy.deepcopy(js1.jsmodel)
        model["_imprint_"]["JSONversion"] = "0.0"
        jsmodel = JSModel(model, pwithversioncheck=False)
        with self.assertRaises(AssertionError):
            jsmodel = JSModel(model, pwithversioncheck=True)
        return

    def test_getbyids(self):
        json1 = JSModel.readfromfile(self.tm1.jsonfile,pwithcheck=False)
        enties = json1.getelements("entities")
        key1 = list(enties.keys())[0]
        enti1 = enties[key1]
        entibyid = json1.getbyid(key1)
        self.assertEqual(len(enti1), len(entibyid))
        self.assertEqual(enti1["name"]["en"], entibyid["name"]["en"])

        odm1 = enti1["sourceref"]["ODM"][0]
        self.assertTupleEqual((key1, enti1), json1.getbysrcref(psrcname='ODM', psrcid=odm1))

        spod = enti1["sourceref"].get("SPOD")
        if spod is not None:
            spodkey = spod[0]
            self.assertTupleEqual((key1, enti1), json1.getbysrcref(psrcname='SPOD', psrcid=spodkey))

    def test_langnames(self):
        jsoncrm = JSModel.readfromfile(self.crm.jsonfile,pwithcheck=False)
        enties = jsoncrm.getelements("entities")
        enti0 = enties[list(enties.keys())[0]]
        with self.assertRaises(AssertionError):
            jsoncrm.getlangtext(pelem=enti0["shortname"],plang='fr',preplacement=False)

        self.assertEqual(enti0["name"]['fr'],jsoncrm.getlangtext(pelem=enti0["name"],plang='fr',preplacement=False))
        enti0["tooltip"]['de'] = 'tooltip1'
        enti0["tooltip"]['en'] = ''
        enti0["tooltip"]['fr'] = '*de* tooltip1'
        self.assertEqual(enti0["tooltip"]['de'], jsoncrm.getlangtext(pelem=enti0["tooltip"], plang='de', preplacement=True))
        self.assertEqual("", jsoncrm.getlangtext(pelem=enti0["tooltip"], plang='en', preplacement=False))
        self.assertEqual(enti0["tooltip"]['de'], jsoncrm.getlangtext(pelem=enti0["tooltip"], plang='en', preplacement=True))
        self.assertEqual("", jsoncrm.getlangtext(pelem=enti0["tooltip"], plang='fr', preplacement=False))
        self.assertEqual(enti0["tooltip"]['de'], jsoncrm.getlangtext(pelem=enti0["tooltip"], plang='fr', preplacement=True))

        enti0["synonyms"]=[{
               "de": "Jemand",
               "en": "*de* Jemand",
               "fr": "Personne de contact"
            },
        ]
        self.assertEqual("Jemand", jsoncrm.getlangtext(pelem=enti0["synonyms"], plang='en', preplacement=True,pidx=0))
        self.assertEqual("", jsoncrm.getlangtext(pelem=enti0["synonyms"], plang='en', preplacement=False,pidx=0))
        self.assertEqual("Personne de contact", jsoncrm.getlangtext(pelem=enti0["synonyms"], plang='fr', preplacement=False,pidx=0))

        return



if __name__ == '__main__':
    unittest.main()
