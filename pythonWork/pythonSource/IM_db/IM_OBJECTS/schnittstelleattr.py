from IM_OBJECTS import baseobject

class Schnittstelleattr(baseobject.Baseobject):

    def __init__(self):
        super().__init__(tablename='schnittstelle_attr', prefix='scha'
                        ,columnlist = ['scha_id', 'scha_column_name', 'scha_format', 'scha_fremdsystem_id'
                                       ,'scha_beschr', 'scha_tabl_id', 'scha_daty_id', 'scha_odm_guid'
                                       ,'scha_uc', 'scha_dc', 'scha_um', 'scha_dm'])

    def createtable(self):
        super().createtable("""
    create table schnittstelle_attr
    (
        scha_id             integer
            primary key autoincrement,
        scha_column_name    varchar(60) not null
            constraint scha_un
                unique,
        scha_format         varchar(200),
        scha_fremdsystem_id varchar(100),
        scha_beschr         varchar(4000),
        scha_tabl_id        integer     not null
            constraint scha_tabl_fk
                references tabelle,
        scha_daty_id        integer     not null
            constraint scha_daty_fk
                references datatypes (daty_id),
        scha_odm_guid       varchar(36),
        scha_uc             varchar(30) not null,
        scha_dc             varchar(30) not null,
        scha_um             varchar(30),
        scha_dm             varchar(30)
        )
        """)

#Schnittstelleattr
def indexlist():
    schas = Schnittstelleattr().select(porderby='scha_name')
    indexlist = [[s.scha_name, '', s.anker(), s.scha_id] for s in schas]
    return indexlist
# indexlist


