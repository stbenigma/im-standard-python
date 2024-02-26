import unittest
from SSOT_infra.mystrings import *

class MyTestCase(unittest.TestCase):
    def test_multiline2blank(self):
        self.assertEqual('abc',multiline2spaceseparated("abc"))
        self.assertEqual(' a b c ',multiline2spaceseparated("  a b  c     "))
        self.assertEqual(' a b \t c',multiline2spaceseparated("  a b     \t   c"))

        return

    def test_text2lines(self):
        self.assertEqual(("abcde",""),shortenstring(text="abcde",maxwidth=10))
        self.assertEqual(("abcdefghij","k"),shortenstring(text="abcdefghijk",maxwidth=10))
        self.assertEqual(("abcdefghij","kl"),shortenstring(text="abcdefghijkl",maxwidth=10))
        self.assertEqual(("abcdefghij","klm"),shortenstring(text="abcdefghijklm",maxwidth=10))
        self.assertEqual(("abcdefghij","klm1234567890"),shortenstring(text="abcdefghijklm1234567890",maxwidth=10))

        self.assertEqual([''], text2multiline(text='',maxlines=1,maxwidth=10))  # add assertion here
        self.assertEqual(None, text2multiline(text=None,maxlines=1,maxwidth=10))  # add assertion here
        self.assertEqual(["abcde",],
                         text2multiline(text="abcdefghijklm1234567890",maxlines=1,maxwidth=5))
        self.assertEqual(["abcde","fghij"],
                         text2multiline(text="abcdefghijklm1234567890",maxlines=2,maxwidth=5))
        self.assertEqual(["abcde","fghij","klm12","34567","890"],
                         text2multiline(text="abcdefghijklm1234567890",maxlines=10,maxwidth=5))

        self.assertEqual(["abcdefgh","ijklm",],
                         text2multiline(text="abcdefgh ijklm",maxlines=10,maxwidth=10))
        self.assertEqual(["abc defghi","jklm",],
                         text2multiline(text="abc defghi jklm",maxlines=10,maxwidth=10))
        self.assertEqual(["abcdefgh i","jklm",],
                         text2multiline(text="abcdefgh i jklm",maxlines=10,maxwidth=10))
        self.assertEqual(["abcdefgh i","jklm123456","7890"],
                         text2multiline(text="abcdefgh i jklm1234567890",maxlines=10,maxwidth=10))
        self.assertEqual(["abcdefgh i","jklm123456"],
                         text2multiline(text="abcdefgh i jklm1234567890",maxlines=2,maxwidth=10))
        self.assertEqual(["abc","defghijk","lm12345678","90"],
                         text2multiline(text="abc defghijk lm12345678 90",maxlines=10,maxwidth=10))


        self.assertEqual("abcd",text2crtext(text='abcd', maxlines=1 , maxwidth=100))
        self.assertEqual("",text2crtext(text='', maxlines=1 , maxwidth=100))
        self.assertEqual(None,text2crtext(text=None, maxlines=1 , maxwidth=100))
        self.assertEqual("abc defghi\njklm",
                         text2crtext(text="abc defghi jklm",maxlines=10,maxwidth=10))


        return

    def test_remove(self):
        self.assertEqual("",removenonchars(''))
        self.assertEqual(None,removenonchars(None))
        self.assertEqual("",removenonchars('$!!  \t*%&'))
        self.assertEqual("_abc_",removenonchars('-_abc_-'))
        self.assertEqual("ab_c_",removenonchars('--ab_-c_'))

if __name__ == '__main__':
    unittest.main()
