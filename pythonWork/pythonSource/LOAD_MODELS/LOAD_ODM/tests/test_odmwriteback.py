import logging
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from LOAD_MODELS.LOAD_ODM import odmwriteback
from SSOT_infra.tests import integration


class OdmWriteBack(unittest.TestCase):
    def setUp(self) -> None:
        from SSOT_db.IM_JSON import JSModel
        self.tm1 = integration.ModelHelper(integration.TESTMODEL1)
        self.tm2 = integration.ModelHelper(integration.TESTMODEL2)
        self.crm = integration.ModelHelper(integration.CRMTEST)
        self.tm1.initDB(palways=False)
        self.tm2.initDB(palways=False)
        self.crm.initDB(palways=False)
        self.tm1json = JSModel.readfromfile(self.tm1.jsonfile)
        self.tm2json = JSModel.readfromfile(self.tm2.jsonfile)
        self.crmjson = JSModel.readfromfile(self.crm.jsonfile)

    def test_writetranslations(self):
        import filecmp
        def findfile(name, path):
            for root, dirs, files in os.walk(path):
                if name in files:
                    return os.path.join(root, name)
            return None

        with tempfile.TemporaryDirectory() as tempdir:
            # testdir = self.tm2.modeldir
            testdir = Path(tempdir, 'tm2')
            shutil.copytree(self.tm2.modeldir, testdir)
            entis = tuple(self.tm2json.getelements('entities').values())
            entis[0]['name']['fr'] = entis[0]['name']['fr'] + 'xyz'
            entiname = entis[0]["sourceref"]["ODM"][0]
            cnt = odmwriteback.writetranslations(pIMdirec=testdir / 'IM',
                                                 pmodelname=self.tm2.modelname,
                                                 pjson=self.tm2json, pdryrun=True)

            self.assertTupleEqual((3, 0, 1, 1), tuple(val for val in cnt.values()))
            cnt = odmwriteback.writetranslations(pIMdirec=testdir / 'IM',
                                                 pmodelname=self.tm2.modelname,
                                                 pjson=self.tm2json, pdryrun=False)

            self.assertTupleEqual((3, 0, 1, 1), tuple(val for val in cnt.values()))
            # 1enti for changed name, 1 Relation for single "is" as non handled assoc
            testroot = testdir / 'IM' / self.tm2.modelname / 'logical' / 'entity'
            odmroot = self.tm2.modeldir / 'IM' / self.tm2.modelname / 'logical' / 'entity'
            odmenti = findfile(entiname + ".xml", odmroot)
            testenti = findfile(entiname + ".xml", testroot)
            self.assertFalse(filecmp.cmp(odmenti, testenti))

        with tempfile.TemporaryDirectory() as tempdir:
            testdir = Path(tempdir, 'tm2')
            shutil.copytree(self.tm2.modeldir, testdir)
            entis = tuple(self.tm2json.getelements('entities').values())
            entis[0]['name']['fr'] = entis[0]['name']['fr'] + 'xyz'
            entiname = entis[0]["sourceref"]["ODM"][0]
            cnt = odmwriteback.writetranslations(pIMdirec=testdir / 'IM',
                                                 pmodelname=self.tm2.modelname,
                                                 pjson=self.tm2json, pdryrun=True)
            # 1 Entityname wird geändert, 1 Relation wegen standalone "is"
            self.assertTupleEqual((3, 0, 1, 1), tuple(val for val in cnt.values()))
            testroot = testdir / 'IM' / self.tm2.modelname / 'logical' / 'entity'
            odmroot = self.tm2.modeldir / 'IM' / self.tm2.modelname / 'logical' / 'entity'
            odmenti = findfile(entiname + ".xml", odmroot)
            testenti = findfile(entiname + ".xml", testroot)
            self.assertTrue(filecmp.cmp(odmenti, testenti))  # dryrun does not change files

            # da es ein Dryrun war, nochmals das gleiche Ergebnis
            cnt = odmwriteback.writetranslations(pIMdirec=testdir / 'IM',
                                                 pmodelname=self.tm2.modelname,
                                                 pjson=self.tm2json, pdryrun=False)
            self.assertTupleEqual((3, 0, 1, 1), tuple(val for val in cnt.values()))
            self.assertFalse(filecmp.cmp(odmenti, testenti))  # this time we changed it

            entis[0]['synonyms'] = [{"de": "desyno1", "en": "*de* desyno1", "fr": ""},
                                    {"de": "desyno2", "en": "*de* desyno1", "fr": "syno FR"}]
            cnt = odmwriteback.writetranslations(pIMdirec=testdir / 'IM',
                                                 pmodelname=self.tm2.modelname,
                                                 pjson=self.tm2json, pdryrun=False)
            self.assertTupleEqual((1, 0, 0, 0), tuple(val for val in cnt.values()))

            attrs = tuple(self.tm2json.getelements('attributes').values())
            attrs[0]["name"]['fr'] = 'gugus'

            cnt = odmwriteback.writetranslations(pIMdirec=testdir / 'IM',
                                                 pmodelname=self.tm2.modelname,
                                                 pjson=self.tm2json, pdryrun=True)
            self.assertTupleEqual((1, 0, 0, 1), tuple(val for val in cnt.values()))
            cnt = odmwriteback.writetranslations(pIMdirec=testdir / 'IM',
                                                 pmodelname=self.tm2.modelname,
                                                 pjson=self.tm2json, pdryrun=False)
            self.assertTupleEqual((1, 0, 0, 1), tuple(val for val in cnt.values()))
            print(cnt)

        # with tempfile.TemporaryDirectory() as tempdir:
        #     testdir = Path(tempdir, 'crm')
        #     shutil.copytree(self.crm.modeldir, testdir)
        #     cnt = odmwriteback.writetranslations(pIMdirec=testdir / 'IM',
        #                                          pmodelname=self.crm.modelname,
        #                                          pjsmodel=self.crmjson)
        #     print(cnt)
        return


if __name__ == '__main__':
    unittest.main()
