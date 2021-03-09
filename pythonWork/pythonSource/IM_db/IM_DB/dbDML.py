# -*- coding: latin-1 -*-

import re
import sqlite3

from IM_DB import logmessages, dbConnect


def select(psql):
    cursor = dbConnect.myDbConn.cursor()

    try:
        cursor.execute(psql)
    except sqlite3.Error as e:
        if re.match("table .* already exists", e.__str__()):
            pass
        else:
            print(psql)
            print("select: Unerwarteter SQL-Fehler: \t%s" % e)
            raise e
    result = cursor.fetchall()
    return result


# end select

def lookup(psql):
    cursor = dbConnect.myDbConn.cursor()

    try:
        cursor.execute(psql)
    except sqlite3.Error as e:
        if re.match("bekannter Fehler", e.__str__()):
            pass
        else:
            print("lookup: Unerwarteter SQL-Fehler: \t%s" % e)
            raise e
    result = cursor.fetchall()
    if result == []:
        e = sqlite3.DataError('No Data Found')
        raise e
    # print ('result=',result)
    return result[0][0]


# lookup

def delete(ptableName, pwhere=None):
    cursor = dbConnect.myDbConn.cursor()
    try:
        sql = "delete from {} where {}".format(ptableName, "1=1" if pwhere is None else pwhere)
        cursor.execute(sql)
    except sqlite3.Error as e:
        logmessages.writelog(sql)
        logmessages.writelog("unexpected SQL-error: \t%s" % e)
        raise e
    dbConnect.myDbConn.commit()


# delete

def insert(psql, rec):
    # print (psql,rec)
    cursor = dbConnect.myDbConn.cursor()

    try:
        if (type(rec) is list):
            cursor.executemany(psql, rec)
        elif (type(rec) is tuple):
            cursor.execute(psql, rec)
        else:
            raise Exception("unknown type for insert {}".format(type(rec)))
    except sqlite3.IntegrityError as ei:
        # Unique kann für Indexweiterzählen gebraucht werden. darum keine Fehlermeldung
        if not str(ei).startswith('UNIQUE'):
            logmessages.writelog(psql)
            logmessages.writelog(rec)
            logmessages.writelog(type(rec))
            logmessages.writelog("insert: Constraint-error: \t{}".format(str(ei)))
        # fi
        raise ei
    except sqlite3.Error as e:
        logmessages.writelog(psql)
        logmessages.writelog(rec)
        logmessages.writelog(type(rec))
        logmessages.writelog("insert: unexpected SQL-error: \t{}".format(str(e)))
        raise e
    id = cursor.lastrowid
    dbConnect.myDbConn.commit()
    return id


# insert

def insertmany(psql, rec):
    insert(psql, rec)
    return

# end insertmany

def exec(psql, *args):
    # print (psql)
    # return
    cursor = dbConnect.myDbConn.cursor()
    try:
        cursor.execute(psql, args)
    except sqlite3.Error as e:
        if re.match("xxxxxxx", e.__str__()):
            pass
        else:
            logmessages.writelog(psql)
            logmessages.writelog("exec: unexpected SQL-error: \t%s" % e)
            raise e
    dbConnect.myDbConn.commit()


# end exec
def execmany(psql, recs):
    # print (psql)
    # return
    cursor = dbConnect.myDbConn.cursor()
    try:
        cursor.executemany(psql, recs)
    except sqlite3.Error as e:
        if re.match("xxxxxxx", e.__str__()):
            pass
        else:
            logmessages.writelog(psql)
            logmessages.writelog("execmany: unexpected SQL-error: \t%s" % e)
            raise e
    dbConnect.myDbConn.commit()


# execmany

def valuepairs2sqlexpr(**colvalues):
    """input: {colname:colvalue,}
       return "(col-name is NULL or col-name = value)" (depending on colvalue) and concatenated for every colname/-value pair
       if value is not of integer type, enclose it with '' """
    sqlstring = lambda val: "'{}'".format(val) if type(val) != int else str(val)
    comp = lambda col, val: "{} is null".format(col) if val is None else "{} = {}".format(col, sqlstring(val))
    retval = " and ".join("({})".format(comp(col, val)) for col, val in colvalues.items())
    return retval


def id2uktranslate():
    """from currently open db, return list of all id's together with their UK-columns
        {<tableshortname>id : {colname:value,}} for every column being in a uk
    """
    tables = select(psql="""SELECT name
                            FROM sqlite_master
                            WHERE type = 'table' 
                            AND name NOT LIKE'sqlite_%'""")
    retval = {}
    for tab in tables:
        t = tab[0]
        rows = t

