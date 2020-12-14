from .baseobject import Baseobject
from .modelelement import Modelelemtype

class Key(Baseobject):
    _tablename: str = 'keys'
    _prefix: str = 'keys'
    _columnlist: list = []

    def __init__(self, psrcname=None, psrcid=None):
        if (len(Key._columnlist) == 0): Key._columnlist = Baseobject.gettablecolumns(Key._tablename)
        super().__init__(tablename=Key._tablename, prefix=Key._prefix
                         , pmodelemtype=Modelelemtype.KEYS
                         , psrcname=psrcname
                         , pscrid=psrcid)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Key._tablename
                               , psql="""
CREATE TABLE KEYS
    (
     KEYS_ID INTEGER NOT NULL primary key autoincrement,
     KEYS_NAME VARCHAR (60) NOT NULL ,
     KEYS_ENTI_ID integer NOT NULL ,
     KEYS_UC VARCHAR(30) NOT NULL  ,
     KEYS_DC VARCHAR (30) NOT NULL ,
     KEYS_UM VARCHAR (30) NULL ,
     KEYS_DM VARCHAR (30) NULL
    ,CONSTRAINT KEYS_UK UNIQUE (KEYS_ENTI_ID ASC, KEYS_NAME ASC)
    ,CONSTRAINT KEYS_ENTI_FK FOREIGN KEY    (     KEYS_ENTI_ID)
            REFERENCES ENTITIES(     ENTI_ID ) ON DELETE CASCADE 
    )
""")

    def getkeyelements(self,ptype=None):
        if ptype == Modelelemtype.RELA:
            which = ' and kele_rela_id is not null'
        elif ptype == Modelelemtype.ATTR:
            which = ' and kele_attr_id is not null'
        else:
            which = ''
        #fi
        return  Keyelement.select(pwhere='kele_keys_id = {}{}'.format(self.getid(),which))

    @staticmethod
    def delete():
        Baseobject.delete(Key._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Key, pwhere=pwhere, porderby=porderby)
# Key

class Keyelement(Baseobject):
    _tablename: str = 'key_elements'
    _prefix: str = 'kele'
    _columnlist: list = []

    def __init__(self):
        if (len(Keyelement._columnlist) == 0): Keyelement._columnlist = Baseobject.gettablecolumns(Keyelement._tablename)
        super().__init__(tablename=Keyelement._tablename, prefix=Keyelement._prefix)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Keyelement._tablename
                               , psql="""
CREATE TABLE KEY_ELEMENTS
    (
     KELE_ID INTEGER NOT NULL primary key autoincrement,
     KELE_KEYS_ID integer NOT NULL ,
     KELE_ATTR_ID integer NULL ,
     KELE_RELA_ID integer NULL ,
     KELE_UC VARCHAR(30) NOT NULL  ,
     KELE_DC VARCHAR (30) NOT NULL ,
     KELE_UM VARCHAR (30) NULL ,
     KELE_DM VARCHAR (30) NULL
,CONSTRAINT FKArc_8 CHECK 
		(( (KELE_RELA_ID IS NOT NULL) AND
		   (KELE_ATTR_ID IS NULL) 
	     ) OR (  (KELE_ATTR_ID IS NOT NULL) AND
                 (KELE_RELA_ID IS NULL) ) 
		 )
	    ,CONSTRAINT KELE_ATTR_FK FOREIGN KEY (     KELE_ATTR_ID)
			 REFERENCES ATTRIBUTES  (     ATTR_ID )
			 ON DELETE CASCADE
	     ,CONSTRAINT KELE_KEYS_FK FOREIGN KEY	     (     KELE_KEYS_ID)
			 REFERENCES KEYS	     (     KEYS_ID )
			 ON DELETE CASCADE
	     ,CONSTRAINT KELE_RELA_FK FOREIGN KEY	     (     KELE_RELA_ID)
			 REFERENCES RELATIONS	     (     RELA_ID )
			 ON DELETE CASCADE
      ,CONSTRAINT KELE_UN UNIQUE (KELE_KEYS_ID ASC, KELE_ATTR_ID ASC, KELE_RELA_ID ASC)
)
""")

    @staticmethod
    def isinkey(pattrid=None, prelaid=None) -> bool:
        if pattrid is not None:
            return len(Keyelement.select(pwhere="kele_attr_id = {}".format(pattrid))) > 0
        if prelaid is not None:
            return len(Keyelement.select(pwhere="kele_rela_id = {}".format(prelaid))) > 0
        return False

    # isinkey

    def getkeyelement(self):
        if self.kele_attr_id is not None:
            return Attribute().getbyid(self.kele_attr_id)
        if self.kele_rela_id is not None:
            return Relation().getbyid(self.kele_rela_id)

    # getkeyelement

    @staticmethod
    def delete():
        Baseobject.delete(Keyelement._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Keyelement, pwhere=pwhere, porderby=porderby)
    # Keyelement
from .attribute import Attribute
from .relationship import Relation
