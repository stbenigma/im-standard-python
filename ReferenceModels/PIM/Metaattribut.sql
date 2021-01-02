-- Generiert von Oracle SQL Developer Data Modeler 18.1.0.082.1035
--   am/um:        2018-06-03 17:57:54 CEST
--   Site:      Oracle Database 11g
--   Typ:      Oracle Database 11g


CREATE TABLE attr_auspraegung (
    atau_id        NUMBER(15)
        CONSTRAINT nnc_atau_atau_id NOT NULL,
    atau_wert_c    VARCHAR2(4000 CHAR),
    atau_wert_n    NUMBER,
    atau_wert_t    TIMESTAMP WITH LOCAL TIME ZONE,
    atau_typ       VARCHAR2(40 CHAR)
        CONSTRAINT nnc_atau_atau_typ NOT NULL,
    atau_atvg_id   NUMBER(15),
    atau_arti_id   NUMBER(15)
        CONSTRAINT nnc_atau_atau_arti_id NOT NULL,
    atau_attr_id   NUMBER(15)
        CONSTRAINT nnc_atau_atau_attr_id NOT NULL,
    atau_ucre      VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT nnc_atau_atau_ucre NOT NULL,
    atau_tcre      TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT nnc_atau_atau_tcre NOT NULL,
    atau_umod      VARCHAR2(30 CHAR),
    atau_tmod      TIMESTAMP WITH LOCAL TIME ZONE
);

ALTER TABLE attr_auspraegung
    ADD CONSTRAINT ck_atau_atau_typ CHECK ( atau_typ IN (
        'FREIER_WERT',
        'LISTENWERT'
    ) );

ALTER TABLE attr_auspraegung
    ADD CONSTRAINT atau_exdep1 CHECK (
        atau_typ != 'FREIER_WERT'
        OR ( atau_atvg_id IS NULL )
    );

ALTER TABLE attr_auspraegung
    ADD CONSTRAINT atau_exdep2 CHECK (
        atau_typ != 'LISTENWERT'
        OR (
            atau_wert_c IS NULL
            AND atau_wert_n IS NULL
            AND atau_wert_t IS NULL
        )
    );

COMMENT ON COLUMN attr_auspraegung.atau_ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN attr_auspraegung.atau_tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN attr_auspraegung.atau_tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

CREATE INDEX atau_atau_attr_id_idx ON
    attr_auspraegung (
        atau_attr_id
    ASC );

CREATE INDEX atau_atau_atvg_id_idx ON
    attr_auspraegung (
        atau_atvg_id
    ASC );

CREATE INDEX atau_atau_arti_id_idx ON
    attr_auspraegung (
        atau_arti_id
    ASC );

ALTER TABLE attr_auspraegung ADD CONSTRAINT atau_pk PRIMARY KEY ( atau_id );

ALTER TABLE attr_auspraegung ADD CONSTRAINT atau_un UNIQUE ( atau_attr_id,
                                                             atau_arti_id );

CREATE TABLE attr_verwendung (
    atvw_id            NUMBER(15)
        CONSTRAINT nnc_atvw_atvw_id NOT NULL,
    atvw_ist_pflicht   VARCHAR2(5 CHAR) DEFAULT 'TRUE'
        CONSTRAINT nnc_atvw_atvw_ist_pflicht NOT NULL,
    atvw_attr_id       NUMBER(15)
        CONSTRAINT nnc_atvw_atvw_attr_id NOT NULL,
    atvw_atwg_id       NUMBER(15)
        CONSTRAINT nnc_atvw_atvw_atwg_id NOT NULL,
    atvw_ucre          VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT nnc_atvw_atvw_ucre NOT NULL,
    atvw_tcre          TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT nnc_atvw_atvw_tcre NOT NULL,
    atvw_umod          VARCHAR2(30 CHAR),
    atvw_tmod          TIMESTAMP WITH LOCAL TIME ZONE
);

ALTER TABLE attr_verwendung
    ADD CONSTRAINT ck_atvw_atvw_ist_pflicht CHECK ( atvw_ist_pflicht IN (
        'FALSE',
        'TRUE'
    ) );

COMMENT ON COLUMN attr_verwendung.atvw_ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN attr_verwendung.atvw_tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN attr_verwendung.atvw_tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

CREATE INDEX atvw_atvw_attr_id_idx ON
    attr_verwendung (
        atvw_attr_id
    ASC );

CREATE INDEX atvw_atvw_atwg_id_idx ON
    attr_verwendung (
        atvw_atwg_id
    ASC );

ALTER TABLE attr_verwendung ADD CONSTRAINT atvw_pk PRIMARY KEY ( atvw_id );

ALTER TABLE attr_verwendung ADD CONSTRAINT atvw_un UNIQUE ( atvw_attr_id,
                                                            atvw_atwg_id );

CREATE TABLE attr_vg_text (
    atvt_id        NUMBER(15)
        CONSTRAINT nnc_atvt_atvt_id NOT NULL,
    atvt_wert      VARCHAR2(60)
        CONSTRAINT nnc_atvt_atvt_wert NOT NULL,
    atvt_krztxt    VARCHAR2(60),
    atvt_lngtxt    VARCHAR2(60),
    atvt_gspr_id   NUMBER(15)
        CONSTRAINT nnc_atvt_atvt_gspr_id NOT NULL,
    atvt_atvg_id   NUMBER(15)
        CONSTRAINT nnc_atvt_atvt_atvg_id NOT NULL,
    atvt_ucre      VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT nnc_atvt_atvt_ucre NOT NULL,
    atvt_tcre      TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT nnc_atvt_atvt_tcre NOT NULL,
    atvt_umod      VARCHAR2(30 CHAR),
    atvt_tmod      TIMESTAMP WITH LOCAL TIME ZONE
);

COMMENT ON COLUMN attr_vg_text.atvt_ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN attr_vg_text.atvt_tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN attr_vg_text.atvt_tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

CREATE INDEX atvt_atvt_gspr_id_idx ON
    attr_vg_text (
        atvt_gspr_id
    ASC );

CREATE INDEX atvt_atvt_atvg_id_idx ON
    attr_vg_text (
        atvt_atvg_id
    ASC );

ALTER TABLE attr_vg_text ADD CONSTRAINT atvt_pk PRIMARY KEY ( atvt_id );

ALTER TABLE attr_vg_text ADD CONSTRAINT atvt_un UNIQUE ( atvt_gspr_id,
                                                         atvt_atvg_id );

CREATE TABLE attr_vorgabewert (
    atvg_id         NUMBER(15)
        CONSTRAINT nnc_atvg_atvg_id NOT NULL,
    atvg_wert       VARCHAR2(60)
        CONSTRAINT nnc_atvg_atvg_wert NOT NULL,
    atvg_krztxt     VARCHAR2(60),
    atvg_lngtxt     VARCHAR2(60),
    atvg_sortrhfg   INTEGER,
    atvg_attr_id    NUMBER(15)
        CONSTRAINT nnc_atvg_atvg_attr_id NOT NULL,
    atvg_ucre       VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT nnc_atvg_atvg_ucre NOT NULL,
    atvg_tcre       TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT nnc_atvg_atvg_tcre NOT NULL,
    atvg_umod       VARCHAR2(30 CHAR),
    atvg_tmod       TIMESTAMP WITH LOCAL TIME ZONE
);

COMMENT ON COLUMN attr_vorgabewert.atvg_ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN attr_vorgabewert.atvg_tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN attr_vorgabewert.atvg_tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

CREATE INDEX atvg_atvg_attr_id_idx ON
    attr_vorgabewert (
        atvg_attr_id
    ASC );

ALTER TABLE attr_vorgabewert ADD CONSTRAINT atvg_pk PRIMARY KEY ( atvg_id );

ALTER TABLE attr_vorgabewert ADD CONSTRAINT atvg_un UNIQUE ( atvg_wert,
                                                             atvg_attr_id );

CREATE TABLE attr_warengruppierung (
    atwg_id         NUMBER(15)
        CONSTRAINT nnc_atwg_atwg_id NOT NULL,
    atwg_name       VARCHAR2(60)
        CONSTRAINT nnc_atwg_atwg_name NOT NULL,
    atwg_sortrhfg   INTEGER,
    atwg_typ        VARCHAR2(4)
        CONSTRAINT nnc_atwg_atwg_typ NOT NULL,
    atwg_atwg_id    NUMBER(15),
    atwg_ucre       VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT nnc_atwg_atwg_ucre NOT NULL,
    atwg_tcre       TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT nnc_atwg_atwg_tcre NOT NULL,
    atwg_umod       VARCHAR2(30 CHAR),
    atwg_tmod       TIMESTAMP WITH LOCAL TIME ZONE
);

ALTER TABLE attr_warengruppierung
    ADD CONSTRAINT ck_atwg_atwg_typ CHECK ( atwg_typ IN (
        'ATGR',
        'ATWH'
    ) );

COMMENT ON COLUMN attr_warengruppierung.atwg_ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN attr_warengruppierung.atwg_tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN attr_warengruppierung.atwg_tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

CREATE INDEX atwg_atwg_atwg_id_idx ON
    attr_warengruppierung (
        atwg_atwg_id
    ASC );

ALTER TABLE attr_warengruppierung ADD CONSTRAINT atwg_pk PRIMARY KEY ( atwg_id );

ALTER TABLE attr_warengruppierung ADD CONSTRAINT atwg_un UNIQUE ( atwg_name );

CREATE TABLE attribut (
    attr_id             NUMBER(15)
        CONSTRAINT nnc_attr_attr_id NOT NULL,
    attr_name           VARCHAR2(60)
        CONSTRAINT nnc_attr_attr_name NOT NULL,
    attr_beschr         VARCHAR2(2000),
    attr_anzgname       VARCHAR2(60),
    attr_tooltip        VARCHAR2(60),
    attr_min_zpkt       VARCHAR2(10 CHAR),
    attr_max_maxzpkt    TIMESTAMP,
    attr_granu          INTEGER,
    attr_min_txtlng     INTEGER DEFAULT 1,
    attr_max_txtlng     INTEGER DEFAULT 1,
    attr_zeichenregel   VARCHAR2(4000 CHAR),
    attr_min_wert       NUMBER,
    attr_max_wert       NUMBER,
    attr_vorkommst      INTEGER,
    attr_nachkommst     INTEGER DEFAULT 0,
    attr_rndg           NUMBER(15,6) DEFAULT 1,
    attr_typ            VARCHAR2(4)
        CONSTRAINT nnc_attr_attr_typ NOT NULL,
    attr_ucre           VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT nnc_attr_attr_ucre NOT NULL,
    attr_tcre           TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT nnc_attr_attr_tcre NOT NULL,
    attr_umod           VARCHAR2(30 CHAR),
    attr_tmod           TIMESTAMP WITH LOCAL TIME ZONE,
    attr_phei_id        NUMBER(15)
);

ALTER TABLE attribut
    ADD CONSTRAINT ck_attr_attr_min_zpkt CHECK ( attr_min_zpkt IN (
        'HALBSTUNDE',
        'JAHR',
        'MINUTE',
        'MONAT',
        'QUARTAL',
        'SEKUNDE',
        'SEMESTER',
        'STUNDE',
        'TAG',
        'VIERTELSTUNDE',
        'WOCHE'
    ) );

ALTER TABLE attribut ADD CONSTRAINT ck_attr_attr_granu CHECK ( attr_granu = 0 );

ALTER TABLE attribut
    ADD CONSTRAINT ck_attr_attr_min_txtlng CHECK ( attr_min_txtlng BETWEEN 0 AND 4000 );

ALTER TABLE attribut
    ADD CONSTRAINT ck_attr_attr_max_txtlng CHECK ( attr_max_txtlng BETWEEN 0 AND 4000 );

ALTER TABLE attribut ADD CONSTRAINT ck_attr_attr_vorkommst CHECK ( attr_vorkommst = 0 );

ALTER TABLE attribut ADD CONSTRAINT ck_attr_attr_nachkommst CHECK ( attr_nachkommst = 0 );

ALTER TABLE attribut ADD CONSTRAINT ck_attr_attr_rndg CHECK ( attr_rndg = 0 );

ALTER TABLE attribut
    ADD CONSTRAINT ck_attr_attr_typ CHECK ( attr_typ IN (
        'LATT',
        'NATT',
        'TATT',
        'ZATT'
    ) );

ALTER TABLE attribut
    ADD CONSTRAINT attr_exdep CHECK (
        (
            attr_typ = 'LATT'
            AND attr_min_zpkt IS NULL
            AND attr_max_maxzpkt IS NULL
            AND attr_granu IS NULL
            AND attr_min_txtlng IS NULL
            AND attr_max_txtlng IS NULL
            AND attr_zeichenregel IS NULL
            AND attr_min_wert IS NULL
            AND attr_max_wert IS NULL
            AND attr_vorkommst IS NULL
            AND attr_nachkommst IS NULL
            AND attr_rndg IS NULL
        )
        OR (
            attr_typ = 'NATT'
            AND attr_min_zpkt IS NULL
            AND attr_max_maxzpkt IS NULL
            AND attr_granu IS NULL
            AND attr_min_txtlng IS NULL
            AND attr_max_txtlng IS NULL
            AND attr_zeichenregel IS NULL
            AND attr_vorkommst IS NOT NULL
            AND attr_nachkommst IS NOT NULL
            AND attr_rndg IS NOT NULL
        )
        OR (
            attr_typ = 'TATT'
            AND attr_min_zpkt IS NULL
            AND attr_max_maxzpkt IS NULL
            AND attr_granu IS NULL
            AND attr_min_txtlng IS NOT NULL
            AND attr_min_wert IS NULL
            AND attr_max_wert IS NULL
            AND attr_vorkommst IS NULL
            AND attr_nachkommst IS NULL
            AND attr_rndg IS NULL
        )
        OR (
            attr_typ = 'ZATT'
            AND attr_granu IS NOT NULL
            AND attr_min_txtlng IS NULL
            AND attr_max_txtlng IS NULL
            AND attr_zeichenregel IS NULL
            AND attr_min_wert IS NULL
            AND attr_max_wert IS NULL
            AND attr_vorkommst IS NULL
            AND attr_nachkommst IS NULL
            AND attr_rndg IS NULL
        )
    );

COMMENT ON COLUMN attribut.attr_ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN attribut.attr_tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN attribut.attr_tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

CREATE INDEX attr_attr_phei_id_idx ON
    attribut (
        attr_phei_id
    ASC );

ALTER TABLE attribut ADD CONSTRAINT attr_pk PRIMARY KEY ( attr_id );

ALTER TABLE attribut ADD CONSTRAINT attr_un UNIQUE ( attr_name );

CREATE TABLE atwg_arti (
    atar_id        NUMBER(15)
        CONSTRAINT nnc_atar_atar_id NOT NULL,
    atar_atwg_id   NUMBER(15)
        CONSTRAINT nnc_atar_atar_atwg_id NOT NULL,
    atar_arti_id   NUMBER(15)
        CONSTRAINT nnc_atar_atar_arti_id NOT NULL
);

CREATE INDEX atar_atar_atwg_id_idx ON
    atwg_arti (
        atar_atwg_id
    ASC );

CREATE INDEX atar_atar_arti_id_idx ON
    atwg_arti (
        atar_arti_id
    ASC );

ALTER TABLE atwg_arti ADD CONSTRAINT atar_pk PRIMARY KEY ( atar_id );

ALTER TABLE atwg_arti ADD CONSTRAINT atar_un UNIQUE ( atar_arti_id,
                                                      atar_atwg_id );

CREATE TABLE bu_text (
    burt_id        NUMBER(15)
        CONSTRAINT nnc_burt_burt_id NOT NULL,
    burt_beschr    VARCHAR2(2000),
    burt_fhlmld    VARCHAR2(60),
    burt_busr_id   NUMBER(15)
        CONSTRAINT nnc_burt_burt_busr_id NOT NULL,
    burt_gspr_id   NUMBER(15)
        CONSTRAINT nnc_burt_burt_gspr_id NOT NULL,
    burt_ucre      VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT nnc_burt_burt_ucre NOT NULL,
    burt_tcre      TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT nnc_burt_burt_tcre NOT NULL,
    burt_umod      VARCHAR2(30 CHAR),
    burt_tmod      TIMESTAMP WITH LOCAL TIME ZONE
);

COMMENT ON COLUMN bu_text.burt_ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN bu_text.burt_tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN bu_text.burt_tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

CREATE INDEX burt_burt_busr_id_idx ON
    bu_text (
        burt_busr_id
    ASC );

CREATE INDEX burt_burt_gspr_id_idx ON
    bu_text (
        burt_gspr_id
    ASC );

ALTER TABLE bu_text ADD CONSTRAINT burt_pk PRIMARY KEY ( burt_id );

ALTER TABLE bu_text ADD CONSTRAINT burt_un UNIQUE ( burt_busr_id,
                                                    burt_gspr_id );

CREATE TABLE business_rule (
    busr_id        NUMBER(15)
        CONSTRAINT nnc_busr_busr_id NOT NULL,
    busr_name      VARCHAR2(60),
    busr_beschr    VARCHAR2(2000),
    busr_regel     VARCHAR2(4000 CHAR)
        CONSTRAINT nnc_busr_busr_regel NOT NULL,
    busr_fhlmld    VARCHAR2(60),
    busr_atvw_id   NUMBER(15)
        CONSTRAINT nnc_busr_busr_atvw_id NOT NULL,
    busr_ucre      VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT nnc_busr_busr_ucre NOT NULL,
    busr_tcre      TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT nnc_busr_busr_tcre NOT NULL,
    busr_umod      VARCHAR2(30 CHAR),
    busr_tmod      TIMESTAMP WITH LOCAL TIME ZONE
);

COMMENT ON COLUMN business_rule.busr_ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN business_rule.busr_tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN business_rule.busr_tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

CREATE INDEX busr_busr_atvw_id_idx ON
    business_rule (
        busr_atvw_id
    ASC );

ALTER TABLE business_rule ADD CONSTRAINT busr_pk PRIMARY KEY ( busr_id );

ALTER TABLE business_rule ADD CONSTRAINT busr_un UNIQUE ( busr_regel,
                                                          busr_atvw_id );

CREATE TABLE busr_atvw (
    buav_id        NUMBER(15),
    buav_busr_id   NUMBER(15)
        CONSTRAINT nnc_buav_buav_busr_id NOT NULL,
    buav_atvw_id   NUMBER(15)
        CONSTRAINT nnc_buav_buav_atvw_id NOT NULL,
    buav_ucre      VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT nnc_buav_buav_ucre NOT NULL,
    buav_tcre      TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT nnc_buav_buav_tcre NOT NULL,
    buav_umod      VARCHAR2(30 CHAR),
    buav_tmod      TIMESTAMP WITH LOCAL TIME ZONE
);

COMMENT ON COLUMN busr_atvw.buav_ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN busr_atvw.buav_tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN busr_atvw.buav_tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

CREATE INDEX buav_buav_busr_id_idx ON
    busr_atvw (
        buav_busr_id
    ASC );

CREATE INDEX buav_buav_atvw_id_idx ON
    busr_atvw (
        buav_atvw_id
    ASC );

ALTER TABLE busr_atvw ADD CONSTRAINT buav_pk PRIMARY KEY ( buav_busr_id,
                                                           buav_atvw_id );

CREATE TABLE einheitumrechnung (
    eumr_faktor        NUMBER(20,10)
        CONSTRAINT nnc_eumr_eumr_faktor NOT NULL,
    eumr_id            NUMBER(15)
        CONSTRAINT nnc_eumr_eumr_id NOT NULL,
    eumr_phei_id_von   NUMBER(15)
        CONSTRAINT nnc_eumr_eumr_phei_id_von NOT NULL,
    eumr_phei_id_zu    NUMBER(15)
        CONSTRAINT nnc_eumr_eumr_phei_id_zu NOT NULL,
    eumr_ucre          VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT nnc_eumr_eumr_ucre NOT NULL,
    eumr_tcre          TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT nnc_eumr_eumr_tcre NOT NULL,
    eumr_umod          VARCHAR2(30 CHAR),
    eumr_tmod          TIMESTAMP WITH LOCAL TIME ZONE
);

COMMENT ON COLUMN einheitumrechnung.eumr_ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN einheitumrechnung.eumr_tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN einheitumrechnung.eumr_tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

CREATE INDEX eumr_eumr_phei_id_von_idx ON
    einheitumrechnung (
        eumr_phei_id_von
    ASC );

CREATE INDEX eumr_eumr_phei_id_zu_idx ON
    einheitumrechnung (
        eumr_phei_id_zu
    ASC );

ALTER TABLE einheitumrechnung ADD CONSTRAINT eumr_pk PRIMARY KEY ( eumr_id );

ALTER TABLE einheitumrechnung ADD CONSTRAINT eumr_un UNIQUE ( eumr_phei_id_zu,
                                                              eumr_phei_id_von );

CREATE TABLE gebietssprache (
    gspr_id                    NUMBER(15)
        CONSTRAINT nnc_gspr_gspr_id NOT NULL,
    gspr_iso_sprachland_code   VARCHAR2(5) 
        CONSTRAINT nnc_gspr_iso_sprachland_code NOT NULL,
    gspr_name                  VARCHAR2(60)
        CONSTRAINT nnc_gspr_gspr_name NOT NULL,
    gspr_land_id               NUMBER(15)
        CONSTRAINT nnc_gspr_gspr_land_id NOT NULL,
    gspr_spra_id               NUMBER(15)
        CONSTRAINT nnc_gspr_gspr_spra_id NOT NULL,
    gspr_tplt_ucre             VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT nnc_gspr_gspr_tplt_ucre NOT NULL,
    gspr_tplt_tcre             TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT nnc_gspr_gspr_tplt_tcre NOT NULL,
    gspr_tplt_umod             VARCHAR2(30 CHAR),
    gspr_tplt_tmod             TIMESTAMP WITH LOCAL TIME ZONE
);

COMMENT ON COLUMN gebietssprache.gspr_tplt_ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN gebietssprache.gspr_tplt_tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN gebietssprache.gspr_tplt_tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

CREATE INDEX gspr_gspr_spra_id_idx ON
    gebietssprache (
        gspr_spra_id
    ASC );

CREATE INDEX gspr_gspr_land_id_idx ON
    gebietssprache (
        gspr_land_id
    ASC );

ALTER TABLE gebietssprache ADD CONSTRAINT gspr_pk PRIMARY KEY ( gspr_id );

ALTER TABLE gebietssprache ADD CONSTRAINT gspr_un UNIQUE ( gspr_iso_sprachland_code );

ALTER TABLE gebietssprache ADD CONSTRAINT gspr_unv3 UNIQUE ( gspr_land_id,
                                                             gspr_spra_id );

ALTER TABLE gebietssprache ADD CONSTRAINT gspr_unv2 UNIQUE ( gspr_name );

CREATE TABLE land (
    land_id          NUMBER(15)
        CONSTRAINT nnc_land_land_id NOT NULL,
    land_name        VARCHAR2(60)
        CONSTRAINT nnc_land_land_name NOT NULL,
    land_iso_code    VARCHAR2(2 CHAR)
        CONSTRAINT nnc_land_land_iso_code NOT NULL,
    land_regi_id     NUMBER(15)
        CONSTRAINT nnc_land_land_regi_id NOT NULL,
    land_tplt_ucre   VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT nnc_land_land_tplt_ucre NOT NULL,
    land_tplt_tcre   TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT nnc_land_land_tplt_tcre NOT NULL,
    land_tplt_umod   VARCHAR2(30 CHAR),
    land_tplt_tmod   TIMESTAMP WITH LOCAL TIME ZONE
);

COMMENT ON COLUMN land.land_tplt_ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN land.land_tplt_tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN land.land_tplt_tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

CREATE INDEX land_land_regi_id_idx ON
    land (
        land_regi_id
    ASC );

ALTER TABLE land ADD CONSTRAINT land_pk PRIMARY KEY ( land_id );

ALTER TABLE land ADD CONSTRAINT land_un UNIQUE ( land_iso_code );

ALTER TABLE land ADD CONSTRAINT land_unv2 UNIQUE ( land_name );

CREATE TABLE phys_einh_text (
    phet_id           NUMBER(15)
        CONSTRAINT nnc_phet_phet_id NOT NULL,
    phet_si_einheit   VARCHAR2(15 CHAR)
        CONSTRAINT nnc_phet_phet_si_einheit NOT NULL,
    phet_name         VARCHAR2(60),
    phet_beschr       VARCHAR2(2000),
    phet_gspr_id      NUMBER(15)
        CONSTRAINT nnc_phet_phet_gspr_id NOT NULL,
    phet_phei_id      NUMBER(15)
        CONSTRAINT nnc_phet_phet_phei_id NOT NULL,
    phet_ucre         VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT nnc_phet_phet_ucre NOT NULL,
    phet_tcre         TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT nnc_phet_phet_tcre NOT NULL,
    phet_umod         VARCHAR2(30 CHAR),
    phet_tmod         TIMESTAMP WITH LOCAL TIME ZONE
);

COMMENT ON COLUMN phys_einh_text.phet_ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN phys_einh_text.phet_tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN phys_einh_text.phet_tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

CREATE INDEX phet_phet_gspr_id_idx ON
    phys_einh_text (
        phet_gspr_id
    ASC );

CREATE INDEX phet_phet_phei_id_idx ON
    phys_einh_text (
        phet_phei_id
    ASC );

ALTER TABLE phys_einh_text ADD CONSTRAINT phet_pk PRIMARY KEY ( phet_id );

ALTER TABLE phys_einh_text ADD CONSTRAINT phet_un UNIQUE ( phet_gspr_id,
                                                           phet_phei_id );

CREATE TABLE phys_einheit (
    phei_id           NUMBER(15)
        CONSTRAINT nnc_phei_phei_id NOT NULL,
    phei_si_einheit   VARCHAR2(15 CHAR)
        CONSTRAINT nnc_phei_phei_si_einheit NOT NULL,
    phei_name         VARCHAR2(60),
    phei_beschr       VARCHAR2(2000),
    phei_ucre         VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT nnc_phei_phei_ucre NOT NULL,
    phei_tcre         TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT nnc_phei_phei_tcre NOT NULL,
    phei_umod         VARCHAR2(30 CHAR),
    phei_tmod         TIMESTAMP WITH LOCAL TIME ZONE
);

COMMENT ON COLUMN phys_einheit.phei_ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN phys_einheit.phei_tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN phys_einheit.phei_tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

ALTER TABLE phys_einheit ADD CONSTRAINT phei_pk PRIMARY KEY ( phei_id );

CREATE TABLE region (
    regi_id          NUMBER(15)
        CONSTRAINT nnc_regi_regi_id NOT NULL,
    regi_name        VARCHAR2(60)
        CONSTRAINT nnc_regi_regi_name NOT NULL,
    regi_tplt_ucre   VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT nnc_regi_regi_tplt_ucre NOT NULL,
    regi_tplt_tcre   TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT nnc_regi_regi_tplt_tcre NOT NULL,
    regi_tplt_umod   VARCHAR2(30 CHAR),
    regi_tplt_tmod   TIMESTAMP WITH LOCAL TIME ZONE
);

COMMENT ON COLUMN region.regi_tplt_ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN region.regi_tplt_tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN region.regi_tplt_tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

ALTER TABLE region ADD CONSTRAINT regi_pk PRIMARY KEY ( regi_id );

ALTER TABLE region ADD CONSTRAINT regi_un UNIQUE ( regi_name );

CREATE TABLE sprache (
    spra_id          NUMBER(15)
        CONSTRAINT nnc_spra_spra_id NOT NULL,
    spra_iso_code    VARCHAR2(2 CHAR)
        CONSTRAINT nnc_spra_spra_iso_code NOT NULL,
    spra_name        VARCHAR2(60)
        CONSTRAINT nnc_spra_spra_name NOT NULL,
    spra_tplt_ucre   VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT nnc_spra_spra_tplt_ucre NOT NULL,
    spra_tplt_tcre   TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT nnc_spra_spra_tplt_tcre NOT NULL,
    spra_tplt_umod   VARCHAR2(30 CHAR),
    spra_tplt_tmod   TIMESTAMP WITH LOCAL TIME ZONE
);

COMMENT ON COLUMN sprache.spra_tplt_ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN sprache.spra_tplt_tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN sprache.spra_tplt_tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

ALTER TABLE sprache ADD CONSTRAINT spra_pk PRIMARY KEY ( spra_id );

ALTER TABLE sprache ADD CONSTRAINT spra_un UNIQUE ( spra_iso_code );

ALTER TABLE sprache ADD CONSTRAINT spra_unv1 UNIQUE ( spra_name );

CREATE TABLE "TEMPLATE TABELLE" (
    ucre   VARCHAR2(30 CHAR) DEFAULT user
        CONSTRAINT "NNC_TEMPLATE TABELLE_UCRE" NOT NULL,
    tcre   TIMESTAMP WITH LOCAL TIME ZONE
        CONSTRAINT "NNC_TEMPLATE TABELLE_TCRE" NOT NULL,
    umod   VARCHAR2(30 CHAR),
    tmod   TIMESTAMP WITH LOCAL TIME ZONE
);

COMMENT ON COLUMN "TEMPLATE TABELLE".ucre IS
    'User der diesen Eintrag erstellt hat';

COMMENT ON COLUMN "TEMPLATE TABELLE".tcre IS
    'Zeitpunkt (Time) zu dem dieser Eintrag erstellt wurde.';

COMMENT ON COLUMN "TEMPLATE TABELLE".tmod IS
    'Zeitpunkt (Time) zu dem dieser Eintrag modifiziert wurde.';

ALTER TABLE atwg_arti
    ADD CONSTRAINT atar_arti_fk FOREIGN KEY ( atar_arti_id )
        REFERENCES artikel ( arti_id2 );

ALTER TABLE atwg_arti
    ADD CONSTRAINT atar_atwg_fk FOREIGN KEY ( atar_atwg_id )
        REFERENCES attr_warengruppierung ( atwg_id );

ALTER TABLE attr_auspraegung
    ADD CONSTRAINT atau_arti_fk FOREIGN KEY ( atau_arti_id )
        REFERENCES artikel ( arti_id2 );

ALTER TABLE attr_auspraegung
    ADD CONSTRAINT atau_attr_fk FOREIGN KEY ( atau_attr_id )
        REFERENCES attribut ( attr_id );

ALTER TABLE attr_auspraegung
    ADD CONSTRAINT atau_atvg_fk FOREIGN KEY ( atau_atvg_id )
        REFERENCES attr_vorgabewert ( atvg_id );

ALTER TABLE attribut
    ADD CONSTRAINT attr_phei_fk FOREIGN KEY ( attr_phei_id )
        REFERENCES phys_einheit ( phei_id );

ALTER TABLE attr_vorgabewert
    ADD CONSTRAINT atvg_attr_fk FOREIGN KEY ( atvg_attr_id )
        REFERENCES attribut ( attr_id );

ALTER TABLE attr_vg_text
    ADD CONSTRAINT atvt_atvg_fk FOREIGN KEY ( atvt_atvg_id )
        REFERENCES attr_vorgabewert ( atvg_id );

ALTER TABLE attr_vg_text
    ADD CONSTRAINT atvt_gspr_fk FOREIGN KEY ( atvt_gspr_id )
        REFERENCES gebietssprache ( gspr_id );

ALTER TABLE attr_verwendung
    ADD CONSTRAINT atvw_attr_fk FOREIGN KEY ( atvw_attr_id )
        REFERENCES attribut ( attr_id );

ALTER TABLE attr_verwendung
    ADD CONSTRAINT atvw_atwg_fk FOREIGN KEY ( atvw_atwg_id )
        REFERENCES attr_warengruppierung ( atwg_id );

ALTER TABLE attr_warengruppierung
    ADD CONSTRAINT atwg_atwg_fk FOREIGN KEY ( atwg_atwg_id )
        REFERENCES attr_warengruppierung ( atwg_id );

ALTER TABLE busr_atvw
    ADD CONSTRAINT buav_atvw_fk FOREIGN KEY ( buav_atvw_id )
        REFERENCES attr_verwendung ( atvw_id );

ALTER TABLE busr_atvw
    ADD CONSTRAINT buav_busr_fk FOREIGN KEY ( buav_busr_id )
        REFERENCES business_rule ( busr_id );

ALTER TABLE bu_text
    ADD CONSTRAINT burt_busr_fk FOREIGN KEY ( burt_busr_id )
        REFERENCES business_rule ( busr_id );

ALTER TABLE bu_text
    ADD CONSTRAINT burt_gspr_fk FOREIGN KEY ( burt_gspr_id )
        REFERENCES gebietssprache ( gspr_id );

ALTER TABLE business_rule
    ADD CONSTRAINT busr_atvw_fk FOREIGN KEY ( busr_atvw_id )
        REFERENCES attr_verwendung ( atvw_id );

ALTER TABLE einheitumrechnung
    ADD CONSTRAINT eumr_phei_fk FOREIGN KEY ( eumr_phei_id_zu )
        REFERENCES phys_einheit ( phei_id );

ALTER TABLE einheitumrechnung
    ADD CONSTRAINT eumr_phei_fkv2 FOREIGN KEY ( eumr_phei_id_von )
        REFERENCES phys_einheit ( phei_id );

ALTER TABLE gebietssprache
    ADD CONSTRAINT gspr_land_fk FOREIGN KEY ( gspr_land_id )
        REFERENCES land ( land_id );

ALTER TABLE gebietssprache
    ADD CONSTRAINT gspr_spra_fk FOREIGN KEY ( gspr_spra_id )
        REFERENCES sprache ( spra_id );

ALTER TABLE land
    ADD CONSTRAINT land_regi_fk FOREIGN KEY ( land_regi_id )
        REFERENCES region ( regi_id );

ALTER TABLE phys_einh_text
    ADD CONSTRAINT phet_gspr_fk FOREIGN KEY ( phet_gspr_id )
        REFERENCES gebietssprache ( gspr_id );

ALTER TABLE phys_einh_text
    ADD CONSTRAINT phet_phei_fk FOREIGN KEY ( phet_phei_id )
        REFERENCES phys_einheit ( phei_id );

CREATE SEQUENCE atau_atau_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER atau_atau_id_trg BEFORE
    INSERT ON attr_auspraegung
    FOR EACH ROW
    WHEN ( new.atau_id IS NULL )
BEGIN
    :new.atau_id := atau_atau_id_seq.nextval;
END;
/

CREATE SEQUENCE atvw_atvw_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER atvw_atvw_id_trg BEFORE
    INSERT ON attr_verwendung
    FOR EACH ROW
    WHEN ( new.atvw_id IS NULL )
BEGIN
    :new.atvw_id := atvw_atvw_id_seq.nextval;
END;
/

CREATE SEQUENCE atvt_atvt_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER atvt_atvt_id_trg BEFORE
    INSERT ON attr_vg_text
    FOR EACH ROW
    WHEN ( new.atvt_id IS NULL )
BEGIN
    :new.atvt_id := atvt_atvt_id_seq.nextval;
END;
/

CREATE SEQUENCE atvg_atvg_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER atvg_atvg_id_trg BEFORE
    INSERT ON attr_vorgabewert
    FOR EACH ROW
    WHEN ( new.atvg_id IS NULL )
BEGIN
    :new.atvg_id := atvg_atvg_id_seq.nextval;
END;
/

CREATE SEQUENCE atwg_atwg_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER atwg_atwg_id_trg BEFORE
    INSERT ON attr_warengruppierung
    FOR EACH ROW
    WHEN ( new.atwg_id IS NULL )
BEGIN
    :new.atwg_id := atwg_atwg_id_seq.nextval;
END;
/

CREATE SEQUENCE attr_attr_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER attr_attr_id_trg BEFORE
    INSERT ON attribut
    FOR EACH ROW
    WHEN ( new.attr_id IS NULL )
BEGIN
    :new.attr_id := attr_attr_id_seq.nextval;
END;
/

CREATE SEQUENCE burt_burt_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER burt_burt_id_trg BEFORE
    INSERT ON bu_text
    FOR EACH ROW
    WHEN ( new.burt_id IS NULL )
BEGIN
    :new.burt_id := burt_burt_id_seq.nextval;
END;
/

CREATE SEQUENCE busr_busr_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER busr_busr_id_trg BEFORE
    INSERT ON business_rule
    FOR EACH ROW
    WHEN ( new.busr_id IS NULL )
BEGIN
    :new.busr_id := busr_busr_id_seq.nextval;
END;
/

CREATE SEQUENCE eumr_eumr_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER eumr_eumr_id_trg BEFORE
    INSERT ON einheitumrechnung
    FOR EACH ROW
    WHEN ( new.eumr_id IS NULL )
BEGIN
    :new.eumr_id := eumr_eumr_id_seq.nextval;
END;
/

CREATE SEQUENCE gspr_gspr_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER gspr_gspr_id_trg BEFORE
    INSERT ON gebietssprache
    FOR EACH ROW
    WHEN ( new.gspr_id IS NULL )
BEGIN
    :new.gspr_id := gspr_gspr_id_seq.nextval;
END;
/

CREATE SEQUENCE land_land_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER land_land_id_trg BEFORE
    INSERT ON land
    FOR EACH ROW
    WHEN ( new.land_id IS NULL )
BEGIN
    :new.land_id := land_land_id_seq.nextval;
END;
/

CREATE SEQUENCE phet_phet_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER phet_phet_id_trg BEFORE
    INSERT ON phys_einh_text
    FOR EACH ROW
    WHEN ( new.phet_id IS NULL )
BEGIN
    :new.phet_id := phet_phet_id_seq.nextval;
END;
/

CREATE SEQUENCE phei_phei_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER phei_phei_id_trg BEFORE
    INSERT ON phys_einheit
    FOR EACH ROW
    WHEN ( new.phei_id IS NULL )
BEGIN
    :new.phei_id := phei_phei_id_seq.nextval;
END;
/

CREATE SEQUENCE regi_regi_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER regi_regi_id_trg BEFORE
    INSERT ON region
    FOR EACH ROW
    WHEN ( new.regi_id IS NULL )
BEGIN
    :new.regi_id := regi_regi_id_seq.nextval;
END;
/

CREATE SEQUENCE spra_spra_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER spra_spra_id_trg BEFORE
    INSERT ON sprache
    FOR EACH ROW
    WHEN ( new.spra_id IS NULL )
BEGIN
    :new.spra_id := spra_spra_id_seq.nextval;
END;
/



-- Zusammenfassungsbericht für Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                            18
-- CREATE INDEX                            24
-- ALTER TABLE                             76
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                          15
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
-- CREATE SEQUENCE                         15
-- CREATE MATERIALIZED VIEW                 0
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
