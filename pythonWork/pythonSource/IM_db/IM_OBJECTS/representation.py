from datetime import date
from .relationship import Relation
from .baseobject import Baseobject
from .modelelement import Modelelement,Modelelemtype
from .entity import Entity
from .attribute import Attribute


class Elementrep(Baseobject):
    _tablename: str = 'elementreps'
    _prefix: str = 'eler'
    _columnlist: list = []

    def __init__(self):
        if (len(Elementrep._columnlist) == 0): Elementrep._columnlist = Baseobject.gettablecolumns(Elementrep._tablename)
        super().__init__(tablename=Elementrep._tablename, prefix=Elementrep._prefix)
        eler_index = 0
        eler_uc = 'system'
        eler_dc = date.today()



    """what is displayed on bottom (0) and what in higer positions"""
    def displorder(self):
        elem = Modelelement.getelement(self.eler_mode_id)
        if isinstance(elem,Entity):
            return elem.getsubtypelevel()
        elif isinstance(elem,Attribute):
            return elem.attr_displ_seq
        else: return 0
    #displorder


    @staticmethod
    def delete(pwhere=None):
        return Baseobject.delete(Elementrep._tablename,pwhere=pwhere)

    def select(self, pwhere=None, porderby=None):
        return super().select(Elementrep,pwhere=pwhere,porderby=porderby)


    @staticmethod
    def getbydiagmode(pdiagid, pmodeid,pidx=None):
        elers = Elementrep().select(pwhere="""eler_diag_id = {} 
                                              and eler_mode_id = {}
                                              and eler_index = {}"""
                                    .format(pdiagid, pmodeid,pidx if pidx is not None else 'eler_index'))
        if elers is None:
            return []
        elif (pidx is None):
            #may be several
            return elers
        else:
            #can only be one
            return elers[0]
    #getbydiagmode
# elementrep

class Relationrep(Baseobject):
    NORTH = 'N'
    EAST = 'O'
    SOUTH = 'S'
    WEST = 'W'
    ONE = Relation.ONE
    MANY = Relation.MANY

    _tablename: str = 'relationreps'
    _prefix: str = 'relr'
    _columnlist: list = []

    def __init__(self):
        if (len(Relationrep._columnlist) == 0): Relationrep._columnlist = Baseobject.gettablecolumns(Relationrep._tablename)
        super().__init__(tablename=Relationrep._tablename, prefix=Relationrep._prefix)
        relr_uc = 'system'
        relr_dc = date.today()

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Relationrep._tablename
                               , psql="""
CREATE TABLE relationreps(
    relr_id                  integer primary key autoincrement,
    relr_diag_id             integer NOT NULL,
    relr_mode_id             integer NOT NULL,
    relr_linewidth        integer DEFAULT 1 NOT NULL,
    relr_linecolor          varchar(6) NULL
        constraint relr_lf_chk CHECK  (length(relr_linecolor)= 6),
    relr_lineopacity      integer NULL
        constraint relr_ldk_chk CHECK(relr_lineopacity BETWEEN 0 AND 100),
    relr_startedge          varchar(1) NULL
        constraint relr_stk_chk CHECK(relr_startedge IN ('N','O','S','W')),
    relr_startposition       integer NULL
        constraint relr_stp_chk CHECK(relr_startposition BETWEEN 0.0 AND 100.0),
		relr_start_connector   VARCHAR2(1) NULL
				CHECK(relr_start_connector IN ('1','M')),
    relr_starttext_angle    integer NULL
        constraint relr_stwi_chk CHECK(relr_starttext_angle BETWEEN - 179 AND 180),
    relr_starttext_distance   integer NULL
        constraint relr_stab_chk CHECK(relr_starttext_distance BETWEEN 1 AND 9999),
    relr_starttext_x         integer NULL
        constraint relr_stx_chk CHECK(relr_starttext_x BETWEEN -9999 AND 999999),
    relr_starttext_y         integer NULL
        constraint relr_sty_chk CHECK(relr_starttext_y BETWEEN -9999 AND 999999),
    relr_starttext_width    integer NULL
        constraint relr_stb_chk CHECK(relr_starttext_width BETWEEN 1 AND 9999),
    relr_starttext_height     integer NULL
        constraint relr_sth_chk CHECK(relr_starttext_height BETWEEN 1 AND 9999),
    relr_endedge            varchar(1) NULL
        constraint relr_ek_chk CHECK(relr_endedge IN ('N','O','S','W')),
    relr_endposition         integer NULL
        constraint relr_ep_chk CHECK(relr_endposition BETWEEN 0.0 AND 100.0),
	relr_end_connector   VARCHAR2(1) NULL
			CHECK(relr_end_connector IN ('1','M')),
    relr_endtext_angle      integer NULL
        constraint relr_ewi_chk CHECK(relr_endtext_angle BETWEEN - 179 AND 180),
    relr_endtext_distance     integer NULL
        constraint relr_eab_chk CHECK(relr_endtext_distance BETWEEN 1 AND 9999),
    relr_endtext_x           integer NULL
        constraint relr_ex_chk CHECK(relr_endtext_x BETWEEN -9999 AND 999999),
    relr_endtext_y           integer NULL
        constraint relr_ey_chk CHECK(relr_endtext_y BETWEEN -9999 AND 999999),
    relr_endtext_width      integer NULL
        constraint relr_eb_chk CHECK(relr_endtext_width BETWEEN 1 AND 9999),
    relr_endtext_height       integer NULL
        constraint relr_eh_chk CHECK(relr_endtext_height BETWEEN 1 AND 9999),
    relr_fontcolor        varchar(6) DEFAULT '000000' NULL
        constraint relr_sf_chk CHECK(length(relr_fontcolor)= 6),
    relr_fontsize      integer NULL
        constraint relr_sg_chk CHECK(relr_fontsize BETWEEN 1 AND 999),
    relr_uc              varchar(30) NOT NULL,
    relr_dc                  varchar(30) NOT NULL,
    relr_um                  varchar(30) ,
    relr_dm                  varchar(30),
	CONSTRAINT relr_un UNIQUE(relr_diag_id,relr_mode_id),
    CONSTRAINT relr_diag_fk FOREIGN KEY(relr_diag_id)
        REFERENCES diagramS(diag_id),
	CONSTRAINT relr_mode_fk FOREIGN KEY(relr_mode_id)
        REFERENCES modelelement(mode_id)
            ON DELETE CASCADE
)
        """)

    @staticmethod
    def delete(pwhere=None):
        return Baseobject.delete(Relationrep._tablename,pwhere=pwhere)


    @staticmethod
    def select(pwhere=None,porderby=None):
        return Baseobject.select(pclass=Relationrep,pwhere=pwhere,porderby=porderby)

    def getlinesegments(self):
        return Linesegment.select(pwhere="lise_relr_id={}".format(self.relr_id))


# relationrep

class Linesegment(Baseobject):
    DADO = "DADO"
    DASHED = "DASHED"
    DOTTED= "DOTTED"
    SOLID = "SOLID"

    _tablename: str = 'linesegments'
    _prefix: str = 'lise'
    _columnlist: list = []

    def __init__(self):
        if (len(Linesegment._columnlist) == 0): Linesegment._columnlist = Baseobject.gettablecolumns(Linesegment._tablename)
        super().__init__(tablename=Linesegment._tablename, prefix=Linesegment._prefix)
        lise_uc = 'system'
        lise_dc = date.today()

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Linesegment._tablename
                               , psql="""
CREATE TABLE linesegments(
    lise_id          integer primary key autoincrement,
    lise_seq        integer NOT NULL,
    lise_relr_id     integer NOT NULL,
    lise_x           integer NOT NULL
        CONSTRAINT ck_relr_relr_fontcolor CHECK(lise_x BETWEEN 0 AND 999999) ,
    lise_y           integer NOT NULL
        CONSTRAINT ck_relr_relr_fontcolor CHECK(lise_y BETWEEN 0 AND 999999) ,
    lise_linetype   VARCHAR2(6)NULL
        CONSTRAINT ck_lise_linetype CHECK(lise_linetype IN('DADO','DASHED','DOTTED','SOLID')),
	lise_angle 	 integer,
    lise_uc       varchar(30) NOT NULL,
    lise_dc           varchar(30) NOT NULL,
    lise_um           varchar(30) ,
    lise_dm           varchar(30),
	CONSTRAINT lise__un UNIQUE(lise_relr_id,lise_seq),
	CONSTRAINT lise_relr_fk FOREIGN KEY(lise_relr_id)
	      REFERENCES relationreps(relr_id)
	            ON DELETE CASCADE
)
        """)

    @staticmethod
    def delete(pwhere=None):
        return Baseobject.delete(Linesegment._tablename)

    @staticmethod
    def select(pwhere=None, porderby="lise_seq"):
        return Baseobject.select(pclass=Linesegment, pwhere=pwhere, porderby=porderby)

# linesegment
