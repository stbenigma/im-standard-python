from .baseobject import Baseobject

class Diagramm(Baseobject):
    _tablename:str = 'diagramme'
    _prefix:str = 'diag'
    _columnlist:list = ['diag_id', 'diag_name', 'diag_diat_id'
                    ,'diag_odm_guid', 'diag_legendx', 'diag_legendy'
                    ,'diag_uc', 'diag_dc', 'diag_um'
                    ,'diag_dm']
    __unknowndaty = None


    def __init__(self):
        super().__init__(tablename= Diagramm._tablename, prefix= Diagramm._prefix
                         , columnlist = Diagramm._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Diagramm._tablename
                                ,psql="""
CREATE TABLE diagramme(
    diag_id      integer primary key autoincrement,
    diag_name      varchar(60) NOT NULL,
    diag_diat_id   integer NOT NULL,
    diag_odm_guid       varchar(36),
    diag_legendx       integer,
    diag_legendy       integer,
     diag_uc    varchar(30) NOT NULL,
    diag_dc        varchar(30) NOT NULL,
    diag_um        varchar(30) ,
    diag_dm        varchar(30),
	CONSTRAINT diag__un UNIQUE(diag_name),
	CONSTRAINT diag_diat_fk FOREIGN KEY(diag_diat_id)
									   REFERENCES diagrammtypen(diat_id)
)	          """)

    @staticmethod
    def delete():
        Baseobject.delete(Diagramm._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Diagramm
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def getbyname(pname):
        return Diagramm().getbyuk(pcolname='diag_name', pukvalue=pname)
    # getbyname

#Diagramm

class Diagrammtyp(Baseobject):
    _tablename:str = 'diagrammtypen'
    _prefix:str = 'diat'
    _columnlist:list = ['diat_id', 'diat_bez'
                    ,'diat_uc', 'diat_dc', 'diat_um'
                    ,'diat_dm']
    __unknowndaty = None


    def __init__(self):
        super().__init__(tablename= Diagrammtyp._tablename, prefix= Diagrammtyp._prefix
                         , columnlist = Diagrammtyp._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Diagrammtyp._tablename
                                ,psql="""
CREATE TABLE diagrammtypen(
    diat_id    integer primary key autoincrement,
    diat_bez   varchar(100) NOT NULL,
     diat_uc varchar(30) NOT NULL,
    diat_dc    varchar(30) NOT NULL,
    diat_um    varchar(30) ,
    diat_dm    varchar(30),
	CONSTRAINT diat_un UNIQUE(diat_bez)
)	          """)

    @staticmethod
    def delete():
        Baseobject.delete(Diagrammtyp._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Diagrammtyp
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def getbyname(pname):
        return Diagrammtyp().getbyuk(pcolname='diat_bez', pukvalue=pname)
    # getbyname

#Diagrammtyp

