import unittest
import pytest


from INTERFACES.DATASPOT import *


class MyTestCase(unittest.TestCase):
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

    def setUp(self) -> None:
        self.fyaycrepo = "https://www.dataspot.io"
        self.fyaycrepodb = "chem-x"
        self.tenantname = "Mandant"
        self.dstenantname = "Basis - Schwipsti GmbH"
        self.username = ""
        self.password = ''
        self.credentialfile = Path.home() / ".dataspot" / "credentials-chemx.yaml"

    def test_good_access(self):

        if not Path.exists(self.credentialfile):
            self.skipTest("\nno credentials found skip test with real credentials")

        # check default access with credentialfile
        try:
            dsaccess = dsrequests.DSAccess(credentialfile=self.credentialfile,
                                           repository=self.fyaycrepo,
                                           repoowner=self.fyaycrepodb,
                                           viaazure=False)
        except Exception as e:
            self.skipTest(f"No access to dataspot-repository {e}")
        dsaccess = dsrequests.DSAccess(credentialfile=self.credentialfile, repository=self.fyaycrepo,
                                       repoowner=self.fyaycrepodb,
                                       tenantname=self.tenantname, viaazure=False)
        with self.assertRaises(Exception) as exp:
            # unknown tenant
            dsaccess = dsrequests.DSAccess(credentialfile=self.credentialfile,
                                           repository=self.fyaycrepo,
                                           repoowner=self.fyaycrepodb,
                                           tenantname="blabla")

        return

    def test_models(self):
        if not Path.exists(self.credentialfile):
            self.skipTest("\nno credentials found skip test with real credentials")
        # check default access with credentialfile
        try:
            dsaccess = dsrequests.DSAccess(credentialfile=self.credentialfile,
                                           repository=self.fyaycrepo, repoowner=self.fyaycrepodb,
                                           tenantname=self.tenantname)
        except Exception as e:
            self.skipTest(f"No access to dataspot-repository {e}")


        self.assertTrue(len(dsaccess._getelements(elemtype="schemes"))>10)
        elements = dsaccess._getelements(elemtype="schemes",
                                         filtercondition=lambda x: x.get("_type") in [dsaccess.BusinessDataModel])
        self.assertTrue(len(elements)>=1)
        schemes = dsaccess.getschemes()
        self.assertTrue(len(dsaccess.getschemes(schemetypes=[dsaccess.BusinessDataModel]))>=1)
        self.assertTrue(len(dsaccess.getschemes(schemetypes=[dsaccess.ReferenceDataModel]))>=1)
        self.assertTrue(len(dsaccess.getschemes(
            schemetypes=[dsaccess.ReferenceDataModel, dsaccess.BusinessDataModel]))>=1)
        schema = dsaccess.getscheme(modelname=schemes[0].get("label"))
        self.assertEqual(dsaccess.BusinessDataModel, schema["_type"])


        bdmobjs = dsaccess.getbusinessobjects()
        self.assertTrue(len(bdmobjs) > 10)


if __name__ == '__main__':
    unittest.main()
