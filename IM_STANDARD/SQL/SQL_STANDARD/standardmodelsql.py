import json
import re

from IM_STANDARD.JSON.jsonvalidation import ImStandardGithub
from IM_STANDARD.SQL.SQL_INFRA import DbDML, SqliteDb


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
        ececutes the sql-schema definition for IM-Standard-SQL database in the open database sqlitedb
        the sqlfile is read from the gitHub repository containing the model-model definition
        :return:
        """
        sql = ImStandardGithub.getsqlschema()
        self.execscript(sql=sql)
        return


class StandardModelSql(DbDML):
    """
        interface the Sqlite database of he information model
        - mapping check-constratins values
        - handling json selects
        - handling of specific im-model selects
    """
    ##### Mapping of codes
    # fk columns to link detail tables to their parent
    # used for geneirc reading of lists of details in a master table select.
    FKCOLS = {"synonyms": "syno_enti_id",
              "examples": "expl_mode_id",
              "user_defined_props": "udpv_mode_id",
              "lov_values": "lovv_doma_id"
              }

    # mapping of database LOV-codes to a readable version
    DOMATYPES = {"TXT": "TextDomain",
                 "GRP": "GroupDomain",
                 "LOV": "LOVDomain",
                 "NUM": "NumericDomain",
                 "DAT": "DatetimeDomain",
                 "BIN": "BinaryDomain",
                 "BOO": "BooleanDomain"
                 }
    DOMATYPESREV = {val: key for key, val in DOMATYPES.items()}

    BURUTYPES = {'CALC': 'calculation',
                 'CHECK': 'check',
                 'TRIGGER': 'trigger'
                 }
    BURULEVEL = {'ATTR': 'attribute',
                 'DB': 'database',
                 'ENTI': 'entity',
                 'TUPL': 'tuple'
                 }

    RELATYPES = {'1:1': "1:1",
                 'M:1': 'M:1',
                 'M:N': 'M:N',
                 'ROLE': 'role',
                 'SUBTYPE': 'subtype'
                 }

    ##### General methods for sql-json handling
    @staticmethod
    def _str2json(values: list):
        """
            changes all str entries, enclosed in [] or {} in json elements
        :return: directly in values
        """
        for entry in values:
            removelist = []
            for key, val in entry.items():
                if val is None:
                    removelist.append(key)
                if isinstance(val, str) and re.match("^{[^}]*}|\[[^]]*]$", val):
                    entry[key] = json.loads(val, strict=False)
                if isinstance(val, str) and val in ('TRUE', 'FALSE'):
                    entry[key] = val == 'TRUE'
            for key in removelist:
                del entry[key]

    @staticmethod
    def _sqlvalue(val):
        """
        adds '' to a value for a select statement
        if it is string
        :param val:
        :return: 'val'
        """
        return "'" + val + "'"

    @staticmethod
    def _listsql(tablename: str,
                 colname: str,
                 idcol: str) -> str:
        return f"""(select {DbDML.listgroup(colname=colname)}  
               from {tablename}
                where {StandardModelSql.FKCOLS[tablename]}={idcol})"""

    @staticmethod
    def _mapstring(col: str, mapping: dict) -> str:
        """
        retruns a sql expression mapping a columnvalue to any of the values in the list
        :param: col
        :param mapping:
        :return: case col when x then y end
        """
        maplist = ' '.join(
            [f" when {StandardModelSql._sqlvalue(key)} then {StandardModelSql._sqlvalue(val)}" for key, val in
             mapping.items()])
        return f"""case {col} {maplist} end"""

    @staticmethod
    def _withprefix(val, prefix: str):
        """
        add prefix, if val is not None, else return None
        :param val:
        :param prefix:
        :return:
        """
        return None if val is None else (prefix + str(val))

    @staticmethod
    def _dictgroup(keycolname: str, valcolname: str):
        return DbDML.dictgroup(keycolname=keycolname,
                               valcolname=valcolname)

    @staticmethod
    def _dictsql(tablename: str,
                 keycolname: str,
                 valcolname: str,
                 idcol: str) -> str:
        return f"""(select {StandardModelSql._dictgroup(keycolname=keycolname,
                                            valcolname=valcolname)} 
               from {tablename}
                where {StandardModelSql.FKCOLS[tablename]}={idcol})"""

    #### Special selects for im- model specific elements
    @staticmethod
    def _langtextsql(colname: str,
                     fkname: str,
                     keycolname: str = "lang_iso_code2",
                     valcolname: str = "lgtx_text"):
        """ return select for language text subquery
        select select '{'||group_concat('''' ||lang_iso_code2||''':''' ||lgtx_text||'''',',') ||'}'as enti_name
               from lang_texts
               join languages on lgtx_lang_id = lang_id

        """
        defaultsql = f"""(select  {StandardModelSql._dictgroup(keycolname=keycolname,
                                                   valcolname='defaultvalue')}
                    from translatedvalues
                   where lgtx_attrname='{colname}'  
                   and lgtx_mode_id={fkname})"""

        #without view usage
        # realsql = f"""(select {self._dictgroup(keycolname=keycolname,
        #                                        valcolname=valcolname)}
        #        from lang_texts
        #        join languages on lgtx_lang_id = lang_id
        #            where lgtx_attrname='{colname}'
        #            and lgtx_mode_id={fkname})
        #            """

        return defaultsql

    @staticmethod
    def _langssql():
        """
         :return: subselect for list of lang_iso_code2 in model_languages
        """
        return f"""(select {DbDML.listgroup(colname="lang_iso_code2")}  
               from languages
               join model_languages on mola_lang_id=lang_id               
                where mola_modl_id=modl_id)"""

    @staticmethod
    def _additionalpropssql(idcol: str) -> str:
        return StandardModelSql._dictsql(tablename="user_defined_props",
                             keycolname="udpv_name",
                             valcolname="udpv_value",
                             idcol=idcol)
