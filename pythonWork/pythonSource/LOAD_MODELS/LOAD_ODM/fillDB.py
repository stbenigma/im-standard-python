# -*- coding: latin-1 -*-
import argparse
import sys
from contextlib import closing
from pathlib import Path

from LOAD_MODELS.LOAD_ODM import transferModel
from LOAD_MODELS.LOAD_INFRA import mergedbs
from SSOT_db.IM_JSON import *
from SSOT_db.IM_OBJECTS import Language
from SSOT_db import existsDB, createnewDB
from SSOT_infra import logmessages, parameters, argparseparent


def fillmergedb(pdbfilepath, transferfunction, **kwargs):
    createnewdb = not existsDB(pdbfilepath)
    if createnewdb:
        createnewDB(pdbfilepath=pdbfilepath)
    else:
        #get languageparameter of current DB
        dbConnect.openDB(pfilepath=parameters.dbFilePath(),pversioncheck=False)
        parameters.dbDefaultLang(newval=Language.getdefaultlang().lang_iso_code2)
        langs = Language.getlanguagecodes()
        parameters.dbLanguages(newval=','.join(langs))
        dbConnect.closeDB()
        createnewDB(pdbfilepath=None)  # create in Memory
    # fi
    transferfunction(**kwargs)
    loadedjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
    dbConnect.closeDB()
    new_git_revision = parameters.read_git_description(Path(parameters.odmIMDirec()))
    loadedjson.printmodel(pfilepath=parameters.dbDirect(), pfilename=parameters.modelName() + "_loaded")
    if createnewdb:
        logging.info(f"Created SPOD for git revision {new_git_revision}")
        with closing(dbConnect.openDB(pfilepath=parameters.dbFilePath())) as conn:
            dbConnect.write_git_reversion(new_git_revision, conn)
        loadedjson.jsmodel['_imprint_']['git-revision'] = new_git_revision
        loadedjson.printmodel(pfilepath=parameters.dbDirect(), pfilename=parameters.modelName())
    else:
        """merge created DB into existing one"""
        conn = dbConnect.openDB(pfilepath=parameters.dbFilePath())
        old_git_revision = dbConnect.read_git_revision(conn)
        logging.info(f"Opening DB '{parameters.dbFilePath()}' for upgrade from git revision '{old_git_revision}'"
                     f" to git revision '{new_git_revision}'")
        newversion = loadedjson.jsmodel['_imprint_']["Modelversion"]
        if newversion != dbConnect.getversion():
            logmessages.showmessages("""existing database  {}\nhas version {} but should have {}"""
                                     .format(parameters.dbFilePath(), dbConnect.getversion(),
                                             newversion))
            raise Exception("DB-Version mismatch: found {} instead of {}".format(dbConnect.getversion(),
                                                                                 newversion))
        mergedbs.mergejson2db(pmodeljson=loadedjson)
        dbConnect.write_git_reversion(new_git_revision, conn)

        """generate json from merged DB"""
        newjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
        dbConnect.closeDB()
        spod = newjson.printmodel(pfilepath=parameters.dbDirect(), pfilename=parameters.modelName())
        logging.info(f"Updated SPOD '{spod}' to git revision {newjson.jsmodel['_imprint_']['git-revision']}")
    # fi
    return


def filldbmain(pparamfile=None, pdbtype=parameters.SQLITE, pmodelname=None, pdestination=None,
               pmodellang=None, planguages=None, plogfilepath=None, pmodelfilepath=None):
    assert (pparamfile is not None or pmodelname is not None), "Parameter file or modelname must be given"
    if pparamfile is not None:
        basedirec = os.path.abspath(os.path.dirname(pparamfile))
    elif pdestination is not None:
            basedirec = os.path.abspath(os.path.dirname(os.path.dirname(pdestination)))
    else:
        # modelname given, take current directory as basedirec
        basedirec = os.getcwd()
    # fi

    if pmodelfilepath is not None:
        filemodelname = str(os.path.basename(pmodelfilepath)).split('.')[0]
        assert (pmodelname is None or (filemodelname == pmodelname)) \
            , f"Modelname {pmodelname} does not match modelfile-name {filemodelname}"

    """Main program for fillDB"""
    parameters.initparam(pbasedirec=basedirec, pparamfile=pparamfile, pmodelname=pmodelname, pdbfile=pdestination,
                         pmodellang=pmodellang, planguages=planguages, plogfilepath=plogfilepath,
                         pmodelfilepath=pmodelfilepath)
    assert (pmodelname is None or (parameters.modelName() == pmodelname)) \
        , f"Modelname {pmodelname} does not match modelname in parameter file {parameters.modelName()}"
    assert (pmodelfilepath is None or (filemodelname == parameters.modelName())) \
        , f"Modelname {parameters.modelName()} does not match modelfile-name {filemodelname}"

    logmessages.initlog('fillDBODM')

    try:
        # create folder for DB files if not exists
        os.makedirs(parameters.dbDirect(), exist_ok=True)
        fillmergedb(pdbfilepath=parameters.dbFilePath(),
                    transferfunction=transferModel.transferODMModel)
    finally:
        logmessages.showmessages("database {} for model {} filled with modeldata and json file generated"
                                 .format(parameters.dbFilePath(),
                                         parameters.modelName()))
    return Path(parameters.dbFilePath())


def main(psysargs):
    parser = argparse.ArgumentParser(description='Fill ODM model into SSOT-DB', parents=[argparseparent.parentparser()])
    parser.add_argument('modelfilepath', nargs='?',
                        help=f"Path of the modelfile. Default ./{parameters.MODELDIREC}" +
                             f"/<modelname>{parameters.ODMMODELEXTENSION})")
    parser.add_argument('--destination', '-d', dest="destination",
                        help=f"Path of databasefile. Default ./{parameters.SSOTDBDIREC}" +
                             f"/<modelname>{parameters.SSOTDBEXTENSION})")
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
            myargs['destination'] = os.path.join(currentdir, parameters.SSOTDBDIREC,
                                                 myargs['modelname'] + parameters.SSOTDBEXTENSION)
        if myargs['modelfilepath'] is None:
            myargs['modelfilepath'] = os.path.join(currentdir, parameters.MODELDIREC,
                                                   myargs['modelname'] + parameters.ODMMODELEXTENSION)
    #fi

    if myargs['modelfilepath'] is not None:
        myargs['modelfilepath'] = os.path.abspath(myargs['modelfilepath'])

    # do only testing of parameterpassing while in unittest
    if not arguments.unittest:
        filldbmain(pparamfile=myargs['paramfile'] , pdbtype=myargs['dbtype'] , pmodelname=myargs['modelname'], pdestination=myargs['destination'] ,
                   pmodellang=myargs['modellanguage'] , planguages=myargs['languages'] , plogfilepath=myargs['logfile'] ,
                   pmodelfilepath=myargs['modelfilepath'] )
    return


if __name__ == '__main__':
    main(sys.argv)
