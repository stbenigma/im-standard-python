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
         tabl_id integer primary key autoincrement , 
         tabl_name varchar (60) not null , 
         tabl_schn_id integer not null , 
         tabl_prefix varchar (60) null , 
         tabl_beschr varchar (4000) null , 
     	 tabl_odm_guid	varchar(36),
         tabl_uc varchar (30) not null , 
         tabl_dc varchar (30) not null , 
         tabl_um varchar (30) null , 
         tabl_dm varchar (30) null ,
    	  CONSTRAINT TABL_UN UNIQUE (TABL_SCHN_ID , TABL_NAME)
     	   ,CONSTRAINT TABL_SCHN_FK FOREIGN KEY (TABL_SCHN_ID) 
     	      REFERENCES SCHNITTSTELLE (SCHN_ID ) 
        )"""
                            )

    def webanker(self):
        return super().webanker(pmodelid=self.tabl_schn_id)

    def getmodellelement(self):
        return Modellelement.getbyelemid(ptablid=self.tabl_id)

    def getcolumns(self):
        return Schnittstelleattr.select("scha_tabl_id = {}".format(self.tabl_id))

    def getname(self):
        return self.tabl_name

    def insert(self):
        self.tabl_id = Modelelement(Modelelemtype.TABL).insert()
        super().insert()

    @staticmethod
    def delete():
        Baseobject.delete(Tabelle._tablename)

    @staticmethod
    def select(pwhere=None, porderby="tabl_name"):
        return Baseobject.select(pclass=Tabelle
                                 , pwhere=pwhere, porderby=porderby)
    @staticmethod
    def selectbyschnid(pschnid):
        return Tabelle.select(pwhere="tabl_schn_id = {}".format(pschnid))

    @staticmethod
    def indexlist(pschnid=None):
        data = Tabelle.select(pwhere= "tabl_schn_id={}".format('tabl_schn_id' if pschnid is None else pschnid))
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
	            /* eigene Schnittstelle wird nicht angezeigt*/
	           and schn_id != (select tabl_schn_id 
	                            from tabellen where tabl_id = {})
            group by tabl_schn_id,schn_name
            """.format(ptablid,ptablid)
        retval = []
        data = dbDML.select(lsqle)
        """[(0,'name', [Entitaet]'), ]"""
        for d in data:
            retval.append([d[0], d[1],[Entitaet().getbyid(e) for e in d[2].split(',')]])
        data = dbDML.select(lsqlt)
        """[(54,'name', [Tabelle])]"""
        for d in data:
            retval.append([d[0], d[1],[Tabelle().getbyid(e) for e in d[2].split(',')]])
        return retval
    #maopingto
#Tabelle
from .schnittstattr import Schnittstelleattr
from .entitaet import Entitaet




