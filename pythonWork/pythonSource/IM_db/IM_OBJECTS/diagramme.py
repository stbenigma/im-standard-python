from .baseobject import Baseobject
from .modelelement import Modelelemtype
from datetime import date

class Diagram(Baseobject):
    _tablename:str = 'diagrams'
    _prefix:str = 'diag'
    _columnlist:list = ['diag_id', 'diag_name', 'diag_diat_id'
                    , 'diag_legendx', 'diag_legendy'
                    ,'diag_uc', 'diag_dc', 'diag_um'
                    ,'diag_dm']

    def __init__(self, psrcname=None, psrcid=None):
        super().__init__(tablename= Diagram._tablename, prefix= Diagram._prefix
                         , columnlist = Diagram._columnlist
                         , pmodelemtype=Modelelemtype.DIAG
                         , pscrid=psrcid
                         , psrcname=psrcname
                         )

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Diagram._tablename
                                ,psql="""
CREATE TABLE diagrams(
    diag_id      integer primary key autoincrement,
    diag_name      varchar(60) NOT NULL,
    diag_diat_id   integer NOT NULL,
    diag_legendx       integer,
    diag_legendy       integer,
     diag_uc    varchar(30) NOT NULL,
    diag_dc        varchar(30) NOT NULL,
    diag_um        varchar(30) ,
    diag_dm        varchar(30),
	CONSTRAINT diag__un UNIQUE(diag_name),
	CONSTRAINT diag_diat_fk FOREIGN KEY(diag_diat_id)
									   REFERENCES diagramtypes(diat_id)
	,CONSTRAINT DIAGRAMS_MODELELEMENT_FK FOREIGN KEY (DIAG_ID) 
       REFERENCES MODELELEMENT (MODE_ID )ON DELETE CASCADE
)	          """)

    @staticmethod
    def delete():
        Baseobject.delete(Diagram._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Diagram
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def getbyname(pname):
        return Diagram().getbyuk(pcolname='diag_name', pukvalue=pname)
    # getbyname

#Diagram

class Diagramtype(Baseobject):
    _tablename:str = 'diagramtypes'
    _prefix:str = 'diat'
    _columnlist:list = ['diat_id', 'diat_name'
                    ,'diat_uc', 'diat_dc', 'diat_um'
                    ,'diat_dm']


    def __init__(self,pname=None):
        super().__init__(tablename= Diagramtype._tablename, prefix= Diagramtype._prefix
                         , columnlist = Diagramtype._columnlist
                         )
        self.diat_name = pname
        self.diat_uc = 'system'
        self.diat_dc = date.today()

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Diagramtype._tablename
                                ,psql="""
CREATE TABLE diagramtypes(
    diat_id    integer primary key autoincrement,
    diat_name   varchar(100) NOT NULL,
     diat_uc varchar(30) NOT NULL,
    diat_dc    varchar(30) NOT NULL,
    diat_um    varchar(30) ,
    diat_dm    varchar(30),
	CONSTRAINT diat_un UNIQUE(diat_name)
)	          """)

    @staticmethod
    def delete():
        Baseobject.delete(Diagramtype._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Diagramtype
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def getbyname(pname):
        return Diagramtype().getbyuk(pcolname='diat_name', pukvalue=pname)
    # getbyname
#Diagramtype

class MeltDiat(Baseobject):
    _tablename:str = 'melt_diats'
    _prefix:str = 'medi'
    _columnlist:list = ['medi_id', 'medi_diat_id','medi_melt_id'
                    ,'medi_uc', 'medi_dc', 'medi_um'
                    ,'medi_dm']

    def __init__(self,pmeltid=None,pdiatid=None):
        super().__init__(tablename= MeltDiat._tablename, prefix= MeltDiat._prefix
                         , columnlist = MeltDiat._columnlist
                         )
        self.medi_melt_id = pmeltid
        self.medi_diat_id = pdiatid
        self.medi_uc = 'system'
        self.medi_dc = date.today()

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=MeltDiat._tablename
                                ,psql="""
CREATE TABLE melt_diats(
    medi_id        integer primary key autoincrement,
    medi_diat_id   integer NOT NULL,
    medi_melt_id   integer NOT NULL,
    medi_uc    varchar(30) NOT NULL,
    medi_dc        varchar(30) NOT NULL,
    medi_um        varchar(30) ,
    medi_dm        varchar(30),
	CONSTRAINT medi__un UNIQUE(medi_diat_id,
	                                   medi_melt_id),
    CONSTRAINT medi_diat_fk FOREIGN KEY(medi_diat_id)			           
					REFERENCES diagramtypes(diat_id)
								    ON DELETE CASCADE,
	CONSTRAINT modi_melt_fk FOREIGN KEY(medi_melt_id)
		REFERENCES MODELELEM_TYPE(melt_id)
		     ON DELETE CASCADE
)	          """)

    @staticmethod
    def delete():
        Baseobject.delete(MeltDiat._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=MeltDiat
                                 , pwhere=pwhere, porderby=porderby)
#Diagramtype
