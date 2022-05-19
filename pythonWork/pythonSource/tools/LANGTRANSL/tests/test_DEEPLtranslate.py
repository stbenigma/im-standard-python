import os.path
import unittest

from tools.LANGTRANSL.DEEPLtranslate import translate,setauthid

class MyTestCase(unittest.TestCase):
    def test_translate(self):
        setauthid(None)
        with self.assertRaises(Exception) as exp:
            _ = translate("Bahnhof",'DE','FR')

        setauthid("Gugus")
        with self.assertRaises(Exception) as exp:
            _ = translate("Bahnhof",'DE','FR')

        if os.path.exists("/Users/stb/.deepl/deeplauthid"):
            with open("/Users/stb/.deepl/deeplauthid") as d:
                deeplid = d.read()
            setauthid(deeplid)
            with self.assertRaises(Exception) as exp:
                _ = translate("Bahnhof",'xx','FR')
            self.assertTrue(translate("Bahnhof",'DE','FR').startswith("Gare"))
            self.assertTrue(translate("Bahnhof",'DE','EN').startswith("Station"))
            self.assertTrue(translate("Bahnhof",'De','en').startswith("Station"))
        else:
            print("******* Test with real deeplid skipped")

        return


if __name__ == '__main__':
    unittest.main()
