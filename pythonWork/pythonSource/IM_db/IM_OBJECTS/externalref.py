from .baseobject import Baseobject
from IM_DB import  dbDML

class Externalref(Baseobject):
    SOURCE_ODM:str='ODM'
    _tablename:str = 'external_refs'
    _prefix:str = 'extr'
    _columnlist:list = []


    def __init__(self,psrcname=None,psrcid=None,pmodeid=None):
        if (len(Externalref._columnlist) == 0): Externalref._columnlist = Baseobject.gettablecolumns(Externalref._tablename)
        super().__init__(tablename= Externalref._tablename, prefix= Externalref._prefix)
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
     EXTR_MODE_ID integer NOT NULL
    ,CONSTRAINT EXTR_UK UNIQUE (EXTR_SOURCE_NAME ASC, EXTR_MODE_ID ASC)
     ,CONSTRAINT EXTR_UK_ID UNIQUE (EXTR_SOURCE_NAME ASC, EXTR_SOURCE_ID ASC)
    ,CONSTRAINT EXTR_MODE_FK FOREIGN KEY(     EXTR_MODE_ID) 
        REFERENCES MODELELEMENT(     MODE_ID )
        ON DELETE CASCADE
    )
""")

    @staticmethod
    def getsources():
        data = dbDML.select("""select distinct extr_source_name from external_refs order by extr_source_name""")
        return [d[0] for d in data]

    @staticmethod
    def getsrcinfo(pmodeid):
        extrs = Externalref.select (pwhere="extr_mode_id = '{}'".format(pmodeid)
                                    ,porderby="extr_source_name,extr_source_id")
        list = {e.extr_source_name : e.extr_source_id for e in extrs}
        return list
    # getsrcsinfo

    @staticmethod
    def getextr(psrcname,pmodeid=None,psrcid=None):
        extr = Externalref.select (pwhere="extr_source_name = '{}' and {}"
                                   .format(psrcname
                                           ,"extr_mode_id = '{}'".format(pmodeid) if pmodeid is not None
                                        else "extr_source_id = '{}'".format(psrcid)
                                           )
                                   )
        return extr


    @staticmethod
    def getsrcid(psrcname,pmodeid):
        extrs = Externalref.getextr(psrcname=psrcname,pmodeid=pmodeid)
        srcid = None if len(extrs) == 0 else extrs[0].extr_source_id
        return srcid
    # getsrcid

    @staticmethod
    def getmodeid(psrcname,psrcid):
        extrs = Externalref.getextr(psrcname=psrcname,psrcid=psrcid)
        modeid = None if len(extrs) == 0 else extrs[0].extr_mode_id
        return modeid

    @staticmethod
    def existssrcid(psrcname,psrcid):
        extrs = Externalref.getextr(psrcname=psrcname,psrcid=psrcid)
        return (len(extrs) > 0)


    @staticmethod
    def delete():
        Baseobject.delete(Externalref._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Externalref
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def getODMmodeid(psrcid):
        return Externalref.getmodeid(psrcname=Externalref.SOURCE_ODM,psrcid=psrcid)


    @staticmethod
    def getODMsrcid(pmodeid):
        return Externalref.getsrcid(psrcname=Externalref.SOURCE_ODM,pmodeid=pmodeid)

#Externalref

