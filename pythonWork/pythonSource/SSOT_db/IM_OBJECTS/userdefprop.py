from datetime import date

from SSOT_db import IM_OBJECTS
from SSOT_db.SQL_INFRA import dbDML
from .baseobject import Baseobject
from .modelelement import Modelelemtype


class Userdefprop(Baseobject):
    _tablename: str = 'user_defined_properties'
    _prefix: str = 'udpr'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []

    def __init__(self, ptheme=None, pgroup=None, pname=None):

        super().__init__()
        self.udpr_theme = ptheme
        self.udpr_group = pgroup
        self.udpr_name = pname
        self.udpr_uc = 'sys'
        self.udpr_dc = date.today()

    def getname(self, plang=None):
        return self.udpr_name

    def getdescr(self, plang=None):
        return self.udpr_descr

    def getqualifiedname(self, plang=None):
        return "{} ({})".format(self.getname(plang=plang), self.udpr_group)

    @classmethod
    def getbyname(cls, pname):
        return cls.getbyuk(UDPR_NAME=pname)

    @staticmethod
    def themelist(pmelttype=None):
        """[(theme)] """
        data = dbDML.select("""select  distinct udpr_theme
                        from user_defined_properties 
                        join MODELEMTYPE_PROPERTIES on metp_udpr_id = udpr_id
                        join MODELELEM_TYPE on melt_id = metp_melt_id  
                       where melt_shortname like '{}'
                    order by udpr_theme""".format('%' if pmelttype is None else pmelttype))
        return data

    @staticmethod
    def grouplist(pudptheme=None, pmelttype=None):
        """[(theme,group)] """
        data = dbDML.select("""select  distinct udpr_theme,udpr_group
                        from user_defined_properties 
                        join MODELEMTYPE_PROPERTIES on metp_udpr_id = udpr_id
                        join MODELELEM_TYPE on melt_id = metp_melt_id  
                       where udpr_theme like '{}' and melt_shortname like '{}'
                    order by udpr_theme,udpr_group""".format('%' if pudptheme is None else pudptheme,
                                                             '%' if pmelttype is None else pmelttype))
        return data

    @staticmethod
    def getudps(pmeltname=None, ptheme=None, pgroup=None):
        return Userdefprop.select(pwhere=("""udpr_theme like ?
                                        and udpr_group like ?
                                        and udpr_id in (select metp_udpr_id
                                                        from modelemtype_properties
                                                        join modelelem_type on melt_id = metp_melt_id
                                                        where melt_shortname like ?)""",
                                          '%' if ptheme is None else ptheme,
                                          '%' if pgroup is None else pgroup,
                                          '%' if pmeltname is None else pmeltname),
                                  porderby="udpr_theme,udpr_group,udpr_name"
                                  )

    @staticmethod
    def removemodelUDP(modeludps):
        """remove all UDP's which are used as model elements (translation, elementdisplay etc.
            modelupds= [(udpr_theme : udpr_name),]"""
        # lsql= """delete from USER_DEFINED_PROPERTIES
        #             where lower(UDPR_THEME) = lower(?) and lower(udpr_name) = lower(?)"""
        # dbDML.execmany(psql=lsql,recs=modeludps)

        lsql = """delete from USER_DEFINED_PROPERTIES 
                    where (lower(UDPR_THEME),lower(udpr_name)) = (lower(?) ,lower(?))"""
        try:
            dbDML.execmany(psql=lsql, recs=modeludps)
        except Exception as e:
            print(lsql)
            print(modeludps)
            print(e)
        return


# Userdefprop


class Userdefpropvalue(Baseobject):
    _tablename: str = 'udp_values'
    _prefix: str = 'udpv'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []

    def __init__(self, pmodeid=None, pudprid=None, pvalue=None):

        super().__init__()
        self.udpv_value = pvalue
        self.udpv_mode_id = pmodeid
        self.udpv_udpr_id = pudprid

    @staticmethod
    def removeemptyUDP(pempties):
        Userdefpropvalue.delete(
            pwhere=("udpv_value is null or udpv_value in ({})".format(','.join('?'.rjust( len(pempties),'?'))), *pempties))
        return

    @staticmethod
    def fillallvalues(pentiid=None, pattrid=None, prelaid=None, ptablid=None, pcoluid=None):
        def fillvalues(pid, ptablename, pprefix):
            sql = f"""insert into UDP_VALUES (
                    udpv_value,udpv_mode_id,UDPV_UDPR_ID,udpv_uc,udpv_dc)
                    select UDPR_DEFAULTVALUE,{pprefix}_id as mode_id,UDPR_ID
                            ,{pprefix}_uc as uc, {pprefix}_dc as dc
                      from {ptablename}
                     cross join (select UDPR_ID,UDPR_DEFAULTVALUE
                                 from modelelem_type
                                 join MODELEMTYPE_PROPERTIES on METP_MELT_ID = melt_id
                                 join USER_DEFINED_PROPERTIES on UDPR_ID = METP_UDPR_ID
                                 where melt_shortname = '{pprefix}')
                    where {pprefix}_id = ?
                    """
            dbDML.exec(sql, pid)
            return

        if pentiid is not None:
            fillvalues(pid=pentiid, ptablename=IM_OBJECTS.Entity._tablename, pprefix=Modelelemtype.ENTI)
        elif pattrid is not None:
            fillvalues(pid=pattrid, ptablename=IM_OBJECTS.Attribute._tablename, pprefix=Modelelemtype.ATTR)
        elif prelaid is not None:
            fillvalues(pid=prelaid, ptablename=IM_OBJECTS.Relation._tablename, pprefix=Modelelemtype.RELA)
        elif ptablid is not None:
            fillvalues(pid=ptablid, ptablename=IM_OBJECTS.Table._tablename, pprefix=Modelelemtype.TABL)
        elif pcoluid is not None:
            fillvalues(pid=pcoluid, ptablename=IM_OBJECTS.Column._tablename, pprefix=Modelelemtype.COLU)
        else:
            pass
        return

    @staticmethod
    def updvalues(prows):
        """[(value,modeid,udpid),...]"""
        dbDML.execmany(psql="""update UDP_VALUES
                            set udpv_value = ?
                            where udpv_mode_id = ?
                            and udpv_udpr_id = ?
                        """, recs=prows)
        return

    @staticmethod
    def udpvalue(pudprid, pmodeid):
        udpv = Userdefpropvalue.select(pwhere=("udpv_udpr_id = ? and udpv_mode_id= ?", pudprid, pmodeid))
        if udpv is None or len(udpv) == 0: return None
        return udpv[0].udpv_value

    @staticmethod
    def udpvalues(ptheme, pgroup, pmodeid, pmeltype):
        """[(udpr_name,udpv_value)]"""
        data = dbDML.select("""select udpr_name, case when udpv_value is NULL then '' else udpv_value end val 
                from user_defined_properties 
                join MODELEMTYPE_PROPERTIES on METP_UDPR_ID = UDPR_ID
                join modelelem_type on melt_id = metp_melt_id
                 left join udp_values on udpv_udpr_id = udpr_id 
                     and udpv_mode_id = ?
                where udpr_theme = ? and udpr_group like ?
                  and MELT_SHORTNAME = ?  
                order by udpr_theme,udpr_group,udpr_name
                """, pmodeid, ptheme, '%' if pgroup == '*' else pgroup, pmeltype)
        return data

