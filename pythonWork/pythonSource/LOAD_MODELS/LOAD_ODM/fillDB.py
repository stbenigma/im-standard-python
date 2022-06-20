# -*- coding: latin-1 -*-
import argparse
import os.path
import sys

from LOAD_MODELS.LOAD_INFRA import mergedbs
from LOAD_MODELS.LOAD_ODM import transferModel,getodmparams,ODMParameter,setodmparams
from SSOT_db import existsDB, createnewDB,dbinfo
from SSOT_db.IM_JSON import *
from SSOT_db.SQL_INFRA import dbConnect
from SSOT_infra import logmessages, argparseparent,Parameter,parameters,nvl2


def ODM2json(pdebug=False) -> JSModel:
    """
        create an empty memory db
        fill odm info into this db
        Class curodmparams contains all information about source of ODM files and model

        :pdebug True, writes the filled sqlite-datase to the getodmparams().dbDirect()/<modelname>_odm.db
        :return jsonsstructure created out of ODM info
        :exception if there are sever errors
    """
    assert getodmparams().modelName() is not None, "no modelname given"
    assert os.path.exists(getodmparams().modelfilepath()), f"no ODM modelmain-file found: {getodmparams().modelfilepath()}"

    # create and open memory database
    createnewDB(pdbfilepath=None)
    transferModel.transferODMModel()

    new_git_revision = parameters.read_git_description(Path(getodmparams().imdirec()))
    dbConnect.write_git_reversion(new_git_revision, dbConnect.getdbcon())

    ODMjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
    ODMjson.jsmodel['_imprint_']['git-revision'] = new_git_revision

    if pdebug:
        debugfilepath =  str(getodmparams().dbFilePath()).replace('.db','_odm.db')
        dbConnect.makebackuptofile(pdbfile=debugfilepath)
    dbConnect.closeDB()
    return ODMjson

def configdir(pconfigdir:Path=None, pmodeldir:Path=None):
    """
    set defaults for configdirectory for ODM
    :param pconfigdir: directory with configuration files
    :param pmodeldir: Base directory of model
    :return:
    """
    if pconfigdir is None:
        retval = None
    elif os.path.isabs(pconfigdir):
        retval = Path(pconfigdir)
    else:
        retval = Path(pmodeldir) / pconfigdir

    assert retval is None or os.path.isdir(retval), f"Path for configuration files does not exist: {retval}"
    return retval

def destdir(pdestdir:Path= None,pmodeldir:Path= None):
    """
    fills default for destination directory

    :param pdestdir:  destination directory or None
    :param pmodeldir:  modelfiledirectory
    :return: pdestdir if it is not None
            pmodeldir/../DB if is None
    assertion failure, if directory does not exist
    """
    assert not (pdestdir is None and pmodeldir is None), f"with no information I would have to guess"
    if pdestdir is None:
        retval = Path(os.path.dirname(pmodeldir)) / Parameter.SPODDBDIREC
    else:
        retval = Path(pdestdir) if isinstance(pdestdir, str) else pdestdir
    assert os.path.isdir(retval), f"Destination path does not exists: {retval} "
    return retval

def transferodm2json(pmodelfile, pdefaultlang=None,planguages=None,pdestdir=None,
                     plogfilepath=None, pconfigdirec=None, pdebug=False) -> JSModel:
    """
    Reads a ODM model and transfers is into a json file.

    :param pmodelfile: .dmd file for the ODM-model
    :param pdefaultlang: iso2 code of model languagen (default 'en')
    :param pdbfilepath: directory for generated json-file
                         default <modeldirectory>/../DB
    :param pconfigdir: directory containing the ODM configuration files
                    default 1. modelfile directory / Configuration
                            2. modelfile directry / Konfiguration
    :param pdebug: True write intermediate sqlite database
                    to a db file modelname_odm.db
                    in pdbfilepath
    :return:
    """
    modelname:str = None if pmodelfile is None else Path(pmodelfile).stem
    modeldir = None if pmodelfile is None else Path(os.path.dirname(os.path.abspath(pmodelfile)))
    setodmparams(ODMParameter(imdirec=modeldir,
                            configdirec=configdir(pconfigdir=pconfigdirec,pmodeldir=modeldir),basedirec=os.path.dirname(modeldir),
                         modelname=modelname,
                         modellang=pdefaultlang, languages=planguages if planguages is not None else pdefaultlang,
                         logfilepath=plogfilepath,
                         dbdirec=destdir(pdestdir=pdestdir,pmodeldir=modeldir)     ))
    logmessages.writelog(f"Transfer ODM to SPOD Model={getodmparams().modelName()}, DB={getodmparams().dbFilePath()}")
    #set global parameter for later use
    ODMjson = ODM2json(pdebug=pdebug)
    return ODMjson


def fillmergedb(pdbfilepath, pmodelname=None,pmodelfilepath=None,pmodellang=None, planguages=None,
                pconfigdirec=None,plogfilepath=None, ):
    """
    Create or merge SPOD (sqlite and json).
    :param pdbfilepath:
    :param pmodelname: Name of model
    :param pmodellang: main language for model
    :param planguages: list of languages in model
    :param pmodelfilepath: filepath of modelfile (dmd)
    :param pconfigdirec: directory of ODM-configuration
    :return:
    """

    if pdbfilepath is None:
        assert pmodelname is not None or pmodelfilepath is not None,"Modelname or modelfile must be given"
        dbdirec = Path(os.path.abspath(os.path.dirname(os.path.dirname(pmodelfilepath)))) / Parameter.SPODDBDIREC
        dbfile = None
    else:
        dbfile = Path(pdbfilepath)
        dbdirec = dbfile.parent

    # create folder for DB files if not exists
    os.makedirs(dbdirec, exist_ok=True)

    if pmodelfilepath is not None:
        # basedirec is parent of IM directory
        basedirec = os.path.abspath(os.path.dirname(os.path.dirname(pmodelfilepath)))
    elif pdbfilepath is not None:
        # basedirec is parent of DB directory
        basedirec = os.path.abspath(os.path.dirname(os.path.dirname(pdbfilepath)))
    else:
        # take current directory as basedirec
        basedirec = os.getcwd()
    # fi

    assert not (pmodelname is None and pmodelfilepath is None), "Modelfile or modelname must be given"
    if pmodelfilepath is not None:
        modelfilepath = Path(pmodelfilepath)
        modelfilename = modelfilepath.stem
        modelname = modelfilename
    elif pmodelname is not None:
        modelname = pmodelname
        modelfilepath = os.path.join(basedirec, ODMParameter.imdefaultdirec(), (modelname + ODMParameter.imextension()))
        modelfilename = modelname

    assert (modelfilename == modelname), f"Modelname {modelname} does not match modelfile-name {modelfilename}"
    if dbfile is None:
        dbfile = dbdirec / (modelname + Parameter.SPODDBEXTENSION)

    modellang, languages = dbinfo.dblanguages(pdbfilepath=dbfile,pmodellang=pmodellang,planguages=planguages)

    logmessages.initlog('fillDBODM',plogfilepath=plogfilepath)

    """Main program for fillDB"""
    loadedjson = transferodm2json(pmodelfile=modelfilepath,
                                  pdefaultlang=modellang,planguages=languages,
                                  pdestdir=dbdirec,
                                  pconfigdirec=pconfigdirec)

    new_git_revision = parameters.read_git_description(Path(os.path.dirname(modelfilepath)))
    loaded_json_file = dbdirec / str(modelname + "_loaded.json")
    loadedjson.jsmodel['_imprint_']['git-revision'] = new_git_revision
    loadedjson.printSPOD(loaded_json_file)

    if not existsDB(dbfile):
        logging.info(f"Created SPOD for git revision {new_git_revision}")
        createnewDB(pdbfilepath=dbfile)
        dbConnect.write_git_reversion(new_git_revision, dbConnect.getdbcon())
        dbConnect.closeDB()
    else:
        ####??? braucht es das?
        dbConnect.openDB(pfilepath=dbfile)
        old_git_revision = dbConnect.read_git_revision(dbConnect.getdbcon())
        logging.info(f"Opening DB '{dbfile}' for upgrade from git revision '{old_git_revision}'"
                     f" to git revision '{new_git_revision}'")
        dbConnect.closeDB()
    # fi

    logging.debug(f"Starting merge")
    """merge created DB into existing one"""
    reloaded = mergedbs.mergejs2db(pdbfile=dbfile, pmodel=loadedjson)

    logging.debug(f"Writing reloaded model to json SPOD")
    js_spod_file = reloaded.printmodel(pfilepath=dbdirec, pfilename=modelname+'.json')
    logging.info(
        f"Merge of SPOD {js_spod_file} to git revision {reloaded.jsmodel['_imprint_']['git-revision']} complete")
    logmessages.writelog(f"model {pmodelname} filled in database: {dbfile}\n" +
                             f"jsonfile of model generated {getodmparams().dbjsonfile()}")

    logmessages.showmessages()
    return dbfile

def main(psysargs):
    """
    parses sysargs, searches for model and directories and calls
    show version

    :param psysargs:
    :return:
    """
    parser = argparse.ArgumentParser(description='Fill ODM model into SSOT-DB', parents=[argparseparent.parentparser()])
    parser.add_argument('modelfilepath', nargs='?',
                        help=f"Path of the modelfile. Default ./{ODMParameter.imdefaultdirec()}" +
                             f"/<modelname>{ODMParameter.imextension()})")
    parser.add_argument('--destination', '-d', dest="destination",
                        help=f"Path of databasefile. Default ./{Parameter.SPODDBDIREC}" +
                             f"/<modelname>{Parameter.SPODDBEXTENSION})")
    parser.add_argument('--configdirec', '-c', dest="configdirec",
                        help=f"Path of ODM configuration directory. Default IM-direc/[CK]onfiguration" +
                             f"/<modelname>{Parameter.SPODDBEXTENSION})")
    # parser.add_argument('--dbtype', '-t', dest='dbtype', default=Parameter.SQLITE,
    #                    help=f"Type of database to be created. Default '{Parameter.SQLITE}'")
    argparse.Namespace()

    if (len(psysargs) > 0) and ('.py' in psysargs[0]) and ('ipykernel' not in psysargs[0]):
        arguments: argparse.Namespace = parser.parse_args(psysargs[1:])
        myargs = arguments.__dict__
    else:
        # in jupyter environment
        """set myargs with arguments """
    # fi
    if 'version' in myargs and myargs['version']:
        argparseparent.showversion()
        exit(0)
    currentdir = os.getcwd()
    argparseparent.checkmodelandparam(parguments=myargs)
    argparseparent.fillssotdefaults(pcurrentdir=currentdir, parguments=myargs)
    if myargs['modelname'] is not None:
        if myargs['destination'] is None:
            myargs['destination'] = os.path.join(currentdir, Parameter.SPODDBDIREC,
                                                 myargs['modelname'] + Parameter.SPODDBEXTENSION)
        if myargs['modelfilepath'] is None:
            myargs['modelfilepath'] = os.path.join(currentdir, ODMParameter.imdefaultdirec(),
                                                   myargs['modelname'] + ODMParameter.imextension())
    # fi

    if myargs['modelfilepath'] is not None:
        if myargs['modelname'] is None:
            myargs['modelname'] = Path(myargs['modelfilepath']).stem
        myargs['modelfilepath'] = os.path.abspath(myargs['modelfilepath'])

    # do only testing of parameterpassing while in unittest
    if not arguments.unittest:
        fillmergedb(pmodelname=myargs['modelname'], pmodelfilepath=myargs['modelfilepath'],
                   pdbfilepath=myargs['destination'],
                   pmodellang=myargs['modellanguage'], planguages=myargs['languages'],
                   plogfilepath=myargs['logfile'],
                   pconfigdirec=myargs['configdirec'])
    return

if __name__ == '__main__':
    main(sys.argv)
