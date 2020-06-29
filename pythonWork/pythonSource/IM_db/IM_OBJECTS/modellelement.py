from .baseobject import Baseobject
from datetime import date

class Modellelemtyp(Baseobject):
    ENTI:str='ENTI'
    BURU:str='BURU'
    SYNO:str='SYNO'
    RELA:str='RELA'
    ATTR:str='ATTR'
    WRTB:str='WRTB'
    ORGE:str='ORGE'
    TABL:str='TABL'
    SCHN:str='SCHN'
    SCHA:str='SCHA'
    ARCS:str='ARCS'
    _tablename:str = 'modellelem_typ'
    _prefix:str = 'melt'
    _columnlist:list = ['melt_id',  'melt_kurzname',    'melt_name',
                        'melt_uc',  'melt_dc',  'melt_um',
                        'melt_dm']

    def __init__(self,pkurzname=None,pname=None):
        super().__init__(tablename= Modellelemtyp._tablename, prefix= Modellelemtyp._prefix
                        ,columnlist = Modellelemtyp._columnlist)
        self.melt_kurzname = pkurzname
        self.melt_name = pname
        self.melt_uc = 'SYS'
        self.melt_dc = date.today()

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Modellelemtyp._tablename
                                ,psql="""
CREATE TABLE modellelem_typ(
    melt_id                  integer NOT NULL primary key autoincrement,
    melt_kurzname            varchar(4)NOT NULL
        CHECK(melt_kurzname IN(
   'ATTR',
   'RELA',
   'BURU',
   'ENTI',
   'WRTB',
   'TABL',
   'SCHA',
   'SCHN',
   'SYNO',
   'ORGE',
   'ARCS'
        )),
    melt_name                varchar(60 )NOT NULL,
    melt_uc                  varchar(30 )NOT NULL,
    melt_dc                  varchar(30)NOT NULL,
    melt_um                  varchar(30 )NULL,
    melt_dm                  varchar(30)NULL,
	CONSTRAINT melt_un UNIQUE(melt_kurzname),
	CONSTRAINT melt_un2 UNIQUE(melt_name)
) 
""")

    @staticmethod
    def delete():
        Baseobject.delete(Modellelemtyp._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Modellelemtyp,pwhere=pwhere, porderby=porderby)

    @staticmethod
    def fillmelt():
        # melt_kurzname,  melt_name    ,melt_uc,  melt_dc
        Modellelemtyp(pkurzname=Modellelemtyp.ATTR, pname='Attribut').insert()
        Modellelemtyp(pkurzname=Modellelemtyp.RELA, pname='Beziehung').insert()
        Modellelemtyp(pkurzname=Modellelemtyp.BURU, pname='Business Rule').insert()
        Modellelemtyp(pkurzname=Modellelemtyp.ENTI, pname='Entität').insert()
        Modellelemtyp(pkurzname=Modellelemtyp.WRTB, pname='Wertebereich').insert()
        Modellelemtyp(pkurzname=Modellelemtyp.SYNO, pname='Synonym').insert()
        Modellelemtyp(pkurzname=Modellelemtyp.ORGE, pname='Organisationseinheit').insert()
        Modellelemtyp(pkurzname=Modellelemtyp.TABL, pname='Tabelle').insert()
        Modellelemtyp(pkurzname=Modellelemtyp.SCHA, pname='Schnittstellenattribut').insert()
        Modellelemtyp(pkurzname=Modellelemtyp.SCHN, pname='Schnittstelle').insert()
        Modellelemtyp(pkurzname=Modellelemtyp.ARCS, pname='Arc').insert()
    #fillmelt


    @staticmethod
    def getbyshortname (pkurzname):
        data = Modellelemtyp.select(pwhere="melt_kurzname = '{}'".format(pkurzname))
        if ((data is None) or (len(data) == 0)):
            raise Exception("no modellelem_typ found for {}".format(pkurzname))
        return data[0]
    #getbyshortname

    @staticmethod
    def getidbyshortname (pkurzname):
        return Modellelemtyp.getbyshortname(pkurzname=pkurzname).melt_id
    #getidbyshortname
    @staticmethod
    def type2melt(type):
        trans = {"Entity": Modellelemtyp.ENTI
                , "Attribute": Modellelemtyp.ATTR
                , "Relation": Modellelemtyp.RELA
                , "Table": Modellelemtyp.TABL
                , "Column": Modellelemtyp.SCHA
                , "Arcs": Modellelemtyp.ARCS
                , "FKIndexAssociation": ""
                 }
        return trans[type]
    # type2melt
#Modellelemtyp

class Modellelement(Baseobject):
    _tablename:str = 'modellelement'
    _prefix:str = 'mode'
    _columnlist:list = ['mode_id',  'mode_melt_id', 'mode_syno_id',
                        'mode_wrtb_id', 'mode_attr_id', 'mode_buru_id',
                        'mode_rela_id', 'mode_enti_id', 'mode_orge_id',
                        'mode_tabl_id', 'mode_scha_id',    'mode_schn_id',
                        'mode_uc',  'mode_dc',  'mode_um',
                        'mode_dm']

    def __init__(self,pmeltid=None, puc=None, pdc=None):
        super().__init__(tablename= Modellelement._tablename, prefix= Modellelement._prefix
                        ,columnlist = Modellelement._columnlist)
        self.mode_melt_id = pmeltid
        self.mode_uc = puc
        self.mode_dc = pdc
    #__init__

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Modellelement._tablename
                                ,psql="""
CREATE TABLE modellelement(
    mode_id        integer NOT NULL primary key autoincrement,
    mode_melt_id   integer NULL,
    mode_syno_id   integer NULL,
    mode_wrtb_id   integer NULL,
    mode_attr_id   integer NULL,
    mode_buru_id   integer NULL,
    mode_rela_id   integer NULL,
    mode_enti_id   integer NULL,
    mode_orge_id   integer NULL,    
    mode_tabl_id  integer NULL,
    mode_scha_id  integer NULL,    
    mode_schn_id  integer NULL,    
    mode_uc        varchar(30 )NOT NULL,
    mode_dc        varchar(30)NOT NULL,
    mode_um        varchar(30 )NULL,
    mode_dm        varchar(30)NULL,
	CONSTRAINT mode_uk UNIQUE(mode_wrtb_id,
	       mode_attr_id,
	       mode_buru_id,
	       mode_enti_id,
	       mode_rela_id,mode_scha_id,mode_tabl_id,mode_schn_id),
		   CONSTRAINT fkarc_4 CHECK (case WHEN mode_buru_id IS NULL THEN 0 else 1 end
		   	 						+case WHEN mode_enti_id IS NULL THEN 0 else 1 end	
		   	 						+case WHEN mode_tabl_id IS NULL THEN 0 else 1 end	
		   	 						+case WHEN mode_scha_id IS NULL THEN 0 else 1 end	
		   	 						+case WHEN mode_syno_id IS NULL THEN 0 else 1 end	
		   	 						+case WHEN mode_rela_id IS NULL THEN 0 else 1 end	
		   	 						+case WHEN mode_wrtb_id IS NULL THEN 0 else 1 end	
		   	 						+case WHEN mode_attr_id IS NULL THEN 0 else 1 end	
		   	 						+case WHEN mode_orge_id IS NULL THEN 0 else 1 end	
		   	 						+case WHEN mode_schn_id IS NULL THEN 0 else 1 end	
									< 2
								),
		CONSTRAINT mode_syno_fk_ist FOREIGN KEY(mode_syno_id)
	  REFERENCES synonyme(syno_id)
	      ON DELETE CASCADE,
	    CONSTRAINT mode_attr_fk_ist FOREIGN KEY(mode_attr_id)
	  REFERENCES attributes(attr_id)
	      ON DELETE CASCADE,
	    CONSTRAINT mode_rela_fk FOREIGN KEY(mode_rela_id)
	  REFERENCES relations(rela_id)
	   	ON DELETE CASCADE,
	    CONSTRAINT mode_enti_fk_ist FOREIGN KEY(mode_enti_id)
	  REFERENCES entitaeten(enti_id)
	      ON DELETE CASCADE,
	    CONSTRAINT mode_wrtb_fk_ist FOREIGN KEY(mode_wrtb_id)
	   	  REFERENCES wertebereiche(wrtb_id)
	   	      ON DELETE CASCADE,
	CONSTRAINT MODE_SCHA_FK FOREIGN KEY ( MODE_SCHA_ID) 
	      REFERENCES SCHNITTSTELLE_ATTR (SCHA_ID ) 
	      ON DELETE CASCADE ,
	CONSTRAINT MODE_TABL_FK FOREIGN KEY ( MODE_TABL_ID) 
	  	      REFERENCES TABELLE ( TABL_ID ) 
	  	      ON DELETE CASCADE ,
	CONSTRAINT MODE_SCHN_FK FOREIGN KEY ( MODE_SCHN_ID) 
		  	      REFERENCES schnittstelle ( schn_ID ) 
		  	      ON DELETE CASCADE ,
	    CONSTRAINT mode_melt_fk_verantw FOREIGN KEY(mode_melt_id)
	  REFERENCES modellelem_typ(melt_id)
	  		ON DELETE CASCADE 
)
""")
    def getodmguid(self):
        extref = ExternalRef.getsources(pmodeid=self.mode_id,psource=ExternalRef.ODM)
        if len(extref == 0): return None
        if len(extref == 1): return extref[0].getsrcid()
        raise Exception("too many rows for source '{}', id '{}'".format(ExternalRef.ODM,self.mode_id))
    #getodmguid

    @staticmethod
    def delete():
        Baseobject.delete(Modellelement._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Modellelement
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def __id2meltid(pentiid=None,pattrid=None,pburuid=None,pwrtbid=None
                    ,prelaid=None,porgeid=None,psynoid=None,ptablid=None
                    ,pschaid=None,pschnid=None):
        if pentiid is not None: meltid = (Modellelemtyp.ENTI, pentiid)
        elif pwrtbid is not None: meltid = (Modellelemtyp.WRTB, pwrtbid)
        elif pattrid is not None: meltid = (Modellelemtyp.ATTR, pattrid)
        elif psynoid is not None: meltid = (Modellelemtyp.SYNO, psynoid)
        elif prelaid is not None: meltid = (Modellelemtyp.RELA, prelaid)
        elif pburuid is not None: meltid = (Modellelemtyp.BURU, pburuid)
        elif ptablid is not None: meltid = (Modellelemtyp.TABL, ptablid)
        elif pschaid is not None: meltid = (Modellelemtyp.SCHA, pschaid)
        elif pschnid is not None: meltid = (Modellelemtyp.SCHN, pschnid)
        elif porgeid is not None: meltid = (Modellelemtyp.ORGE, porgeid)
        else: meltid = (None,None)
        #fi
        return meltid
    #id2meltid
    @staticmethod
    def __id2melt(pentiid=None,pattrid=None,pburuid=None,pwrtbid=None
                    ,prelaid=None,porgeid=None,psynoid=None,ptablid=None
                    ,pschaid=None,pschnid=None):
        return Modellelement.__id2meltid(pentiid=pentiid,pattrid=pattrid,pburuid=pburuid,pwrtbid=pwrtbid
                    ,prelaid=prelaid,porgeid=porgeid,psynoid=psynoid,ptablid=ptablid
                    ,pschaid=pschaid,pschnid=pschnid)[0]
    def __id2id(pentiid=None,pattrid=None,pburuid=None,pwrtbid=None
                    ,prelaid=None,porgeid=None,psynoid=None,ptablid=None
                    ,pschaid=None,pschnid=None):
        return Modellelement.__id2meltid(pentiid=pentiid,pattrid=pattrid,pburuid=pburuid,pwrtbid=pwrtbid
                    ,prelaid=prelaid,porgeid=porgeid,psynoid=psynoid,ptablid=ptablid
                    ,pschaid=pschaid,pschnid=pschnid)[1]

    @staticmethod
    def getbyelemid (pentiid=None,pattrid=None,pburuid=None,pwrtbid=None
                    ,prelaid=None,porgeid=None,psynoid=None,ptablid=None
                    ,pschaid=None,pschnid=None):
        meltid = Modellelement.__id2meltid(pentiid=pentiid,pattrid=pattrid,pburuid=pburuid,pwrtbid=pwrtbid
                    ,prelaid=prelaid,porgeid=porgeid,psynoid=psynoid,ptablid=ptablid
                    ,pschaid=pschaid,pschnid=pschnid)
        colname,id = 'mode_{}_id'.format(meltid[0]),meltid[1]
        data = Modellelement.select(pwhere="{} = '{}'".format(colname.lower(),id))
        if ((data is None) or (len(data) == 0)): return None
        return data[0]
    #getbyshortname

    @staticmethod
    def getidbyelemid (pentiid=None,pattrid=None,pburuid=None,pwrtbid=None
                    ,prelaid=None,porgeid=None,psynoid=None,ptablid=None
                    ,pschaid=None,pschnid=None):
        mode = Modellelement.getbyelemid(pentiid=pentiid,pattrid=pattrid,pburuid=pburuid,pwrtbid=pwrtbid
                    ,prelaid=prelaid,porgeid=porgeid,psynoid=psynoid,ptablid=ptablid
                    ,pschaid=pschaid,pschnid=pschnid)
        return None if mode is None else mode.mode_id
    #getidbyelemid
    
    @staticmethod
    def getelement(pmodeid):
        mode = Modellelement.getbyid(pmodeid)
        if mode.mode_syno_id is not None: element = Synonym.getbyid(mode_syno_id)
        elif mode.mode_wrtb_id is not None: element = Wertebereich.getbyid(mode_wrtb_id)
        elif mode.mode_attr_id is not None: element = Attribut.getbyid(mode_attr_id)
        elif mode.mode_buru_id is not None: element = Buseinssrule.getbyid(mode_buru_id)
        elif mode.mode_rela_id is not None: element = Relation.getbyid(mode_rela_id)
        elif mode.mode_enti_id is not None: element = Entitaet.getbyid(mode_enti_id)
        elif mode.mode_orge_id is not None: element = Organisationseinheit.getbyid(mode_orge_id)
        elif mode.mode_tabl_id is not None: element = Tabelle.getbyid(mode_tabl_id)
        elif mode.mode_scha_id is not None: element = Schnittstelleattr.getbyid(mode_scha_id)
        elif mode.mode_schn_id is not None: element = Schnittstelle.getbyid(mode_schn_id)
        return element

    @staticmethod
    def insertmode(pentiid=None,pattrid=None,pburuid=None,pwrtbid=None
                    ,prelaid=None,porgeid=None,psynoid=None,ptablid=None
                    ,pschaid=None,pschnid=None):
        mode = Modellelement()
        mode.mode_melt_id = Modellelemtyp.getidbyshortname\
                    (pkurzname=Modellelement.__id2melt(pentiid=pentiid,pattrid=pattrid,pburuid=pburuid,pwrtbid=pwrtbid
                    ,prelaid=prelaid,porgeid=porgeid,psynoid=psynoid,ptablid=ptablid
                    ,pschaid=pschaid,pschnid=pschnid))
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
        mode.mode_uc = '--'
        mode.mode_dc = date.today()
        mode.insert()
        return mode.mode_id
    #insertmodellelement
#Modellelement

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
		  	      REFERENCES modellelemente ( mode_id ) 
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
# ExternalRef

