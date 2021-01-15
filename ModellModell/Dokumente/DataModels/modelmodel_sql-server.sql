create table BUSINESS_RULE
(
	BURU_ID numeric(10) not null
		constraint BURU_PK
			primary key,
	BURU_NAME varchar(60) not null,
	BURU_DESCR varchar(4000),
	BURU_IMPACT varchar(4000),
	BURU_TYPE varchar(10) not null
		check ([BURU_TYPE]='TRIGGER' OR [BURU_TYPE]='CHECK' OR [BURU_TYPE]='CALC'),
	BURU_LEVEL varchar(10) not null
		check ([BURU_LEVEL]='TUPL' OR [BURU_LEVEL]='ENTI' OR [BURU_LEVEL]='DB' OR [BURU_LEVEL]='ATTR'),
	BURU_ERRORMSG varchar(100) not null
)
go

create table DEFAULT_VALUES
(
	DEVA_ID numeric(10) identity
		constraint DEVA_PK
			primary key,
	DEVA_DOMA_ID numeric(10) not null,
	DEVA_VALUE varchar(100) not null,
	DEVA_SORT_ORDER numeric(3),
	DEVA_DISPL varchar(max),
	DEVA_DESCR varchar(max),
	DEVA_UC varchar(30) not null,
	DEVA_DC datetime not null,
	DEVA_UM varchar(30),
	DEVA_DM datetime,
	constraint DEVA_VGWT_UK
		unique (DEVA_DOMA_ID, DEVA_VALUE)
)
go

create table DIAGRAMTYPES
(
	DIAT_ID numeric(10) identity
		constraint DIAT_PK
			primary key,
	DIAT_NAME varchar(100) not null
		constraint DIAT__UN
			unique,
	DIAT_UC varchar(30) not null,
	DIAT_DC datetime not null,
	DIAT_UM varchar(30),
	DIAT_DM datetime
)
go

create table LANGUAGES
(
	LANG_ID numeric(10) identity
		constraint LANG_PK
			primary key,
	LANG_ISO_NAME varchar(60)
		constraint LANG_ISO_NAME_UN
			unique,
	LANG_ISO_CODE2 char(2) not null
		constraint LANG_ISO_CODE2_UN
			unique
		constraint LANG_ISO2_CHK
			check ([LANG_ISO_CODE2]=lower([LANG_ISO_CODE2])),
	LANG_ISO_CODE3 char(3) not null
		constraint LANG_ISO_CODE3_UN
			unique
		constraint LANG_ISO3_CHK
			check ([LANG_ISO_CODE3]=lower([LANG_ISO_CODE3])),
	LANG_IS_TEXT_LANG varchar(5) not null
		check ([LANG_IS_TEXT_LANG]='TRUE' OR [LANG_IS_TEXT_LANG]='FALSE'),
	LANG_IS_BASE_LANG varchar(5) not null
		check ([LANG_IS_BASE_LANG]='TRUE' OR [LANG_IS_BASE_LANG]='FALSE'),
	LANG_LANG_ID numeric(10)
		constraint LANG_REPLACE_FK
			references LANGUAGES,
	LANG_UC varchar(30) not null,
	LANG_DC datetime not null,
	LANG_UM varchar(30),
	LANG_DM datetime
)
go

create table MODELELEM_TYPE
(
	MELT_ID numeric(10) identity
		constraint MELT_PK
			primary key,
	MELT_SHORTNAME varchar(4) not null
		constraint MELT_UN
			unique
		check ([MELT_SHORTNAME]='TABL' OR [MELT_SHORTNAME]='SYNO' OR [MELT_SHORTNAME]='RELA' OR [MELT_SHORTNAME]='ORGU' OR [MELT_SHORTNAME]='KEYS' OR [MELT_SHORTNAME]='INTF' OR [MELT_SHORTNAME]='ENTI' OR [MELT_SHORTNAME]='DOMA' OR [MELT_SHORTNAME]='DOCU' OR [MELT_SHORTNAME]='DIAG' OR [MELT_SHORTNAME]='DGRM' OR [MELT_SHORTNAME]='DATY' OR [MELT_SHORTNAME]='COLU' OR [MELT_SHORTNAME]='BURU' OR [MELT_SHORTNAME]='ATTR' OR [MELT_SHORTNAME]='ARCS'),
	MELT_NAME varchar(60) not null
		constraint MELT_UN2
			unique,
	MELT_UC varchar(30) not null,
	MELT_DC datetime not null,
	MELT_UM varchar(30),
	MELT_DM datetime
)
go

create table MELT_DIATS
(
	MEDI_ID numeric(10) not null
		constraint MEDI_PK
			primary key,
	MEDI_DIAT_ID numeric(10) not null
		constraint MEDI_DIAT_FK
			references DIAGRAMTYPES
				on delete cascade,
	MEDI_MELT_ID numeric(10) not null
		constraint MODI_MELT_FK
			references MODELELEM_TYPE
				on delete cascade,
	MEDI_UC varchar(30) not null,
	MEDI_DC datetime not null,
	MEDI_UM varchar(30),
	MEDI_DM datetime,
	constraint MEDI__UN
		unique (MEDI_DIAT_ID, MEDI_MELT_ID)
)
go

create table MODELELEMENT
(
	MODE_ID numeric(10) identity
		constraint MODE_PK
			primary key,
	MODE_TYPE varchar(4) not null
		check ([MODE_TYPE]='TABL' OR [MODE_TYPE]='SYNO' OR [MODE_TYPE]='RELA' OR [MODE_TYPE]='ORGU' OR [MODE_TYPE]='KEYS' OR [MODE_TYPE]='INTF' OR [MODE_TYPE]='ENTI' OR [MODE_TYPE]='DOMA' OR [MODE_TYPE]='DOCU' OR [MODE_TYPE]='DIAG' OR [MODE_TYPE]='DGRM' OR [MODE_TYPE]='DATY' OR [MODE_TYPE]='COLU' OR [MODE_TYPE]='BURU' OR [MODE_TYPE]='ATTR' OR [MODE_TYPE]='ARCS'),
	MODE_MELT_ID numeric(10) not null
		constraint MODE_MELT_FK
			references MODELELEM_TYPE
)
go

create table DATATYPES
(
	DATY_ID numeric(10) identity
		constraint DATY_PK
			primary key
		constraint DATY_MODE_FK
			references MODELELEMENT,
	DATY_NAME varchar(60) not null
		constraint DATY_UN
			unique,
	DATY_BASETYPE varchar(60) not null
		constraint DATY_BASETYPE_CK
			check ([DATY_BASETYPE]='STRING' OR [DATY_BASETYPE]='NUMERIC' OR [DATY_BASETYPE]='DATETIME' OR [DATY_BASETYPE]='BINARY'),
	DATY_UC varchar(30) not null,
	DATY_DC datetime not null,
	DATY_UM varchar(30),
	DATY_DM datetime
)
go

create table DIAGRAMS
(
	DIAG_ID numeric(10) not null
		constraint DIAG_PK
			primary key
		constraint DIAGRAMS_MODELELEMENT_FK
			references MODELELEMENT
				on delete cascade,
	DIAG_NAME varchar(60) not null
		constraint DIAG__UN
			unique,
	DIAG_DIAT_ID numeric(10) not null
		constraint DIAG_DIAT_FK
			references DIAGRAMTYPES,
	DIAG_LEGENDX numeric(8),
	DIAG_LEGENDY numeric(8),
	DIAG_UC varchar(30) not null,
	DIAG_DC datetime not null,
	DIAG_UM varchar(30),
	DIAG_DM datetime
)
go

create table ELEMENTREPS
(
	ELER_ID numeric(10) not null
		constraint ELER_Elemendarstellung_PK
			primary key,
	ELER_MODE_ID numeric(10) not null
		constraint ELER_MODE_FK
			references MODELELEMENT,
	ELER_DIAG_ID numeric(10) not null
		constraint ELER_DIAG_FK
			references DIAGRAMS
				on delete cascade,
	ELER_INDEX numeric(4) default 0 not null,
	ELER_POSITION_X numeric(6),
	ELER_POSITION_Y numeric(6),
	ELER_WITDH numeric(4) not null,
	ELER_HEIGHT numeric(4) not null,
	ELER_OPACITY numeric(3) default 100
		check ([ELER_OPACITY]>=0 AND [ELER_OPACITY]<=100),
	ELER_COLOR varchar(6) default '000000' not null
		check (datalength([ELER_COLOR])=6),
	ELER_MARGINWIDTH numeric(3,1) default 1,
	ELER_MARGINOPACITY numeric(3) default 100
		check ([ELER_MARGINOPACITY]>=0 AND [ELER_MARGINOPACITY]<=100),
	ELER_MARGINCOLOR varchar(6) default '000000'
		check (datalength([ELER_MARGINCOLOR])=6),
	ELER_FONTSIZE numeric(3)
		check ([ELER_FONTSIZE]>=1 AND [ELER_FONTSIZE]<=999),
	ELER_FONTCOLOR varchar(6) default '000000'
		check (datalength([ELER_FONTCOLOR])=6),
	ELER_UC varchar(30) not null,
	ELER_DC datetime not null,
	ELER_UM varchar(30),
	ELER_DM datetime,
	constraint ELER__UN
		unique (ELER_MODE_ID, ELER_DIAG_ID, ELER_INDEX)
)
go

exec sp_addextendedproperty 'MS_Description', 'Vorgabewert einer Darstellung eines Elementtyps', 'SCHEMA', 'dbo', 'TABLE', 'ELEMENTREPS', 'COLUMN', 'ELER_POSITION_X'
go

exec sp_addextendedproperty 'MS_Description', 'Vorgabewert einer Darstellung eines Elementtyps', 'SCHEMA', 'dbo', 'TABLE', 'ELEMENTREPS', 'COLUMN', 'ELER_POSITION_Y'
go

exec sp_addextendedproperty 'MS_Description', 'Vorgabewert der Darstellung des Randes um das Element', 'SCHEMA', 'dbo', 'TABLE', 'ELEMENTREPS', 'COLUMN', 'ELER_WITDH'
go

exec sp_addextendedproperty 'MS_Description', 'Vorgabewert der Darstellung des Randes um das Element', 'SCHEMA', 'dbo', 'TABLE', 'ELEMENTREPS', 'COLUMN', 'ELER_HEIGHT'
go

exec sp_addextendedproperty 'MS_Description', 'Vorgabewert der Darstellung des Randes um das Element', 'SCHEMA', 'dbo', 'TABLE', 'ELEMENTREPS', 'COLUMN', 'ELER_MARGINWIDTH'
go

exec sp_addextendedproperty 'MS_Description', 'Vorgabewert der Schriftgrösse des Elementsnamens', 'SCHEMA', 'dbo', 'TABLE', 'ELEMENTREPS', 'COLUMN', 'ELER_FONTSIZE'
go

create table ENTITIES
(
	ENTI_ID numeric(10) not null
		constraint ENTI_PK
			primary key
		constraint ENTI_MODE_FK
			references MODELELEMENT,
	ENTI_NAME varchar(60) not null
		constraint ENTI_NAME_UK
			unique,
	ENTI_SHORT_NAME varchar(15),
	ENTI_PREFIX varchar(5),
	ENTI_TOOLTIP varchar(4000),
	ENTI_DESCR varchar(4000),
	ENTI_EXP_TUPLE# varchar(500),
	ENTI_UC varchar(30) not null,
	ENTI_DC datetime not null,
	ENTI_UM varchar(30),
	ENTI_DM datetime
)
go

create table ARCS
(
	ARCS_ID numeric(10) not null
		constraint ARCS_PK
			primary key
		constraint ARCS_MODE_FK
			references MODELELEMENT
				on delete cascade,
	ARCS_NAME varchar(60) not null,
	ARCS_ENTI_ID numeric(10) not null
		constraint ARCS_ENTI_FK
			references ENTITIES
				on delete cascade,
	ARCS_UC varchar(30) not null,
	ARCS_DC datetime not null,
	ARCS_UM varchar(30),
	ARCS_DM datetime,
	constraint ARCS_UK
		unique (ARCS_ENTI_ID, ARCS_NAME)
)
go

create table EXTERNAL_REFS
(
	EXTR_ID numeric(10) not null
		constraint EXTR_PK
			primary key,
	EXTR_SOURCE_NAME varchar(60) not null,
	EXTR_SOURCE_ID varchar(100) not null,
	EXTR_MODE_ID numeric(10) not null
		constraint EXTR_MODE_FK
			references MODELELEMENT
				on delete cascade,
	constraint EXTR_UK
		unique (EXTR_SOURCE_NAME, EXTR_MODE_ID),
	constraint Extr_UK_id
		unique (EXTR_SOURCE_NAME, EXTR_SOURCE_ID)
)
go

create table INTERFACES
(
	INTF_ID numeric(10) not null
		constraint INTF_PK
			primary key
		constraint INFT_MODE_FK
			references MODELELEMENT,
	INTF_NAME varchar(60) not null
		constraint SCHN_UN
			unique,
	INTF_DESCR varchar(4000) not null,
	INTF_UC varchar(30) not null,
	INTF_DC datetime not null,
	INTF_UM varchar(30),
	INTF_DM datetime
)
go

create table LANG_TEXTS
(
	LGTX_ID numeric(10) identity
		constraint LGTX_PK
			primary key,
	LGTX_ATTRNAME varchar(60) not null,
	LGTX_TEXT varchar(4000),
	LGTX_LANG_ID numeric(10) not null
		constraint SPTX_LANG_FK
			references LANGUAGES,
	LGTX_MODE_ID numeric(10) not null
		constraint SPTX_MODE_FK
			references MODELELEMENT
				on delete cascade,
	LGTX_UC varchar(30) not null,
	LGTX_DC datetime not null,
	LGTX_UM varchar(30),
	LGTX_DM datetime,
	constraint LGTX_UK
		unique (LGTX_LANG_ID, LGTX_MODE_ID, LGTX_ATTRNAME)
)
go

create table ORGANISATIONALUNITS
(
	ORGU_ID numeric(10) not null
		constraint ORGU_PK
			primary key
		constraint ORGU_MODE_FK
			references MODELELEMENT,
	ORGU_NAME varchar(60) not null
		constraint ORGU_NAME_UN
			unique,
	ORGU_DESCR varchar(4000),
	ORGU_MAIL varchar(200)
		constraint ORGU_EMAIL_UN
			unique,
	ORGU_TELEFON varchar(30),
	ORGU_ADDRESS varchar(4000),
	ORGU_ORGU_ID numeric(10)
		constraint ORGU_ORGU_FK
			references ORGANISATIONALUNITS,
	ORGU_UC varchar(30) not null,
	ORGU_DC datetime not null,
	ORGU_UM varchar(30),
	ORGU_DM datetime
)
go

create table MODE_ORGU
(
	MOOU_ID numeric(10) not null
		constraint MOOU_PK
			primary key,
	MOOU_MODE_ID numeric(10) not null
		constraint MOOU_MODE_FK
			references MODELELEMENT
				on delete cascade,
	MOOU_ORGU_ID numeric(10) not null
		constraint MOOU_ORGU_FK
			references ORGANISATIONALUNITS
				on delete cascade,
	constraint MOOU_UK
		unique (MOOU_MODE_ID, MOOU_ORGU_ID)
)
go

create table PHYSICAL_UNIT
(
	PHYU_ID numeric(10) identity
		constraint PHYU_PK
			primary key,
	PHYU_SI_UNIT varchar(10)
		constraint PHYU_UK_SI
			unique,
	PHYU_NAME varchar(60) not null
		constraint PHYU_UK_NAME
			unique,
	PHYU_DESCR varchar(4000),
	PHYU_UC varchar(30) not null,
	PHYU_DC datetime not null,
	PHYU_UM varchar(30),
	PHYU_DM datetime
)
go

create table RELATIONREPS
(
	RELR_ID numeric(10) not null
		constraint RELR_PK
			primary key,
	RELR_DIAG_ID numeric(10) not null
		constraint RELR_DIAG_FK
			references DIAGRAMS,
	RELR_MODE_ID numeric(10) not null
		constraint RELR_MODE_FK
			references MODELELEMENT
				on delete cascade,
	RELR_LINEWIDTH numeric(3,1) default 1 not null,
	RELR_LINECOLOR varchar(6) default '000000'
		check (datalength([RELR_LINECOLOR])=6),
	RELR_LINEOPACITY numeric(3) default 100
		check ([RELR_LINEOPACITY]>=0 AND [RELR_LINEOPACITY]<=100),
	RELR_STARTEDGE varchar
		check ([RELR_STARTEDGE]='W' OR [RELR_STARTEDGE]='S' OR [RELR_STARTEDGE]='O' OR [RELR_STARTEDGE]='N'),
	RELR_STARTPOSITION numeric(4,1)
		check ([RELR_STARTPOSITION]>=0.0 AND [RELR_STARTPOSITION]<=100.0),
	RELR_START_CONNECTOR varchar
		check ([RELR_START_CONNECTOR]='M' OR [RELR_START_CONNECTOR]='1'),
	RELR_STARTTEXT_ANGEL numeric(3)
		check ([RELR_STARTTEXT_ANGEL]>=(-179) AND [RELR_STARTTEXT_ANGEL]<=180),
	RELR_STARTTEXT_DISTANCE numeric(4)
		check ([RELR_STARTTEXT_DISTANCE]>=1 AND [RELR_STARTTEXT_DISTANCE]<=9999),
	RELR_STARTTEXT_X numeric(6)
		check ([RELR_STARTTEXT_X]>=0 AND [RELR_STARTTEXT_X]<=999999),
	RELR_STARTTEXT_Y numeric(6)
		check ([RELR_STARTTEXT_Y]>=0 AND [RELR_STARTTEXT_Y]<=999999),
	RELR_STARTTEXT_WIDTH numeric(4)
		check ([RELR_STARTTEXT_WIDTH]>=1 AND [RELR_STARTTEXT_WIDTH]<=9999),
	RELR_STARTTEXT_HEIGHT numeric(4)
		check ([RELR_STARTTEXT_HEIGHT]>=1 AND [RELR_STARTTEXT_HEIGHT]<=9999),
	RELR_ENDEDGE varchar
		check ([RELR_ENDEDGE]='W' OR [RELR_ENDEDGE]='S' OR [RELR_ENDEDGE]='O' OR [RELR_ENDEDGE]='N'),
	RELR_ENDPOSITION numeric(4,1)
		check ([RELR_ENDPOSITION]>=0.0 AND [RELR_ENDPOSITION]<=100.0),
	RELR_END_CONNECTOR varchar
		check ([RELR_END_CONNECTOR]='M' OR [RELR_END_CONNECTOR]='1'),
	RELR_ENDTEXT_ANGEL numeric(3)
		check ([RELR_ENDTEXT_ANGEL]>=(-179) AND [RELR_ENDTEXT_ANGEL]<=180),
	RELR_ENDTEXT_DISTANCE numeric(4)
		check ([RELR_ENDTEXT_DISTANCE]>=1 AND [RELR_ENDTEXT_DISTANCE]<=9999),
	RELR_ENDTEXT_X numeric(6)
		check ([RELR_ENDTEXT_X]>=0 AND [RELR_ENDTEXT_X]<=999999),
	RELR_ENDTEXT_Y numeric(6)
		check ([RELR_ENDTEXT_Y]>=0 AND [RELR_ENDTEXT_Y]<=999999),
	RELR_ENDTEXT_WIDTH numeric(4)
		check ([RELR_ENDTEXT_WIDTH]>=1 AND [RELR_ENDTEXT_WIDTH]<=9999),
	RELR_ENDTEXT_HEIGHT numeric(4)
		check ([RELR_ENDTEXT_HEIGHT]>=1 AND [RELR_ENDTEXT_HEIGHT]<=9999),
	RELR_FONTCOLOR varchar(6) default '000000'
		check (datalength([RELR_FONTCOLOR])=6),
	RELR_FONTSIZE numeric(3)
		check ([RELR_FONTSIZE]>=1 AND [RELR_FONTSIZE]<=999),
	RELR_UC varchar(30) not null,
	RELR_DC datetime not null,
	RELR_UM varchar(30),
	BEDA_DM datetime,
	constraint RELR_UN
		unique (RELR_DIAG_ID, RELR_MODE_ID)
)
go

create table LINESEGMENTS
(
	LISE_ID numeric(10) not null
		constraint LISE_PK
			primary key,
	LISE_SEQ numeric(4) not null,
	LISE_RELR_ID numeric(10) not null
		constraint LISE_BEDA_FK
			references RELATIONREPS
				on delete cascade,
	LISE_X numeric(6) not null
		constraint LISE_CK_X
			check ([LISE_X]>=0 AND [LISE_X]<=999999),
	LISE_Y numeric(6) not null
		constraint LISE_CK_Y
			check ([LISE_Y]>=0 AND [LISE_Y]<=999999),
	LISE_LINETYPE varchar(6) default 'SOLID'
		constraint LISE_CK_BEDA_BEDA_SCHRIFTGROESSE
			check ([LISE_LINETYPE]='SOLID' OR [LISE_LINETYPE]='DOTTED' OR [LISE_LINETYPE]='DASHED' OR [LISE_LINETYPE]='DADO'),
	LISE_ANGEL int,
	LISE_UC varchar(30) not null,
	LISE_DC datetime not null,
	LISE_UM varchar(30),
	LISE_DM datetime,
	constraint LISE__UN
		unique (LISE_RELR_ID, LISE_SEQ)
)
go

create table RELATIONS
(
	RELA_ID numeric(10) not null
		constraint RELA_PK
			primary key
		constraint RELA_MODE_FK
			references MODELELEMENT,
	RELA_NAME varchar(60) not null
		constraint RELA_UK_NAME
			unique,
	RELA_TYPE varchar(4) not null
		check ([RELA_TYPE]='M:N' OR [RELA_TYPE]='M:1' OR [RELA_TYPE]='ISA' OR [RELA_TYPE]='1:1'),
	RELA_ENTI_ID_FROM numeric(10) not null
		constraint RELA_ENTI_FROM_FK
			references ENTITIES,
	RELA_ARCS_ID_FROM numeric(10)
		constraint RELA_ARCS_FROM_FK
			references ARCS,
	RELA_ASSOC_FROM_TO varchar(max),
	RELA_MAPTYPE_FROM_TO char not null
		check ([RELA_MAPTYPE_FROM_TO]='M' OR [RELA_MAPTYPE_FROM_TO]='1'),
	RELA_MANDATORY_FROM_TO varchar(5) not null
		check ([RELA_MANDATORY_FROM_TO]='TRUE' OR [RELA_MANDATORY_FROM_TO]='FALSE'),
	RELA_HIST_FROM_TO varchar(5) not null
		check ([RELA_HIST_FROM_TO]='TRUE' OR [RELA_HIST_FROM_TO]='FALSE'),
	RELA_ENTI_ID_TO numeric(10) not null
		constraint RELA_ENTI_TO_FK
			references ENTITIES,
	RELA_ARCS_ID_TO numeric(10)
		constraint RELA_ARCS_TO_FK
			references ARCS,
	RELA_ASSOC_TO_FROM varchar(100),
	RELA_MAPTYPE_TO_FROM char not null
		check ([RELA_MAPTYPE_TO_FROM]='M' OR [RELA_MAPTYPE_TO_FROM]='1'),
	RELA_MANDATORY_TO_FROM varchar(5) not null
		check ([RELA_MANDATORY_TO_FROM]='TRUE' OR [RELA_MANDATORY_TO_FROM]='FALSE'),
	RELA_HIST_TO_FROM varchar(max) not null,
	RELA_UC varchar(30) not null,
	RELA_DC datetime not null,
	RELA_UM varchar(30),
	RELA_DM datetime,
	constraint RELA_MAPTYPE_CHK
		check ([RELA_TYPE]='ISAR' AND [RELA_MAPTYPE_FROM_TO]='1' AND [RELA_MAPTYPE_TO_FROM]='1' AND ([RELA_MANDATORY_FROM_TO]='TRUE' OR [RELA_MANDATORY_TO_FROM]='TRUE') OR [RELA_TYPE]='ISAS' AND [RELA_MAPTYPE_FROM_TO]='1' AND [RELA_MAPTYPE_TO_FROM]='1' AND [RELA_MANDATORY_FROM_TO]='TRUE' AND [RELA_MANDATORY_TO_FROM]='TRUE' AND ([RELA_ARCS_ID_FROM] IS NOT NULL OR [RELA_ARCS_ID_TO] IS NOT NULL) OR [RELA_TYPE]='1:1' AND [RELA_MAPTYPE_FROM_TO]='1' AND [RELA_MAPTYPE_TO_FROM]='1' OR [RELA_TYPE]='M:1' AND ([RELA_MAPTYPE_FROM_TO]='1' AND [RELA_MAPTYPE_TO_FROM]='M' OR [RELA_MAPTYPE_FROM_TO]='M' AND [RELA_MAPTYPE_TO_FROM]='1') OR [RELA_TYPE]='M:N' AND [RELA_MAPTYPE_TO_FROM]='M' AND [RELA_MAPTYPE_FROM_TO]='M')
)
go

create table STORAGE_FORMATS
(
	STFO_ID numeric(10) identity
		constraint STFO_PK
			primary key,
	STFO_NAME varchar(60) not null
		constraint STFO_UN
			unique,
	STFO_DESCR varchar(4000),
	STFO_UC varchar(30) not null,
	STFO_DC datetime not null,
	STFO_UM varchar(30),
	STFO_DM datetime
)
go

create table DOCUMENTS
(
	DOCU_ID numeric(10) identity
		constraint DOCU_PK
			primary key
		constraint DOCU_MODE_FK
			references MODELELEMENT,
	DOCU_NAME varchar(60) not null,
	DOCU_STFO_ID numeric(10)
		constraint DOCU_STFO_FK
			references STORAGE_FORMATS,
	DOCU_REFERENCE varchar(500),
	DOCU_CONTENT image,
	DOCU_DOCU_ID numeric(10)
		constraint DOCU_DOCU_FK
			references DOCUMENTS
)
go

create table DOMAINS
(
	DOMA_ID numeric(10) not null
		constraint DOMAINS_PK
			primary key
		constraint DOMA_MODE_FK
			references MODELELEMENT,
	DOMA_NAME varchar(60) not null
		constraint DOMA_UK
			unique,
	DOMA_DESCR varchar(4000),
	DOMA_TYPE varchar(4) not null
		check ([DOMA_TYPE]='TXT' OR [DOMA_TYPE]='NUM' OR [DOMA_TYPE]='LOV' OR [DOMA_TYPE]='GRP' OR [DOMA_TYPE]='DAT' OR [DOMA_TYPE]='BIN'),
	DOMA_ORIGIN varchar(6) not null
		check ([DOMA_ORIGIN]='DOM' OR [DOMA_ORIGIN]='DER'),
	DOMA_INTF_ID numeric(10)
		constraint DOMA_INTF_FK
			references INTERFACES,
	DOMA_DATY_ID numeric(10)
		constraint DOMA_DATY_ID
			references DATATYPES,
	DOMA_DAT_MINVALUE numeric(28),
	DOMA_DAT_MAXVALUE numeric(28),
	DOMA_DAT_GRANULARITY varchar(15)
		check ([DOMA_DAT_GRANULARITY]='YEAR' OR [DOMA_DAT_GRANULARITY]='WEEK' OR [DOMA_DAT_GRANULARITY]='SEMESTER' OR [DOMA_DAT_GRANULARITY]='SECOND' OR [DOMA_DAT_GRANULARITY]='QUARTER' OR [DOMA_DAT_GRANULARITY]='MONTH' OR [DOMA_DAT_GRANULARITY]='MINUTE' OR [DOMA_DAT_GRANULARITY]='MILlISECOND' OR [DOMA_DAT_GRANULARITY]='HOUR' OR [DOMA_DAT_GRANULARITY]='DAY'),
	DOMA_TXT_MAXLNG numeric(28),
	DOMA_TXT_SYNTAXRULE varchar(4000),
	DOMA_NUM_MAXVALUE numeric(30,10),
	DOMA_NUM_MINVALUE numeric(30,10),
	DOMA_NUM_TOTAL_DIGITS numeric(3),
	DOMA_NUM_FRACT_DIGITS numeric(3) default 0,
	DOMA_NUM_ROUND_VALUE numeric(7,3),
	DOMA_NUM_PHYU_ID numeric(10)
		constraint DOMA_PHYU_FK
			references PHYSICAL_UNIT,
	DOMA_BIN_CONTENTTYPE varchar(30)
		check ([DOMA_BIN_CONTENTTYPE]='TEXT' OR [DOMA_BIN_CONTENTTYPE]='SOUND' OR [DOMA_BIN_CONTENTTYPE]='OTHER' OR [DOMA_BIN_CONTENTTYPE]='IMAGE' OR [DOMA_BIN_CONTENTTYPE]='FILM' OR [DOMA_BIN_CONTENTTYPE]='DRAWING'),
	DOMA_BIN_STFO_ID numeric(10)
		constraint DOMA_STFO_FK
			references STORAGE_FORMATS,
	DOMA_UC varchar(30) not null,
	DOMA_DC datetime not null,
	DOMA_UM varchar(30),
	DOMA_DM datetime,
	constraint DOMA_ExDep1
		check ([DOMA_TYPE]<>'BIN' OR [DOMA_BIN_CONTENTTYPE] IS NOT NULL AND [DOMA_NUM_FRACT_DIGITS] IS NULL AND [DOMA_NUM_MAXVALUE] IS NULL AND [DOMA_NUM_MINVALUE] IS NULL AND [DOMA_NUM_PHYU_ID] IS NULL AND [DOMA_NUM_ROUND_VALUE] IS NULL AND [DOMA_NUM_TOTAL_DIGITS] IS NULL AND [DOMA_DAT_GRANULARITY] IS NULL AND [DOMA_DAT_MAXVALUE] IS NULL AND [DOMA_DAT_MINVALUE] IS NULL AND [DOMA_TXT_SYNTAXRULE] IS NULL AND [DOMA_TXT_MAXLNG] IS NULL),
	constraint DOMA_ExDep2
		check ([DOMA_TYPE]<>'DAT' OR [DOMA_BIN_CONTENTTYPE] IS NULL AND [DOMA_BIN_STFO_ID] IS NULL AND [DOMA_NUM_FRACT_DIGITS] IS NULL AND [DOMA_NUM_MAXVALUE] IS NULL AND [DOMA_NUM_MINVALUE] IS NULL AND [DOMA_NUM_PHYU_ID] IS NULL AND [DOMA_NUM_ROUND_VALUE] IS NULL AND [DOMA_NUM_TOTAL_DIGITS] IS NULL AND [DOMA_DAT_GRANULARITY] IS NOT NULL AND [DOMA_TXT_SYNTAXRULE] IS NULL AND [DOMA_TXT_MAXLNG] IS NULL),
	constraint DOMA_ExDep3
		check ([DOMA_TYPE]<>'GRP' OR [DOMA_BIN_CONTENTTYPE] IS NULL AND [DOMA_BIN_STFO_ID] IS NULL AND [DOMA_NUM_FRACT_DIGITS] IS NULL AND [DOMA_NUM_MAXVALUE] IS NULL AND [DOMA_NUM_MINVALUE] IS NULL AND [DOMA_NUM_PHYU_ID] IS NULL AND [DOMA_NUM_ROUND_VALUE] IS NULL AND [DOMA_NUM_TOTAL_DIGITS] IS NULL AND [DOMA_DAT_GRANULARITY] IS NULL AND [DOMA_DAT_MAXVALUE] IS NULL AND [DOMA_DAT_MINVALUE] IS NULL AND [DOMA_TXT_SYNTAXRULE] IS NULL AND [DOMA_TXT_MAXLNG] IS NULL),
	constraint DOMA_ExDep4
		check ([DOMA_TYPE]<>'LOV' OR [DOMA_BIN_CONTENTTYPE] IS NULL AND [DOMA_BIN_STFO_ID] IS NULL AND [DOMA_NUM_FRACT_DIGITS] IS NULL AND [DOMA_NUM_MAXVALUE] IS NULL AND [DOMA_NUM_MINVALUE] IS NULL AND [DOMA_NUM_PHYU_ID] IS NULL AND [DOMA_NUM_ROUND_VALUE] IS NULL AND [DOMA_NUM_TOTAL_DIGITS] IS NULL AND [DOMA_DAT_GRANULARITY] IS NULL AND [DOMA_DAT_MAXVALUE] IS NULL AND [DOMA_DAT_MINVALUE] IS NULL AND [DOMA_TXT_SYNTAXRULE] IS NULL AND [DOMA_TXT_MAXLNG] IS NULL),
	constraint DOMA_ExDep5
		check ([DOMA_TYPE]<>'NUM' OR [DOMA_BIN_CONTENTTYPE] IS NULL AND [DOMA_BIN_STFO_ID] IS NULL AND [DOMA_NUM_FRACT_DIGITS] IS NOT NULL AND [DOMA_NUM_TOTAL_DIGITS] IS NOT NULL AND [DOMA_DAT_GRANULARITY] IS NULL AND [DOMA_DAT_MAXVALUE] IS NULL AND [DOMA_DAT_MINVALUE] IS NULL AND [DOMA_TXT_SYNTAXRULE] IS NULL AND [DOMA_TXT_MAXLNG] IS NULL),
	constraint DOMA_ExDep6
		check ([DOMA_TYPE]<>'TXT' OR [DOMA_BIN_CONTENTTYPE] IS NULL AND [DOMA_BIN_STFO_ID] IS NULL AND [DOMA_NUM_FRACT_DIGITS] IS NULL AND [DOMA_NUM_MAXVALUE] IS NULL AND [DOMA_NUM_MINVALUE] IS NULL AND [DOMA_NUM_PHYU_ID] IS NULL AND [DOMA_NUM_ROUND_VALUE] IS NULL AND [DOMA_NUM_TOTAL_DIGITS] IS NULL AND [DOMA_DAT_GRANULARITY] IS NULL AND [DOMA_DAT_MAXVALUE] IS NULL AND [DOMA_DAT_MINVALUE] IS NULL)
)
go

create table ATTRIBUTES
(
	ATTR_ID numeric(10) not null
		constraint ATTR_PK
			primary key
		constraint ATTR_MODE_FK
			references MODELELEMENT
				on delete cascade,
	ATTR_ENTI_ID numeric(10)
		constraint ATTR_ENTI_FK
			references ENTITIES,
	ATTR_RELA_ID numeric(10)
		constraint ATTR_RELA_FK
			references RELATIONS,
	ATTR_DOMA_ID numeric(10) not null
		constraint ATTR_DOMA_FK
			references DOMAINS,
	ATTR_TECH_NAME varchar(60) not null,
	ATTR_DISPL_NAME varchar(4000),
	ATTR_DISPL_SEQ numeric(5),
	ATTR_TOOLTIP varchar(max),
	ATTR_DESCR varchar(max),
	ATTR_IS_DESCRIPTIVE varchar(5) not null
		check ([ATTR_IS_DESCRIPTIVE]='TRUE' OR [ATTR_IS_DESCRIPTIVE]='FALSE'),
	ATTR_IS_MANDATORY varchar(5) not null
		check ([ATTR_IS_MANDATORY]='TRUE' OR [ATTR_IS_MANDATORY]='FALSE'),
	ATTR_IS_HISTORICISED varchar(5) not null
		check ([ATTR_IS_HISTORICISED]='TRUE' OR [ATTR_IS_HISTORICISED]='FALSE'),
	ATTR_IS_REPEATED varchar(5) not null
		check ([ATTR_IS_REPEATED]='TRUE' OR [ATTR_IS_REPEATED]='FALSE'),
	ATTR_IS_TRANSLATED varchar(5) not null
		check ([ATTR_IS_TRANSLATED]='TRUE' OR [ATTR_IS_TRANSLATED]='FALSE'),
	ATTR_IS_ENCRYPTED varchar(5) not null
		check ([ATTR_IS_ENCRYPTED]='TRUE' OR [ATTR_IS_ENCRYPTED]='FALSE'),
	ATTR_UC varchar(30) not null,
	ATTR_DC datetime not null,
	ATTR_UM varchar(30),
	ATTR_DM datetime,
	constraint ATTR_UK
		unique (ATTR_TECH_NAME, ATTR_RELA_ID, ATTR_ENTI_ID),
	constraint ATTR_UK2
		unique (ATTR_DISPL_NAME, ATTR_RELA_ID, ATTR_ENTI_ID),
	constraint ENTI_OR_RELA_ARC
		check ([ATTR_ENTI_ID] IS NOT NULL AND [ATTR_RELA_ID] IS NULL OR [ATTR_RELA_ID] IS NOT NULL AND [ATTR_ENTI_ID] IS NULL)
)
go

create table DOMAINGROUP_MEMBERS
(
	DGRM_ID numeric(10) not null
		constraint DGRM_PK
			primary key
		constraint DGRM_MODE_FK
			references MODELELEMENT
				on delete cascade,
	DGRM_NAME varchar(60) not null,
	DGRM_DESCR varchar(4000),
	DGRM_IS_MANDATORY varchar(5) not null
		check ([DGRM_IS_MANDATORY]='TRUE' OR [DGRM_IS_MANDATORY]='FALSE'),
	DGRM_DOMA_ID_GROUP numeric(10) identity
		constraint dgrm_fk_doma_group
			references DOMAINS,
	DGRM_DOMA_ID_MEMBER numeric(10) not null
		constraint DGRM_FK_DOMA_MEMBER
			references DOMAINS
				on delete cascade,
	DGRM_UC varchar(30) not null,
	DGRM_DC datetime not null,
	DGRM_UM varchar(30),
	DGRM_DM datetime,
	constraint DGRM_DOMA_UK
		unique (DGRM_DOMA_ID_GROUP, DGRM_NAME)
)
go

create table KEY_ELEMENTS
(
	KELE_ID numeric(10) identity
		constraint KELE_PK
			primary key,
	KELE_KEYS_ID numeric(10) not null,
	KELE_ATTR_ID numeric(10) not null
		constraint KELE_ATTR_FK
			references ATTRIBUTES
				on delete cascade,
	KELE_RELA_ID numeric(10) not null
		constraint KELE_RELA_FK
			references RELATIONS
				on delete cascade,
	KELE_UC varchar(30) not null,
	KELE_DC datetime not null,
	KELE_UM varchar(30),
	KELE_DM datetime,
	constraint KELE_UN
		unique (KELE_KEYS_ID, KELE_ATTR_ID, KELE_RELA_ID),
	constraint FKArc_8
		check ([KELE_RELA_ID] IS NOT NULL AND [KELE_ATTR_ID] IS NULL OR [KELE_ATTR_ID] IS NOT NULL AND [KELE_RELA_ID] IS NULL)
)
go

create table MODE_DOCU
(
	MODO_ID numeric(10) not null
		constraint MODO_PKv2
			primary key,
	MODO_MODE_ID numeric(10) not null
		constraint MODO_MODE_FKv2
			references MODELELEMENT
				on delete cascade,
	MODO_DOCU_ID numeric(10) not null
		constraint MODO_DOCU_FK
			references DOCUMENTS
				on delete cascade,
	constraint MODO_UK
		unique (MODO_MODE_ID, MODO_DOCU_ID)
)
go

create table SYNONYMS
(
	SYNO_ID numeric(10) not null
		constraint SYNO_PK
			primary key
		constraint SYNO_MODE_FK
			references MODELELEMENT
				on delete cascade,
	SYNO_NAME varchar(60) not null,
	SYNO_ENTI_ID numeric(10) not null
		constraint SYNO_ENTI_FK
			references ENTITIES
				on delete cascade,
	SYNO_UC varchar(30) not null,
	SYNO_DC datetime not null,
	SYNO_UM varchar(30),
	SYNO_DM datetime
)
go

create table TABLES
(
	TABL_ID numeric(10) not null
		constraint TABL_PKv2
			primary key
		constraint TABL_MODE_FK
			references MODELELEMENT,
	TABL_NAME varchar(60) not null,
	TABL_DESCR varchar(4000),
	TABL_INTF_ID numeric(10) not null
		constraint TABL_INTF_FK
			references INTERFACES,
	TABL_UC varchar(30) not null,
	TABL_DC datetime not null,
	TABL_UM varchar(30),
	TABL_DM datetime,
	constraint TABL__UN
		unique (TABL_NAME, TABL_INTF_ID)
)
go

create table COLUMNS
(
	COLU_ID numeric(10) identity
		constraint COLU_PK
			primary key,
	COLU_COLUMN_NAME varchar(60) not null,
	COLU_MANDATORY varchar(5) not null,
	COLU_FORMAT varchar(200),
	COLU_DESCR varchar(4000),
	COLU_EXT_SYSTEM_ID varchar(100),
	COLU_TYPE_STRING varchar(100),
	COLU_TABL_ID numeric(10) not null
		constraint COLU_UK
			unique
		constraint COLU_TABL_FK
			references TABLES,
	COLU_DOMA_ID numeric(10) not null
		constraint COLU_DOMA_FK
			references DOMAINS,
	COLU_UC varchar(30) not null,
	COLU_DC datetime not null,
	COLU_UM varchar(30),
	COLU_DM datetime
)
go

exec sp_addextendedproperty 'MS_Description', 'ID / Code der Attributbdefinition in einer Standardsoftware', 'SCHEMA', 'dbo', 'TABLE', 'COLUMNS', 'COLUMN', 'COLU_EXT_SYSTEM_ID'
go

create table BUSINESSRULE_ELEMENT
(
	BURE_ID numeric(10) not null
		constraint BURE_PK
			primary key,
	BURE_BURU_ID numeric(10) not null
		constraint BURE_BURU_FK
			references BUSINESS_RULE
				on delete cascade,
	BURE_WRITEABLE varchar(5) not null
		check ([BURE_WRITEABLE]='TRUE' OR [BURE_WRITEABLE]='FALSE'),
	BURE_ATTR_ID numeric(10)
		constraint BURE_ATTR_FK
			references ATTRIBUTES
				on delete cascade,
	BURE_ENTI_ID numeric(10)
		constraint BURE_ENTI_FK
			references ENTITIES
				on delete cascade,
	BURE_RELA_ID numeric(10)
		constraint BURE_RELA_FK
			references RELATIONS
				on delete cascade,
	BURE_DEVA_ID numeric(10)
		constraint BURE_DEVA_FK
			references DEFAULT_VALUES
				on delete cascade,
	BURE_TABL_ID numeric(10)
		constraint BURU_TABL_FK
			references TABLES
				on delete cascade,
	BURE_UC varchar(30) not null,
	BURE_DC datetime not null,
	BURE_UM varchar(30),
	BURE_DM datetime,
	BURE_COLU_ID1 numeric(10)
		constraint BURU_COLU_FK
			references COLUMNS
				on delete cascade,
	constraint ENTI_OR_ATTR_OR_RELA_ARC
		check ([BURE_ATTR_ID] IS NOT NULL AND [BURE_ENTI_ID] IS NULL AND [BURE_RELA_ID] IS NULL AND [BURE_DEVA_ID] IS NULL AND [BURE_COLU_ID1] IS NULL AND [BURE_TABL_ID] IS NULL OR [BURE_ENTI_ID] IS NOT NULL AND [BURE_ATTR_ID] IS NULL AND [BURE_RELA_ID] IS NULL AND [BURE_DEVA_ID] IS NULL AND [BURE_COLU_ID1] IS NULL AND [BURE_TABL_ID] IS NULL OR [BURE_RELA_ID] IS NOT NULL AND [BURE_ATTR_ID] IS NULL AND [BURE_ENTI_ID] IS NULL AND [BURE_DEVA_ID] IS NULL AND [BURE_COLU_ID1] IS NULL AND [BURE_TABL_ID] IS NULL OR [BURE_DEVA_ID] IS NOT NULL AND [BURE_ATTR_ID] IS NULL AND [BURE_ENTI_ID] IS NULL AND [BURE_RELA_ID] IS NULL AND [BURE_COLU_ID1] IS NULL AND [BURE_TABL_ID] IS NULL OR [BURE_COLU_ID1] IS NOT NULL AND [BURE_ATTR_ID] IS NULL AND [BURE_ENTI_ID] IS NULL AND [BURE_RELA_ID] IS NULL AND [BURE_DEVA_ID] IS NULL AND [BURE_TABL_ID] IS NULL OR [BURE_TABL_ID] IS NOT NULL AND [BURE_ATTR_ID] IS NULL AND [BURE_ENTI_ID] IS NULL AND [BURE_RELA_ID] IS NULL AND [BURE_DEVA_ID] IS NULL AND [BURE_COLU_ID1] IS NULL OR [BURE_ATTR_ID] IS NULL AND [BURE_ENTI_ID] IS NULL AND [BURE_RELA_ID] IS NULL AND [BURE_DEVA_ID] IS NULL AND [BURE_COLU_ID1] IS NULL AND [BURE_TABL_ID] IS NULL)
)
go

create table COLU_ATTR_MAP
(
	coam_id int not null
		constraint colu_attr_map_PK
			primary key,
	coam_seq int not null,
	coam_direction varchar(7) not null
		check ([coam_direction]='OUTBOUND' OR [coam_direction]='INBOUND'),
	coam_colu_id numeric(10) not null
		constraint coma_colu_FK
			references COLUMNS
				on delete cascade,
	coam_attr_id numeric(10) not null
		constraint coma_attr_FK
			references ATTRIBUTES
				on delete cascade,
	coam_transf_rule varchar(4000),
	coam_triggertype varchar(10)
		check ([coam_triggertype]='ZPKT' OR [coam_triggertype]='PERIODE' OR [coam_triggertype]='MANUELL'),
	coam_triggerperiod int,
	constraint coam_un
		unique (coam_direction, coam_colu_id, coam_attr_id, coam_seq)
)
go

create table TABL_ENTI_MAP
(
	TEMA_ID numeric(10) not null
		constraint TEMA_PK
			primary key,
	TEMA_TABL_ID numeric(10) not null
		constraint tema_tabl_FK
			references TABLES,
	TEMA_ENTI_ID numeric(10)
		constraint TEMA_ENTI_FK
			references ENTITIES
				on delete cascade,
	TEMA_RELA_ID numeric(10)
		constraint TEMA_RELA_FK
			references RELATIONS
				on delete cascade,
	constraint TEMA_UN
		unique (TEMA_TABL_ID, TEMA_ENTI_ID),
	constraint FKArc_5
		check ([TEMA_RELA_ID] IS NOT NULL AND [TEMA_ENTI_ID] IS NULL OR [TEMA_ENTI_ID] IS NOT NULL AND [TEMA_RELA_ID] IS NULL OR [TEMA_RELA_ID] IS NULL AND [TEMA_ENTI_ID] IS NULL)
)
go

create table USER_DEFINED_PROPERTIES
(
	UDPR_ID numeric(10) identity
		constraint UDPR_PK
			primary key,
	UDPR_THEME varchar(60) not null,
	UDPR_GROUP varchar(60),
	UDPR_NAME varchar(60) not null,
	UDPR_DESCR varchar(4000),
	UDPR_UC varchar(30) not null,
	UDPR_DC datetime not null,
	UDPR_UM varchar(30),
	UDPR_DM datetime,
	constraint UDPR_UN
		unique (UDPR_THEME, UDPR_NAME)
)
go

create table MODELEMTYPE_PROPERTIES
(
	METP_ID numeric(10) not null
		constraint METP_PK
			primary key,
	METP_MELT_ID numeric(10) not null
		constraint METP_MELT_FK
			references MODELELEM_TYPE,
	METP_UDPR_ID numeric(10) not null
		constraint METP_UDPR_FK
			references USER_DEFINED_PROPERTIES,
	METP_OPTIONAL varchar(5) not null
		check ([METP_OPTIONAL]='TRUE' OR [METP_OPTIONAL]='FALSE'),
	constraint METP_UN
		unique (METP_MELT_ID, METP_UDPR_ID)
)
go

create table UDP_VALUES
(
	UDPV_ID numeric(10) identity
		constraint UDPV_PK
			primary key,
	UDPV_VALUE varchar(max),
	UDPV_MODE_ID numeric(10) not null
		constraint UDPV_MODE_FK
			references MODELELEMENT
				on delete cascade,
	UDPV_UDPR_ID numeric(10) not null
		constraint UDPV_UDPR_FK
			references USER_DEFINED_PROPERTIES,
	UDPV_UC varchar(30) not null,
	UDPV_DC datetime not null,
	UDPV_UM varchar(30),
	UDPV_DM datetime,
	constraint UDPV_UN
		unique (UDPV_MODE_ID, UDPV_UDPR_ID)
)
go

create table projects
(
	proj_id int not null
		constraint proj_pk
			primary key nonclustered,
	proj_name varchar(60) not null
		constraint proj_uk
			unique,
	proj_curr_lang varchar(2),
	proj_uc varchar(30) not null,
	proj_dc varchar(30) not null,
	proj_um varchar(30),
	proj_dm varchar(30)
)
go

CREATE  VIEW SUPERENTI AS
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
        join ENTITIES subentity on subentity.ENTI_ID = rela_subenti_id
go

