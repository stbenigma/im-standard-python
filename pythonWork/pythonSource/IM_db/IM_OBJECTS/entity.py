from .key import Key
from IM_DB import dbDML,dbDDL
from datetime import date
from .baseobject import Baseobject,MultilangBaseobject
from .languagetext import Languagetext
from .language import Language
import IM_OBJECTS
from .userdefprop import Userdefpropvalue,Userdefprop


class Entity(MultilangBaseobject):
    _tablename:str = 'entities'
    _prefix:str = 'enti'
    _columnlist:list = []

    def __init__(self, psrcname=None, psrcid=None):
        if (len(Entity._columnlist) == 0): Entity._columnlist = Baseobject.gettablecolumns(Entity._tablename)
        super().__init__(tablename=Entity._tablename, prefix=Entity._prefix
                         , multilangcols = {'enti_name':Languagetext.ENTI_NAME
                                          ,'enti_descr':Languagetext.ENTI_COMMENT
                                          ,'enti_tooltip': Languagetext.ENTI_TOOLTIP}
                         , pmodelemtype=Modelelemtype.ENTI
                         , pscrid=psrcid
                         , psrcname=psrcname
                         )
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
        dbDDL.createTable("""
        create view SUPERENTI AS
    select rela_type,superentity.enti_id as superenti_id, superentity.enti_name as super_enti_name
        ,subentity.enti_id as subenti_id, subentity.enti_name as sub_enti_name
          from ENTITIES superentity
            join ARCS on ARCS_ENTI_ID = superentity.enti_id
            join relations
                  on  ((rela_arcs_id_from  = ARCS_ID and RELA_ENTI_ID_from = superentity.ENTI_ID)
                   or (rela_arcs_id_to  = ARCS_ID and RELA_ENTI_ID_to = superentity.ENTI_ID))
                     and RELA_TYPE =  'ISAS'
           left  join ENTITIES subentity on  (subentity.ENTI_ID =  rela_enti_id_to and rela_arcs_id_from = arcs_id )
                or (subentity.ENTI_ID =  rela_enti_id_from and rela_arcs_id_to = arcs_id )
    union all
    select rela_type,superentity.enti_id as superenti_id, superentity.enti_name as super_enti_name
        ,subentity.enti_id as subenti_id, subentity.enti_name as sub_enti_name
          from ENTITIES superentity
          join (select rela_type
               , case
                     when RELA_MANDATORY_TO_FROM = 'TRUE' then RELA_ENTI_ID_FROM
                     else RELA_ENTI_ID_TO end as rela_superenti_id
               , case
                     when RELA_MANDATORY_FROM_TO = 'TRUE' then RELA_ENTI_ID_FROM
                     else RELA_ENTI_ID_TO end as rela_subenti_id
                 from relations
                where rela_type = 'ISAR'
                ) on rela_superenti_id = superentity.ENTI_ID
        join ENTITIES subentity on subentity.ENTI_ID = rela_subenti_id
        """)

    def getmodellelement(self):
        return Modelelement.getbyelemid(pentiid=self.enti_id)

    def getmodeid(self):
        return self.enti_id

    def getname(self,plang=None):
        return self._getsprachval(colname='enti_name',plang=plang)

    def getdescr(self,plang=None):
        return self._getsprachval(colname='enti_descr',plang=plang)

    def getcategory(pid):
        return Entity().getbyid(pid).enti_category_guid

    def getparents(self):
        parents = Entity.select(pwhere="enti_id in (select superenti_id from SUPERENTI where subenti_id = {})"
                                .format(self.getid()))
        return [] if parents is None else parents
    #getparent

    def getchildren(self,ptype=None):
        """ptype None-> ALL, ISAS,'ISAR"""
        if ptype in (IM_OBJECTS.Relation.ISASUBTYPE,IM_OBJECTS.Relation.ISAROLE):
            relatype = ptype
        else:
            relatype = "%"
        children =  Entity.select(pwhere=
                                """enti_id in 
                                    (select subenti_id 
                                      from SUPERENTI 
                                      where superenti_id = {} 
                                      and rela_type like '{}')""".format(self.getid(),relatype)
                                )
        return []  if children is None else children
    #getchildren

    def getsynonyms(self):
        if (self.getid() is not None) and (self._synonyms is None):
            self._synonyms = Synonym.select(pwhere='syno_enti_id = {}'.format(self.getid())
                                             , porderby='syno_name')
        # fi
        return self._synonyms
    #getsynonyms


    def getkeys(self):
        return Key.select(pwhere='keys_enti_id = {}'.format(self.getid())
                                  , porderby='keys_name')
    #getkeys

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

    def getsubtypelevel(self):
        subtypelevel = dbDML.select("""
            with recursive enti as
            ( select 0 entilev, enti_id
            from entities
            where not exists (select 1 from superenti where rela_type = 'ISAS' AND subenti_id = enti_id)
            union all
            select enti.entilev + 1, subenti_id
            from superenti
            join enti on enti_id = superenti_id
            )
            select entilev from enti
            where enti_id = {}
            """.format(self.enti_id))
        return subtypelevel[0][0]

    @staticmethod
    def delete():
        Baseobject.delete(Entity._tablename)


    @staticmethod
    def select(pwhere=None, porderby="enti_name"):
        entis = Baseobject.select(pclass=Entity
                                 , pwhere=pwhere, porderby=porderby)
        return entis

    @staticmethod
    def mappingto(ptablid):
        lsqle = """select 0 intf_id, 'Logisches Modell' intf_name, group_concat(enti_id,',')
        	from  tabl_enti_maps as mastermap
	        left join entitaeten on enti_id = mastermap.tema_enti_id
	        where  mastermap.tema_tabl_id = {}
	        GROUP BY mastermap.tema_tabl_id""".format(ptablid)
        lsqlt = """select tabl_intf_id,intf_name,group_concat(tabl_id,',')
	        from tables subtab
	        join interfaces on intf_id = TABL_intf_ID
	        where tabl_id in
    	          (select tema1.tema_tabl_id
	               from tabl_enti_maps tema1
	                 join tabl_enti_maps tema2 on tema2.tema_enti_id = tema1.tema_enti_id
	                                and tema2.tema_tabl_id != tema1.tema_tabl_id
	                  where tema2.tema_tabl_id = {}
	            )
	            /* eigene Interface wird nicht angezeigt*/
	           and intf_id != (select tabl_intf_id 
	                            from tables where tabl_id = {})
            group by tabl_intf_id,intf_name
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
    _columnlist: list = []
##    _multilangcols: list = {'syno_name': 'ENTI_SYNONYM'}

    def __init__(self,pname=None,pentiid=None):
        if (len(Synonym._columnlist) == 0): Synonym._columnlist = Baseobject.gettablecolumns(Synonym._tablename)
        super().__init__(tablename=Synonym._tablename, prefix=Synonym._prefix
                         ,multilangcols = {'syno_name': Languagetext.ENTI_SYNONYM}
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
     ENTI_SYNONYM VARCHAR (60) NOT NULL ,
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
        retval = self._getsprachval(colname='syno_name',plang=plang)
        return '' if retval is None else retval

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
    @staticmethod
    def transfersynotransl():
        """get all udpr translations for synonyms except for the default language
           if it is comma separated, dispatch an entry per synonym into language texts.
           If order or number is not the same, ignore it"""
        for udpr in Userdefprop.select(pwhere="udpr_name like '___ENTI_SYNONYM'"):
            langiso2 = udpr.udpr_name[0:2].lower()
            langid=Language().getbyuk(lang_iso_code2=langiso2).getid()
            if langid == Language.liesdeflangid(): continue
            for udpv in Userdefpropvalue.select(pwhere="udpv_udpr_id = {}".format(udpr.udpr_id)):
                langsynos = udpv.udpv_value.split(',')
                for idx,syno in enumerate(Entity().getbyid(udpv.udpv_mode_id).getsynonyms()):
                    try:
                        synotransl = langsynos[idx]
                    except:
                        continue
                    lgtx=Languagetext()
                    lgtx.lgtx_attrname=Languagetext.ENTI_SYNONYM
                    lgtx.lgtx_text=synotransl
                    lgtx.lgtx_lang_id=langid
                    lgtx.lgtx_mode_id=syno.syno_id
                    lgtx.lgtx_uc=udpv.udpv_uc
                    lgtx.lgtx_dc=udpv.udpv_dc
                    lgtx.lgtx_um = udpv.udpv_um
                    lgtx.lgtx_dm = udpv.udpv_dm
                    lgtx.insert()

from .attribute import Attribute
from .modelelement import Modelelemtype,Modelelement



