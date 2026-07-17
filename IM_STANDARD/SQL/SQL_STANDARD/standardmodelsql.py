from IM_STANDARD import IMSTANDARDPATH
from IM_STANDARD.SQL import DbDML, SqliteDb


class StandardModelDb(DbDML):
    """
        with a SqliteDb,
        sets up a DbDML connection (db-connection with special functions for the Standard-SQL-MOdel)
    """
    STANDARD_IM_SQLFILE = IMSTANDARDPATH / "Model" / "im-standard-sql" / "im-standard-ddl-sqlite.sql"

    def __init__(self, sqlitedb: SqliteDb, withsqlmodel: bool = True):
        super().__init__(sqlitedb=sqlitedb)

        if withsqlmodel:
            self.createimstandarddb()
        return

    def createimstandarddb(self):
        """
        ececutes the SQL-script for IM-Standard-SQL database in the open database db
        :return:
        """
        with open(self.STANDARD_IM_SQLFILE, "r", encoding="utf-8") as sqlfile:
            sql = sqlfile.read()
        self.execscript(sql=sql)
        return
