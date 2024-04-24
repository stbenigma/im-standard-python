
import os
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
DATASPOT: str = 'dataspot'


def crmmapentityhack(jscrm):
    # TODO remove unused code
    return
    ##ist jetzt bei filldb gemacht
    # DEBUG set up special mapping as load from odm does not yet work
    # reads a json file adds a subentity-Mapping and writes the file back
    tabl = jscrm.getelements("tables")
    testtablid = [key for key, val in tabl.items() if val["name"] == "ColAttr"][0]
    testcolid, testcol = [(key, val) for key, val in jscrm.getelements("columns").items() if
                          (val["table-id"] == testtablid and val["name"] == "coltosub")][0]
    attr= jscrm.getbyid("ATTR190")
    attr["columnsmapped+"][testcol["datamodel-id+"]].append(testcolid)
    testcol["attributesmapped"] = [["ATTR190", "ENTI121"]]
    return

class ModelHelper:

    def __init__(self, modelname, modeldir: Path = None):
        self.modelname = modelname
        if modeldir is None:
            modeldir = path_to_testmodels()
        self.modeldir = modeldir / modelname
        self.modelfile = modeldir / modelname / 'IM' / (modelname + '.dmd')
        self.logfile = self.modeldir / (modelname + '.log')
        self.paramfile = self.modeldir / (modelname + '.params')
        self.dbdir = self.modeldir / 'DB'
        self.dbfile = self.dbdir / (modelname + '.db')
        self.jsonfilename = modelname + '.json'
        self.jsonfile = self.dbdir / self.jsonfilename
        self.webdir = self.modeldir / 'Web'

    def initDB(self, palways=False):
        def age(ptimestamp):
            diff = datetime.datetime.now() - datetime.datetime.fromtimestamp(ptimestamp)
            return int(round(diff.total_seconds() / 60))

        #if runs on gitHub (CI=True) create new db
        if (os.getenv("CI") in [True,'True']) or palways or not os.path.exists(self.dbfile) or age(os.path.getmtime(self.dbfile)) > 60:
            if palways and os.path.exists(self.dbfile):
                os.remove(self.dbfile)
            elif os.path.exists(self.dbfile):
                # upgrade
                createDB(pmodelname=self.modelname, pupgrade=True, pdestination=self.dbfile,
                         plogfilepath=self.logfile)

            fillDB.fillmergedb(pmodelname=self.modelname, pdbfilepath=self.dbfile)

        if palways or not os.path.exists(self.jsonfile) or age(os.path.getmtime(self.jsonfile)) > 60:
            createJSON.createJSON(pdbfilepath=self.dbfile, pmodelname=self.modelname,
                                  pjsfilepath=self.dbdir, pjsfilename=self.jsonfilename)
        return self

    def remove_web_infrastructure(self,webdir = None):
        drop_web_infrastructure(webdir if webdir else self.webdir)


def drop_web_infrastructure(webdir: Path):
    assert isinstance(webdir, Path)
    # make sure new templates files are reloaded
    template_folder = webdir / "infra" / "jinjatemplates"
    if template_folder.exists():
        shutil.rmtree(template_folder)
    js_folder = webdir / "infra" / "js"
    if js_folder.exists():
        shutil.rmtree(js_folder)
    style_folder = webdir / "infra" / "css"
    if style_folder.exists():
        shutil.rmtree(style_folder)
    assert not template_folder.exists(), f"Folder '{template_folder}' should not exist"
    assert not js_folder.exists(), f"Folder '{js_folder}' should not exist"
    assert not style_folder.exists(), f"Folder '{style_folder}' should not exist"
    return


def initDB(pmodel):
    tm = ModelHelper(pmodel).initDB()
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


def path_to_testenvironment_root() -> Path:
    return source_root() / 'testenvironment'


def path_to_testmodels() -> Path:
    return path_to_testenvironment_root() / 'testmodels'


def riddle_json() -> Path:
    return path_to_testmodels() / RIDDLE / 'DB' / (RIDDLE + '.json')


def odmtestmodelnames():
    return [TESTMODEL1, TESTMODEL2, CRMTEST, RIDDLE]


"""init module with regenerating the testmodels db and jsons"""
try:
    ModelHelper(TESTMODEL1).initDB()
except:
    print(f"could not fill {TESTMODEL1}")
try:
    ModelHelper(TESTMODEL2).initDB()
except:
    print(f"could not fill {TESTMODEL2}")
try:
    ModelHelper(CRMTEST).initDB()
except:
    print(f"could not fill {CRMTEST}")
try:
    ModelHelper(RIDDLE).initDB()
except:
    print(f"could not fill {RIDDLE}")
