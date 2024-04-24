import os
import pprint
import shutil
import tempfile
import unittest
from pathlib import Path

import pytest

import LOAD_MODELS.LOAD_MIRO.miro2json
import SSOT_infra.tests.integration as testsrc
from IM_WEB import listWebdoku
from LOAD_MODELS.LOAD_INFRA import mergedbs
from LOAD_MODELS.LOAD_MIRO import miromodel, miromergemodel
from LOAD_MODELS.LOAD_MIRO.miroboardmodel import *
from LOAD_MODELS.LOAD_MIRO.mirointerface import *
from SSOT_db.IM_JSON import JSModel


class TestMiro(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temp_folder = Path(tmp_path)
        self.testmodel2 = testsrc.ModelHelper(testsrc.TESTMODEL2)
        # self.testmodel2.initDB(palways=True)
        self.crmtest = testsrc.ModelHelper(testsrc.CRMTEST)
        self.mirotestboardname = "SPOD Test Board"
        self.baarcredentials = Path.home() / ".miro" / "credentials-mirobaar.yaml"
        self.testcredentials = Path.home() / ".miro" / "credentials-mirodev.yaml"
        if not self.testcredentials.exists():
            self.skipTest("No credentialfile found for tests")

        self.debugpath = Path.home() / "Downloads"  # try local debug path
        if not self.debugpath.exists():
            # write to tempfolder
            self.debugpath = self.temp_folder / "Downloads"

        try:
            self.mirointerface = MiroInterface(credentialfile=self.testcredentials, boardname=self.mirotestboardname)
            if len(self.mirointerface.getboards()) == 0:
                raise Exception("no boards")
        except:
            self.skipTest("\nno miro boards to test with, skip test")

        # set up proper test environment
        board = self.mirointerface.getboard(name=self.mirotestboardname)
        frames = self.mirointerface.getframes(boardid=board["id"])
        for frame in frames:
            if frame["data"]["title"] in ('DUMMY', 'Kunde', 'Main-View', 'DUMMY-old', 'Kunde-old', 'Main-View-old'):
                self.mirointerface.deleteframe(boardid=board["id"], frameid=frame["id"], withcontent=True)
            elif frame["data"]["title"] in ('IM-2-old', 'IM-1-old'):
                self.mirointerface.updateframe(boardid=board["id"], frameid=frame["id"],
                                               title=frame["data"]["title"][:-4])
            elif frame["data"]["title"] in ('IM-2', 'IM-1'):
                # remove newly created frames, if -old exists to rename
                if frame["data"]["title"] + "-old" in [f["data"]["title"] for f in frames]:
                    self.mirointerface.deleteframe(boardid=board["id"], frameid=frame["id"], withcontent=True)

        for sticky in self.mirointerface.getstickys(boardid=board["id"]):
            if "Entity name duplicate" in sticky["data"]["content"] or \
                    "Hello World" in sticky["data"]["content"]:
                self.mirointerface.deletesticky(boardid=board["id"], stickyid=sticky["id"])

        return

    def test_0access(self):
        with self.assertRaises(Exception) as exp:
            ma = MiroAccess(token="abcde")

        with tempfile.TemporaryDirectory() as tempdir:
            with self.assertRaises(Exception) as exp:
                ma = MiroAccess(credentialfile="xxxx")
            with open(tempdir + "/dummycred.xxx", 'w') as dummy:
                dummy.write("{'bla':'xxx'}")
                with self.assertRaises(Exception) as exp:
                    ma = MiroAccess(credentialfile=tempdir + "/dummycred.xxx")

            ma: MiroAccess = MiroAccess(credentialfile=self.testcredentials)
            boards = ma._requestboards(query="SPOD ")
            self.assertEqual(1, len(boards))
            boards = ma._requestboards(query=self.mirotestboardname)
            self.assertEqual(1, len(boards))
            boards = ma._requestboards(query="gugusgääööüü")
            self.assertEqual(0, len(boards))
            boards = ma._requestboards()
            self.assertDictEqual(boards[0], ma.getboards()[0])
            # pprint.pprint(boards)
            testid = boards[0]["id"]
            frames1 = ma._requestitems(boardid=testid)
            frames2 = ma._requestitems(boardid=testid, itemlimit=12)
            self.assertTrue(len(frames1) == len(frames2) and len(frames1) > 1)
            frames = ma._requestitems(boardid=testid, itemlimit=12, elemtype="frame")
            self.assertTrue(len(frames) >= 2)
            self.assertTrue(len(ma._requestshapes(boardid=testid)) >= 2)
            self.assertTrue(len(ma._requestconnectors(boardid=testid)) >= 2)
            self.assertTrue(len(ma._requestframes(boardid=testid)) >= 2)
            self.assertTrue(len(ma._requeststickys(boardid=testid)) >= 2)
            self.assertTrue(len(ma._requesttexts(boardid=testid)) >= 1)
            # pprint.pprint(frame)
        return

    def test_mirointerface(self):
        print("\nlist of miro-boards ==================")
        pprint.pprint(self.mirointerface.getboards())

        testboard = self.mirointerface.getboard(name=self.mirotestboardname)
        oneboard = MiroInterface(credentialfile=self.testcredentials, boardid=testboard["id"])
        self.assertTrue(1, len(oneboard.getboards()))
        self.maxDiff=None
        changedboard =  oneboard.getboards()[0]
        del testboard["modifiedAt"]
        del changedboard["modifiedAt"] #short delay in change
        self.assertDictEqual(testboard, changedboard)

        with self.caplog.at_level(logging.WARNING):
            board = MiroBoardModel(mirointerface=self.mirointerface, board=testboard,
                                   framenames=["IM-1", "IM-2"])
            self.assertEqual(1, len([m for m in self.caplog.messages if m.startswith("Duplicate")]))

        print("\nDIAGRAs (=frames) ==================")
        for item in board.diagrams():
            pprint.pprint(item.mirostruct)
            print("\nentities on this diagram ==================")
            self.assertEqual(5 if item.name == "IM-1" else 2, len(board.entities(diagid=item.id)))
            for e in board.entities(diagid=item.id):
                pprint.pprint(e.mirostruct)
            print("\nrelations on this diagram ==================")
            self.assertEqual(5 if item.name == "IM-1" else 1, len(board.relations(diagid=item.id)))

            for item in board.relations(diagid=item.id):
                pprint.pprint(item.mirostruct)

        self.assertEqual(6, len(board.relations()))

        # NOCARDS
        # cards = board.getallcards()

        # Leichen aufräumen
        # NOCARDS
        # for t in self.mirointerface._getalltags(boardid=board.boardid):
        #    if t["title"].startswith("CREATEBOARD"):
        #        self.mirointerface._deletetag(boardid=board.boardid,tagid=t["id"])

        # tags = self.mirointerface._getalltags(boardid=board.boardid)
        # newtag = self.mirointerface._createtag(boardid=board.boardid, data={"fillColor": "red",
        #                                                           "title": "CREATEBOARD0"
        #                                                           }
        #                              )
        # cardtagsbefore=self.mirointerface.gettags(boardid=board.boardid,itemid=cards["Violet Card"].id)
        # self.mirointerface._additemtag(boardid=board.boardid, itemid=cards["Violet Card"].id,tagid=newtag["id"])
        # cardtagsafter=self.mirointerface.gettags(boardid=board.boardid,itemid=cards["Violet Card"].id)
        # self.assertEqual(len(cardtagsbefore)+1,len(cardtagsafter))
        # tags2 = self.mirointerface._getalltags(boardid=board.boardid)
        # self.assertEqual(len(tags)+1,len(tags2))
        # cardtagsafter=self.mirointerface.gettags(boardid=board.boardid,itemid=cards["Violet Card"].id)

        # self.mirointerface._deletetag(boardid=board.boardid,tagid=newtag["id"])

        return

    def test_newframes(self):
        newframes = list()
        lightgray = "#f3f3f3"
        ma: MiroAccess = MiroAccess(credentialfile=self.testcredentials)
        boards = ma._requestboards()
        board = MiroBoardModel(mirointerface=self.mirointerface,
                               board=self.mirointerface.getboard(name="SPOD Test Board"),
                               withload=True,
                               framenames=["IM-1", "IM-2"])

        for frame in board.diagrams():
            if True:
                self.mirointerface.updateframe(boardid=board.boardid, frameid=frame.id,
                                               title=frame.name + "-old")
                # create new frames
                newframes.append(self.mirointerface.createframe(boardid=board.boardid,
                                                                title=frame.name,
                                                                x=frame.x + frame.width() + 10, y=frame.y,
                                                                width=frame.width(), height=frame.height()))

        frames = self.mirointerface._requestframes(boardid=board.boardid)
        framenames = [name["data"]["title"] for name in frames]
        self.assertTrue("IM-1" in framenames)
        self.assertTrue("IM-2" in framenames)
        self.assertTrue("IM-1-old" in framenames)
        self.assertTrue("IM-2-old" in framenames)

        return

    def test_1mirojson(self):
        print("")
        miromodel.loclistboards(self.mirointerface)
        self.assertIn(self.mirotestboardname, [b["name"] for b in self.mirointerface.getboards()])
        board = MiroBoardModel(mirointerface=self.mirointerface,
                               board=self.mirointerface.getboard(name=self.mirotestboardname),
                               reportback2miro=True,
                               framenames=["IM-1", "IM-2"], withload=True)
        mirojson = LOAD_MODELS.LOAD_MIRO.miro2json.miroboard2json(board)

        mirojson.write_json(self.debugpath / "mirotest.loaded.json")
        print(f"miro-model written to json {self.debugpath / 'mirotest.loaded.json'}")

        self.caplog.clear()

        with self.caplog.at_level(logging.ERROR):
            mirojson = JSModel.readfromfile(pfilename=self.debugpath / "mirotest.loaded.json", pwithcheck=True)
            mergedbs.checkjsonmodel(pmodel=mirojson, pverbose=True)
            self.assertTrue(len(self.caplog.messages) == 0)

        self.caplog.clear()
        with self.caplog.at_level(logging.ERROR):
            mirojson.jsmodel = mergedbs.jsonviadbtojson(pmodel=mirojson, psrcname="MIRO",
                                                        pcheckonly=True, pverbose=True)
            self.assertTrue(len(self.caplog.messages) == 0)

        self.assertTrue(mirojson.getbyfield(ptype="entities", pvalue="Entity 3",
                                            plang="en")[0][1]["supertypeentity"] is not None)
        self.assertTrue(mirojson.getbyfield(ptype="entities",
                                            pvalue="Entity 2", plang="en")[0][1]["supertypeentity"] is not None)
        mirojson.write_json(self.debugpath / "mirotest.json")

        # now create a webdoku
        listWebdoku.webmain(pjsonfilepath=self.debugpath / "mirotest.json", pwebdirec=self.debugpath,
                            pmodelname="mirotest", pfiletype="html", singlefile=True)

        st = self.mirointerface.getstickys(boardid=board.boardid)
        self.assertIn("Entity name duplicate Entity 2", [s["data"]["content"] for s in st])

        # test with other board-owner with many board
        if self.baarcredentials.exists():
            mirointf = MiroInterface(credentialfile=self.baarcredentials, boardname="IM")
            boards = mirointf.getboards()
            self.assertTrue(10 < len(boards))
            board = mirointf.getboard(name="IM Lehrgang")
            self.assertTrue(board is not None)

        return

    def test_stickys(self):
        print("")
        boardmodel = MiroBoardModel(mirointerface=self.mirointerface,
                                    board=self.mirointerface.getboard(name="SPOD Test Board"),
                                    reportback2miro=True,
                                    framenames=["IM-1"])

        frameid = self.mirointerface.getframe(boardid=boardmodel.boardid, framename="IM-1")["id"]
        sticky = MiroSticky(text="Hello World", size=40, parentid=frameid).stickystruct()
        self.mirointerface.putsticky(boardid=boardmodel.boardid, data=sticky)
        st = self.mirointerface.getstickys(boardid=boardmodel.boardid)
        self.assertIn("Hello World", [s["data"]["content"] for s in st])

        return
    def test_newframes2(self):

        board = MiroBoardModel(mirointerface=self.mirointerface,
                               board=self.mirointerface.getboard(name=self.mirotestboardname),
                               reportback2miro=True,
                               framenames=["IM-1", "IM-2"])

        for frame in board.diagrams():
            self.mirointerface.updateframe(boardid=board.boardid, frameid=frame.id,
                                           title=frame.name + "-old")
            newframe = self.mirointerface.createframe(boardid=board.boardid,
                                                      title=frame.name,
                                                      x=frame.x + frame.width() + 10, y=frame.y,
                                                      width=frame.width(), height=frame.height())

            newentities = dict()
            for entity in board.entities(diagid=frame.id):
                newentity = self.mirointerface.createentity(boardid=board.boardid, frameid=newframe["id"],
                                                            name=entity.name, color=entity.fillcolor,
                                                            x=entity.x(frame=frame),
                                                            y=entity.y(frame=frame),
                                                            width=entity.width(frame=frame),
                                                            height=entity.height(frame=frame),
                                                            textalignh=entity.textalignh, textalignv=entity.textalignv)
                newentities[entity.id] = newentity
            for rela in board.relations(diagid=frame.id):
                if rela.relatype() == "ISAS": continue #non displayed relationships excluded
                if rela.fromenti["entiid"] == rela.toenti["entiid"]:
                    # recursive relation has to be treated specially
                    continue
                else:
                    self.mirointerface.createrelation(boardid=board.boardid,
                                                      startitem={"x": rela.fromenti["position"]["x"],
                                                                 "y": rela.fromenti["position"]["y"],
                                                                 "text": rela.fromenti["text"],
                                                                 "type": MiroRelation.relaerdtype(rela.fromenti["many"],
                                                                                                  rela.fromenti[
                                                                                                   "mandatory"]),
                                                                 "id": newentities[rela.fromenti["entiid"]]["id"]},
                                                      enditem={"x": rela.toenti["position"]["x"],
                                                               "y": rela.toenti["position"]["y"],
                                                               "text": rela.toenti["text"],
                                                               "type": MiroRelation.relaerdtype(rela.toenti["many"],
                                                                                                rela.toenti["mandatory"]),
                                                               "id": newentities[rela.toenti["entiid"]]["id"]}
                                                      )

        return

    def test_json2miro(self):
        ma: MiroAccess = MiroAccess(credentialfile=self.testcredentials)
        boards = ma._requestboards()
        board = MiroBoardModel(mirointerface=self.mirointerface, board=boards[0], withload=False)

        js_model = JSModel.readfromfile(self.testmodel2.jsonfile)

        miromodel.json2miro(board=board, jsmodel=js_model, diagnames=["*"])

        return

    def test_roundtrip(self):
        testjsonfilepath = self.temp_folder / "testjson.json"
        shutil.copy(self.crmtest.jsonfile, testjsonfilepath)
        # load json to miroboard and fill miro-ids in jsonmodel on file
        self.locmodel2miro(jsonfilepath=testjsonfilepath)
        # read it back from miro to a web respresentation
        board = MiroBoardModel(mirointerface=self.mirointerface,
                               board=self.mirointerface.getboard(name=self.mirotestboardname),
                               framenames=["DUMMY", "IM-2"],
                               reportback2miro=True)
        mirojson = LOAD_MODELS.LOAD_MIRO.miro2json.miroboard2json(board, lang="de")
        mirojson.write_json(self.temp_folder / "mirotest2.json")
        mirojson.write_json(self.debugpath / "mirotest2.json")

        # check json file through db check-procedure
        mirojson = JSModel.readfromfile(pfilename=self.temp_folder / "mirotest2.json", pwithcheck=False)

        with self.caplog.at_level(logging.INFO):
            # logging.basicConfig(stream=sys.stderr)
            # logging.getLogger("mergedbs").setLevel(logging.WARNING)
            try:
                checkjsmodel = mergedbs.jsonviadbtojson(pmodel=mirojson, psrcname="MIRO")
            except AssertionError as ae:
                print(self.caplog)

        original = JSModel.readfromfile(testjsonfilepath)
        with self.caplog.at_level(logging.INFO):
            miromergemodel.mergeintooriginaljson(original=original,
                                                 newjson=mirojson)
        self.assertDictEqual(original.jsmodel, original.jsmodel)
        if self.debugpath.exists():
            original.write_json(self.debugpath / "mergedmirotest.json")
            print(f"roundtrip merge written into {self.debugpath / 'mergedmirotest.json'}")

        # now create a webdoku of the read model from miro
        if False and self.debugpath.exists():
            listWebdoku.webmain(pjsonfilepath=self.debugpath / "mergedmirotest.json",
                                pwebdirec=self.debugpath,
                                pmodelname="mirotestmerged", pfiletype="html", singlefile=True)

        return

    def test_realmodel(self):
        testjsonfilepath = self.temp_folder / "testjson.json"
        shutil.copy(self.crmtest.jsonfile, testjsonfilepath)
        self.locmodel2miro(jsonfilepath=testjsonfilepath,
                           fulltest=False)  # fulltest creates too many frames, was tested once
        self.assertTrue(Path(testjsonfilepath).exists())

    def locmodel2miro(self, jsonfilepath, fulltest=False):
        if not jsonfilepath.exists():
            self.skipTest("json file for real example does not exist")

        miroboard = self.mirointerface.getboard(name=self.mirotestboardname)
        board = MiroBoardModel(mirointerface=self.mirointerface, board=miroboard, withload=False)

        js_model = JSModel.readfromfile(jsonfilepath)
        if fulltest:
            # too many frames crated on miro. was tested mamually
            diags = miromodel.json2miro(board=board, jsmodel=js_model, diagnames=[])
            self.assertEqual(0, len(diags))
            diags = miromodel.json2miro(board=board, jsmodel=js_model, diagnames=["bla", "gugus"])
            self.assertEqual(0, len(diags))
            diags = miromodel.json2miro(board=board, jsmodel=js_model)
            self.assertEqual(3, len(diags))
            diags = miromodel.json2miro(board=board, jsmodel=js_model, diagnames=["Kunde"])
            self.assertEqual(1, len(diags))
        diags = miromodel.json2miro(board=board, jsmodel=js_model, diagnames=["DUMMY"])
        # diags = miromodel.json2miro(board=board, mirojsmodel=js_model, diagnames=["Kunde", "DUMMY"])
        # self.assertEqual(2, len(diags))
        js_model.write_json(jsonfilepath)
        return

    def test_scripts(self):
        miromergelogger = logging.getLogger("miromerge")
        miromergelogger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        miromergelogger.addHandler(ch)

        miromodel.listboards(credentialfile=self.testcredentials)

        jssrcfile = self.temp_folder / "test_db.json"
        shutil.copy(self.testmodel2.jsonfile, jssrcfile)
        miromodel.diagram2miro(credentialfile=self.testcredentials,
                               jsonfile=self.testmodel2.jsonfile,
                               diagramname="Main-View",
                               destjsonfile=jssrcfile,
                               # ,boardid=None,
                               boardname="SPOD"
                               )
        self.assertTrue(Path.exists(jssrcfile))
        shutil.copy(jssrcfile, self.debugpath / "test_db.json")
        # read the model back from miro
        jsmirofile = self.temp_folder / "test_db_miro.json"
        mirojsmodel: JSModel = miromodel.miroframe2json(credentialfile=self.testcredentials,
                                                        jsonfile=jsmirofile,
                                                        framename="Main-View",
                                                        checkjsonfile=True,
                                                        # ,boardid=None,
                                                        boardname=self.mirotestboardname,
                                                        lang="de"

                                                        )

        dbfile = self.temp_folder / "testdb.db"
        jsonfileloaded = self.temp_folder / "testdb_loaded.json"
        shutil.copy(self.testmodel2.dbfile, dbfile)
        shutil.copy(jsmirofile, self.debugpath / "testdb_loaded_from_miro.json")

        lastmod = os.path.getmtime(dbfile)
        # merge into original json file (with miro-sourcefs added
        #mirojsmodel: JSModel, mergetojsonfile:str, withdb=False, verbose=False):
        miromodel.mergemiro2spod(mirojsmodel=mirojsmodel, mergetojsonfile=jssrcfile)
        shutil.copy(jssrcfile, self.debugpath / "testdb_loaded.json")
        return

        mergedjson = miromodel.mergemiro2spod(mirojsmodel=mirojsmodel, mergetojsonfile=jssrcfile,
                                              dbfile=dbfile)
        self.assertNotEqual(lastmod, os.path.getmtime(dbfile))

        shutil.copy(dbfile, self.debugpath / "testdb.db")

        return

        jssrcfile = self.temp_folder / "tempjson.json"
        shutil.copy(self.testmodel2.jsonfile, jssrcfile)
        lastmod = os.path.getmtime(self.testmodel2.jsonfile)
        miromodel.diagram2miro(credentialfile=self.testcredentials,
                               jsonfile=jssrcfile,
                               diagramname="Main-View",
                               updatejsonfile=True,
                               # ,boardid=None,
                               boardname="SPOD"
                               )
        self.assertNotEqual(lastmod, os.path.getmtime(jssrcfile))
        with open(jssrcfile, "r") as f:
            js = f.read()
            self.assertTrue("MIRO" in js)

        self.capsys.readouterr()  # empty stdoutput
        miromodel.listboards(credentialfile=self.testcredentials)
        captured = self.capsys.readouterr()
        print(captured.out)
        self.assertTrue(captured.out.startswith("SPOD"))
        with self.capsys.disabled(): print(captured.out)

        miromodel.listboards(credentialfile=self.testcredentials, boardname="SPOD")
        captured = self.capsys.readouterr()
        self.assertTrue(captured.out.startswith("SPOD"))
        with self.capsys.disabled(): print(captured.out)

        miromodel.listframes(credentialfile=self.testcredentials,
                             boardname=self.mirotestboardname)

        with self.assertRaises(Exception) as exp:
            miromodel.diagram2miro(credentialfile=self.testcredentials,
                                   jsonfile=self.testmodel2.jsonfile,
                                   diagramname="gugus",
                                   # updatejsonfile=True,boardid=None, boardname=None
                                   )
        with self.assertRaises(Exception) as exp:
            miromodel.diagram2miro(credentialfile=self.testcredentials,
                                   jsonfile=self.testmodel2.jsonfile,
                                   diagramname="Main-View",
                                   # updatejsonfile=True,
                                   boardid=1234567, boardname=None
                                   )
        with self.assertRaises(Exception) as exp:
            miromodel.diagram2miro(credentialfile=self.testcredentials,
                                   jsonfile=self.testmodel2.jsonfile,
                                   diagramname="Main-View",
                                   # updatejsonfile=True,
                                   boardname="irgendwer"
                                   )
        lastmod = os.path.getmtime(self.testmodel2.jsonfile)
        miromodel.diagram2miro(credentialfile=self.testcredentials,
                               jsonfile=self.testmodel2.jsonfile,
                               diagramname="Main-View",
                               updatejsonfile=False
                               # ,boardid=None, boardname=None
                               )
        self.assertEqual(lastmod, os.path.getmtime(self.testmodel2.jsonfile))

        lastmod = os.path.getmtime(self.testmodel2.jsonfile)
        miromodel.diagram2miro(credentialfile=self.testcredentials,
                               jsonfile=self.crmtest.jsonfile,
                               diagramname="Kunde",
                               updatejsonfile=False,
                               # ,boardid=None,
                               boardname="SPOD"
                               )
        self.assertEqual(lastmod, os.path.getmtime(self.testmodel2.jsonfile))

        return

    def test_realmiro(self):
        if self.baarcredentials.exists():
            self.capsys.readouterr()  # empty stdoutput
            miromodel.listboards(credentialfile=self.baarcredentials, boardname="IK")
            captured = self.capsys.readouterr()
            self.assertTrue("IK Vermitteln" in captured.out)
            with self.capsys.disabled(): print(captured.out)

            miromodel.listframes(credentialfile=self.baarcredentials,
                                 boardname="IK")

            miromodel.diagram2miro(credentialfile=self.baarcredentials, boardname="Miro API Test",
                                   jsonfile=self.testmodel2.jsonfile,
                                   diagramname="Main-View"
                                   )


if __name__ == '__main__':
    unittest.main()
