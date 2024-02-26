import logging
import re

import pytest
import unittest
from pathlib import Path
import shutil

import SSOT_infra.tests.integration as testsrc
from LOAD_MODELS.LOAD_INFRA import mergedbs
from LOAD_MODELS.LOAD_MIRO import miromodel, miromergemodel
from LOAD_MODELS.LOAD_MIRO.miroboardmodel import *
from LOAD_MODELS.LOAD_MIRO.mirointerface import *
from SSOT_db.IM_JSON import JSModel
from LOAD_MODELS.LOAD_INFRA import mergedbs


class MyTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        self.capsys = capsys
        self.temppath = Path(tmp_path)

    def setUp(self) -> None:
        self.testcredentials = Path.home() / ".miro" / "credentials-mirodev.yaml"
        if not self.testcredentials.exists():
            self.skipTest("No test-credentialfile found for tests")
        self.devtestboardname = "SPOD Test Board"

        self.baarcredentials = Path.home() / ".miro" / "credentials-mirobaar.yaml"
        if not self.baarcredentials.exists():
            self.skipTest("No baar-credentialfile found for tests")
        self.mirotestboardname = "Miro API Test"


        self.crmt=testsrc.ModelHelper(testsrc.CRMTEST)

        self.testpath = testsrc.testmodels_dir() / testsrc.DATASPOT

        #file updated by load to miro, used for merge in second test
        self.crmmirojsonfile= self.crmt.dbdir / "miroboardversion.json"
        self.debugpath = Path.home() / "Downloads"
        if not self.debugpath.exists():
            # write to tempfolder
            self.debugpath = self.temppath / "Downloads"

    def test_elements(self):
        try:
            mirointerface = MiroInterface(credentialfile=self.testcredentials, boardname=self.devtestboardname)
            if len(mirointerface.getboards()) == 0:
                raise Exception("no boards")
        except:
            self.skipTest("\nno miro boards to test with, skip test")

        testframename="Testelements"
        board = MiroBoardModel(mirointerface=mirointerface,
                               board=mirointerface.getboard(name=self.devtestboardname),
                               reportback2miro=True,
                               framenames=[testframename])
        testframes=board.diagrams()
        if len(testframes)>0:
            mirointerface.deleteframe(board.boardid,frameid=testframes[0].id,withcontent=True)
        newframe = mirointerface.createframe(boardid=board.boardid,
                                                      title=testframename,
                                                      x=0, y=0,
                                                      width=400, height=400)

        newentity = mirointerface.createentity(boardid=board.boardid, frameid=newframe["id"],
                                                        name="testcolors", color="#FF7276",
                                                        x=60,y=50,
                                                        width=80,height=50,
                                                        textalignh='center', textalignv='middle')
            # mirointerface.createrelation(boardid=board.boardid,
            #                                           startitem={"x": rela.fromenti["position"]["x"],
            #                                                      "y": rela.fromenti["position"]["y"],
            #                                                      "text": rela.fromenti["text"],
            #                                                      "type": MiroRelation.relaerdtype(rela.fromenti["many"],
            #                                                                                       rela.fromenti[
            #                                                                                        "mandatory"]),
            #                                                      "id": newentities[rela.fromenti["entiid"]]["id"]},
            #                                           enditem={"x": rela.toenti["position"]["x"],
            #                                                    "y": rela.toenti["position"]["y"],
            #                                                    "text": rela.toenti["text"],
            #                                                    "type": MiroRelation.relaerdtype(rela.toenti["many"],
            #                                                                                     rela.toenti["mandatory"]),
            #                                                    "id": newentities[rela.toenti["entiid"]]["id"]}
            #                                           )

        return

    def test_tomiro(self):
        miromodel.listboards(credentialfile=self.baarcredentials,
                             boardname=self.mirotestboardname)

        miromodel.listframes(credentialfile=self.baarcredentials,
                             boardname=self.mirotestboardname)

        """load model to miro. add miro-references to special json file """
        shutil.copy(self.crmt.jsonfile,self.crmmirojsonfile )
        miromodel.diagram2miro(credentialfile=self.baarcredentials,
                             boardname=self.mirotestboardname,
                             jsonfile= self.crmmirojsonfile,
                             diagramname="Kunde",
                               destjsonfile=self.debugpath / 'miroboardversion.json')
        #shutil.copy(self.crmmirojsonfile, self.debugpath / 'miroboardversion.json')
        print (f"TEST1: update jsonfile copied to {self.debugpath / 'miroboardversion.json'}")


        return

    def test_frommiro(self):
        #create from Kunde a second frame NeuKunde manually on miro

        miromodel.miroframe2json(credentialfile=self.baarcredentials,
                             boardname=self.mirotestboardname,
                             jsonfile=self.temppath / "NeuKunde.json",
                                 framename="NeuKunde",
                                 checkjsonfile=True,lang="de")
        shutil.copy(self.temppath /"NeuKunde.json",self.debugpath / "NeuKunde.json")
        print (f"TEST2-1: loaded jsonfile copied to {self.debugpath / 'NeuKunde.json'}")

        originaljson=JSModel().readfromfile(self.crmmirojsonfile)
        newjson =JSModel().readfromfile(self.temppath /"NeuKunde.json")

        miromodel.mergeintooriginaljson(original=originaljson,newjson=newjson)
        originaljson.write_json(self.temppath / 'mergedjson.json')
        shutil.copy(self.temppath / 'mergedjson.json', self.debugpath / 'mergedjson.json')
        print (f"TEST2-2: merged jsonfile copied to {self.debugpath / 'mergedjson.json'}")

        originaljson=JSModel().readfromfile(self.temppath / 'mergedjson.json')
        newjson=JSModel().readfromfile(self.temppath /"NeuKunde.json")
        miromodel.mergeintooriginaljson(original=originaljson,newjson=newjson)

        originaljson=JSModel().readfromfile(self.temppath / 'mergedjson.json')
        with self.caplog.at_level(logging.INFO):
            self.assertTrue(mergedbs.checkjsonfile(pjsonfilepath=self.temppath / 'mergedjson.json',pverbose=True))

        shutil.copy(self.crmt.dbfile,self.temppath / 'newdb.db')
        with self.caplog.at_level(logging.INFO):
            mergedbs.mergejs2db(pdbfile=self.temppath / 'newdb.db',pmodel=originaljson,psrcname="MIRO",pverbose=True,pdryrun=False)
        shutil.copy(self.temppath / 'newdb.db',self.debugpath / 'newdb.db')
        print("new merged db written to self.debugpath / 'newdb.db'")
        return

    def test_miroboardlist(self):
        miromodel.listboards(credentialfile=self.baarcredentials,boardname="Miro")
        captured = self.capsys.readouterr()
        print (captured.out)
        self.assertTrue(re.match((r"1 board"),captured.out))

        miromodel.listboards(credentialfile=self.baarcredentials,boardname="Test")
        captured = self.capsys.readouterr()
        print (captured.out)
        self.assertTrue(re.match((r"\d+ board"),captured.out))

        miromodel.listboards(credentialfile=self.baarcredentials,boardname=None)
        captured = self.capsys.readouterr()
        print (captured.out)
        self.assertTrue(re.match((r"\d+ board"),captured.out))



if __name__ == '__main__':
    unittest.main()
