from IM_OBJECTS import baseobject

class Datatype(baseobject.Baseobject):

    def __init__(self):
        super().__init__(tablename='datatypes', prefix='daty'
                        ,columnlist = ['daty_id',  'daty_name', 'daty_grundtyp', 'daty_odm_guid'])

    def createtable(self):
        super().createtable("""
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
#Datatype

def indexlist():
        datys = Datatype().select(porderby='daty_name')
        indexlist = [[s.daty_name, '', s.anker(), s.daty_id] for s in datys]
        return indexlist
# indexlist

