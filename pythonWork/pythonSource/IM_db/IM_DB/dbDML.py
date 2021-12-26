# -*- coding: latin-1 -*-

import re
import sqlite3

from IM_db.IM_DB import  dbConnect
from SSOT_infra import logmessages

def select(psql, *args):
    """execute a sql select statement
    returns the resultset of the sql statement
    args is the set of substitution variables "?" in the sql statement
    """
    cursor = dbConnect.getdbcon().cursor()

    try:
        cursor.execute(psql, args)
    except sqlite3.Error as e:
        print(psql)
        print(f"execute: unexpected SQL-error: \t{e}")
        raise Exception(f'Statement failed "{psql}" {args}') from e
    result = cursor.fetchall()
    return result

def exec(psql, *args):
    """execute a sql statement without returning any values
    args is the set of substitution variables "?" in the sql statement
    """

    cursor = dbConnect.getdbcon().cursor()
    try:
        cursor.execute(psql, args)
    except sqlite3.Error as e:
        print('Failed to execute {} {}'.format(psql, str(args)))
        logmessages.writelog(psql)
        logmessages.writelog(f"exec: unexpected SQL-error: \t{str(e)}")
        raise e
    dbConnect.getdbcon().commit()
    return

def delete(psql, *args):
    """execute a sql delete statement
    args is the set of substitution variables "?" in the sql statement
    returns the number of deleted rows
    """
    cursor = dbConnect.getdbcon().cursor()
    try:
        rows = cursor.execute(psql, args).rowcount
    except sqlite3.Error as e:
        logmessages.writelog(psql)
        logmessages.writelog(args)
        logmessages.writelog("unexpected SQL-error: \t%s" % e)
        raise e
    dbConnect.getdbcon().commit()
    return rows

def insert(psql, rec):
    """inserts data
    if rec is a list, insert many tuples with the values from each list element
    if rec is a tuple insert one row, rec elements used for sql-substitution "?"
    returns the id of the last inserted row
    """
    cursor = dbConnect.getdbcon().cursor()

    try:
        if (type(rec) is list):
            cursor.executemany(psql, rec)
        elif (type(rec) is tuple):
            cursor.execute(psql, rec)
        else:
            raise Exception(f"unknown type for insert {type(rec)}")
    except sqlite3.IntegrityError as ei:
        # Unique und FK kann für Indexweiterzählen gebraucht werden. darum keine Fehlermeldung
        if not (str(ei).startswith("UNIQUE constraint failed") \
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
        logmessages.writelog(f"insert: unexpected SQL-error: \t{str(e)}")
        raise e
    id = cursor.lastrowid
    dbConnect.getdbcon().commit()
    return id

def dbval(pval):
    """translates None into NULL, string into 'string' """
    return 'NULL' if pval is None \
        else str(pval) if type(pval) == int \
        else "'{}'".format(Boolean.bool2str(pval) if type(pval) == bool
                           else pval)


def execmany(psql, recs):
    """perform sql statement with a list of rows as input
    """
    cursor = dbConnect.getdbcon().cursor()
    try:
        cursor.executemany(psql, recs)
    except sqlite3.Error as e:
        if re.match("xxxxxxx", e.__str__()):
            pass
        else:
            logmessages.writelog(psql)
            logmessages.writelog(f"execmany: unexpected SQL-error: \t{e}")
            raise e
    dbConnect.getdbcon().commit()
    return


def valuepairs2sqlexpr(**colvalues):
    """changes a pair columnname, -value into a string used as sqlexpression, properly handling NULLs
       input: {colname:colvalue,}
       return "(col-name is NULL or col-name = value)" (depending on colvalue) and concatenated for every colname/-value pair
       if value is not of integer type, enclose it with '' """
    condition = ''
    for key in colvalues:
        if len(condition) > 0:
            condition = condition + ' and '
        condition = condition + '{} = ?'.format(key)
    arguments = list(colvalues.values())
    return f'({condition})', *arguments


def getrowcount(ptablename):
    """git the number of rows in the table
    """
    retval = select(psql=f"select count(*) from {ptablename}")[0][0]
    return retval
