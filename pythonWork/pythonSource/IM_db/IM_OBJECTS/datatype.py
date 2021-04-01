from .baseobject import Baseobject
import re
from datetime import date
from .modelelement import Modelelemtype
from IM_DB import dbDML

class Datatype(Baseobject):
    BINARY:str='BINARY'
    STRING:str='STRING'
    DATETIME:str='DATETIME'
    NUMERIC:str='NUMERIC'
    _tablename:str = 'datatypes'
    _prefix:str = 'daty'
    _columnlist:list = []
    __srcname = None
    __srcid = None

    def __init__(self,pname=None,pbasetype=None,psrcname=None,pscrid=None):
        if (len(Datatype._columnlist) == 0): Datatype._columnlist = Baseobject.gettablecolumns(Datatype._tablename)
        super().__init__(pmodelemtype=Modelelemtype.DATY
                        ,pscrid=pscrid
                        ,psrcname=psrcname)
        self.daty_name = pname
        self.daty_basetype = pbasetype
        self.daty_uc = 'fillDB'
        self.daty_dc = date.today()


    @staticmethod
    def baseType(dt):
        if (dt in ('BLOB', 'RAW, size', 'BFIE', 'BINARY_DOUBLE', 'BINARY_DOUBLE', 'CLOB' \
                           , 'LONG', 'LONG RAW', 'NCLOB', '')):
            return Datatype.BINARY
        elif (dt in ('DATE', 'TIMESTAMP') or (re.match('INTERVAL.*', dt,flags=re.IGNORECASE)) or re.match('TIMESTAMP.*', dt,flags=re.IGNORECASE)):
            return Datatype.DATETIME
        elif (re.match('NUMBER.*', dt) or re.match('.*INT.*', dt) or re.match('FLOAT.*', dt) \
              or re.match('.*REAL.*', dt)):
            return Datatype.NUMERIC
        else:
            return Datatype.STRING
    # baseType

    @staticmethod
    def deleteunused():
        sql = """delete from datatypes 
                where daty_id not in (select doma_daty_id from DOMAINs where doma_daty_id is not null
                                      )"""
        dbDML.exec(psql=sql)

    @classmethod
    def getbyname(cls,pname):
        return cls.getbyuk(daty_name=pname)
    # getbyname

    @classmethod
    def getunknown():
        return cls.getbyname(pname='unknown')
#Datatype


