from .baseobject import Baseobject

class Schnittstelle(Baseobject):
    def __init__(self):
        super().__init__(tablename='schnittstelle',prefix='schn'
                         ,columnlist=['schn_id',  'schn_name',    'schn_beschr'
                ,'schn_odm_guid',   'schn_uc',  'schn_dc'
                ,'schn_um', 'schn_dm'])

    def createtable(self):
        super().createtable("""
    CREATE TABLE schnittstelle
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

    def webfilespec(self):
        return self.schn_name.upper() + '.html'
#Schnittstelle

def indexlist():
    schn = Schnittstelle().select(porderby='schn_name')
    indexlist = [[s.schn_name, '',s.webfilespec(), s.schn_id] for s in schn]
    return indexlist
#indexlist


