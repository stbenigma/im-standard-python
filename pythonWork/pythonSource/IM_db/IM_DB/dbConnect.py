# -*- coding: latin-1 -*-

import sqlite3

from IM_DB import parameters

""" Datenbank erstellen bzw. dazu connecten """

myDbConn: sqlite3.Connection = None
actualdbversion = {}

def openDBbasic(pfilepath, pfks='OFF'):
    """ öffnet die DB pfad/Name """
    try:
        locconn = sqlite3.connect(pfilepath)
        setdbcon(locconn)
        setversion()
    except Exception as exp:
        raise exp
    getdbcon().execute("PRAGMA foreign_keys = {}".format(pfks))
    return

def opendDB4DDL(pfilepath, pfks="OFF"):
    """ erstellt eine Datenbank im Pfad mit diesem Namen """
    openDBbasic(pfilepath, pfks=pfks)

def openDB(pfilepath, pfks='OFF'):
    openDBbasic(pfilepath=pfilepath,pfks=pfks)
    checkversion()

def closeDB():
    getdbcon().close()
    setdbcon(None)
    return


def isopenDB():
    return getdbcon() is not None


def getDBname():

    cursor = getdbcon().cursor()
    cursor.execute("PRAGMA database_list;")
    curr_table = cursor.fetchall()
    return curr_table[0][2]

def setdbcon(pconn):
    global myDbConn
    myDbConn = pconn
    return

def getdbcon():
    global myDbConn
    return myDbConn

def readversion(pconn):
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
    actversion, expversion = readversion(getdbcon())['version'], parameters.expecteddbversion()
    if actversion is not None and (actversion != expversion):
        raise Exception("DB-Versions expected {}, DB-version found {}"
                        .format(expversion, actversion))
    return


def setversion():
    global actualdbversion
    actualdbversion = readversion(getdbcon())
    return


def getversion():
    global actualdbversion
    return actualdbversion["version"]
