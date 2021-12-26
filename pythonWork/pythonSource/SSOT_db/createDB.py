# -*- coding: latin-1 -*-
import getopt
import os
import re
import sys
from pathlib import Path
from IM_db.IM_DB import  dbConnect, dbDDL
from IM_db.IM_OBJECTS import  MeltDiat, Modelelemtype, Diagramtype
from SSOT_infra import parameters, logmessages, nvl


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
    diatid = Diagramtype(pname=Diagramtype.RELATIONAL).insert()
    return


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
    """
    memorydb = ":memory:"
    dbfilepath = pdbfilepath if pdbfilepath is not None else memorydb
    dbConnect.opendDB4DDL(pfilepath=dbfilepath, pfks='OFF');
    applysqlscript(psqlfilepath=parameters.sqlfilepath());
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
    upgrfiles = getlistofupgrfiles(psqlpath=parameters.sqlpath())
    upgrfiles.sort()  # order is important as upgrades follow each other sequentally
    for upgrfile in upgrfiles:
        if version(upgrfile) <= actversion: continue
        if version(upgrfile) > parameters.expecteddbversion(): break
        applysqlscript(psqlfilepath=parameters.sqlpath() + "/" + upgrfile)
    # for
    dbConnect.setversion()


def upgradeDB():
    # get list of upgrade-files
    dbConnect.opendDB4DDL(pfilepath=parameters.dbFilePath(), pfks='OFF')
    actversion = dbConnect.getversion()
    if actversion == parameters.expecteddbversion():
        print("DB {} is up to date: version {}".format(parameters.dbFilePath(), actversion))
        return
    applyupgrades()
    dbConnect.closeDB()


def createDB(par1, pforcecreate=False, pupgrade=False, pdbtype=parameters.SQLITE):
    """create new or upgrade existing database
        par1 directory containing paramfile or model or paramfile-path
        pforcecreate => True: force new db, False: error, if db exists
        pupgrade => upgrade existing database
        pdbtype => type of db to generate
     """
    parameters.initparam(p_callarg=par1)
    logmessages.initlog('CreateDB')

    if pdbtype == parameters.SQLITE:
        if existsDB(parameters.dbFilePath()):
            if pforcecreate:
                os.remove(parameters.dbFilePath())
            elif pupgrade:
                pass
            else:
                raise Exception(f"********* {pdbtype}-DB-File {parameters.dbFilePath()} already exists, cannot create it")
            # fi
        elif not os.path.isdir(parameters.dbDirect()):
            """if there is not dbdirectory, create one"""
            os.mkdir(parameters.dbDirect())
        # fi
        # here we have to create or upgrade a DB
        if pupgrade:
            upgradeDB()
            dbConnect.closeDB()
            logmessages.showmessages(
                f"database {parameters.dbFilePath()} for model {parameters.modelName()} upgraded to version {dbConnect.getversion()}")
        else:
            createnewDB(pdbfilepath=parameters.dbFilePath())
            dbConnect.closeDB()
            logmessages.showmessages(
                f"database {parameters.dbFilePath()} version {dbConnect.getversion()} for model {parameters.modelName()} created")
        # fi
    # fi


# end main

if __name__ == '__main__':
    """create new or upgrade existing database
    
        usage: {sys.argv[0]} [-f|-u|-p] directory
          -p,--paramfile=  paramfile
          -f,--force: force creation of new database
          -u,--upgrade: upgrade existing database 
          -t,--dbtype= SQLITE 
     """

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:fut:', ['upgrade', 'force', 'paramfile=', 'dbtype='])
    except getopt.error as msg:
        print(msg)
        print(f"""usage: {sys.argv[0]} [-f|-u|-p] directory
          -p,--paramfile=  paramfile
          -f,--force: force creation of new database
          -u,--upgrade: upgrade existing database 
          -t,--dbtype= SQLITE
          """)
        sys.exit(2)
    # try
    direc: str = args[0]
    force, upgrade = False, False
    paramfile = None
    dbtype = parameters.SQLITE

    for o, a in opts:
        if o in ('-f', '--force'):
            force = True
        if o in ('-u', '--upgrade'):
            upgrade = True
        if o in ('-p', '--paramfile'):
            paramfile = a
        if o in ('-t', '--dbtype'):
            if a.lower() in (parameters.SQLITE):
                dbtype = a.lower()
            else:
                print()
                print(f"""usage: {sys.argv[0]} [-f|-u|-p] directory
                  -p,--paramfile=  paramfile
                  -f,--force: force creation of new database
                  -u,--upgrade: upgrade existing database 
                  -t,--dbtype= SQLITE
                  """)

    # for
    param1 = direc + ('' if direc.endswith('/') else '/') + nvl(paramfile)
    createDB(par1=param1, pforcecreate=force, pupgrade=upgrade, pdbtype=dbtype)
