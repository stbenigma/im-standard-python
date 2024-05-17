import os.path
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from SSOT_infra.tests import integration as tb
from SSOT_db.IM_JSON import JSModel, filterjson


class FilteredJson(unittest.TestCase):
    def setUp(self) -> None:
        self.crm = tb.ModelHelper(tb.CRMTEST)
        self.crm.initDB(palways=False)
        self.localrun = os.path.isdir(Path.home()/"Downloads")


    def comparefiles(self,file1,file2):
        import difflib
        with open(file1) as lfile1:
            file1text = lfile1.readlines()
        with open(file2) as lfile2:
            file2text = lfile2.readlines()

        # Find and print the diff:
        return difflib.unified_diff(
                file1text, file2text, fromfile=str(file1),tofile=str(file2), lineterm='')

    def test_filteredjson(self):
        with tempfile.TemporaryDirectory() as tempdir:
            testfile = Path(tempdir + "/testfile.json")
            filteredfile = Path(tempdir + "/testfiltered.json")
            shutil.copy(self.crm.jsonfile, testfile)
            destfile= filterjson.filterjsonfile(pjsonfile=testfile, pdestination=filteredfile,
                                                pstatus=None, pdiagrams=None)
            self.assertTrue(os.path.isfile(destfile))
            cmp=[l for l in self.comparefiles(file1=testfile, file2=destfile)]
            self.assertEqual(0,len(cmp))

            destfile= filterjson.filterjsonfile(pjsonfile=testfile, pdestination=filteredfile,
                                                pstatus=None, pdiagrams=["DUMMY"])
            self.assertTrue(os.path.isfile(destfile))
            jsmodel=JSModel.readfromfile(pfilename=destfile)
            self.assertTrue(1,len(jsmodel.jsmodel["diagrams"].keys()))
            cmp=[l for l in self.comparefiles(file1=testfile, file2=destfile)]
            # DEBUG
            if self.localrun:
                shutil.copy(testfile, Path.home() / "Downloads")
                print(f"DEBUG: copied original json to {Path.home() / 'Downloads'}")
                shutil.copy(destfile, Path.home() / "Downloads")
                print(f"DEBUG: copied filtered json to {Path.home() / 'Downloads'}")
            self.assertLess(0,len(cmp))

        return

    def test_recursivdocumentsfilter(self):
        with tempfile.TemporaryDirectory() as tempdir:
            # Test mit lokalem spezialfile
            if os.path.exists('/Users/stb/Documents/Projekte/FYAYC_intern/FYAIM/DB/FYAYC_intern.json'):
                testfile = Path(tempdir + "/testfile2.json")
                filteredfile = Path(tempdir + "/testfiltered2.json")
                shutil.copy('/Users/stb/Documents/Projekte/FYAYC_intern/FYAIM/DB/FYAYC_intern.json', testfile)
                jsmodel = JSModel.readfromfile(pfilename=testfile)
                destmodel= filterjson.filterjson(pjsmodel=jsmodel,
                                                    pstatus="PUBL",
                                                 pdiagrams=["Organisation-Overview","Organisation-Detail",
                                                            "Who-Why-How-Base","Who-Why-How-Overview"])
                self.assertTrue(len(destmodel.getbyfield(ptype="documents",pvalue="TQMI-Roles"))>0)

            testfile = Path(tempdir + "/testfile2.json")
            shutil.copy(self.crm.jsonfile, testfile)
            jsmodel = JSModel.readfromfile(pfilename=testfile)
            diag=jsmodel.getbyfield(ptype="diagrams",pvalue="DUMMY")
            entiid=diag[0][1]["elements"]["entity"][0]["element"] #first entity on this diagram
            enti=jsmodel.getbyid(entiid)
            docu=jsmodel.getbyfield(ptype="documents",pvalue="webbild") #has unreferenced parent
            docu2id= docu[0][1]["parent"]
            docu2=jsmodel.getbyid(docu2id) #has unreferenced parent
            enti["referencedby"].append(docu[0][0]) #entity referenced by child
            docu[0][1]["references+"].append(entiid) #docu points to entity
            for elemid in docu2["references+"]:
                elem=jsmodel.getbyid(elemid)
                elem["referencedby"].remove(docu2id)
            docu2["references+"]=["ENTI9999"] #parent docu has no reference
            filterjs= filterjson.filterjson(jsmodel,pstatus=None, pdiagrams=["DUMMY"])
            self.assertTrue(len(filterjs.getbyfield(ptype="documents",pvalue=docu2["name"]))>0)
        return

    def test_datmproblem(self):
        jsmodel = JSModel.readfromfile(pfilename=self.crm.jsonfile)

        removedtabs=[]
        removedcols=[]
        mappedentis=[]
        mappedattrs=[]
        dmremoved=None
        onetab,onecol=None,None #for next test
        #set all tables of one datamodel to DRAFT -> data model should no longer be mapped in entities
        for key,dm in jsmodel.getelements("datamodels").items():
            if dm.get('name')=='TestMapping':
                dmremoved=key
                for tabid in dm.get('tables+'):
                    tab=jsmodel.getbyid(tabid)
                    if tab.get("name")=='ColAttr':
                        mappedentis=tab.get('entitiesmapped')
                        for colid in tab.get("columns+"):
                            col = jsmodel.getbyid(colid)
                            col["publstatus"]='DRAFT'
                            removedcols.append(colid)
                            mappedattrs += ([am[0] for am in col.get('attributesmapped')])
                            if len(col.get('attributesmapped')) > 0:
                                onetab,onecol=tab,col #for later test

                    if onetab is None:
                        onetab=tab

                    removedtabs.append(tabid)
                    tab["publstatus"]='DRAFT'

        self.assertEqual(4,len(mappedentis))
        self.assertEqual(5,len(jsmodel.getelements("datamodels")))

        filteredmodel = filterjson.filterjson(pjsmodel=jsmodel, pstatus="GTOP", pdiagrams=["Kunde"])
        self.assertEqual(4,len(filteredmodel.getelements("datamodels")))
        for e in mappedentis:
            enti = filteredmodel.getbyid(e)
            self.assertTrue(dmremoved not in enti.get('tablesmapped+').keys())
        for a in mappedattrs:
            attr = filteredmodel.getbyid(a)
            self.assertTrue(dmremoved not in attr.get('columnsmapped+').keys())

        onetab["publstatus"]='GTOP'
        onecol["publstatus"]='GTOP'
        filteredmodel = filterjson.filterjson(pjsmodel=jsmodel, pstatus="GTOP", pdiagrams=["Kunde"])
        self.assertEqual(5,len(filteredmodel.getelements("datamodels")))
        for e in mappedentis:
            enti = filteredmodel.getbyid(e)
            self.assertEqual(1,len(enti.get('tablesmapped+')[dmremoved]))
        for a in mappedattrs:
            attr = filteredmodel.getbyid(a)
            self.assertTrue(len(attr.get('columnsmapped+')[dmremoved])<2)


        return

    def test_call(self):
        sys.argv = [
            filterjson.__file__,
            str(self.crm.jsonfile)
        ]
        filterjson.main()

        with tempfile.TemporaryDirectory() as tempdir:
            testfile = tempdir + "myfilteredjson.json"
            sys.argv = [
                filterjson.__file__,
                '--destination', testfile,
                str(self.crm.jsonfile)
                #'-s', 'PUBL',
                #'--diagrams=Organisation-Detail,Organisaton-Overview',
                #'/Users/stb/Documents/Projekte/FYAYC_intern/FYAIM/DB/FYAYC_intern.json'
            ]
            filterjson.main()
            self.assertTrue(os.path.isfile(testfile))

            # test diagrams and stat filters
            sys.argv = [
                filterjson.__file__,
                '-s', 'GTOP',
                '--diagrams=DUMMY',
                '--destination', testfile,
                str(self.crm.jsonfile)
            ]
            filterjson.main()
            self.assertTrue(os.path.isfile(testfile))
            if self.localrun:
                shutil.copy(testfile, Path.home() / "Downloads" / "filtered.json")

        return


if __name__ == '__main__':
    unittest.main()
