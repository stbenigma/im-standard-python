# -*- coding: latin-1 -*-

from IM_DB import *
import sqlite3
import re

#demo_table = """
#CREATE TABLE temp(
#id INTEGER PRIMARY KEY NOT NULL,
#fname VARCHAR(20),
#joining DATE NOT NULL,
#lohn NUMBER(8,2));"""

def createTable(psql):
    cursor = dbConnect.myDbConn.cursor()

    try:
        cursor.execute(psql)
    except sqlite3.Error as e:
        if re.match("table .* already exists",e.__str__()):
            pass
        else:
            print ("Unerwarteter SQL-Fehler: \t{}" .format(e))
            raise e
#end createTable

def dropTable(ptableName):
    cursor = dbConnect.myDbConn.cursor()

    try:
        cursor.execute("drop table "+ptableName+";")
    except sqlite3.Error as e:
        if re.match("no such table:.* ",e.__str__()):
            pass
        else:
            print ("Unerwarteter SQL-Fehler: \t{}" .format(e))
            raise e
#end dropTable
def dropView(ptableName):
    cursor = dbConnect.myDbConn.cursor()

    try:
        cursor.execute("drop view "+ptableName+";")
    except sqlite3.Error as e:
        if re.match("no such view:.* ",e.__str__()):
            pass
        else:
            print ("Unerwarteter SQL-Fehler: \t{}" .format(e))
            raise e
#end dropView

def execscript(psql):
    cursor = dbConnect.myDbConn.cursor()
    try:
        cursor.executescript(psql)
    except sqlite3.Error as e:
        if re.match("xxxxxxx",e.__str__()):
            pass
        else:
            print(psql)
            print ("exec: unexpected SQL-error: \t%s" % e)
            raise e
    dbConnect.myDbConn.commit()
#end executescript
