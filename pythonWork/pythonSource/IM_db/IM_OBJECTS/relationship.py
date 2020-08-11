from datetime import datetime

from IM_DB import dbDML
from .baseobject import Baseobject
from .modellelement import Modellelement, Modellelemtype, ExternalRef


class Arc(Baseobject):
    _tablename: str = 'arcs'
    _prefix: str = 'arcs'
    _columnlist: list = ['arcs_id', 'arcs_name', 'arcs_enti_id', 'arcs_uc', 'arcs_dc', 'arcs_um', 'arcs_dm']

    __extref = {}

    def __init__(self, pname, pentiid, puc, pdc=None):
        super().__init__(tablename=Arc._tablename, prefix=Arc._prefix
                         , columnlist=Arc._columnlist)
        self.arcs_name = pname
        self.arcs_enti_id = pentiid
        self.arcs_uc = puc
        self.arcs_dc = pdc if (pdc is not None) else str(datetime)

    def setsourceid(self, psrc, psrcid):
        self.__extref[psrc] = psrcid

    def getsourceid(self, psrc):
        try:
            return self.__extref[psrc]
        except:
            return None

    def insert(self):
        self.arcs_id = Modellelement(Modellelemtype.getidbyshortname(Modellelemtype.ARCS)).insert()
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
CREATE TABLE arcs(
    arcs_id        integer  not null primary key,
    arcs_name      VARCHAR2(60) NOT NULL,
    arcs_enti_id   integer NOT NULL,
    arcs_uc        VARCHAR2(30) NOT NULL,
    arcs_dc        varchar(30) NOT NULL,
    arcs_um        VARCHAR2(30) NULL,
    arcs_dm        varchar(30) NULL,
	UNIQUE(arcs_enti_id,arcs_name),
	CONSTRAINT arcs_enti_fk FOREIGN KEY(arcs_enti_id)
	        REFERENCES entitaeten(enti_id) ON DELETE CASCADE
)
    """
                               )

    @staticmethod
    def delete():
        Baseobject.delete(Arc._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        arcs = Baseobject.select(pclass=Arc
                                 , pwhere=pwhere, porderby=porderby)
        for value in arcs.values:
            for extr in ExternalRef.getbymodeid(pmodeid=value.arcs_id):
                value.setsourceid(psrc=extr.extr_source, psrcid=extr.extr_source_id)

        return arcs


class Relation(Baseobject):
    @staticmethod
    def updaterela(parcid, prelids):
        dbDML.exec("""update beziehungen
                set (bezi_von_arcs_id,bezi_zu_arcs_id) =
                    (select case earc.enti_odm_guid
                            when evon.enti_odm_guid
                            then arcs_id else bezi_von_arcs_id end von_arcs_id
                            ,case earc.enti_odm_guid
                            when ezu.enti_odm_guid
                            then arcs_id else bezi_zu_arcs_id end zu_arcs_id
                    from arcs
                    join entitaeten earc on arcs_enti_id = earc.enti_id
                    left join entitaeten evon on bezi_enti_id_von = evon.enti_id
                    left join entitaeten ezu on bezi_enti_id_zu = ezu.enti_id
                    where arcs_id = {}
                    )
                where bezi_odm_guid in ({})
                """.format(parcid, prelids))

    @staticmethod
    def insertisa():
        dbDML.exec("""insert into beziehungen (bezi_type, bezi_enti_id_von, bezi_assoc_von_zu
                    ,bezi_pflicht_assoc_von_zu, bezi_hist_von_zu
                    , bezi_enti_id_zu, bezi_assoc_zu_von, BEZI_PFLICHT_ASSOC_ZU_VON, bezi_hist_zu_von
                    , bezi_von_arcs_id,bezi_uc, bezi_dc,bezi_name)
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
