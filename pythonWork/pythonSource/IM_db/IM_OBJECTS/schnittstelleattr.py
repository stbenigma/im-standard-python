from .baseobject import Baseobject
import IM_OBJECTS

class Schnittstelleattr(Baseobject):

    _tablename:str = 'schnittstelle_attrs'
    _prefix:str = 'scha'
    _columnlist:list = ['scha_id', 'scha_column_name', 'scha_format', 'scha_fremdsystem_id'
                                       ,'scha_beschr', 'scha_type_string', 'scha_tabl_id', 'scha_daty_id'
                                    , 'scha_wrtb_id','scha_odm_guid'
                                       ,'scha_uc', 'scha_dc', 'scha_um', 'scha_dm']

    def __init__(self):
        super().__init__(tablename=Schnittstelleattr._tablename, prefix=Schnittstelleattr._prefix
                        ,columnlist = Schnittstelleattr._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Schnittstelleattr._tablename
                               , psql="""
    create table schnittstelle_attrs
    (
        scha_id             integer
            primary key autoincrement,
        scha_column_name    varchar(60) not null,
        scha_format         varchar(200),
        scha_fremdsystem_id varchar(100),
        scha_beschr         varchar(4000),
        scha_type_string    varchar(200),
        scha_tabl_id        integer     not null,
        scha_daty_id        integer     not null,
        scha_wrtb_id        integer ,
        scha_odm_guid       varchar(36),
        scha_uc             varchar(30) not null,
        scha_dc             varchar(30) not null,
        scha_um             varchar(30),
        scha_dm             varchar(30),
        constraint scha_daty_fk FOREIGN KEY (scha_daty_id) references datatypes (daty_id),
        constraint scha_wrtb_fk FOREIGN KEY (scha_wrtb_id) references wertebereiche (wrtb_id),
        constraint scha_tabl_fk FOREIGN KEY (scha_tabl_id) references tabellen(tabl_id),
        constraint scha_uk unique (scha_tabl_id,scha_column_name)        
        )
        """)

    def webanker(self,pmodelid):
        return super().webanker(pmodelid)

    def getmodellelement(self):
        return Modellelement.getbyelemid(pschaid=self.scha_id)

    @staticmethod
    def delete():
        Baseobject.delete(Schnittstelleattr._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Schnittstelleattr
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def columnlist(ptablid):
        return Schnittstelleattr.select(pwhere='scha_tabl_id = {}'.format(ptablid),porderby='scha_column_name')

    @staticmethod
    def indexlist(pschnid):
        schas = Schnittstelleattr.select(pwhere= """scha_tabl_id in (select tabl_id from tabellen where tabl_schn_id={})""".format(pschnid)
                                        ,porderby='scha_column_name')
        indexlist = []
        for s in schas:
            t = IM_OBJECTS.tabelle.Tabelle().getbyid(s.scha_tabl_id)
            indexlist.append(["{} ({})".format(s.scha_column_name,t.tabl_name),  s.webanker(t.tabl_schn_id), s.scha_id])
        return indexlist
    #indexlist
#Schnittstelleattr

class Attrtransf(Baseobject):
    INBOUND:str = 'INBOUND'
    OUTBOUND:str = 'OUTBOUND'
    MANUELL:str = 'MANUELL'
    PERIODE:str = 'PERIODE'
    ZPKT:str = 'ZPKT'

    _tablename: str = 'attr_transf'
    _prefix: str = 'attf'
    _columnlist: list = ['attf_id' ,'attf_laufnr'  ,'attf_richtung'
                        ,'attf_transf_formel'   ,'attf_ausloeseart' ,'attf_ausloeseperiod'
                        ,'attf_scha_id' ,'attf_attr_id' ,'attf_uc'
                        ,'attf_dc'  ,'attf_um'  ,'attf_dm']

    def __init__(self):
        super().__init__(tablename=Attrtransf._tablename, prefix=Attrtransf._prefix
                     , columnlist=Attrtransf._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Attrtransf._tablename
                           , psql="""
                            create table attr_transf 
         (
       attf_id integer primary key autoincrement,
       attf_laufnr integer  not null check ( attf_laufnr > 0) , 
       attf_richtung varchar (7) not null check ( attf_richtung in ('INBOUND', 'OUTBOUND') ) , 
       attf_transf_formel varchar (4000) null , 
       attf_ausloeseart varchar (10) null check ( attf_ausloeseart in ('MANUELL', 'PERIODE', 'ZPKT') ) , 
       attf_ausloeseperiod integer null , 
       attf_scha_id integer null , 
       attf_attr_id integer null , 
       attf_uc varchar (30)  , 
       attf_dc varchar (30)  , 
       attf_um varchar (30) null , 
       attf_dm varchar (30)  null  
		,constraint attf_un unique (attf_richtung , attf_scha_id , attf_attr_id, attf_laufnr )
 	   ,constraint attf_attr_fk foreign key (attf_attr_id) 
 	      references attributes (attr_id )  on delete cascade 
 	   ,constraint attf_scha_fk foreign key (attf_scha_id) 
 	      references schnittstelle_attr (scha_id ) on delete cascade 
 	      )
    """)

    @staticmethod
    def delete():
        Baseobject.delete(Attrtransf._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Attrtransf
                                    , pwhere=pwhere, porderby=porderby)
    @staticmethod
    def columnlist(pattrid):
        data = dbDML.select("""select  schn_name,group_concat(attr_id,',') tabids
                            from attr_transf 
                            join attributes OM ATTR_ID = ATTF_ATTR_ID
                            join tabellen on tabl_id = ATTF_ATTR_ID
                            join schnittstellen on schn_id = tabl_schn_id 
                            where attf_attr_id = {}
                            group by schn_name
                            order by schn_name
                            """.format(pattrid))
        retval = []
        try:
            for d in data:
                tablist = {}
                schn_name = d[0]
                collist = {}
                for colid in d[1].split(','):
                    #collist[] = Attrtransf().getbyid(colid)
                    collist[col.att_name] = tab.webanker()
                # for
                retval.append([schn_name, colist])
            # for
        except:
            pass
        # try
        return retval
# tablelist
#Attrtransf



