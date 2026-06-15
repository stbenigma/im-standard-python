from pathlib import Path
import sqlite3
from IM_STANDARD.SQL import DbDML

class StandardSqlModel:
    SCHEMADEFPATH = Path(__file__).parent.parent.parent.parent.parent / "Information-model-standard"
    STANDARD_IM_SQLFILE = SCHEMADEFPATH / "Model" / "im-standard-sql" / "im-standard-ddl-sqlite.sql"

    def __init__(self,connection:sqlite3.Connection):
        self.mydb:DbDML = DbDML(connection=connection)
        return

    @staticmethod
    def createimstandarddb(db:DbDML):
        with open(StandardSqlModel.STANDARD_IM_SQLFILE, "r", encoding="utf-8") as sqlfile:
            sql = sqlfile.read()
        db.execscript(sql=sql)
        return


    def getmainlang(self):
        mainlang = self.dmlconn.lookupvalue(tablename="languages",
                                            colname="lang_iso_code2",
                                        lang_is_base_lang='TRUE')
        return mainlang