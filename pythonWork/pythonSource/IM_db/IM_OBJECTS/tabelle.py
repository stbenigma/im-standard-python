from .baseobject import Baseobject

class Tabelle(Baseobject):
    def __init__(self):
        super().__init__(tablename='tabelle', prefix='tabl'
                        ,columnlist = ['tabl_id', 	'tabl_name', 	'tabl_schn_id'
                ,  'tabl_prefix', 	'tabl_beschr', 	'tabl_odm_guid'
                ,'tabl_uc', 	'tabl_dc', 	'tabl_um', 	'tabl_dm'])

    def createtable(self):
        super().createtable("""
    CREATE TABLE tabelle
        (
         TABL_ID integer primary key autoincrement , 
         TABL_NAME VARCHAR (60) NOT NULL , 
         TABL_SCHN_ID integer NOT NULL , 
         TABL_PREFIX VARCHAR (60) NULL , 
         TABL_BESCHR VARCHAR (4000) NULL , 
     	 TABL_odm_guid	varchar(36),
         TABL_UC VARCHAR (30) NOT NULL , 
         TABL_DC VARCHAR (30) NOT NULL , 
         TABL_UM VARCHAR (30) NULL , 
         TABL_DM VARCHAR (30) NULL ,
    	  CONSTRAINT TABL_UN UNIQUE (TABL_SCHN_ID , TABL_NAME)
     	   ,CONSTRAINT TABL_SCHN_FK FOREIGN KEY (TABL_SCHN_ID) 
     	      REFERENCES SCHNITTSTELLE (SCHN_ID ) 
        )"""
                            )
#Tabelle

def indexlist(pschnid=None):
    data = Tabelle().select(pwhere= "tabl_schn_id={}".format('tabl_schn_id' if pschnid is None else pschnid)
                  ,porderby='tabl_name')
    indexlist = [[d.tabl_name,d.anker(),d.tabl_id] for d in data]
    return indexlist
#indexlist
