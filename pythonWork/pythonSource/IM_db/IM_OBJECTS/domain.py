from IM_DB import *
from .baseobject import MultilangBaseobject, Baseobject
from .datatype import Datatype
from .modelelement import Modelelement, Modelelemtype
from .sprachtext import Sprachtext

class Domain(MultilangBaseobject):
    DERIVED: str = 'DER'
    DOMAIN: str = 'DOM'
    BIN: str = 'BIN'
    GRP: str = 'GRP'
    LOV: str = 'LOV'
    NUM: str = 'NUM'
    TXT: str = 'TXT'
    DAT: str = 'DAT'
    DAY: str = 'DAY'
    HOUR: str = 'HOUR'
    MILlISECOND: str = 'MILlISECOND'
    MINUTE: str = 'MINUTE'
    MONTH: str = 'MONTH'
    QUARTER: str = 'QUARTER'
    SECOND: str = 'SECOND'
    SEMESTER: str = 'SEMESTER'
    WEEK: str = 'WEEK'
    YEAR: str = 'YEAR'
    DRAWING: str = 'DRAWING'
    FILM: str = 'FILM'
    IMAGE: str = 'IMAGE'
    OTHER: str = 'OTHER'
    SOUND: str = 'SOUND'
    TEXT: str = 'TEXT'
    _tablename: str = 'domains'
    _prefix: str = 'doma'
    _columnlist: list = ['doma_id', 'doma_business_rule', 'doma_name', 'doma_descr',
                         'doma_type', 'doma_origin', 'doma_dat_minwert', 'doma_dat_maxwert',
                         'doma_dat_granularity', 'doma_txt_maxlng', 'doma_txt_syntaxrule', 'doma_num_maxwert',
                         'doma_num_minwert', 'doma_total_digits', 'doma_fract_digits', 'doma_num_round_value',
                         'doma_num_pheh_id', 'doma_bin_contenttype', 'doma_bin_spfo_id', 'doma_daty_id',
                         'doma_schn_id', 'doma_daty_id', 'doma_uc', 'doma_dc',
                         'doma_um', 'doma_dm']
    __unknowndom = None

    def __init__(self, psrcname=None, psrcid=None):
        super().__init__(tablename=Domain._tablename, prefix=Domain._prefix
                         , columnlist=Domain._columnlist
                         , multilangcols={'doma_name': Sprachtext.DOMA_NAME}
                         , pmodelemtype=Modelelemtype.DATY
                         , pscrid=psrcid
                         , psrcname=psrcname
                         )

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Domain._tablename
                               , psql="""
CREATE TABLE DOMAINS
    (
     DOMA_ID NUMERIC (10) NOT NULL  primary key,
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
     DOMA_NUM_PHYU_ID NUMERIC (10) NULL ,
     DOMA_BIN_CONTENTTYPE VARCHAR (30) NULL CHECK ( DOMA_BIN_CONTENTTYPE IN ('DRAWING', 'FILM', 'IMAGE', 'OTHER', 'SOUND', 'TEXT') ) ,
     DOMA_BIN_STFO_ID NUMERIC (10) NULL ,
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
)"""
                               )

    def getmodellelement(self):
        return Modelelement.getbyelemid(pwrtbid=self.doma_id)

    def getname(self, plang):
        return self._getsprachval(colname='doma_name', plang=plang)

    def getmodeid(self):
        mode = self.getmodellelement()
        return mode.mode_id if (mode is not None) else None

    # getmodeid

    def isderived(self):
        return self.doma_origin == Domain.DERIVED

    def typeinfo(self):
        def nvl(x, default=''):
            return x if (x is not None) else default

        daty = Datatype().getbyid(self.doma_daty_id)
        typestring = daty.daty_name if daty is not None else ''
        if (self.doma_type in (Domain.TXT, Domain.LOV)):
            infoheaders = (
            Sprachtext.transl('Datentyp'), Sprachtext.transl('Max. Länge'), Sprachtext.transl('Syntaxregel'),
            Sprachtext.transl('geändert'))
            infovalues = (nvl(self.doma_type), nvl(self.doma_txt_maxlng), nvl(self.doma_txt_syntaxrule),
                          nvl(self.doma_uc) + ',' + nvl(self.doma_dc))
            typestring += " ({})".format(nvl(self.doma_txt_maxlng))
        elif (self.doma_type == Domain.BIN):
            infoheaders = (Sprachtext.transl('Datentyp'), Sprachtext.transl('Inhaltstyp'), Sprachtext.transl('Format'),
                           Sprachtext.transl('geändert'))
            infovalues = (
            nvl(self.doma_type), Domain.displcontenttype(nvl(self.doma_bin_contenttype)), nvl(self.doma_bin_spfo_id),
            nvl(self.doma_uc) + ',' + nvl(self.doma_dc))
            typestring += " ({}, {})".format(Domain.displcontenttype(nvl(self.doma_bin_contenttype)),
                                             nvl(self.doma_bin_spfo_id))
        elif (self.doma_type == Domain.GRP):
            infoheaders = (Sprachtext.transl('Datentyp'), Sprachtext.transl('geändert'))
            infovalues = (self.doma_type, nvl(self.doma_uc) + ',' + nvl(self.doma_dc))
        elif (self.doma_type == Domain.NUM):
            infoheaders = (
            Sprachtext.transl('Datentyp'), Sprachtext.transl('Vorkommast.'), Sprachtext.transl('Nachkommast.')
            , Sprachtext.transl('Rundungseinh.'), Sprachtext.transl('Einheit'), Sprachtext.transl('Min. Wert'),
            Sprachtext.transl('Max. Wwert')
            , Sprachtext.transl('geändert'))
            infovalues = (nvl(self.doma_type), nvl(self.doma_total_digits), nvl(self.doma_fract_digits),
                          nvl(self.doma_num_round_value), nvl(self.doma_num_pheh_id)
                          , nvl(self.doma_num_minwert), nvl(self.doma_num_maxwert)
                          , nvl(self.doma_uc) + ',' + nvl(self.doma_dc))
            typestring += " ({}{}) {} {}".format(nvl(self.doma_total_digits)
                                                 , '' if self.doma_fract_digits is None else '.' + str(
                    self.doma_fract_digits)
                                                 , '' if self.doma_num_minwert is None else '>= ' + str(
                    self.doma_num_minwert)
                                                 , '' if self.doma_num_maxwert is None else '<= ' + str(
                    self.doma_num_maxwert))
        elif (self.doma_type == Domain.DAT):
            infoheaders = (
            Sprachtext.transl('Datentyp'), Sprachtext.transl('Min. Wert'), Sprachtext.transl('Max. Wwert'),
            Sprachtext.transl('Granularität')
            , Sprachtext.transl('geändert'))
            infovalues = (nvl(self.doma_type), nvl(self.doma_dat_minwert), nvl(self.doma_dat_maxwert),
                          Domain.displgranul(nvl(self.doma_dat_granularity)),
                          nvl(self.doma_uc) + ',' + nvl(self.doma_dc))
            typestring += " {} {} {}".format(
                '' if self.doma_dat_granularity is None else Sprachtext.transl('Granularität =') + Domain.displgranul(
                    self.doma_dat_granularity)
                , '' if self.doma_dat_minwert is None else '>= ' + self.doma_dat_minwert
                , '' if self.doma_dat_maxwert is None else '<= ' + self.doma_dat_maxwert)
        else:
            infoheaders, infovalues, typestring = None, None, ''
        return [infoheaders, infovalues, typestring]

    # typeinfo

    def typestring(self):
        info = self.typeinfo()
        return info[2]

    # typestring

    def insert(self):
        self.doma_id = Modelelement(Modelelemtype.DOMA).insert()
        super().insert()

    def webanker(self):
        return super().webanker()

    def refattranz(self):
        data = dbDML.select("""select count(*) 
                    from attributes where attr_doma_id = {}
                    """.format(self.doma_id))
        return data[0][0]

    # refattranz

    def displdatatype(self):
        return Domain.anzdatentyp(self.doma_type)

    @staticmethod
    def basetype2domatype(pdatybasetype):
        transl = {Datatype.BINARY: Domain.BIN,
                  Datatype.DATETIME: Domain.DAT,
                  Datatype.NUMERIC: Domain.NUM,
                  Datatype.STRING: Domain.TXT
                  }
        return transl[pdatybasetype]

    @staticmethod
    def select(pwhere=None, porderby=None):
        wrtbs = Baseobject.select(pclass=Domain
                                  , pwhere=pwhere, porderby=porderby)
        return wrtbs

    # select

    @staticmethod
    def delete():
        Baseobject.delete(Domain._tablename)

    @staticmethod
    def indexlist(pherkunft, plang: str):
        data = Domain.select(pwhere="doma_origin = '{}'".format(pherkunft), porderby='doma_name')
        indexlist = [['{} ({})'.format(d.getname(plang), d.refattranz())
                         , d.webanker(), d.doma_id] for d in data]
        return indexlist

    # indexlist

    @staticmethod
    def getbyname(pname: str):
        return Domain().getbyuk(pcolname='doma_name', pukvalue=pname)

    @staticmethod
    def getunknown():
        if Domain.__unknowndom is None:
            dom = Domain.getbyname(pname='Unknown')
            if dom.doma_id is None:
                dom = Domain.getbyname(pname='unknown')
            # fi
            Domain.__unknowndom = dom
        # fi
        return Domain.__unknowndom

    # getunknown

    @staticmethod
    def anzdatentyp(dt: str):
        anzDT = {Domain.BIN: Sprachtext.transl('Binär')
            , Domain.GRP: Sprachtext.transl('Gruppenattribut')
            , Domain.LOV: Sprachtext.transl('Werteliste')
            , Domain.NUM: Sprachtext.transl('Numerisch')
            , Domain.TXT: Sprachtext.transl('Text')
            , Domain.DAT: Sprachtext.transl('Zeitpunkt')}
        return anzDT[dt]

    # anzDatentyp

    @staticmethod
    def displcontenttype(dt):
        anzDT = {Domain.DRAWING: Sprachtext.transl('Bild')
            , Domain.FILM: Sprachtext.transl('Film')
            , Domain.IMAGE: Sprachtext.transl('Grafik')
            , Domain.TEXT: Sprachtext.transl('Text')
            , Domain.SOUND: Sprachtext.transl('Ton')
                 }
        if dt in anzDT.keys():
            return anzDT[dt]
        else:
            return Sprachtext.transl('Andere')

    # displcontenttype

    @staticmethod
    def displgranul(dt):
        anzDT = {
            Domain.YEAR: Sprachtext.transl('Jahr'),
            Domain.MILlISECOND: Sprachtext.transl('Millisekunde'),
            Domain.MINUTE: Sprachtext.transl('Minute'),
            Domain.MONTH: Sprachtext.transl('Monat'),
            Domain.QUARTER: Sprachtext.transl('Quartal'),
            Domain.SECOND: Sprachtext.transl('Sekunde'),
            Domain.SEMESTER: Sprachtext.transl('Semester'),
            Domain.HOUR: Sprachtext.transl('Stunde'),
            Domain.DAY: Sprachtext.transl('Tag'),
            Domain.WEEK: Sprachtext.transl('Woche')
        }
        return anzDT[dt]
    # displgranul


# Domain

class Wertebereichgruppe(Baseobject):
    _tablename: str = 'wertebereichgruppen'
    _prefix: str = 'wbgr'
    _columnlist: list = ['wbgr_id', 'wbgr_name', 'wbgr_beschr',
                         'wbgr_doma_id_gruppe', 'wbgr_doma_id_member', 'wbgr_type_ref',
                         'wbgr_uc', 'wbgr_dc', 'wbgr_um',
                         'wbgr_dm'
                         ]

    def __init__(self):
        super().__init__(tablename=Wertebereichgruppe._tablename, prefix=Wertebereichgruppe._prefix
                         , columnlist=Wertebereichgruppe._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Wertebereichgruppe._tablename
                               , psql="""
        create table wertebereichgruppen
    (
    wbgr_id               integer not null primary key autoincrement,
    wbgr_name             varchar(60)not null,
    wbgr_beschr           varchar(4000)null,
    wbgr_doma_id_gruppe   integer not null ,
     wbgr_doma_id_member integer not null , 
	 wbgr_type_ref	varchar(40),
     wbgr_uc varchar (30) not null , 
     wbgr_dc varchar (30) not null , 
     wbgr_um varchar (30)    null,
      wbgr_dm varchar (30) null
,constraint wbgr_doma_uk unique (wbgr_doma_id_gruppe ,wbgr_name )
,constraint wbgr_doma_fk_gruppe foreign key(wbgr_doma_id_gruppe)
        references DOMAINS(doma_id) on delete cascade
,constraint wbgr_doma_fk_member foreign key(wbgr_doma_id_member)
        references DOMAINS(doma_id) 
	)
    """);

    @staticmethod
    def delete():
        Baseobject.delete(Wertebereichgruppe._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Wertebereichgruppe
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def updmembers():
        ukwnid = Domain().getunknown().doma_id
        lupd = """update wertebereichgruppen 
            set wbgr_doma_id_member = 
            case when (select doma_id
                     from DOMAINS 
                    where doma_odm_guid = wbgr_type_ref) 
                is null
             then {} 
             else (select doma_id
             from DOMAINS 
             where doma_odm_guid = wbgr_type_ref)
             end
            where wbgr_doma_id_member = {}
        """.format(ukwnid, ukwnid)
        dbDML.exec(lupd)


# Wertebereichgruppe

class Vorgabewert(Baseobject):
    _tablename: str = 'vorgabewerte'
    _prefix: str = 'vgwt'
    _columnlist: list = ['vgwt_id', 'vgwt_guid', 'vgwt_wert',
                         'vgwt_sortrhfg', 'vgwt_doma_id', 'vgwt_anzeige',
                         'vgwt_beschr', 'vgwt_uc', 'vgwt_dc',
                         'vgwt_um', 'vgwt_dm'
                         ]

    def __init__(self):
        super().__init__(tablename=Vorgabewert._tablename, prefix=Vorgabewert._prefix
                         , columnlist=Vorgabewert._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Vorgabewert._tablename
                               , psql="""
        CREATE TABLE vorgabewerte(
    vgwt_id               integer NOT NULL primary key autoincrement,
	vgwt_guid varchar(40),
    vgwt_wert              VARCHAR(100) NOT NULL,
    vgwt_sortrhfg          integer NULL,
    vgwt_doma_id           integer NOT NULL,
    vgwt_anzeige   varchar(200),
    vgwt_beschr    varchar(4000),
    vgwt_uc         varchar(30) NOT NULL,
    vgwt_dc        varchar(30) NOT NULL,
    vgwt_um        varchar(30),
    vgwt_dm        varchar(30),
	constraint vgwt_uk unique (vgwt_doma_id,vgwt_wert),
	constraint vgwt_doma_fk foreign key (vgwt_doma_id) references DOMAINS(doma_id) ON DELETE CASCADE
    )
    """)

    @staticmethod
    def delete():
        Baseobject.delete(Vorgabewert._tablename)

    @staticmethod
    def select(pwhere=None, porderby="vgwt_sortrhfg"):
        return Baseobject.select(pclass=Vorgabewert
                                 , pwhere=pwhere, porderby=porderby)

# Vorgabewert
