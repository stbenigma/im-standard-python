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
        return super().webanker(self.tabl_schn_id)

    def getmodellelement(self):
        return Modellelement.getbyelemid(ptablid=self.tabl_id)

    def getcolumns(self):
        return Schnittstelleattr.select("scha_tabl_id = {}".format(self.tabl_id))

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
        """[(0,'name', [Entitaet]'), (54,'name', [Tabelle])]"""
        for d in data:
            entis = []
            for e in d[2].split(','):
                ename = dbDML.select("select enti_name from entitaeten where enti_id = {}".format(e))
                entis.append((ename[0][0],'ENTI'+str(e)))
            retval.append([d[0], d[1],entis])
        data = dbDML.select(lsqlt)
        """[(0,'name', [Entitaet]'), (54,'name', [Tabelle])]"""
        for d in data:
            retval.append([d[0], d[1],[Tabelle().getbyid(e) for e in d[2].split(',')]])
        return retval
    #maopingto
#Tabelle

class Schnittstelleattr(Baseobject):

    _tablename:str = 'schnittstelle_attrs'
    _prefix:str = 'scha'
    _columnlist:list = ['scha_id', 'scha_column_name', 'scha_format', 'scha_fremdsystem_id'
                                       ,'scha_beschr', 'scha_type_string', 'scha_tabl_id', 'scha_daty_id'
                                    , 'scha_wrtb_id','scha_odm_guid'
                                       ,'scha_uc', 'scha_dc', 'scha_um', 'scha_dm']

    def __init__(self):
        super().__init__(tablename=Schnittstelleattr._tablename, prefix=Schnittstelleattr._prefix
                        ,columnlist = Schnittstelleattr._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Schnittstelleattr._tablename
                               , psql="""
    create table schnittstelle_attrs
    (
        scha_id             integer
            primary key autoincrement,
        scha_column_name    varchar(60) not null,
        scha_format         varchar(200),
        scha_fremdsystem_id varchar(100),
        scha_beschr         varchar(4000),
        scha_type_string    varchar(200),
        scha_tabl_id        integer     not null,
        scha_daty_id        integer     not null,
        scha_wrtb_id        integer ,
        scha_odm_guid       varchar(36),
        scha_uc             varchar(30) not null,
        scha_dc             varchar(30) not null,
        scha_um             varchar(30),
        scha_dm             varchar(30),
        constraint scha_daty_fk FOREIGN KEY (scha_daty_id) references datatypes (daty_id),
        constraint scha_wrtb_fk FOREIGN KEY (scha_wrtb_id) references wertebereiche (wrtb_id),
        constraint scha_tabl_fk FOREIGN KEY (scha_tabl_id) references tabellen(tabl_id),
        constraint scha_uk unique (scha_tabl_id,scha_column_name)        
        )
        """)

    def webanker(self,pmodelid):
        return super().webanker(pmodelid)

    def getmodellelement(self):
        return Modellelement.getbyelemid(pschaid=self.scha_id)

    def gettablname(self):
        tabname = Tabelle().getbyid(self.scha_tabl_id).tabl_name
        return tabname
    #gettablname

    def getschnid(self):
        tab = Tabelle().getbyid(self.scha_tabl_id)
        return tab.tabl_schn_id
    #getschnid

    @staticmethod
    def delete():
        Baseobject.delete(Schnittstelleattr._tablename)

    @staticmethod
    def select(pwhere=None, porderby="scha_column_name"):
        return Baseobject.select(pclass=Schnittstelleattr
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def indexlist(pschnid):
        schas = Schnittstelleattr.select(pwhere= """scha_tabl_id in (select tabl_id from tabellen where tabl_schn_id={})""".format(pschnid)
                                        ,porderby='scha_column_name')
        indexlist = []
        for s in schas:
            t = Tabelle().getbyid(s.scha_tabl_id)
            indexlist.append(["{} ({})".format(s.scha_column_name,t.tabl_name),  s.webanker(t.tabl_schn_id), s.scha_id])
        return indexlist
    #indexlist

    @staticmethod
    def mappingto(pschaid):
        lsqle = """select 0 schn_id, 'Logisches Modell' schn_name, group_concat(attr_id,',')
            	from  attr_transf as mastermap
    	        left join attributes on attr_id = mastermap.attf_attr_id
    	        where  mastermap.attf_scha_id = {}
    	        GROUP BY mastermap.attf_scha_id""".format(pschaid)
        lsqlt = """select schn_id,schn_name,group_concat(scha_id,',')
    	        from schnittstelle_attrs subscha
    	        join tabellen subtab on subtab.tabl_id = subscha.scha_tabl_id
    	        join schnittstellen on schn_id = subtab.TABL_SCHN_ID
    	        where subscha.scha_id in
        	          (select attf1.ATTF_SCHA_ID
    	               from attr_transf attf1
    	                 join attr_transf attf2  on attf2.attf_attr_id = attf1.attf_attr_id
    	                                and attf2.attf_scha_id != attf1.attf_scha_id
    	                  where attf2.attf_scha_id = {}
    	            )
    	            /* eigene Schnittstelle wird nicht angezeigt*/
    	           and schn_id != (select supertab.tabl_schn_id 
    	                            from schnittstelle_attrs superattr
    	                            join tabellen supertab on supertab.tabl_id = superattr.scha_tabl_id
    	                            where superattr.scha_id = {})
                group by schn_id,schn_name
                """.format(pschaid, pschaid)
        retval = []
        data = dbDML.select(lsqle)
        """[(0,'name', [Attribute]'), (54,'name', [Schnittstelleattr])]"""
        for d in data:
            attrs = []
            for e in d[2].split(','):
                aname = dbDML.select("select attr_anzname from attributes where attr_id = {}".format(e))
                attrs.append((aname[0][0], 'ATTR' + str(e)))
            retval.append([d[0], d[1], attrs])
        data = dbDML.select(lsqlt)
        """[(0,'name', [Attribute]'), (54,'name', [Schnittstelleattr])]"""
        for d in data:
            retval.append([d[0], d[1], [Schnittstelleattr().getbyid(e) for e in d[2].split(',')]])
        return retval
    # maopingto
#Schnittstelleattr

class Attrtransf(Baseobject):
    INBOUND:str = 'INBOUND'
    OUTBOUND:str = 'OUTBOUND'
    MANUELL:str = 'MANUELL'
    PERIODE:str = 'PERIODE'
    ZPKT:str = 'ZPKT'

    _tablename: str = 'attr_transf'
    _prefix: str = 'attf'
    _columnlist: list = ['attf_id' ,'attf_laufnr'  ,'attf_richtung'
                        ,'attf_transf_formel'   ,'attf_ausloeseart' ,'attf_ausloeseperiod'
                        ,'attf_scha_id' ,'attf_attr_id' ,'attf_uc'
                        ,'attf_dc'  ,'attf_um'  ,'attf_dm']

    def __init__(self):
        super().__init__(tablename=Attrtransf._tablename, prefix=Attrtransf._prefix
                     , columnlist=Attrtransf._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Attrtransf._tablename
                           , psql="""
                            create table attr_transf 
         (
       attf_id integer primary key autoincrement,
       attf_laufnr integer  not null check ( attf_laufnr > 0) , 
       attf_richtung varchar (7) not null check ( attf_richtung in ('INBOUND', 'OUTBOUND') ) , 
       attf_transf_formel varchar (4000) null , 
       attf_ausloeseart varchar (10) null check ( attf_ausloeseart in ('MANUELL', 'PERIODE', 'ZPKT') ) , 
       attf_ausloeseperiod integer null , 
       attf_scha_id integer null , 
       attf_attr_id integer null , 
       attf_uc varchar (30)  , 
       attf_dc varchar (30)  , 
       attf_um varchar (30) null , 
       attf_dm varchar (30)  null  
		,constraint attf_un unique (attf_richtung , attf_scha_id , attf_attr_id, attf_laufnr )
 	   ,constraint attf_attr_fk foreign key (attf_attr_id) 
 	      references attributes (attr_id )  on delete cascade 
 	   ,constraint attf_scha_fk foreign key (attf_scha_id) 
 	      references schnittstelle_attr (scha_id ) on delete cascade 
 	      )
    """)

    @staticmethod
    def delete():
        Baseobject.delete(Attrtransf._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Attrtransf
                                    , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def columnlist(pattrid=None):
        data = dbDML.select("""select  schn_name,schn_id,group_concat(scha_id,',') schaids
                            from attr_transf
                            join schnittstelle_attrs on scha_id = ATTF_SCHA_ID
                            join tabellen on tabl_id = scha_tabl_id
                            join schnittstellen on schn_id = tabl_schn_id 
                            where ATTF_ATTR_ID = {}
                            group by schn_name,schn_id
                            order by schn_name
                            """.format(pattrid))
        retval = []
        try:
            for d in data:
                schn_name,schn_id = d[0],d[1]
                collist = {}
                for schaid in d[2].split(','):
                    scha = Schnittstelleattr().getbyid(schaid)
                    tabname = Tabelle().getbyid(scha.scha_tabl_id).tabl_name
                    collist[tabname+'.'+scha.scha_column_name] = scha.webanker(schn_id)
                # for
                retval.append([schn_name, collist])
            # for
        except  Exception as e:
            print(str(e))
            pass
        # try
        return retval
    #columnlist
#Attrtransf


