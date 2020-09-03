from datetime import date
from .baseobject import Baseobject
class Modelelemtype(Baseobject):
    ENTI: str = 'ENTI'
    BURU: str = 'BURU'
    SYNO: str = 'SYNO'
    RELA: str = 'RELA'
    ATTR: str = 'ATTR'
    DOMA: str = 'DOMA'
    ORGU: str = 'ORGU'
    TABL: str = 'TABL'
    INTF: str = 'INTF'
    COLU: str = 'COLU'
    ARCS: str = 'ARCS'
    DOCU: str = 'DOCU'
    KEYS: str = 'KEYS'
    DATY: str = 'DATY'
    DGRM: str = 'DGRM'

    _tablename: str = 'modelelem_type'
    _prefix: str = 'melt'
    _columnlist: list = ['melt_id', 'melt_shortname', 'melt_name',
                         'melt_uc', 'melt_dc', 'melt_um',
                         'melt_dm']
    __meltids: dict = {}

    def __init__(self, pshortname=None, pname=None):
        super().__init__(tablename=Modelelemtype._tablename, prefix=Modelelemtype._prefix
                         , columnlist=Modelelemtype._columnlist)
        self.melt_shortname = pshortname
        self.melt_name = pname
        self.melt_uc = 'SYS'
        self.melt_dc = date.today()

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Modelelemtype._tablename
                               , psql="""
CREATE TABLE MODELELEM_TYPE
    (
     MELT_ID INTEGER NOT NULL primary key autoincrement,
     MELT_SHORTNAME VARCHAR (4) NOT NULL CHECK 
            ( MELT_SHORTNAME IN ('ARCS', 'ATTR', 'BURU', 'COLU', 'DOMA', 'ENTI'
                                , 'INTF', 'ORGU', 'RELA', 'SYNO', 'TABL','DOCU','KEYS','DATY') ) ,
     MELT_NAME VARCHAR (60) NOT NULL ,
     MELT_UC VARCHAR(30) NULL  ,
     MELT_DC VARCHAR (30) NOT NULL ,
     MELT_UM VARCHAR (30) NULL ,
     MELT_DM VARCHAR (30) NULL
    ,CONSTRAINT MELT_UN UNIQUE (MELT_SHORTNAME ASC)
    ,CONSTRAINT MELT_UN2 UNIQUE (MELT_NAME ASC)
) 
""")

    @staticmethod
    def delete():
        Baseobject.delete(Modelelemtype._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Modelelemtype, pwhere=pwhere, porderby=porderby)

    def insert(self):
        meltid = super().insert()
        Modelelemtype.__meltids[self.melt_shortname] = meltid

    @staticmethod
    def fillmelt():
        # melt_shortname,  melt_name    ,melt_uc,  melt_dc
        Modelelemtype(pshortname=Modelelemtype.ARCS, pname='Arc').insert()
        Modelelemtype(pshortname=Modelelemtype.ATTR, pname='Attribut').insert()
        Modelelemtype(pshortname=Modelelemtype.BURU, pname='Business Rule').insert()
        Modelelemtype(pshortname=Modelelemtype.COLU, pname='Column').insert()
        Modelelemtype(pshortname=Modelelemtype.DOMA, pname='Domain').insert()
        Modelelemtype(pshortname=Modelelemtype.ENTI, pname='Entität').insert()
        Modelelemtype(pshortname=Modelelemtype.INTF, pname='Schnittstelle').insert()
        Modelelemtype(pshortname=Modelelemtype.ORGU, pname='Organisationseinheit').insert()
        Modelelemtype(pshortname=Modelelemtype.RELA, pname='Beziehung').insert()
        Modelelemtype(pshortname=Modelelemtype.SYNO, pname='Synonym').insert()
        Modelelemtype(pshortname=Modelelemtype.TABL, pname='Tabelle').insert()
        Modelelemtype(pshortname=Modelelemtype.DATY, pname='Datentyp').insert()
        Modelelemtype(pshortname=Modelelemtype.KEYS, pname='Keys').insert()
        Modelelemtype(pshortname=Modelelemtype.DOCU, pname='Document').insert()

    @staticmethod
    def getidbyshortname(pshortname):
        return Modelelemtype.__meltids[pshortname]

    @staticmethod
    def getshortname(pmeltid):
        return Modelelemtype().getbyid(pid).melt_shortname

    @staticmethod
    def getbyshortname(pshortname):
        return Modelelemtype().getbyid(Modelelemtype.getidbyshortname(pshortname))

    @staticmethod
    def type2melt(type):
        trans = {"Entity": Modelelemtype.ENTI
            , "Attribute": Modelelemtype.ATTR
            , "Relation": Modelelemtype.RELA
            , "Table": Modelelemtype.TABL
            , "Column": Modelelemtype.INTF
            , "Arcs": Modelelemtype.ARCS
            , "FKIndexAssociation": ""
                 }
        return trans[type]
    # type2melt

# Modelelemtype

class Modelelement(Baseobject):
    """Modelelement is a supertype of a lot of entities. It shares common attributes and relationships
        It's ID is identical to id's in subtype tables.
        So Modelelement is created first (with a system generated ID, unique over all subtables). It's ID is then
        used as ID' of the subtables
    """
    _tablename: str = 'modelelement'
    _prefix: str = 'mode'
    _columnlist: list = ['mode_id', 'mode_type', 'mode_melt_id']

    def __init__(self, pmeltshortname=None):
        super().__init__(tablename=Modelelement._tablename, prefix=Modelelement._prefix
                         , columnlist=Modelelement._columnlist)
        self.mode_type = pmeltshortname
        if pmeltshortname is not None: self.mode_melt_id = Modelelemtype.getidbyshortname(pshortname=pmeltshortname)
    # __init__

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Modelelement._tablename
                               , psql="""
CREATE TABLE MODELELEMENT
    (
     MODE_ID INTEGER NOT NULL primary key autoincrement ,
     MODE_TYPE VARCHAR (4) NOT NULL CHECK ( MODE_TYPE IN ('ARCS', 'ATTR', 'BURU', 'COLU', 'DOMA', 'ENTI'
                            , 'INTF', 'ORGU', 'RELA', 'SYNO', 'TABL','DOCU','KEYS','DATY','DGRM') ) ,
     MODE_MELT_ID NUMERIC (10) NOT NULL
     ,CONSTRAINT MODE_MELT_FK FOREIGN KEY     (     MODE_MELT_ID)
        REFERENCES MODELELEM_TYPE(     MELT_ID )
)
""")

    @staticmethod
    def delete(pwhere=''):
        Baseobject.delete(Modelelement._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Modelelement
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def getelementbyextref(psrcname, psrcid):
        return Modelelement.getelement(pmodeid=Externalref.getmodeid(psrcname=psrcname, psrcid=psrcid))

    @staticmethod
    def getelement(pmodeid):
        mode = Modelelement().getbyid(pid=pmodeid)
        if mode.mode_type == Modelelemtype.SYNO:
            element = Synonym().getbyid(mode.mode_id)
        elif mode.mode_type == Modelelemtype.DOMA:
            element = Wertebereich().getbyid(mode.mode_id)
        elif mode.mode_type == Modelelemtype.ATTR:
            element = Attribut().getbyid(mode.mode_id)
        elif mode.mode_type == Modelelemtype.BURU:
            element = Buseinssrule().getbyid(mode.mode_id)
        elif mode.mode_type == Modelelemtype.RELA:
            element = Relation().getbyid(mode.mode_id)
        elif mode.mode_type == Modelelemtype.ENTI:
            element = Entitaet().getbyid(mode.mode_id)
        elif mode.mode_type == Modelelemtype.ORGU:
            element = Organisationseinheit().getbyid(mode.mode_id)
        elif mode.mode_type == Modelelemtype.TABL:
            element = Tabelle().getbyid(mode.mode_id)
        elif mode.mode_type == Modelelemtype.COLU:
            element = Schnittstelleattr().getbyid(mode.mode_id)
        elif mode.mode_type == Modelelemtype.INTF:
            element = Schnittstelle().getbyid(mode.mode_id)
        elif mode.mode_type == Modelelemtype.ARCS:
            element = Arc().getbyid(mode.mode_id)
        elif mode.mode_type == Modelelemtype.DGRM:
            element = DefaultValue().getbyid(mode.mode_id)
        elif mode.mode_type == Modelelemtype.DATY:
            element = Datatype().getbyid(mode.mode_id)
        else:
            element = None
        return element
# modelelement
from .externalref import Externalref
from .datatype import Datatype
