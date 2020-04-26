from .baseobject import Baseobject
from .sprachtext import Sprachtext
from .datatype import Datatype
from IM_DB import dbDML

class Wertebereich(Baseobject):
    DERIVED:str ='DER'
    DOMAIN:str ='DOM'
    BIN:str='BIN'
    GRP:str='GRP'
    LOV:str='LOV'
    NUM:str='NUM'
    TEXT:str='TEXT'
    ZPKT:str='ZPKT'
    _tablename:str ='wertebereiche'
    _prefix:str ='wrtb'
    _columnlist:list = ['wrtb_id',  'wrtb_business_rule',   'wrtb_name',    'wrtb_beschr',
                        'wrtb_typ', 'wrtb_herkunft',    'wrtb_zpkt_minwert',    'wrtb_zpkt_maxwert',
                        'wrtb_zpkt_granularitaet',  'wrtb_text_maxlng', 'wrtb_text_syntaxregel',    'wrtb_num_maxwert',
                        'wrtb_num_minwert', 'wrtb_num_vorkstellen', 'wrtb_num_nachkstellen',    'wrtb_num_rundng_einh',
                        'wrtb_num_pheh_id', 'wrtb_bin_inhalttyp',   'wrtb_bin_spfo_id', 'wrtb_odm_guid',
                        'wrtb_schn_id', 'wrtb_datatype_odm', 'wrtb_daty_id',    'wrtb_uc',  'wrtb_dc',
                        'wrtb_um',  'wrtb_dm']
    _multilangcols:list = {'wrtb_name':'WRTB_NAME'}
    __unknowndom = None

    def __init__(self):
        super().__init__(tablename=Wertebereich._tablename,prefix=Wertebereich._prefix
                        ,columnlist = Wertebereich._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Wertebereich._tablename
                               , psql="""
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
    wrtb_herkunft            VARCHAR2(6 )
	        CHECK ( wrtb_herkunft IN (
	            'DER',
	            'DOM'
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
    wrtb_schn_id    NUMBER(10) NULL,	
    wrtb_datatype_odm varchar(40),
    wrtb_daty_id integer,
    wrtb_uc         varchar(30) NOT NULL,
    wrtb_dc        varchar(30) NOT NULL,
    wrtb_um        varchar(30),
    wrtb_dm        varchar(30),
 CONSTRAINT wrtb_schn_fk FOREIGN KEY (wrtb_schn_id) references schnittstelle (schn_id),
 CONSTRAINT wrtb_daty_fk FOREIGN KEY (wrtb_daty_id) references datatypes (daty_id)
 )"""
    )
    @staticmethod
    def delete():
        Baseobject.delete(Wertebereich._tablename)

    def getmodellelement(self):
        return Modellelement.getbyelemid(pwrtbid=self.wrtb_id)

    @staticmethod
    def select(pwhere=None,porderby=None):
        wrtbs = Baseobject.select(pclass=Wertebereich
                                ,pwhere=pwhere,porderby=porderby)
        if not Sprachtext.sptxistleer():
            for wrtb in wrtbs:
                wrtb.getsprachvals()
            #for
        #fi
        return wrtbs
    #select

    def getwrtb_name(self,plang):
        try:
            name = self.wrtb_name_L[plang]
        except:
            name = self.wrtb_name
        return name
    #wrtb_name_L

    def getsprachvals(self):
        modeid = self.getmodeid()
        for col in self._multilangcols.keys():
#            print(col,self._multilangcols[col])
#            print(Sprachtext.getsprachtexte(pattrname=self._multilangcols[col], pmodeid=self.getmodeid()))
            self.__dict__[col+'_L'] = Sprachtext.getsprachtexte(pattrname=self._multilangcols[col], pmodeid=modeid)
        #for
    #getsprachvals

    def getmodeid(self):
        data = dbDML.select("""select mode_id from modellelement where mode_wrtb_id = {}""".format(self.wrtb_id))
        try:
            return data[0][0]
        except:
            return None
    #getmodeid
    
    def typeinfo(self):
        def nvl(x, default=''):
            return x if (x is not None) else default

        daty= Datatype().getbyid(self.wrtb_daty_id)
        typestring = daty.daty_name
        if (self.wrtb_typ in (Wertebereich.TEXT,Wertebereich.LOV)):
            infoheaders = (Sprachtext.transl('Datentyp'), Sprachtext.transl('Max. Länge'), Sprachtext.transl('Syntaxregel'), Sprachtext.transl('geändert'))
            infovalues = (nvl(self.wrtb_typ),nvl(self.wrtb_text_maxlng),nvl(self.wrtb_text_syntaxregel),nvl(self.wrtb_uc)+','+nvl(self.wrtb_dc))
            typestring += " ({})".format(nvl(self.wrtb_text_maxlng))
        elif (self.wrtb_typ == Wertebereich.BIN):
            infoheaders = (Sprachtext.transl('Datentyp'), Sprachtext.transl('Inhaltstyp'), Sprachtext.transl('Format'), Sprachtext.transl('geändert'))
            infovalues = (nvl(self.wrtb_typ),Wertebereich.anzinhalttyp(nvl(self.wrtb_bin_inhalttyp)), nvl(self.wrtb_bin_spfo_id),nvl(self.wrtb_uc)+','+nvl(self.wrtb_dc))
            typestring += " ({}, {})".format(Wertebereich.anzinhalttyp(nvl(self.wrtb_bin_inhalttyp)), nvl(self.wrtb_bin_spfo_id))
        elif (self.wrtb_typ ==  Wertebereich.GRP):
            infoheaders = (Sprachtext.transl('Datentyp'), Sprachtext.transl('geändert'))
            infovalues = (self.wrtb_typ,nvl(self.wrtb_uc)+','+nvl(self.wrtb_dc))
        elif (self.wrtb_typ == Wertebereich.NUM):
            infoheaders = (Sprachtext.transl('Datentyp'), Sprachtext.transl('Vorkommast.'), Sprachtext.transl('Nachkommast.')
                           , Sprachtext.transl('Rundungseinh.'), Sprachtext.transl('Einheit'), Sprachtext.transl('Min. Wert'), Sprachtext.transl('Max. Wwert')
                           , Sprachtext.transl('geändert'))
            infovalues = (nvl(self.wrtb_typ),nvl(self.wrtb_num_vorkstellen),nvl(self.wrtb_num_nachkstellen),nvl(self.wrtb_num_rundng_einh),nvl(self.wrtb_num_pheh_id)
                          ,nvl(self.wrtb_num_minwert),nvl(self.wrtb_num_maxwert)
                          ,nvl(self.wrtb_uc)+','+nvl(self.wrtb_dc))
            typestring += " ({}{}) {} {}".format(nvl(self.wrtb_num_vorkstellen)
                                                  , '' if self.wrtb_num_nachkstellen is None else '.' + str(self.wrtb_num_nachkstellen)
                                                  , '' if self.wrtb_num_minwert is None else '>= ' + str(self.wrtb_num_minwert)
                                                  , '' if self.wrtb_num_maxwert is None else '<= ' + str(self.wrtb_num_maxwert))
        elif (self.wrtb_typ == Wertebereich.ZPKT):
            infoheaders = (Sprachtext.transl('Datentyp'), Sprachtext.transl('Min. Wert'), Sprachtext.transl('Max. Wwert'), Sprachtext.transl('Granularität')
                           , Sprachtext.transl('geändert'))
            infovalues = (nvl(self.wrtb_typ),nvl(self.wrtb_zpkt_minwert),nvl(self.wrtb_zpkt_maxwert),Wertebereich.anzgranul(nvl(self.wrtb_zpkt_granularitaet)), nvl(self.wrtb_uc)+','+nvl(self.wrtb_dc))
            typestring += " {} {} {}".format( '' if self.wrtb_zpkt_granularitaet is None else  Sprachtext.transl('Granularität =') + Wertebereich.anzgranul(self.wrtb_zpkt_granularitaet)
                                              , '' if self.wrtb_zpkt_minwert is None else '>= ' + self.wrtb_zpkt_minwert
                                              ,   '' if self.wrtb_zpkt_maxwert is None else '<= ' + self.wrtb_zpkt_maxwert)
        else:  infoheaders,infovalues,typestring = None,None,''
        return [infoheaders,infovalues,typestring]
    #typeinfo
    def typestring(self):
        info = self.typeinfo()
        return info[2]
    #typestring

    def webanker(self):
        return super().webanker()

    def refattranz(self):
        data = dbDML.select("""select count(*) 
                    from attributes where attr_wrtb_id = {}
                    """.format (self.wrtb_id))
        return data[0][0]
    #refattranz

    @staticmethod
    def indexlist(pherkunft,plang):
        data = Wertebereich.select(pwhere="wrtb_herkunft = '{}'".format(pherkunft), porderby='wrtb_name')
        indexlist = [['{} ({})'.format(d.getwrtb_name(plang),d.refattranz())
                    ,d.webanker(),d.wrtb_id] for d in data]
        return indexlist

    #indexlist

    @staticmethod
    def getbyname(pname):
        return Wertebereich().getbyuk(pcolname='wrtb_name', pukvalue=pname)
    # getbyname¨

    @staticmethod
    def getunknown():
        if Wertebereich.__unknowndom is None:
            dom = Wertebereich.getbyname(pname='Unknown')
            if dom.wrtb_id is None:
                dom = Wertebereich.getbyname(pname='unknown')
            #fi
            Wertebereich.__unknowndom = dom
        #fi
        return Wertebereich.__unknowndom
    #getunknown

    @staticmethod
    def anzdatentyp(dt):
        anzDT = {'BIN': Sprachtext.transl('Binär')
            , 'GRP': Sprachtext.transl('Gruppenattribut')
            , 'LOV': Sprachtext.transl('Werteliste')
            , 'NUM': Sprachtext.transl('Numerisch')
            , 'TEXT': Sprachtext.transl('Text')
            , 'ZPKT': Sprachtext.transl('Zeitpunkt')}
        return anzDT[dt]
    # anzDatentyp

    @staticmethod
    def anzinhalttyp(dt):
        anzDT = {'BILD': Sprachtext.transl('Bild')
            , 'FILM': Sprachtext.transl('Film')
            , 'GRAPH': Sprachtext.transl('Grafik')
            , 'TEXT': Sprachtext.transl('Text')
            , 'TON': Sprachtext.transl('Ton')}
        return anzDT[dt]
    # anzinhalttyp

    @staticmethod
    def anzgranul(dt):
        anzDT = {
            'JAHR': Sprachtext.transl('Jahr'),
            'MILLISEKUNDE': Sprachtext.transl('Millisekunde'),
            'MINUTE': Sprachtext.transl('Minute'),
            'MONAT': Sprachtext.transl('Monat'),
            'QUARTAL': Sprachtext.transl('Quartal'),
            'SEKUNDE': Sprachtext.transl('Sekunde'),
            'SEMESTER': Sprachtext.transl('Semester'),
            'STUNDE': Sprachtext.transl('Stunde'),
            'TAG': Sprachtext.transl('Tag'),
            'WOCHE': Sprachtext.transl('Woche')
        }
        return anzDT[dt]
    # anzgranul

#Wertebereich

class Wertebereichgruppe(Baseobject):
    _tablename: str = 'wertebereichgruppen'
    _prefix: str = 'wbgr'
    _columnlist: list = ['wbgr_id', 'wbgr_name',    'wbgr_beschr',
                        'wbgr_wrtb_id_gruppe',  'wbgr_wrtb_id_member',  'wbgr_type_ref',
                        'wbgr_uc',  'wbgr_dc',  'wbgr_um',
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
    wbgr_wrtb_id_gruppe   integer not null ,
     wbgr_wrtb_id_member integer not null , 
	 wbgr_type_ref	varchar(40),
     wbgr_uc varchar (30) not null , 
     wbgr_dc varchar (30) not null , 
     wbgr_um varchar (30)    null,
      wbgr_dm varchar (30) null
,constraint wbgr_wrtb_uk unique (wbgr_wrtb_id_gruppe ,wbgr_name )
,constraint wbgr_wrtb_fk_gruppe foreign key(wbgr_wrtb_id_gruppe)
        references wertebereich(wrtb_id) on delete cascade
,constraint wbgr_wrtb_fk_member foreign key(wbgr_wrtb_id_member)
        references wertebereich(wrtb_id) 
	)
    """);
    @staticmethod
    def delete():
        Baseobject.delete(Wertebereichgruppe._tablename)

    @staticmethod
    def select(pwhere=None,porderby=None):
        return Baseobject.select(pclass=Wertebereichgruppe
                                ,pwhere=pwhere,porderby=porderby)

    @staticmethod
    def updmembers():
        ukwnid = Wertebereich().getunknown().wrtb_id
        lupd= """update wertebereichgruppen 
            set wbgr_wrtb_id_member = 
            case when (select wrtb_id
                     from wertebereiche 
                    where wrtb_odm_guid = wbgr_type_ref) 
                is null
             then {} 
             else (select wrtb_id
             from wertebereiche 
             where wrtb_odm_guid = wbgr_type_ref)
             end
            where wbgr_wrtb_id_member = {}
        """.format(ukwnid,ukwnid)
        dbDML.exec(lupd)
#Wertebereichgruppe

class Vorgabewert(Baseobject):
    _tablename: str = 'vorgabewerte'
    _prefix: str = 'vgwt'
    _columnlist: list = ['vgwt_id',	'vgwt_guid',	'vgwt_wert',
                        'vgwt_sortrhfg',	'vgwt_wrtb_id',	'vgwt_anzeige',
                        'vgwt_beschr',	'vgwt_uc',	'vgwt_dc',
                        'vgwt_um',	'vgwt_dm'
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
    vgwt_wrtb_id           integer NOT NULL,
    vgwt_anzeige   varchar(200),
    vgwt_beschr    varchar(4000),
    vgwt_uc         varchar(30) NOT NULL,
    vgwt_dc        varchar(30) NOT NULL,
    vgwt_um        varchar(30),
    vgwt_dm        varchar(30),
	constraint vgwt_uk unique (vgwt_wrtb_id,vgwt_wert),
	constraint vgwt_wrtb_fk foreign key (vgwt_wrtb_id) references wertebereiche(wrtb_id) ON DELETE CASCADE
    )
    """);
    @staticmethod
    def delete():
        Baseobject.delete(Vorgabewert._tablename)

    @staticmethod
    def select(pwhere=None,porderby=None):
        return Baseobject.select(pclass=Vorgabewert
                                ,pwhere=pwhere,porderby=porderby)

#Vorgabewert

