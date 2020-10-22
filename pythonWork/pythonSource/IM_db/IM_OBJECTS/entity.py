from .baseobject import Baseobject,MultilangBaseobject
from .key import Key
from .sprachtext import Sprachtext
from IM_DB import dbDML,dbDDL
from datetime import date


class Entity(MultilangBaseobject):
    _tablename:str = 'entities'
    _prefix:str = 'enti'
    _columnlist:list = ['enti_id'
		,'enti_name'		,'enti_descr'
		,'enti_tooltip'	,'enti_short_name'	,'enti_prefix'
		,'enti_exp_tuplecnt'
        ,'enti_uc'
		,'enti_dc','enti_um','enti_dm'
        ]

    def __init__(self, psrcname=None, psrcid=None):
        super().__init__(tablename=Entity._tablename, prefix=Entity._prefix
                         , columnlist = Entity._columnlist
                         , multilangcols = {'enti_name':Sprachtext.ENTI_NAME
                                          ,'enti_descr':Sprachtext.ENTI_COMMENT
                                          ,'enti_tooltip': Sprachtext.ENTI_TOOLTIP}
                         , pmodelemtype=Modelelemtype.ENTI
                         , pscrid=psrcid
                         , psrcname=psrcname
                         )
        self._parents = None
        self._children = None
        self._synonyms = None
        self._schluessel = None
        self._attributes = None

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Entity._tablename
                               , psql="""
CREATE TABLE ENTITIES
    (
     ENTI_ID integer NOT NULL  primary key,
     ENTI_NAME VARCHAR (60) NOT NULL ,
     ENTI_SHORT_NAME VARCHAR (15) NULL ,
     ENTI_PREFIX VARCHAR (5) NULL ,
     ENTI_TOOLTIP VARCHAR (4000) NULL ,
     ENTI_DESCR VARCHAR (4000) NULL ,
     ENTI_EXP_TUPLECNT VARCHAR (500) NULL ,
     ENTI_UC VARCHAR(30) NULL  ,
     ENTI_DC VARCHAR (30) NOT NULL ,
     ENTI_UM VARCHAR (30) NULL ,
     ENTI_DM VARCHAR (30) NULL
    ,CONSTRAINT ENTI_NAME_UK UNIQUE (ENTI_NAME ASC)
    ,CONSTRAINT ENTI_MODE_FK FOREIGN KEY    (     ENTI_ID)
		REFERENCES MODELELEMENT    (     MODE_ID )
    ON DELETE CASCADE
    )"""
    )

    @staticmethod
    def createviews():
        dbDDL.dropView("SUPERENTI");
        dbDDL.createTable("""create view SUPERENTI AS 
            select superentity.enti_id as superenti_id, superentity.enti_name as super_enti_name
            ,subentity.enti_id as subenti_id, subentity.enti_name as sub_enti_name
 from ENTITIES superentity
      join arcs on superentity.enti_id = arcs_enti_id
      join relations relfrom on  (rela_arcs_id_from  = ARCS_ID and RELA_ENTI_ID_from = superentity.ENTI_ID)
                        or (rela_arcs_id_to  = ARCS_ID and RELA_ENTI_ID_to = superentity.ENTI_ID)
       left  join ENTITIES subentity on  (subentity.ENTI_ID =  rela_enti_id_to and rela_arcs_id_from = arcs_id )
 or (subentity.ENTI_ID =  rela_enti_id_from and rela_arcs_id_to = arcs_id )
      where RELA_TYPE in ('ISAS')
        """)

    def getmodellelement(self):
        return Modelelement.getbyelemid(pentiid=self.enti_id)
    def getmodeid(self):
        return self.getmodellelement().mode_id

    def getname(self,plang=None):
        return self._getsprachval(colname='enti_name',plang=plang)
    def getdescr(self,plang=None):
        return self._getsprachval(colname='enti_descr',plang=plang)

    def getcategory(pid):
        return Entity().getbyid(pid).enti_category_guid

    def getparents(self):
        if (self.getid() is not None) and (self._parents is None):
            parents = Entity.select(pwhere="enti_id in (select superenti_id from SUPERENTI where subenti_id = {})".format(self.getid()))
            if parents is not None and len(parents) > 0:
                self._parents = parents
        #fi
        return self._parents
    #getparent

    def getchildren(self):
        if (self.getid() is not None) and (self._children is None):
            self._children =  Entity.select(pwhere='enti_id in (select subenti_id from SUPERENTI where superenti_id = {})'.format(self.getid())
                                            , porderby= 'enti_name')
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
            self._schluessel = Key.select(pwhere='keys_enti_id = {}'.format(self.getid())
                                          , porderby='keys_laufnr')
        # fi
        return self._schluessel
    #getschluessel

    def getattributes(self):
        if (self.getid() is not None) and (self._attributes is None):
            self._attributes = Attribute.select(pwhere='attr_enti_id = {}'.format(self.getid()))
        # fi
        return self._attributes
    #getschluessel

    @staticmethod
    def delete():
        Baseobject.delete(Entity._tablename)

    @staticmethod
    def select(pwhere=None, porderby="enti_name"):
        entis =  Baseobject.select(pclass=Entity
                                 , pwhere=pwhere, porderby=porderby)
        return entis

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
        """[(0,'name', [Entity]'), (54,'name', [Entity])]"""
        for d in data:
            entis = []
            for e in d[2].split(','):
                ename = dbDML.select("select enti_name from entitaeten where enti_id = {}".format(e))
                entis.append((ename[0][0],'ENTI'+str(e)))
            retval.append([d[0], d[1],entis])
        data = dbDML.select(lsqlt)
        """[(0,'name', [Entity]'), (54,'name', [Entity])]"""
        for d in data:
            retval.append([d[0], d[1], [Entity().getbyid(e) for e in d[2].split(',')]])
        return retval
    #maopingto
#Entity

class Synonym(MultilangBaseobject):
    _tablename: str = 'synonyms'
    _prefix: str = 'syno'
    _columnlist: list = ['syno_id','syno_name','syno_enti_id','syno_uc','syno_dc','syno_um','syno_dm']
##    _multilangcols: list = {'syno_name': 'SYNO_NAME'}

    def __init__(self,pname=None,pentiid=None):
        super().__init__(tablename=Synonym._tablename, prefix=Synonym._prefix
                         , columnlist=Synonym._columnlist
                         ,multilangcols = {'syno_name': Sprachtext.SYNO_NAME}
                         ,pmodelemtype=Modelelemtype.SYNO)
        self.syno_name = pname
        self.syno_enti_id = pentiid
        self.syno_uc = 'SYS'
        self.syno_dc = date.today()

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Synonym._tablename
                               , psql="""
CREATE TABLE SYNONYMS
    (
     SYNO_ID INTEGER NOT NULL primary key,
     SYNO_NAME VARCHAR (60) NOT NULL ,
     SYNO_ENTI_ID integer NOT NULL ,
     SYNO_UC VARCHAR(30) NULL  ,
     SYNO_DC VARCHAR (30) NOT NULL ,
     SYNO_UM VARCHAR (30) NULL ,
     SYNO_DM VARCHAR (30) NULL
     ,CONSTRAINT SYNO_ENTI_FK FOREIGN KEY     (     SYNO_ENTI_ID)
		 REFERENCES ENTITIES     (     ENTI_ID )
		 ON DELETE CASCADE
     ,CONSTRAINT SYNO_MODE_FK FOREIGN KEY     (     SYNO_ID)
		 REFERENCES MODELELEMENT     (     MODE_ID )
		 ON DELETE CASCADE
    )
        """)

    def getname(self,plang=None):
        return self._getsprachval(colname='syno_name',plang=plang)

    def getparent(self):
        return Entity.getbyid(self.syno_enti_id)
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
from .attribute import Attribute
from .modelelement import Modelelemtype,Modelelement



