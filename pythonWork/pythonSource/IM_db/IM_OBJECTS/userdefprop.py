from IM_DB import dbDML
from .baseobject import Baseobject
from datetime import date


class Userdefprop(Baseobject):
    _tablename: str = 'user_defined_properties'
    _prefix: str = 'udpr'
    _columnlist: list = ['udpr_id','udpr_group','udpr_name','udpr_descr' 
                ,'udpr_uc','udpr_dc','udpr_um','udpr_dm']

    def __init__(self):
        super().__init__(tablename=Userdefprop._tablename, prefix=Userdefprop._prefix
                         , columnlist=Userdefprop._columnlist)
        self.udpr_uc = 'SYS'
        self.udpr_dc = date.today()

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Userdefprop._tablename
                               , psql=
        """CREATE TABLE USER_DEFINED_PROPERTIES
    (
     UDPR_ID INTEGER NOT NULL primary key autoincrement ,
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
     UDPV_VALUE VARCHAR (4000) NOT NULL ,
     UDPV_MODE_ID NUMERIC (10) NOT NULL ,
     UDPV_UDPR_ID NUMERIC (10) NOT NULL ,
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
        dbDML.exec("""delete from {} 
                        where udpv_value is null
                            or udpv_value  in ({})""".format(Userdefpropvalue._tablename, emptylist)
                   )

    # removeemptydup
    @staticmethod
    def delete():
        Baseobject.delete(Userdefpropvalue._tablename)

    @staticmethod
    def fillallvalues(pmodetype,pentiid):
        dbDML.exec("""insert into UDP_VALUES (
                udpv_value,udpv_mode_id,UDPV_UDPR_ID,udpv_uc,udpv_dc)
                select '.',enti_id,METP_UDPR_ID,enti_uc,enti_dc
                from entitaeten
                cross join (select METP_UDPR_ID 
                             from modelelem_type
                             join MODELEMTYPE_PROPERTIES on METP_MELT_ID = melt_id
                             where melt_shortname = '{}')
                where enti_id = {}
            """.format(pmodetype,pentiid))

    @staticmethod
    def updvalues(prows):
        """[(value,modeid,udpid),...]"""
        print (prows)
        dbDML.execmany(psql="""update UDP_VALUES
                            set udpv_value = ?
                            where udpv_mode_id = ?
                            and udpv_udpr_id = ?
                        """, recs=prows)
    # updvalues
# Userdefpropvalue
