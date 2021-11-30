# -*- coding: latin-1 -*-

import re
import sqlite3

from IM_DB import dbConnect

def concursor(pconn):
    """
    establish a connection if it not yet done.
    et a cursor from the connection
    """
    conn = pconn if pconn is not None else dbConnect.myDbConn
    return conn.cursor()

def createTable(psql, pconn=None):
    """
    create a table with the definition in psql.
    If it alreday exists, skip the error.
    """
    cursor = concursor(pconn)
    try:
        cursor.execute(psql)
    except sqlite3.Error as e:
        if re.match("table .* already exists", e.__str__()):
            pass
        else:
            print(f"Unexpected SQL-error: \t{e}")
            raise e
    return

def dropTable(ptableName, pconn=None):
    """
    drop the table with ptablename
    If it did not exist, skip the error.
    """
    cursor = concursor(pconn)

    try:
        cursor.execute("drop table " + ptableName + ";")
    except sqlite3.Error as e:
        if re.match("no such table:.* ", e.__str__()):
            pass
        else:
            print(f"Unexpected SQL-error: \t{e}")
            raise e
    return


def dropView(pviewName, pconn=None):
    """
    drop the view with pviewName
    If it did not exist, skip the error.
    """
    cursor = concursor(pconn)
    try:
        cursor.execute("drop view " + pviewName + ";")
    except sqlite3.Error as e:
        if re.match("no such view:.* ", e.__str__()):
            pass
        else:
            print(f"Unexpected SQL-error: \t{e}")
            raise e
    return

def execscript(psql, pconn=None):
    """
    execute the sqlstatement in psql
    in case of error, print the statement + an errormessage to standard outpout and reraise the error
    """
    cursor = concursor(pconn)
    try:
        cursor.executescript(psql)
    except sqlite3.Error as e:
        print(psql)
        print(f"Unexpected SQL-error: \t{e}")
        raise e
    dbConnect.myDbConn.commit()
    return


def getuklist(ptablename, pconn=None):
    """List of all uk (list of columns) for the table ptablename
     return a list of lists of columnnames [[colname,],]
     """
    cursor = concursor(pconn)
    cursor.execute("PRAGMA index_list('{}')".format(ptablename))
    indices = cursor.fetchall()
    """index_list [seq,name,unique(0,1),origin (u),partial]
        index_info [seqno,cid,colname]
        foreign_key_list [id,seq,table,from,to,on_update (NO_ACTION),on_delete(CASCADE),match]
        """
    retval = []
    for i in indices:
        if i[2] == 1 and i[3] == 'u':
            """unique key"""
            cursor.execute("PRAGMA index_info('{}')".format(i[1]))
            cols = cursor.fetchall()
            retval.append([c[2] for c in sorted(cols)])
        # fi
    # for
    cursor.close()
    return retval


def getfklist(ptablename, pconn=None):
    """List of all foreign keys (with columns) of table ptablename
    return {colname:[fktable,fkcolname]} all names in lowercase
    """
    cursor = concursor(pconn)
    cursor.execute("PRAGMA foreign_key_list('{}')".format(ptablename))
    fks = cursor.fetchall()
    """foreign_key_list [id,seq,table,from,to,on_update (NO_ACTION),on_delete(CASCADE),match]
       """
    retval = {fk[3].lower(): [fk[2].lower(), fk[4].lower()] for fk in fks}
    cursor.close()
    return retval


def gettablelist(pconn=None):
    """
    list of all tables (except sqlite_system tables starting with sqlite_) from currently open db,
    return list of all tablenames
    """
    cursor = concursor(pconn)
    cursor.execute("""SELECT name
                       FROM sqlite_master
                       WHERE type = 'table' 
                       AND name NOT LIKE'sqlite_%'"""
                   )
    tables = cursor.fetchall()
    retval = [tab[0] for tab in tables]
    return retval


def getcolums(ptablename, pconn=None):
    """
    list of all columns from table ptablename
    return dict of all columns with {colname: (datatype ,"[NOT] NULL")}
    """
    cursor = concursor(pconn)
    cursor.execute("PRAGMA table_info ({})".format(ptablename))
    cols = cursor.fetchall()
    colsinfo = {col[1]: (col[2], ("NOT " if col[3] == 1 else "") + "NULL") for col in cols}
    return colsinfo
