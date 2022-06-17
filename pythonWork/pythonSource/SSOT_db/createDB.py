# -*- coding: latin-1 -*-
import argparse
import os
import re
import sys
from pathlib import Path
from packaging import version

from SSOT_db.SQL_INFRA import dbConnect
from SSOT_db.SQL_INFRA import dbDDL
from SSOT_db.IM_OBJECTS import MeltDiat, Modelelemtype, Diagramtype
from SSOT_infra import parameters,Parameter, logmessages, argparseparent,nvl


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

# #no longer in use languages are filled from import
# def insertlanguages():
#     for key, value in Parameter.SUPPORTEDLANGUAGES.items():
#         if key in parameters.languages():
#             Language(lang_iso_name=value[0], lang_iso_code2=key, lang_iso_code3=value[1]).insert()
#
#     Language.setmodellang(pmodellang=parameters.modelLang())
#     Language.setallreplacementlang()
#     return


def insertBaseData():
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
        baselang and languages are used to prefill the database
        if they are None, the values from parameters are used
    """

    memorydb = ":memory:"
    dbfilepath = pdbfilepath if pdbfilepath is not None else memorydb
    connection = dbConnect.opendDB4DDL(pfilepath=dbfilepath)
    applysqlscript(psqlfilepath=Parameter.sqlfilepath())
    insertBaseData()
    dbConnect.setversion()
    dbConnect.checkson() #enable all constraints
    return connection


def extract_version(pfilename):
    searchversion = re.search(r"\d+.\d+(.\d+)?", pfilename)
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
        if re.match(r"modelmodel_sqlite_\d+.\d+(.\d+)?\.sql", el):
            retval.append(el)
    # for
    return retval


def applyupgrades():
    actversion = dbConnect.getversion()
    if actversion is None or not dbConnect.isopenDB():
        raise Exception(f"Database '{dbConnect.getDBname()}' not open")

    upgrfiles = getlistofupgrfiles(psqlpath=Parameter.sqlpath())
    upgrfiles.sort(key=lambda s:s[:-4])  # order is important as upgrades follow each other sequentally
    applied = []
    for upgrfile in upgrfiles:
        ev = version.parse(extract_version(upgrfile))
        if ev <= version.parse(actversion):
            continue
        if ev > version.parse(parameters.expecteddbversion()):
            break
        applysqlscript(psqlfilepath=os.path.join(Parameter.sqlpath(), upgrfile))
        applied.append(upgrfile)
    # for
    dbConnect.setversion()
    return applied


def upgradeDB(pdbfilepath,pmodelname):
    # get list of upgrade-files
    dbConnect.opendDB4DDL(pfilepath=pdbfilepath)
    actversion = dbConnect.getversion()
    applied = []
    if actversion is None:
        raise Exception(f"Database '{pdbfilepath}' does not contain version information.")
    elif actversion == parameters.expecteddbversion():
        print("DB {} is up to date: version {}".format(pdbfilepath, actversion))
    else:
        applied = applyupgrades()
        logmessages.showmessages(
            f"database {pdbfilepath} for model {pmodelname}" +
            f" upgraded to version {dbConnect.getversion()}")
    #fi
    dbConnect.closeDB()
    return applied

myparam:Parameter = None
def createDB(pupgrade=False, pdbtype=Parameter.SQLITE, pmodelname=None, pdestination=None,
             pmodellang=None, planguages=None, plogfilepath=None):
    """create new or upgrade existing database
        pparamfile  => paramfilepath
        pupgrade => upgrade existing database
        pdbtype => type of db to generate
        pmodelname
        pdbfilepath => Filepath of dbfile to be created
     """
    global myparam
    modelname=nvl(pmodelname)
    if pdestination is not None:
        basedirec = os.path.dirname(pdestination)
        modelname =nvl(modelname,Path(pdestination).stem)
    else:
        assert (modelname is not None), "modelname or dbfile must be given"
        # no paramfile or destination is given, take current directory as basedirec
        basedirec = os.getcwd()
    # fi
    myparam= Parameter(basedirec=basedirec, modelname=modelname, dbfilepath=pdestination,
                       modellang=pmodellang, languages=planguages, logfilepath=plogfilepath)
    try:
        logmessages.initlog('CreateDB',plogfilepath=myparam.logfilepath())

        if pdbtype == Parameter.SQLITE:
            if existsDB(myparam.dbFilePath()) and not pupgrade:
                raise Exception(
                    f"********* {pdbtype}-DB-File {myparam.dbFilePath()} already exists, cannot create it")
            elif not os.path.isdir(myparam.dbDirect()):
                """if there is not dbdirectory, create one"""
                os.mkdir(myparam.dbDirect())
            # fi
            # here we have to create or upgrade a DB
            if pupgrade:
                if existsDB(pfilepath=myparam.dbFilePath()):
                    upgradeDB(pdbfilepath=myparam.dbFilePath(),pmodelname=myparam.modelName())
                else:
                    raise Exception(f"No DB found to upgrade. {myparam.dbFilePath()}")
            else:
                createnewDB(pdbfilepath=myparam.dbFilePath())
                dbConnect.closeDB()
                logmessages.showmessages(
                    f"database {myparam.dbFilePath()} version {dbConnect.getversion()} " +
                    f"for model {myparam.modelName()} created")
            # fi
        # fi
    finally:
        logmessages.closelog()
    return myparam.dbFilePath()


def main(psysargs):
    parser = argparse.ArgumentParser(description='Create or upgrade SSOT-DB', parents=[argparseparent.parentparser()])
    parser.add_argument('--destination', '-d', dest="destination",
                        help=f"Path of databasefile. Default ./{Parameter.SPODDBDIREC}" +
                             f"/<modelname>{Parameter.SPODDBEXTENSION})")
    parser.add_argument('--upgrade', '-u', action='store_true', dest='upgrade',
                        help="Upgrade existing database to latest version.")
    argparse.Namespace()

    if (len(psysargs) > 0) and ('.py' in psysargs[0]) and ('ipykernel' not in psysargs[0]):
        arguments: argparse.Namespace = parser.parse_args(psysargs[1:])
        myargs = arguments.__dict__
    else:
        # in jupyter environment
        """set myargs with arguments """
        arguments = argparse.Namespace()
        myargs = arguments.__dict__
    # fi
    if 'version' in myargs and myargs['version']:
        argparseparent.showversion()
        exit(0)
    argparseparent.checkmodelandparam(myargs)
    argparseparent.fillssotdefaults(pcurrentdir=os.getcwd(), parguments=myargs)

    currentdir = os.getcwd()
    if myargs['modelname'] is not None:
        if myargs['destination'] is None:
            myargs['destination'] = os.path.join(currentdir, Parameter.SPODDBDIREC,
                                                 myargs['modelname'] + Parameter.SPODDBEXTENSION)

    # do only testing of parameterpassing while in unittest
    if not arguments.unittest:
        createDB(pupgrade=myargs['upgrade'], pdbtype=myargs['dbtype'],
                 pmodelname=myargs['modelname'],
                 pdestination=myargs['destination'], pmodellang=myargs['modellanguage'], planguages=myargs['languages'],
                 plogfilepath=myargs['logfile'])

if __name__ == '__main__':
    main(sys.argv)
