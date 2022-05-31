import re

from SSOT_db.SQL_INFRA import dbDML
from .baseobject import Baseobject
from .modelelement import Modelelemtype,Modelelement


class Datatype(Baseobject):
    BINARY: str = 'BINARY'
    STRING: str = 'STRING'
    DATETIME: str = 'DATETIME'
    NUMERIC: str = 'NUMERIC'
    _tablename: str = 'datatypes'
    _prefix: str = 'daty'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.DATY
    _columnlist: list = []
    __srcname = None
    __srcid = None

    def __init__(self, pname=None, pbasetype=None, psrcname=None, pscrid=None):

        super().__init__(pscrid=pscrid
                         , psrcname=psrcname)
        self.daty_name = pname
        self.daty_basetype = pbasetype
        return

    @staticmethod
    def baseType(dt):
        if (dt in ('BLOB', 'RAW, size', 'BFIE', 'BINARY_DOUBLE', 'BINARY_DOUBLE', 'CLOB',
                   'LONG', 'LONG RAW', 'NCLOB', '')):
            return Datatype.BINARY
        elif (dt in ('DATE', 'TIMESTAMP') or (re.match('INTERVAL.*', dt, flags=re.IGNORECASE)) \
              or re.match('TIMESTAMP.*', dt, flags=re.IGNORECASE)):
            return Datatype.DATETIME
        elif (re.match('NUMBER.*', dt) or re.match('.*INT.*', dt) or re.match('FLOAT.*', dt) \
              or re.match('.*REAL.*', dt)):
            return Datatype.NUMERIC
        else:
            return Datatype.STRING

    # baseType

    @staticmethod
    def deleteunused():
        #deleting modelelements cascades to datatypes
        sql = f"""delete from modelelement
                where mode_type = "{Modelelemtype.DATY}"
                and mode_id not in (select doma_daty_id from DOMAINs where doma_daty_id is not null
                                      )"""
        dbDML.exec(psql=sql)

    @classmethod
    def getbyname(cls, pname):
        return cls.getbyuk(daty_name=pname)

    @classmethod
    def getunknown(cls):
        return cls.getbyname(pname='unknown')
# Datatype
