from datetime import datetime

from IM_DB import dbDML
from .baseobject import Baseobject, MultilangBaseobject
from .baseobject import Boolean
from .entity import Entity
from .modelelement import Modelelemtype
from .sprachtext import Sprachtext


class Arc(Baseobject):
    _tablename: str = 'arcs'
    _prefix: str = 'arcs'
    _columnlist: list = ['arcs_id', 'arcs_name', 'arcs_enti_id', 'arcs_uc', 'arcs_dc', 'arcs_um', 'arcs_dm']

    def __init__(self, pname=None, pentiid=None, puc=None, pdc=None, psrcname=None, psrcid=None):
        super().__init__(tablename=Arc._tablename, prefix=Arc._prefix
                         , columnlist=Arc._columnlist
                         , pmodelemtype=Modelelemtype.ARCS
                         , psrcname=psrcname
                         , pscrid=psrcid)
        self.arcs_name = pname
        self.arcs_enti_id = pentiid
        self.arcs_uc = puc
        self.arcs_dc = pdc if (pdc is not None) else str(datetime)

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
     ARCS_ENTI_ID integer NOT NULL ,
     ARCS_UC VARCHAR(30) NULL  ,
     ARCS_DC VARCHAR (30) NOT NULL ,
     ARCS_UM VARCHAR (30) NULL ,
     ARCS_DM VARCHAR (30) NULL
    ,CONSTRAINT ARCS_UK UNIQUE  (ARCS_ENTI_ID ASC, ARCS_NAME ASC)
	,CONSTRAINT ARCS_ENTI_FK FOREIGN KEY    (     ARCS_ENTI_ID) 
	    REFERENCES entities (     ENTI_ID ) ON DELETE CASCADE ON UPDATE NO ACTION
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
    ONE: str = '1'
    MANY: str = 'M'

    _tablename: str = 'relations'
    _prefix: str = 'rela'
    _columnlist: list = ['rela_id', 'rela_name', 'rela_type', 'rela_enti_id_from',
                         'rela_arcs_id_from', 'rela_assoc_from_to', 'rela_maptype_from_to',
                         'rela_mandatory_from_to',
                         'rela_hist_from_to', 'rela_enti_id_to', 'rela_arcs_id_to', 'rela_assoc_to_from',
                         'rela_maptype_to_from', 'rela_mandatory_to_from', 'rela_hist_to_from',
                         'rela_uc', 'rela_dc', 'rela_um', 'rela_dm', ]

    def __init__(self, psrcname=None, psrcid=None):
        super().__init__(tablename=Relation._tablename, prefix=Relation._prefix
                         , columnlist=Relation._columnlist
                         , multilangcols={'rela_assoc_from_to': Sprachtext.RELA_TEXT_FROM
                                        , 'rela_assoc_to_from': Sprachtext.RELA_TEXT_TO}
                         , pmodelemtype=Modelelemtype.RELA
                         , psrcname=psrcname
                         , pscrid=psrcid
                         )

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Relation._tablename
                               , psql="""
CREATE TABLE RELATIONS
    (
     RELA_ID integer NOT NULL  primary key,
     RELA_NAME VARCHAR (60) NOT NULL ,
     RELA_TYPE VARCHAR (4) NOT NULL CHECK ( RELA_TYPE IN ('1:1', 'ISAR', 'ISAS', 'M:1', 'M:N') ) ,
     RELA_ENTI_ID_FROM integer NOT NULL ,
     RELA_ARCS_ID_FROM integer  ,
     RELA_ASSOC_FROM_TO VARCHAR (4000) NULL ,
     RELA_MAPTYPE_FROM_TO CHAR (1) NOT NULL CHECK ( RELA_MAPTYPE_FROM_TO IN ('1', 'M') ) ,
     RELA_MANDATORY_FROM_TO VARCHAR (5) NOT NULL  CHECK(RELA_MANDATORY_FROM_TO IN('FALSE','TRUE')),
     RELA_HIST_FROM_TO VARCHAR (5) NOT NULL  CHECK(RELA_HIST_FROM_TO IN('FALSE','TRUE')),
     RELA_ENTI_ID_TO integer NOT NULL ,
     RELA_ARCS_ID_TO integer  ,
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

    def getmandatorytofrom(self):
        return Boolean.str2bool(self.rela_mandatory_to_from)

    def getmandatoryfromto(self):
        return Boolean.str2bool(self.rela_mandatory_from_to)

    def gethisttofrom(self):
        return Boolean.str2bool(self.rela_hist_to_from)

    def gethistfromto(self):
        return Boolean.str2bool(self.rela_hist_from_to)

    def getassocfromto(self,plang=None):
        return self._getsprachval(colname='rela_assoc_from_to',plang=plang)
    def getassoctofrom(self,plang=None):
        return self._getsprachval(colname='rela_assoc_to_from',plang=plang)
    def getfromentity(self):
        return Entity().getbyid(pid=self.rela_enti_id_from)
    def gettoentity(self):
        return Entity().getbyid(pid=self.rela_enti_id_to)

    @staticmethod
    def delete():
        Baseobject.delete(Relation._tablename)

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
        # fi
        return retval

    @staticmethod
    def setarcinrela(prelids):
        """set arc-id for all relations in prelids"""
        dbDML.exec("""update RELATIONS
                      set RELA_ARCS_ID_FROM = 
                            (select arcs_id 
                                from arcs
                                join ENTITIES earc on earc.ENTI_ID = ARCS_ENTI_ID
                                    and earc.ENTI_ID = RELA_ENTI_ID_from)
                        ,rela_arcs_id_to = 
                            (select arcs_id 
                            from arcs
                            join ENTITIES earc on earc.ENTI_ID = ARCS_ENTI_ID
                                    and earc.ENTI_ID = RELA_ENTI_ID_to)
                        where rela_id in (select EXTR_MODE_ID from  external_refs
                                          where extr_source_id in ({})
                                        )
                    """.format(prelids))

    @staticmethod
    def setrelatypes():
        """make all relations to ISAS which are 1:1, both sides mandatory an all elements in arc are also mandatory"""
        dbDML.exec("""with arcrela as
            (select * from
  (select arcs_id,arcs_name,count(*) relacnt
   ,sum(case when RELA_MANDATORY_TO_FROM = 'TRUE'
                and RELA_MANDATORY_FROM_TO = 'TRUE'
                and rela_type = '1:1'
                then 1 else 0
                end
                ) isacnt
    from arcs
    join relations on (RELA_ARCS_ID_FROM = arcs_id or RELA_ARCS_ID_TO = arcs_id)
    group by arcs_id,arcs_name
    )
   where relacnt = isacnt
   )
update RELATIONS
set rela_type = 'ISAS'
where RELA_ARCS_ID_TO in (select arcs_id from arcrela)
   or RELA_ARCS_ID_from in (select arcs_id from arcrela)
            """
                   )
        """Roles are 1:1 with differen relationshipsend mandataory flag (TRUE/FALSE FALSE/TRUE)"""
        dbDML.exec("""update relations set  rela_type = 'ISAR'
                    where rela_type = '1:1'
                        and (RELA_MANDATORY_FROM_TO  !=  RELA_MANDATORY_TO_FROM)
                        """
                   )

    @staticmethod
    def insertisa(parc, pentiids):
        for entiid in pentiids:
            enti = Entity().getbyid(entiid)
            rela = Relation()
            rela.rela_type = Relation.ISASUBTYPE
            rela.rela_enti_id_from = enti.enti_id
            rela.rela_enti_id_to = parc.arcs_enti_id
            rela.rela_arcs_id_to = parc.arcs_id
            rela.rela_assoc_to_from = ''
            rela.rela_mandatory_to_from = 'TRUE'
            rela.rela_hist_to_from = 'FALSE'
            rela.rela_assoc_from_to = ''
            rela.rela_mandatory_from_to = 'TRUE'
            rela.rela_hist_from_to = 'FALSE'
            rela.rela_uc = parc.arcs_uc
            rela.rela_dc = parc.arcs_dc
            rela.rela_name = parc.arcs_name + '_' + enti.enti_name
            rela.rela_maptype_from_to = Relation.ONE
            rela.rela_maptype_to_from = Relation.ONE
            rela.insert()
    # insertisa
# setarcinrela
