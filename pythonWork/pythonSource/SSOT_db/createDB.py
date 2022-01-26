# -*- coding: latin-1 -*-
import argparse
import os
import re
import sys
from pathlib import Path

from SSOT_db.SQL_INFRA import dbConnect
from SSOT_db.SQL_INFRA import dbDDL
from SSOT_db.IM_OBJECTS import MeltDiat, Modelelemtype, Diagramtype, Language
from SSOT_infra import parameters, logmessages, argparseparent


def applysqlscript(psqlfilepath):
    """
    creates the sqlite dbstructure out of psqlfilepath in the already open Databas
    """
    sqltxt = Path(psqlfilepath).read_text()
    dbDDL.execscript(psql=sqltxt)
    return


def insertdiagtypes():
    diatid = Diagramtype(pname=Diagramtype.ENTITY).insert()
    MeltDiat(pdiatid=diatid, pmeltid=Modelelemtype.getidbyshortname(pshortname=Modelelemtype.ENTI)).insert()
    MeltDiat(pdiatid=diatid, pmeltid=Modelelemtype.getidbyshortname(pshortname=Modelelemtype.RELA)).insert()
    MeltDiat(pdiatid=diatid, pmeltid=Modelelemtype.getidbyshortname(pshortname=Modelelemtype.ATTR)).insert()
    Diagramtype(pname=Diagramtype.RELATIONAL).insert()
    return


def insertlanguages():
    for key, value in parameters.SUPPORTEDLANGUAGES.items():
        if key in parameters.dbLanguages():
            Language(pname=value[0], piso2=key, piso3=value[1]).insert()

    Language.setmodellang(pmodellang=parameters.dbDefaultLang())
    Language.setallreplacementlang()
    return


def insertBaseData():
    insertlanguages()
    Modelelemtype.fillmelt()
    insertdiagtypes()
    return


def existsDB(pfilepath):
    """True if the file exists
    """
    return os.path.exists(pfilepath)


def createnewDB(pdbfilepath):
    """create a new database and fill in the basic data and leaves it open

        pdbfilepath = None => create it in memory and do not close it
    """
    memorydb = ":memory:"
    dbfilepath = pdbfilepath if pdbfilepath is not None else memorydb
    dbConnect.opendDB4DDL(pfilepath=dbfilepath, pfks='OFF')
    applysqlscript(psqlfilepath=parameters.sqlfilepath())
    insertBaseData()
    dbConnect.setversion()
    if dbConnect.getversion() != parameters.expecteddbversion():
        applyupgrades()
    return


def version(pfilename):
    searchversion = re.search(r"\d+\.\d+", pfilename)
    return searchversion[0] if searchversion else None


def getlistofupgrfiles(psqlpath):
    try:
        listdir = os.listdir(psqlpath)
    except Exception as ex:
        logmessages.writelog('getlistofupgrfiles: directory "{}" not found.'.format(psqlpath))
        raise ex
    # try
    retval = []
    for el in listdir:
        if re.match(r"modelmodel_sqlite_\d+\.\d+\.sql", el):
            retval.append(el)
    # for
    return retval


def applyupgrades():
    actversion = dbConnect.getversion()
    if actversion is None or not dbConnect.isopenDB():
        raise Exception(f"Database '{dbConnect.getDBname()}' not open")

    upgrfiles = getlistofupgrfiles(psqlpath=parameters.sqlpath())
    upgrfiles.sort()  # order is important as upgrades follow each other sequentally
    applied = []
    for upgrfile in upgrfiles:
        if version(upgrfile) <= actversion:
            continue
        if version(upgrfile) > parameters.expecteddbversion():
            break
        applysqlscript(psqlfilepath=os.path.join(parameters.sqlpath(), upgrfile))
        applied.append(upgrfile)
    # for
    dbConnect.setversion()
    return applied


def upgradeDB():
    # get list of upgrade-files
    dbConnect.opendDB4DDL(pfilepath=parameters.dbFilePath(), pfks='OFF')
    actversion = dbConnect.getversion()
    applied = []
    if actversion is None:
        raise Exception(f"Database '{parameters.dbFilePath()}' does not contain version information.")
    elif actversion == parameters.expecteddbversion():
        print("DB {} is up to date: version {}".format(parameters.dbFilePath(), actversion))
    else:
        applied = applyupgrades()
        logmessages.showmessages(
            f"database {parameters.dbFilePath()} for model {parameters.modelName()}" +
            f" upgraded to version {dbConnect.getversion()}")
    #fi
    dbConnect.closeDB()
    return applied
    return applied


def createDB(pparamfile=None, pupgrade=False, pdbtype=parameters.SQLITE, pmodelname=None, pdestination=None,
             pmodellang=None, planguages=None, plogfilepath=None):
    """create new or upgrade existing database
        pparamfile  => paramfilepath
        pupgrade => upgrade existing database
        pdbtype => type of db to generate
        pmodelname
        pdestination => Filepath of dbfile to be created
     """
    assert (pparamfile is not None or pmodelname is not None), "Parameter file or modelname must be given"
    if pparamfile is not None:
        basedirec = os.path.abspath(os.path.dirname(pparamfile))
    else:
        # modelname given, take current directory as basedirec
        basedirec = os.getcwd()
    # fi
    parameters.initparam(pbasedirec=basedirec, pparamfile=pparamfile, pmodelname=pmodelname, pdbfile=pdestination,
                         pmodellang=pmodellang, planguages=planguages, plogfilepath=plogfilepath)
    try:
        logmessages.initlog('CreateDB')

        if pdbtype == parameters.SQLITE:
            if existsDB(parameters.dbFilePath()) and not pupgrade:
                raise Exception(
                    f"********* {pdbtype}-DB-File {parameters.dbFilePath()} already exists, cannot create it")
            elif not os.path.isdir(parameters.dbDirect()):
                """if there is not dbdirectory, create one"""
                os.mkdir(parameters.dbDirect())
            # fi
            # here we have to create or upgrade a DB
            if pupgrade:
                if existsDB(pfilepath=parameters.dbFilePath()):
                    upgradeDB()
                else:
                    raise Exception(f"No DB found to upgrade. {parameters.dbFilePath()}")
            else:
                createnewDB(pdbfilepath=parameters.dbFilePath())
                dbConnect.closeDB()
                logmessages.showmessages(
                    f"database {parameters.dbFilePath()} version {dbConnect.getversion()} " +
                    f"for model {parameters.modelName()} created")
            # fi
        # fi
    finally:
        logmessages.closelog()
    return


def main(psysargs):
    parser = argparse.ArgumentParser(description='Create or upgrade SSOT-DB', parents=[argparseparent.parentparser()])
    parser.add_argument('--destination', '-d', dest="destination",
                        help=f"Path of databasefile. Default ./{parameters.SSOTDBDIREC}" +
                             f"/<modelname>{parameters.SSOTDBEXTENSION})")
    parser.add_argument('--upgrade', '-u', action='store_true', dest='upgrade',
                        help="Upgrade existing database to latest version.")

    if (len(psysargs) > 0) and ('.py' in psysargs[0]) and ('ipykernel' not in psysargs[0]):
        arguments: argparse.Namespace = parser.parse_args(psysargs[1:])
        myargs = arguments.__dict__
    else:
        # in jupyter environment
        """set myargs with arguments """
        arguments = argparse.Namespace({})
        myargs = arguments.__dict__
    # fi
    if 'version' in myargs and myargs['version']:
        argparseparent.showversion()
        exit(0)
    argparseparent.checkmodelandparam(parguments=myargs)
    argparseparent.fillssotdefaults(pcurrentdir=os.getcwd(), parguments=myargs)

    if myargs['modelname'] is not None:
        if myargs['destination'] is None:
            myargs['destination'] = os.path.join(os.getcwd(), parameters.SSOTDBDIREC,
                                                 myargs['modelname'] + parameters.SSOTDBEXTENSION)

    # do only testing of parameterpassing while in unittest
    if not arguments.unittest:
        createDB(pparamfile=myargs['paramfile'], pupgrade=myargs['upgrade'], pdbtype=myargs['dbtype'],
                 pmodelname=myargs['modelname'],
                 pdestination=myargs['destination'], pmodellang=myargs['modellanguage'], planguages=myargs['languages'],
                 plogfilepath=myargs['logfile'])


if __name__ == '__main__':
    main(sys.argv)
