from .baseobject import Baseobject
import re

class Datatype(Baseobject):
    BIN:str='BIN'
    TEXT:str='TEXT'
    ZPKT:str='ZPKT'
    NUM:str='NUM'
    _tablename:str = 'datatypes'
    _prefix:str = 'daty'
    _columnlist:list = ['daty_id',  'daty_name', 'daty_grundtyp', 'daty_odm_guid']

    def __init__(self):
        super().__init__(tablename= Datatype._tablename, prefix= Datatype._prefix
                        ,columnlist = Datatype._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Datatype._tablename
                                ,psql="""
create table datatypes
(
    daty_id       integer      not null
        primary key autoincrement,
    daty_name     VARCHAR2(60) not null
        unique,
    daty_grundtyp VARCHAR2(6)  not null,
    daty_odm_guid VARCHAR2(36),
    check (daty_grundtyp IN (
                             'BIN',
                             'NUM',
                             'TEXT',
                             'ZPKT'
        ))
)
""")

    @staticmethod
    def delete():
        Baseobject.delete(Datatype._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Datatype
                                 , pwhere=pwhere, porderby=porderby)
    @staticmethod
    def basisType(dt):
        if (dt in ('BLOB', 'RAW, size', 'BFIE', 'BINARY_DOUBLE', 'BINARY_DOUBLE', 'CLOB' \
                           , 'LONG', 'LONG RAW', 'NCLOB', '')):
            return Datatype.BIN
        elif (dt in ('DATE', 'TIMESTAMP') or (re.match('INTERVAL.*', dt))):
            return Datatype.ZPKT
        elif (re.match('NUMBER.*', dt) or re.match('.*INT.*', dt) or re.match('FLOAT.*', dt) \
              or re.match('.*REAL.*', dt)):
            return Datatype.NUM
        else:
            return Datatype.TEXT
    # basisType
#Datatype


