# -*- coding: latin-1 -*-

from IM_DB import dbDDL,dbDML


def erstelleInfra():
    #erlaube alles droppen

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
    enti_enti_id integer
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

    dbDDL.dropTable("datatypes");
    dbDDL.createTable("""
CREATE TABLE datatypes(
    daty_id         integer NOT NULL primary key autoincrement,
    daty_name       VARCHAR2(60)NOT NULL unique,
    daty_grundtyp   VARCHAR2(6)NOT NULL
        CHECK(daty_grundtyp IN(
            'BIN',
            'NUM',
            'TEXT',
            'ZPKT'
        )),
    daty_odm_guid       VARCHAR2(36)
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
    bezi_arcs_id                    integer NULL,
	bezi_odm_guid		varchar(36),bezi_name varchar(100),
        bezi_uc                        varchar(30) NOT NULL,
    bezi_dc                        varchar(30) NOT NULL,
    bezi_um                        varchar(30) NULL,
    bezi_dm                        varchar(30) NULL,
    bezi_source_enti_guid          VARCHAR2(36) NULL,
    bezi_target_enti_guid          VARCHAR2(36) NULL,
	CONSTRAINT bezi_isa_ck2 CHECK((bezi_type = 'ISA' AND bezi_pflicht_assoc_von_zu = 'TRUE')
                                   OR (bezi_type != 'ISA')),
	CONSTRAINT bezi_arc_fk FOREIGN KEY(bezi_arcs_id)
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
            'SYNO'
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
    mode_syno_id   integer NULL,
    mode_wrtb_id   integer NULL,
    mode_attr_id   integer NULL,
    mode_buru_id   integer NULL,
    mode_bezi_id   integer NULL,
    mode_enti_id   integer NULL,
    mode_orge_id   integer NULL,    
    mode_melt_id   integer NOT NULL,
    mode_uc        varchar(30 )NOT NULL,
    mode_dc        varchar(30)NOT NULL,
    mode_um        varchar(30 )NULL,
    mode_dm        varchar(30)NULL,
	CONSTRAINT mode_uk UNIQUE(mode_wrtb_id,
	                                  mode_attr_id,
	                                  mode_buru_id,
	                                  mode_enti_id,
	                                  mode_bezi_id),
	CONSTRAINT fkarc_4 CHECK(((mode_buru_id IS NOT NULL)
                                  AND(mode_bezi_id IS NULL)
                                  AND(mode_enti_id IS NULL)
                                  AND(mode_wrtb_id IS NULL)
                                  AND(mode_attr_id IS NULL)
                                  AND(mode_syno_id IS NULL))
                                 OR((mode_bezi_id IS NOT NULL)
                                    AND(mode_buru_id IS NULL)
                                    AND(mode_enti_id IS NULL)
                                    AND(mode_wrtb_id IS NULL)
                                    AND(mode_attr_id IS NULL)
                                  AND(mode_syno_id IS NULL))
                                 OR((mode_enti_id IS NOT NULL)
                                    AND(mode_buru_id IS NULL)
                                    AND(mode_bezi_id IS NULL)
                                    AND(mode_wrtb_id IS NULL)
                                    AND(mode_attr_id IS NULL)
                                  AND(mode_syno_id IS NULL))
                                 OR((mode_wrtb_id IS NOT NULL)
                                    AND(mode_buru_id IS NULL)
                                    AND(mode_bezi_id IS NULL)
                                    AND(mode_enti_id IS NULL)
                                    AND(mode_attr_id IS NULL)
                                  AND(mode_syno_id IS NULL))
                                 OR((mode_attr_id IS NOT NULL)
                                    AND(mode_buru_id IS NULL)
                                    AND(mode_bezi_id IS NULL)
                                    AND(mode_enti_id IS NULL)
                                    AND(mode_wrtb_id IS NULL)
                                  AND(mode_syno_id IS NULL))
                                 OR((mode_buru_id IS NULL)
                                    AND(mode_bezi_id IS NULL)
                                    AND(mode_enti_id IS NULL)
                                    AND(mode_wrtb_id IS NULL)
                                    AND(mode_attr_id IS NULL)
                                  AND(mode_syno_id IS NOT NULL)))
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
								    CONSTRAINT mode_melt_fk_verantw FOREIGN KEY(mode_melt_id)
								           REFERENCES modellelem_typ(melt_id)
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

    dbDDL.dropTable("sprachen")
    dbDDL.createTable("""CREATE TABLE sprachen(
    spra_id                integer primary key autoincrement,
    spra_iso_name          varchar(60) NOT NULL,
    spra_iso_code2         CHAR(2) NOT NULL,
    spra_iso_code3         CHAR(3) NOT NULL,
    spra_ist_textsprache   varchar(5) NOT NULL,
    spra_ist_modellsprache   varchar(5) NOT NULL,
    spra_spra_id           integer,
    spra_uc                varchar(30) NOT NULL,
    spra_dc                varchar(30) NOT NULL,
    spra_um                varchar(30) ,
    spra_dm                varchar(30),
    constraint spra_txt_bool CHECK(spra_ist_textsprache IN(
        'FALSE',
        'TRUE'
    )),
    constraint spra_mod_bool CHECK(spra_ist_modellsprache IN(
        'FALSE',
        'TRUE'
    )),
    constraint spra_iso3_low CHECK(spra_iso_code3 = lower(spra_iso_code3)),
    constraint spra_iso2_low CHECK(spra_iso_code2 = lower(spra_iso_code2)),
	constraint spra_iso_uk unique (spra_iso_name),
	constraint spra_iso2_uk unique (spra_iso_code2),
	constraint spra_iso3_uk unique (spra_iso_code3)
)"""
    )

    dbDDL.dropTable("sprachtexte")
    dbDDL.createTable("""CREATE TABLE sprachtexte(
    sptx_id           integer primary key autoincrement,
	sptx_attrname	  varchar(30) NOT NULL,
    sptx_text         varchar(4000) ,
    sptx_spra_id      integer,
    sptx_mode_id      integer NOT NULL,
    sptx_uc           varchar(30) NOT NULL,
    sptx_dc           varchar(30) NOT NULL,
    sptx_um           varchar(30) ,
    sptx_dm           varchar(30),
	constraint sptx_attrnameUC check(sptx_attrname = upper(sptx_attrname)),
	constraint sptx_uk unique (sptx_attrname,sptx_spra_id,sptx_mode_id),
    CONSTRAINT sptx_mode_fk FOREIGN KEY(sptx_mode_id)
									   REFERENCES modellelement(mode_id),
	CONSTRAINT sptx_spra_fk FOREIGN KEY(sptx_spra_id)
									   REFERENCES sprachen(spra_id)	
    )
    """)
    #    dbDDL.dropTable("arc")
    #    dbDDL.createTable("""
    # """)

    dbDDL.dropView("SUPERENTI");
    dbDDL.createTable("""create view SUPERENTI AS select ae.enti_id super_enti_id,ae.enti_name super_enti_name
               ,e1.enti_id sub_enti_id,e1.enti_name sub_enti_name
      from arcs
      join entitaeten as ae on ae.enti_id = arcs_enti_id 
      join (select bezi_arcs_id,count(*) alleanz
           , SUM(case when bezi_type in ('ISA','1:1') then 1 else 0 end) isaanz
           , SUM(case bezi_pflicht_assoc_von_zu when 'TRUE' then 1 else 0 end) nnvonanz
           , SUM(case bezi_pflicht_assoc_zu_von when 'TRUE' then 1 else 0 end) nnzuanz
            from  beziehungen
            where bezi_type in ('ISA','1:1') 
            group by bezi_arcs_id) as st
            on st.bezi_arcs_id = arcs_id AND alleanz = isaanz and alleanz = nnvonanz and alleanz = nnzuanz
      join beziehungen b1 on b1.bezi_arcs_id = arcs_id
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
    beda_liniefarbe          varchar(6) DEFAULT '000000' NULL
        CHECK(length(beda_liniefarbe)= 6),
    beda_liniedeckkraft      integer DEFAULT 100 NULL
        CHECK(beda_liniedeckkraft BETWEEN 0 AND 100),
    beda_startkante          varchar(1) NULL
        CHECK(beda_startkante IN(
            'N',
            'O',
            'S',
            'W'
        )),
    beda_startposition       integer NULL
        CHECK(beda_startposition BETWEEN 0.0 AND 100.0),
    beda_starttext_winkel    integer NULL
        CHECK(beda_starttext_winkel BETWEEN - 179 AND 180),
    beda_starttext_abstand   integer NULL
        CHECK(beda_starttext_abstand BETWEEN 1 AND 9999),
    beda_starttext_x         integer NULL
        CHECK(beda_starttext_x BETWEEN 0 AND 999999),
    beda_starttext_y         integer NULL
        CHECK(beda_starttext_y BETWEEN 0 AND 999999),
    beda_starttext_breite    integer NULL
        CHECK(beda_starttext_breite BETWEEN 1 AND 9999),
    beda_starttext_hoehe     integer NULL
        CHECK(beda_starttext_hoehe BETWEEN 1 AND 9999),
    beda_endkante            varchar(1) NULL
        CHECK(beda_endkante IN(
            'N',
            'O',
            'S',
            'W'
        )),
    beda_endposition         integer NULL
        CHECK(beda_endposition BETWEEN 0.0 AND 100.0),
    beda_endtext_winkel      integer NULL
        CHECK(beda_endtext_winkel BETWEEN - 179 AND 180),
    beda_endtext_abstand     integer NULL
        CHECK(beda_endtext_abstand BETWEEN 1 AND 9999),
    beda_endtext_x           integer NULL
        CHECK(beda_endtext_x BETWEEN 0 AND 999999),
    beda_endtext_y           integer NULL
        CHECK(beda_endtext_y BETWEEN 0 AND 999999),
    beda_endtext_breite      integer NULL
        CHECK(beda_endtext_breite BETWEEN 1 AND 9999),
    beda_endtext_hoehe       integer NULL
        CHECK(beda_endtext_hoehe BETWEEN 1 AND 9999),
    beda_schriftfarbe        varchar(6) DEFAULT '000000' NULL
        CHECK(length(beda_schriftfarbe)= 6),
    beda_schriftgroesse      integer NULL
        CHECK(beda_schriftgroesse BETWEEN 1 AND 999),
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
    dbDDL.dropTable("projekt");
    dbDDL.createTable("""CREATE TABLE projekt(
    proj_id            integer primary key autoincrement,
    proj_name          VARCHAR(60) NOT NULL,
    proj_uc            VARCHAR(30) NOT NULL,
    proj_dc            VARCHAR(30) NOT NULL,
    proj_sprachen      VARCHAR(60),
    proj_akt_sprache   VARCHAR2(2),
	CONSTRAINT proj__un UNIQUE(proj_name)
    )"""
    );

#    dbDDL.dropTable("");
#    dbDDL.createTable("""

#end erstelleInfra