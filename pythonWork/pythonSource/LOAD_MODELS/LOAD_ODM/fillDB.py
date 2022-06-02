# -*- coding: latin-1 -*-
import argparse
import os.path
import sys

from LOAD_MODELS.LOAD_INFRA import mergedbs
from LOAD_MODELS.LOAD_ODM import transferModel
from SSOT_db import existsDB, createnewDB
from SSOT_db.IM_JSON import *
from SSOT_db.SQL_INFRA import dbConnect
from SSOT_infra import logmessages, parameters, argparseparent, nvl


def ODM2json(pdebug=False) -> str:
    """
        create an empty memory db
        fill odm info into this db
        Module parameters contains all information about source of ODM files and model

        :pdebug True, writes the filled sqlite-datase to the parameters.dbDirect()/<modelname>_odm.db
        :return jsonsstructure created out of ODM info
        :exception if there are sever errors
    """
    assert parameters.modelName() is not None, "no modelname given"
    odmmainfile = os.path.join(nvl(parameters.odmIMDirec(),''), nvl(parameters.modelName(),'') + nvl(parameters.odmIMExtension(),''))
    assert os.path.exists(odmmainfile), f"no ODM modelmain-file found: {odmmainfile}"

    # create and open memory database
    createnewDB(pdbfilepath=None)
    transferModel.transferODMModel()

    new_git_revision = parameters.read_git_description(Path(parameters.odmIMDirec()))
    dbConnect.write_git_reversion(new_git_revision, dbConnect.getdbcon())

    ODMjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
    ODMjson.jsmodel['_imprint_']['git-revision'] = new_git_revision

    if pdebug:
        dbConnect.makebackuptofile(pdbfile=parameters.dbDirect() / (parameters.modelName()+"_odm.db"))
    dbConnect.closeDB()
    return ODMjson

def configdir(pconfigdir:Path=None, pmodeldir:Path=None):
    """
    set defaults for configdirectory for ODM
    :param pconfigdir: directory with configuration files
    :param pmodeldir: Base directory of model
    :return:
    """
    assert not (pconfigdir is None and pmodeldir is None), f"with no information I would have to guess"
    if pconfigdir is None:
        retval = Path(pmodeldir) / 'Configuration'
        if not os.path.isdir(retval):
            retval = Path(pmodeldir) / 'Konfiguration'
    else:
        if os.path.isabs(pconfigdir) :
            retval = Path(pconfigdir) if isinstance(pconfigdir, str) else pconfigdir
        else:
            retval = Path(pmodeldir) / pconfigdir

    assert os.path.isdir(retval), f"Path for configuration files does not exist: {retval}"
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
        retval = Path(os.path.dirname(pmodeldir)) / 'DB'
    else:
        retval = Path(pdestdir) if isinstance(pdestdir, str) else pdestdir
    assert os.path.isdir(retval), f"Destination path does not exists: {retval} "
    return retval

def transferodm2json(pmodelfile, pdefaultlang=None,planguages=None,pdestdir=None, pconfigdir=None, pdebug=False):
    """
    Reads a ODM model and transfers is into a json file.

    :param pmodelfile: .dmd file for the ODM-model
    :param pdefaultlang: iso2 code of model languagen (default 'en')
    :param pdestination: directory for generated json-file
                         default <modeldirectory>/../DB
    :param pconfigdir: directory containing the ODM configuration files
                    default 1. modelfile directory / Configuration
                            2. modelfile directry / Konfiguration
    :param pdebug: True write intermediate sqlite database
                    to a db file modelname_odm.db
                    in pdestination
    :return:
    """
    modelname:str = str(os.path.basename(pmodelfile)).split('.')[0]
    modeldir = Path(os.path.dirname(os.path.abspath(pmodelfile)))
    parameters.parameterdefaults()
    parameters.modelName(modelname)
    parameters.odmKonfDirec(configdir(pconfigdir=pconfigdir,pmodeldir=modeldir))
    parameters.dbDirect(destdir(pdestdir=pdestdir,pmodeldir=modeldir))
    parameters.odmIMDirec(modeldir)
    parameters.baseDirec(os.path.dirname(modeldir))
    parameters.dbDefaultLang(pdefaultlang)
    parameters.dbLanguages(planguages if planguages is not None else pdefaultlang)
    parameters.filldefaultparams()
    ODMjson = ODM2json(pdebug=pdebug)
    return ODMjson


def fillmergedb(pdbfilepath, **kwargs):
    """
    Create or merge SPOD (sqlite and json).
    :param pdbfilepath:
    :param transferfunction:
    :param kwargs:
    :return:
    """
    dbfile = Path(pdbfilepath)
    loadedjson = transferodm2json(pmodelfile=parameters.odmIMDirec()+'/'+parameters.modelName()+parameters.odmIMExtension(),
                                  pdefaultlang=parameters.dbDefaultLang(),planguages=parameters.dbLanguages(),
                                  pdestdir=dbfile.parent,
                                  pconfigdir=parameters.odmKonfDirec())

    new_git_revision = parameters.read_git_description(Path(parameters.odmIMDirec()))
    loaded_json_file = dbfile.parent / str(dbfile.stem + "_loaded.json")
    loadedjson.jsmodel['_imprint_']['git-revision'] = new_git_revision
    loadedjson.write_json(loaded_json_file)

    if not existsDB(pdbfilepath):
        logging.info(f"Created SPOD for git revision {new_git_revision}")
        createnewDB(pdbfilepath=pdbfilepath)
        dbConnect.write_git_reversion(new_git_revision, dbConnect.getdbcon())
        dbConnect.closeDB()
    else:
        ####??? braucht es das?
        dbConnect.openDB(pfilepath=pdbfilepath)
        old_git_revision = dbConnect.read_git_revision(dbConnect.getdbcon())
        logging.info(f"Opening DB '{parameters.dbFilePath()}' for upgrade from git revision '{old_git_revision}'"
                     f" to git revision '{new_git_revision}'")
        dbConnect.closeDB()
    # fi

    logging.debug(f"Starting merge")
    """merge created DB into existing one"""
    reloaded = mergedbs.mergejs2db(pdbfile=pdbfilepath, pmodel=loadedjson)

    logging.debug(f"Writing reloaded model to json SPOD")
    js_spod_file = reloaded.printmodel(pfilepath=parameters.dbDirect(), pfilename=parameters.modelName()+'.json')
    logging.info(
        f"Merge of SPOD {js_spod_file} to git revision {reloaded.jsmodel['_imprint_']['git-revision']} complete")

    return


def filldbmain(pparamfile=None, pdbtype=parameters.SQLITE, pmodelname=None, pdestination=None,
               pmodellang=None, planguages=None, plogfilepath=None, pmodelfilepath=None):
    """
    fills the call-parameters into parameter and calls the fillmerge (read model and merge into db)
    :param pparamfile: parameterfile containing all parameters,
    :param pdbtype:  NOT USED Currently
    :param pmodelname: Name of the model
    :param pdestination:
    :param pmodellang: Baselanguage of the model (in case ODM-file does not contain any languages)
    :param planguages: languages of the model (in case ODM-file does not contain any languages)
    :param plogfilepath:  file to write the logs to
    :param pmodelfilepath: ODM-dmd file main file of ODM model
    :return: path to database file
    """

    assert (pparamfile is not None or pmodelname is not None), "Parameter file or modelname must be given"
    if pparamfile is not None:
        basedirec = os.path.abspath(os.path.dirname(pparamfile))
    elif pdestination is not None:
        #basedirec is parent of DB directory
        basedirec = os.path.abspath(os.path.dirname(os.path.dirname(pdestination)))
    else:
        # take current directory as basedirec
        basedirec = os.getcwd()
    # fi

    if pmodelfilepath is not None:
        modelfilename = str(os.path.basename(pmodelfilepath)).split('.')[0]

    """Main program for fillDB"""
    parameters.initparam(pbasedirec=basedirec, pparamfile=pparamfile, pmodelname=pmodelname, pdbfile=pdestination,
                         pmodellang=pmodellang, planguages=planguages, plogfilepath=plogfilepath,
                         pmodelfilepath=pmodelfilepath)
    assert (pmodelname is None or (parameters.modelName() == pmodelname)) \
        , f"Modelname {pmodelname} does not match modelname in parameter file {parameters.modelName()}"
    assert (pmodelfilepath is None or (modelfilename == parameters.modelName())) \
        , f"Modelname {parameters.modelName()} does not match modelfile-name {modelfilename}"

    logmessages.initlog('fillDBODM')

    try:
        # create folder for DB files if not exists
        os.makedirs(parameters.dbDirect(), exist_ok=True)
        fillmergedb(pdbfilepath=parameters.dbFilePath())
    finally:
        jsonfile=os.path.join(parameters.dbDirect(),(parameters.modelName()+'.json'))
        logmessages.showmessages(f"model {parameters.modelName()} filled in database: {parameters.dbFilePath()}\n"+
                                 f"jsonfile of model generated {jsonfile}")
    return Path(parameters.dbFilePath())


def main(psysargs):
    """
    parses sysargs, searches for model and directories and calls
    filldbmain
    show version

    :param psysargs:
    :return:
    """
    parser = argparse.ArgumentParser(description='Fill ODM model into SSOT-DB', parents=[argparseparent.parentparser()])
    parser.add_argument('modelfilepath', nargs='?',
                        help=f"Path of the modelfile. Default ./{parameters.MODELDIREC}" +
                             f"/<modelname>{parameters.ODMMODELEXTENSION})")
    parser.add_argument('--destination', '-d', dest="destination",
                        help=f"Path of databasefile. Default ./{parameters.SPODDBDIREC}" +
                             f"/<modelname>{parameters.SPODDBEXTENSION})")
    # parser.add_argument('--dbtype', '-t', dest='dbtype', default=parameters.SQLITE,
    #                    help=f"Type of database to be created. Default '{parameters.SQLITE}'")
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
            myargs['destination'] = os.path.join(currentdir, parameters.SPODDBDIREC,
                                                 myargs['modelname'] + parameters.SPODDBEXTENSION)
        if myargs['modelfilepath'] is None:
            myargs['modelfilepath'] = os.path.join(currentdir, parameters.MODELDIREC,
                                                   myargs['modelname'] + parameters.ODMMODELEXTENSION)
    # fi

    if myargs['modelfilepath'] is not None:
        myargs['modelfilepath'] = os.path.abspath(myargs['modelfilepath'])

    # do only testing of parameterpassing while in unittest
    if not arguments.unittest:
        filldbmain(pparamfile=myargs['paramfile'], pdbtype=myargs['dbtype'], pmodelname=myargs['modelname'],
                   pdestination=myargs['destination'],
                   pmodellang=myargs['modellanguage'], planguages=myargs['languages'], plogfilepath=myargs['logfile'],
                   pmodelfilepath=myargs['modelfilepath'])
    return

if __name__ == '__main__':
    main(sys.argv)
