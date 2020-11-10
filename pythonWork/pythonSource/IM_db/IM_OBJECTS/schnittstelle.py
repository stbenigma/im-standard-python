from .baseobject import Baseobject
from .modelelement import Modelelemtype

class Schnittstelle(Baseobject):
    _tablename:str = 'schnittstellen'
    _prefix:str = 'schn'
    _columnlist:list = ['schn_id',  'schn_name',    'schn_beschr'
                ,'schn_odm_guid',   'schn_uc',  'schn_dc'
                ,'schn_um', 'schn_dm']

    def __init__(self, psrcname=None, psrcid=None):
        super().__init__(tablename=Schnittstelle._tablename,prefix=Schnittstelle._prefix
                         ,columnlist= Schnittstelle._columnlist
                         , pmodelemtype=Modelelemtype.INTF
                         , pscrid=psrcid
                         , psrcname=psrcname)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Schnittstelle._tablename
                               , psql="""
    CREATE TABLE schnittstellen
        (
         SCHN_ID integer primary key autoincrement, 
         SCHN_NAME VARCHAR (60) NOT NULL , 
         SCHN_BESCHR VARCHAR (4000)  , 
     	 SCHN_odm_guid	varchar(36),
         SCHN_UC VARCHAR (30) NOT NULL , 
         SCHN_DC VARCHAR (30) NOT NULL , 
         SCHN_UM VARCHAR (30) NULL , 
         SCHN_DM VARCHAR (30) NULL ,
     CONSTRAINT SCHN_UN UNIQUE (SCHN_NAME)
        )
        """)

    def getname(self,plang=None):
        return self.schn_name
    def getqualifiedname(self,plang=None):
        return self.schn_name

    def getdescr(self, plang=None):
        return self.schn_beschr

    @staticmethod
    def delete():
        Baseobject.delete(Schnittstelle._tablename)

    @staticmethod
    def select(pwhere=None, porderby='schn_name'):
        return Baseobject.select(pclass=Schnittstelle
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def getmapped(pentiid=None,pattrid=None):
        if pentiid is not None:
            return Schnittstelle.select(pwhere="""schn_id in (select tabl_schn_id 
                                                        from tabellen
                                                        join tabl_enti_maps on tema_tabl_id = tabl_id
                                                        where tema_enti_id = {}
                                                        )""".format(pentiid))
        if pattrid is not None:
            return Schnittstelle.select(pwhere="""schn_id in (select tabl_schn_id 
                                                        from tabellen
                                                        join schnittstelle_attrs on scha_tabl_id = tabl_id
                                                        join attr_transf on attf_scha_id = scha_id
                                                        where attf_attr_id = {}
                                                        )""".format(pattrid))
        return []

#Schnittstelle



