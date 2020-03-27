from .baseobject import Baseobject

class Schnittstelle(Baseobject):
    _tablename:str = 'schnittstellen'
    _prefix:str = 'schn'
    _columnlist:list = ['schn_id',  'schn_name',    'schn_beschr'
                ,'schn_odm_guid',   'schn_uc',  'schn_dc'
                ,'schn_um', 'schn_dm']

    def __init__(self):
        super().__init__(tablename=Schnittstelle._tablename,prefix=Schnittstelle._prefix
                         ,columnlist= Schnittstelle._columnlist)

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

    def webanker(self):
        return super().webanker(self.schn_id)

    @staticmethod
    def delete():
        Baseobject.delete(Schnittstelle._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Schnittstelle
                                 , pwhere=pwhere, porderby=porderby)

#Schnittstelle

def indexlist():
    schn = Schnittstelle.select(porderby='schn_name')
    indexlist = [[s.schn_name, s.webanker(),s.schn_id] for s in schn]
    return indexlist
#indexlist


