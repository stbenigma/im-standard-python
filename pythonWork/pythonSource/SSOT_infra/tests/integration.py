import os.path
import shutil
import traceback
import unittest
from pathlib import Path
import datetime

from LOAD_MODELS.LOAD_ODM import fillDB
from SSOT_db import createDB, createJSON

ROOT_MARKER = 'pythonWork'
TESTMODEL1: str = 'testmodel-1'
TESTMODEL2: str = 'testmodel-2'
CRMTEST: str = 'crmTest'
RIDDLE: str = 'riddle'


class Testmodel:
    def __init__(self, modelname):
        self.modelname = modelname
        self.modeldir = testmodels_dir() / modelname
        self.modelfile = testmodels_dir() / modelname / 'IM' / (modelname+'.dmd')
        self.logfile = self.modeldir / (modelname + '.log')
        self.paramfile = self.modeldir / (modelname + '.params')
        self.dbdir = self.modeldir / 'DB'
        self.dbfile = self.dbdir / (modelname + '.db')
        self.jsonfilename = modelname + '.json'
        self.jsonfile = self.dbdir / self.jsonfilename
        self.webdir = self.modeldir / 'Web'

    def initDB(self,palways=False):
        def age(ptimestamp):
            diff = datetime.datetime.now()-datetime.datetime.fromtimestamp(ptimestamp)
            return int(round(diff.total_seconds()/60))

        if palways or not os.path.exists(self.dbfile) or age(os.path.getmtime(self.dbfile))>60:
            if palways and os.path.exists(self.dbfile):
                os.remove(self.dbfile)
            elif os.path.exists(self.dbfile):
                #upgrade
                createDB(pmodelname=self.modelname, pupgrade=True, pdestination=self.dbfile,
                         plogfilepath=self.logfile)

            fillDB.filldbmain(pmodelname=self.modelname, pdestination=self.dbfile)

        if palways or not os.path.exists(self.jsonfile) or age(os.path.getmtime(self.jsonfile))>60:
            createJSON.createJSON(pdbfilepath=self.dbfile, pmodelname=self.modelname,
                                  pjsfilepath=self.dbdir, pjsfilename=self.jsonfilename)
        return self

    def initWeb(self):
        # make sure new templates files are reloaded
        if os.path.exists(self.webdir / "jinjatemplates"):
            shutil.rmtree(self.webdir / "jinjatemplates/")
        if os.path.exists(self.webdir / "js"):
            shutil.rmtree(self.webdir / "js/")
        if os.path.exists(self.webdir / "css"):
            shutil.rmtree(self.webdir / "css/")
        if os.path.exists(self.webdir / "images"):
            shutil.rmtree(self.webdir / "images/")


def initDB(pmodel):
    tm = Testmodel(pmodel).initDB()
    return


class IntegrationTest(unittest.TestCase):

    def setUp(self) -> None:
        stack = traceback.extract_stack()
        for frame in reversed(stack):
            if ROOT_MARKER in frame.filename:
                self.set_folders(frame.filename)
        super().setUp()

    def set_folders(self, file: Path) -> Path:
        self.base_path = Path(file).parent
        self.project_root = resolve_project_root(file)
        return self.project_root


def resolve_project_root(folder: Path = __file__) -> Path:
    base_path = Path(folder).parent
    dirs = list(base_path.parts)
    base = dirs.index(ROOT_MARKER)
    # reduce path down to project base folder
    project_root = Path(*list(dirs[0:base]))
    return project_root

def testdata_root() -> Path:
    return resolve_project_root() / 'testdata'

def source_root() -> Path:
    return resolve_project_root() / ROOT_MARKER / "pythonSource"


def testenvironment_root() -> Path:
    return source_root() / 'testenvironment'


def testmodels_dir() -> Path:
    return testenvironment_root() / 'testmodels'


def riddle_json() -> Path:
    return testmodels_dir() / RIDDLE / 'DB' / (RIDDLE + '.json')


def odmtestmodelnames():
    return [TESTMODEL1, TESTMODEL2, CRMTEST, RIDDLE]

"""init module with regenerating the testmodels db and jsons"""
try:
    Testmodel(TESTMODEL1).initDB()
except:
        print (f"could not fill {TESTMODEL1}")
try:
    Testmodel(TESTMODEL2).initDB()
except:
    print(f"could not fill {TESTMODEL2}")
try:
        Testmodel(CRMTEST).initDB()
except:
    print(f"could not fill {CRMTEST}")
try:
    Testmodel(RIDDLE).initDB()
except:
    print(f"could not fill {RIDDLE}")


