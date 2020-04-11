# -*- coding: latin-1 -*-

from IM_DB import dbDDL
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

    dbDDL.dropTable("entitaeten");
    dbDDL.createTable("""
CREATE TABLE entitaeten(
    enti_id                 integer NOT NULL primary key autoincrement,
    enti_odm_guid varchar(36),
    enti_augb_id            integer ,
    enti_tech_name          varchar(60) unique,
    enti_name       varchar(60) NOT NULL unique,
    enti_beschr     varchar(4000) ,
    enti_tooltip    varchar(100) ,
    enti_kurzname   varchar(20) ,
    enti_prefix             varchar(10),
    enti_beispiele          varchar(4000),
    enti_erw_tupel         varchar(10)
        CHECK(enti_erw_tupel IN(
            '1 Mio',
            '100',
            '10000',
            '>100 Mio'
        )),
    enti_uc varchar(30),
    enti_dc varchar(30),
    enti_enti_guid varchar(80),
    enti_enti_id integer,
    enti_category_guid varchar(80)
    )    
    """);

    dbDDL.dropTable("synonyme");
    dbDDL.createTable("""
CREATE TABLE synonyme(
    syno_id             integer NOT NULL primary key autoincrement,
    syno_name   		varchar(200),
    syno_enti_id        integer NOT NULL,
	unique(syno_name,syno_enti_id),
	foreign key (syno_enti_id) references entitaeten(enti_id) ON DELETE CASCADE
)
    """);

    dbDDL.dropTable("schluessel");
    dbDDL.createTable("""
CREATE TABLE schluessel(
    schl_id        integer NOT NULL primary key autoincrement,
    schl_laufnr    integer NOT NULL,
	schl_name	varchar(60),
	schl_odm_guid		varchar(36),
    schl_uc varchar(30),
    schl_dc varchar(30),
    schl_enti_id   integer NOT NULL,
	unique (schl_enti_id,schl_laufnr),
	foreign key (schl_enti_id) references entitaeten(enti_id) ON DELETE CASCADE
)    """);

    dbDDL.dropTable("schluesselelement");
    dbDDL.createTable("""CREATE TABLE schluesselelement(
    scel_id        integer NOT NULL primary key autoincrement,
    scel_schl_id   integer NOT NULL,
    scel_attr_id   integer ,
    scel_bezi_id   integer ,
    scel_uc         varchar(30) NOT NULL,
    scel_dc        varchar(30) NOT NULL,
    scel_um        varchar(30),
    scel_dm        varchar(30),
	UNIQUE(scel_schl_id,scel_attr_id,scel_bezi_id),
	CONSTRAINT scel_element_ck CHECK((scel_attr_id IS NOT NULL
                                   AND scel_bezi_id IS NULL)
                                  OR(scel_attr_id IS NULL
                                     AND scel_bezi_id IS NOT NULL)),
	FOREIGN KEY(scel_attr_id)
        REFERENCES attributes(attr_id)
            ON DELETE CASCADE,
	FOREIGN KEY(scel_bezi_id)
        REFERENCES beziehungen(bezi_id)
            ON DELETE CASCADE,
	FOREIGN KEY(scel_schl_id)
        REFERENCES schluessel(schl_id)
            ON DELETE CASCADE
		)""");
    dbDDL.dropTable("wertebereiche");
    dbDDL.createTable("""
CREATE TABLE wertebereiche(
    wrtb_id                   integer NOT NULL primary key autoincrement,
    wrtb_business_rule        varchar(4000),
    wrtb_name         varchar(60) NOT NULL unique,
    wrtb_beschr       varchar(4000) ,
    wrtb_typ                  varchar(4)NOT NULL
        CHECK(wrtb_typ IN(
            'BIN',
            'GRP',
            'LOV',
            'NUM',
            'TEXT',
            'ZPKT'
        )),
    wrtb_zpkt_minwert         varchar(30),
    wrtb_zpkt_maxwert         varchar(30),
    wrtb_zpkt_granularitaet   varchar(15)
        CHECK(wrtb_zpkt_granularitaet IN(
            'JAHR',
            'MILLISEKUNDE',
            'MINUTE',
            'MONAT',
            'QUARTAL',
            'SEKUNDE',
            'SEMESTER',
            'STUNDE',
            'TAG',
            'WOCHE'
        )),
    wrtb_text_maxlng          integer ,
    wrtb_text_syntaxregel     varchar(4000),
    wrtb_num_maxwert          integer ,
    wrtb_num_minwert          integer ,
    wrtb_num_vorkstellen      integer ,
    wrtb_num_nachkstellen     integer DEFAULT 0,
    wrtb_num_rundng_einh      integer 
        CHECK(wrtb_num_rundng_einh IN(
            0.001,
            0.01,
            0.05,
            0.1,
            0.25,
            0.5,
            1,
            10,
            100,
            1000
        )),
    wrtb_num_pheh_id          integer ,
    wrtb_bin_inhalttyp        varchar(30)
        CHECK(wrtb_bin_inhalttyp IN(
            'BILD',
            'FILM',
            'GRAPH',
            'TEXT',
            'TON'
        )),
    wrtb_bin_spfo_id          varchar(100),
	wrtb_odm_guid		varchar(36),
    wrtb_uc         varchar(30) NOT NULL,
    wrtb_dc        varchar(30) NOT NULL,
    wrtb_um        varchar(30),
    wrtb_dm        varchar(30),
    wrtb_datatype_ref varchar(40)
)
""");

    dbDDL.dropTable("wertebereichgruppen");
    dbDDL.createTable("""
CREATE TABLE wertebereichgruppen
    (
    wbgr_id               integer NOT NULL primary key autoincrement,
    wbgr_name             VARCHAR(60)NOT NULL,
    wbgr_beschr           VARCHAR(4000)NULL,
    wbgr_wrtb_id_gruppe   integer NOT NULL ,
     WBGR_WRTB_ID_MEMBER integer NOT NULL , 
	 wbgr_type_ref	varchar(40),
     WBGR_UC VARCHAR (30) NOT NULL , 
     WBGR_DC VARCHAR (30) NOT NULL , 
     WBGR_UM VARCHAR (30)    null,
      wbgr_dm VARCHAR (30) null
,CONSTRAINT WBGR_WRTB_UK UNIQUE (wbgr_wrtb_id_gruppe ,wbgr_name )
,FOREIGN KEY(wbgr_wrtb_id_gruppe)
        REFERENCES wertebereich(wrtb_id) ON DELETE CASCADE
,FOREIGN KEY(wbgr_wrtb_id_member)
        REFERENCES wertebereich(wrtb_id) 
	)
;
""");

    dbDDL.dropTable("vorgabewerte");
    dbDDL.createTable("""
CREATE TABLE vorgabewerte(
    vgwt_id               integer NOT NULL primary key autoincrement,
	vgwt_guid varchar(40),
    vgwt_wert              VARCHAR(100) NOT NULL,
    vgwt_sortrhfg          integer NULL,
    vgwt_wrtb_id           integer NOT NULL,
    vgwt_anzeige   varchar(200),
    vgwt_beschr    varchar(4000),
    vgwt_uc         varchar(30) NOT NULL,
    vgwt_dc        varchar(30) NOT NULL,
    vgwt_um        varchar(30),
    vgwt_dm        varchar(30),
	unique (vgwt_wrtb_id,vgwt_wert),
	foreign key (vgwt_wrtb_id) references wertebereiche(wrtb_id) ON DELETE CASCADE
)
""");

    dbDDL.dropTable("attributes")
    dbDDL.createTable("""
CREATE TABLE attributes(
    attr_id                integer NOT NULL primary key autoincrement,
    attr_enti_id           integer ,
    attr_bezi_id           integer,
    attr_wrtb_id           integer NOT NULL,
    attr_tech_name         varchar(60)NOT NULL,
    attr_anzname   varchar(100) ,
    attr_tooltip   varchar(100) ,
    attr_beschr    varchar(2000) ,
    attr_business_rule     varchar(4000),
    attr_anz_rhflg         integer ,
    attr_deskriptor        varchar(5) default 'FALSE' NOT NULL
        CHECK(attr_deskriptor IN(
            'FALSE',
            'TRUE'
        )),
    attr_pflichtattr       varchar(5) default 'FALSE' NOT NULL
        CHECK(attr_pflichtattr IN(
            'FALSE',
            'TRUE'
        )),
    attr_historisiert      varchar(5) default 'FALSE' NOT NULL
        CHECK(attr_historisiert IN(
            'FALSE',
            'TRUE'
        )),
    attr_wiederholt        varchar(5) default 'FALSE' NOT NULL
        CHECK(attr_wiederholt IN(
            'FALSE',
            'TRUE'
        )),
    attr_sprachabhaengig   varchar(5) default 'FALSE' NOT NULL
        CHECK(attr_sprachabhaengig IN(
            'FALSE',
            'TRUE'
        )),
    attr_verschluesselt    varchar(5) default 'FALSE' NOT NULL
        CHECK(attr_verschluesselt IN(
            'FALSE',
            'TRUE'
        )),
    attr_odm_guid		varchar(36),	
    attr_uc                varchar(30 )NOT NULL,
    attr_dc                varchar(30 ),
    attr_um                varchar(30),
    attr_dm                varchar(30 ),
    UNIQUE(attr_enti_id, attr_tech_name),
	CONSTRAINT attr_arc_fk CHECK((attr_enti_id is null and attr_bezi_id is not null) 
								or (attr_enti_id is not null and attr_bezi_id is null)),
 	CONSTRAINT attr_enti_fk FOREIGN KEY(attr_enti_id)
        REFERENCES entitaeten(enti_id),
	CONSTRAINT attr_wrtb_fk	FOREIGN KEY(attr_wrtb_id)        
			REFERENCES wertebereiche(wrtb_id),
	CONSTRAINT attr_bezi_fk FOREIGN KEY(attr_bezi_id)
		        REFERENCES beziehungen(bezi_id)
)
   """);

    dbDDL.dropTable("arcs")
    dbDDL.createTable("""
CREATE TABLE arcs(
    arcs_id        integer  not null primary key autoincrement,
    arcs_name      VARCHAR2(60) NOT NULL,
    arcs_enti_id   integer NOT NULL,
	arcs_odm_guid		varchar(36),
    arcs_uc        VARCHAR2(30) NOT NULL,
    arcs_dc        varchar(30) NOT NULL,
    arcs_um        VARCHAR2(30) NULL,
    arcs_dm        varchar(30) NULL,
	UNIQUE(arcs_enti_id,arcs_name),
	CONSTRAINT arcs_enti_fk FOREIGN KEY(arcs_enti_id)
	        REFERENCES entitaeten(enti_id) ON DELETE CASCADE
)
""");

    dbDDL.dropTable("beziehungen")
    dbDDL.createTable("""
CREATE TABLE beziehungen(
    bezi_id                        integer NOT NULL primary key autoincrement,
    bezi_type                      varchar(3)NOT NULL
           CHECK(bezi_type IN(
               '1:1',
               'ISA',
               'M:1',
               'M:N'
           )),
	bezi_enti_id_von               integer NOT NULL,
    bezi_assoc_von_zu      varchar(100) NULL,
    bezi_pflicht_assoc_von_zu      varchar(5) NOT NULL
        CHECK(bezi_pflicht_assoc_von_zu IN(
            'FALSE',
            'TRUE'
        )),
    bezi_hist_von_zu               varchar(5) NOT NULL
        CHECK(bezi_hist_von_zu IN(
            'FALSE',
            'TRUE'
        )),
    bezi_enti_id_zu                integer NOT NULL,
    bezi_assoc_zu_von      varchar(100)  NULL,
    BEZI_PFLICHT_ASSOC_ZU_VON   varchar(5) NOT NULL
        CHECK(BEZI_PFLICHT_ASSOC_ZU_VON IN(
            'FALSE',
            'TRUE'
        )),
    bezi_hist_zu_von               varchar(5) NOT NULL
        CHECK(bezi_hist_zu_von IN(
            'FALSE',
            'TRUE'
        )),
    bezi_von_arcs_id                    integer NULL,
    bezi_zu_arcs_id                    integer NULL,
	bezi_odm_guid		varchar(36),bezi_name varchar(100),
        bezi_uc                        varchar(30) NOT NULL,
    bezi_dc                        varchar(30) NOT NULL,
    bezi_um                        varchar(30) NULL,
    bezi_dm                        varchar(30) NULL,
    bezi_source_enti_guid          VARCHAR2(36) NULL,
    bezi_target_enti_guid          VARCHAR2(36) NULL,
	CONSTRAINT bezi_isa_ck2 CHECK((bezi_type = 'ISA' AND bezi_pflicht_assoc_von_zu = 'TRUE')
                                   OR (bezi_type != 'ISA')),
	CONSTRAINT bezi_von_arc_fk FOREIGN KEY(bezi_von_arcs_id)
							REFERENCES arcs(arcs_id),
	CONSTRAINT bezi_zu_arc_fk FOREIGN KEY(bezi_zu_arcs_id)
							REFERENCES arcs(arcs_id),
	CONSTRAINT bezi_enti_fk_von FOREIGN KEY(bezi_enti_id_von)
											         REFERENCES entitaeten(enti_id)
											             ON DELETE CASCADE,
	CONSTRAINT bezi_enti_fk_zu FOREIGN KEY(bezi_enti_id_zu)
											         REFERENCES entitaeten(enti_id)
											             ON DELETE CASCADE
)
""")


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

    dbDDL.dropTable("modellelem_typ")
    dbDDL.createTable("""
CREATE TABLE modellelem_typ(
    melt_id                  integer NOT NULL primary key autoincrement,
    melt_kurzname            varchar(4)NOT NULL
        CHECK(melt_kurzname IN(
   'ATTR',
   'BEZI',
   'BURU',
   'ENTI',
   'WRTB',
   'TABL',
   'SCHA',
   'SCHN',
   'SYNO',
   'ORGE'
        )),
    melt_name                varchar(60 )NOT NULL,
        melt_uc                  varchar(30 )NOT NULL,
    melt_dc                  varchar(30)NOT NULL,
    melt_um                  varchar(30 )NULL,
    melt_dm                  varchar(30)NULL,
	CONSTRAINT melt_un UNIQUE(melt_kurzname),
	CONSTRAINT melt_un2 UNIQUE(melt_name)
) 
""")

    dbDDL.dropTable("modellelement")
    dbDDL.createTable("""
CREATE TABLE modellelement(
    mode_id        integer NOT NULL primary key autoincrement,
    mode_melt_id   integer NULL,
    mode_syno_id   integer NULL,
    mode_wrtb_id   integer NULL,
    mode_attr_id   integer NULL,
    mode_buru_id   integer NULL,
    mode_bezi_id   integer NULL,
    mode_enti_id   integer NULL,
    mode_orge_id   integer NULL,    
    mode_tabl_id  integer NULL,
    mode_scha_id  integer NULL,    
    mode_schn_id  integer NULL,    
    mode_uc        varchar(30 )NOT NULL,
    mode_dc        varchar(30)NOT NULL,
    mode_um        varchar(30 )NULL,
    mode_dm        varchar(30)NULL,
	CONSTRAINT mode_uk UNIQUE(mode_wrtb_id,
	       mode_attr_id,
	       mode_buru_id,
	       mode_enti_id,
	       mode_bezi_id,mode_scha_id,mode_tabl_id,mode_schn_id),
		   CONSTRAINT fkarc_4 CHECK (case WHEN mode_buru_id IS NULL THEN 0 else 1 end
		   	 						+case WHEN mode_enti_id IS NULL THEN 0 else 1 end	
		   	 						+case WHEN mode_tabl_id IS NULL THEN 0 else 1 end	
		   	 						+case WHEN mode_scha_id IS NULL THEN 0 else 1 end	
		   	 						+case WHEN mode_syno_id IS NULL THEN 0 else 1 end	
		   	 						+case WHEN mode_bezi_id IS NULL THEN 0 else 1 end	
		   	 						+case WHEN mode_wrtb_id IS NULL THEN 0 else 1 end	
		   	 						+case WHEN mode_attr_id IS NULL THEN 0 else 1 end	
		   	 						+case WHEN mode_orge_id IS NULL THEN 0 else 1 end	
		   	 						+case WHEN mode_schn_id IS NULL THEN 0 else 1 end	
									= 1
								),
		CONSTRAINT mode_syno_fk_ist FOREIGN KEY(mode_syno_id)
	  REFERENCES synonyme(syno_id)
	      ON DELETE CASCADE,
	    CONSTRAINT mode_attr_fk_ist FOREIGN KEY(mode_attr_id)
	  REFERENCES attributes(attr_id)
	      ON DELETE CASCADE,
	    CONSTRAINT mode_bezi_fk FOREIGN KEY(mode_bezi_id)
	  REFERENCES beziehungen(bezi_id)
	   	ON DELETE CASCADE,
	    CONSTRAINT mode_enti_fk_ist FOREIGN KEY(mode_enti_id)
	  REFERENCES entitaeten(enti_id)
	      ON DELETE CASCADE,
	    CONSTRAINT mode_wrtb_fk_ist FOREIGN KEY(mode_wrtb_id)
	   	  REFERENCES wertebereiche(wrtb_id)
	   	      ON DELETE CASCADE,
	CONSTRAINT MODE_SCHA_FK FOREIGN KEY ( MODE_SCHA_ID) 
	      REFERENCES SCHNITTSTELLE_ATTR (SCHA_ID ) 
	      ON DELETE CASCADE ,
	CONSTRAINT MODE_TABL_FK FOREIGN KEY ( MODE_TABL_ID) 
	  	      REFERENCES TABELLE ( TABL_ID ) 
	  	      ON DELETE CASCADE ,
	CONSTRAINT MODE_SCHN_FK FOREIGN KEY ( MODE_SCHN_ID) 
		  	      REFERENCES schnittstelle ( schn_ID ) 
		  	      ON DELETE CASCADE ,
	    CONSTRAINT mode_melt_fk_verantw FOREIGN KEY(mode_melt_id)
	  REFERENCES modellelem_typ(melt_id)
	  		ON DELETE CASCADE 
)
""")
#  CONSTRAINT mode_orge_fk_verantw FOREIGN KEY(mode_orge_id) REFERENCES org_einh(orge_id),

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
           , SUM(case bezi_pflicht_assoc_von_zu when 'TRUE' then 1 else 0 end) nnvonanz
           , SUM(case bezi_pflicht_assoc_zu_von when 'TRUE' then 1 else 0 end) nnzuanz
            from   (select case when bezi_von_arcs_id is null then bezi_zu_arcs_id else bezi_von_arcs_id end bezi_arcs_id
                        , bezi_pflicht_assoc_von_zu
                        , bezi_pflicht_assoc_zu_von
                   from beziehungen
                   where bezi_type in ('ISA', '1:1')
                )
            group by bezi_arcs_id) as st
            on st.bezi_arcs_id = arcs_id AND  alleanz = nnvonanz and alleanz = nnzuanz
      join beziehungen b1 on b1.bezi_von_arcs_id = arcs_id or b1.bezi_zu_arcs_id = arcs_id
      join entitaeten e1 on e1.enti_id = b1.bezi_enti_id_von  
    order by ae.enti_name""")


    dbDDL.dropView("SPRAATTR");
    dbDDL.createTable("""
            create view spraattr as
	        select sptx_text,spra_id,spra_iso_code2,sptx_mode_id,sptx_attrname
	          from sprachtexte 
	          join sprachen on spra_id = sptx_spra_id
	          """);

    dbDDL.dropTable("diagrammtypen");
    dbDDL.createTable("""
CREATE TABLE diagrammtypen(
    diat_id    integer primary key autoincrement,
    diat_bez   varchar(100) NOT NULL,
     diat_uc varchar(30) NOT NULL,
    diat_dc    varchar(30) NOT NULL,
    diat_um    varchar(30) ,
    diat_dm    varchar(30),
	CONSTRAINT diat_un UNIQUE(diat_bez)
)	          """);
    dbDDL.dropTable("diagramme");
    dbDDL.createTable("""
CREATE TABLE diagramme(
    diag_id      integer primary key autoincrement,
    diag_name      varchar(60) NOT NULL,
    diag_diat_id   integer NOT NULL,
    diag_odm_guid       varchar(36),
    diag_legendx       integer,
    diag_legendy       integer,
     diag_uc    varchar(30) NOT NULL,
    diag_dc        varchar(30) NOT NULL,
    diag_um        varchar(30) ,
    diag_dm        varchar(30),
	CONSTRAINT diag__un UNIQUE(diag_name),
	CONSTRAINT diag_diat_fk FOREIGN KEY(diag_diat_id)
									   REFERENCES diagrammtypen(diat_id)
)	          """);
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

    dbDDL.dropTable("TRANSF_USAGE");
    dbDDL.createTable("""
  CREATE TABLE TRANSF_USAGE 
      (
       TFUS_ID integer primary key autoincrement , 
       TFUS_ATTF_ID integer NOT NULL , 
       TFUS_ATTR_ID integer NULL , 
       TFUS_SCHA_ID integer NULL , 
       TFUS_UC VARCHAR (30) NOT NULL , 
       TFUS_DC VARCHAR (30) NOT NULL , 
       TFUS_UM VARCHAR (30) NULL , 
       TFUS_DM VARCHAR (30) NULL ,
       CONSTRAINT FKArc_7 CHECK ( 
          (  (TFUS_SCHA_ID IS NOT NULL) AND   (TFUS_ATTR_ID IS NULL) ) OR 
          (  (TFUS_ATTR_ID IS NOT NULL) AND   (TFUS_SCHA_ID IS NULL) )  ) ,
       CONSTRAINT TFUS__UN UNIQUE  (TFUS_ATTF_ID , TFUS_ATTR_ID , TFUS_SCHA_ID )
	   ,CONSTRAINT TFUS_ATTF_FK FOREIGN KEY (TFUS_ATTF_ID) 
	      REFERENCES ATTR_TRANSF (ATTF_ID ) 
	   ,CONSTRAINT TFUS_ATTR_FK FOREIGN KEY (TFUS_ATTR_ID) 
	      REFERENCES ATTRIBUTES (ATTR_ID ) 
	      ,CONSTRAINT TFUS_SCHA_FK FOREIGN KEY (TFUS_SCHA_ID) 
	         REFERENCES SCHNITTSTELLE_ATTR (SCHA_ID ) 
      )
    """)
    dbDDL.dropTable("ATTR_TRANSF");
    dbDDL.createTable("""
 CREATE TABLE ATTR_TRANSF 
      (
       ATTF_ID integer primary key autoincrement,
       ATTF_RICHTUNG VARCHAR (7) NOT NULL CHECK ( ATTF_RICHTUNG IN ('INBOUND', 'OUTBOUND') ) , 
       ATTF_TRANSF_FORMEL VARCHAR (4000) NULL , 
       ATTF_AUSLOESEART VARCHAR (10) NULL CHECK ( ATTF_AUSLOESEART IN ('MANUELL', 'PERIODE', 'ZPKT') ) , 
       ATTF_AUSLOESEPERIOD integer NULL , 
       ATTF_SCHA_ID integer NULL , 
       ATTF_ATTR_ID integer NULL , 
       ATTF_UC VARCHAR (30)  , 
       ATTF_DC VARCHAR (30)  , 
       ATTF_UM VARCHAR (30) NULL , 
       ATTF_DM VARCHAR (30)  NULL , 
       CONSTRAINT ATTF_CHK CHECK ((ATTF_SCHA_ID IS NULL AND ATTF_ATTR_ID IS NOT NULL AND ATTF_RICHTUNG = 'INBOUND')
   						   OR (ATTF_SCHA_ID IS NOT NULL AND ATTF_ATTR_ID IS NULL AND ATTF_RICHTUNG = 'OUTBOUND'))
		,CONSTRAINT ATTR_UN UNIQUE (ATTF_RICHTUNG , ATTF_SCHA_ID , ATTF_ATTR_ID )
 	   ,CONSTRAINT ATTF_ATTR_FK FOREIGN KEY (ATTF_ATTR_ID) 
 	      REFERENCES ATTRIBUTES (ATTR_ID ) 
 	      ON DELETE CASCADE 
 	   ,CONSTRAINT ATTF_SCHA_FK FOREIGN KEY (ATTF_SCHA_ID) 
 	      REFERENCES SCHNITTSTELLE_ATTR (SCHA_ID ) 
 	      ON DELETE CASCADE 
 	      )
 	          """)

#    dbDDL.dropTable("");
#    dbDDL.createTable("""""")

#end erstelleInfra