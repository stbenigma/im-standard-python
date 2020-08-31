from .baseobject import Baseobject
from .modelelement import Modelelement

class Externalref(Baseobject):
    SOURCE_ODM:str='ODM'
    _tablename:str = 'external_refs'
    _prefix:str = 'extr'
    _columnlist:list = ['extr_id','extr_source_name','extr_source_id','extr_mode_id']


    def __init__(self,psrcname=None,psrcid=None,pmodeid=None):
        super().__init__(tablename= Externalref._tablename, prefix= Externalref._prefix
                         , columnlist = Externalref._columnlist)
        self.extr_source_name = psrcname
        self.extr_source_id = psrcid
        self.extr_mode_id = pmodeid

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Externalref._tablename
                                ,psql="""
CREATE TABLE EXTERNAL_REFS
    (
     EXTR_ID INTEGER NOT NULL primary key autoincrement,
     EXTR_SOURCE_NAME VARCHAR (60) NOT NULL ,
     EXTR_SOURCE_ID VARCHAR (100) NOT NULL ,
     EXTR_MODE_ID NUMERIC (10) NOT NULL
    ,CONSTRAINT EXTR_UK UNIQUE (EXTR_SOURCE_NAME ASC, EXTR_MODE_ID ASC)
     ,CONSTRAINT EXTR_UK_ID UNIQUE (EXTR_SOURCE_NAME ASC, EXTR_SOURCE_ID ASC)
    ,CONSTRAINT EXTR_MODE_FK FOREIGN KEY(     EXTR_MODE_ID) 
        REFERENCES MODELELEMENT(     MODE_ID )
        ON DELETE CASCADE
    )
""")

    @staticmethod
    def delete():
        Baseobject.delete(Externalref._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Externalref
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def getmodeid(psrcname,psrcid):
        extrs = Externalref.select (pwhere="extr_source_name = '{}' and extr_source_id = '{}'".format(psrcname,psrcid))
        modeid = None if length(extr) == 0 else extrs[0].extr_mode_id
        return modeid
    # getmodeid

    @staticmethod
    def getsrcid(psrcname,pmodeid):
        extrs = Externalref.select (pwhere="extr_source_name = '{}' and extr_mode_id = '{}'".format(psrcname,pmodeid))
        srcid = None if length(extr) == 0 else extrs[0].extr_source_id
        return srcid
    # getsrcid


#Externalref

