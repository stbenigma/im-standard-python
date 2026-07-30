import logging
import sqlite3

from IM_STANDARD.SQL.SQL_INFRA.dbConnect import  SqliteDb,dict_factory

class DbDDL():

    """
        a collection of metadata functions for a sqlite-database
    """

    def __init__(self, sqlitedb:SqliteDb):
        self.sqlitedb:SqliteDb= sqlitedb
        return

    def getcursor(self, factory=dict_factory) -> sqlite3.Cursor: #
        """
        get a cursor for my connection
        :param factory: transformation factory to change output of cursor
        :return:
        """
        self.sqlitedb.connection.row_factory = factory
        return self.sqlitedb.connection.cursor()

    def execscript(self, sql):
        """
            execute the sqlstatements in sql-script
        """
        cursor = self.getcursor(factory=dict_factory)
        try:
            cursor.executescript(sql)
            cursor.close()
        except sqlite3.Error as e:
            logging.error(sql)
            print(f"Unexpected SQL-error: \t{e}")
            raise e
        return

    def getuklist(self, tablename):
        """
            List of all uk (list of columns) for the table tablename
            return a list of lists of columnnames [[colname,],]
         """
        cursor = self.getcursor(factory=dict_factory)
        cursor.execute(f"PRAGMA index_list('{tablename}')")
        indices = cursor.fetchall()
        """
            index_list [seq,name,unique ,origin ,partial]
            index_info [seqno,cid,colname]
            foreign_key_list 
            {<ukname>: {id,seq,table,from,to,on_update (NO_ACTION),on_delete(CASCADE),match}}
            """
        retval = []
        for i in indices:
            if i["unique"] == 1 and i["origin"] == 'u':
                # unique key found
                cursor.execute(f"PRAGMA index_info('{i['name']}')")
                cols = cursor.fetchall()
                retval.append({i["name"]: [c["name"] for c in sorted(cols, key=lambda x: x["seqno"])]
                               })
        cursor.close()
        return retval

    def getfklist(self, tablename):
        """List of all foreign keys (with columns) of table tablename
        return {colname:[fktable,fkcolname]} all names in lowercase
        """
        cursor = self.getcursor(factory=dict_factory)
        cursor.execute(f"PRAGMA foreign_key_list('{tablename}')")
        fks = cursor.fetchall()
        cursor.close()
        """
            foreign_key_list [id,
                            seq,
                            table,
                            from,
                            to,
                            on_update (NO_ACTION),
                            on_delete(CASCADE),
                            match]
           """
        fkids =list(set([f["id"]for f in fks]))
        retval = {}
        for fk in fks:
            fkid=fk["id"]
            fromto=sorted([(f["from"],f["to"],f["seq"]) for f in fks if f["id"]==fkid],
                          key=lambda x:x[2])
            retval[f"fk-{str(fk['id'])}"]={"id":fkid,
                            "table":fk["table"],
                            "from":[f[0] for f in fromto],
                            "to":[f[1] for f in fromto],
                            "on_update":fk["on_update"],
                            "on_delete":fk["on_delete"],
                            "match":fk["match"]}

        return retval

    def gettablelist(self):
        """
        list of all tables (except sqlite_system tables starting with sqlite_) from currently open db,
        return list of all tablenames
        """
        cursor = self.getcursor(factory=None)
        cursor.execute("""SELECT name
                           FROM sqlite_master
                           WHERE type = 'table' 
                           AND name NOT LIKE'sqlite_%'"""
                       )
        tables = cursor.fetchall()
        retval = [tab[0] for tab in tables]
        return retval

    def getcolums(self, tablename):
        """
        list of all columns from table tablename
        return dict of all columns with
            {<colname>:
                ("datatype":<type>,
                "mandatory": <boolean>,
                "default":<defvalue>,
                "inpk": boolean
                }
        """
        cursor = self.getcursor(factory=dict_factory)
        cursor.execute(f"PRAGMA table_info ({tablename})")
        cols = cursor.fetchall()
        colsinfo = {col["name"]:
                        {"datatype": col["type"],
                         "mandatory": (col["notnull"] == 1 or col["pk"]!=0),
                         "default": col["dflt_value"],
                         "inpk": col["pk"] != 0
                         }
                    for col in cols}
        return colsinfo
