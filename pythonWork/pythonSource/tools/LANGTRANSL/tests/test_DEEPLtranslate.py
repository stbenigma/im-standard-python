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

        setauthid("9043d070-26fd-f874-6b80-37ddc4b6367c")
        with self.assertRaises(Exception) as exp:
            _ = translate("Bahnhof",'xx','FR')
        self.assertTrue(translate("Bahnhof",'DE','FR').startswith("Gare"))
        self.assertTrue(translate("Bahnhof",'DE','EN').startswith("Station"))
        self.assertTrue(translate("Bahnhof",'De','en').startswith("Station"))

        return


if __name__ == '__main__':
    unittest.main()
