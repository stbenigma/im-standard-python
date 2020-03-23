from .baseobject import Baseobject

class Datatype(Baseobject):
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
#Datatype

def indexlist():
        datys = Datatype().select(porderby='daty_name')
        indexlist = [[s.daty_name, '', s.anker(), s.daty_id] for s in datys]
        return indexlist
# indexlist

