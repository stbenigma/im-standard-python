import json
import os
import subprocess
import logging
from pathlib import Path

"""  Collection of all parameters for the management of the database and all tools

    Contains projectwide global parameter-Dictionary
    searches and reads parameterfile  
"""
# my set of parameters
parameter = {}

# databasetypes
SQLITE: str = 'sqlite'
SQLSERVER: str = 'sql-server'
POSTGRES: str = 'postgres'
PARAMFILEEXTENSION: str = ".params"
LOGFILEEXTENSION: str = '.log'
SPODDBEXTENSION: str = '.db'
SPODDBDIREC: str = 'DB'
MODELDIREC: str = 'IM'
WEBDEFAULTDIREC: str = 'Web'
JSONEXTENSION: str = '.json'
ODMMODELEXTENSION: str = '.dmd'
SUPPORTEDLANGUAGES = \
    {'de': ['Deutsch', 'deu'],
     'en': ['English', 'eng'],
     'fr': ['Français', 'fra'],
     'es': ['Español', 'esp'],
     'it': ['Italiano', 'ita'],
     'nl': ['Nederlandse','nld'],
     'pl': ['Polska','pol'],
     'pt': ['Português', 'prt'],
     'gr': ['Ελληνικά', 'grc'],
     'bg': ['Български', 'bgr']
     }

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


def parameterdefaults():
    global parameter
    """Initializes a dictionary of all parameters with default values
    """

    parameter = {'dbtype': SQLITE,
                 'sqlpath': os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "SSOT_db", "dbstructure",
                                         "sqlite"),
                 'sqlfilename': 'modelmodel_' + SQLITE,
                 'dbfilepath': None,
                 'dbdirec': None,
                 'modelname': None,
                 'dbfileextension': SPODDBEXTENSION,
                 'dbdefaultdirec': SPODDBDIREC,
                 'dbdefaultlang': 'en',
                 'dblanguages': 'en',
                 'dbdefaultlangid': None,
                 'basedirec': None,
                 'webdirec': None,
                 'webdefaultdirec': WEBDEFAULTDIREC,
                 'logfiledirec': None,
                 'logfilepath': None,
                 'iconmasterdocumentname': "ENTITY-ICONS"
                 }

def dbjsonfile():
    return os.path.join(dbDirect(),(modelName()+JSONEXTENSION))

def getsetparam(pparamname, pnewval: str = None):
    """returns the parameterset value named pparamname if pnewval  is None
    sets the the parameterset value to pnewval otherwise
    """

    global parameter
    if pnewval is None:
        return parameter[pparamname]
    else:
        parameter[pparamname] = pnewval
        return


def logfilepath(newval: str = None):
    """returns the parameterset value if newval is None
    sets the the parameterset value to newval otherwise
    """

    return getsetparam(pparamname='logfilepath', pnewval=newval)


def logfiledirec(newval: str = None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """

    return getsetparam(pparamname='logfiledirec', pnewval=newval)


def dbFilePath(newval=None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """

    return getsetparam(pparamname='dbfilepath', pnewval=newval)


def dbDirect(newval=None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """

    return getsetparam(pparamname='dbdirec', pnewval=newval)


def dbFileExtension(newval=None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """

    return getsetparam(pparamname='dbfileextension', pnewval=newval)


def dbDefaultDirect(newval=None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """

    return getsetparam(pparamname='dbdefaultdirec', pnewval=newval)


def dbDefaultLang(newval=None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """

    return getsetparam(pparamname='dbdefaultlang', pnewval=newval)


def dbLanguages(newval=None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """

    return getsetparam(pparamname='dblanguages', pnewval=newval)


def dbDefaultLangID(newval=None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """

    return getsetparam(pparamname='dbdefaultlangid', pnewval=newval)


def baseDirec(newval=None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """

    return getsetparam(pparamname='basedirec', pnewval=newval)


def modelName(newval=None):
    return getsetparam(pparamname='modelname', pnewval=newval)


def dbtype(newval=None):
    return getsetparam(pparamname='dbtype', pnewval=newval)


def sqlpath(newval=None):
    return getsetparam(pparamname='sqlpath', pnewval=newval)


def sqlfilename(newval=None):
    return getsetparam(pparamname='sqlfilename', pnewval=newval)

def sqlfilepath():
    return os.path.join(sqlpath(), sqlfilename() + ".sql")


def iconmasterdocumentname(newval=None):
    return getsetparam(pparamname='iconmasterdocumentname', pnewval=newval)


def webDirec(newval=None):
    return getsetparam(pparamname='webdirec', pnewval=newval)


def webDefaultDirec(newval=None):
    return getsetparam(pparamname='webdefaultdirec', pnewval=newval)

def readparamfile(pparamfilepath):
    """ read the parameter file contained in pparamfilepath

        fill the global parameter dictionnary
    """
    import configparser
    global parameter

    paramfile = configparser.RawConfigParser()
    try:
        paramfile.read(pparamfilepath)
    except:
        print("parameterfile reading error")
        raise
    # try

    for sect in paramfile.sections():
        # print (sect,paramfile[sect])
        for param in paramfile[sect]:
            val = paramfile[sect][param].strip('"' + "'")
            # print (param,paramfile[sect][param],val)
            # Grundparameter sind speziell
            if param in ('basedirec'):
                if baseDirec() is None:
                    baseDirec(newval=val)
                else:
                    # wurde schon gesetzt, muss gleich sein
                    if (val is not None) \
                            and (val != baseDirec()):
                        raise Exception("Base-direc mismatch '{}' and '{}'".format(val, baseDirec()))
                    # fi
                # fi
            elif param == 'dbdefaultlang':
                dbDefaultLang(val)
            elif param == 'dblanguages':
                dbLanguages(val)
            elif param in ('modelname'):
                if modelName() is None:
                    modelName(newval=val)
                else:
                    # wurde schon gesetzt, muss gleich sein
                    if (val is not None) \
                            and (val != modelName()):
                        raise Exception(
                            "Model name mismatch '{}' and '{}'".format(val, modelName()))
                    # fi
                # fi
            else:
                parameter[param] = val
            # fi
        # for
    # for
    """
    basedirec is special, default  is the directory of the loaded parameter file 
    """
    if baseDirec() is None:
        baseDirec(newval=os.path.abspath(os.path.dirname(os.path.realpath(pparamfilepath))))
    return


def convert2abspath(*args):
    for a in args:
        if not os.path.isabs(a()):
            a(newval=os.path.abspath(os.path.join(baseDirec(), a())))


def filldefaultparams():
    """ Parameters defaulted in relation to other parameters
    """
    if dbLanguages() is None and dbDefaultLang() is not None:
        dbLanguages(newval=dbDefaultLang())
    if dbDirect() is None:
        dbDirect(newval=os.path.join(baseDirec(), dbDefaultDirect()))
    if dbFilePath() is None:
        dbFilePath(newval=os.path.join(dbDirect(), modelName() + dbFileExtension()))
    if webDirec() is None:
        webDirec(newval=webDefaultDirec())
    if logfiledirec() is None:
        if logfilepath() is None:
            logfiledirec(newval=baseDirec())
        else:
            logfiledirec(newval=os.path.dirname(logfilepath()))
    if logfilepath() is None:
        logfilepath(os.path.join(logfiledirec(), modelName() + LOGFILEEXTENSION))

    # transform all path in parameter dict into absolut pathes
    convert2abspath(dbDirect, dbFilePath, webDirec,
                    sqlpath, logfiledirec, logfilepath)
    return


def initparam(pbasedirec, pparamfile=None, pmodelname=None, pdbfile=None, pmodellang=None, planguages=None,
              pwebdirec=None, plogfilepath=None):
    global parameter
    parameterdefaults()
    baseDirec(newval=pbasedirec)
    # provoke mismatch check in readparamfile
    if pmodelname is not None:
        modelName(newval=pmodelname)

    if pparamfile is not None and os.path.isfile(pparamfile):
        # file found, read it
        readparamfile(pparamfilepath=pparamfile)
    # fi

    # overwrite parameters from real parameters, if they exist
    if pdbfile is not None:
        dbDirect(newval=os.path.dirname(pdbfile))
        dbFilePath(newval=pdbfile)

    if pwebdirec is not None:
        webDirec(newval=pwebdirec)

    if plogfilepath is not None:
        logfiledirec(os.path.dirname(plogfilepath))
        logfilepath(plogfilepath)

    if pmodellang is not None:
        dbDefaultLang(pmodellang)

    if planguages is not None:
        dbLanguages(planguages)

    if dbDefaultLang() not in SUPPORTEDLANGUAGES.keys():
        raise Exception(f"Language {dbDefaultLang()} not supported.  {','.join(SUPPORTEDLANGUAGES.keys())}")

    for lang in dbLanguages().split(','):
        if lang not in SUPPORTEDLANGUAGES.keys():
            raise Exception(f"Language {lang} not supported.  [{','.join(SUPPORTEDLANGUAGES.keys())}]")

    if modelName() is None:
        raise Exception("no modelname given")

    filldefaultparams()

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

parameterdefaults()
