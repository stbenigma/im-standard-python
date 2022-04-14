import traceback
import unittest
from pathlib import Path

ROOT_MARKER = 'pythonWork'
TESTMODEL1: str = 'testmodel-1'
TESTMODEL2: str = 'testmodel-2'
CRMTEST: str = 'crmTest'
RIDDLE: str = 'riddle'


def testmodel(ptestmodel):
    return ptestmodel, \
          testmodels_dir() / ptestmodel, \
         testmodels_dir() / ptestmodel / 'DB' / (ptestmodel + '.db')

def testmodel1():
    return testmodel(TESTMODEL1)

def testmodelcrm():
    return testmodel(CRMTEST)

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
