# -*- coding: latin-1 -*-

""" Datenbank erstellen bzw. dazu connecten """

import sqlite3

myDbConn: sqlite3.Connection = None
dbversion = {}

def createDB(p_filepath):
    """ erstellt eine Datenbank im Pfad mit diesem Namen """
    openDB(p_filepath)

def openDB(p_filepath,fks='OFF'):
    """ öffnet die DB pfad/Name """
    global myDbConn,dbversion
    try:
        myDbConn = sqlite3.connect(p_filepath)
        dbversion = readversion(myDbConn)
    except Exception as exp:
        raise exp
    myDbConn.execute("PRAGMA foreign_keys = {}".format(fks))

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

def getversion():
    global dbversion
    return dbversion["version"]
