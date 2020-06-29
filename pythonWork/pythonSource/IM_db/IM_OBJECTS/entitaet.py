from .baseobject import Baseobject,MultilangBaseobject
from .modellelement import Modellelement
from .schluessel import Schluessel
from .sprachtext import Sprachtext
from IM_DB import dbDML
from .attribut import Attribut


class Entitaet(MultilangBaseobject):
    _tablename:str = 'entitaeten'
    _prefix:str = 'enti'
    _columnlist:list = ['enti_id'		,'enti_odm_guid'		,'enti_augb_id'
		,'enti_tech_name'	,'enti_name'		,'enti_beschr'
		,'enti_tooltip'	,'enti_kurzname'	,'enti_prefix'
		,'enti_beispiele'	,'enti_erw_tupel'	,'enti_uc'
		,'enti_dc'	,'enti_enti_guid',	'enti_enti_id'
		,'enti_category_guid']


    def __init__(self):
        super().__init__(tablename=Entitaet._tablename, prefix=Entitaet._prefix
                        ,columnlist = Entitaet._columnlist
                         ,multilangcols = {'enti_name':Sprachtext.ENTI_NAME
                                          ,'enti_beschr':Sprachtext.ENTI_COMMENT})
        self._parent = None
        self._children = None
        self._synonyms = None
        self._schluessel = None
        self._attributes = None

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Entitaet._tablename
                               , psql="""
create table entitaeten
(
	enti_id integer not null
		primary key autoincrement,
	enti_odm_guid varchar(36),
	enti_augb_id integer,
	enti_tech_name varchar(60)
		unique,
	enti_name varchar(60) not null
		unique,
	enti_beschr varchar(4000),
	enti_tooltip varchar(100),
	enti_kurzname varchar(20),
	enti_prefix varchar(10),
	enti_beispiele varchar(4000),
	enti_erw_tupel varchar(10),
	enti_uc varchar(30),
	enti_dc varchar(30),
	enti_enti_guid varchar(80),
	enti_enti_id integer,
	enti_category_guid varchar(80),
	check (enti_erw_tupel IN(
            '1 Mio',
            '100',
            '10000',
            '>100 Mio'
        ))
    ,CONSTRAINT enti_enti_FK FOREIGN KEY (enti_enti_guid) 
     	      REFERENCES entitaeten (enti_id ) 
        
)"""
                            )

    def webanker(self):
        return super().webanker()

    def getmodellelement(self):
        return Modellelement.getbyelemid(pentiid=self.enti_id)
    def getmodeid(self):
        return self.getmodellelement().mode_id

    def getname(self,plang=None):
        return self._getsprachval(colname='enti_name',plang=plang)
    def getbeschr(self,plang=None):
        return self._getsprachval(colname='enti_beschr',plang=plang)

    def getcategory(pid):
        return Entitaet().getbyid(pid).enti_category_guid

    def getparent(self):
        if (self.getid() is not None) and (self.enti_enti_id is not None)\
                and (self._parent is None):
            #es hat ID und es hat einen Parentid aber noch nicht gelesen
            self._parent = Entitaet().getbyid(self.enti_enti_id)
        #fi
        return self._parent
    #getparent

    def getchildren(self):
        if (self.getid() is not None) and (self._children is None):
            self._children =  Entitaet.select(pwhere= 'enti_enti_id = {}'.format(self.getid())
                                              ,porderby= 'enti_name')
        #fi
        return self._children
    #getchildren
    def getsynonyms(self):
        if (self.getid() is not None) and (self._synonyms is None):
            self._synonyms = Synonym.select(pwhere='syno_enti_id = {}'.format(self.getid())
                                             , porderby='syno_name')
        # fi
        return self._synonyms
    #getsynonyms
    def getschluessel(self):
        if (self.getid() is not None) and (self._schluessel is None):
            self._schluessel = Schluessel.select(pwhere='schl_enti_id = {}'.format(self.getid())
                                             , porderby='schl_laufnr')
        # fi
        return self._schluessel
    #getschluessel

    def getattributes(self):
        if (self.getid() is not None) and (self._attributes is None):
            self._attributes = Attribut.select(pwhere='attr_enti_id = {}'.format(self.getid()))
        # fi
        return self._attributes
    #getschluessel

    @staticmethod
    def delete():
        Baseobject.delete(Entitaet._tablename)

    @staticmethod
    def select(pwhere=None, porderby="enti_name"):
        entis =  Baseobject.select(pclass=Entitaet
                                 , pwhere=pwhere, porderby=porderby)
        return entis

    @staticmethod
    def indexlist(plang=None):
        data = Entitaet.select(porderby='enti_name')
        indexlist = []
        for d in data:
            indexlist.append([d.getname(),d.webanker(),d.enti_id])
        #for
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
        """[(0,'name', [Entitaet]'), (54,'name', [Entitaet])]"""
        for d in data:
            entis = []
            for e in d[2].split(','):
                ename = dbDML.select("select enti_name from entitaeten where enti_id = {}".format(e))
                entis.append((ename[0][0],'ENTI'+str(e)))
            retval.append([d[0], d[1],entis])
        data = dbDML.select(lsqlt)
        """[(0,'name', [Entitaet]'), (54,'name', [Entitaet])]"""
        for d in data:
            retval.append([d[0], d[1],[Entitaet().getbyid(e) for e in d[2].split(',')]])
        return retval
    #maopingto
#Entitaet

class Synonym(MultilangBaseobject):
    _tablename: str = 'synonyme'
    _prefix: str = 'syno'
    _columnlist: list = ['syno_id','syno_name','syno_enti_id']
##    _multilangcols: list = {'syno_name': 'SYNO_NAME'}

    def __init__(self,pname=None,pentiid=None):
        super().__init__(tablename=Synonym._tablename, prefix=Synonym._prefix
                         , columnlist=Synonym._columnlist
                         ,multilangcols = {'syno_name': Sprachtext.SYNO_NAME})
        self.syno_name = pname
        self.syno_enti_id = pentiid

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Synonym._tablename
                               , psql="""
            create table synonyme
(
	syno_id integer not null
		primary key autoincrement,
	syno_name varchar(200),
	syno_enti_id integer not null
		references entitaeten
			on delete cascade,
	unique (syno_name, syno_enti_id)
)
        """)
    def webanker(self):
        return super().webanker()

    def getname(self,plang:str=None):
        return self._getsprachval(colname='syno_name',plang=plang)

    def getmodellelement(self):
        return Modellelement.getbyelemid(psynoid=self.syno_id)

    def getmodeid(self):
        return self.getmodellelement().mode_id

    def getparent(self):
        return Entitaet.getbyid(self.syno_enti_id)
    # getparent

    @staticmethod
    def delete():
        Baseobject.delete(Synonym._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        synos = Baseobject.select(pclass=Synonym
                                  ,pwhere=pwhere, porderby=porderby)
        return synos
    #select
#Synonym




