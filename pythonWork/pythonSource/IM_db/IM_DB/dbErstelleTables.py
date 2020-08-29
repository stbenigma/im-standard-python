# -*- coding: latin-1 -*-

from IM_DB import *
from IM_OBJECTS import *


def erstelleInfra():
    #erlaube alles droppen
    Schnittstelle.createtable()
    Tabelle.createtable()
    Schnittstelleattr.createtable()
    Datatype.createtable()

    dbDDL.dropTable("speicherformate");
    dbDDL.createTable("""
    CREATE TABLE speicherformate(
    spfo_id             integer primary key autoincrement,
    spfo_name           varchar(60) unique NOT NULL,
    spfo_beschreibung   varchar(4000)
)
    """);

    Entitaet.createtable()
    Synonym.createtable()

    Schluessel.createtable()
    Schluesselelement.createtable()

    Wertebereich.createtable()
    Wertebereichgruppe.createtable()
    Vorgabewert.createtable()

    Attribut.createtable()

    Arc.createtable()

    Relation.createtable()

    dbDDL.dropTable("benudef_eigenschaft")
    dbDDL.createTable("""
CREATE TABLE benudef_eigenschaft(
    bdeg_id             integer NOT NULL primary key autoincrement,
    bdeg_thema          varchar(60 )NOT NULL,
    bdeg_gruppe         varchar(60 )NOT NULL,
    bdeg_name           varchar(60 )NOT NULL,
    bdeg_default_value           varchar(60 ),
    bdeg_beschreibung   varchar(4000 )NULL,
    bdeg_optional       varchar(5 )NOT NULL
        CHECK(bdeg_optional IN(
            'FALSE',
            'TRUE'
        )),
    bdeg_wrtb_id        integer ,
        bdeg_uc             varchar(30 )NOT NULL,
    bdeg_dc             varchar(30)NOT NULL,
    bdeg_um             varchar(30 )NULL,
    bdeg_dm             varchar(30)NULL,
	CONSTRAINT bdeg_un UNIQUE(bdeg_name),
	CONSTRAINT bdeg_wrtb_fk FOREIGN KEY(bdeg_wrtb_id)
	        REFERENCES wertebereiche(wrtb_id)	
)
""")

    dbDDL.dropTable("benudef_wert")
    dbDDL.createTable("""
CREATE TABLE benudef_wert(
    bdwe_id        integer NOT NULL primary key autoincrement,
    bdwe_wert      varchar(4000),
    bdwe_mode_id   varchar(4)NOT NULL,
    bdwe_bdeg_id   integer NOT NULL,
        bdwe_uc        varchar(30 )NOT NULL,
    bdwe_dc        varchar(30)NOT NULL,
    bdwe_um        varchar(30 )NULL,
    bdwe_dm        varchar(30)NULL,
	CONSTRAINT bdwe_un UNIQUE(bdwe_mode_id, bdwe_bdeg_id),
	CONSTRAINT bdwe_mode_fk FOREIGN KEY(bdwe_mode_id)
	        REFERENCES modellelement(mode_id) on delete cascade,
	CONSTRAINT bdwe_bdeg_fk FOREIGN KEY(bdwe_bdeg_id)
	        REFERENCES benudef_eigenschaft(bdeg_id) on delete cascade
		)
""")

    Modelelemtype.createtable()
    Modelelement.createtable()
    Externalref.createtable()

    dbDDL.dropTable("modelltyp_eigensch")
    dbDDL.createTable("""
CREATE TABLE modelltyp_eigensch(
	mote_id        integer NOT NULL primary key autoincrement,
    mote_melt_id   integer NOT NULL,
    mote_bdeg_id   integer NOT NULL,
	CONSTRAINT mote_un UNIQUE(mote_melt_id,mote_bdeg_id),
	CONSTRAINT mote_bdeg_fk FOREIGN KEY(mote_bdeg_id)
								        REFERENCES benudef_eigenschaft(bdeg_id) on delete cascade,
    CONSTRAINT mote_melt_fk FOREIGN KEY(mote_melt_id)
									   REFERENCES modellelem_typ(melt_id)
)
""")

    Sprache.createtable()
    Sprachtext.createtable()

    dbDDL.dropView("SUPERENTI");
    dbDDL.createTable("""create view SUPERENTI AS 
    select ae.enti_id super_enti_id,ae.enti_name super_enti_name
               ,e1.enti_id sub_enti_id,e1.enti_name sub_enti_name
      from arcs
      join entitaeten as ae on ae.enti_id = arcs_enti_id 
      join (select bezi_arcs_id
                   ,count(*) alleanz
           , SUM(case rela_mandatory_from_to when 'TRUE' then 1 else 0 end) nnvonanz
           , SUM(case rela_mandatory_to_from when 'TRUE' then 1 else 0 end) nnzuanz
            from   (select case when rela_arcs_id_from is null then rela_arcs_id_to else rela_arcs_id_from end bezi_arcs_id
                        , rela_mandatory_from_to
                        , rela_mandatory_to_from
                   from beziehungen
                   where rela_type in ('ISA', '1:1')
                )
            group by bezi_arcs_id) as st
            on st.bezi_arcs_id = arcs_id AND  alleanz = nnvonanz and alleanz = nnzuanz
      join beziehungen b1 on b1.rela_arcs_id_from = arcs_id or b1.rela_arcs_id_to = arcs_id
      join entitaeten e1 on e1.enti_id = b1.rela_enti_id_from  
    order by ae.enti_name""")

    Diagrammtyp.createtable()
    Diagramm.createtable();

    dbDDL.dropTable("melt_diat");
    dbDDL.createTable("""
CREATE TABLE melt_diat(
    medi_id        integer primary key autoincrement,
    medi_diat_id   integer NOT NULL,
    medi_melt_id   integer NOT NULL,
    medi_uc    varchar(30) NOT NULL,
    medi_dc        varchar(30) NOT NULL,
    medi_um        varchar(30) ,
    medi_dm        varchar(30),
	CONSTRAINT medi__un UNIQUE(medi_diat_id,
	                                   medi_melt_id),
    CONSTRAINT medi_diat_fk FOREIGN KEY(medi_diat_id)			           
					REFERENCES diagrammtypen(diat_id)
								    ON DELETE CASCADE,
	CONSTRAINT modi_melt_fk FOREIGN KEY(medi_melt_id)
		REFERENCES modellelem_typ(melt_id)
		     ON DELETE CASCADE
)	          """);
    dbDDL.dropTable("elementdarst");
    dbDDL.createTable("""
CREATE TABLE elementdarst(
				      eled_id               integer primary key autoincrement,
				      eled_position_x       integer NULL,
				      eled_position_y       integer NULL,
				      eled_breite           integer NOT NULL,
				      eled_hoehe            integer NOT NULL,
				      eled_deckkraft        integer NULL
				          CHECK(eled_deckkraft BETWEEN 0 AND 100),
				      eled_farbe            varchar(6)  NOT NULL
				          CHECK(length(eled_farbe)= 6),
				      eled_randbreite       integer NULL,
				      eled_randdeckkraft    integer NULL
				          CHECK(eled_randdeckkraft BETWEEN 0 AND 100),
				      eled_randfarbe        varchar(6)  NULL
				          CHECK(length(eled_randfarbe)= 6),
				      eled_schriftgroesse   integer NULL
				          CHECK(eled_schriftgroesse BETWEEN 1 AND 999),
				      eled_schriftfarbe     varchar(6) NULL
				          CHECK(length(eled_schriftfarbe)= 6),
				      eled_mode_id          integer NOT NULL,
				      eled_diag_id          integer NOT NULL,
				      eled_index            NUMBER(4)DEFAULT 0 NOT NULL,
				      eled_uc           varchar(30) NOT NULL,
				      eled_dc               varchar(30) NOT NULL,
				      eled_um               varchar(30) ,
				      eled_dm               varchar(30),
				  	CONSTRAINT eled_un UNIQUE(eled_diag_id,eled_mode_id,eled_index),
				      CONSTRAINT eled_diag_fk FOREIGN KEY(eled_diag_id)
				          REFERENCES diagramme(diag_id)
				              ON DELETE CASCADE,
				  	CONSTRAINT eled_mode_fk FOREIGN KEY(eled_mode_id)
				  			        REFERENCES modellelement(mode_id)
				  			            ON DELETE CASCADE
				  )""");
    dbDDL.dropTable("beziehung_darst");
    dbDDL.createTable("""
				  CREATE TABLE beziehung_darst(
				      beda_id                  integer primary key autoincrement,
				      beda_diag_id             integer NOT NULL,
				      beda_mode_id             integer NOT NULL,
				      beda_linienbreite        integer DEFAULT 1 NOT NULL,
				      beda_liniefarbe          varchar(6) NULL
				          constraint beda_lf_chk CHECK  (length(beda_liniefarbe)= 6),
				      beda_liniedeckkraft      integer NULL
				          constraint beda_ldk_chk CHECK(beda_liniedeckkraft BETWEEN 0 AND 100),
				      beda_startkante          varchar(1) NULL
				          constraint beda_stk_chk CHECK(beda_startkante IN(
				              'N',
				              'O',
				              'S',
				              'W'
				          )),
				      beda_startposition       integer NULL
				          constraint beda_stp_chk CHECK(beda_startposition BETWEEN 0.0 AND 100.0),
				      beda_starttext_winkel    integer NULL
				          constraint beda_stwi_chk CHECK(beda_starttext_winkel BETWEEN - 179 AND 180),
				      beda_starttext_abstand   integer NULL
				          constraint beda_stab_chk CHECK(beda_starttext_abstand BETWEEN 1 AND 9999),
				      beda_starttext_x         integer NULL
				          constraint beda_stx_chk CHECK(beda_starttext_x BETWEEN -9999 AND 999999),
				      beda_starttext_y         integer NULL
				          constraint beda_sty_chk CHECK(beda_starttext_y BETWEEN -9999 AND 999999),
				      beda_starttext_breite    integer NULL
				          constraint beda_stb_chk CHECK(beda_starttext_breite BETWEEN 1 AND 9999),
				      beda_starttext_hoehe     integer NULL
				          constraint beda_sth_chk CHECK(beda_starttext_hoehe BETWEEN 1 AND 9999),
				      beda_endkante            varchar(1) NULL
				          constraint beda_ek_chk CHECK(beda_endkante IN(
				              'N',
				              'O',
				              'S',
				              'W'
				          )),
				      beda_endposition         integer NULL
				          constraint beda_ep_chk CHECK(beda_endposition BETWEEN 0.0 AND 100.0),
				      beda_endtext_winkel      integer NULL
				          constraint beda_ewi_chk CHECK(beda_endtext_winkel BETWEEN - 179 AND 180),
				      beda_endtext_abstand     integer NULL
				          constraint beda_eab_chk CHECK(beda_endtext_abstand BETWEEN 1 AND 9999),
				      beda_endtext_x           integer NULL
				          constraint beda_ex_chk CHECK(beda_endtext_x BETWEEN -9999 AND 999999),
				      beda_endtext_y           integer NULL
				          constraint beda_ey_chk CHECK(beda_endtext_y BETWEEN -9999 AND 999999),
				      beda_endtext_breite      integer NULL
				          constraint beda_eb_chk CHECK(beda_endtext_breite BETWEEN 1 AND 9999),
				      beda_endtext_hoehe       integer NULL
				          constraint beda_eh_chk CHECK(beda_endtext_hoehe BETWEEN 1 AND 9999),
				      beda_schriftfarbe        varchar(6) DEFAULT '000000' NULL
				          constraint beda_sf_chk CHECK(length(beda_schriftfarbe)= 6),
				      beda_schriftgroesse      integer NULL
				          constraint beda_sg_chk CHECK(beda_schriftgroesse BETWEEN 1 AND 999),
				          beda_uc              varchar(30) NOT NULL,
				      beda_dc                  varchar(30) NOT NULL,
				      beda_um                  varchar(30) ,
				      beda_dm                  varchar(30),
				  	CONSTRAINT beda_un UNIQUE(beda_diag_id,beda_mode_id),
				      CONSTRAINT beda_diag_fk FOREIGN KEY(beda_diag_id)
				          REFERENCES diagramme(diag_id),
				  	CONSTRAINT beda_mode_fk FOREIGN KEY(beda_mode_id)
				          REFERENCES modellelement(mode_id)
				              ON DELETE CASCADE
				  )
        """);
    dbDDL.dropTable("linie_segment");
    dbDDL.createTable("""
CREATE TABLE linie_segment(
    lise_id          integer primary key autoincrement,
    lise_rhfg        integer NOT NULL,
    lise_beda_id     integer NOT NULL,
    lise_x           integer NOT NULL
        CONSTRAINT ck_beda_beda_schriftfarbe CHECK(lise_x BETWEEN 0 AND 999999) ,
    lise_y           integer NOT NULL
        CONSTRAINT ck_beda_beda_schriftfarbe CHECK(lise_y BETWEEN 0 AND 999999) ,
    lise_linientyp   VARCHAR2(6)NULL
        CONSTRAINT ck_beda_beda_schriftgroesse CHECK(lise_linientyp IN(
            'DADO',
            'DASHED',
            'DOTTED',
            'SOLID'
        )),
		  lise_konnektor   VARCHAR2(1) NULL
		CHECK(lise_konnektor IN(
		'1',
		'M'
		)),
	lise_winkel 	 integer,
    lise_uc       varchar(30) NOT NULL,
    lise_dc           varchar(30) NOT NULL,
    lise_um           varchar(30) ,
    lise_dm           varchar(30),
	CONSTRAINT lise__un UNIQUE(lise_beda_id,lise_rhfg),
	CONSTRAINT lise_beda_fk FOREIGN KEY(lise_beda_id)
	        REFERENCES beziehung_darst(beda_id)
	            ON DELETE CASCADE
)
	          """);
    Projekt.createtable()

    dbDDL.dropTable("geschaeftsbereich");
    dbDDL.createTable("""CREATE TABLE geschaeftsbereich 
				      (
				      gber_id              integer primary key autoincrement,
				      gber_name            VARCHAR(60)NOT NULL,
				      gber_beschreibung   VARCHAR(4000)NULL,
				      gber_zweck           VARCHAR(2000)NULL,
				      gber_uc  VARCHAR(30) not null , 
				       GBER_DC VARCHAR(30)  NOT NULL , 
				       GBER_UM VARCHAR (30),
				      gber_dm VARCHAR(30),
				      CONSTRAINT Bereich_UN UNIQUE (gber_name asc)
				  )""")
    dbDDL.dropTable("bereich_elemdarst");
    dbDDL.createTable("""CREATE TABLE bereich_elemdarst 
				      ( beld_id integer primary key autoincrement,
				       BELD_MELT_ID INTEGER NOT NULL , 
				       BELD_GBER_ID INTEGER NOT NULL , 
				       BELD_BREITE INTEGER NULL , 
				       BELD_HOEHE INTEGER NULL , 
				       BELD_DECKKRAFT INTEGER NULL DEFAULT 100 CHECK ( BELD_DECKKRAFT BETWEEN 0 AND 100 ) , 
				       BELD_FARBE VARCHAR (6) NULL DEFAULT '000000' CHECK ( LENGTH(BELD_FARBE) = 6 ) , 
				       BELD_RANDBREITE INTEGER NULL DEFAULT 1 , 
				       BELD_RANDDECKKRAFT INTEGER NULL DEFAULT 100 CHECK ( BELD_RANDDECKKRAFT BETWEEN 0 AND 100 ) , 
				       BELD_RANDFARBE VARCHAR (6) NULL DEFAULT '000000' CHECK ( LENGTH(BELD_RANDFARBE) = 6 ) , 
				       BELD_SCHRIFTGROESSE INTEGER NULL CHECK ( BELD_SCHRIFTGROESSE BETWEEN 1 AND 999 ) , 
				       BELD_SCHRIFTFARBE VARCHAR (6) NULL DEFAULT '000000' CHECK ( LENGTH(BELD_SCHRIFTFARBE) = 6 ) , 
				      BELD_UC VARCHAR (30) NULL , 
				       BELD_DC VARCHAR (30) NOT NULL , 
				       BELD_UM VARCHAR (30) NULL , 
				       BELD_DM VARCHAR (30) NULL ,
				      CONSTRAINT BELD_UN UNIQUE (beld_melt_id,beld_gber_id),
					  CONSTRAINT beld_mode_fk FOREIGN KEY(beld_melt_id)
					          REFERENCES modellelem_typ(melt_id)
					              ON DELETE CASCADE ,
					  CONSTRAINT beld_gber_fk FOREIGN KEY(beld_gber_id)
	  				          REFERENCES geschaeftsbereich(gber_id)
	  				              ON DELETE CASCADE 
			      )""")

    Dokument.createtable()
    ModelelemDoku.createtable()
    TablEntiMap.createtable()
    AttrTransf.createtable()

#end erstelleInfra