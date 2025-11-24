import unittest
from IM_STANDARD import JsonSchema

class MyTestCase(unittest.TestCase):
    def test_additionalprops(self):
        schema=JsonSchema()
        jsonstruct= {"Start": 42}
        schema.add_restprops(jsonstruct=jsonstruct,
                                      fields= ["f1", "f2"],
                                      f1="f1",
                                      f3="f3"
                                      )
        self.assertTrue("f1" in jsonstruct)
        self.assertFalse("f2" in jsonstruct)
        self.assertFalse("f3" in jsonstruct)
        self.assertTrue("additionalProps" in jsonstruct)
        self.assertTrue("f3" in [key for d in jsonstruct.get("additionalProps") for key in d.keys()])

        jsonstruct = {"Start": 42}
        schema.add_restprops(jsonstruct=jsonstruct,
                                        fields=["f1", "f2"],
                                        f1="f1",
                                        f3="f3",
                                        additionalProps={"HALLO": "xx"}
                                        )
        self.assertTrue("f1" in jsonstruct)
        self.assertFalse("f2" in jsonstruct)
        self.assertFalse("f3" in jsonstruct)
        self.assertTrue("additionalProps" in jsonstruct)
        self.assertTrue("f3" in keys for ap in  jsonstruct.get("additionalProps") for keys in ap.keys())
        self.assertTrue("HALLO" in keys for ap in  jsonstruct.get("additionalProps") for keys in ap.keys())

        jsonstruct = {"Start": 42}
        schema.add_restprops(jsonstruct=jsonstruct,
                                        fields=["f1", "f2"],
                                        f1="f1"
                                        )
        self.assertTrue("f1" in jsonstruct)
        self.assertFalse("f2" in jsonstruct)
        self.assertFalse("additionalProps" in jsonstruct)
        return

if __name__ == '__main__':
    unittest.main()
