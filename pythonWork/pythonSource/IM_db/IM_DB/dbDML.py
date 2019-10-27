# -*- coding: latin-1 -*-

from IM_DB import dbConnect
import sqlite3
import re



def select(psql):
    cursor = dbConnect.myDbConn.cursor()

    try:
        cursor.execute(psql)
    except sqlite3.Error as e:
        if re.match("table .* already exists",e.__str__()):
            pass
        else:
            print (psql)
            print ("Unerwarteter SQL-Fehler: \t%s" % e)
            raise e
    result = cursor.fetchall()
    return result
#end select

def lookup(psql):
    cursor = dbConnect.myDbConn.cursor()

    try:
        cursor.execute(psql)
    except sqlite3.Error as e:
        if re.match("bekannter Fehler",e.__str__()):
            pass
        else:
            print ("Unerwarteter SQL-Fehler: \t%s" % e)
            raise e
    result = cursor.fetchall()
    if result == []:
        e = sqlite3.DataError('No Data Found')
        raise e
    #print ('result=',result)
    return result[0][0]
#lookup

def delete(ptableName):
    cursor = dbConnect.myDbConn.cursor()
    try:
        cursor.execute("delete from " + ptableName)
    except sqlite3.Error as e:
        if re.match("table .* already exists",e.__str__()):
            pass
        else:
            print ("Unerwarteter SQL-Fehler: \t%s" % e)
            raise e
#end delete

def insert(psql,rec):
    #print (psql,rec)
    #return
    cursor = dbConnect.myDbConn.cursor()

    try:
        if (type(rec) is list):
            cursor.executemany(psql, rec)
        elif (type(rec) is tuple):
            cursor.execute(psql, rec)
        else:
            raise Exception("unknown type for insert {}".format(type(rec)))
    except sqlite3.Error as e:
        if re.match("xxxxxxx",e.__str__()):
            pass
        else:
            print(psql, rec,type(rec))
            print ("Unerwarteter SQL-Fehler: \t{}" .format (str(e)))
            raise e
    id = cursor.lastrowid
    dbConnect.myDbConn.commit()
    return id
#end insert

def insertmany(psql,rec):
    insert(psql,rec)
    return
#end insertmany

def exec(psql,*args):
    #print (psql)
    #return
    cursor = dbConnect.myDbConn.cursor()
    try:
        cursor.execute(psql,args)
    except sqlite3.Error as e:
        print(psql)
        if re.match("xxxxxxx",e.__str__()):
            pass
        else:
            print ("Unerwarteter SQL-Fehler: \t%s" % e)
            raise e
    dbConnect.myDbConn.commit()
#end exec
def execmany(psql,recs):
    #print (psql)
    #return
    cursor = dbConnect.myDbConn.cursor()
    try:
        cursor.executemany(psql,recs)
    except sqlite3.Error as e:
        print(psql,recs)
        if re.match("xxxxxxx",e.__str__()):
            pass
        else:
            print ("Unerwarteter SQL-Fehler: \t%s" % e)
            raise e
    dbConnect.myDbConn.commit()
#execmany
