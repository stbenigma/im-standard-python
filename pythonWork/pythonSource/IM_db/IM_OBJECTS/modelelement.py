from datetime import date
from .baseobject import Baseobject, Boolean

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
    DIAG: str = 'DIAG'

    _tablename: str = 'modelelem_type'
    _prefix: str = 'melt'
    _columnlist: list = ['melt_id', 'melt_shortname', 'melt_name',
                         'melt_uc', 'melt_dc', 'melt_um',
                         'melt_dm']

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
                                , 'INTF', 'ORGU', 'RELA', 'SYNO', 'TABL','DOCU','KEYS','DATY'
                                ,'DGRM','DIAG') ) ,
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

    def getname(self,plang=None):
        return self.melt_name

    @staticmethod
    def fillmelt():
        # melt_shortname,  melt_name    ,melt_uc,  melt_dc
        Modelelemtype(pshortname=Modelelemtype.ARCS, pname='Arc').insert()
        Modelelemtype(pshortname=Modelelemtype.ATTR, pname='Attribute').insert()
        Modelelemtype(pshortname=Modelelemtype.BURU, pname='Business Rule').insert()
        Modelelemtype(pshortname=Modelelemtype.COLU, pname='Column').insert()
        Modelelemtype(pshortname=Modelelemtype.DOMA, pname='Domain').insert()
        Modelelemtype(pshortname=Modelelemtype.ENTI, pname='Entity').insert()
        Modelelemtype(pshortname=Modelelemtype.INTF, pname='Interface').insert()
        Modelelemtype(pshortname=Modelelemtype.ORGU, pname='Organizational Unit').insert()
        Modelelemtype(pshortname=Modelelemtype.RELA, pname='Relation').insert()
        Modelelemtype(pshortname=Modelelemtype.SYNO, pname='Synonym').insert()
        Modelelemtype(pshortname=Modelelemtype.TABL, pname='Table').insert()
        Modelelemtype(pshortname=Modelelemtype.DATY, pname='Datatyope').insert()
        Modelelemtype(pshortname=Modelelemtype.KEYS, pname='Key').insert()
        Modelelemtype(pshortname=Modelelemtype.DOCU, pname='Document').insert()
        Modelelemtype(pshortname=Modelelemtype.DGRM, pname='Domaingroupmember').insert()
        Modelelemtype(pshortname=Modelelemtype.DIAG, pname='Diagram').insert()

    @staticmethod
    def getidbyshortname(pshortname):
        melt = Modelelemtype.select(pwhere="melt_shortname= '{}'".format(pshortname))
        if melt is None or (len(melt)==0): return None
        return melt[0].melt_id

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
                            , 'INTF', 'ORGU', 'RELA', 'SYNO', 'TABL','DOCU','KEYS','DATY','DGRM','DIAG') ) ,
     MODE_MELT_ID integer NOT NULL
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
    def getmodebyextref(psrcname, psrcid):
        modeid = Externalref.getmodeid(psrcname=psrcname, psrcid=psrcid)
        return None if modeid is None else Modelelement().getbyid(pid=modeid)

    @staticmethod
    def getmodebyodmguid(psrcid):
        return Modelelement.getmodebyextref(psrcname=Externalref.SOURCE_ODM,psrcid=psrcid)

    def getmyelement(self):
        if self.mode_type == Modelelemtype.SYNO:
            element = Synonym().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.DOMA:
            element = Domain().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.ATTR:
            element = Attribute().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.BURU:
            element = Buseinssrule().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.RELA:
            element = Relation().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.ENTI:
            element = Entity().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.ORGU:
            element = Organisationseinheit().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.TABL:
            element = Tabelle().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.COLU:
            element = Schnittstelleattr().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.INTF:
            element = Schnittstelle().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.ARCS:
            element = Arc().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.DGRM:
            element = DefaultGroupMember().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.DATY:
            element = Datatype().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.DIAG:
            element = Diagram().getbyid(self.mode_id)
        else:
            element = None
        return element

    @staticmethod
    def getelement(pmodeid):
        mode = Modelelement().getbyid(pid=pmodeid)
        return None if mode is None else mode.getmyelement()


    @staticmethod
    def getelementbyextref(psrcname, psrcid):
        return Modelelement.getelement(pmodeid=Externalref.getmodeid(psrcname=psrcname, psrcid=psrcid))

    @staticmethod
    def getelementbyodmguid(psrcid):
        return Modelelement.getelementbyextref(psrcname=Externalref.SOURCE_ODM, psrcid=psrcid)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Modelelement, pwhere=pwhere, porderby=porderby)
# modelelement

class ModelelementProperty(Baseobject):
    _tablename: str = 'modelemtype_properties'
    _prefix: str = 'metp'
    _columnlist: list = ['metp_id','metp_melt_id','metp_udpr_id','metp_optional']

    def __init__(self, pmeltid,pudprid):
        super().__init__(tablename=ModelelementProperty._tablename, prefix=ModelelementProperty._prefix
                         , columnlist=ModelelementProperty._columnlist)
        self.metp_melt_id = pmeltid
        self.metp_udpr_id = pudprid
        self.metp_optional = Boolean.FALSE

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=ModelelementProperty._tablename
                               , psql="""
CREATE TABLE MODELEMTYPE_PROPERTIES
    (
     METP_ID INTEGER NOT NULL primary key autoincrement,
     METP_MELT_ID integer NOT NULL ,
     METP_UDPR_ID integer NOT NULL ,
     METP_OPTIONAL VARCHAR (5) NOT NULL CHECK ( METP_OPTIONAL IN ('FALSE', 'TRUE') )
    ,CONSTRAINT METP_UN UNIQUE (METP_MELT_ID ASC, METP_UDPR_ID ASC)
    ,CONSTRAINT METP_MELT_FK FOREIGN KEY    (     METP_MELT_ID)
		REFERENCES MODELELEM_TYPE    (     MELT_ID )
    ,CONSTRAINT METP_UDPR_FK FOREIGN KEY    (     METP_UDPR_ID)
		REFERENCES USER_DEFINED_PROPERTIES    (     UDPR_ID )
    )
""")

    @staticmethod
    def delete():
        Baseobject.delete(ModelelementProperty._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=ModelelementProperty, pwhere=pwhere, porderby=porderby)

#ModelelementProperty
from .externalref import Externalref
from .datatype import Datatype
from .domain import Domain
from .entity import Entity
from .tabelle import Tabelle
from .attribute import Attribute
from .schnittstattr import Schnittstelleattr
from .schnittstelle import Schnittstelle
