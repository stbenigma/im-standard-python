import json
import os
import re
from pathlib import Path

"""  Collection of all parameters for the management of the database and all tools

    Contains projectwide global parameter-Dictionary
    searches and reads parameterfile  
"""

ODMMODELNAME: str = 'odmmodelname'  # to be removed
MODELNAME: str = 'modelname'
ODMIMDIREC: str = 'odmimdirec'
ODMBASEDIREC: str = 'odmbasedirec'  # to be removed
BASEDIREC: str = 'basedirec'
DBDEFAULTLANG: str = 'dbdefaultlang'
DBLANGUAGES: str = 'dblanguages'
LOGFILEDIREC: str = 'logfiledirec'
LOGFILEPATH: str = 'logfilepath'
VERSIONFILEPATH: str = os.path.dirname(os.path.abspath(__file__)) + "/versions.json"
with open(VERSIONFILEPATH, 'r') as handle:
    versions = json.load(handle)


def toolversion():
    """Version currently running
    """
    return versions['TOOLVERSION']


def expecteddbversion():
    """version of database expected in this tool version"""
    return versions['DBVERSION']


SQLITE: str = 'sqlite'
SQLSERVER: str = 'sql-server'
POSTGRES: str = 'postgres'
PARAMFILEEXTENSION: str = ".params"


def parameterdefaults():
    global parameter
    """Initializes a dictionary of all parameters with default values
    """

    parameter = {'dbtype': SQLITE
        , 'sqlpath': os.path.dirname(os.path.abspath(__file__)) + "/../SSOT_db/dbstructure/sqlite/"
        , 'sqlfilename': 'modelmodel_' + SQLITE
        , 'dbfilepath': None
        , 'dbdirec': None
        , 'dbfileextension': '.db'
        , 'dbdefaultdirec': 'DB/'
        , DBDEFAULTLANG: 'de'
        , DBLANGUAGES: 'de'
        , 'dbdefaultlangid': None
        , BASEDIREC: None
        , 'localbasedirec': None
        , ODMIMDIREC: None
        , 'odmimdefaultdirec': 'IM/'
        , 'odmimextension': '.dmd'
        , MODELNAME: None
        , 'odmkonfdirec': 'Konfiguration/'
        , 'odmdefdomainsfile': 'defaultdomains.xml'
        , 'odmsettingsfile': 'dl_settings.xml'
        , 'odmdefdomainsfilepath': None
        , 'odmtypesfile': 'types.xml'
        , 'odmstructypesdir': "datatypes/structuredtype/"
        , 'odmfilesdirec': 'files/'
        , 'odmentitydirec': 'logical/entity/'
        , 'odmrelationdirec': 'logical/relation/'
        , 'odmentisubviewdirec': 'logical/subviews/'
        , 'odmarcdirec': 'logical/arc/'
        , 'odmdocumentdirec': 'businessinfo/document/'
        , 'odmorgunitdirec': 'businessinfo/party/'
        , 'odmudptranslfilename': 'translation'
        , 'odmudpmappingfilename': 'datamapping'
        , 'odmudpelemdisplfilename': 'elementdisplay'
        , 'odmmappingdirec': 'mapping/'
        , 'odmudpfileextension': '.udposdm'
        , 'odmvcsdirec': 'gitHub/'
        , 'webdirec': None
        , 'webdefaultdirec': 'Web/'
        , 'logofilename': None
        , 'odmreldirec': 'rel/'
        , 'odmtabledirec': 'table/'
        , 'odmdomainsdirec': 'domains/'
        , 'odmsubviewsdirec': 'subviews/'
        , 'odmfkdirec': 'foreignkey/'
        , LOGFILEDIREC: None
        , LOGFILEPATH: None
        , 'iconmasterdocumentname': "ENTITY-ICONS"
            }


# my set of parameters
parameter: dict()


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

    return getsetparam(pparamname=LOGFILEPATH, pnewval=newval)


def logfiledirec(newval: str = None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """

    return getsetparam(pparamname=LOGFILEDIREC, pnewval=newval)


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

    return getsetparam(pparamname=DBDEFAULTLANG, pnewval=newval)


def dbLanguages(newval=None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """

    return getsetparam(pparamname=DBLANGUAGES, pnewval=newval)


def dbDefaultLangID(newval=None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """

    return getsetparam(pparamname='dbdefaultlangid', pnewval=newval)


def baseDirec(newval=None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """

    return getsetparam(pparamname=BASEDIREC, pnewval=newval)


def odmIMDirec(newval=None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """

    return getsetparam(pparamname=ODMIMDIREC, pnewval=newval)


def odmIMDefaultDirec(newval=None):
    """returns the parameterset value if functionparameter is None
    sets the the parameterset value if it is not None
    """
    return getsetparam(pparamname='odmimdefaultdirec', pnewval=newval)


def odmIMExtension(newval=None):
    return getsetparam(pparamname='odmimextension', pnewval=newval)


def modelName(newval=None):
    return getsetparam(pparamname=MODELNAME, pnewval=newval)


def odmsettingsfile(newval=None):
    global parameter
    if newval is None:
        filepath = odmIMDirec() + modelName() + '/' + parameter['odmsettingsfile']
        if not os.path.exists(filepath):
            filepath = odmIMDirec() + odmKonfDirec() + parameter['odmsettingsfile']
        return filepath
    else:
        parameter['odmsettingsfile'] = newval


def odmentisubviewdirec(newval=None):
    global parameter
    if newval is None:
        return odmIMDirec() + modelName() + '/' + parameter['odmentisubviewdirec']
    else:
        parameter['odmentisubviewdirec'] = newval


def odmKonfDirec(newval=None):
    return getsetparam(pparamname='odmkonfdirec', pnewval=newval)


def odmVCSDirec(newval=None):
    return getsetparam(pparamname='odmvcsdirec', pnewval=newval)


def odmdefdomainsfile(newval=None):
    return getsetparam(pparamname='odmdefdomainsfile', pnewval=newval)


def localbasedirec(newval=None):
    return getsetparam(pparamname='localbasedirec', pnewval=newval)


def odmdocumentdirec(newval=None):
    global parameter
    if newval is None:
        return odmIMDirec() + modelName() + '/' + parameter['odmdocumentdirec']
    else:
        parameter['odmdocumentdirec'] = newval


def odmorgunitdirec(newval=None):
    global parameter
    if newval is None:
        return odmIMDirec() + modelName() + '/' + parameter['odmorgunitdirec']
    else:
        parameter['odmorgunitdirec'] = newval


def odmDefDomainsfilePath(newval=None):
    return getsetparam(pparamname='odmdefdomainsfilepath', pnewval=newval)


def odmTypesFile(newval=None):
    return getsetparam(pparamname='odmtypesfile', pnewval=newval)


def odmFilesDirec(newval=None):
    global parameter
    if newval is None:
        return odmIMDirec() + modelName() + '/' + parameter['odmfilesdirec']
    else:
        parameter['odmfilesdirec'] = newval


def odmstructypesdir(newval=None):
    global parameter
    if newval is None:
        return odmIMDirec() + modelName() + '/' + parameter['odmstructypesdir']
    else:
        parameter['odmstructypesdir'] = newval


def odmEntityDirec(newval=None):
    global parameter
    if newval is None:
        return odmIMDirec() + modelName() + '/' + parameter['odmentitydirec']
    else:
        parameter['odmentitydirec'] = newval


def odmRelationDirec(newval=None):
    global parameter
    if newval is None:
        return odmIMDirec() + modelName() + '/' + parameter['odmrelationdirec']
    else:
        parameter['odmrelationdirec'] = newval


def odmArcDirec(newval=None):
    global parameter
    if newval is None:
        return odmIMDirec() + modelName() + '/' + parameter['odmarcdirec']
    else:
        parameter['odmarcdirec'] = newval


def odmUDPTranslFileName(newval=None):
    return getsetparam(pparamname='odmudptranslfilename', pnewval=newval)


def odmUDPElemdisplFileName(newval=None):
    return getsetparam(pparamname='odmudpelemdisplfilename', pnewval=newval)


def odmmappingdirec(newval=None):
    global parameter
    if newval is None:
        return odmIMDirec() + modelName() + '/' + parameter['odmmappingdirec']
    else:
        parameter['odmmappingdirec'] = newval


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


def odmtabledirec(newval=None):
    return getsetparam(pparamname='odmtabledirec', pnewval=newval)


def odmdomainsdirec(newval=None):
    global parameter
    if newval is None:
        return odmIMDirec() + modelName() + '/' + parameter['odmdomainsdirec']
    else:
        parameter['odmdomainsdirec'] = newval


def odmsubviewsdirec(newval=None):
    return getsetparam(pparamname='odmsubviewsdirec', pnewval=newval)


def odmfkdirec(newval=None):
    return getsetparam(pparamname='odmfkdirec', pnewval=newval)


def odmreldirec(newval=None):
    global parameter
    if newval is None:
        return odmIMDirec() + modelName() + '/' + parameter['odmreldirec']
    else:
        parameter['odmreldirec'] = newval


def dbtype(newval=None):
    return getsetparam(pparamname='dbtype', pnewval=newval)


def sqlpath(newval=None):
    return getsetparam(pparamname='sqlpath', pnewval=newval)


def sqlfilename(newval=None):
    return getsetparam(pparamname='sqlfilename', pnewval=newval)


def iconmasterdocumentname(newval=None):
    return getsetparam(pparamname='iconmasterdocumentname', pnewval=newval)


def sqlfilepath():
    return sqlpath() + sqlfilename() + ".sql"


def readparamfile(p_filepath):
    """ read the parameter file contained in p_filepath

        fill the global parameter dictionnary
    """
    import configparser
    global parameter

    paramfile = configparser.RawConfigParser()
    try:
        paramfile.read(p_filepath)
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
            if param in (ODMBASEDIREC, BASEDIREC):  # ODMBASEDIREC to be removed
                if baseDirec() is None:
                    baseDirec(newval=val)
                else:
                    # wurde schon gesetzt, muss gleich sein
                    if (val is not None) \
                            and (val != baseDirec()):
                        raise Exception("Base-direc mismatch '{}' and '{}'".format(val, baseDirec()))
                    # fi
                # fi
            elif param == DBDEFAULTLANG:
                dbDefaultLang(val)
            elif param == DBLANGUAGES:
                dbLanguages(val)
            elif param == ODMIMDIREC:
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
            elif param in (ODMMODELNAME, MODELNAME):  # ODMMODELNAME to be removed
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
        baseDirec(newval=os.path.dirname(os.path.realpath(p_filepath)) + '/')
    return


# readparamfile

def filldefaultparams():
    """ Parameters defaulted in relation to other parameters

    """
    if localbasedirec() is None:
        localbasedirec(newval=baseDirec())
    if odmIMDirec() is None:
        odmIMDirec(newval=baseDirec() + odmIMDefaultDirec())
    if dbDirect() is None:
        dbDirect(newval=localbasedirec() + dbDefaultDirect())
    if dbFilePath() is None:
        dbFilePath(newval=dbDirect() + modelName() + dbFileExtension())
    if odmDefDomainsfilePath() is None:
        odmDefDomainsfilePath(newval=odmIMDirec() + odmKonfDirec() + odmdefdomainsfile())
    if webDirec() is None:
        webDirec(newval=localbasedirec() + webDefaultDirec())
    if logfiledirec() is None:
        logfiledirec(localbasedirec())
    if logfilepath() is None:
        logfilepath(logfiledirec() + modelName() + '.log')
    return


def lookfor1file(p_direc):
    """ search one file in directory and returns
         modelname (=filenamepart of dmd-file) if exactly one exists

        return None if none exists
        raise excpetion if multiple exist
    """
    lretval = None
    dmdfiles = []
    try:
        dmdfiles = [f for f in os.listdir(p_direc) if re.match('.+'+re.escape(odmIMExtension()),f)]
    except Exception as e:
        pass
    # fi
    if (len(dmdfiles) == 1):
        # exactly one found, return filename (without extension)
        lretval = re.sub(odmIMExtension(), '', dmdfiles[0])
    elif (len(dmdfiles) == 0):
        pass  # to be handled by caller
    else:
        raise Exception("more than 1 model found in {}".format(p_direc))
    # fi
    return lretval


def lookformodelname(p_direc):
    """ get the name for the only .dmd file
        search in sequence ./  ./IM/ and  ./gitHub/IM/
    """
    immodelname = lookfor1file(p_direc=p_direc)
    if immodelname is not None:
        imdirectory = p_direc
    else:
        # look in ./IM
        testdirec = p_direc + odmIMDefaultDirec()
        immodelname = lookfor1file(p_direc=testdirec)
        if immodelname is not None:
            imdirectory = testdirec
        else:
            """search in the gitHub/IM directory"""
            testdirec = p_direc + odmVCSDirec() + odmIMDefaultDirec()
            immodelname = lookfor1file(p_direc=testdirec)
            if (immodelname is not None):
                imdirectory = testdirec
            else:
                raise Exception("No model found in {}...".format(p_direc))
            # fi
        # fi
    # fi
    return (imdirectory, immodelname)


def initparam(p_callarg, pfileonly=False):
    global parameter
    parameterdefaults()
    my_file = Path(p_callarg)
    if my_file.is_file():
        # file found, read it
        paramfile = p_callarg
    elif my_file.is_dir():
        #add / if necessary
        if (p_callarg[-1] != '/'):
            p_callarg = p_callarg + '/'
        # got directory, look for a model (only dmd in directory) and then for param file with same name
        (imdirec, modelname) = lookformodelname(p_direc=p_callarg)
        odmIMDirec(newval=imdirec)
        baseDirec(newval=imdirec[0:len(imdirec) - len(odmIMDefaultDirec())] if (
                imdirec.split('/')[-2] + '/' == odmIMDefaultDirec()) else imdirec)
        modelName(newval=modelname)
        paramfile = p_callarg + modelname + PARAMFILEEXTENSION
    else:
        print(my_file)
        if pfileonly:
            raise Exception("parameter is no file")
        else:
            raise Exception("parameter is neither file nor directory")

    if os.path.exists(paramfile):
        readparamfile(p_filepath=paramfile)
    elif ((odmIMDirec() is None) or (modelName() is None) or pfileonly):
        # check for minimal information
        raise Exception('No parameter file and no model found in "{}"'.format(p_callarg))
    # fi
    filldefaultparams()
    return
