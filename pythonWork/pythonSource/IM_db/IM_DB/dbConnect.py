# -*- coding: latin-1 -*-

""" Datenbank erstellen bzw. dazu connecten """

import sqlite3

myDbConn: sqlite3.Connection = None

def createDB(ppath,pname):
    """ erstellt eine Datenbank im Pfad mit diesem Namen """
    openDB(ppath,pname)

def openDB(ppath,pname,fks='OFF'):
    """ öffnet die DB pfad/Name """
    global myDbConn
    myDbConn = sqlite3.connect(ppath.__str__()+'/'+pname)
    myDbConn.execute("PRAGMA foreign_keys = {}".format(fks))

