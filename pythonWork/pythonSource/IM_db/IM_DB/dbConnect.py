# -*- coding: latin-1 -*-

""" Datenbank erstellen bzw. dazu connecten """

import sqlite3

myDbConn: sqlite3.Connection = None

def createDB(p_filepath):
    """ erstellt eine Datenbank im Pfad mit diesem Namen """
    openDB(p_filepath)

def openDB(p_filepath,fks='OFF'):
    """ öffnet die DB pfad/Name """
    global myDbConn
    try:
        myDbConn = sqlite3.connect(p_filepath)
    except Exception as exp:
        return
        raise exp
    myDbConn.execute("PRAGMA foreign_keys = {}".format(fks))

def closeDB():
    myDbConn.close()

