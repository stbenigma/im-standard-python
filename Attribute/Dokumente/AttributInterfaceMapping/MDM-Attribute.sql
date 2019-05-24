-- Generiert von Oracle SQL Developer Data Modeler 19.1.0.081.0911
--   am/um:        2019-05-24 10:03:09 MESZ
--   Site:      Oracle Database 12cR2
--   Typ:      Oracle Database 12cR2



CREATE SEQUENCE modm_seq START WITH 1 INCREMENT BY 1 NOMINVALUE NOMAXVALUE NOCYCLE NOCACHE ORDER;

PROMPT CREATING TABLE 'Ansprechsperson';

CREATE TABLE ansprechsperson(
    geschäft_telnr       VARCHAR2(30 CHAR)NULL,
    geschäft_email       VARCHAR2(100 CHAR)NULL,
    contact_id           NUMBER(10)DEFAULT modm_seq.NEXTVAL NOT NULL,
    natpers_natpers_id   NUMBER(10)NOT NULL,
    fk                   INTEGER NULL,
    firma_firma_id       NUMBER(10)NOT NULL
)
ORGANIZATION HEAP NOCOMPRESS
    NOCACHE
        NOPARALLEL
    NOROWDEPENDENCIES DISABLE ROW MOVEMENT;

PROMPT CREATING PRIMARY KEY ON 'Ansprechsperson';
ALTER TABLE ansprechsperson
    ADD CONSTRAINT contact_pk PRIMARY KEY(contact_id)NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING TABLE 'Juristische_Person';
CREATE TABLE juristische_person(
    name       VARCHAR2(80 CHAR)NOT NULL,
    "UID"      VARCHAR2(80 CHAR)NOT NULL,
    website    VARCHAR2(200 CHAR)NULL,
    firma_id   NUMBER(10)DEFAULT modm_seq.NEXTVAL NOT NULL
)
ORGANIZATION HEAP NOCOMPRESS
    NOCACHE
        NOPARALLEL
    NOROWDEPENDENCIES DISABLE ROW MOVEMENT;

PROMPT CREATING PRIMARY KEY ON 'Juristische_Person';
ALTER TABLE juristische_person
    ADD CONSTRAINT firma_pk PRIMARY KEY(firma_id)NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING UNIQUE KEY ON 'Juristische_Person';

ALTER TABLE juristische_person
    ADD CONSTRAINT firma_uid_un UNIQUE("UID")NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING TABLE 'Natürliche_Person';
CREATE TABLE natürliche_person(
    name                      VARCHAR2(80 CHAR)NOT NULL,
    vorname                   VARCHAR2(80 CHAR)NOT NULL,
    privat_telnr              VARCHAR2(30 CHAR)NULL,
    mobil_telnr               VARCHAR2(30 CHAR)NULL,
    geburtsdatum              DATE NOT NULL,
    zivilstand                VARCHAR2(4 CHAR)NULL
        CHECK(zivilstand IN(
            'GESC',
            'LEDI',
            'VERH',
            'VERW'
        ))NOT DEFERRABLE ENABLE VALIDATE,
    "Sozialversicherung-Nr"   NUMBER(20)NOT NULL,
    natpers_id                NUMBER(10)DEFAULT modm_seq.NEXTVAL NOT NULL
)
ORGANIZATION HEAP NOCOMPRESS
    NOCACHE
        NOPARALLEL
    NOROWDEPENDENCIES DISABLE ROW MOVEMENT;

PROMPT CREATING PRIMARY KEY ON 'Natürliche_Person';
ALTER TABLE natürliche_person
    ADD CONSTRAINT natpers_pk PRIMARY KEY(natpers_id)NOT DEFERRABLE ENABLE VALIDATE;

--  ERROR: UK name length exceeds maximum allowed length(30) 
PROMPT CREATING UNIQUE KEY ON 'Natürliche_Person';

ALTER TABLE natürliche_person
    ADD CONSTRAINT "NatPers_Sozialversicherung-Nr_UN" UNIQUE("Sozialversicherung-Nr")NOT DEFERRABLE ENABLE VALIDATE;

PROMPT CREATING FOREIGN KEY ON 'Ansprechsperson';
ALTER TABLE ansprechsperson
    ADD CONSTRAINT contact_firma_fk FOREIGN KEY(firma_firma_id)
        REFERENCES juristische_person(firma_id);

PROMPT CREATING FOREIGN KEY ON 'Ansprechsperson';
ALTER TABLE ansprechsperson
    ADD CONSTRAINT contact_natpers_fk FOREIGN KEY(natpers_natpers_id)
        REFERENCES natürliche_person(natpers_id);



-- Zusammenfassungsbericht für Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                             3
-- CREATE INDEX                             0
-- ALTER TABLE                              7
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
-- CREATE SEQUENCE                          1
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
-- ERRORS                                   1
-- WARNINGS                                 0
