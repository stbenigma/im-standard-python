# -*- coding: latin-1 -*-
import os
import re
import sys

from IM_DB import dbConnect, dbCreateStructure
from SSOT_infra import parameters, logmessages
from IM_ODM import transferModel


def existsDB(pfilepath):
    return os.path.exists(pfilepath)


def createnewDB():
    dbConnect.opendDB4DDL(pfilepath=parameters.dbFilePath(), pfks='OFF');
    dbCreateStructure.applysqlscript(psqlfilepath=parameters.sqlfilepath());
    transferModel.insertBaseData()
    dbConnect.setversion()
    if dbConnect.getversion() != parameters.expecteddbversion():
        applyupgrades()
    dbConnect.closeDB()
    logmessages.showmessages("database {} version {} for model {} created"
                             .format(parameters.dbFilePath(), dbConnect.getversion()
                                 , parameters.modelName())
                             )


def version(pfilename):
    searchversion = re.search(r"\d+\.\d+",pfilename)
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
    #for
    return retval

def applyversionfile(psqlfilepath):
    dbCreateStructure.applysqlscript(psqlfilepath=psqlfilepath)
    return

def applyupgrades():
    actversion = dbConnect.getversion()
    upgrfiles = getlistofupgrfiles(psqlpath=parameters.sqlpath())
    upgrfiles.sort() #order is important as upgrades follow each other sequentally
    for upgrfile in upgrfiles:
        if version(upgrfile) <= actversion: continue
        if version(upgrfile) > parameters.expecteddbversion(): break
        applyversionfile(psqlfilepath=parameters.sqlpath() + "/" + upgrfile)
    #for
    dbConnect.setversion()

def upgradeDB():
    #get list of upgrade-files
    dbConnect.opendDB4DDL(pfilepath=parameters.dbFilePath(), pfks='OFF')
    actversion = dbConnect.getversion()
    if actversion == parameters.expecteddbversion():
        print ("DB {} is up to date: version {}".format(parameters.dbFilePath(), actversion))
        return
    applyupgrades()
    logmessages.showmessages("database {} for model {} upgraded to version {}"
                             .format(parameters.dbFilePath()
                                 , parameters.modelName()
                                 , dbConnect.getversion())
                             )
    dbConnect.closeDB()


def createDB(par1, pforcecreate=False, pupgrade=False):
    """Main program for createDB"""
    parameters.initparam(p_callarg=par1)
    logmessages.initlog('CreateDB')

    dbtype = parameters.SQLITE  # only option for the moment
    if dbtype == parameters.SQLITE:
        if existsDB(parameters.dbFilePath()):
            if pforcecreate:
                os.remove(parameters.dbFilePath())
            elif pupgrade: pass
            else:
                print("********* {}-DB-File {} already exists, cannot create it".format(parameters.SQLITE,
                                                                                        parameters.dbFilePath()))
                return
            # fi
        elif not os.path.isdir(parameters.dbDirect()):
            """falls es das Verzeichnis für die DB nicht gibt erzeuge es"""
            os.mkdir(parameters.dbDirect())
        # fi
        # here we have to create or upgrade a DB
        if pupgrade:
            upgradeDB()
        else:
            createnewDB()
        # fi
    # fi
# end main

if __name__ == '__main__':
    par1 = sys.argv[1]
    force = (len(sys.argv) > 2) and (sys.argv[2] == 'FORCE')
    upgrade = (len(sys.argv) > 2) and (sys.argv[2] == 'UPGRADE')
    createDB(par1, pforcecreate=force, pupgrade=upgrade)
