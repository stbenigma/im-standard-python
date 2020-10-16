-- Generiert von Oracle SQL Developer Data Modeler 20.2.0.167.1538
--   am/um:        2020-08-10 15:15:10 MESZ
--   Site:      SQL Server 2012
--   Typ:      SQL Server 2012


CREATE TABLE ARCS
    (
     ARCS_ID INTEGER NOT NULL primary key autoincrement,
     ARCS_NAME VARCHAR (60) NOT NULL ,
     ARCS_ENTI_ID integer NOT NULL ,
     ARCS_UC VARCHAR(30) NULL  ,
     ARCS_DC VARCHAR (30) NOT NULL ,
     ARCS_UM VARCHAR (30) NULL ,
     ARCS_DM VARCHAR (30) NULL
    ,CONSTRAINT ARCS_UK UNIQUE  (ARCS_ENTI_ID ASC, ARCS_NAME ASC)
	,CONSTRAINT ARCS_ENTI_FK FOREIGN KEY    (     ARCS_ENTI_ID)
		REFERENCES ENTITIES    (     ENTI_ID )
    ON DELETE CASCADE
    ,CONSTRAINT ARCS_MODE_FK FOREIGN KEY    (     ARCS_ID)
		REFERENCES MODELELEMENT    (     MODE_ID )
		ON DELETE CASCADE
    );
CREATE TABLE ATTRIBUTES
    (
     ATTR_ID integer NOT NULL  primary key,
     ATTR_ENTI_ID integer NULL ,
     ATTR_RELA_ID integer NULL ,
     ATTR_DOMA_ID integer NOT NULL ,
     ATTR_TECH_NAME VARCHAR (60) NOT NULL ,
     ATTR_DISPL_NAME VARCHAR (4000) NULL ,
     ATTR_DISPL_SEQ NUMERIC (5) NULL ,
     ATTR_TOOLTIP VARCHAR (4000) NULL ,
     ATTR_DESCR VARCHAR (4000) NULL ,
     ATTR_IS_DESCRIPTIVE VARCHAR (5) NOT NULL 
   		CHECK(ATTR_IS_DESCRIPTIVE IN('FALSE','TRUE')),
     ATTR_IS_MANDATORY VARCHAR (5) NOT NULL  
   		CHECK(ATTR_IS_MANDATORY IN('FALSE','TRUE')),
     ATTR_IS_HISTORICISED VARCHAR (5) NOT NULL  
   		CHECK(ATTR_IS_HISTORICISED IN('FALSE','TRUE')),
     ATTR_IS_REPEATED VARCHAR (5) NOT NULL  
   		CHECK(ATTR_IS_REPEATED IN('FALSE','TRUE')),
     ATTR_IS_TRANSLATED VARCHAR (5) NOT NULL  
   		CHECK(ATTR_IS_TRANSLATED IN('FALSE','TRUE')),
     ATTR_IS_ENCRYPTED VARCHAR (5) NOT NULL  
   		CHECK(ATTR_IS_ENCRYPTED IN('FALSE','TRUE')),
     ATTR_UC VARCHAR(30) NULL  ,
     ATTR_DC VARCHAR (30) NOT NULL ,
     ATTR_UM VARCHAR (30) NULL ,
     ATTR_DM VARCHAR (30) NULL
    ,CONSTRAINT ENTI_OR_RELA_ARC CHECK (
        (  (ATTR_ENTI_ID IS NOT NULL) AND
         (ATTR_RELA_ID IS NULL) ) OR
        (  (ATTR_RELA_ID IS NOT NULL) AND
         (ATTR_ENTI_ID IS NULL) )  )
      ,CONSTRAINT ATTR_UK UNIQUE (ATTR_TECH_NAME ASC, ATTR_RELA_ID ASC, ATTR_ENTI_ID ASC)
      ,CONSTRAINT ATTR_UK2 UNIQUE (ATTR_DISPL_NAME ASC, ATTR_RELA_ID ASC, ATTR_ENTI_ID ASC)
      ,CONSTRAINT ATTR_ENTI_FK FOREIGN KEY      (     ATTR_ENTI_ID)
		  REFERENCES ENTITIES      (     ENTI_ID )
      ,CONSTRAINT ATTR_MODE_FK FOREIGN KEY      (     ATTR_ID)
		  REFERENCES MODELELEMENT      (     MODE_ID )
		  ON DELETE CASCADE
      ,CONSTRAINT ATTR_RELA_FK FOREIGN KEY      (     ATTR_RELA_ID)
		  REFERENCES RELATIONS      (     RELA_ID )
	  ,CONSTRAINT ATTR_DOMA_FK FOREIGN KEY	  (     ATTR_DOMA_ID)
		  REFERENCES DOMAINS	  (     DOMA_ID )
		  ON DELETE NO ACTION
  );
CREATE TABLE BUSINESS_RULE
    (
     BURU_ID integer NOT NULL  primary key,
     BURU_NAME VARCHAR (4000) NOT NULL ,
     BURU_RULE VARCHAR (4000) NOT NULL ,
     BURU_DESCR VARCHAR (4000) NULL ,
     BURU_ERRMSG VARCHAR (4000) NULL ,
     BURU_UC VARCHAR(30) NULL  ,
     BURU_DC VARCHAR (30) NOT NULL ,
     BURU_UM VARCHAR (30) NULL ,
     BURU_DM VARCHAR (30) NULL
    ,CONSTRAINT BURU_NAME_UN UNIQUE (BURU_NAME ASC)
    ,CONSTRAINT BURU_MODE_FK FOREIGN KEY
    (     BURU_ID)
    REFERENCES MODELELEMENT
    (     MODE_ID )
    ON DELETE CASCADE
    ON UPDATE NO ACTION
    );
CREATE TABLE BUSINESSRULE_ELEMENT
    (
     BURE_ID INTEGER NOT NULL primary key autoincrement,
     BURE_BURU_ID integer NOT NULL ,
     BURE_ATTR_ID integer NULL ,
     BURE_ENTI_ID integer NULL ,
     BURE_RELA_ID integer NULL ,
     BURE_UC VARCHAR(30) NULL  ,
     BURE_DC VARCHAR (30) NOT NULL ,
     BURE_UM VARCHAR (30) NULL ,
     BURE_DM VARCHAR (30) NULL ,
    CONSTRAINT ENTI_OR_ATTR_OR_RELA_ARC CHECK (
        (  (BURE_ATTR_ID IS NOT NULL) AND
         (BURE_ENTI_ID IS NULL)  AND
         (BURE_RELA_ID IS NULL) ) OR
        (  (BURE_ENTI_ID IS NOT NULL) AND
         (BURE_ATTR_ID IS NULL)  AND
         (BURE_RELA_ID IS NULL) ) OR
        (  (BURE_RELA_ID IS NOT NULL) AND
         (BURE_ATTR_ID IS NULL)  AND
         (BURE_ENTI_ID IS NULL) ) OR
        (  (BURE_ATTR_ID IS NULL)  AND
         (BURE_ENTI_ID IS NULL)  AND
         (BURE_RELA_ID IS NULL) )  )
	     ,CONSTRAINT BURE_ATTR_FK FOREIGN KEY
	     (     BURE_ATTR_ID)
	     REFERENCES ATTRIBUTES
	     (     ATTR_ID )
	     ON DELETE CASCADE
	     ON UPDATE NO ACTION
	     ,CONSTRAINT BURE_BURU_FK FOREIGN KEY
	     (     BURE_BURU_ID)
	     REFERENCES BUSINESS_RULE
	     (     BURU_ID )
	     ON DELETE CASCADE
	     ON UPDATE NO ACTION
	     ,CONSTRAINT BURE_ENTI_FK FOREIGN KEY
	     (     BURE_ENTI_ID)
	     REFERENCES ENTITIES
	     (     ENTI_ID )
	     ON DELETE CASCADE
	     ON UPDATE NO ACTION
	     ,CONSTRAINT BURE_RELA_FK FOREIGN KEY
	     (     BURE_RELA_ID)
	     REFERENCES RELATIONS
	     (     RELA_ID )
	     ON DELETE CASCADE
	     ON UPDATE NO ACTION
);



CREATE TABLE DEFAULT_VALUES
    (
     DEVA_ID INTEGER NOT NULL primary key autoincrement,
     DEVA_DOMA_ID integer NOT NULL ,
     DEVA_VALUE VARCHAR (100) NOT NULL ,
     DEVA_SORT_ORDER NUMERIC (3) NULL ,
     DEVA_DISPL VARCHAR (4000) NULL ,
     DEVA_DESCR VARCHAR (4000) NULL ,
     DEVA_UC VARCHAR(30) NULL  ,
     DEVA_DC VARCHAR (30) NOT NULL ,
     DEVA_UM VARCHAR (30) NULL ,
     DEVA_DM VARCHAR (30) NULL
    ,CONSTRAINT DEVA_UK UNIQUE (DEVA_DOMA_ID ASC, DEVA_VALUE ASC);
    ,CONSTRAINT DEVA_DOMA_FK FOREIGN KEY    (     DEVA_DOMA_ID)
		REFERENCES DOMAINS    (     DOMA_ID )
    ON DELETE CASCADE
);
CREATE TABLE DOCUMENTS
    (
     DOCU_ID INTEGER NOT NULL primary key ,
     DOCU_NAME VARCHAR (60) NOT NULL ,
     DOCU_STFO_ID integer NULL ,
     DOCU_REFERENCE VARCHAR (500) NULL ,
     DOCU_CONTENT IMAGE NULL ,
     DOCU_DOCU_ID integer NULL
     ,CONSTRAINT DOCU_DOCU_FK FOREIGN KEY     (     DOCU_DOCU_ID)
		 REFERENCES DOCUMENTS     (     DOCU_ID )
	 ,CONSTRAINT DOCU_STFO_FK FOREIGN KEY (     DOCU_STFO_ID)
		 REFERENCES STORAGE_FORMATS (     STFO_ID )
	 
    );


CREATE TABLE DOMAINGROUP_MEMBERS
    (
     DGRM_ID INTEGER NOT NULL primary key autoincrement,
     DGRM_NAME VARCHAR (4000) NOT NULL ,
     DGRM_DESCR VARCHAR (4000) NULL ,
     DRGM_IS_MANDATORY VARCHAR (5) NOT NULL CHECK ( DRGM_Is_MANDATORY IN ('FALSE', 'TRUE') ) ,
     DGRM_DOMA_ID_GROUP integer NOT NULL  ,
     DGRM_DOMA_ID_MEMBER integer NOT NULL ,
     DGRM_UC VARCHAR (30) NOT NULL ,
     DGRM_DC VARCHAR (30) NOT NULL ,
     DGRM_UM VARCHAR (30) NULL ,
     DGRM_DM VARCHAR (30) NULL
    ,CONSTRAINT DGRM_DOMA_UK UNIQUE (DGRM_DOMA_ID_GROUP ASC, DGRM_NAME ASC)
    ,CONSTRAINT DGRM_DOMA_FK_GROUP FOREIGN KEY    (     DGRM_DOMA_ID_GROUP)
		REFERENCES DOMAINS    (     DOMA_ID )
    ,CONSTRAINT DGRM_DOMA_FK_MEMBER FOREIGN KEY(     DGRM_DOMA_ID_MEMBER)
		REFERENCES DOMAINS    (     DOMA_ID )
    ,CONSTRAINT DGRM_MODE_FK FOREIGN KEY    (     DGRM_ID)
		REFERENCES MODELELEMENT    (     MODE_ID )
    ON DELETE CASCADE
);
CREATE TABLE DOMAINS
    (
     DOMA_ID integer NOT NULL  primary key,
     DOMA_NAME VARCHAR (60) NOT NULL ,
     DOMA_DESCR VARCHAR (4000) NULL ,
     DOMA_TYPE VARCHAR (4) NOT NULL CHECK ( DOMA_TYPE IN ('BIN', 'DAT', 'GRP', 'LOV', 'NUM', 'TXT') ) ,
     DOMA_ORIGIN VARCHAR (6) NOT NULL CHECK ( DOMA_ORIGIN IN ('DER', 'DOM') ) ,
	 DOMA_DATY_ID integer,
     DOMA_DAT_MINVALUE VARCHAR (30) NULL ,
     DOMA_DAT_MAXVALUE VARCHAR (30) NULL ,
     DOMA_DAT_GRANULARITY VARCHAR (15) NULL CHECK ( DOMA_DAT_GRANULARITY IN ('DAY', 'HOUR', 'MILlISECOND', 'MINUTE', 'MONTH', 'QUARTER', 'SECOND', 'SEMESTER', 'WEEK', 'YEAR') ) ,
     DOMA_TXT_MAXLNG NUMERIC (28) NULL ,
     DOMA_TXT_SYNTAXRULE VARCHAR (4000) NULL ,
     DOMA_NUM_MAXVALUE NUMERIC (30,10) NULL ,
     DOMA_NUM_MINVALUE NUMERIC (30,10) NULL ,
     DOMA_NUM_TOTAL_DIGITS NUMERIC (3) NULL ,
     DOMA_NUM_FRACT_DIGITS NUMERIC (3) NULL DEFAULT 0 ,
     DOMA_NUM_ROUND_VALUE NUMERIC (7,3) NULL ,
     DOMA_NUM_PHYU_ID integer NULL ,
     DOMA_BIN_CONTENTTYPE VARCHAR (30) NULL CHECK ( DOMA_BIN_CONTENTTYPE IN ('DRAWING', 'FILM', 'IMAGE', 'OTHER', 'SOUND', 'TEXT') ) ,
     DOMA_BIN_STFO_ID integer NULL ,
     DOMA_UC VARCHAR (30) NOT NULL ,
     DOMA_DC VARCHAR (30) NOT NULL ,
     DOMA_UM VARCHAR (30) NULL ,
     DOMA_DM VARCHAR (30) NULL
,CONSTRAINT DOMA_ExDep1
    CHECK ( DOMA_TYPE != 'BIN'
 OR ( DOMA_BIN_CONTENTTYPE IS NOT NULL AND DOMA_NUM_FRACT_DIGITS IS NULL AND DOMA_NUM_MAXVALUE IS NULL AND DOMA_NUM_MINVALUE IS NULL
	 AND DOMA_NUM_PHYU_ID IS NULL AND DOMA_NUM_ROUND_VALUE IS NULL AND DOMA_NUM_TOTAL_DIGITS IS NULL AND DOMA_DAT_GRANULARITY IS NULL
	 AND DOMA_DAT_MAXVALUE IS NULL AND DOMA_DAT_MINVALUE IS NULL AND DOMA_TXT_SYNTAXRULE IS NULL AND DOMA_TXT_MAXLNG IS NULL))
	 ,CONSTRAINT DOMA_ExDep2
    CHECK ( DOMA_TYPE != 'DAT'
 OR ( DOMA_BIN_CONTENTTYPE IS NULL AND DOMA_BIN_STFO_ID IS NULL AND DOMA_NUM_FRACT_DIGITS IS NULL
	 AND DOMA_NUM_MAXVALUE IS NULL AND DOMA_NUM_MINVALUE IS NULL AND DOMA_NUM_PHYU_ID IS NULL AND DOMA_NUM_ROUND_VALUE IS NULL
	 AND DOMA_NUM_TOTAL_DIGITS IS NULL AND DOMA_DAT_GRANULARITY IS NOT NULL AND DOMA_TXT_SYNTAXRULE IS NULL AND DOMA_TXT_MAXLNG IS NULL))
	 ,CONSTRAINT DOMA_ExDep3
    CHECK ( DOMA_TYPE != 'GRP'
 OR ( DOMA_BIN_CONTENTTYPE IS NULL AND DOMA_BIN_STFO_ID IS NULL AND DOMA_NUM_FRACT_DIGITS IS NULL AND DOMA_NUM_MAXVALUE IS NULL AND DOMA_NUM_MINVALUE IS NULL AND DOMA_NUM_PHYU_ID IS NULL AND DOMA_NUM_ROUND_VALUE IS NULL AND DOMA_NUM_TOTAL_DIGITS IS NULL AND DOMA_DAT_GRANULARITY IS NULL AND DOMA_DAT_MAXVALUE IS NULL AND DOMA_DAT_MINVALUE IS NULL AND DOMA_TXT_SYNTAXRULE IS NULL AND DOMA_TXT_MAXLNG IS NULL))
 ,CONSTRAINT DOMA_ExDep4
    CHECK ( DOMA_TYPE != 'LOV'
 OR ( DOMA_BIN_CONTENTTYPE IS NULL AND DOMA_BIN_STFO_ID IS NULL AND DOMA_NUM_FRACT_DIGITS IS NULL AND DOMA_NUM_MAXVALUE IS NULL AND DOMA_NUM_MINVALUE IS NULL AND DOMA_NUM_PHYU_ID IS NULL AND DOMA_NUM_ROUND_VALUE IS NULL AND DOMA_NUM_TOTAL_DIGITS IS NULL AND DOMA_DAT_GRANULARITY IS NULL AND DOMA_DAT_MAXVALUE IS NULL AND DOMA_DAT_MINVALUE IS NULL AND DOMA_TXT_SYNTAXRULE IS NULL AND DOMA_TXT_MAXLNG IS NULL))
 ,CONSTRAINT DOMA_ExDep5
    CHECK ( DOMA_TYPE != 'NUM'
 OR ( DOMA_BIN_CONTENTTYPE IS NULL AND DOMA_BIN_STFO_ID IS NULL AND DOMA_NUM_FRACT_DIGITS IS NOT NULL AND DOMA_NUM_TOTAL_DIGITS IS NOT NULL AND DOMA_DAT_GRANULARITY IS NULL AND DOMA_DAT_MAXVALUE IS NULL AND DOMA_DAT_MINVALUE IS NULL AND DOMA_TXT_SYNTAXRULE IS NULL AND DOMA_TXT_MAXLNG IS NULL))
 , CONSTRAINT DOMA_ExDep6
    CHECK ( DOMA_TYPE != 'TXT'
 OR ( DOMA_BIN_CONTENTTYPE IS NULL AND DOMA_BIN_STFO_ID IS NULL AND DOMA_NUM_FRACT_DIGITS IS NULL AND DOMA_NUM_MAXVALUE IS NULL AND DOMA_NUM_MINVALUE IS NULL AND DOMA_NUM_PHYU_ID IS NULL AND DOMA_NUM_ROUND_VALUE IS NULL AND DOMA_NUM_TOTAL_DIGITS IS NULL AND DOMA_DAT_GRANULARITY IS NULL AND DOMA_DAT_MAXVALUE IS NULL AND DOMA_DAT_MINVALUE IS NULL))
 ,CONSTRAINT DOMA_NAME_UK UNIQUE (DOMA_NAME ASC)
 ,CONSTRAINT DOMA_MODE_FK FOREIGN KEY (     DOMA_ID)
	 REFERENCES MODELELEMENT (     MODE_ID )
 ON DELETE CASCADE
 ,CONSTRAINT DOMA_PHYU_FK FOREIGN KEY (     DOMA_NUM_PHYU_ID)
	 REFERENCES PHYSICAL_UNIT (     PHYU_ID )
 ,CONSTRAINT DOMA_daty_FK FOREIGN KEY (     DOMA_DATY_ID)
		 REFERENCES DATATYPES (DATY_ID )
 ,CONSTRAINT DOMA_STFO_FK FOREIGN KEY (     DOMA_BIN_STFO_ID)
	 REFERENCES STORAGE_FORMATS (     STFO_ID )
);
CREATE TABLE ENTITIES
    (
     ENTI_ID integer NOT NULL  primary key,
     ENTI_NAME VARCHAR (60) NOT NULL ,
     ENTI_SHORT_NAME VARCHAR (15) NULL ,
     ENTI_PREFIX VARCHAR (5) NULL ,
     ENTI_TOOLTIP VARCHAR (4000) NULL ,
     ENTI_DESCR VARCHAR (4000) NULL ,
     ENTI_EXP_TUPLECNT VARCHAR (500) NULL ,
     ENTI_UC VARCHAR(30) NULL  ,
     ENTI_DC VARCHAR (30) NOT NULL ,
     ENTI_UM VARCHAR (30) NULL ,
     ENTI_DM VARCHAR (30) NULL
    ,CONSTRAINT ENTI_NAME_UK UNIQUE (ENTI_NAME ASC)
    ,CONSTRAINT ENTI_MODE_FK FOREIGN KEY    (     ENTI_ID)
		REFERENCES MODELELEMENT    (     MODE_ID )
    ON DELETE CASCADE
);
CREATE TABLE EXTERNAL_REFS
    (
     EXTR_ID INTEGER NOT NULL primary key autoincrement,
     EXTR_SOURCE_NAME VARCHAR (60) NOT NULL ,
     EXTR_SOURCE_ID VARCHAR (100) NOT NULL ,
     EXTR_MODE_ID integer NOT NULL
     ,CONSTRAINT EXTR_UK UNIQUE (EXTR_SOURCE_NAME ASC, EXTR_MODE_ID ASC)
     ,CONSTRAINT EXTR_UK_ID UNIQUE (EXTR_SOURCE_NAME ASC, EXTR_SOURCE_ID ASC)
    ,CONSTRAINT EXTR_MODE_FK FOREIGN KEY
    (     EXTR_MODE_ID)
    REFERENCES MODELELEMENT
    (     MODE_ID )
    ON DELETE CASCADE
    ON UPDATE NO ACTION
    );

	CREATE TABLE DATATYPES 
	    (
	     DATY_ID INTEGER NOT NULL primary key , 
	     DATY_NAME VARCHAR (60) NOT NULL , 
	     DATY_BASETYPE VARCHAR (60) NOT NULL CONSTRAINT DATY_BASETYPE_CK CHECK ( DATY_BASETYPE IN ('BINARY', 'NUMERIC', 'STRING', 'DATETIME') ) , 
	     DATY_UC VARCHAR (30) , 
	     DATY_DC VARCHAR (30) NOT NULL , 
	     DATY_UM VARCHAR (30) NULL , 
	     DATY_DM VARCHAR (30) NULL 
		 ,CONSTRAINT DATY_MODE_FK FOREIGN KEY (DATY_ID) 
			REFERENCES MODELELEMENT (MODE_ID ) 
			ON DELETE CASCADE 
		);


CREATE TABLE KEY_ELEMENTS
    (
     KELE_ID INTEGER NOT NULL primary key autoincrement,
     KELE_KEYS_ID integer NOT NULL ,
     KELE_ATTR_ID integer NULL ,
     KELE_RELA_ID integer NULL ,
     KELE_UC VARCHAR(30) NOT NULL  ,
     KELE_DC VARCHAR (30) NOT NULL ,
     KELE_UM VARCHAR (30) NULL ,
     KELE_DM VARCHAR (30) NULL
,CONSTRAINT FKArc_8 CHECK 
		(( (KELE_RELA_ID IS NOT NULL) AND
		   (KELE_ATTR_ID IS NULL) 
	     ) OR (  (KELE_ATTR_ID IS NOT NULL) AND
                 (KELE_RELA_ID IS NULL) ) 
		 )
	    ,CONSTRAINT KELE_ATTR_FK FOREIGN KEY (     KELE_ATTR_ID)
			 REFERENCES ATTRIBUTES  (     ATTR_ID )
			 ON DELETE CASCADE
	     ,CONSTRAINT KELE_KEYS_FK FOREIGN KEY	     (     KELE_KEYS_ID)
			 REFERENCES KEYS	     (     KEYS_ID )
			 ON DELETE CASCADE
	     ,CONSTRAINT KELE_RELA_FK FOREIGN KEY	     (     KELE_RELA_ID)
			 REFERENCES RELATIONS	     (     RELA_ID )
			 ON DELETE CASCADE
      ,CONSTRAINT KELE_UN UNIQUE (KELE_KEYS_ID ASC, KELE_ATTR_ID ASC, KELE_RELA_ID ASC)
);


CREATE TABLE KEYS
    (
     KEYS_ID INTEGER NOT NULL primary key autoincrement,
     KEYS_NAME VARCHAR (60) NOT NULL ,
     KEYS_ENTI_ID integer NOT NULL ,
     KEYS_UC VARCHAR(30) NOT NULL  ,
     KEYS_DC VARCHAR (30) NOT NULL ,
     KEYS_UM VARCHAR (30) NULL ,
     KEYS_DM VARCHAR (30) NULL
    ,CONSTRAINT KEYS_UK UNIQUE (KEYS_ENTI_ID ASC, KEYS_NAME ASC)
    ,CONSTRAINT KEYS_ENTI_FK FOREIGN KEY    (     KEYS_ENTI_ID)
		REFERENCES ENTITIES    (     ENTI_ID )    ON DELETE CASCADE
);
CREATE TABLE LANG_TEXTS
    (
     LGTX_ID INTEGER NOT NULL primary key autoincrement ,
     LGTX_ATTRNAME VARCHAR (60) NOT NULL ,
     LGTX_TEXT VARCHAR (4000) NULL ,
     LGTX_LANG_ID integer NOT NULL ,
     LGTX_MODE_ID integer NOT NULL ,
     LGTX_UC VARCHAR(30) NULL  ,
     LGTX_DC VARCHAR (30) NOT NULL ,
     LGTX_UM VARCHAR (30) NULL ,
     LGTX_DM VARCHAR (30) NULL
    ,CONSTRAINT LGTX_UK UNIQUE (LGTX_LANG_ID ASC, LGTX_MODE_ID ASC, LGTX_ATTRNAME ASC)
	,CONSTRAINT LGTX_LANG_FK FOREIGN KEY    (     LGTX_LANG_ID)
    	REFERENCES LANGUAGES    (     LANG_ID )
    ,CONSTRAINT LGTX_MODE_FK FOREIGN KEY    (     LGTX_MODE_ID)
		REFERENCES MODELELEMENT    (     MODE_ID )    ON DELETE CASCADE
);
CREATE TABLE LANGUAGES
    (
     LANG_ID INTEGER NOT NULL primary key autoincrement,
     LANG_ISO_NAME VARCHAR (60) NULL ,
     LANG_ISO_CODE2 CHAR (2) NOT NULL CONSTRAINT LANG_ISO2_CHK CHECK ( LANG_ISO_CODE2 = lower(LANG_ISO_CODE2) ) ,
     LANG_ISO_CODE3 CHAR (3) NOT NULL CONSTRAINT LANG_ISO3_CHK CHECK ( LANG_ISO_CODE3 = lower(LANG_ISO_CODE3) ) ,
     LANG_IS_TEXT_LANG VARCHAR (5) NOT NULL CHECK ( LANG_IS_TEXT_LANG IN ('FALSE', 'TRUE') ) ,
     LANG_IS_BASE_LANG VARCHAR (5) NOT NULL CHECK ( LANG_IS_BASE_LANG IN ('FALSE', 'TRUE') ) ,
     LANG_LANG_ID integer NULL ,
     LANG_UC VARCHAR(30) NULL  ,
     LANG_DC VARCHAR (30) NOT NULL ,
     LANG_UM VARCHAR (30) NULL ,
     LANG_DM VARCHAR (30) NULL
    ,CONSTRAINT LANG_ISO_NAME_UN UNIQUE (LANG_ISO_NAME ASC)
      ,CONSTRAINT LANG_ISO_CODE2_UN UNIQUE (LANG_ISO_CODE2 ASC)
      ,CONSTRAINT LANG_ISO_CODE3_UN UNIQUE (LANG_ISO_CODE3 ASC)
      ,CONSTRAINT LANG_REPLACE_FK FOREIGN KEY      (     LANG_LANG_ID)
      REFERENCES LANGUAGES      (     LANG_ID )      ON DELETE SET NULL
  );
CREATE TABLE MODE_DOCU
    (
     MODO_ID INTEGER NOT NULL primary key autoincrement,
     MODO_MODE_ID integer NOT NULL ,
     MODO_DOCU_ID integer NOT NULL
    ,CONSTRAINT MODO_UK UNIQUE (MODO_MODE_ID ASC, MODO_DOCU_ID ASC)
    ,CONSTRAINT MODO_DOCU_FK FOREIGN KEY
    (     MODO_DOCU_ID)
    REFERENCES DOCUMENTS
    (     DOCU_ID )
    ON DELETE CASCADE
    ON UPDATE NO ACTION
    ,CONSTRAINT MODO_MODE_FKv2 FOREIGN KEY
    (     MODO_MODE_ID)
    REFERENCES MODELELEMENT
    (     MODE_ID )
    ON DELETE CASCADE
    ON UPDATE NO ACTION
    );
CREATE TABLE MODELELEM_TYPE
    (
     MELT_ID INTEGER NOT NULL primary key autoincrement,
     MELT_SHORTNAME VARCHAR (4) NOT NULL CHECK ( MELT_SHORTNAME IN ('ARCS', 'ATTR', 'BURU', 'COLU', 'DOMA', 'ENTI'
                            , 'INTF', 'ORGU', 'RELA', 'SYNO', 'TABL','DOCU','KEYS','DATY','DGRM') ) ,
     MELT_NAME VARCHAR (60) NOT NULL ,
     MELT_UC VARCHAR(30) NULL  ,
     MELT_DC VARCHAR (30) NOT NULL ,
     MELT_UM VARCHAR (30) NULL ,
     MELT_DM VARCHAR (30) NULL
    ,CONSTRAINT MELT_UN UNIQUE (MELT_SHORTNAME ASC)
    ,CONSTRAINT MELT_UN2 UNIQUE (MELT_NAME ASC)
);
CREATE TABLE MODELELEMENT
    (
     MODE_ID INTEGER NOT NULL primary key autoincrement ,
     MODE_TYPE VARCHAR (4) NOT NULL CHECK ( MODE_TYPE IN ('ARCS', 'ATTR', 'BURU', 'COLU', 'DOMA', 'ENTI'
                            , 'INTF', 'ORGU', 'RELA', 'SYNO', 'TABL','DOCU','KEYS','DATY','DGRM','DIAG') ) ,
     MODE_MELT_ID integer NOT NULL
     ,CONSTRAINT MODE_MELT_FK FOREIGN KEY
     (     MODE_MELT_ID)
     REFERENCES MODELELEM_TYPE
     (     MELT_ID )
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
    );


CREATE TABLE MODELEMTYPE_PROPERTIES
    (
     METP_ID INTEGER NOT NULL primary key autoincrement,
     METP_MELT_ID integer NOT NULL ,
     METP_UDPR_ID integer NOT NULL ,
     METP_OPTIONAL VARCHAR (5) NOT NULL CHECK ( METP_OPTIONAL IN ('FALSE', 'TRUE') )
    ,CONSTRAINT METP_UN UNIQUE (METP_MELT_ID ASC, METP_UDPR_ID ASC)
    ,CONSTRAINT METP_MELT_FK FOREIGN KEY    (     METP_MELT_ID)
		REFERENCES MODELELEM_TYPE    (     MELT_ID )
    ,CONSTRAINT METP_UDPR_FK FOREIGN KEY    (     METP_UDPR_ID)
		REFERENCES USER_DEFINED_PROPERTIES    (     UDPR_ID )
    );
CREATE TABLE PHYSICAL_UNIT
    (
     PHYU_ID INTEGER NOT NULL primary key autoincrement,
     PHYU_SI_UNIT VARCHAR (10) NOT NULL ,
     PHYU_NAME VARCHAR (60) NULL ,
     PHYU_DESCR VARCHAR (4000) NULL ,
     PHYU_UC VARCHAR (30) NOT NULL ,
     PHYU_DC VARCHAR (30) NOT NULL ,
     PHYU_UM VARCHAR (30) NULL ,
     PHYU_DM VARCHAR (30) NULL
     ,CONSTRAINT PHYU_UK_NAME UNIQUE (PHYU_NAME ASC)
 );
CREATE TABLE RELATIONS
    (
     RELA_ID integer NOT NULL  primary key,
     RELA_NAME VARCHAR (60) NOT NULL ,
     RELA_TYPE VARCHAR (4) NOT NULL CHECK ( RELA_TYPE IN ('1:1', 'ISAR', 'ISAS', 'M:1', 'M:N') ) ,
     RELA_ENTI_ID_FROM integer NOT NULL ,
     RELA_ARCS_ID_FROM integer  ,
     RELA_ASSOC_FROM_TO VARCHAR (4000) NULL ,
     RELA_MAPTYPE_FROM_TO CHAR (1) NOT NULL CHECK ( RELA_MAPTYPE_FROM_TO IN ('1', 'M') ) ,
     RELA_MANDATORY_FROM_TO VARCHAR (5) NOT NULL  
   		CHECK(RELA_MANDATORY_FROM_TO IN('FALSE','TRUE')),
     RELA_HIST_FROM_TO VARCHAR (5) NOT NULL 
   		CHECK(RELA_HIST_FROM_TO IN('FALSE','TRUE')),
     RELA_ENTI_ID_TO integer NOT NULL ,
     RELA_ARCS_ID_TO integer  ,
     RELA_ASSOC_TO_FROM VARCHAR (100) NULL ,
     RELA_MAPTYPE_TO_FROM CHAR (1) NOT NULL CHECK ( RELA_MAPTYPE_TO_FROM IN ('1', 'M') ) ,
     RELA_MANDATORY_TO_FROM VARCHAR (5) NOT NULL  
   		CHECK(RELA_MANDATORY_TO_FROM IN('FALSE','TRUE')),
     RELA_HIST_TO_FROM VARCHAR (4000) NOT NULL 
   		CHECK(RELA_HIST_TO_FROM IN('FALSE','TRUE')),
     RELA_UC VARCHAR(30) NULL  ,
     RELA_DC VARCHAR (30) NOT NULL ,
     RELA_UM VARCHAR (30) NULL ,
     RELA_DM VARCHAR (30) NULL ,
     CONSTRAINT RELA_MAPTYPE_CHK CHECK ((RELA_TYPE = 'ISAR'
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
)
)
    ,CONSTRAINT RELA_UK1 UNIQUE (RELA_ENTI_ID_FROM ASC, RELA_ENTI_ID_TO ASC, RELA_TYPE ASC, RELA_ASSOC_TO_FROM ASC, RELA_ASSOC_FROM_TO ASC)
    ,CONSTRAINT RELA_UK_NAME UNIQUE (RELA_NAME ASC)
    ,CONSTRAINT RELA_ARCS_FROM_FK FOREIGN KEY
    (     RELA_ARCS_ID_FROM)
    REFERENCES ARCS
    (     ARCS_ID )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    ,CONSTRAINT RELA_ARCS_TO_FK FOREIGN KEY
    (     RELA_ARCS_ID_TO)
    REFERENCES ARCS
    (     ARCS_ID )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    ,CONSTRAINT RELA_ENTI_FROM_FK FOREIGN KEY
    (     RELA_ENTI_ID_FROM)
    REFERENCES ENTITIES
    (     ENTI_ID )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    ,CONSTRAINT RELA_ENTI_TO_FK FOREIGN KEY
    (     RELA_ENTI_ID_TO)
    REFERENCES ENTITIES
    (     ENTI_ID )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    ,CONSTRAINT RELA_MODE_FK FOREIGN KEY
    (     RELA_ID)
    REFERENCES MODELELEMENT
    (     MODE_ID )
    ON DELETE CASCADE
    ON UPDATE NO ACTION
);
CREATE TABLE STORAGE_FORMATS
    (
     STFO_ID INTEGER NOT NULL primary key autoincrement,
     STFO_NAME VARCHAR (60) NOT NULL ,
     STFO_DESCR VARCHAR (4000) NULL ,
     STFO_UC VARCHAR (30) NOT NULL ,
     STFO_DC VARCHAR (30) NOT NULL ,
     STFO_UM VARCHAR (30) NULL ,
     STFO_DM VARCHAR (30) NULL
    ,CONSTRAINT STFO_UN UNIQUE (STFO_NAME ASC)
    );
CREATE TABLE SYNONYMS
    (
     SYNO_ID INTEGER NOT NULL primary key,
     SYNO_NAME VARCHAR (60) NOT NULL ,
     SYNO_ENTI_ID integer NOT NULL ,
     SYNO_UC VARCHAR(30) NULL  ,
     SYNO_DC VARCHAR (30) NOT NULL ,
     SYNO_UM VARCHAR (30) NULL ,
     SYNO_DM VARCHAR (30) NULL
     ,CONSTRAINT SYNO_ENTI_FK FOREIGN KEY     (     SYNO_ENTI_ID)
		 REFERENCES ENTITIES     (     ENTI_ID )
		 ON DELETE CASCADE
     ,CONSTRAINT SYNO_MODE_FK FOREIGN KEY     (     SYNO_ID)
		 REFERENCES MODELELEMENT     (     MODE_ID )
		 ON DELETE CASCADE
    );


CREATE TABLE UDP_VALUES
    (
     UDPV_ID INTEGER NOT NULL primary key autoincrement,
     UDPV_VALUE VARCHAR (4000)  pNULL ,
     UDPV_MODE_ID integer NOT NULL ,
     UDPV_UDPR_ID integer NOT NULL ,
     UDPV_UC VARCHAR (30) NOT NULL ,
     UDPV_DC VARCHAR (30) NOT NULL ,
     UDPV_UM VARCHAR (30) NULL ,
     UDPV_DM VARCHAR (30) NULL
    ,CONSTRAINT UDPV_UN UNIQUE (UDPV_MODE_ID ASC, UDPV_UDPR_ID ASC)
    ,CONSTRAINT UDPV_MODE_FK FOREIGN KEY    (     UDPV_MODE_ID)
		REFERENCES MODELELEMENT    (     MODE_ID )
    ON DELETE CASCADE
    ,CONSTRAINT UDPV_UDPR_FK FOREIGN KEY    (     UDPV_UDPR_ID)
		REFERENCES USER_DEFINED_PROPERTIES    (     UDPR_ID )
    );
CREATE TABLE USER_DEFINED_PROPERTIES
    (
     UDPR_ID INTEGER NOT NULL primary key autoincrement ,
     UDPR_THEME VARCHAR (60) NULL ,
     UDPR_GROUP VARCHAR (60) NULL ,
     UDPR_NAME VARCHAR (60) NOT NULL ,
     UDPR_DESCR VARCHAR (4000) NULL ,
     UDPR_UC VARCHAR (30) NOT NULL ,
     UDPR_DC VARCHAR (30) NOT NULL ,
     UDPR_UM VARCHAR (30) NULL ,
     UDPR_DM VARCHAR (30) NULL
    ,CONSTRAINT UDPR_UN UNIQUE (UDPR_NAME ASC)
    );

create view SUPERENTI AS 
    select superentity.enti_id as superenti_id, superentity.enti_name as super_enti_name
    ,subentity.enti_id as subenti_id, subentity.enti_name as sub_enti_name
from ENTITIES superentity
 join ARCS on ARCS_ENTI_ID = superentity.enti_id
 join (select rela_id
            ,case when RELA_ARCS_ID_FROM is NULL then RELA_ARCS_ID_TO else RELA_ARCS_ID_FROM end as rela_arcs_id
            ,case when RELA_ARCS_ID_FROM is NULL then  RELA_ENTI_ID_TO else RELA_ENTI_ID_FROM end as rela_enti_id
            from relations
            where RELA_TYPE = 'ISAS') relas on RELA_ARCS_ID= arcs_id
join ENTITIES subentity on subentity.ENTI_ID = rela_enti_id
;

CREATE TABLE diagramtypes(
    diat_id    integer primary key autoincrement,
    diat_name   varchar(100) NOT NULL,
     diat_uc varchar(30) NOT NULL,
    diat_dc    varchar(30) NOT NULL,
    diat_um    varchar(30) ,
    diat_dm    varchar(30),
	CONSTRAINT diat_un UNIQUE(diat_name)
)

CREATE TABLE diagrams(
    diag_id      integer primary key autoincrement,
    diag_name      varchar(60) NOT NULL,
    diag_diat_id   integer NOT NULL,
    diag_legendx       integer,
    diag_legendy       integer,
    diag_uc    varchar(30) NOT NULL,
    diag_dc        varchar(30) NOT NULL,
    diag_um        varchar(30) ,
    diag_dm        varchar(30),
	CONSTRAINT diag__un UNIQUE(diag_name),
	CONSTRAINT diag_diat_fk FOREIGN KEY(diag_diat_id)
			REFERENCES diagramtypes(diat_id)
	,CONSTRAINT DIAGRAMS_MODELELEMENT_FK FOREIGN KEY (DIAG_ID) 
       REFERENCES MODELELEMENT (MODE_ID )ON DELETE CASCADE
;

CREATE TABLE melt_diats(
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
		REFERENCES diagramtypes(diat_id)
		ON DELETE CASCADE,
	CONSTRAINT modi_melt_fk FOREIGN KEY(medi_melt_id)
		REFERENCES modelelem_type(melt_id)
		 ON DELETE CASCADE
);

CREATE TABLE elementreps(
	  eler_id               integer primary key autoincrement,
      eler_mode_id          integer NOT NULL,
      eler_diag_id          integer NOT NULL,
      eler_index            NUMBER(4)DEFAULT 0 NOT NULL,
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
);

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
);

CREATE TABLE linesegments(
    lise_id          integer primary key autoincrement,
    lise_seq        integer NOT NULL,
    lise_relr_id     integer NOT NULL,
    lise_x           integer NOT NULL
        CONSTRAINT ck_relr_relr_fontcolor CHECK(lise_x BETWEEN 0 AND 999999) ,
    lise_y           integer NOT NULL
        CONSTRAINT ck_relr_relr_fontcolor CHECK(lise_y BETWEEN 0 AND 999999) ,
    lise_linetyp   VARCHAR2(6)NULL
        CONSTRAINT ck_lise_linetype CHECK(lise_linetyp IN(
            'DADO',
            'DASHED',
            'DOTTED',
            'SOLID'
        )),
	lise_angle 	 integer,
    lise_uc       varchar(30) NOT NULL,
    lise_dc           varchar(30) NOT NULL,
    lise_um           varchar(30) ,
    lise_dm           varchar(30),
	CONSTRAINT lise__un UNIQUE(lise_relr_id,lise_rhfg),
	CONSTRAINT lise_relr_fk FOREIGN KEY(lise_relr_id)
	      REFERENCES relationreps(relr_id)
	            ON DELETE CASCADE
);

CREATE TABLE schnittstellen
    (
     SCHN_ID integer primary key autoincrement, 
     SCHN_NAME VARCHAR (60) NOT NULL , 
     SCHN_BESCHR VARCHAR (4000)  , 
 	 SCHN_odm_guid	varchar(36),
     SCHN_UC VARCHAR (30) NOT NULL , 
     SCHN_DC VARCHAR (30) NOT NULL , 
     SCHN_UM VARCHAR (30) NULL , 
     SCHN_DM VARCHAR (30) NULL ,
 CONSTRAINT SCHN_UN UNIQUE (SCHN_NAME)
    );

CREATE TABLE tabellen
    (
     tabl_id integer primary key autoincrement , 
     tabl_name varchar (60) not null , 
     tabl_schn_id integer not null , 
     tabl_prefix varchar (60) null , 
     tabl_beschr varchar (4000) null , 
 	 tabl_odm_guid	varchar(36),
     tabl_uc varchar (30) not null , 
     tabl_dc varchar (30) not null , 
     tabl_um varchar (30) null , 
     tabl_dm varchar (30) null ,
	  CONSTRAINT TABL_UN UNIQUE (TABL_SCHN_ID , TABL_NAME)
 	   ,CONSTRAINT TABL_SCHN_FK FOREIGN KEY (TABL_SCHN_ID) 
 	      REFERENCES SCHNITTSTELLEn (SCHN_ID ) 
    );
create table schnittstelle_attrs
(
    scha_id             integer primary key ,
    scha_column_name    varchar(60) not null,
    scha_format         varchar(200),
    scha_fremdsystem_id varchar(100),
    scha_beschr         varchar(4000),
    scha_type_string    varchar(200),
    scha_tabl_id        integer     not null,
    scha_daty_id        integer     not null,
    scha_doma_id        integer ,
    scha_uc             varchar(30) not null,
    scha_dc             varchar(30) not null,
    scha_um             varchar(30),
    scha_dm             varchar(30),
    constraint scha_daty_fk FOREIGN KEY (scha_daty_id) references datatypes (daty_id),
    constraint scha_doma_fk FOREIGN KEY (scha_doma_id) references domains (doma_id),
    constraint scha_tabl_fk FOREIGN KEY (scha_tabl_id) references tabellen(tabl_id),
    constraint scha_uk unique (scha_tabl_id,scha_column_name)        
    );
	
 create table tabl_enti_maps 
 (
  tema_id integer primary key autoincrement , 
  tema_tabl_id integer not null , 
  tema_enti_id integer null , 
  tema_rela_id integer null , 
  constraint tema_ck check ((tema_enti_id is not null and tema_rela_id is null )
      	        		  or (tema_enti_id is null and tema_rela_id is not null)),
		   constraint tema_un unique (tema_tabl_id , tema_enti_id ,tema_rela_id)
	   ,constraint tema_bezi_fk foreign key (tema_rela_id) 
	      references relations (rela_id ) 
	   ,constraint tema_enti_fk foreign key (tema_enti_id) 
	      references entities (enti_id ) 
	   ,constraint tema_tabl_fk foreign key (tema_tabl_id) 
	      references tabellen (tabl_id ) 
 );
 
create view langattr as
select lgtx_text,lang_id,lang_iso_code2,lgtx_mode_id,lgtx_attrname
  from lang_texts 
  join languages on lang_id = lgtx_lang_id
