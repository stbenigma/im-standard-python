from datetime import date
from .relationship import Relation
from .baseobject import Baseobject


class Elementrep(Baseobject):
    _tablename: str = 'elementreps'
    _prefix: str = 'eler'
    _columnlist: list = ['eler_id', 'eler_position_x', 'eler_position_y'
        , 'eler_mode_id', 'eler_diag_id', 'eler_index'
        , 'eler_width', 'eler_height', 'eler_opacity', 'eler_color'
        , 'eler_marginwidth', 'eler_marginopacity', 'eler_margincolor'
        , 'eler_fontsize', 'eler_fontcolor'
        , 'eler_uc', 'eler_dc', 'eler_um', 'eler_dm'
                         ]

    def __init__(self):
        super().__init__(tablename=Elementrep._tablename, prefix=Elementrep._prefix
                         , columnlist=Elementrep._columnlist)
        eler_index = 0
        eler_uc = 'system'
        eler_dc = date.today()

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Elementrep._tablename
                               , psql="""
CREATE TABLE elementreps(
	  eler_id               integer primary key autoincrement,
      eler_mode_id          integer NOT NULL,
      eler_diag_id          integer NOT NULL,
      eler_index            NUMBER(4) DEFAULT 0 NOT NULL,
      eler_position_x       integer NULL,
      eler_position_y       integer NULL,
      eler_width           integer NOT NULL,
      eler_height            integer NOT NULL,
      eler_opacity        integer NULL
          CHECK(eler_opacity BETWEEN 0 AND 100),
      eler_color            varchar(6)  NOT NULL
          CHECK(length(eler_color)= 6),
      eler_marginwidth       integer NULL,
      eler_marginopacity    integer NULL
          CHECK(eler_marginopacity BETWEEN 0 AND 100),
      eler_margincolor        varchar(6)  NULL
          CHECK(length(eler_margincolor)= 6),
      eler_fontsize   integer NULL
          CHECK(eler_fontsize BETWEEN 1 AND 999),
      eler_fontcolor     varchar(6) NULL
          CHECK(length(eler_fontcolor)= 6),
      eler_uc           varchar(30) NOT NULL,
      eler_dc               varchar(30) NOT NULL,
      eler_um               varchar(30) ,
      eler_dm               varchar(30),
  	CONSTRAINT eler_un UNIQUE(eler_diag_id,eler_mode_id,eler_index),
    CONSTRAINT eler_diag_fk FOREIGN KEY(eler_diag_id)
          REFERENCES diagrams(diag_id)
              ON DELETE CASCADE,
  	CONSTRAINT eler_mode_fk FOREIGN KEY(eler_mode_id)
          REFERENCES MODELELEMENT(mode_id)
              ON DELETE CASCADE
)
        """)

    @staticmethod
    def delete():
        Baseobject.delete(Elementrep._tablename)


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
    _columnlist: list = ['relr_id', 'relr_diag_id', 'relr_mode_id'
        , 'relr_linewidth', 'relr_linecolor', 'relr_lineopacity'
        , 'relr_startedge', 'relr_startposition', 'relr_start_connector'
        , 'relr_starttext_angle', 'relr_starttext_distance', 'relr_starttext_x', 'relr_starttext_y'
        , 'relr_starttext_width', 'relr_starttext_height'
        , 'relr_endedge', 'relr_endposition', 'relr_end_connector'
        , 'relr_endtext_angle'
        , 'relr_endtext_distance', 'relr_endtext_x', 'relr_endtext_y'
        , 'relr_endtext_width', 'relr_endtext_height'
        , 'relr_fontcolor', 'relr_fontsize'
        , 'relr_uc', 'relr_dc', 'relr_um', 'relr_dm'
                         ]

    def __init__(self):
        super().__init__(tablename=Relationrep._tablename, prefix=Relationrep._prefix
                         , columnlist=Relationrep._columnlist)
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
    def delete():
        Baseobject.delete(Relationrep._tablename)

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
    _columnlist: list = ['lise_id', 'lise_seq', 'lise_relr_id'
        , 'lise_x', 'lise_y', 'lise_linetyp', 'lise_angle'
        , 'lise_uc', 'lise_dc', 'lise_um', 'lise_dm']

    def __init__(self):
        super().__init__(tablename=Linesegment._tablename, prefix=Linesegment._prefix
                         , columnlist=Linesegment._columnlist
                         )
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
    lise_linetyp   VARCHAR2(6)NULL
        CONSTRAINT ck_lise_linetype CHECK(lise_linetyp IN('DADO','DASHED','DOTTED','SOLID')),
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
    def delete():
        Baseobject.delete(Linesegment._tablename)

    @staticmethod
    def select(pwhere=None, porderby="lise_seq"):
        return Baseobject.select(pclass=Linesegment, pwhere=pwhere, porderby=porderby)

# linesegment
