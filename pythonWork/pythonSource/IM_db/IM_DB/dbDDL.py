# -*- coding: latin-1 -*-

from IM_DB import dbConnect
import sqlite3
import re

def createTable(psql,pconn=None):
    conn = pconn if pconn is not None else dbConnect.myDbConn
    cursor = conn.cursor()
    try:
        cursor.execute(psql)
    except sqlite3.Error as e:
        if re.match("table .* already exists", e.__str__()):
            pass
        else:
            print("Unerwarteter SQL-Fehler: \t{}".format(e))
            raise e
    return


# end createTable

def dropTable(ptableName,pconn=None):
    conn = pconn if pconn is not None else dbConnect.myDbConn
    cursor = conn.cursor()

    try:
        cursor.execute("drop table " + ptableName + ";")
    except sqlite3.Error as e:
        if re.match("no such table:.* ", e.__str__()):
            pass
        else:
            print("Unerwarteter SQL-Fehler: \t{}".format(e))
            raise e
    return

def dropView(ptableName,pconn=None):
    conn = pconn if pconn is not None else dbConnect.myDbConn
    cursor = conn.cursor()
    try:
        cursor.execute("drop view " + ptableName + ";")
    except sqlite3.Error as e:
        if re.match("no such view:.* ", e.__str__()):
            pass
        else:
            print("Unerwarteter SQL-Fehler: \t{}".format(e))
            raise e
    return

# end dropView

def execscript(psql,pconn=None):
    conn = pconn if pconn is not None else dbConnect.myDbConn
    cursor = conn.cursor()
    try:
        cursor.executescript(psql)
    except sqlite3.Error as e:
        if re.match("xxxxxxx", e.__str__()):
            pass
        else:
            print(psql)
            print("exec: unexpected SQL-error: \t%s" % e)
            raise e
    conn.commit()
# end executescript

def getsoleukcolname(ptablename,pconn=None):
    uks = getuklist(ptablename,pconn=pconn)
    if len(uks)== 1 and len(uks[0])==1:
        return uks[0][0]
    else:
        return None

def getuklist(ptablename,pconn=None):
    """List of all uk (list of columns) for this table  [[colname,],]"""
    conn = pconn if pconn is not None else dbConnect.myDbConn
    cursor = conn.cursor()
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
        #fi
    #for
    cursor.close()
    return retval

def getfklist(ptablename,pconn=None):
    """return {colname:[fktable,fkcolname]} all names in lowercase"""
    conn = pconn if pconn is not None else dbConnect.myDbConn
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_key_list('{}')".format(ptablename))
    fks = cursor.fetchall()
    """foreign_key_list [id,seq,table,from,to,on_update (NO_ACTION),on_delete(CASCADE),match]
       """
    retval = {fk[3].lower(): [fk[2].lower(), fk[4].lower()] for fk in fks}
    cursor.close()
    return retval


def gettablelist(pconn=None):
    """from currently open db, return list of all tables
    """
    conn = pconn if pconn is not None else dbConnect.myDbConn
    cursor = conn.cursor()
    cursor.execute("""SELECT name
                       FROM sqlite_master
                       WHERE type = 'table' 
                       AND name NOT LIKE'sqlite_%'"""
                   )
    tables = cursor.fetchall()
    retval = [tab[0] for tab in tables]
    return retval

def getcolums(ptablename,pconn=None):
    conn = pconn if pconn is not None else dbConnect.myDbConn
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info ({})".format(ptablename))
    cols = cursor.fetchall()
    colsinfo = {col[1]:(col[2],("NOT " if col[3]==1 else "") + "NULL") for col in cols}
    return colsinfo
