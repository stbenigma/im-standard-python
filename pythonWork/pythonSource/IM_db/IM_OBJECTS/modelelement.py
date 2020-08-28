from .baseobject import Baseobject
from datetime import date
from IM_DB import dbDML

class Modelelemtype(Baseobject):
    ENTI:str='ENTI'
    BURU:str='BURU'
    SYNO:str='SYNO'
    RELA:str='RELA'
    ATTR:str='ATTR'
    DOMA:str= 'DOMA'
    ORGU:str= 'ORGU'
    TABL:str='TABL'
    INTF:str= 'INTF'
    COLU:str= 'COLU'
    ARCS:str='ARCS'
    _tablename:str = 'modelelem_type'
    _prefix:str = 'melt'
    _columnlist:list = ['melt_id',  'melt_shortname',    'melt_name',
                        'melt_uc',  'melt_dc',  'melt_um',
                        'melt_dm']
    __meltids:dict = {}

    def __init__(self, pshortname=None, pname=None):
        super().__init__(tablename= Modelelemtype._tablename, prefix= Modelelemtype._prefix
                         , columnlist = Modelelemtype._columnlist)
        self.melt_shortname = pshortname
        self.melt_name = pname
        self.melt_uc = 'SYS'
        self.melt_dc = date.today()

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Modelelemtype._tablename
                                ,psql="""
CREATE TABLE MODELELEM_TYPE
    (
     MELT_ID INTEGER NOT NULL primary key autoincrement,
     MELT_SHORTNAME VARCHAR (4) NOT NULL CHECK ( MELT_SHORTNAME IN ('ARCS', 'ATTR', 'BURU', 'COLU', 'DOMA', 'ENTI', 'INTF', 'ORGU', 'RELA', 'SYNO', 'TABL') ) ,
     MELT_NAME VARCHAR (60) NOT NULL ,
     MELT_UC VARCHAR(30) NULL  ,
     MELT_DC VARCHAR (30) NOT NULL ,
     MELT_UM VARCHAR (30) NULL ,
     MELT_DM VARCHAR (30) NULL
    ,CONSTRAINT MELT_UN UNIQUE (MELT_SHORTNAME ASC)
    ,CONSTRAINT MELT_UN2 UNIQUE (MELT_NAME ASC)
) 
""")

    @staticmethod
    def delete():
        Baseobject.delete(Modelelemtype._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Modelelemtype, pwhere=pwhere, porderby=porderby)

    def insert(self):
        meltid = super().insert()
        Modelelemtype.__meltids[self.melt_shortname] = meltid

    @staticmethod
    def fillmelt():
        # melt_shortname,  melt_name    ,melt_uc,  melt_dc
        Modelelemtype(pshortname=Modelelemtype.ARCS, pname='Arc').insert()
        Modelelemtype(pshortname=Modelelemtype.ATTR, pname='Attribut').insert()
        Modelelemtype(pshortname=Modelelemtype.BURU, pname='Business Rule').insert()
        Modelelemtype(pshortname=Modelelemtype.COLU, pname='Column').insert()
        Modelelemtype(pshortname=Modelelemtype.DOMA, pname='Wertebereich').insert()
        Modelelemtype(pshortname=Modelelemtype.ENTI, pname='Entität').insert()
        Modelelemtype(pshortname=Modelelemtype.INTF, pname='Schnittstelle').insert()
        Modelelemtype(pshortname=Modelelemtype.ORGU, pname='Organisationseinheit').insert()
        Modelelemtype(pshortname=Modelelemtype.RELA, pname='Beziehung').insert()
        Modelelemtype(pshortname=Modelelemtype.SYNO, pname='Synonym').insert()
        Modelelemtype(pshortname=Modelelemtype.TABL, pname='Tabelle').insert()

    @staticmethod
    def getidbyshortname (pshortname):
        return Modelelemtype.__meltids[pshortname]

    @staticmethod
    def getshortname (pmeltid:int):
        return Modelelemtype().getbyid(pid).melt_shortname

    @staticmethod
    def getbyshortname (pshortname):
        return Modelelemtype().getbyid(Modelelemtype.getidbyshortname(pshortname))

    @staticmethod
    def type2melt(type):
        trans = {"Entity": Modelelemtype.ENTI
                , "Attribute": Modelelemtype.ATTR
                , "Relation": Modelelemtype.RELA
                , "Table": Modelelemtype.TABL
                , "Column": Modelelemtype.INTF
                , "Arcs": Modelelemtype.ARCS
                , "FKIndexAssociation": ""
                 }
        return trans[type]
    # type2melt
#Modelelemtype

class Modelelement(Baseobject):
    """Modelelement is a supertype of a lot of entities. It shares common attributes and relationships
        It's ID is identical to id's in subtype tables.
        So Modelelement is created first (with a system generated ID, unique over all subtables). It's ID is then
        used as ID' of the subtables
    """
    _tablename:str = 'modelelement'
    _prefix:str = 'mode'
    _columnlist:list = ['mode_id',  'mode_type', 'mode_melt_id'
                        , 'mode_syno_id',
                        'mode_wrtb_id', 'mode_attr_id', 'mode_buru_id',
                        'mode_rela_id', 'mode_enti_id', 'mode_orge_id',
                        'mode_tabl_id', 'mode_scha_id',    'mode_schn_id']

    def __init__(self, pmeltshortname):
        super().__init__(tablename= Modelelement._tablename, prefix= Modelelement._prefix
                         , columnlist = Modelelement._columnlist)
        self.mode_type = pmeltshortname
        self.mode_melt_id = Modelelemtype.getidbyshortname(pshortname=pmeltshortname)
    #__init__

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Modelelement._tablename
                                ,psql="""
CREATE TABLE MODELELEMENT
    (
     MODE_ID INTEGER NOT NULL primary key autoincrement ,
     MODE_TYPE VARCHAR (4) NOT NULL CHECK ( MODE_TYPE IN ('ARCS', 'ATTR', 'BURU', 'COLU', 'DOMA', 'ENTI', 'INTF', 'ORGU', 'RELA', 'SYNO', 'TABL') ) ,
     MODE_MELT_ID NUMERIC (10) NOT NULL
    ,mode_syno_id   integer NULL,
    mode_wrtb_id   integer NULL,
    mode_attr_id   integer NULL,
    mode_buru_id   integer NULL,
    mode_rela_id   integer NULL,
    mode_enti_id   integer NULL,
    mode_orge_id   integer NULL,    
    mode_tabl_id  integer NULL,
    mode_scha_id  integer NULL,    
    mode_schn_id  integer NULL
     ,CONSTRAINT MODE_MELT_FK FOREIGN KEY     (     MODE_MELT_ID)
        REFERENCES MODELELEM_TYPE(     MELT_ID )
     ON DELETE NO ACTION     ON UPDATE NO ACTION
)
""")
    def getodmguid(self):
        extref = ExternalRef.getsources(pmodeid=self.mode_id,psource=ExternalRef.ODM)
        if len(extref == 0): return None
        if len(extref == 1): return extref[0].getsrcid()
        raise Exception("too many rows for source '{}', id '{}'".format(ExternalRef.ODM,self.mode_id))
    #getodmguid

    @staticmethod
    def delete(pwhere=''):
        Baseobject.delete(Modelelement._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Modelelement
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def __id2meltid(pentiid=None,pattrid=None,pburuid=None,pwrtbid=None
                    ,prelaid=None,porgeid=None,psynoid=None,ptablid=None
                    ,pschaid=None,pschnid=None):
        if pentiid is not None: meltid = (Modelelemtype.ENTI, pentiid)
        elif pwrtbid is not None: meltid = (Modelelemtype.DOMA, pwrtbid)
        elif pattrid is not None: meltid = (Modelelemtype.ATTR, pattrid)
        elif psynoid is not None: meltid = (Modelelemtype.SYNO, psynoid)
        elif prelaid is not None: meltid = (Modelelemtype.RELA, prelaid)
        elif pburuid is not None: meltid = (Modelelemtype.BURU, pburuid)
        elif ptablid is not None: meltid = (Modelelemtype.TABL, ptablid)
        elif pschaid is not None: meltid = (Modelelemtype.INTF, pschaid)
        elif pschnid is not None: meltid = (Modelelemtype.INTF, pschnid)
        elif porgeid is not None: meltid = (Modelelemtype.ORGU, porgeid)
        else: meltid = (None,None)
        #fi
        return meltid
    #id2meltid
    @staticmethod
    def __id2melt(pentiid=None,pattrid=None,pburuid=None,pwrtbid=None
                    ,prelaid=None,porgeid=None,psynoid=None,ptablid=None
                    ,pschaid=None,pschnid=None):
        return Modelelement.__id2meltid(pentiid=pentiid, pattrid=pattrid, pburuid=pburuid, pwrtbid=pwrtbid
                                        , prelaid=prelaid, porgeid=porgeid, psynoid=psynoid, ptablid=ptablid
                                        , pschaid=pschaid, pschnid=pschnid)[0]

    @staticmethod
    def getbyelemid (pentiid=None,pattrid=None,pburuid=None,pwrtbid=None
                    ,prelaid=None,porgeid=None,psynoid=None,ptablid=None
                    ,pschaid=None,pschnid=None):
        meltid = Modelelement.__id2meltid(pentiid=pentiid, pattrid=pattrid, pburuid=pburuid, pwrtbid=pwrtbid
                                          , prelaid=prelaid, porgeid=porgeid, psynoid=psynoid, ptablid=ptablid
                                          , pschaid=pschaid, pschnid=pschnid)
        colname,id = 'mode_{}_id'.format(meltid[0]),meltid[1]
        data = Modelelement.select(pwhere="{} = '{}'".format(colname.lower(), id))
        if ((data is None) or (len(data) == 0)): return None
        return data[0]


    @staticmethod
    def getidbyelemid (pentiid=None,pattrid=None,pburuid=None,pwrtbid=None
                    ,prelaid=None,porgeid=None,psynoid=None,ptablid=None
                    ,pschaid=None,pschnid=None):
        mode = Modelelement.getbyelemid(pentiid=pentiid, pattrid=pattrid, pburuid=pburuid, pwrtbid=pwrtbid
                                        , prelaid=prelaid, porgeid=porgeid, psynoid=psynoid, ptablid=ptablid
                                        , pschaid=pschaid, pschnid=pschnid)
        return None if mode is None else mode.mode_id
    #getidbyelemid
    
    @staticmethod
    def getelement(pmodeid):
        mode = Modelelement.getbyid(pmodeid)
        meltkrz = Modelelemtype.getshortname(pmeltid=mode.mode_melt_id)
        if meltkrz == Modelelemtype.SYNO: element = Synonym.getbyid(mode_ref_id)
        elif meltkrz == Modelelemtype.DOMA: element = Wertebereich.getbyid(mode_wrtb_id)
        elif meltkrz == Modelelemtype.ATTR: element = Attribut.getbyid(mode_attr_id)
        elif meltkrz == Modelelemtype.BURU: element = Buseinssrule.getbyid(mode_buru_id)
        elif meltkrz == Modelelemtype.RELA: element = Relation.getbyid(mode_rela_id)
        elif meltkrz == Modelelemtype.ENTI: element = Entitaet.getbyid(mode_enti_id)
        elif meltkrz == Modelelemtype.ORGU: element = Organisationseinheit.getbyid(mode_orge_id)
        elif meltkrz == Modelelemtype.TABL: element = Tabelle.getbyid(mode_tabl_id)
        elif meltkrz == Modelelemtype.INTF: element = Schnittstelleattr.getbyid(mode_scha_id)
        elif meltkrz == Modelelemtype.INTF: element = Schnittstelle.getbyid(mode_schn_id)
        elif meltkrz == Modelelemtype.ARC: element = Arc.getbyid(mode_id)
        else: element = None
        return element


    @staticmethod
    def insertmode(pentiid=None,pattrid=None,pburuid=None,pwrtbid=None
                    ,prelaid=None,porgeid=None,psynoid=None,ptablid=None
                    ,pschaid=None,pschnid=None):
        refid=pentiid if pentiid is not None\
                    else pattrid if pattrid is not None\
                    else pburuid if pburuid is not None\
                    else pwrtbid if pwrtbid is not None\
                    else prelaid if prelaid is not None\
                    else porgeid if porgeid is not None\
                    else psynoid if psynoid is not None\
                    else ptablid if ptablid is not None\
                    else pschaid if pschaid is not None\
                    else pschnid if pschnid is not None\
                    else mode.mode_ref_id
        meltid=Modelelemtype.getidbyshortname\
                    (pshortname=Modelelement.__id2melt(pentiid=pentiid, pattrid=pattrid, pburuid=pburuid, pwrtbid=pwrtbid
                                                       , prelaid=prelaid, porgeid=porgeid, psynoid=psynoid, ptablid=ptablid
                                                       , pschaid=pschaid, pschnid=pschnid))
        mode = Modelelement(pmeltshortname=meltid)
        mode.mode_ref_id = refid
        mode.mode_wrtb_id = pwrtbid
        mode.mode_attr_id = pattrid
        mode.mode_buru_id = pburuid
        mode.mode_rela_id = prelaid
        mode.mode_enti_id = pentiid
        mode.mode_orge_id = porgeid
        mode.mode_syno_id = psynoid
        mode.mode_tabl_id = ptablid
        mode.mode_scha_id = pschaid
        mode.mode_schn_id = pschnid
        mode.insert()
        return mode.mode_id
    #insertmodelelement
#modelelement

class ExternalRef(Baseobject):
    ODM: str = 'ODM'
    _tablename: str = 'externalrefs'
    _prefix: str = 'extr'
    _columnlist: list = ['extr_id', 'extr_source', 'extr_source_id', 'extr_mode_id']

    def __init__(self,psrc,psrcid,pmodeid):
        super().__init__(tablename=ExternalRef._tablename, prefix=ExternalRef._prefix
                         , columnlist=ExternalRef._columnlist)
        self.extr_source = psrc
        self.extr_source_id = psrcid
        self.extr_mode_id = pmodeid
    #__init__

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=ExternalRef._tablename
                               , psql="""
CREATE TABLE externalrefs(
    extr_id            integer primary key autoincrement,
    extr_source        VARCHAR(20) NOT NULL,
    extr_source_id     VARCHAR(250) NOT NULL,
    extr_mode_id        integer NOT NULL,
	CONSTRAINT extr_un UNIQUE(extr_source,extr_mode_id),
	CONSTRAINT extr_mode_fk FOREIGN KEY ( extr_mode_id) 
		  	      REFERENCES modelelement ( mode_id ) 
		  	      ON DELETE CASCADE 
    )"""
                               )
    def getsrcid(self):
        return self.extr_source_id


    @staticmethod
    def getsources(self,pmodeid,psource=None):
        sources = ExternalRef.select(pwhere="extr_mode_id = {} and extr_source like '{}'"
                                     .format(pmodeid, psource if psource is not None else '%'))
        return sources
    #getsources


    @staticmethod
    def getmodesbysrcid(self,psource,psourceid):
        modes = ExternalRef.select(pwhere="extr_source = '{}' and extr_sourceid= '{}'"
                                   .format(psource,psourceid))
        return modes
    #getmodbybysrcid

    @staticmethod
    def get1modebysrcid(self,psource,psourceid):
        modes = ExternalRef.getmodebyodm(psource,psourceid)
        if len(modes) == 0: return None
        if len(modes)== 1: return modes[0]
        raise Exception("too many rows for source '{}' sourceid '{}'".format(psource,psourceid))
    #get1modebysrcid

    @staticmethod
    def delete():
        Baseobject.delete(ExternalRef._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=ExternalRef
                                 , pwhere=pwhere, porderby=porderby)
    @staticmethod
    def getbymodeid(pmodeid):
        return ExternalRef.select(pwhere="extr_mode_id = {}".format(pmodeid))

    @staticmethod
    def insertextrefs(pmodeid:int,preflist:dict):
        """insert list of ext.ref entires for one modeid"""
        dbDML.insert(psql="insert into {} ({}) values ({})"
                          .format(ExternalRef._tablename
                                 ,Baseobject.columnsliststring(pcollist=ExternalRef._columnlist)
                                ,Baseobject.columnsliststring(pcollist=ExternalRef._columnlist,pplaceholder=True))
                     ,rec=[(None,pmodeid,key,value) for key, value in preflist.items()])

# ExternalRef

