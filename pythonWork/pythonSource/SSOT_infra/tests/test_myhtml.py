import unittest

from SSOT_infra import striphtml

class MyTestCase(unittest.TestCase):
    def test_striphtml(self):
        self.assertEqual("ab< c de", striphtml("ab< c de"))
        self.assertEqual("ab\nc\nde", striphtml("<p>ab<br />c<br/>de<br>"))
        self.assertEqual("ab\nc\nde\n ", striphtml("<p>ab<br />c<br/>de<br> "))
        self.assertEqual("ab\nc\nde", striphtml("<p>ab<br />c<br/>de</p>"))
        self.assertEqual("ab\nc\nde\n ", striphtml("<p>ab<br />c<br/>de</p> "))
        self.assertEqual("abcde", striphtml("<p>ab<br />c<br/>de</p>",keeplinebreaks=False))
        self.assertEqual(""" class="codeBlockContainer_I0IT 
theme-code-block"
und so """,
                        striphtml("""<p><div> class="codeBlockContainer_I0IT <br>theme-code-block"</div></div>
und so """))
if __name__ == '__main__':
    unittest.main()
