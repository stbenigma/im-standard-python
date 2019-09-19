# -*- coding: latin-1 -*-

from IM_DB import dbConnect,dbDDL
import sqlite3

def erstelleInfra():
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
	foreign key (syno_enti_id) references entitaeten(enti_id)
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
	foreign key (schl_enti_id) references entitaeten(enti_id)
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
        REFERENCES beziehung(bezi_id)
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
    wrtb_num_pheh          varchar(100) ,
    wrtb_bin_inhalttyp        varchar(30)
        CHECK(wrtb_bin_inhalttyp IN(
            'BILD',
            'FILM',
            'GRAPH',
            'TEXT',
            'TON'
        )),
    wrtb_bin_spfo_id          integer,
    wrtb_uc varchar(30),
    wrtb_dc varchar(30),
    wrtb_odm_guid varchar(36),
    wrtb_datatype_ref varchar(40)
    ,foreign key (wrtb_bin_spfo_id) REFERENCES speicherformate(spfo_id)
)    
""");

    dbDDL.dropTable("vorgabewerte");
    dbDDL.createTable("""
CREATE TABLE vorgabewerte(
    vgwt_id               integer NOT NULL primary key autoincrement,
    vgwt_wert              varchar(100) NOT NULL,
    vgwt_sortrhfg          integer NULL,
    vgwt_wrtb_id           integer NOT NULL,
    vgwt_anzeige   varchar(200),
    vgwt_beschr    varchar(4000),
	unique (vgwt_wrtb_id,vgwt_wert),
	foreign key (vgwt_wrtb_id) references wertebereiche(wrtb_id)
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
        REFERENCES entitaet(enti_id),
	CONSTRAINT attr_wrtb_fk	FOREIGN KEY(attr_wrtb_id)        
			REFERENCES wertebereich(wrtb_id),
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
	        REFERENCES entitaet(enti_id) ON DELETE CASCADE
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
	CONSTRAINT bezi_isa_ck2 CHECK((bezi_type = 'ISA' AND bezi_pflicht_assoc_von_zu = 'TRUE')
                                   OR (bezi_type != 'ISA')),
	CONSTRAINT bezi_arc_fk FOREIGN KEY(bezi_arcs_id)
											         REFERENCES arcs(arcs_id),
	CONSTRAINT bezi_enti_fk_von FOREIGN KEY(bezi_enti_id_von)
											         REFERENCES entitaet(enti_id)
											             ON DELETE CASCADE,
	CONSTRAINT bezi_enti_fk_zu FOREIGN KEY(bezi_enti_id_zu)
											         REFERENCES entitaet(enti_id)
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
	        REFERENCES wertebereich(wrtb_id)	
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
	        REFERENCES benudef_eigenschaft(bdeg_id)
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
            'WRTB'
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
    mode_type      varchar(4)NOT NULL
        CHECK(mode_type IN(
            'ATTR',
            'BEZI',
            'BURU',
            'ENTI',
            'WRTB'
        )),
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
	CONSTRAINT mode_arc_fk1 CHECK(mode_type != 'ATTR'
                                  OR(mode_attr_id IS NOT NULL)),
	CONSTRAINT mode_arc_fk2 CHECK(mode_type != 'BEZI'
                                      OR(mode_bezi_id IS NOT NULL)),								  
	CONSTRAINT mode_arc_fk3 CHECK(mode_type != 'BURU'
                                      OR(mode_buru_id IS NOT NULL)),
	CONSTRAINT mode_arc_fk4 CHECK(mode_type != 'ENTI'
                                      OR(mode_enti_id IS NOT NULL)),
	CONSTRAINT mode_arc_fk5 CHECK(mode_type != 'WRTB'
                                      OR(mode_wrtb_id IS NOT NULL)),								  
	CONSTRAINT fkarc_4 CHECK(((mode_buru_id IS NOT NULL)
                                  AND(mode_bezi_id IS NULL)
                                  AND(mode_enti_id IS NULL)
                                  AND(mode_wrtb_id IS NULL)
                                  AND(mode_attr_id IS NULL))
                                 OR((mode_bezi_id IS NOT NULL)
                                    AND(mode_buru_id IS NULL)
                                    AND(mode_enti_id IS NULL)
                                    AND(mode_wrtb_id IS NULL)
                                    AND(mode_attr_id IS NULL))
                                 OR((mode_enti_id IS NOT NULL)
                                    AND(mode_buru_id IS NULL)
                                    AND(mode_bezi_id IS NULL)
                                    AND(mode_wrtb_id IS NULL)
                                    AND(mode_attr_id IS NULL))
                                 OR((mode_wrtb_id IS NOT NULL)
                                    AND(mode_buru_id IS NULL)
                                    AND(mode_bezi_id IS NULL)
                                    AND(mode_enti_id IS NULL)
                                    AND(mode_attr_id IS NULL))
                                 OR((mode_attr_id IS NOT NULL)
                                    AND(mode_buru_id IS NULL)
                                    AND(mode_bezi_id IS NULL)
                                    AND(mode_enti_id IS NULL)
                                    AND(mode_wrtb_id IS NULL))
                                 OR((mode_buru_id IS NULL)
                                    AND(mode_bezi_id IS NULL)
                                    AND(mode_enti_id IS NULL)
                                    AND(mode_wrtb_id IS NULL)
                                    AND(mode_attr_id IS NULL)))
								    CONSTRAINT mode_attr_fk_ist FOREIGN KEY(mode_attr_id)
								           REFERENCES attributes(attr_id)
								               ON DELETE CASCADE,
								    CONSTRAINT mode_bezi_fk FOREIGN KEY(mode_bezi_id)
								           REFERENCES beziehung(bezi_id)
								   		ON DELETE CASCADE,
								    CONSTRAINT mode_enti_fk_ist FOREIGN KEY(mode_enti_id)
								           REFERENCES entitaet(enti_id)
								               ON DELETE CASCADE,
								    CONSTRAINT mode_wrtb_fk_ist FOREIGN KEY(mode_wrtb_id)
								   		           REFERENCES wertebereich(wrtb_id)
								   		               ON DELETE CASCADE,
								    CONSTRAINT mode_orge_fk_verantw FOREIGN KEY(mode_orge_id)
								           REFERENCES org_einh(orge_id),
								    CONSTRAINT mode_melt_fk_verantw FOREIGN KEY(mode_melt_id)
								           REFERENCES modellelem_typ(melt_id)
)
""")

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

#    dbDDL.dropTable("arc")
#    dbDDL.createTable("""
#""")
#end erstelleInfra