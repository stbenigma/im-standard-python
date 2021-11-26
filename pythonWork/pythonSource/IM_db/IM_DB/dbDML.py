# -*- coding: latin-1 -*-

import re
import sqlite3

from IM_DB import dbConnect
from SSOT_infra import logmessages


def select(psql,*args):
    cursor = dbConnect.getdbcon().cursor()

    try:
        cursor.execute(psql,args)
    except sqlite3.Error as e:
        if re.match("table .* already exists", e.__str__()):
            pass
        else:
            print(psql)
            print("select: Unerwarteter SQL-Fehler: \t%s" % e)
            raise e
    result = cursor.fetchall()
    return result


def execute(psql, *args):
    cursor = dbConnect.getdbcon().cursor()

    try:
        cursor.execute(psql, args)
    except sqlite3.Error as e:
        if re.match("table .* already exists", e.__str__()):
            pass
        else:
            print(psql)
            print("execute: Unerwarteter SQL-Fehler: \t%s" % e)
            raise Exception('Statement failed "{}" {}'.format(psql, args)) from e
    result = cursor.fetchall()
    return result

# end select

def lookup(psql):
    cursor = dbConnect.getdbcon().cursor()

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

def delete(psql, *args):
    cursor = dbConnect.getdbcon().cursor()
    try:
        rows = cursor.execute(psql,args).rowcount
    except sqlite3.Error as e:
        logmessages.writelog(psql)
        logmessages.writelog(args)
        logmessages.writelog("unexpected SQL-error: \t%s" % e)
        raise e
    dbConnect.getdbcon().commit()
    return rows
# delete

def insert(psql, rec):
    # print (psql,rec)
    cursor = dbConnect.getdbcon().cursor()

    try:
        if (type(rec) is list):
            cursor.executemany(psql, rec)
        elif (type(rec) is tuple):
            cursor.execute(psql, rec)
        else:
            raise Exception("unknown type for insert {}".format(type(rec)))
    except sqlite3.IntegrityError as ei:
        # Unique und FK kann für Indexweiterzählen gebraucht werden. darum keine Fehlermeldung
        if not (str(ei).startswith("UNIQUE constraint failed")\
                or str(ei).startswith("FOREIGN KEY constraint failed")):
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
    dbConnect.getdbcon().commit()
    return id
# insert

def insertmany(psql, rec):
    insert(psql, rec)
    return

# end insertmany

def exec(psql, *args):
    # print (psql)
    # return
    cursor = dbConnect.getdbcon().cursor()
    try:
        cursor.execute(psql, args)
    except sqlite3.Error as e:
        print('Failed to execute {} {}'.format(psql, str(args)))
        if re.match("xxxxxxx", e.__str__()):
            pass
        else:
            logmessages.writelog(psql)
            logmessages.writelog("exec: unexpected SQL-error: \t%s" % e)
            raise e
    dbConnect.getdbcon().commit()
# end exec

"""translates None into NULL, string into 'string' """
def dbval(pval):
    return 'NULL' if pval is None \
                else str(pval) if type(pval)==int \
                else "'{}'".format(Boolean.bool2str(pval) if type(pval)==bool
                                    else pval)

def execmany(psql, recs):
    # print (psql)
    # return
    cursor = dbConnect.getdbcon().cursor()
    try:
        cursor.executemany(psql, recs)
    except sqlite3.Error as e:
        if re.match("xxxxxxx", e.__str__()):
            pass
        else:
            logmessages.writelog(psql)
            logmessages.writelog("execmany: unexpected SQL-error: \t%s" % e)
            raise e
    dbConnect.getdbcon().commit()
# execmany

def valuepairs2sqlexpr(**colvalues):
    """input: {colname:colvalue,}
       return "(col-name is NULL or col-name = value)" (depending on colvalue) and concatenated for every colname/-value pair
       if value is not of integer type, enclose it with '' """
#    sqlstring = lambda val: "'{}'".format(val) if type(val) != int else str(val)
#    comp = lambda col, val: "{} is null".format(col) if val is None else "{} = {}".format(col, sqlstring(val))
#    retval = " and ".join("({})".format(comp(col, val)) for col, val in colvalues.items())
#    return retval

    condition = ''
    for key in colvalues:
        if len(condition) > 0:
            condition = condition + ' and '
        condition = condition + '{} = ?'.format(key)
    arguments = list(colvalues.values())
    return '({})'.format(condition), *arguments


def getrowcount(ptablename):
    retval = select(psql="select count(*) from {}".format(ptablename))[0][0]
    return retval