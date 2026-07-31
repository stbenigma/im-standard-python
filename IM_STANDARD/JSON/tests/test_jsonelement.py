import unittest
from IM_STANDARD import JsonElement

class MyTestCase(unittest.TestCase):
    def test_jsonelements(self):
        elem=JsonElement(start= 42,Ende="string")
        elem=JsonElement()
        elem.domainjson(elementId="DOMA1",name="meinDomain",Anything=[1,2,3])
        self.assertEqual("DOMA1",elem["elementId"])
        self.assertEqual("DOMA1",elem.getid())
        self.assertEqual("DOMA1",elem.data.get("elementId"))
        self.assertListEqual([1,2,3],elem.data.get("Anything"))
        self.assertEqual({},elem.filterprops({"name": None}))
        self.assertEqual({"abcd":1},elem.filterprops({"abcd":1,"name": None}))
        elem.add_restprops(fields=["a"],a=123,b="addittiona")
        self.assertEqual(123,elem.data.get("a"))
        self.assertEqual("addittiona",elem.data.get("additionalProps",dict()).get("b"))
        ap=elem["name"]
        elem["name"]="neuDomain"
        self.assertEqual("neuDomain",elem.data.get("name"))
        with self.assertRaises(Exception) as e:
            elem["irgendwas!!"]="neuDomain"

        elem=JsonElement(elemtype="Entity",elementId=1,name="myentity")
        self.assertEqual(1,elem["elementId"])
        self.assertEqual("myentity",elem.data["name"])
        self.assertEqual("Entity",elem.elemtype)

        return

if __name__ == '__main__':
    unittest.main()
