from .baseobject import Baseobject
import re
from datetime import date
from .modelelement import Modelelemtype
from IM_DB import dbDML

class Datatype(Baseobject):
    BINARY:str='BINARY'
    STRING:str='STRING'
    DATETIME:str='DATETIME'
    NUMERIC:str='NUMERIC'
    _tablename:str = 'datatypes'
    _prefix:str = 'daty'
    _columnlist:list = []
    __srcname = None
    __srcid = None



    def __init__(self,pname=None,pbasetype=None,psrcname=None,pscrid=None):
        if (len(Datatype._columnlist) == 0): Datatype._columnlist = Baseobject.gettablecolumns(Datatype._tablename)
        super().__init__(tablename= Datatype._tablename, prefix= Datatype._prefix
                        ,pmodelemtype=Modelelemtype.DATY
                        ,pscrid=pscrid
                        ,psrcname=psrcname)
        self.daty_name = pname
        self.daty_basetype = pbasetype
        self.daty_uc = 'fillDB'
        self.daty_dc = date.today()


    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Datatype._tablename
                                ,psql="""
	CREATE TABLE DATATYPES 
	    (
	     DATY_ID INTEGER NOT NULL primary key , 
	     DATY_NAME VARCHAR (60) NOT NULL , 
	     DATY_BASETYPE VARCHAR (60) NOT NULL 
	        CONSTRAINT DATY_BASETYPE_CK CHECK ( DATY_BASETYPE IN ('BINARY', 'NUMERIC', 'STRING', 'DATETIME') ) , 
	     DATY_UC VARCHAR (30) , 
	     DATY_DC VARCHAR (30) NOT NULL , 
	     DATY_UM VARCHAR (30) NULL , 
	     DATY_DM VARCHAR (30) NULL 
		 ,CONSTRAINT DATY_MODE_FK FOREIGN KEY (DATY_ID) 
			REFERENCES MODELELEMENT (MODE_ID ) 
			ON DELETE CASCADE 
		)""")

    @staticmethod
    def delete():
        Baseobject.delete(Datatype._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Datatype
                                 , pwhere=pwhere, porderby=porderby)
    @staticmethod
    def baseType(dt):
        if (dt in ('BLOB', 'RAW, size', 'BFIE', 'BINARY_DOUBLE', 'BINARY_DOUBLE', 'CLOB' \
                           , 'LONG', 'LONG RAW', 'NCLOB', '')):
            return Datatype.BINARY
        elif (dt in ('DATE', 'TIMESTAMP') or (re.match('INTERVAL.*', dt,flags=re.IGNORECASE)) or re.match('TIMESTAMP.*', dt,flags=re.IGNORECASE)):
            return Datatype.DATETIME
        elif (re.match('NUMBER.*', dt) or re.match('.*INT.*', dt) or re.match('FLOAT.*', dt) \
              or re.match('.*REAL.*', dt)):
            return Datatype.NUMERIC
        else:
            return Datatype.STRING
    # baseType

    @staticmethod
    def deleteunused():
        sql = """delete from datatypes 
                where daty_id not in (select doma_daty_id from DOMAINs where doma_daty_id is not null
                                        union
                                        select colu_daty_id from columns where colu_daty_id is not null
                                      )"""
        dbDML.exec(psql=sql)

    @staticmethod
    def getbyname(pname):
        return Datatype().getbyuk(pcolname='daty_name', pukvalue=pname)
    # getbyname

    @staticmethod
    def getunknown():
        return Datatype.getbyname(pname='unknown')
#Datatype


