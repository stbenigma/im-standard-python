# -*- coding: latin-1 -*-

import sqlite3

from SSOT_infra import parameters

"""create database and connect to it
"""

#global db connection used for all DML statements
myDbConn: sqlite3.Connection = None
#db version read from database view dbversion
actualdbversion = {}


def openDBbasic(pfilepath, pfks='OFF'):
    """ opens the db pfilepath
    """
    try:
        locconn = sqlite3.connect(pfilepath)
        setdbcon(locconn)
        setversion()
    except Exception as exp:
        raise exp
    getdbcon().execute(f"PRAGMA foreign_keys = {pfks}")
    getdbcon().execute("PRAGMA main.cache_size = -2000")
    return locconn


def opendDB4DDL(pfilepath, pfks="OFF"):
    """ creates a database and opens it.
     by default checking is off as I want to do DDL
     """
    openDBbasic(pfilepath, pfks=pfks)


def openDB(pfilepath, pfks='OFF'):
    """opens the database pfilepath
    pfks OFF -> no checks enabled (for DDL)
        on -> checks enabled (for DML)
    checks the version and guarantees matching with version-file
    """
    openDBbasic(pfilepath=pfilepath, pfks=pfks)
    checkversion()


def closeDB():
    """ closes open DB and resets the global db-connector
    """
    getdbcon().close()
    setdbcon(None)
    return


def isopenDB():
    """if the global db for my environment open?
    """
    return getdbcon() is not None


def getDBname():
    """returns the name of the current DB"""
    cursor = getdbcon().cursor()
    cursor.execute("PRAGMA database_list;")
    curr_table = cursor.fetchall()
    return curr_table[0][2]


def setdbcon(pconn):
    """sets the global db connection to pconn"""
    global myDbConn
    myDbConn = pconn
    return


def getdbcon():
    """gets the global db connection"""
    global myDbConn
    return myDbConn


def readversion(pconn):
    """returns the current version and installation date
    from the connection pconn
    {"version": <version>, "installdate": <installationdate>}
    """
    cursor = pconn.cursor()
    try:
        cursor.execute("select * from dbversion")
        curr_table = cursor.fetchall()
    except:
        curr_table = [[None, None]]
    # try
    return {"version": curr_table[0][0]
        , "installdate": curr_table[0][1]
            }


def checkversion():
    """compares the expected db version (stored in parameters) with
    the currently opend db-Version
    raises exception if they mismatch
    """
    actversion, expversion = readversion(getdbcon())['version'], parameters.expecteddbversion()
    if actversion is not None and (actversion != expversion):
        raise Exception(f"DB-Versions expected {expversion}, DB-version found {actversion}")
    return


def setversion():
    """sets the global actualdbversion with the value out the database
    """
    global actualdbversion
    actualdbversion = readversion(getdbcon())
    return


def getversion():
    """return the version of the actually open DB
    """
    global actualdbversion
    return actualdbversion["version"]
