import json
import logging
import os
import subprocess
from pathlib import Path

from SSOT_infra.nvl import nvl

"""  Collection of all parameters for the management of the database and all tools

    Contains projectwide global parameter-Dictionary
    searches and reads parameterfile  
"""

VERSIONFILEPATH: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "versions.json")
with open(VERSIONFILEPATH, 'r') as handle:
    versions = json.load(handle)


def toolversion():
    """Version currently running
    """
    return versions['TOOLVERSION']


def expecteddbversion():
    """version of database expected in this tool version"""
    return versions['DBVERSION']


def nvlPath(p):
    if p is None: return None
    return Path(p).resolve()


class Parameter():
    SQLITE: str = 'sqlite'
    SQLFILENAME: str = 'modelmodel_' + SQLITE
    SQLEXTENSION: str = ".sql"
    SQLSERVER: str = 'sql-server'
    POSTGRES: str = 'postgres'
    LOGFILEEXTENSION: str = '.log'
    SPODDBEXTENSION: str = '.db'
    SPODDBDIREC: str = 'DB'
    JSONEXTENSION: str = '.json'
    DEFAULTLANG: str = 'en'
    SUPPORTEDLANGUAGES = \
        {'de': ['Deutsch', 'deu'],
         'en': ['English', 'eng'],
         'fr': ['Français', 'fra'],
         'es': ['Español', 'esp'],
         'it': ['Italiano', 'ita'],
         'nl': ['Nederlandse', 'nld'],
         'pl': ['Polska', 'pol'],
         'pt': ['Português', 'prt'],
         'gr': ['Ελληνικά', 'grc'],
         'bg': ['Български', 'bgr']
         }

    def __init__(self, **kwargs):
        self._basedirec = nvlPath(kwargs.get("basedirec"))
        self._dbfilepath = self.convert2abspath(nvlPath(kwargs.get('dbfilepath')))
        self._dbdirec = self.convert2abspath(nvlPath(kwargs.get('dbdirec')))
        self._modelname = kwargs.get('modelname')
        self._dbdefaultdirec: Parameter.SPODDBDIREC
        self._modellang = nvl(kwargs.get('modellang'), Parameter.DEFAULTLANG)
        self._languages = nvl(kwargs.get('languages'), Parameter.DEFAULTLANG)
        self._logfilepath = self.convert2abspath(nvlPath(kwargs.get('logfilepath')))

        assert self.modelLang() in Parameter.SUPPORTEDLANGUAGES.keys(), f"Language {self.modelLang()} not supported.  {','.join(Parameter.SUPPORTEDLANGUAGES.keys())}"
        for lang in self.languages().split(','):
            assert lang in Parameter.SUPPORTEDLANGUAGES.keys(),f"Language {lang} not supported.  [{','.join(Parameter.SUPPORTEDLANGUAGES.keys())}]"
        assert self.modelName() is not None, "no modelname given for parameters"
        return

    def baseDirec(self, newval=None):
        if newval is None:
            if self._basedirec is not None:
                return self._basedirec
            else:
                return Path(os.getcwd())
        else:
            self._basedirec = Path(newval)
            return

    def modelName(self, newval=None):
        if newval is None:
            return self._modelname
        else:
            self._modelname = newval
            return

    def logfilepath(self, newval: str = None):
        if newval is None:
            if self._logfilepath is not None:
                return self._logfilepath
            else:
                return self.baseDirec() / (self.modelName() + Parameter.LOGFILEEXTENSION)
        else:
            self._logfilepath = newval

    def logfiledirec(self):
        return os.path.dirname(self.logfilepath())

    def dbDirect(self, newval=None):
        if newval is None:
            if self._dbdirec is not None:
                return self._dbdirec
            elif self._dbfilepath is not None:
                return os.path.dirname(self._dbfilepath)
            else:
                return self._basedirec / Parameter.SPODDBDIREC
        else:
            self._dbdirec = newval
            return

    def dbFilePath(self, newval=None):
        if newval is None:
            if self._dbfilepath is not None:
                return self._dbfilepath
            elif self.dbDirect() is not None:
                return self.dbDirect() / (self.modelName() + Parameter.SPODDBEXTENSION)
            else:
                return None
        else:
            self._dbfilepath = newval
            return

    def dbjsonfile(self):
        return os.path.join(self.dbDirect(), (self.modelName() + Parameter.JSONEXTENSION))

    def modelLang(self, newval=None):
        if newval is None:
            return self._modellang
        else:
            self._modellang = newval
            return

    def languages(self, newval=None):
        if newval is None:
            if self._languages is not None:
                return self._languages
            elif self.modelLang() is not None:
                return self.modelLang()
            else:
                return None
        else:
            self._languages = newval
            return

    @staticmethod
    def dbtype():
        return Parameter.SQLITE

    @staticmethod
    def sqlpath():
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "SSOT_db", "dbstructure", "sqlite")

    @staticmethod
    def sqlfilepath():
        return os.path.join(Parameter.sqlpath(), (Parameter.SQLFILENAME + Parameter.SQLEXTENSION))

    def convert2abspath(self,p):
        if p is None:
            return None
        elif os.path.isabs(p):
            return p
        else:
            return os.path.abspath(os.path.join(self.baseDirec(), p))

# my set of parameters
parameter = None

def initparam(**kwargs):
    """
    initializes the singleton parameter object
    :param kwargs: same as for class Parameter
    :return:
    """
    global parameter
    parameter = Parameter(**kwargs)

    return


def read_git_description(folder: Path = None):
    """@:returns The git reference describing the repo status seen in folder"""
    if folder is not None:
        assert folder.is_dir()
    command = ['git', 'describe', '--always']
    try:
        git_tag = subprocess.check_output(command, cwd=str(folder), stderr=subprocess.DEVNULL).decode().strip()
        return git_tag
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.warning(f"Cannot obtain git revision from folder {folder}.\n{e}")
        return f'<unknown@{str(folder)}>'
