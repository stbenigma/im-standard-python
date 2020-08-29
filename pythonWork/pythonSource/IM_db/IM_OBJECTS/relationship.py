from datetime import datetime

from IM_DB import dbDML
from .baseobject import Baseobject, MultilangBaseobject
from .modelelement import Modelelement, Modelelemtype
from .sprachtext import Sprachtext


class Arc(Baseobject):
    _tablename: str = 'arcs'
    _prefix: str = 'arcs'
    _columnlist: list = ['arcs_id', 'arcs_name', 'arcs_enti_id', 'arcs_uc', 'arcs_dc', 'arcs_um', 'arcs_dm']

    def __init__(self, pname, pentiid, puc, pdc=None):
        super().__init__(tablename=Arc._tablename, prefix=Arc._prefix
                         , columnlist=Arc._columnlist)
        self.arcs_name = pname
        self.arcs_enti_id = pentiid
        self.arcs_uc = puc
        self.arcs_dc = pdc if (pdc is not None) else str(datetime)

    def insert(self):
        self.arcs_id = Modelelement(Modelelemtype.getidbyshortname(Modelelemtype.ARCS)).insert()
        super().insert()

        ExternalRef.insertextrefs(pmodeid=self.arcs_id, preflist=self.__extref)
        return self.arcs_id

    def getmodeid(self):
        return self.arcs_id

    def getrelalist(self):
        """List of relations in this arc"""
        return Relation().select(pwhere="arcs_id = {}".format(self.arcs_id))

    def getentity(self):
        return Entity().getbyid(self.arcs_enti_id)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Arc._tablename
                               , psql="""
CREATE TABLE ARCS
    (
     ARCS_ID INTEGER NOT NULL primary key autoincrement,
     ARCS_NAME VARCHAR (60) NOT NULL ,
     ARCS_ENTI_ID NUMERIC (10) NOT NULL ,
     ARCS_UC VARCHAR(30) NULL  ,
     ARCS_DC VARCHAR (30) NOT NULL ,
     ARCS_UM VARCHAR (30) NULL ,
     ARCS_DM VARCHAR (30) NULL
    ,CONSTRAINT ARCS_UK UNIQUE  (ARCS_ENTI_ID ASC, ARCS_NAME ASC)
	,CONSTRAINT ARCS_ENTI_FK FOREIGN KEY    (     ARCS_ENTI_ID) 
	    REFERENCES ENTITIES (     ENTI_ID ) ON DELETE CASCADE ON UPDATE NO ACTION
    ,CONSTRAINT ARCS_MODE_FK FOREIGN KEY (     ARCS_ID)
        REFERENCES MODELELEMENT (MODE_ID ) ON DELETE CASCADE ON UPDATE NO ACTION)
    """
        )

    @staticmethod
    def delete():
        Baseobject.delete(Arc._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        arcs = Baseobject.select(pclass=Arc
                                 , pwhere=pwhere, porderby=porderby)
        return arcs

class Relation(MultilangBaseobject):
    ONE2ONE: str = '1:1'
    ISAROLE: str = 'ISAR'
    ISASUBTYPE: str = 'ISAS'
    MANY2ONE: str = 'M:1'
    MANY2MANY: str = 'M:N'
    ONE:str = '1'
    MANY:str = 'M'

    _tablename: str = 'relations'
    _prefix: str = 'rela'
    _columnlist: list = ['rela_id', 'rela_name', 'rela_type', 'rela_enti_id_from',
                            'rela_arcs_id_from', 'rela_assoc_from_to', 'rela_maptype_from_to',
                         'rela_mandatory_from_to',
                         'rela_hist_from_to', 'rela_enti_id_to', 'rela_arcs_id_to', 'rela_assoc_to_from',
                         'rela_maptype_to_from', 'rela_mandatory_to_from', 'rela_hist_to_from',
                         'rela_uc', 'rela_dc', 'rela_um', 'rela_dm', ]

    """        (rela_type, rela_enti_id_from, rela_assoc_from_to
         , rela_mandatory_from_to, rela_hist_from_to
         , rela_enti_id_to, rela_assoc_to_from
         , rela_mandatory_to_from, bezi_hist_zu_von
         , bezi_odm_guid, bezi_uc, bezi_dc, rela_name
         , bezi_source_enti_guid, bezi_target_enti_guid
         )
"""

    def __init__(self):
            super().__init__(tablename=Relation._tablename, prefix=Relation._prefix
                             , columnlist=Relation._columnlist
                             , multilangcols={'rela_assoc_from_to': Sprachtext.RELA_TEXT_FROM
                    , 'rela_assoc_to_from': Sprachtext.RELA_TEXT_TO}
                             )

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Relation._tablename
                                   , psql="""
CREATE TABLE RELATIONS
    (
     RELA_ID NUMERIC (10) NOT NULL  primary key,
     RELA_NAME VARCHAR (60) NOT NULL ,
     RELA_TYPE VARCHAR (4) NOT NULL CHECK ( RELA_TYPE IN ('1:1', 'ISAR', 'ISAS', 'M:1', 'M:N') ) ,
     RELA_ENTI_ID_FROM NUMERIC (10) NOT NULL ,
     RELA_ARCS_ID_FROM NUMERIC (10)  ,
     RELA_ASSOC_FROM_TO VARCHAR (4000) NULL ,
     RELA_MAPTYPE_FROM_TO CHAR (1) NOT NULL CHECK ( RELA_MAPTYPE_FROM_TO IN ('1', 'M') ) ,
     RELA_MANDATORY_FROM_TO VARCHAR (5) NOT NULL  CHECK(RELA_MANDATORY_FROM_TO IN('FALSE','TRUE')),
     RELA_HIST_FROM_TO VARCHAR (5) NOT NULL  CHECK(RELA_HIST_FROM_TO IN('FALSE','TRUE')),
     RELA_ENTI_ID_TO NUMERIC (10) NOT NULL ,
     RELA_ARCS_ID_TO NUMERIC (10)  ,
     RELA_ASSOC_TO_FROM VARCHAR (100) NULL ,
     RELA_MAPTYPE_TO_FROM CHAR (1) NOT NULL CHECK ( RELA_MAPTYPE_TO_FROM IN ('1', 'M') ) ,
     RELA_MANDATORY_TO_FROM VARCHAR (5) NOT NULL  CHECK(RELA_MANDATORY_TO_FROM IN('FALSE','TRUE')),
     RELA_HIST_TO_FROM VARCHAR (4000) NOT NULL    		CHECK(RELA_HIST_TO_FROM IN('FALSE','TRUE')),
     RELA_UC VARCHAR(30) NULL  ,
     RELA_DC VARCHAR (30) NOT NULL ,
     RELA_UM VARCHAR (30) NULL ,
     RELA_DM VARCHAR (30) NULL ,
     CONSTRAINT RELA_MAPTYPE_CHK CHECK ((RELA_TYPE = 'ISAR'
  AND RELA_MAPTYPE_FROM_TO = '1'
  AND RELA_MAPTYPE_TO_FROM = '1'
  AND (RELA_MANDATORY_FROM_TO = 'TRUE'
  	  OR
  	  RELA_MANDATORY_TO_FROM = 'TRUE'
  	  )
) OR
(RELA_TYPE = 'ISAS'
  AND RELA_MAPTYPE_FROM_TO = '1'
  AND RELA_MAPTYPE_TO_FROM = '1'
  AND RELA_MANDATORY_FROM_TO = 'TRUE'
  AND RELA_MANDATORY_TO_FROM = 'TRUE'
  AND (RELA_ARCS_ID_FROM IS NOT NULL
  		OR
	   RELA_ARCS_ID_TO IS NOT NULL
	  )
) OR
(RELA_TYPE = '1:1'
  AND RELA_MAPTYPE_FROM_TO = '1'
  AND RELA_MAPTYPE_TO_FROM = '1'
) OR
(RELA_TYPE ='M:1'
  AND (
  	(RELA_MAPTYPE_FROM_TO = '1'
 	 AND RELA_MAPTYPE_TO_FROM = 'M'
  	) OR
  	(RELA_MAPTYPE_FROM_TO = 'M'
  	 AND RELA_MAPTYPE_TO_FROM = '1'
	)
  )
) OR
(RELA_TYPE = 'M:N'
  AND RELA_MAPTYPE_TO_FROM = 'M'
  AND RELA_MAPTYPE_FROM_TO = 'M'
)
)
    ,CONSTRAINT RELA_UK1 UNIQUE (RELA_ENTI_ID_FROM ASC, RELA_ENTI_ID_TO ASC, RELA_TYPE ASC, RELA_ASSOC_TO_FROM ASC, RELA_ASSOC_FROM_TO ASC)
    ,CONSTRAINT RELA_UK_NAME UNIQUE (RELA_NAME ASC)
    ,CONSTRAINT RELA_ARCS_FROM_FK FOREIGN KEY(     RELA_ARCS_ID_FROM)
    REFERENCES ARCS    (     ARCS_ID )
    ,CONSTRAINT RELA_ARCS_TO_FK FOREIGN KEY(     RELA_ARCS_ID_TO)
    REFERENCES ARCS    (     ARCS_ID )
    ,CONSTRAINT RELA_ENTI_FROM_FK FOREIGN KEY (     RELA_ENTI_ID_FROM)
    REFERENCES ENTITIES    (     ENTI_ID )
    ,CONSTRAINT RELA_ENTI_TO_FK FOREIGN KEY(     RELA_ENTI_ID_TO)
    REFERENCES ENTITIES(     ENTI_ID )
    ,CONSTRAINT RELA_MODE_FK FOREIGN KEY(     RELA_ID)
    REFERENCES MODELELEMENT(     MODE_ID )    ON DELETE CASCADE
)"""
                        )

    @staticmethod
    def delete():
        Baseobject.delete(Relation._tablename)

    def insert(self):
        self.rela_id = Modelelement(pmeltshortname=Modelelemtype.RELA).insert()
        super().insert()

    @staticmethod
    def select(pwhere=None, porderby=None):
        rela = Baseobject.select(pclass=Relation
                                 , pwhere=pwhere, porderby=porderby)
        return rela

    def simpleType(self):
        """only the first try. Add arcs later to find distinguisch ISAR and ISAS"""
        if (self.rela_maptype_from_to == Relation.ONE and self.rela_maptype_to_from == Relation.ONE):
            retval = Relation.ONE2ONE
        elif (self.rela_maptype_from_to == Relation.MANY and self.rela_maptype_to_from == Relation.MANY):
            retval = Relation.MANY2MANY
        else:
            retval = Relation.MANY2ONE
        #fi
        return retval

    @staticmethod
    def updaterela(parcid, prelids):
        dbDML.exec("""update beziehungen
                set (rela_arcs_id_from,rela_arcs_id_to) =
                    (select case earc.enti_odm_guid
                            when evon.enti_odm_guid
                            then arcs_id else rela_arcs_id_from end von_arcs_id
                            ,case earc.enti_odm_guid
                            when ezu.enti_odm_guid
                            then arcs_id else rela_arcs_id_to end zu_arcs_id
                    from arcs
                    join entitaeten earc on arcs_enti_id = earc.enti_id
                    left join entitaeten evon on rela_enti_id_from = evon.enti_id
                    left join entitaeten ezu on rela_enti_id_to = ezu.enti_id
                    where arcs_id = {}
                    )
                where bezi_odm_guid in ({})
                """.format(parcid, prelids))

    @staticmethod
    def insertisa():
        dbDML.exec("""insert into beziehungen (rela_type, rela_enti_id_from, rela_assoc_from_to
                    ,rela_mandatory_from_to, rela_hist_from_to
                    , rela_enti_id_to, rela_assoc_to_from, rela_mandatory_to_from, bezi_hist_zu_von
                    , rela_arcs_id_from,bezi_uc, bezi_dc,rela_name)
                select 'ISA', slave_enti_id,''
                            , 'TRUE','FALSE'
                            ,master_enti_id,'','TRUE','FALSE'
                            ,arcs_id,arcs_uc, arcs_dc
                            ,arcs_name + '_' + slave_enti_name beziname
                            from arcs
                            join (select enti_id as master_enti_id
                                       , enti_odm_guid as master_guid from entitaeten) on master_enti_id = arcs_enti_id
                            join  (select enti_id as slave_enti_id
                                       , enti_enti_guid as slave_master_guid 
                                       ,enti_name as slave_enti_name from entitaeten) on slave_master_guid = master_guid
                           left join externalrefs on extr_mode_id = arcs_id
                           where extr_id is null
                """)
    # insertisa
# updaterela
