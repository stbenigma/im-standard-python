import sqlite3

from IM_STANDARD.SQL.SQL_INFRA import DbDDL,SqliteDb,dict_factory

class DbDML(DbDDL):
    def __init__(self,sqlitedb:SqliteDb):
        super().__init__(sqlitedb=sqlitedb)
        return

    @staticmethod
    def dictgroup(keycolname:str,valcolname:str=None,
                  subdict:dict=None,
                  sublist:list=None)->str:
        """
        creates a select part selecting a json dictionary in a groupconcat
        to be used in a subselect
        group_concat('''' ||lang_iso_code2||''':''' ||lgtx_text||'''',',')
        param: keycolname name of the column for the key
        param: valcolname name of the column for the value
        param: subddict dictionary for the value
        param: sublist list for the value
        :return: string to be used in subselect
                """
        if valcolname is not None:
#            retval= f"""group_concat('"' ||{keycolname} ||'":"' || REPLACE(REPLACE({valcolname}, '\', '\\'), '"', '\"') || '"',',')"""
            retval= f"json_group_object({keycolname},{valcolname})"
        elif subdict is not None:
            retval = f"""group_concat('"' ||{keycolname} ||'":"' || {subdict}||'"',',')"""
        elif sublist is not None:
            retval = f"""group_concat('"' ||{keycolname} ||'":"' || {sublist}||'"',',')"""
        else:
            assert False,"value, dict or list must be provided"
        return retval

    @staticmethod
    def listgroup(colname:str)->str:
        """
        creates a select part selecting a json-list in a groupconcat
        to be used in a subselect
        group_concat('''' ||lang_iso_code2||'''',',')
        :return: string to be used in subselect
                """
        #return f"""group_concat('"' || REPLACE(REPLACE({colname}, '\', '\\'), '"', '\"') ||  '"', ',')"""
        return f"json_group_array({colname})"

    def writedbtofile(self, filepath):
        """
        makes a backup of the open database to a file
        :param filepath: filenpath to write the database to

        """
        self.sqlitedb.writedbtofile(filepath=filepath)
        return

    def execsql(self,
             sql: str,
            **kwargs
             ):
        """execute a sql statement with a commit  returning the number of affected rows
          kwargs is the set of substitution variables ":x" in the sql statement
        """

        cursor = self.getcursor(factory=dict_factory)
        try:
            rows = cursor.execute(sql, kwargs).rowcount
        except sqlite3.Error as e:
            raise sqlite3.Error(f"{e.__class__} '{e.args}' when executing statement '{sql}' with args {kwargs}.")
        self.sqlitedb.connection.commit()
        return rows

    def select(self,
               sql: str,
               aslist=False,
               **kwargs):
        """execute a sql select statement
        kwargs is the dict of substitution variables :x in the sql statement
        returns the resultset of the sql statement

        """
        cursor = self.getcursor(factory=None if aslist else dict_factory)

        try:
            cursor.execute(sql, kwargs)
        except sqlite3.Error as e:
            raise Exception(f'Statement failed "{sql}"'+
                            f'\n{e.args}') from e
        result = cursor.fetchall()
        return result


    def lookuprow(self, tablename: str,
                    **kwargs):
        """
        reads a row with a  where-condition
        :param tablename table to read
        :param kwargs: list of column-value pairs combined to col=val AND ... as a where clause
        return: databaserow for the where condition
        raises TOO_MANY VALUES exception, if more than one row is found
        raises NOT_FOUND exception returns None if nothing found
        """

        sql = f"""select * from {tablename}              
              where {' and '.join(f"({k} is :{k})"  for k in kwargs.keys())} 
             """
        rows= self.select(sql=sql,**kwargs)
        if len(rows)==0:
            raise SqliteDb.NO_DATA_FOUND(f"{tablename} for {kwargs} ")
        if len(rows)>1:
            raise SqliteDb.TOO_MANY_ROWS(f"{tablename} for {kwargs} ")
        return rows[0]

    def lookupvalue(self, tablename: str,
                    colname:str,
                    **kwargs):
        """
        reads a value with a  where-condition
        :param tablename table to read
        :param colname name of column to return
        :param kwargs: list of column-value pairs combined to col=val AND ... as a where clause
        return: databasevalue of value
        raises TOO_MANY VALUES exception, if more than one row is found
        raises NOT_FOUND exception returns None if nothing found
        """

        return self.lookuprow(tablename=tablename,**kwargs)[colname]

    def rowinsert(self, tablename: str,
                  **kwargs):
        """ inserts a list of columns (kwargs as key value pairs) as one row into the table
        the keys are the column names to be inserted
        returns the (probably system generated) id of the inserted row
        """
        sql = f"""insert into {tablename}
              ({','.join(kwargs.keys())})
              values({','.join(":" + k for k in kwargs.keys())}) 
             """
        lastid = self.insert(sql=sql,
                            rec=kwargs)
        return lastid

    def insert(self,
               sql: str,
               rec):
        """inserts data
        if rec is a list, insert many tuples with the values from each list element
            if listelement is tupel: use ? in VALUES list
            if listelement is dict: use :name in VALUES list
        if rec is a tuple insert one row, rec elements used for sql-substitution "?"
        if rec is a dict insert one row, rec elements in VALUES with :name
        return:
            number of inserted rows if rec is a list
            id of inserted row if rec is tuple or dict
        """
        cursor = self.getcursor(factory=dict_factory)

        try:
            if type(rec) is list:
                cursor.executemany(sql, rec)
                retval=cursor.rowcount
            elif type(rec) in (tuple, dict):
                cursor.execute(sql, rec)
                retval = cursor.lastrowid
            else:
                assert False, f"unknown type for insert {type(rec)}"

        except sqlite3.IntegrityError as ei:
            # Unique und FK kann für Indexweiterzählen gebraucht werden. Darum keine Fehlermeldung
            if str(ei).startswith("UNIQUE constraint failed"):
                raise SqliteDb.UK_VIOLATED(str(ei))
            if str(ei).startswith("FOREIGN KEY constraint failed"):
                raise SqliteDb.FK_VIOLATED(str(ei))
            if str(ei).startswith("CHECK constraint failed"):
                raise SqliteDb.CHECK_VIOLATED(str(ei))

            raise ei
        except sqlite3.Error as e:
            raise e
        self.sqlitedb.connection.commit()
        return retval

    def rowcount(self,
                 tablename: str) -> int:
        """get the number of rows in the table
        """
        retval = self.select(sql=f"select count(*) as cnt from {tablename}")[0]["cnt"]
        return retval
