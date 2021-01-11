from IM_DB import *
from .baseobject import MultilangBaseobject, Baseobject
from .datatype import Datatype
from .interface import Interface
from .languagetext import Languagetext
from .modelelement import Modelelemtype
from .physicals import Storageformat


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
    _columnlist: list = []
    __unknowndom = None

    def __init__(self, psrcname=None, psrcid=None):
        if (len(Domain._columnlist) == 0): Domain._columnlist = Baseobject.gettablecolumns(Domain._tablename)
        super().__init__(tablename=Domain._tablename, prefix=Domain._prefix
                         , multilangcols={'doma_name': Languagetext.DOMA_NAME, 'doma_descr': Languagetext.DOMA_DESCR}
                         , pmodelemtype=Modelelemtype.DOMA
                         , pscrid=psrcid
                         , psrcname=psrcname
                         )

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Domain._tablename
                               , psql="""
CREATE TABLE DOMAINS
    (
     DOMA_ID integer NOT NULL  primary key,
     DOMA_NAME VARCHAR (60) NOT NULL ,
     DOMA_DESCR VARCHAR (4000) NULL ,
     DOMA_TYPE VARCHAR (4) NOT NULL CHECK ( DOMA_TYPE IN ('BIN', 'DAT', 'GRP', 'LOV', 'NUM', 'TXT') ) ,
     DOMA_ORIGIN VARCHAR (6) NOT NULL CHECK ( DOMA_ORIGIN IN ('DER', 'DOM') ) ,
     DOMA_INTF_ID integer NULL ,
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
 OR ( DOMA_BIN_CONTENTTYPE IS NULL AND DOMA_BIN_STFO_ID IS NULL AND DOMA_NUM_FRACT_DIGITS IS NULL AND DOMA_NUM_MAXVALUE IS NULL AND DOMA_NUM_MINVALUE IS NULL AND DOMA_NUM_PHYU_ID IS NULL AND DOMA_NUM_ROUND_VALUE IS NULL AND DOMA_NUM_TOTAL_DIGITS IS NULL AND DOMA_DAT_GRANULARITY IS NULL AND DOMA_DAT_MAXVALUE IS NULL AND DOMA_DAT_MINVALUE IS NULL AND DOMA_TXT_SYNTAXRULE IS NULL))
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
 ,CONSTRAINT DOMA_INTF_FK FOREIGN KEY (     DOMA_INTF_ID) REFERENCES INTERFACES (     INTF_ID )
)"""
                               )

    def getname(self, plang=None):
        return self._getsprachval(colname='doma_name', plang=plang)

    def getmodeid(self):
        return self.doma_id
    # getmodeid

    def isderived(self):
        return self.doma_origin == Domain.DERIVED

    def typeinfo(self):
        daty = Datatype().getbyid(self.doma_daty_id)
        typestring = '' if daty is None else daty.daty_name
        if (self.doma_type in (Domain.TXT, Domain.LOV)):
            infoheaders = (
                Languagetext.transl('Datentyp'), Languagetext.transl('Max. Länge'), Languagetext.transl('Syntaxregel'),
                Languagetext.transl('geändert'))
            infovalues = (parameters.nvl(self.doma_type), parameters.nvl(self.doma_txt_maxlng), parameters.nvl(self.doma_txt_syntaxrule),
                          parameters.nvl(self.doma_uc) + ',' + parameters.nvl(self.doma_dc))
            typestring += parameters.nvl2(self.doma_txt_maxlng,''," ({})".format(self.doma_txt_maxlng))
        elif (self.doma_type == Domain.BIN):
            stf = Storageformat().getbyid(self.doma_bin_stfo_id)
            stfname = stf.getname() if stf is not None else ''
            infoheaders = (Languagetext.transl('Datentyp'), Languagetext.transl('Inhaltstyp'), Languagetext.transl('Format'),
                           Languagetext.transl('geändert'))
            infovalues = (
                parameters.nvl(self.doma_type), self.displcontenttype(), stfname,
                parameters.nvl(self.doma_uc) + ',' + parameters.nvl(self.doma_dc)
            )
            typestring += " ({}, {})".format(self.displcontenttype(),stfname)
        elif (self.doma_type == Domain.GRP):
            infoheaders = (Languagetext.transl('Datentyp'), Languagetext.transl('geändert'))
            infovalues = (self.doma_type, parameters.nvl(self.doma_uc) + ',' + parameters.nvl(self.doma_dc))
        elif (self.doma_type == Domain.NUM):
            infoheaders = (
                Languagetext.transl('Datentyp'), Languagetext.transl('Vorkommast.'), Languagetext.transl('Nachkommast.')
            , Languagetext.transl('Rundungseinh.'), Languagetext.transl('Einheit'), Languagetext.transl('Min. Wert'),
                Languagetext.transl('Max. Wwert')
            , Languagetext.transl('geändert'))
            infovalues = (parameters.nvl(self.doma_type), parameters.nvl(self.doma_num_total_digits), parameters.nvl(self.doma_num_fract_digits),
                          parameters.nvl(self.doma_num_round_value), parameters.nvl(self.doma_num_phyu_id)
                          , parameters.nvl(self.doma_num_minvalue), parameters.nvl(self.doma_num_maxvalue)
                          , parameters.nvl(self.doma_uc) + ',' + parameters.nvl(self.doma_dc))
            typestring += " ({}{}{}{})".format(parameters.nvl(self.doma_num_total_digits)
                                                 , parameters.nvl2(self.doma_num_fract_digits,'', ',{}'.format(self.doma_num_fract_digits))
                                                 , parameters.nvl2(self.doma_num_minvalue,'', '  >= {}'.format(self.doma_num_minvalue))
                                                 , parameters.nvl2(self.doma_num_maxvalue,'', '  <= {}'.format(self.doma_num_maxvalue)))
        elif (self.doma_type == Domain.DAT):
            infoheaders = (
                Languagetext.transl('Datentyp'), Languagetext.transl('Min. Wert'), Languagetext.transl('Max. Wwert'),
                Languagetext.transl('Granularität')
            , Languagetext.transl('geändert'))
            infovalues = (parameters.nvl(self.doma_type), parameters.nvl(self.doma_dat_minvalue), parameters.nvl(self.doma_dat_maxvalue),
                          parameters.nvl(self.displgranul()),
                          parameters.nvl(self.doma_uc) + ',' + parameters.nvl(self.doma_dc))
            typestring += " ({}{}{})".format(
                '' if self.doma_dat_granularity is None else ('  Granularity = {}'.format(self.doma_dat_granularity))
                , '' if self.doma_dat_minvalue is None else '  >= {}'.format(self.doma_dat_minvalue)
                , '' if self.doma_dat_maxvalue is None else '  <= {}'.format(self.doma_dat_maxvalue))
        else:
            infoheaders, infovalues, typestring = None, None, ''
        return [infoheaders, infovalues, typestring]
    # typeinfo

    def typestring(self):
        info = self.typeinfo()
        return info[2]

    # typestring

    def basedatatype(self):
        if self.doma_daty_id is None:
            retval =  ''
        else:
            retval = Datatype().getbyid(self.doma_daty_id).daty_name
        #fi
        return retval

    def refattrcnt(self):
        data = dbDML.select("""select count(*) 
                    from attributes where attr_doma_id = {}
                    """.format(self.doma_id))
        return data[0][0]
    # refattrcnt

    def refcolucnt(self):
        data = dbDML.select("""select count(*) 
                    from columns where colu_doma_id = {}
                    """.format(self.doma_id))
        return data[0][0]
    # refattrcnt

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
    def _displdatatype(dt,plang=None):
        anzDT = {Domain.BIN: Languagetext.transl('Binär', plang=plang)
            , Domain.GRP: Languagetext.transl('Gruppenattribut', plang=plang)
            , Domain.LOV: Languagetext.transl('Werteliste', plang=plang)
            , Domain.NUM: Languagetext.transl('Numerisch', plang=plang)
            , Domain.TXT: Languagetext.transl('Text', plang=plang)
            , Domain.DAT: Languagetext.transl('Zeitpunkt', plang=plang)}
        return anzDT[dt]
    # anzDatentyp

    def displdatatype(self,plang=None):
        return Domain._displdatatype(self.doma_type,plang=plang)

    def displcontenttype(self,plang=None):
        return Domain._displcontenttype(self.doma_bin_contenttype)

    @staticmethod
    def _displcontenttype(dt,plang=None):
        anzDT = {Domain.DRAWING: Languagetext.transl('Bild', plang=plang)
            , Domain.FILM: Languagetext.transl('Film', plang=plang)
            , Domain.IMAGE: Languagetext.transl('Grafik', plang=plang)
            , Domain.TEXT: Languagetext.transl('Text', plang=plang)
            , Domain.SOUND: Languagetext.transl('Ton', plang=plang)
                 }
        if dt in anzDT.keys():
            return anzDT[dt]
        else:
            return Languagetext.transl('Andere', plang=plang)
    # displcontenttype

    def displgranul(self,plang=None):
        return Domain._displgranul(dt=self.doma_dat_granularity,plang=plang)

    @staticmethod
    def _displgranul(dt,plang=None):
        anzDT = {
            Domain.YEAR: Languagetext.transl('Jahr', plang=plang),
            Domain.MILlISECOND: Languagetext.transl('Millisekunde', plang=plang),
            Domain.MINUTE: Languagetext.transl('Minute', plang=plang),
            Domain.MONTH: Languagetext.transl('Monat', plang=plang),
            Domain.QUARTER: Languagetext.transl('Quartal', plang=plang),
            Domain.SECOND: Languagetext.transl('Sekunde', plang=plang),
            Domain.SEMESTER: Languagetext.transl('Semester', plang=plang),
            Domain.HOUR: Languagetext.transl('Stunde', plang=plang),
            Domain.DAY: Languagetext.transl('Tag', plang=plang),
            Domain.WEEK: Languagetext.transl('Woche', plang=plang)
        }
        return anzDT[dt]
    # displgranul

    def getgroupmembers(self):
        members = Domain.select(pwhere="doma_id in (select dgrm_doma_id_member from domaingroup_members where dgrm_doma_id_group = {})".format(self.doma_id))


    @staticmethod
    def fixdomaininterfaces(pinterfacedomains):
        """{doma_id: <filename>}
            domains in non-default file are IM or interface (relationale model) dependent.
           filename = IM_Domains or <relname>_Domains
         """
        interfacename = lambda filename : filename[:-8]
        interfaces = set((pinterfacedomains.values()))
        intf2id = {}
        for filename in interfaces:
            if filename is None: continue
            intf = Interface().getbyuk(pcolname='intf_name',pukvalue=interfacename(filename))
            intfid = None if intf is None else intf.intf_id
            intf2id[filename] = intfid
        #for
        domainterfaces = [(intf2id[filename],domaid) for domaid,filename in pinterfacedomains.items()]
        if len(domainterfaces) > 0:
            dbDML.execmany(psql="update domains set doma_intf_id = ? where doma_id = ?",recs=domainterfaces)
# Domain

class DomaingroupMember(Baseobject):
    _tablename: str = 'domaingroup_members'
    _prefix: str = 'dgrm'
    _columnlist: list = []

    def __init__(self,psrcname=None,psrcid=None ):
        if (len(DomaingroupMember._columnlist) == 0): DomaingroupMember._columnlist = Baseobject.gettablecolumns(DomaingroupMember._tablename)
        super().__init__(tablename=DomaingroupMember._tablename, prefix=DomaingroupMember._prefix
                         , pmodelemtype=Modelelemtype.DGRM
                         , pscrid=psrcid
                         , psrcname=psrcname
                         )

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=DomaingroupMember._tablename
                               , psql="""
CREATE TABLE DOMAINGROUP_MEMBERS
    (
     DGRM_ID INTEGER NOT NULL primary key autoincrement,
     DGRM_NAME VARCHAR (4000) NOT NULL ,
     DGRM_DESCR VARCHAR (4000) NULL ,
     DGRM_IS_MANDATORY VARCHAR (5) NOT NULL CHECK ( DGRM_IS_MANDATORY IN ('FALSE', 'TRUE') ) ,
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
)
    """);

    def getname(self,plang=None):
        return self.dgrm_name
    def getdescr(self,plang=None):
        return self.dgrm_descr

    @staticmethod
    def delete():
        Baseobject.delete(DomaingroupMember._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=DomaingroupMember
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def updmember(pid,pdomaid):
        lupd = """update domaingroup_members 
            set dgrm_doma_id_member = {} 
            where dgrm_id = {}
        """.format(pdomaid,pid)
        dbDML.exec(lupd)

# DomaingroupMember

class DefaultValue(Baseobject):
    _tablename: str = 'default_values'
    _prefix: str = 'deva'
    _columnlist: list = []

    def __init__(self):
        if (len(DefaultValue._columnlist) == 0): DefaultValue._columnlist = Baseobject.gettablecolumns(DefaultValue._tablename)
        super().__init__(tablename=DefaultValue._tablename, prefix=DefaultValue._prefix)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=DefaultValue._tablename
                               , psql="""
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
    ,CONSTRAINT DEVA_UK UNIQUE (DEVA_DOMA_ID ASC, DEVA_VALUE ASC)
    ,CONSTRAINT DEVA_DOMA_FK FOREIGN KEY    (     DEVA_DOMA_ID)
		REFERENCES DOMAINS    (     DOMA_ID )
    ON DELETE CASCADE
)
    """)

    @staticmethod
    def delete():
        Baseobject.delete(DefaultValue._tablename)

    @staticmethod
    def select(pwhere=None, porderby="deva_sort_order"):
        return Baseobject.select(pclass=DefaultValue
                                 , pwhere=pwhere, porderby=porderby)

# DefaultValue
