create table LANGUAGES
(
	LANG_ID INTEGER not null
		primary key autoincrement,
	LANG_ISO_NAME VARCHAR(60)
		constraint LANG_ISO_NAME_UN
			unique,
	LANG_ISO_CODE2 CHAR(2) not null
		constraint LANG_ISO_CODE2_UN
			unique,
	LANG_ISO_CODE3 CHAR(3) not null
		constraint LANG_ISO_CODE3_UN
			unique,
	LANG_IS_TEXT_LANG VARCHAR(5) not null,
	LANG_IS_BASE_LANG VARCHAR(5) not null,
	LANG_LANG_ID integer
		references LANGUAGES (lang_id)
			on delete set null,
	LANG_UC VARCHAR(30),
	LANG_DC VARCHAR(30) not null,
	LANG_UM VARCHAR(30),
	LANG_DM VARCHAR(30),
	check (LANG_IS_BASE_LANG IN ('FALSE', 'TRUE')),
	check (LANG_IS_TEXT_LANG IN ('FALSE', 'TRUE')),
	constraint LANG_ISO2_CHK
		check (LANG_ISO_CODE2 = lower(LANG_ISO_CODE2)),
	constraint LANG_ISO3_CHK
		check (LANG_ISO_CODE3 = lower(LANG_ISO_CODE3))
);

create table MODELELEM_TYPE
(
	MELT_ID INTEGER not null
		primary key autoincrement,
	MELT_SHORTNAME VARCHAR(4) not null
		constraint MELT_UN
			unique,
	MELT_NAME VARCHAR(60) not null
		constraint MELT_UN2
			unique,
	MELT_UC VARCHAR(30),
	MELT_DC VARCHAR(30) not null,
	MELT_UM VARCHAR(30),
	MELT_DM VARCHAR(30),
	check (MELT_SHORTNAME IN ('ARCS', 'ATTR', 'BURU', 'COLU', 'DOMA', 'ENTI'
                                , 'INTF', 'ORGU', 'RELA', 'SYNO', 'TABL','DOCU','KEYS','DATY'
                                ,'DGRM','DIAG'))
);

create table MODELELEMENT
(
	MODE_ID INTEGER not null
		primary key autoincrement,
	MODE_TYPE VARCHAR(4) not null,
	MODE_MELT_ID integer not null
		references MODELELEM_TYPE (melt_id),
    MODE_MIN_ZOOM_LEVEL numeric(1) NULL CHECK ( MODE_MIN_ZOOM_LEVEL BETWEEN 0 AND 4 ) ,
    MODE_MAX_ZOOM_LEVEL numeric(1)  NULL CHECK ( MODE_MAX_ZOOM_LEVEL BETWEEN 0 AND 4 ) ,
    MODE_DEV_STATUS VARCHAR (4) NULL DEFAULT 'DEV' CHECK ( MODE_DEV_STATUS IN ('DEV', 'REL', 'TEST') ),
	check (MODE_TYPE IN ('ARCS', 'ATTR', 'BURU', 'COLU', 'DOMA', 'ENTI'
                            , 'INTF', 'ORGU', 'RELA', 'SYNO', 'TABL','DOCU','KEYS','DATY','DGRM','DIAG'))
);

create table DATATYPES
(
	DATY_ID INTEGER not null
		primary key
		references MODELELEMENT (mode_id)
			on delete cascade,
	DATY_NAME VARCHAR(60) not null
		constraint DATI_UN unique,
	DATY_BASETYPE VARCHAR(60) not null,
	DATY_UC VARCHAR(30),
	DATY_DC VARCHAR(30) not null,
	DATY_UM VARCHAR(30),
	DATY_DM VARCHAR(30),
	constraint DATY_BASETYPE_CK
		check (DATY_BASETYPE IN ('BINARY', 'NUMERIC', 'STRING', 'DATETIME'))
);

create table ENTITIES
(
	ENTI_ID integer not null
		primary key
		references MODELELEMENT (mode_id)
			on delete cascade,
	ENTI_NAME VARCHAR(60) not null
		constraint ENTI_NAME_UK
			unique,
	ENTI_SHORT_NAME VARCHAR(15),
	ENTI_PREFIX VARCHAR(5),
	ENTI_TOOLTIP VARCHAR(4000),
	ENTI_DESCR VARCHAR(4000),
	ENTI_EXP_TUPLECNT VARCHAR(500),
	ENTI_UC VARCHAR(30),
	ENTI_DC VARCHAR(30) not null,
	ENTI_UM VARCHAR(30),
	ENTI_DM VARCHAR(30)
);

create table ARCS
(
	ARCS_ID INTEGER not null
		primary key autoincrement
		references MODELELEMENT (mode_id)
			on delete cascade,
	ARCS_NAME VARCHAR(60) not null,
	ARCS_ENTI_ID integer not null
		references ENTITIES (enti_id)
			on delete cascade,
	ARCS_UC VARCHAR(30),
	ARCS_DC VARCHAR(30) not null,
	ARCS_UM VARCHAR(30),
	ARCS_DM VARCHAR(30),
	constraint ARCS_UK
		unique (ARCS_ENTI_ID, ARCS_NAME)
);

create table EXTERNAL_REFS
(
	EXTR_ID INTEGER not null
		primary key autoincrement,
	EXTR_SOURCE_NAME VARCHAR(60) not null,
	EXTR_SOURCE_ID VARCHAR(100) not null,
	EXTR_MODE_ID integer not null
		references MODELELEMENT (mode_id)
			on delete cascade,
	EXTR_LAST_UPDATE VARCHAR(30) NOT NULL,
	constraint EXTR_UK
		unique (EXTR_SOURCE_NAME, EXTR_MODE_ID),
	constraint EXTR_UK_ID
		unique (EXTR_SOURCE_NAME, EXTR_SOURCE_ID)
);

create table KEYS
(
	KEYS_ID INTEGER not null
		primary key autoincrement,
	KEYS_NAME VARCHAR(60) not null,
	KEYS_ENTI_ID integer not null
		references ENTITIES (enti_id)
			on delete cascade,
	KEYS_UC VARCHAR(30) not null,
	KEYS_DC VARCHAR(30) not null,
	KEYS_UM VARCHAR(30),
	KEYS_DM VARCHAR(30),
	constraint KEYS_UK
		unique (KEYS_ENTI_ID, KEYS_NAME)
);

create table LANG_TEXTS
(
	LGTX_ID INTEGER not null
		primary key autoincrement,
	LGTX_ATTRNAME VARCHAR(60) not null,
	LGTX_TEXT VARCHAR(4000),
	LGTX_LANG_ID integer not null
		references LANGUAGES (lang_id),
	LGTX_MODE_ID integer not null
		references MODELELEMENT (mode_id)
			on delete cascade,
	LGTX_UC VARCHAR(30),
	LGTX_DC VARCHAR(30) not null,
	LGTX_UM VARCHAR(30),
	LGTX_DM VARCHAR(30),
	constraint LGTX_UK
		unique (LGTX_LANG_ID, LGTX_MODE_ID, LGTX_ATTRNAME)
);

create table PHYSICAL_UNIT
(
	PHYU_ID INTEGER not null
		primary key autoincrement,
	PHYU_SI_UNIT VARCHAR(10),
	PHYU_NAME VARCHAR(60) not null
		constraint PHYU_UK_NAME
			unique,
	PHYU_DESCR VARCHAR(4000),
	PHYU_UC VARCHAR(30) not null,
	PHYU_DC VARCHAR(30) not null,
	PHYU_UM VARCHAR(30),
	PHYU_DM VARCHAR(30)
);

create table RELATIONS
(
	RELA_ID integer not null
		primary key
		references MODELELEMENT (mode_id)
			on delete cascade,
	RELA_NAME VARCHAR(60) not null
		constraint RELA_UK_NAME
			unique,
	RELA_TYPE VARCHAR(4) not null,
	RELA_ENTI_ID_FROM integer not null
		references ENTITIES (enti_id),
	RELA_ARCS_ID_FROM integer
		references ARCS (arcs_id),
	RELA_ASSOC_FROM_TO VARCHAR(4000),
	RELA_MAPTYPE_FROM_TO CHAR(1) not null,
	RELA_MANDATORY_FROM_TO VARCHAR(5) not null,
	RELA_HIST_FROM_TO VARCHAR(5) not null,
	RELA_ENTI_ID_TO integer not null
		references ENTITIES (enti_id),
	RELA_ARCS_ID_TO integer
		references ARCS (arcs_id),
	RELA_ASSOC_TO_FROM VARCHAR(100),
	RELA_MAPTYPE_TO_FROM CHAR(1) not null,
	RELA_MANDATORY_TO_FROM VARCHAR(5) not null,
	RELA_HIST_TO_FROM VARCHAR(4000) not null,
	RELA_UC VARCHAR(30),
	RELA_DC VARCHAR(30) not null,
	RELA_UM VARCHAR(30),
	RELA_DM VARCHAR(30),
	check (RELA_HIST_FROM_TO IN('FALSE','TRUE')),
	check (RELA_HIST_TO_FROM IN('FALSE','TRUE')),
	check (RELA_MANDATORY_FROM_TO IN('FALSE','TRUE')),
	check (RELA_MANDATORY_TO_FROM IN('FALSE','TRUE')),
	check (RELA_MAPTYPE_FROM_TO IN ('1', 'M')),
	check (RELA_MAPTYPE_TO_FROM IN ('1', 'M')),
	check (RELA_TYPE IN ('1:1', 'ISAR', 'ISAS', 'M:1', 'M:N')),
	constraint RELA_MAPTYPE_CHK
		check ((RELA_TYPE = 'ISAR'
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
))
);

create table STORAGE_FORMATS
(
	STFO_ID INTEGER not null
		primary key autoincrement,
	STFO_NAME VARCHAR(60) not null
		constraint STFO_UN
			unique,
	STFO_DESCR VARCHAR(4000),
	STFO_UC VARCHAR(30) not null,
	STFO_DC VARCHAR(30) not null,
	STFO_UM VARCHAR(30),
	STFO_DM VARCHAR(30)
);

create table DOCUMENTS
(
	DOCU_ID INTEGER not null
		primary key,
	DOCU_NAME VARCHAR(60) not null CONSTRAINT DOCU_UK UNIQUE,
	DOCU_STFO_ID integer
		references STORAGE_FORMATS (STFO_ID),
	DOCU_REFERENCE VARCHAR(500),
	DOCU_CONTENT IMAGE,
	DOCU_DOCU_ID integer
		references DOCUMENTS (docu_id)
);

create table MODE_DOCU
(
	MODO_ID INTEGER not null
		primary key autoincrement,
	MODO_MODE_ID integer not null
		references MODELELEMENT (mode_id)
			on delete cascade,
	MODO_DOCU_ID integer not null
		references DOCUMENTS (DOCU_ID)
			on delete cascade,
	constraint MODO_UK
		unique (MODO_MODE_ID, MODO_DOCU_ID)
);

create table SYNONYMS
(
	SYNO_ID INTEGER not null
		primary key
		references MODELELEMENT (mode_id)
			on delete cascade,
	SYNO_NAME VARCHAR(60) not null,
	SYNO_ENTI_ID integer not null
		references ENTITIES (ENTI_ID)
			on delete cascade,
	SYNO_UC VARCHAR(30),
	SYNO_DC VARCHAR(30) not null,
	SYNO_UM VARCHAR(30),
	SYNO_DM VARCHAR(30),
	constraint SYNO_UK unique (SYNO_ENTI_ID,SYNO_NAME)
);

create table USER_DEFINED_PROPERTIES
(
	UDPR_ID INTEGER not null
		primary key autoincrement,
	UDPR_THEME VARCHAR(60) not null,
	UDPR_GROUP VARCHAR(60),
	UDPR_NAME VARCHAR(60) not null,
	UDPR_DESCR VARCHAR(4000),
	UDPR_UC VARCHAR(30) not null,
	UDPR_DC VARCHAR(30) not null,
	UDPR_UM VARCHAR(30),
	UDPR_DM VARCHAR(30),
	constraint UDPR_UN
		unique (UDPR_THEME, UDPR_NAME)
);

create table MODELEMTYPE_PROPERTIES
(
	METP_ID INTEGER not null
		primary key autoincrement,
	METP_MELT_ID integer not null
		references MODELELEM_TYPE (MELT_ID)
            on delete cascade,
	METP_UDPR_ID integer not null
		references USER_DEFINED_PROPERTIES (UDPR_ID)
            on delete cascade,
	METP_OPTIONAL VARCHAR(5) not null,
	constraint METP_UN
		unique (METP_MELT_ID, METP_UDPR_ID),
	check (METP_OPTIONAL IN ('FALSE', 'TRUE'))
);

create table UDP_VALUES
(
	UDPV_ID INTEGER not null
		primary key autoincrement,
	UDPV_VALUE VARCHAR(4000),
	UDPV_MODE_ID integer not null
		references MODELELEMENT (mode_id)
			on delete cascade,
	UDPV_UDPR_ID integer not null
		references USER_DEFINED_PROPERTIES (UDPR_ID)
            on delete cascade,
	UDPV_UC VARCHAR(30) not null,
	UDPV_DC VARCHAR(30) not null,
	UDPV_UM VARCHAR(30),
	UDPV_DM VARCHAR(30),
	constraint UDPV_UN
		unique (UDPV_MODE_ID, UDPV_UDPR_ID)
);

create table diagramtypes
(
	diat_id integer
		primary key autoincrement,
	diat_name varchar(100) not null
		constraint diat_un
			unique,
	diat_uc varchar(30) not null,
	diat_dc varchar(30) not null,
	diat_um varchar(30),
	diat_dm varchar(30)
);

create table diagrams
(
	diag_id integer
		primary key autoincrement
		references MODELELEMENT (mode_id)
			on delete cascade,
	diag_name varchar(60) not null
		constraint diag__un
			unique,
	diag_diat_id integer not null
		references diagramtypes (diat_id),
	diag_legendx integer,
	diag_legendy integer,
	diag_uc varchar(30) not null,
	diag_dc varchar(30) not null,
	diag_um varchar(30),
	diag_dm varchar(30)
);

create table elementreps
(
	eler_id integer
		primary key autoincrement,
	eler_mode_id integer not null
		constraint eler_mode_fk
			references MODELELEMENT (mode_id)
				on delete cascade,
	eler_diag_id integer not null
		references diagrams (diag_id)
			on delete cascade,
	eler_index NUMBER(4) default 0 not null,
	eler_position_x integer,
	eler_position_y integer,
	eler_width integer not null,
	eler_height integer not null,
	eler_opacity integer,
	eler_color varchar(6) not null,
	eler_marginwidth integer,
	eler_marginopacity integer,
	eler_margincolor varchar(6),
	eler_fontsize integer,
	eler_fontcolor varchar(6),
	eler_uc varchar(30) not null,
	eler_dc varchar(30) not null,
	eler_um varchar(30),
	eler_dm varchar(30),
	constraint eler_un
		unique (eler_diag_id, eler_mode_id, eler_index),
	check (eler_fontsize BETWEEN 1 AND 999),
	check (eler_marginopacity BETWEEN 0 AND 100),
	check (eler_opacity BETWEEN 0 AND 100),
	check (length(eler_color)= 6),
	check (length(eler_fontcolor)= 6),
	check (length(eler_margincolor)= 6)
);

create table interfaces
(
	intf_ID integer
		primary key autoincrement
		references MODELELEMENT (MODE_ID),
	intf_NAME VARCHAR(60) not null
		constraint intf_UN
			unique,
	intf_DESCR VARCHAR(4000),
	intf_UC VARCHAR(30) not null,
	intf_DC VARCHAR(30) not null,
	intf_UM VARCHAR(30),
	intf_DM VARCHAR(30)
);

create table DOMAINS
(
	DOMA_ID integer not null
		primary key
		references MODELELEMENT (MODE_ID)
			on delete cascade,
	DOMA_NAME VARCHAR(60) not null
		constraint DOMA_NAME_UK
			unique,
	DOMA_DESCR VARCHAR(4000),
	DOMA_TYPE VARCHAR(4) not null,
	DOMA_ORIGIN VARCHAR(6) not null,
	DOMA_INTF_ID integer
		constraint DOMA_INTF_FK
			references interfaces (INTF_ID),
	DOMA_DATY_ID integer
		references DATATYPES (daty_id) ,
	DOMA_DAT_MINVALUE VARCHAR(30),
	DOMA_DAT_MAXVALUE VARCHAR(30),
	DOMA_DAT_GRANULARITY VARCHAR(15),
	DOMA_TXT_MAXLNG NUMERIC(28),
	DOMA_TXT_SYNTAXRULE VARCHAR(4000),
	DOMA_NUM_MAXVALUE NUMERIC(30,10),
	DOMA_NUM_MINVALUE NUMERIC(30,10),
	DOMA_NUM_TOTAL_DIGITS NUMERIC(3),
	DOMA_NUM_FRACT_DIGITS NUMERIC(3) default 0,
	DOMA_NUM_ROUND_VALUE NUMERIC(7,3),
	DOMA_NUM_PHYU_ID integer
		references PHYSICAL_UNIT (PHYU_ID),
	DOMA_BIN_CONTENTTYPE VARCHAR(30),
	DOMA_BIN_STFO_ID integer
		references STORAGE_FORMATS (STFO_ID),
	DOMA_UC VARCHAR(30) not null,
	DOMA_DC VARCHAR(30) not null,
	DOMA_UM VARCHAR(30),
	DOMA_DM VARCHAR(30),
	check (DOMA_BIN_CONTENTTYPE IN ('DRAWING', 'FILM', 'IMAGE', 'OTHER', 'SOUND', 'TEXT')),
	check (DOMA_DAT_GRANULARITY IN ('DAY', 'HOUR', 'MILlISECOND', 'MINUTE', 'MONTH', 'QUARTER', 'SECOND', 'SEMESTER', 'WEEK', 'YEAR')),
	check (DOMA_ORIGIN IN ('DER', 'DOM')),
	check (DOMA_TYPE IN ('BIN', 'DAT', 'GRP', 'LOV', 'NUM', 'TXT')),
	constraint DOMA_ExDep1
		check (DOMA_TYPE != 'BIN'
 OR ( DOMA_BIN_CONTENTTYPE IS NOT NULL AND DOMA_NUM_FRACT_DIGITS IS NULL AND DOMA_NUM_MAXVALUE IS NULL AND DOMA_NUM_MINVALUE IS NULL
	 AND DOMA_NUM_PHYU_ID IS NULL AND DOMA_NUM_ROUND_VALUE IS NULL AND DOMA_NUM_TOTAL_DIGITS IS NULL AND DOMA_DAT_GRANULARITY IS NULL
	 AND DOMA_DAT_MAXVALUE IS NULL AND DOMA_DAT_MINVALUE IS NULL AND DOMA_TXT_SYNTAXRULE IS NULL AND DOMA_TXT_MAXLNG IS NULL)),
	constraint DOMA_ExDep2
		check (DOMA_TYPE != 'DAT'
 OR ( DOMA_BIN_CONTENTTYPE IS NULL AND DOMA_BIN_STFO_ID IS NULL AND DOMA_NUM_FRACT_DIGITS IS NULL
	 AND DOMA_NUM_MAXVALUE IS NULL AND DOMA_NUM_MINVALUE IS NULL AND DOMA_NUM_PHYU_ID IS NULL AND DOMA_NUM_ROUND_VALUE IS NULL
	 AND DOMA_NUM_TOTAL_DIGITS IS NULL AND DOMA_DAT_GRANULARITY IS NOT NULL AND DOMA_TXT_SYNTAXRULE IS NULL AND DOMA_TXT_MAXLNG IS NULL)),
	constraint DOMA_ExDep3
		check (DOMA_TYPE != 'GRP'
 OR ( DOMA_BIN_CONTENTTYPE IS NULL AND DOMA_BIN_STFO_ID IS NULL AND DOMA_NUM_FRACT_DIGITS IS NULL AND DOMA_NUM_MAXVALUE IS NULL AND DOMA_NUM_MINVALUE IS NULL AND DOMA_NUM_PHYU_ID IS NULL AND DOMA_NUM_ROUND_VALUE IS NULL AND DOMA_NUM_TOTAL_DIGITS IS NULL AND DOMA_DAT_GRANULARITY IS NULL AND DOMA_DAT_MAXVALUE IS NULL AND DOMA_DAT_MINVALUE IS NULL AND DOMA_TXT_SYNTAXRULE IS NULL AND DOMA_TXT_MAXLNG IS NULL)),
	constraint DOMA_ExDep4
		check (DOMA_TYPE != 'LOV'
 OR ( DOMA_BIN_CONTENTTYPE IS NULL AND DOMA_BIN_STFO_ID IS NULL AND DOMA_NUM_FRACT_DIGITS IS NULL AND DOMA_NUM_MAXVALUE IS NULL AND DOMA_NUM_MINVALUE IS NULL AND DOMA_NUM_PHYU_ID IS NULL AND DOMA_NUM_ROUND_VALUE IS NULL AND DOMA_NUM_TOTAL_DIGITS IS NULL AND DOMA_DAT_GRANULARITY IS NULL AND DOMA_DAT_MAXVALUE IS NULL AND DOMA_DAT_MINVALUE IS NULL AND DOMA_TXT_SYNTAXRULE IS NULL)),
	constraint DOMA_ExDep5
		check (DOMA_TYPE != 'NUM'
 OR ( DOMA_BIN_CONTENTTYPE IS NULL AND DOMA_BIN_STFO_ID IS NULL AND DOMA_NUM_FRACT_DIGITS IS NOT NULL AND DOMA_NUM_TOTAL_DIGITS IS NOT NULL AND DOMA_DAT_GRANULARITY IS NULL AND DOMA_DAT_MAXVALUE IS NULL AND DOMA_DAT_MINVALUE IS NULL AND DOMA_TXT_SYNTAXRULE IS NULL AND DOMA_TXT_MAXLNG IS NULL)),
	constraint DOMA_ExDep6
		check (DOMA_TYPE != 'TXT'
 OR ( DOMA_BIN_CONTENTTYPE IS NULL AND DOMA_BIN_STFO_ID IS NULL AND DOMA_NUM_FRACT_DIGITS IS NULL AND DOMA_NUM_MAXVALUE IS NULL AND DOMA_NUM_MINVALUE IS NULL AND DOMA_NUM_PHYU_ID IS NULL AND DOMA_NUM_ROUND_VALUE IS NULL AND DOMA_NUM_TOTAL_DIGITS IS NULL AND DOMA_DAT_GRANULARITY IS NULL AND DOMA_DAT_MAXVALUE IS NULL AND DOMA_DAT_MINVALUE IS NULL))
);

create table ATTRIBUTES
(
	ATTR_ID integer not null
		primary key
		references MODELELEMENT (mode_id)			on delete cascade,
	ATTR_ENTI_ID integer not null		references ENTITIES (ENTI_ID),
	ATTR_DOMA_ID integer not null		references DOMAINS (DOMA_ID),
	ATTR_TECH_NAME VARCHAR(60) not null,
	ATTR_DISPL_NAME VARCHAR(4000),
	ATTR_DISPL_SEQ NUMERIC(5),
	ATTR_TOOLTIP VARCHAR(4000),
	ATTR_DESCR VARCHAR(4000),
	ATTR_IS_DESCRIPTIVE VARCHAR(5) not null,
	ATTR_IS_MANDATORY VARCHAR(5) not null,
	ATTR_IS_HISTORICISED VARCHAR(5) not null,
	ATTR_IS_REPEATED VARCHAR(5) not null,
	ATTR_IS_TRANSLATED VARCHAR(5) not null,
	ATTR_IS_ENCRYPTED VARCHAR(5) not null,
	ATTR_UC VARCHAR(30),
	ATTR_DC VARCHAR(30) not null,
	ATTR_UM VARCHAR(30),
	ATTR_DM VARCHAR(30),
	constraint ATTR_UK	unique (ATTR_TECH_NAME, ATTR_ENTI_ID),
	constraint ATTR_UK2	unique (ATTR_DISPL_NAME, ATTR_ENTI_ID),
	check (ATTR_IS_DESCRIPTIVE IN('FALSE','TRUE')),
	check (ATTR_IS_ENCRYPTED IN('FALSE','TRUE')),
	check (ATTR_IS_HISTORICISED IN('FALSE','TRUE')),
	check (ATTR_IS_MANDATORY IN('FALSE','TRUE')),
	check (ATTR_IS_REPEATED IN('FALSE','TRUE')),
	check (ATTR_IS_TRANSLATED IN('FALSE','TRUE'))
);

create table DEFAULT_VALUES
(
	DEVA_ID INTEGER not null
		primary key autoincrement,
	DEVA_DOMA_ID integer not null
		references DOMAINS (DOMA_ID)
			on delete cascade,
	DEVA_VALUE VARCHAR(100) not null,
	DEVA_SORT_ORDER NUMERIC(3),
	DEVA_DISPL VARCHAR(4000),
	DEVA_DESCR VARCHAR(4000),
	DEVA_UC VARCHAR(30),
	DEVA_DC VARCHAR(30) not null,
	DEVA_UM VARCHAR(30),
	DEVA_DM VARCHAR(30),
	constraint DEVA_UK
		unique (DEVA_DOMA_ID, DEVA_VALUE)
);

create table DOMAINGROUP_MEMBERS
(
	DGRM_ID INTEGER not null
		primary key autoincrement
		references MODELELEMENT (mode_id)
			on delete cascade,
	DGRM_NAME VARCHAR(4000) not null,
	DGRM_DESCR VARCHAR(4000),
	DGRM_IS_MANDATORY VARCHAR(5) not null,
	DGRM_DOMA_ID_GROUP integer not null
		references DOMAINS (DOMA_ID),
	DGRM_DOMA_ID_MEMBER integer not null
		references DOMAINS (DOMA_ID),
	DGRM_UC VARCHAR(30) not null,
	DGRM_DC VARCHAR(30) not null,
	DGRM_UM VARCHAR(30),
	DGRM_DM VARCHAR(30),
	constraint DGRM_DOMA_UK
		unique (DGRM_DOMA_ID_GROUP, DGRM_NAME),
	check (DGRM_IS_MANDATORY IN ('FALSE', 'TRUE'))
);

create table KEY_ELEMENTS
(
	KELE_ID INTEGER not null
		primary key autoincrement,
	KELE_KEYS_ID integer not null
		references KEYS (KEYS_ID)
			on delete cascade,
	KELE_ATTR_ID integer
		references ATTRIBUTES (ATTR_ID)
			on delete cascade,
	KELE_RELA_ID integer
		references RELATIONS (RELA_ID)
			on delete cascade,
	KELE_UC VARCHAR(30) not null,
	KELE_DC VARCHAR(30) not null,
	KELE_UM VARCHAR(30),
	KELE_DM VARCHAR(30),
	constraint KELE_UN
		unique (KELE_KEYS_ID, KELE_ATTR_ID, KELE_RELA_ID),
	constraint FKArc_8
		check (( (KELE_RELA_ID IS NOT NULL) AND
		   (KELE_ATTR_ID IS NULL)
	     ) OR (  (KELE_ATTR_ID IS NOT NULL) AND
                 (KELE_RELA_ID IS NULL) ))
);

create table melt_diats
(
	medi_id integer
		primary key autoincrement,
	medi_diat_id integer not null
		references diagramtypes (diat_id)
			on delete cascade,
	medi_melt_id integer not null
		constraint modi_melt_fk
			references MODELELEM_TYPE (melt_id)
				on delete cascade,
	medi_uc varchar(30) not null,
	medi_dc varchar(30) not null,
	medi_um varchar(30),
	medi_dm varchar(30),
	constraint medi__un
		unique (medi_diat_id, medi_melt_id)
);

create table organisationalunits
(
	orgu_id integer
		primary key
		constraint orgu_mode_fk
			references MODELELEMENT (mode_id)
				on delete cascade,
	orgu_name VARCHAR(60) not null
		constraint orgu_name_un
			unique,
	orgu_descr VARCHAR(4000),
	orgu_mail VARCHAR(200)
		constraint orgu_email_un
			unique,
	orgu_telefon VARCHAR(30),
	orgu_address VARCHAR(4000),
	orgu_orgu_id NUMBER(10)
		references organisationalunits (orgu_id),
	orgu_uc varchar(30) not null,
	orgu_dc varchar(30) not null,
	orgu_um varchar(30),
	orgu_dm varchar(30)
);

create table mode_orgu
(
	moou_id integer
		primary key,
	moou_mode_id integer not null
		constraint moou_mode_fk
			references MODELELEMENT (mode_id)
				on delete cascade,
	moou_orgu_id integer not null
		references organisationalunits (orgu_id)
			on delete cascade
);

create table projects
(
	proj_id integer
		primary key autoincrement,
	proj_name VARCHAR(60) not null
		constraint proj__un
			unique,
	proj_languages VARCHAR(60),
	proj_curr_lang VARCHAR2(2),
	proj_uc VARCHAR(30) not null,
	proj_dc VARCHAR(30) not null,
	proj_um VARCHAR(30),
	proj_dm VARCHAR(30)
);

create table relationreps
(
	relr_id integer
		primary key autoincrement,
	relr_diag_id integer not null
		references diagrams (diag_id),
	relr_mode_id integer not null
		constraint relr_mode_fk
			references MODELELEMENT (mode_id)
				on delete cascade,
	relr_linewidth integer default 1 not null,
	relr_linecolor varchar(6),
	relr_lineopacity integer,
	relr_startedge varchar(1),
	relr_startposition integer,
	relr_start_connector VARCHAR2(1),
	relr_starttext_angle integer,
	relr_starttext_distance integer,
	relr_starttext_x integer,
	relr_starttext_y integer,
	relr_starttext_width integer,
	relr_starttext_height integer,
	relr_endedge varchar(1),
	relr_endposition integer,
	relr_end_connector VARCHAR2(1),
	relr_endtext_angle integer,
	relr_endtext_distance integer,
	relr_endtext_x integer,
	relr_endtext_y integer,
	relr_endtext_width integer,
	relr_endtext_height integer,
	relr_fontcolor varchar(6) default '000000',
	relr_fontsize integer,
	relr_uc varchar(30) not null,
	relr_dc varchar(30) not null,
	relr_um varchar(30),
	relr_dm varchar(30),
	constraint relr_un
		unique (relr_diag_id, relr_mode_id),
	check (relr_end_connector IN ('1','M')),
	check (relr_start_connector IN ('1','M')),
	constraint relr_eab_chk
		check (relr_endtext_distance BETWEEN 1 AND 9999),
	constraint relr_eb_chk
		check (relr_endtext_width BETWEEN 1 AND 9999),
	constraint relr_eh_chk
		check (relr_endtext_height BETWEEN 1 AND 9999),
	constraint relr_ek_chk
		check (relr_endedge IN ('N','O','S','W')),
	constraint relr_ep_chk
		check (relr_endposition BETWEEN 0.0 AND 100.0),
	constraint relr_ewi_chk
		check (relr_endtext_angle BETWEEN - 179 AND 180),
	constraint relr_ex_chk
		check (relr_endtext_x BETWEEN -9999 AND 999999),
	constraint relr_ey_chk
		check (relr_endtext_y BETWEEN -9999 AND 999999),
	constraint relr_ldk_chk
		check (relr_lineopacity BETWEEN 0 AND 100),
	constraint relr_lf_chk
		check (length(relr_linecolor)= 6),
	constraint relr_sf_chk
		check (length(relr_fontcolor)= 6),
	constraint relr_sg_chk
		check (relr_fontsize BETWEEN 1 AND 999),
	constraint relr_stab_chk
		check (relr_starttext_distance BETWEEN 1 AND 9999),
	constraint relr_stb_chk
		check (relr_starttext_width BETWEEN 1 AND 9999),
	constraint relr_sth_chk
		check (relr_starttext_height BETWEEN 1 AND 9999),
	constraint relr_stk_chk
		check (relr_startedge IN ('N','O','S','W')),
	constraint relr_stp_chk
		check (relr_startposition BETWEEN 0.0 AND 100.0),
	constraint relr_stwi_chk
		check (relr_starttext_angle BETWEEN - 179 AND 180),
	constraint relr_stx_chk
		check (relr_starttext_x BETWEEN -9999 AND 999999),
	constraint relr_sty_chk
		check (relr_starttext_y BETWEEN -9999 AND 999999)
);

create table linesegments
(
	lise_id integer
		primary key autoincrement,
	lise_seq integer not null,
	lise_relr_id integer not null
		references relationreps (relr_id)
			on delete cascade,
	lise_x integer not null,
	lise_y integer not null,
	lise_linetype VARCHAR2(6),
	lise_angle integer,
	lise_uc varchar(30) not null,
	lise_dc varchar(30) not null,
	lise_um varchar(30),
	lise_dm varchar(30),
	constraint lise__un
		unique (lise_relr_id, lise_seq),
	constraint ck_lise_linetype
		check (lise_linetype IN('DADO','DASHED','DOTTED','SOLID')),
	constraint ck_relr_relr_fontcolor
		check (lise_y BETWEEN 0 AND 999999)
);

create table tables
(
	tabl_id integer
		primary key autoincrement
		constraint TABL_MODE_FK
			references MODELELEMENT (mode_ID),
	tabl_name varchar(60) not null,
	tabl_intf_id integer not null
		references interfaces (intf_ID),
	tabl_prefix varchar(60),
	tabl_descr varchar(4000),
	tabl_uc varchar(30) not null,
	tabl_dc varchar(30) not null,
	tabl_um varchar(30),
	tabl_dm varchar(30),
	constraint TABL_UN
		unique (tabl_intf_id, tabl_name)
);

create table columns
(
	colu_id integer
		primary key
		constraint colu_mode_fk
			references MODELELEMENT (mode_id),
	colu_column_name varchar(60) not null,
	colu_mandatory varchar(5) not null,
	colu_format varchar(200),
	colu_ext_system_id varchar(100),
	colu_descr varchar(4000),
	colu_type_string varchar(200),
	colu_tabl_id integer not null
		references tables (tabl_id),
	colu_doma_id integer not null
		constraint colu_doma_fk
			references DOMAINS (doma_id),
	colu_uc varchar(30) not null,
	colu_dc varchar(30) not null,
	colu_um varchar(30),
	colu_dm varchar(30),
	constraint colu_uk
		unique (colu_tabl_id, colu_column_name),
	check (colu_mandatory in ('TRUE', 'FALSE'))
);

create table colu_attr_map
(
	coam_id integer
		primary key autoincrement,
	coam_seq integer not null,
	coam_direction varchar(7) not null,
	coam_transf_rule varchar(4000),
	coam_triggertype varchar(10),
	coam_triggerperiod integer,
	coam_colu_id integer not null
		references columns (colu_id)
			on delete cascade,
	coam_attr_id integer not null
		constraint coam_attr_fk
			references ATTRIBUTES (attr_id)
				on delete cascade,
	constraint coam_un
		unique (coam_direction, coam_colu_id, coam_attr_id, coam_seq),
	check (coam_direction in ('INBOUND', 'OUTBOUND')),
	check (coam_seq > 0),
	check (coam_triggertype in ('MANUELL', 'PERIODE', 'ZPKT'))
);

create table tabl_enti_maps
(
	tema_id integer
		primary key autoincrement,
	tema_tabl_id integer not null
		references tables (tabl_id) on delete  cascade ,
	tema_enti_id integer
		constraint tema_enti_fk
			references ENTITIES (enti_id) on delete cascade ,
	tema_rela_id integer
		constraint tema_rela_fk
			references RELATIONS (rela_id) on delete cascade ,
	constraint tema_un
		unique (tema_tabl_id, tema_enti_id, tema_rela_id),
	constraint tema_ck
		check ((tema_enti_id is not null and tema_rela_id is null )
      	        		  or (tema_enti_id is null and tema_rela_id is not null))
);

CREATE TABLE BUSINESS_RULES
    (
     BURU_ID integer NOT NULL primary key autoincrement
    		constraint BURU_MODE_FK
			references MODELELEMENT (mode_ID),
     BURU_NAME VARCHAR (60) NOT NULL ,
     BURU_RULE VARCHAR (4000) NOT NULL ,
     BURU_DESCR VARCHAR (4000) NULL ,
     BURU_IMPACT VARCHAR (4000) NULL ,
     BURU_TYPE VARCHAR (10) NOT NULL CONSTRAINT CK__BUSINESS___BURU___1293BD5E CHECK ( [BURU_TYPE]='TRIGGER' OR [BURU_TYPE]='CHECK' OR [BURU_TYPE]='CALC' ) ,
     BURU_LEVEL VARCHAR (10) NOT NULL CONSTRAINT CK__BUSINESS___BURU___1387E197 CHECK ( [BURU_LEVEL]='TUPL' OR [BURU_LEVEL]='ENTI' OR [BURU_LEVEL]='DB' OR [BURU_LEVEL]='ATTR' ) ,
     BURU_ERRORMSG VARCHAR (100) ,
     BURU_UC VARCHAR (30) NOT NULL ,
     BURU_DC DATETIME (8) NOT NULL ,
     BURU_UM VARCHAR (30) NULL ,
     BURU_DM DATETIME (8) NULL
    );

CREATE TABLE BUSINESSRULE_ELEMENTS
    (
     BURE_ID integer NOT NULL primary key autoincrement,
     BURE_BURU_ID NUMERIC (10) NOT NULL ,
     BURE_WRITEABLE VARCHAR (5) NOT NULL CONSTRAINT CK__BUSINESSR__BURE___10216507 CHECK ( [BURE_WRITEABLE]='TRUE' OR [BURE_WRITEABLE]='FALSE' ) ,
     BURE_ATTR_ID NUMERIC (10) NULL ,
     BURE_ENTI_ID NUMERIC (10) NULL ,
     BURE_RELA_ID NUMERIC (10) NULL ,
     BURE_DEVA_ID NUMERIC (10) NULL ,
     BURE_TABL_ID NUMERIC (10) NULL ,
     BURE_COLU_ID NUMERIC (10) NULL ,
     BURE_UC VARCHAR (30) NOT NULL ,
     BURE_DC DATETIME (8) NOT NULL ,
     BURE_UM VARCHAR (30) NULL ,
     BURE_DM DATETIME (8) NULL ,
	 CONSTRAINT FKArc_1 CHECK (
        (  (BURE_ENTI_ID IS NOT NULL) AND
         (BURE_TABL_ID IS NULL)  AND
         (BURE_RELA_ID IS NULL)  AND
         (BURE_ATTR_ID IS NULL)  AND
         (BURE_COLU_ID IS NULL)  AND
         (BURE_DEVA_ID IS NULL) ) OR
        (  (BURE_TABL_ID IS NOT NULL) AND
         (BURE_ENTI_ID IS NULL)  AND
         (BURE_RELA_ID IS NULL)  AND
         (BURE_ATTR_ID IS NULL)  AND
         (BURE_COLU_ID IS NULL)  AND
         (BURE_DEVA_ID IS NULL) ) OR
        (  (BURE_RELA_ID IS NOT NULL) AND
         (BURE_ENTI_ID IS NULL)  AND
         (BURE_TABL_ID IS NULL)  AND
         (BURE_ATTR_ID IS NULL)  AND
         (BURE_COLU_ID IS NULL)  AND
         (BURE_DEVA_ID IS NULL) ) OR
        (  (BURE_ATTR_ID IS NOT NULL) AND
         (BURE_ENTI_ID IS NULL)  AND
         (BURE_TABL_ID IS NULL)  AND
         (BURE_RELA_ID IS NULL)  AND
         (BURE_COLU_ID IS NULL)  AND
         (BURE_DEVA_ID IS NULL) ) OR
        (  (BURE_COLU_ID IS NOT NULL) AND
         (BURE_ENTI_ID IS NULL)  AND
         (BURE_TABL_ID IS NULL)  AND
         (BURE_RELA_ID IS NULL)  AND
         (BURE_ATTR_ID IS NULL)  AND
         (BURE_DEVA_ID IS NULL) ) OR
        (  (BURE_DEVA_ID IS NOT NULL) AND
         (BURE_ENTI_ID IS NULL)  AND
         (BURE_TABL_ID IS NULL)  AND
         (BURE_RELA_ID IS NULL)  AND
         (BURE_ATTR_ID IS NULL)  AND
         (BURE_COLU_ID IS NULL) ) OR
        (  (BURE_ENTI_ID IS NULL)  AND
         (BURE_TABL_ID IS NULL)  AND
         (BURE_RELA_ID IS NULL)  AND
         (BURE_ATTR_ID IS NULL)  AND
         (BURE_COLU_ID IS NULL)  AND
         (BURE_DEVA_ID IS NULL) )  ),
		 CONSTRAINT BURE_ATTR_FK FOREIGN KEY
    (
     BURE_ATTR_ID
    )
    REFERENCES ATTRIBUTES
    (
     ATTR_ID
    )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
	CONSTRAINT BURE_BURU_FK FOREIGN KEY
    (
     BURE_BURU_ID
    )
    REFERENCES BUSINESS_RULES
    (
     BURU_ID
    )
    ON DELETE CASCADE
    ON UPDATE NO ACTION ,
	 CONSTRAINT BURE_DEVA_FK FOREIGN KEY
    (
     BURE_DEVA_ID
    )
    REFERENCES DEFAULT_VALUES
    (
     DEVA_ID
    )
    ON DELETE CASCADE
	  ON UPDATE NO ACTION,
	  CONSTRAINT BURE_ENTI_FK FOREIGN KEY
    (
     BURE_ENTI_ID
    )
    REFERENCES ENTITIES
    (
     ENTI_ID
    )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
	CONSTRAINT BURE_RELA_FK FOREIGN KEY
    (
     BURE_RELA_ID
    )
    REFERENCES RELATIONS
    (
     RELA_ID
    )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
	 CONSTRAINT BURU_COLU_FK FOREIGN KEY
    (
     BURE_COLU_ID
    )
    REFERENCES COLUMNS
    ( 
     COLU_ID 
    ) 
    ON DELETE CASCADE 
    ON UPDATE NO ACTION,
 CONSTRAINT BURU_TABL_FK FOREIGN KEY 
    ( 
     BURE_TABL_ID
    ) 
    REFERENCES TABLES 
    ( 
     TABL_ID 
    ) 
    ON DELETE CASCADE 
    ON UPDATE NO ACTION 
);
	
CREATE VIEW SUPERENTI AS
        with rel as (select rela_type
               , case
                     when RELA_MANDATORY_TO_FROM = 'TRUE' then RELA_ENTI_ID_FROM
                     else RELA_ENTI_ID_TO end as rela_superenti_id
               , case
                     when RELA_MANDATORY_FROM_TO = 'TRUE' then RELA_ENTI_ID_FROM
                     else RELA_ENTI_ID_TO end as rela_subenti_id
                 from relations
                where rela_type = 'ISAR'
                )
    select rela_type,superentity.enti_id as superenti_id, superentity.enti_name as super_enti_name
        ,subentity.enti_id as subenti_id, subentity.enti_name as sub_enti_name
          from ENTITIES superentity
            join ARCS on ARCS_ENTI_ID = superentity.enti_id
            join relations
                  on  ((rela_arcs_id_from  = ARCS_ID and RELA_ENTI_ID_from = superentity.ENTI_ID)
                   or (rela_arcs_id_to  = ARCS_ID and RELA_ENTI_ID_to = superentity.ENTI_ID))
                     and RELA_TYPE =  'ISAS'
           left  join ENTITIES subentity on  (subentity.ENTI_ID =  rela_enti_id_to and rela_arcs_id_from = arcs_id )
                or (subentity.ENTI_ID =  rela_enti_id_from and rela_arcs_id_to = arcs_id )
    union all
        select rela_type,superentity.enti_id as superenti_id, superentity.enti_name as super_enti_name
        ,subentity.enti_id as subenti_id, subentity.enti_name as sub_enti_name
          from ENTITIES superentity
          join rel on rela_superenti_id = superentity.ENTI_ID
        join ENTITIES subentity on subentity.ENTI_ID = rela_subenti_id;

create view dbversion as select '1.1' as version, datetime() as installedtime;
	-- sql-server: create view  dbversion as select '1.0' as version, current_timestamp as installedtime
	-- postgres: create view  dbversion as select '1.0' as version, current_timestamp as installedtime
