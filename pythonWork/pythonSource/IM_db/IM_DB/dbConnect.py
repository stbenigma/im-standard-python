# -*- coding: latin-1 -*-

import sqlite3

from parameters import expecteddbversion

""" Datenbank erstellen bzw. dazu connecten """

myDbConn: sqlite3.Connection = None
actualdbversion = {}

def openDBbasic(pfilepath, pfks='OFF'):
    """ öffnet die DB pfad/Name """
    global myDbConn
    try:
        locconn = sqlite3.connect(pfilepath)
        myDbConn = locconn
        setversion()
    except Exception as exp:
        raise exp
    myDbConn.execute("PRAGMA foreign_keys = {}".format(pfks))

def opendDB4DDL(pfilepath, pfks="OFF"):
    """ erstellt eine Datenbank im Pfad mit diesem Namen """
    openDBbasic(pfilepath, pfks=pfks)

def openDB(pfilepath, pfks='OFF'):
    openDBbasic(pfilepath=pfilepath,pfks=pfks)
    checkversion()

def closeDB():
    global myDbConn
    myDbConn.close()
    myDBConn = None


def isopenDB():
    return myDbConn is not None


def getDBname():
    global myDbConn
    cursor = myDbConn.cursor()
    cursor.execute("PRAGMA database_list;")
    curr_table = cursor.fetchall()
    return curr_table[0][2]


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
    actversion, expversion = readversion(myDbConn)['version'], expecteddbversion()
    if actversion is not None and (actversion != expversion):
        raise Exception("DB-Versions expected {}, DB-version found {}"
                        .format(expversion, actversion))


def setversion():
    global actualdbversion, myDbConn
    actualdbversion = readversion(myDbConn)
    return


def getversion():
    global actualdbversion
    return actualdbversion["version"]
