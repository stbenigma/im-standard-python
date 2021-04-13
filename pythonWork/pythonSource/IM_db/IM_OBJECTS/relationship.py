from datetime import datetime

from IM_DB import dbDML
from .baseobject import Baseobject, MultilangBaseobject
from .baseobject import Boolean
from .modelelement import Modelelemtype
from .languagetext import Languagetext
import IM_OBJECTS


class Arc(Baseobject):
    _tablename: str = 'arcs'
    _prefix: str = 'arcs'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.ARCS
    _columnlist: list = []
    _defaultorderby = "arcs_id"

    def __init__(self, pname=None, pentiid=None, puc=None, pdc=None, psrcname=None, psrcid=None):
        if (len(Arc._columnlist) == 0): Arc._columnlist = Baseobject.gettablecolumns(Arc._tablename)
        super().__init__( psrcname=psrcname
                         , pscrid=psrcid)
        self.arcs_name = pname
        self.arcs_enti_id = pentiid
        self.arcs_uc = puc
        self.arcs_dc = pdc if (pdc is not None) else str(datetime)

    def getmodeid(self):
        return self.arcs_id

    def getrelalist(self):
        """List of relations in this arc"""
        return Relation.select(pwhere=("rela_arcs_id_from = ? or rela_arcs_id_to = ?", self.arcs_id,self.arcs_id))

    def getentity(self):
        return IM_OBJECTS.Entity().getbyid(self.arcs_enti_id)

    def getarcselem(self,pdiagid):
        data = dbDML.select("""with lseg as (select linesegments.*
                   ,row_number() over (PARTITION BY lise_relr_id ORDER BY lise_seq ASC) up
                   ,row_number() over (PARTITION BY lise_relr_id ORDER BY lise_seq desc) down
               from linesegments)
            select relr_id,lsegstart.lise_x startx,lsegstart.lise_y starty
                 ,lsegend.lise_x endx,lsegend.lise_y endy
                 ,earc.enti_id,earc.enti_name
                 ,case when lsegstart.up = 1 then lsegstart.lise_angle else lsegend.lise_angle  end angle
            from arcs
            join entities earc on earc.enti_id =arcs_enti_id
            join relations on rela_arcs_id_from = arcs_id or rela_arcs_id_to = arcs_id
            join relationreps on relr_mode_id = rela_id
            join lseg lsegstart        on relr_id = lsegstart.lise_relr_id
                                and ((lsegstart.up = 1 and RELA_ARCS_ID_from = arcs_id)
                                    or (lsegstart.down = 1 and RELA_ARCS_ID_to = arcs_id)
                                    )
            left join lseg lsegend on relr_id = lsegend.lise_relr_id
                                and ((lsegend.up = lsegstart.up + 1 and RELA_ARCS_ID_from = arcs_id)
                                    or (lsegend.down = lsegstart.down + 1 and RELA_ARCS_ID_to = arcs_id)
                                    )
        where relr_diag_id = {}
        and arcs_id = {}
        """.format(pdiagid, self.arcs_id))
        return data
    # liesarcselem


    @staticmethod
    def getrelaarcs(pdiagid):
        return Arc.select(pwhere=("""arcs_id in (select case when rela_arcs_id_from is NULL 
                                                then rela_arcs_id_to
                                                else rela_arcs_id_from end rela_arcs_id 
                                            from relations 
                                            where rela_id = ?)""", prelaid))

        #getrelaarcs
    @staticmethod
    def getdiagarcs(pdiagid):
        return Arc.select(pwhere=("""arcs_id in (select case when rela_arcs_id_from is NULL 
                                                then rela_arcs_id_to
                                                else rela_arcs_id_from end rela_arcs_id 
                                            from relations 
                                            join relationreps on relr_mode_id = rela_id
                                            where relr_diag_id = ?)""", pdiagid)
                          ,porderby="arcs_id")
        #getrelaarcs


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
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.RELA
    _columnlist: list = []
    _defaultorderby = "rela_name"

    def __init__(self, psrcname=None, psrcid=None):
        if (len(Relation._columnlist) == 0): Relation._columnlist = Baseobject.gettablecolumns(Relation._tablename)
        super().__init__( multilangcols={'rela_assoc_from_to': Languagetext.RELA_TEXT_FROM
                                        , 'rela_assoc_to_from': Languagetext.RELA_TEXT_TO}
                         , psrcname=psrcname
                         , pscrid=psrcid
                         )



    def getmandatorytofrom(self):
        return Boolean.str2bool(self.rela_mandatory_to_from)

    def getmandatoryfromto(self):
        return Boolean.str2bool(self.rela_mandatory_from_to)

    def gethisttofrom(self):
        return Boolean.str2bool(self.rela_hist_to_from)

    def gethistfromto(self):
        return Boolean.str2bool(self.rela_hist_from_to)

    def getname(self,plang=None):
        return self.rela_name

    def getassocfromto(self,plang=None):
        return self._getsprachval(colname='rela_assoc_from_to',plang=plang)
    def getassoctofrom(self,plang=None):
        return self._getsprachval(colname='rela_assoc_to_from',plang=plang)
    def getfromentity(self):
        return IM_OBJECTS.Entity().getbyid(pid=self.rela_enti_id_from)
    def gettoentity(self):
        return IM_OBJECTS.Entity().getbyid(pid=self.rela_enti_id_to)
    def getanyarcid(self):
        return self.rela_arcs_id_from if self.rela_arcs_id_to is None else self.rela_arcs_id_to

    @staticmethod
    def getbyentity(pentiid):
        return Relation.select(pwhere=("""rela_enti_id_from = ? or rela_enti_id_to = ?""", pentiid,pentiid))


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

    def to_cardstr(self):
        return self._minmaxcardinality(pfromto=False)
    def from_cardstr(self):
        return self._minmaxcardinality(pfromto=True)

    def _minmaxcardinality(self, pfromto):
        maptype = self.rela_maptype_from_to if pfromto else self.rela_maptype_to_from
        mandatory = self.getmandatoryfromto() if pfromto else self.getmandatorytofrom()

        if maptype == Relation.ONE:
            return '1' if mandatory else '0..1'
        elif maptype == Relation.MANY:
            return '1..N' if mandatory else '0..N'
        else:
            raise Exception("invalid Value for Maptype {}".format(maptype))
    # minmaxcartinality

    @staticmethod
    def setarcinrela(prelids,parcid):
        """set arc-id for all relations in prelids"""
        dbDML.exec("""update RELATIONS
                      set RELA_ARCS_ID_FROM = 
                            (select arcs_id 
                                from arcs
                                where arcs_id = {} 
                                and ARCS_ENTI_ID = RELA_ENTI_ID_FROM) 
                        ,rela_arcs_id_to = 
                            (select arcs_id 
                            from arcs
                            where arcs_id = {} 
                                and ARCS_ENTI_ID = RELA_ENTI_ID_TO)
                        where rela_id in (select EXTR_MODE_ID from  external_refs
                                          where extr_source_id in ({})
                                        )
                    """.format(parcid,parcid,prelids))

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
            enti = IM_OBJECTS.Entity().getbyid(entiid)
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

