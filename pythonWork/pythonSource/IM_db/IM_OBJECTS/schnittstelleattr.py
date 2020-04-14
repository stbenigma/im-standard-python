from .baseobject import Baseobject

class Schnittstelleattr(Baseobject):

    _tablename:str = 'schnittstelle_attrs'
    _prefix:str = 'scha'
    _columnlist:list = ['scha_id', 'scha_column_name', 'scha_format', 'scha_fremdsystem_id'
                                       ,'scha_beschr', 'scha_tabl_id', 'scha_daty_id', 'scha_odm_guid'
                                       ,'scha_uc', 'scha_dc', 'scha_um', 'scha_dm']

    def __init__(self):
        super().__init__(tablename=Schnittstelleattr._tablename, prefix=Schnittstelleattr._prefix
                        ,columnlist = Schnittstelleattr._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Schnittstelleattr._tablename
                               , psql="""
    create table schnittstelle_attrs
    (
        scha_id             integer
            primary key autoincrement,
        scha_column_name    varchar(60) not null,
        scha_format         varchar(200),
        scha_fremdsystem_id varchar(100),
        scha_beschr         varchar(4000),
        scha_tabl_id        integer     not null,
        scha_daty_id        integer     not null,
        scha_odm_guid       varchar(36),
        scha_uc             varchar(30) not null,
        scha_dc             varchar(30) not null,
        scha_um             varchar(30),
        scha_dm             varchar(30),
        constraint scha_daty_fk FOREIGN KEY (scha_daty_id) references datatypes (daty_id),
        constraint scha_uk unique (scha_tabl_id,scha_column_name)        
        )
        """)

    @staticmethod
    def delete():
        Baseobject.delete(Schnittstelleattr._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Schnittstelleattr
                                 , pwhere=pwhere, porderby=porderby)
#Schnittstelleattr

def indexlist():
    schas = Schnittstelleattr.select(porderby='scha_name')
    indexlist = [[s.scha_name, '', s.anker(), s.scha_id] for s in schas]
    return indexlist
# indexlist


