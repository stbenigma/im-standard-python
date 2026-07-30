from IM_STANDARD.SQL.SQL_INFRA import DbDML, SqliteDb
from IM_STANDARD.jsonvalidation import ImStandardGithub


class StandardModelDb(DbDML):
    """
        with a SqliteDb,
        sets up a DbDML connection (db-connection with special functions for the Standard-SQL-MOdel)
    """

    def __init__(self, sqlitedb: SqliteDb, withsqlmodel: bool = True):
        super().__init__(sqlitedb=sqlitedb)

        if withsqlmodel:
            self.createimstandarddb()
        return

    def createimstandarddb(self):
        """
        ececutes the SQL-script for IM-Standard-SQL database in the open database sqlitedb
        :return:
        """
        sql = ImStandardGithub.getsqlschema()
        self.execscript(sql=sql)
        return

