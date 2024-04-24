import os.path
import unittest

from PUBLISH_MODEL.confluence import ConfluenceApi


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.yamlfile='/Users/stb/Documents/Projekte/FYAYC_intern/FYAIM/fyayc-intern_dev.yaml'

    def test_confluence(self):
        if not os.path.exists(self.yamlfile):
            self.skipTest(f"confluence credential yamlfile not found")

        capi = ConfluenceApi(yamlfile=self.yamlfile)
        self.assertEqual('IF',capi.space)
        rootpage=capi.getspace(title=capi.rootpagename)
        self.assertEqual("Informationsmodell",rootpage["title"])
        pages=capi.getpages(root_page=rootpage)
        pagescnt=len(pages)
        self.assertTrue(pagescnt>10)
        print()
        for page in pages:
            print (page)

    def test_delete(self):
        if not os.path.exists(self.yamlfile):
            self.skipTest(f"confluence credential yamlfile not found")
        capi = ConfluenceApi(yamlfile=self.yamlfile)
        rootpage=capi.getspace(title=capi.rootpagename)
        pages=capi.getpages(root_page=rootpage)
        pagescnt=len(pages)

        print ("vorher1",pages[0])
        print ("vorher2",pages[1])
        capi.deltepage(pageid=pages[0]['id'])

        import time
        time.sleep(10) #confluence braucht seine Zeit
        neupages=capi.getpages(root_page=rootpage)
        print ("nachher",neupages[0])
        self.assertEqual(pagescnt-1,len(neupages))

        return


if __name__ == '__main__':
    unittest.main()
