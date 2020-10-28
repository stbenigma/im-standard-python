from IM_DB import dbDML
from .baseobject import Baseobject,Webanker
from datetime import date
from mystring import nvl


class Userdefprop(Baseobject):
    _tablename: str = 'user_defined_properties'
    _prefix: str = 'udpr'
    _columnlist: list = ['udpr_id','udpr_group','udpr_theme','udpr_name','udpr_descr'
                ,'udpr_uc','udpr_dc','udpr_um','udpr_dm']

    def __init__(self,ptheme=None,pgroup=None,pname=None):
        super().__init__(tablename=Userdefprop._tablename, prefix=Userdefprop._prefix
                         , columnlist=Userdefprop._columnlist)
        self.udpr_theme = ptheme
        self.udpr_group = pgroup
        self.udpr_name = pname
        self.udpr_uc = 'SYS'
        self.udpr_dc = date.today()

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Userdefprop._tablename
                               , psql=
        """CREATE TABLE USER_DEFINED_PROPERTIES
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
    )
    """)
    @staticmethod
    def delete():
        Baseobject.delete(Userdefprop._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Userdefprop
                                  , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def getbyname(pname):
        return Userdefprop().getbyuk(pcolname='UDPR_NAME',pukvalue=pname)

    @staticmethod
    def udpAnker(id):
        return Webanker(pname='UDP',pid=id)

    @staticmethod
    def indexlist(pudptheme):
        data = dbDML.select("""select  distinct udpr_group,udpr_theme||'-'||udpr_group id
                         ,udpr_theme
                        from user_defined_properties 
                       where udpr_theme = '{}'
                       union 
                       select '*' grp,'datamapping-alle','{}'
                       where exists (select  1 from
                                user_defined_properties 
                                where udpr_theme = '{}')
                    order by udpr_group""".format(pudptheme
                                                  , pudptheme
                                                  , pudptheme))
        datalist = [(e[0], Userdefprop.udpAnker(e[1]), '', e[2]) for e in data]
        return datalist

    @staticmethod
    def udpnames(pmeltname, ptheme=None, pgroup=None):
        """returns list of udps ("theme", "group", "names,...")"""
        if pgroup is None:
            lsql = """select  udpr_theme,udpr_group,group_concat(udpr_name,',') attrs
                               from modelelem_type
                               join modelemtype_properties on metp_melt_id = melt_id  
                               join user_defined_properties on udpr_id = metp_udpr_id
                               where melt_shortname = '{}'
                            group by udpr_theme,udpr_group
                            order by udpr_theme,udpr_group""".format(pmeltname)
        elif pgroup == '*':
            lsql = """select  udpr_theme,'*'gr,group_concat(udpr_name,',') attrs
                               from modelelem_type
                               join modelemtype_properties on metp_melt_id = melt_id  
                               join user_defined_properties on udpr_id = metp_udpr_id
                               where melt_shortname = '{}'
                               and udpr_theme = {} 
                            group by udpr_theme
                            order by udpr_theme""".format(pmeltname
                                                          , 'udpr_theme' if ptheme is None else "'{}'".format(ptheme))
        else:
            lsql = """select  udpr_theme,udpr_group,group_concat(udpr_name,',') attrs
                       from modelelem_type
                       join modelemtype_properties on metp_melt_id = melt_id  
                       join user_defined_properties on udpr_id = metp_udpr_id
                       where melt_shortname = '{}'
                       and udpr_theme = {} 
                       and udpr_group = '{}' 
                    group by udpr_theme,udpr_group
                    order by udpr_theme,udpr_group""".format(pmeltname
                                                             , 'udpr_theme' if ptheme is None else "'{}'".format(ptheme)
                                                             , pgroup)
        data = dbDML.select(lsql)
        return data
    # udpnames
# Userdefprop


class Userdefpropvalue(Baseobject):
    _tablename: str = 'udp_values'
    _prefix: str = 'udpv'
    _columnlist: list = ['udpv_id', 'udpv_value', 'udpv_mode_id', 'udpv_udpr_id',
                        'udpv_uc', 'udpv_dc', 'udpv_um', 'udpv_dm']

    def __init__(self):
        super().__init__(tablename=Userdefpropvalue._tablename, prefix=Userdefpropvalue._prefix
                         , columnlist=Userdefpropvalue._columnlist)
        self.udpv_uc = 'SYS'
        self.udpv_dc = date.today()

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Userdefpropvalue._tablename
                               , psql="""CREATE TABLE UDP_VALUES
    (
     UDPV_ID INTEGER NOT NULL primary key autoincrement,
     UDPV_VALUE VARCHAR (4000) NULL ,
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
    )"""
    )

    @staticmethod
    def removeemptyUDP(pempties):
        emptylist = ','.join("'{}'".format(e) for e in pempties)
        Userdefpropvalue.delete(pwhere="udpv_value is null or udpv_value  in ({})".format(emptylist)
                   )
    # removeemptydup

    @staticmethod
    def delete(pwhere=None):
        Baseobject.delete(Userdefpropvalue._tablename,pwhere=pwhere)

    @staticmethod
    def select(pwhere=None,porderby=None):
        return Baseobject.select(Userdefpropvalue,pwhere=pwhere,porderby=porderby)

    @staticmethod
    def fillallvalues(pmodetype,pentiid=None,pattrid=None,prelaid=None):
        dbDML.exec("""insert into UDP_VALUES (
                udpv_value,udpv_mode_id,UDPV_UDPR_ID,udpv_uc,udpv_dc)
                select '.',mode_id,METP_UDPR_ID,uc,dc
                from (select enti_id as mode_id,enti_uc as uc, enti_dc as dc
                    from entities
                    where enti_id = {}
                    union all
                    select attr_id as mode_id, attr_uc as uc,attr_dc as dc
                    from attributes
                    where attr_id = {}
                    union all
                    select rela_id as mode_id,rela_uc as uc,rela_dc as dc
                    from RELATIONS
                    where rela_id = {}
                    )
                cross join (select METP_UDPR_ID 
                             from modelelem_type
                             join MODELEMTYPE_PROPERTIES on METP_MELT_ID = melt_id
                             where melt_shortname = '{}')
            """.format(nvl(pentiid,-1),nvl(pattrid,-1),nvl(prelaid,-1),pmodetype))

    @staticmethod
    def updvalues(prows):
        """[(value,modeid,udpid),...]"""
        dbDML.execmany(psql="""update UDP_VALUES
                            set udpv_value = ?
                            where udpv_mode_id = ?
                            and udpv_udpr_id = ?
                        """, recs=prows)
    # updvalues

    def udpvalues(pmeltname, ptheme, pgroup, pmodeid):
        data = dbDML.select("""select udpr_name,udpv_value
                from udp_values
                join user_defined_properties on udpr_id = udpv_udpr_id
                        and udpr_theme = '{}' and udpr_group like '{}'
                where udpv_mode_id = {}
                order by udpr_theme,udpr_group,udpr_name
                """.format(ptheme, '%' if pgroup == '*' else pgroup, pmodeid))
        return data
    # udpvalues

# Userdefpropvalue
