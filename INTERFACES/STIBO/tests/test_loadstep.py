import logging
import os.path
import unittest
from pathlib import Path

import pytest

from STIBO.loadstep import LoadStep


class MyTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        caplog.set_level(logging.WARNING)
        self.capsys = capsys
        self.temppath = tmp_path

    def setUp(self) -> None:
        self.debugpath = Path.home() / "Downloads"
        if not self.debugpath.is_dir():
            self.debugpath = self.temppath

        self.mytestxml = Path(__file__).parent / "testfiles" / "simpletest.xml"
        if not self.mytestxml.is_file():
            self.skipTest("Testpath does not exist")
            return

    def _localtestall(self, loadstep):
        elem = loadstep.getelement(loadstep.attrgroups, "group1")
        self.assertEqual(elem.get("PATH"), [elem.get("ID")])
        elem = loadstep.getelement(loadstep.attrgroups, 'group-1-2')
        self.assertEqual(['group1', 'group-1-2'], elem.get("PATH"))

        elem = loadstep.getelement(loadstep.attributes, "AttrLOV")
        self.assertEqual([elem.get("AttributeGroupLink")[0].get(
            '@AttributeGroupID'),
            elem.get("ID")],
            elem.get("PATH"),
        )
        self.assertEqual([elem.get("AttributeGroupLink")[0].get(
            '@AttributeGroupID'),
            elem.get("ID")],
            elem.get("PATH")
        )
        elem = loadstep.getelement(loadstep.lovgroups, 'List Of Values group root')
        self.assertEqual([elem.get("ID")], elem.get("PATH"))
        elem = loadstep.getelement(loadstep.lovgroups, 'lovs_1_1')
        self.assertEqual([loadstep.lovgroups[0].get("ID"),
                          loadstep.lovgroups[1].get("ID"),
                          elem.get("ID")],
                         elem.get("PATH")
                         )

        elem = loadstep.getelement(loadstep.lovs, 'unit')
        self.assertEqual([loadstep.lovgroups[0].get("ID"),
                          elem.get("ParentID"), elem.get("ID")],
                         elem.get("PATH")
                         )

        elem = loadstep.getelement(loadstep.allusertypes, 'product_group')
        self.assertEqual(3, len(elem.get("PATH")))
        self.assertEqual(elem.get("ID"), elem.get("PATH")[-1])
        self.assertEqual('product_usertype_root',
                         elem.get("PATH")[0])

        elem = loadstep.getelement(loadstep.myusertypes, 'packaging_root')
        self.assertEqual([elem.get("ID")],
                         elem.get("PATH"))
        elem = loadstep.getelement(loadstep.myusertypes, 'logistic_packaging')
        self.assertEqual([elem.get("UserTypeLink")[0].get("@UserTypeID"),
                          elem.get("ID")],
                         elem.get("PATH")
                         )

        return

    def test_xmlloadfull(self):

        loadstep = LoadStep(
            stepfilepath=self.mytestxml,
            rootusertypes="^.*$"
        )
        self.assertEqual(4, len(loadstep.lovgroups))
        self.assertEqual(1, len(loadstep.models))
        self.assertEqual(1, len(loadstep.xreftypes))
        self.assertEqual(len(loadstep.allusertypes),
                         len(loadstep.myusertypes))
        # detect missing root pathes
        allknownUT = set([myut.get("ID")
                      for myut in loadstep.myusertypes])
        self.assertTrue(set([myut.get("PATH")[0]
                             for myut in loadstep.myusertypes]). \
                        issubset(allknownUT))
        # alle source and target utlinks in crossreferences exist
        self.assertSetEqual(set(),
                            set([d.get("@UserTypeID","")
                             for x in loadstep.xreftypes["EntityCrossReferenceType"]
                             for linktype in ("UserTypeLink", "TargetUserTypeLink")
                             for d in x.get(linktype, [])
                             ]).difference(allknownUT))
        elem = loadstep.getelement(loadstep.xreftypes["EntityCrossReferenceType"],
                                   'packaging-with')
        self.assertEqual([elem.get("TargetUserTypeLink")[0].get("@UserTypeID"),
                          "EntityCrossReferenceType",
                          elem.get("ID")],
                         elem.get("PATH"))
        elem = loadstep.getelement(loadstep.attributes,"Attr1")
        self.assertTrue("ListOfValueLink" not in elem)
        self.assertEqual(1,len(elem.get("AttributeGroupLink",[])))
        self._localtestall(loadstep)

        return

    def test_xmlloadpartial(self):

        loadstep = LoadStep(
            stepfilepath=self.mytestxml,
            rootusertypes="^packaging_root$"
        )
        self.assertEqual(4, len(loadstep.lovgroups))
        self.assertEqual(1, len(loadstep.models))
        self.assertEqual(1, len(loadstep.xreftypes))
        self.assertEqual(3, len(loadstep.myusertypes))
        self._localtestall(loadstep)

        loadstep = LoadStep(
            stepfilepath=self.mytestxml,
            rootusertypes="^(product_usertype_root|packaging_root)$"
        )
        print(len(loadstep.lovgroups), len(loadstep.models),
              len(loadstep.models), len(loadstep.xreftypes), len(loadstep.myusertypes))
        self.assertEqual(4, len(loadstep.lovgroups))
        self.assertEqual(1, len(loadstep.models))
        self.assertEqual(1, len(loadstep.xreftypes))
        self.assertEqual(3 + 7, len(loadstep.myusertypes))
        self.assertEqual(7, len(loadstep.attrgroups))
        self.assertEqual(6, len(loadstep.attributes))
        self._localtestall(loadstep)
        elem = loadstep.getelement(loadstep.xreftypes["EntityCrossReferenceType"],
                                   'packaging-with')
        self.assertEqual([elem.get("TargetUserTypeLink")[0].get("@UserTypeID"),
                          "EntityCrossReferenceType",
                          elem.get("ID")],
                         elem.get("PATH"))
        elem = loadstep.getelement(elements=loadstep.xreftypes["EntityCrossReferenceType"],
                                   idval='packaging_logistic with')
        self.assertEqual(["packaging_root",
                          elem.get("TargetUserTypeLink")[0].get("@UserTypeID"),
                          "EntityCrossReferenceType",
                          elem.get("ID")], elem.get("PATH"))

        return

    def test_xmlloaddebug(self):
        if not self.mytestxml.is_file():
            self.skipTest("Testpath does not exist")
            return
        loadstep = LoadStep(
            stepfilepath=self.mytestxml,
            rootusertypes="^(product_usertype_root|packaging_root)$",
            debugpath=self.debugpath
        )
        self.assertTrue(os.path.isfile(
            self.debugpath / (self.mytestxml.stem + ".json")))
        return


if __name__ == '__main__':
    unittest.main()
