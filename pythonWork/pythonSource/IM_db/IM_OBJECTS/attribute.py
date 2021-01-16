from .baseobject import Baseobject, MultilangBaseobject
from .languagetext import Languagetext
from .domain import Domain
from .key import Key
import IM_OBJECTS

class Attribute(MultilangBaseobject):
    _tablename: str = 'attributes'
    _prefix: str = 'attr'
    _columnlist: list = []

    def __init__(self, pname=None, pentiid=None
                    ,psrcname=None, psrcid=None):

        if (len(Attribute._columnlist) == 0): Attribute._columnlist = Baseobject.gettablecolumns(Attribute._tablename)
        super().__init__(tablename=Attribute._tablename, prefix=Attribute._prefix
                         , multilangcols={'attr_displ_name': Languagetext.ATTR_NAME,
                                          'attr_descr': Languagetext.ATTR_COMMENT,
                                          'attr_tooltip': Languagetext.ATTR_TOOLTIP}
                         , pmodelemtype=Modelelemtype.ATTR
                         , pscrid=psrcid
                         , psrcname=psrcname)
        self.attr_displ_name = pname
        self.attr_enti_id = pentiid

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Attribute._tablename
                               , psql="""
CREATE TABLE ATTRIBUTES
    (
     ATTR_ID integer NOT NULL  primary key,
     ATTR_ENTI_ID integer NULL ,
     ATTR_DOMA_ID integer NOT NULL ,
     ATTR_TECH_NAME VARCHAR (60) NOT NULL ,
     ATTR_DISPL_NAME VARCHAR (4000) NULL ,
     ATTR_DISPL_SEQ NUMERIC (5) NULL ,
     ATTR_TOOLTIP VARCHAR (4000) NULL ,
     ATTR_DESCR VARCHAR (4000) NULL ,
     ATTR_IS_DESCRIPTIVE VARCHAR (5) NOT NULL 
   		CHECK(ATTR_IS_DESCRIPTIVE IN('FALSE','TRUE')),
     ATTR_IS_MANDATORY VARCHAR (5) NOT NULL  
   		CHECK(ATTR_IS_MANDATORY IN('FALSE','TRUE')),
     ATTR_IS_HISTORICISED VARCHAR (5) NOT NULL  
   		CHECK(ATTR_IS_HISTORICISED IN('FALSE','TRUE')),
     ATTR_IS_REPEATED VARCHAR (5) NOT NULL  
   		CHECK(ATTR_IS_REPEATED IN('FALSE','TRUE')),
     ATTR_IS_TRANSLATED VARCHAR (5) NOT NULL  
   		CHECK(ATTR_IS_TRANSLATED IN('FALSE','TRUE')),
     ATTR_IS_ENCRYPTED VARCHAR (5) NOT NULL  
   		CHECK(ATTR_IS_ENCRYPTED IN('FALSE','TRUE')),
     ATTR_UC VARCHAR(30) NULL  ,
     ATTR_DC VARCHAR (30) NOT NULL ,
     ATTR_UM VARCHAR (30) NULL ,
     ATTR_DM VARCHAR (30) NULL
      ,CONSTRAINT ATTR_UK UNIQUE (ATTR_TECH_NAME ASC, ATTR_ENTI_ID ASC)
      ,CONSTRAINT ATTR_UK2 UNIQUE (ATTR_DISPL_NAME ASC, ATTR_ENTI_ID ASC)
      ,CONSTRAINT ATTR_ENTI_FK FOREIGN KEY      (     ATTR_ENTI_ID)
		  REFERENCES ENTITIES      (     ENTI_ID )
      ,CONSTRAINT ATTR_MODE_FK FOREIGN KEY      (     ATTR_ID)
		  REFERENCES MODELELEMENT      (     MODE_ID )
		  ON DELETE CASCADE
	  ,CONSTRAINT ATTR_DOMA_FK FOREIGN KEY	  (     ATTR_DOMA_ID)
		  REFERENCES DOMAINS	  (     DOMA_ID )
		  ON DELETE NO ACTION
  )
        """)


    def getname(self, plang=None):
        return self._getsprachval(colname='attr_displ_name', plang=plang)

    def getdescr(self, plang=None):
        return self._getsprachval(colname='attr_descr', plang=plang)

    def gettooltip(self, plang=None):
        return self._getsprachval(colname='attr_tooltip', plang=plang)

    def getentiname(self, plang=None):
        return self.getparent().getname(plang)

    def getmodellelement(self):
        return Modelelement.getbyelemid(pattrid=self.attr_id)

    def getmodeid(self):
        return self.getmodellelement().mode_id

    def getparent(self):
        return IM_OBJECTS.Entity().getbyid(self.attr_enti_id)

    def isinkey(self):
        return Keyelement.isinkey(pattrid=self.attr_id)

    def getdomain(self):
        return Domain().getbyid(self.attr_doma_id)


    def getkeys(self):
        return Key.select(pwhere="""keys_id in 
                                    (select kele_keys_id 
                                    from key_elements 
                                    where kele_attr_id = {})""".format(self.attr_id))
    @staticmethod
    def delete():
        Baseobject.delete(Attribute._tablename)

    @staticmethod
    def select(pwhere=None, porderby="attr_displ_seq"):
        attrs = Baseobject.select(pclass=Attribute
                                  , pwhere=pwhere, porderby=porderby)
        return attrs
    # select
# Attribute
from .modelelement import Modelelement,Modelelemtype
from .key import Keyelement





