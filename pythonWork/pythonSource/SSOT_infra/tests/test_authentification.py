import tempfile
import unittest
from pathlib import Path
import shutil

from SSOT_infra import authentification


class MyTestCase(unittest.TestCase):

    def test_credentials(self):
        with self.assertRaises(Exception) as exp:
            credentialname,credentials = authentification.getcredentials(credentialfile="blalba.bla")

        # illegal yaml file content
        with tempfile.TemporaryDirectory() as td:
            credfile = td + "/credillegal.yaml"
            with open(credfile, "w") as cred:
                cred.write("foryouandyourcustomers:-- user: xxx, [password: yyy}")
                cred.close()
            with self.assertRaises(Exception) as exp:
                credentialname,credentials = authentification.getcredentials(credentialfile=credfile)

            testcred = dict()
            testcred={'username': 'me@mail.com', 'password' : 'geheim'}

            credfile = td + "/cred.yaml"
            with open(credfile, "w") as cred:
                cred.write("foryouandyourcustomers: {username: 'me@mail.com', password: 'geheim'}")
                cred.close()
                #DEBUG
                shutil.copy(credfile,Path().home() / "Downloads")
                credentialname,credentials = authentification.getcredentials(credentialfile=credfile)
                self.assertDictEqual(testcred, credentials)

                credentialname,credentials = authentification.getcredentials(credentialfile=credfile)
                self.assertEqual('me@mail.com',credentials["username"])
                self.assertEqual('geheim', credentials["password"])
        return

    def test_getgetazuretoken(self):
        credpath = Path.home() / ".dataspot" / "credentials-fyayc.yaml"
        if not Path.exists(credpath):
            self.skipTest("No credential file in current environment")

        credentialname,credentials=authentification.getcredentials(credentialfile=credpath)
        self.assertEqual("foryouandyourcustomers",credentialname)
        token = authentification.getazuretoken(clientid=credentials["clientid"],
                                        username=credentials["username"],
                                         password=credentials["password"])
        return


if __name__ == '__main__':
    unittest.main()
