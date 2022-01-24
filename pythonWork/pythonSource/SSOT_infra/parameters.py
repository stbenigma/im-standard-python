import json
import os

"""  Collection of all parameters for the management of the database and all tools

    Contains projectwide global parameter-Dictionary
    searches and reads parameterfile  
"""

# databasetypes
SQLITE: str = 'sqlite'
SQLSERVER: str = 'sql-server'
POSTGRES: str = 'postgres'
PARAMFILEEXTENSION: str = ".params"
LOGFILEEXTENSION: str = '.log'
SSOTDBEXTENSION: str = '.db'
SSOTDBDIREC: str = 'DB'
MODELDIREC: str = 'IM'
WEBDEFAULTDIREC: str = 'Web'
JSONEXTENSION: str = '.json'
ODMMODELEXTENSION: str = '.dmd'
SUPPORTEDLANGUAGES = \
    {'de': ['Deutsch', 'deu'],
     'en': ['English', 'eng'],
     'fr': ['Français', 'fra'],
     'es': ['Español', 'esp'],
     'it': ['Italiano', 'ita']
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
                 'dbfileextension': SSOTDBEXTENSION,
                 'dbdefaultdirec': SSOTDBDIREC,
                 'dbdefaultlang': 'en',
                 'dblanguages': 'en',
                 'dbdefaultlangid': None,
                 'basedirec': None,
                 'odmimdirec': None,
                 'odmimdefaultdirec': MODELDIREC,
                 'odmimextension': ODMMODELEXTENSION,
                 'modelname': None,
                 'odmkonfdirec': 'Konfiguration',
                 'odmdefdomainsfile': 'defaultdomains.xml',
                 'odmsettingsfile': 'dl_settings.xml',
                 'odmdefdomainsfilepath': None,
                 'odmtypesfile': 'types.xml',
                 'odmstructypesDirec': os.path.join("datatypes", "structuredtype"),
                 'odmfilesdirec': 'files',
                 'odmentitydirec': os.path.join('logical', 'entity'),
                 'odmrelationdirec': os.path.join('logical', 'relation'),
                 'odmentisubviewDirec': os.path.join('logical', 'subviews'),
                 'odmarcdirec': os.path.join('logical', 'arc'),
                 'odmdocumentDirec': os.path.join('businessinfo', 'document'),
                 'odmorgunitDirec': os.path.join('businessinfo', 'party'),
                 'odmudptranslfilename': 'translation',
                 'odmudpmappingfilename': 'datamapping',
                 'odmudpelemdisplfilename': 'elementdisplay',
                 'odmmappingDirec': 'mapping',
                 'odmudpfileextension': '.udposdm',
                 'webdirec': None,
                 'webdefaultdirec': WEBDEFAULTDIREC,
                 'logofilename': None,
                 'odmrelDirec': 'rel',
                 'odmtabledirec': 'table',
                 'odmdomainsDirec': 'domains',
                 'odmsubviewsdirec': 'subviews',
                 'odmfkdirec': 'foreignkey',
                 'logfiledirec': None,
                 'logfilepath': None,
                 'iconmasterdocumentname': "ENTITY-ICONS"
                 }


# my set of parameters
parameter: {}


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


def odmIMDirec(newval=None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """

    return getsetparam(pparamname='odmimdirec', pnewval=newval)


def odmIMDefaultDirec(newval=None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """
    return getsetparam(pparamname='odmimdefaultdirec', pnewval=newval)


def odmIMExtension(newval=None):
    return getsetparam(pparamname='odmimextension', pnewval=newval)


def modelName(newval=None):
    return getsetparam(pparamname='modelname', pnewval=newval)


def odmKonfDirec(newval=None):
    return getsetparam(pparamname='odmkonfdirec', pnewval=newval)


def odmdefdomainsfile(newval=None):
    return getsetparam(pparamname='odmdefdomainsfile', pnewval=newval)


def odmTypesFile(newval=None):
    return getsetparam(pparamname='odmtypesfile', pnewval=newval)


def odmDefDomainsfilePath(newval=None):
    return getsetparam(pparamname='odmdefdomainsfilepath', pnewval=newval)


def odmUDPTranslFileName(newval=None):
    return getsetparam(pparamname='odmudptranslfilename', pnewval=newval)


def odmUDPElemdisplFileName(newval=None):
    return getsetparam(pparamname='odmudpelemdisplfilename', pnewval=newval)


def dbtype(newval=None):
    return getsetparam(pparamname='dbtype', pnewval=newval)


def sqlpath(newval=None):
    return getsetparam(pparamname='sqlpath', pnewval=newval)


def sqlfilename(newval=None):
    return getsetparam(pparamname='sqlfilename', pnewval=newval)


def iconmasterdocumentname(newval=None):
    return getsetparam(pparamname='iconmasterdocumentname', pnewval=newval)


def odmUDPMappingFileName(newval=None):
    return getsetparam(pparamname='odmudpmappingfilename', pnewval=newval)


def odmUDPFileExtension(newval=None):
    return getsetparam(pparamname='odmudpfileextension', pnewval=newval)


def webDirec(newval=None):
    return getsetparam(pparamname='webdirec', pnewval=newval)


def webDefaultDirec(newval=None):
    return getsetparam(pparamname='webdefaultdirec', pnewval=newval)


def logoFileName(newval=None):
    return getsetparam(pparamname='logofilename', pnewval=newval)


def odmsubviewsdirec(newval=None):
    return getsetparam(pparamname='odmsubviewsdirec', pnewval=newval)


# The following pathes are ODM-specific and are all relative to the odmIMDirec
def odmspecificpath(ppath):
    return os.path.join(odmIMDirec(), modelName(), ppath)


def odmtabledirec(newval=None):
    global parameter
    if newval is None:
        return odmspecificpath(parameter['odmtabledirec'])
    else:
        parameter['odmtabledirec'] = newval
    return


def odmsettingsfile(newval=None):
    global parameter
    """settings can be in config or in ODM-directory"""
    if newval is None:
        filepath = odmspecificpath(parameter['odmsettingsfile'])
        if not os.path.exists(filepath):
            filepath = os.path.join(odmIMDirec(), odmKonfDirec(), parameter['odmsettingsfile'])
        return filepath
    else:
        parameter['odmsettingsfile'] = newval
    return


def odmentisubviewDirec(newval=None):
    global parameter
    if newval is None:
        return odmspecificpath(parameter['odmentisubviewDirec'])
    else:
        parameter['odmentisubviewDirec'] = newval
    return


def odmdocumentDirec(newval=None):
    global parameter
    if newval is None:
        return odmspecificpath(parameter['odmdocumentDirec'])
    else:
        parameter['odmdocumentDirec'] = newval
    return


def odmorgunitDirec(newval=None):
    global parameter
    if newval is None:
        return odmspecificpath(parameter['odmorgunitDirec'])
    else:
        parameter['odmorgunitDirec'] = newval
    return


def odmFilesDirec(newval=None):
    global parameter
    if newval is None:
        return odmspecificpath(parameter['odmfilesdirec'])
    else:
        parameter['odmfilesdirec'] = newval
    return


def odmstructypesDirec(newval=None):
    global parameter
    if newval is None:
        return odmspecificpath(parameter['odmstructypesDirec'])
    else:
        parameter['odmstructypesDirec'] = newval
    return


def odmEntityDirec(newval=None):
    global parameter
    if newval is None:
        return odmspecificpath(parameter['odmentitydirec'])
    else:
        parameter['odmentitydirec'] = newval
    return


def odmRelationDirec(newval=None):
    global parameter
    if newval is None:
        return odmspecificpath(parameter['odmrelationdirec'])
    else:
        parameter['odmrelationdirec'] = newval
    return


def odmArcDirec(newval=None):
    global parameter
    if newval is None:
        return odmspecificpath(parameter['odmarcdirec'])
    else:
        parameter['odmarcdirec'] = newval
    return


def odmmappingDirec(newval=None):
    global parameter
    if newval is None:
        return odmspecificpath(parameter['odmmappingDirec'])
    else:
        parameter['odmmappingDirec'] = newval
    return


def odmdomainsDirec(newval=None):
    global parameter
    if newval is None:
        return odmspecificpath(parameter['odmdomainsDirec'])
    else:
        parameter['odmdomainsDirec'] = newval
    return


def odmrelDirec(newval=None):
    global parameter
    if newval is None:
        return odmspecificpath(parameter['odmrelDirec'])
    else:
        parameter['odmrelDirec'] = newval
    return


def odmfkdirec(newval=None):
    global parameter
    if newval is None:
        return odmspecificpath(parameter['odmfkdirec'])
    else:
        parameter['odmfkdirec'] = newval
    return


def sqlfilepath():
    return os.path.join(sqlpath(), sqlfilename() + ".sql")


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
            elif param == 'odmimdirec':
                if odmIMDirec() is None:
                    odmIMDirec(newval=val)
                else:
                    # wurde schon gesetzt, muss gleich sein
                    if (val is not None) \
                            and (val != odmIMDirec()):
                        raise Exception(
                            "IM-Direc mismatch '{}' and '{}'".format(val, odmIMDirec()))
                    # fi
                # fi
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
    if odmIMDirec() is None:
        odmIMDirec(newval=os.path.join(baseDirec(), odmIMDefaultDirec()))
    if dbDirect() is None:
        dbDirect(newval=os.path.join(baseDirec(), dbDefaultDirect()))
    if dbFilePath() is None:
        dbFilePath(newval=os.path.join(dbDirect(), modelName() + dbFileExtension()))
    # Konfiguration is always relative to base direc
    if odmKonfDirec() is None:
        odmKonfDirec(newval=os.path.join(odmIMDirec(), 'Konfiguration'))
    else:
        odmKonfDirec(newval=os.path.join(odmIMDirec(), odmKonfDirec()))
    if odmDefDomainsfilePath() is None:
        odmDefDomainsfilePath(newval=os.path.join(odmKonfDirec(), odmdefdomainsfile()))
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
    convert2abspath(odmIMDirec, dbDirect, dbFilePath, odmDefDomainsfilePath, webDirec,
                    sqlpath, odmKonfDirec,
                    odmDefDomainsfilePath, logfiledirec, logfilepath)
    return


def initparam(pbasedirec, pparamfile=None, pmodelname=None, pdbfile=None, pmodellang=None, planguages=None,
              pwebdirec=None, plogfilepath=None, pmodelfilepath=None):
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
    if pmodelfilepath is not None:
        odmIMDirec(newval=os.path.dirname(pmodelfilepath))
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
