from .baseobject import Baseobject
from IM_DB import dbDML

class Tabelle(Baseobject):
    _tablename:str = 'tabellen'
    _prefix:str = 'tabl'
    _columnlist:list = ['tabl_id', 	'tabl_name', 	'tabl_schn_id'
                ,  'tabl_prefix', 	'tabl_beschr', 	'tabl_odm_guid'
                ,'tabl_uc', 	'tabl_dc', 	'tabl_um', 	'tabl_dm']

    def __init__(self):
        super().__init__(tablename=Tabelle._tablename, prefix=Tabelle._prefix
                        ,columnlist = Tabelle._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Tabelle._tablename
                               , psql="""
    CREATE TABLE tabellen
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

    def webanker(self):
        return super().webanker(self.tabl_schn_id)

    @staticmethod
    def delete():
        Baseobject.delete(Tabelle._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Tabelle
                                 , pwhere=pwhere, porderby=porderby)
    @staticmethod
    def selectbyschnid(pschnid):
        return Tabelle.select(pwhere="tabl_schn_id = {}".format(pschnid), porderby="tabl_name")

    @staticmethod
    def indexlist(pschnid=None):
        data = Tabelle.select(pwhere= "tabl_schn_id={}".format('tabl_schn_id' if pschnid is None else pschnid)
                  ,porderby='tabl_name')
        indexlist = [[d.tabl_name,d.webanker(),d.tabl_id] for d in data]
        return indexlist
    #indexlist

    @staticmethod
    def mappingto(ptablid):
        lsqle = """select 0 schn_id, 'Logisches Modell' schn_name, group_concat(enti_id,',')
        	from  tabl_enti_maps as mastermap
	        left join entitaeten on enti_id = mastermap.tema_enti_id
	        where  mastermap.tema_tabl_id = {}
	        GROUP BY mastermap.tema_tabl_id""".format(ptablid)
        lsqlt = """select tabl_schn_id,schn_name,group_concat(tabl_id,',')
	        from tabellen subtab
	        join schnittstellen on schn_id = TABL_SCHN_ID
	        where tabl_id in
    	          (select tema1.tema_tabl_id
	               from tabl_enti_maps tema1
	                 join tabl_enti_maps tema2 on tema2.tema_enti_id = tema1.tema_enti_id
	                                and tema2.tema_tabl_id != tema1.tema_tabl_id
	                  where tema2.tema_tabl_id = {}
	            )
            group by tabl_schn_id,schn_name
            """.format(ptablid)
        retval = []
        data = dbDML.select(lsqle)
        """[(0,'name', [Entitaet]'), (54,'name', [Tabelle])]"""
        ###for d in data:
            ####retval.append([d[0], d[1],[Entitaet().getbyid(e) for e in d[2].split(',')]])
        data = dbDML.select(lsqlt)
        """[(0,'name', [Entitaet]'), (54,'name', [Tabelle])]"""
        for d in data:
            retval.append([d[0], d[1],[Tabelle().getbyid(e) for e in d[2].split(',')]])
        return retval
    #maopingto
#Tabelle


