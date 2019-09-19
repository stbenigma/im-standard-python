
CREATE TABLE sprache(
    spra_iso_name          VARCHAR2(60 CHAR)NULL,
    spra_uetx_id_name      NUMBER(10)NULL,
    spra_iso_code2         CHAR(2 CHAR)NOT NULL
        CHECK(spra_iso_code2 = lower(spra_iso_code2))NOT DEFERRABLE ENABLE VALIDATE,
    spra_iso_code3         CHAR(3 CHAR)NOT NULL
        CHECK(spra_iso_code3 = lower(spra_iso_code3))NOT DEFERRABLE ENABLE VALIDATE,
    spra_ist_textsprache   VARCHAR2(5 CHAR)NOT NULL
        CHECK(spra_ist_textsprache IN(
            'FALSE',
            'TRUE'
        ))NOT DEFERRABLE ENABLE VALIDATE,
    spra_id                NUMBER(10)DEFAULT infra_seq.NEXTVAL NOT NULL,
    spra_spra_id           NUMBER(10)NULL,
    spra_uc                VARCHAR2(30 BYTE)NOT NULL,
    spra_dc                TIMESTAMP WITH LOCAL TIME ZONE NOT NULL,
    spra_um                VARCHAR2(30 BYTE)NULL,
    spra_dm                TIMESTAMP WITH LOCAL TIME ZONE NULL
)
ORGANIZATION HEAP NOCOMPRESS
    NOCACHE
        NOPARALLEL
    NOROWDEPENDENCIES DISABLE ROW MOVEMENT;

PROMPT CREATING INDEX 'SPRA__IDX';

CREATE INDEX spra__idx ON
    sprache(
        spra_spra_id
    ASC);

PROMPT CREATING PRIMARY KEY ON 'SPRACHE';
ALTER TABLE sprache
    ADD CONSTRAINT spra_pk PRIMARY KEY(spra_id)NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING UNIQUE KEY ON 'SPRACHE';

ALTER TABLE sprache
    ADD CONSTRAINT spra_iso_name_un UNIQUE(spra_iso_name)NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING UNIQUE KEY ON 'SPRACHE';

ALTER TABLE sprache
    ADD CONSTRAINT spra_iso_code2_un UNIQUE(spra_iso_code2)NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING UNIQUE KEY ON 'SPRACHE';

ALTER TABLE sprache
    ADD CONSTRAINT spra_iso_code3_un UNIQUE(spra_iso_code3)NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING TABLE 'SPRACHTEXT';
CREATE TABLE sprachtext(
    sptx_text         VARCHAR2(4000 CHAR)NOT NULL,
    sptx_gueltig_ab   TIMESTAMP NOT NULL,
    sptx_id           NUMBER(10)DEFAULT infra_seq.NEXTVAL NOT NULL,
    sptx_spra_id      NUMBER(10)NOT NULL,
    sptx_uetx_id      NUMBER(10)NOT NULL,
    sptx_uc           VARCHAR2(30 BYTE)NOT NULL,
    sptx_dc           TIMESTAMP WITH LOCAL TIME ZONE NOT NULL,
    sptx_um           VARCHAR2(30 BYTE)NULL,
    sptx_dm           TIMESTAMP WITH LOCAL TIME ZONE NULL
)
ORGANIZATION HEAP NOCOMPRESS
    NOCACHE
        NOPARALLEL
    NOROWDEPENDENCIES DISABLE ROW MOVEMENT;

PROMPT CREATING INDEX 'SPTX__IDX';

CREATE INDEX sptx__idx ON
    sprachtext(
        sptx_spra_id
    ASC);

PROMPT CREATING INDEX 'SPTX__IDXv1';

CREATE INDEX sptx__idxv1 ON
    sprachtext(
        sptx_uetx_id
    ASC);

PROMPT CREATING PRIMARY KEY ON 'SPRACHTEXT';
ALTER TABLE sprachtext
    ADD CONSTRAINT sptx_pk PRIMARY KEY(sptx_id)NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING UNIQUE KEY ON 'SPRACHTEXT';

ALTER TABLE sprachtext
    ADD CONSTRAINT sptx_glt_ab_uk UNIQUE(sptx_spra_id,
                                         sptx_uetx_id,
                                         sptx_gueltig_ab)NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING TABLE 'UEBERSETZ_TEXT';
CREATE TABLE uebersetz_text(
    uetx_originaltext   VARCHAR2(4000 CHAR)NOT NULL,
    uetx_id             NUMBER(10)DEFAULT infra_seq.NEXTVAL NOT NULL,
    uetx_spra_id        NUMBER(10)NOT NULL,
    uetx_wrtb_id        NUMBER(10)NULL,
    uetx_uc             VARCHAR2(30 BYTE)NOT NULL,
    uetx_dc             TIMESTAMP WITH LOCAL TIME ZONE NOT NULL,
    uetx_um             VARCHAR2(30 BYTE)NULL,
    uetx_dm             TIMESTAMP WITH LOCAL TIME ZONE NULL
)
ORGANIZATION HEAP NOCOMPRESS
    NOCACHE
        NOPARALLEL
    NOROWDEPENDENCIES DISABLE ROW MOVEMENT;

PROMPT CREATING INDEX 'UETX_IDX_SPRA';

CREATE INDEX uetx_idx_spra ON
    uebersetz_text(
        uetx_spra_id
    ASC);

PROMPT CREATING INDEX 'UETX_IDX_TXT';

CREATE INDEX uetx_idx_txt ON
    uebersetz_text(
        uetx_wrtb_id
    ASC);

PROMPT CREATING PRIMARY KEY ON 'UEBERSETZ_TEXT';
ALTER TABLE uebersetz_text
    ADD CONSTRAINT uetx_pk PRIMARY KEY(uetx_id)NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING TABLE 'WERTEBEREICH';
CREATE TABLE wertebereich(
    wrtb_id                   NUMBER(10)DEFAULT modm_seq.NEXTVAL NOT NULL,
    wrtb_business_rule        VARCHAR2(4000 CHAR)NULL,
    wrtb_uetx_id_name         NUMBER(10)NOT NULL,
    wrtb_uetx_id_beschr       NUMBER(10)NULL,
    wrtb_typ                  VARCHAR2(4 CHAR)NOT NULL
        CHECK(wrtb_typ IN(
            'BIN',
            'GRP',
            'LOV',
            'NUM',
            'TEXT',
            'ZPKT'
        ))NOT DEFERRABLE ENABLE VALIDATE,
    wrtb_zpkt_minwert         TIMESTAMP NULL,
    wrtb_zpkt_maxwert         TIMESTAMP NULL,
    wrtb_zpkt_granularitaet   VARCHAR2(15 CHAR)NULL
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
        ))NOT DEFERRABLE ENABLE VALIDATE,
    wrtb_text_maxlng          NUMBER(4)NULL,
    wrtb_text_syntaxregel     VARCHAR2(4000 CHAR)NULL,
    wrtb_num_maxwert          NUMBER(30,10)NULL,
    wrtb_num_minwert          NUMBER(30,10)NULL,
    wrtb_num_vorkstellen      NUMBER(2)NULL,
    wrtb_num_nachkstellen     NUMBER(2)DEFAULT 0 NULL,
    wrtb_num_rundng_einh      NUMBER(7,3)NULL
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
        ))NOT DEFERRABLE ENABLE VALIDATE,
    wrtb_num_pheh_id          NUMBER(10)NULL,
    wrtb_bin_inhalttyp        VARCHAR2(30 CHAR)NULL
        CHECK(wrtb_bin_inhalttyp IN(
            'BILD',
            'FILM',
            'GRAPH',
            'TEXT',
            'TON'
        ))NOT DEFERRABLE ENABLE VALIDATE,
    wrtb_bin_spfo_id          NUMBER(10)NULL,
    wrtb_uc                   VARCHAR2(30 BYTE)NOT NULL,
    wrtb_dc                   TIMESTAMP WITH LOCAL TIME ZONE NOT NULL,
    wrtb_um                   VARCHAR2(30 BYTE)NULL,
    wrtb_dm                   TIMESTAMP WITH LOCAL TIME ZONE NULL
)
ORGANIZATION HEAP NOCOMPRESS
    NOCACHE
        NOPARALLEL
    NOROWDEPENDENCIES DISABLE ROW MOVEMENT;

PROMPT CREATING INDEX 'WRTB_UETX_FK_NAME';

CREATE INDEX wrtb_uetx_fk_name ON
    wertebereich(
        wrtb_uetx_id_name
    ASC);

PROMPT CREATING CHECK CONSTRAINT ON 'WERTEBEREICH';
ALTER TABLE wertebereich
    ADD CONSTRAINT wrtb_ck_zpkt CHECK((wrtb_typ = 'ZPKT'
                                       AND wrtb_zpkt_granularitaet IS NOT NULL
                                       AND wrtb_text_maxlng IS NULL
                                       AND wrtb_text_syntaxregel IS NULL
                                       AND wrtb_num_vorkstellen IS NULL
                                       AND wrtb_num_nachkstellen IS NULL
                                       AND wrtb_num_rundng_einh IS NULL
                                       AND wrtb_num_minwert IS NULL
                                       AND wrtb_num_maxwert IS NULL
                                       AND wrtb_num_pheh_id IS NULL
                                       AND wrtb_bin_spfo_id IS NULL
                                       AND wrtb_bin_inhalttyp IS NULL)
                                      OR(wrtb_typ <> 'ZPKT'
                                         AND wrtb_zpkt_granularitaet IS NULL
                                         AND wrtb_zpkt_maxwert IS NULL
                                         AND wrtb_zpkt_minwert IS NULL))NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING CHECK CONSTRAINT ON 'WERTEBEREICH';

ALTER TABLE wertebereich
    ADD CONSTRAINT wrtb_ck_lov CHECK((wrtb_typ = 'LOV'
                                      AND wrtb_zpkt_granularitaet IS NULL
                                      AND wrtb_zpkt_maxwert IS NULL
                                      AND wrtb_zpkt_minwert IS NULL
                                      AND wrtb_text_maxlng IS NULL
                                      AND wrtb_text_syntaxregel IS NULL
                                      AND wrtb_num_vorkstellen IS NULL
                                      AND wrtb_num_nachkstellen IS NULL
                                      AND wrtb_num_rundng_einh IS NULL
                                      AND wrtb_num_minwert IS NULL
                                      AND wrtb_num_maxwert IS NULL
                                      AND wrtb_num_pheh_id IS NULL
                                      AND wrtb_bin_spfo_id IS NULL
                                      AND wrtb_bin_inhalttyp IS NULL)
                                     OR(wrtb_typ <> 'LOV'))NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING CHECK CONSTRAINT ON 'WERTEBEREICH';

ALTER TABLE wertebereich
    ADD CONSTRAINT wrtb_ck_text CHECK((wrtb_typ = 'TEXT'
                                       AND wrtb_zpkt_granularitaet IS NULL
                                       AND wrtb_zpkt_maxwert IS NULL
                                       AND wrtb_zpkt_minwert IS NULL
                                       AND wrtb_num_vorkstellen IS NULL
                                       AND wrtb_num_nachkstellen IS NULL
                                       AND wrtb_num_rundng_einh IS NULL
                                       AND wrtb_num_minwert IS NULL
                                       AND wrtb_num_maxwert IS NULL
                                       AND wrtb_num_pheh_id IS NULL
                                       AND wrtb_bin_spfo_id IS NULL
                                       AND wrtb_bin_inhalttyp IS NULL)
                                      OR(wrtb_typ <> 'TEXT'))NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING CHECK CONSTRAINT ON 'WERTEBEREICH';

ALTER TABLE wertebereich
    ADD CONSTRAINT wrtb_ck_num CHECK((wrtb_typ = 'NUM'
                                      AND wrtb_num_vorkstellen IS NOT NULL
                                      AND wrtb_num_nachkstellen IS NOT NULL
                                      AND wrtb_zpkt_granularitaet IS NULL
                                      AND wrtb_text_maxlng IS NULL
                                      AND wrtb_text_syntaxregel IS NULL)
                                     OR(wrtb_typ <> 'NUM'
                                        AND wrtb_num_vorkstellen IS NULL
                                        AND wrtb_num_nachkstellen IS NULL
                                        AND wrtb_num_rundng_einh IS NULL
                                        AND wrtb_num_minwert IS NULL
                                        AND wrtb_num_maxwert IS NULL
                                        AND wrtb_num_pheh_id IS NULL))NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING CHECK CONSTRAINT ON 'WERTEBEREICH';

ALTER TABLE wertebereich
    ADD CONSTRAINT wrtb_ck_grp CHECK((wrtb_typ = 'GRP'
                                      AND wrtb_zpkt_granularitaet IS NULL
                                      AND wrtb_zpkt_maxwert IS NULL
                                      AND wrtb_zpkt_minwert IS NULL
                                      AND wrtb_text_maxlng IS NULL
                                      AND wrtb_text_syntaxregel IS NULL
                                      AND wrtb_num_vorkstellen IS NULL
                                      AND wrtb_num_nachkstellen IS NULL
                                      AND wrtb_num_rundng_einh IS NULL
                                      AND wrtb_num_minwert IS NULL
                                      AND wrtb_num_maxwert IS NULL
                                      AND wrtb_num_pheh_id IS NULL)
                                     OR(wrtb_typ <> 'GRP'))NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING CHECK CONSTRAINT ON 'WERTEBEREICH';

ALTER TABLE wertebereich
    ADD CONSTRAINT wrtb_ck_bin CHECK((wrtb_typ = 'BIN'
                                      AND wrtb_bin_inhalttyp IS NOT NULL
                                      AND wrtb_zpkt_granularitaet IS NULL
                                      AND wrtb_zpkt_maxwert IS NULL
                                      AND wrtb_zpkt_minwert IS NULL
                                      AND wrtb_num_vorkstellen IS NULL
                                      AND wrtb_num_nachkstellen IS NULL
                                      AND wrtb_num_rundng_einh IS NULL
                                      AND wrtb_num_minwert IS NULL
                                      AND wrtb_num_maxwert IS NULL
                                      AND wrtb_num_pheh_id IS NULL)
                                     OR(wrtb_typ <> 'BIN'
                                        AND wrtb_bin_spfo_id IS NULL
                                        AND wrtb_bin_inhalttyp IS NULL))NOT DEFERRABLE ENABLE VALIDATE;
PROMPT CREATING PRIMARY KEY ON 'WERTEBEREICH';

ALTER TABLE wertebereich
    ADD CONSTRAINT wrtb_pk PRIMARY KEY(wrtb_id)NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING UNIQUE KEY ON 'WERTEBEREICH';

ALTER TABLE wertebereich
    ADD CONSTRAINT wrtb_name_uk UNIQUE(wrtb_uetx_id_name)NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING FOREIGN KEY ON 'SPRACHE';
ALTER TABLE sprache
    ADD CONSTRAINT spra_ersetzt_fk FOREIGN KEY(spra_spra_id)
        REFERENCES sprache(spra_id)
            ON DELETE SET NULL;

PROMPT CREATING FOREIGN KEY ON 'SPRACHE';
ALTER TABLE sprache
    ADD CONSTRAINT spra_uetx_fk FOREIGN KEY(spra_uetx_id_name)
        REFERENCES uebersetz_text(uetx_id)
            ON DELETE SET NULL;

PROMPT CREATING FOREIGN KEY ON 'SPRACHTEXT';
ALTER TABLE sprachtext
    ADD CONSTRAINT sptx_spra_fk FOREIGN KEY(sptx_spra_id)
        REFERENCES sprache(spra_id);

PROMPT CREATING FOREIGN KEY ON 'SPRACHTEXT';
ALTER TABLE sprachtext
    ADD CONSTRAINT sptx_uetx_fk FOREIGN KEY(sptx_uetx_id)
        REFERENCES uebersetz_text(uetx_id)
            ON DELETE CASCADE;

PROMPT CREATING FOREIGN KEY ON 'UEBERSETZ_TEXT';
ALTER TABLE uebersetz_text
    ADD CONSTRAINT uetx_spra_fk FOREIGN KEY(uetx_spra_id)
        REFERENCES sprache(spra_id);

PROMPT CREATING FOREIGN KEY ON 'UEBERSETZ_TEXT';
ALTER TABLE uebersetz_text
    ADD CONSTRAINT uetx_wrtb_fk FOREIGN KEY(uetx_wrtb_id)
        REFERENCES wertebereich(wrtb_id);

PROMPT CREATING FOREIGN KEY ON 'WERTEBEREICH';
ALTER TABLE wertebereich
    ADD CONSTRAINT wrtb_phys_einheit_fk FOREIGN KEY(wrtb_num_pheh_id)
        REFERENCES phys_einheit(pheh_id);

PROMPT CREATING FOREIGN KEY ON 'WERTEBEREICH';
ALTER TABLE wertebereich
    ADD CONSTRAINT wrtb_spfo_fk FOREIGN KEY(wrtb_bin_spfo_id)
        REFERENCES speicherformat(spfo_id);

PROMPT CREATING FOREIGN KEY ON 'WERTEBEREICH';
ALTER TABLE wertebereich
    ADD CONSTRAINT wrtb_uetx_fk_beschr FOREIGN KEY(wrtb_uetx_id_beschr)
        REFERENCES uebersetz_text(uetx_id)
            ON DELETE SET NULL;

PROMPT CREATING FOREIGN KEY ON 'WERTEBEREICH';
ALTER TABLE wertebereich
    ADD CONSTRAINT wrtb_uetx_fk_name FOREIGN KEY(wrtb_uetx_id_name)
        REFERENCES uebersetz_text(uetx_id);



-- Oracle SQL Developer Data Modeler Summary Report: 
-- 
-- CREATE TABLE                             5
-- CREATE INDEX                             6
-- ALTER TABLE                             27
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          2
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
