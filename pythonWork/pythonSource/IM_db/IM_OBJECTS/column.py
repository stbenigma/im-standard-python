from collections import defaultdict
from IM_DB import dbDML
from .attribute import Attribute
from .baseobject import Baseobject
from .datatype import Datatype
from .interface import Interface
from .table import Table
from .domain import  Domain
from .modelelement import Modelelemtype


class Column(Baseobject):
    EXTIDUDP: str = 'EXT_ATTR_ID'
    _tablename: str = 'columns'
    _prefix: str = 'colu'
    _columnlist = []

    def __init__(self, psrcname=None, psrcid=None):
        if (len(Column._columnlist) == 0): Column._columnlist = Baseobject.gettablecolumns(Column._tablename)
        super().__init__(tablename=Column._tablename, prefix=Column._prefix
                         , pmodelemtype=Modelelemtype.COLU
                         , pscrid=psrcid
                         , psrcname=psrcname)


    def getname(self, plang=None):
        return self.colu_column_name

    def getdescr(self, plang=None):
        return self.colu_descr

    def getmodellelement(self):
        return Modellelement.getbyelemid(pschaid=self.colu_id)

    def gettable(self):
        return Table().getbyid(self.colu_tabl_id)

    def gettablname(self):
        return self.gettable().tabl_name

    def getintf(self):
        return Interface().getbyid(self.gettable().tabl_intf_id)

    def getintfname(self):
        return self.getintf().intf_name


    def getintfid(self):
        return self.getintf().intf_id

    def getwrtb(self):
        if (self.colu_doma_id is None): return None
        return Domain().getbyid(self.colu_doma_id)


    def getintfid(self):
        tab = Table().getbyid(self.colu_tabl_id)
        return tab.tabl_intf_id

    @staticmethod
    def delete(pwhere=None):
        return Baseobject.delete(Column._tablename)

    @staticmethod
    def select(pwhere=None, porderby="colu_column_name"):
        return Baseobject.select(pclass=Column
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def indexlist(pschnid):
        schas = Column.select(
            pwhere=("""colu_tabl_id in (select tabl_id from tables where tabl_intf_id = ?)""", pschnid)
            , porderby='colu_column_name')
        indexlist = []
        for s in schas:
            t = Table().getbyid(s.colu_tabl_id)
            indexlist.append(["{} ({})".format(s.colu_column_name, t.tabl_name), 'COL', s.colu_id])
        return indexlist

    # grouplist

    @staticmethod
    def selectbyschnid(pschnid):
        return Column.select(pwhere=("""exists (select 1 from tables where
                                     tabl_intf_id = ? 
                                     and tabl_id = colu_tabl_id)""", pschnid))

    @staticmethod
    def mappingto(pschaid):
        lsqle = """select 0 intf_id, 'Logisches Modell' intf_name, group_concat(attr_id,',')
            	from  colu_attr_map as mastermap
    	        left join attributes on attr_id = mastermap.coam_attr_id
    	        where  mastermap.coam_colu_id = {}
    	        GROUP BY mastermap.coam_colu_id""".format(pschaid)
        lsqlt = """select intf_id,intf_name,group_concat(colu_id,',')
    	        from columns subscha
    	        join tables subtab on subtab.tabl_id = subscha.colu_tabl_id
    	        join interfaces on intf_id = subtab.TABL_intf_ID
    	        where subscha.colu_id in
        	          (select attf1.coam_colu_ID
    	               from colu_attr_map attf1
    	                 join colu_attr_map attf2  on attf2.coam_attr_id = attf1.coam_attr_id
    	                                 and attf2.coam_colu_id != attf1.coam_colu_id
    	                  where attf2.coam_colu_id = {}
    	            )
    	            /* eigene Interface wird nicht angezeigt*/
    	           and intf_id != (select supertab.tabl_intf_id 
    	                            from columns superattr
    	                            join tables supertab on supertab.tabl_id = superattr.colu_tabl_id 
    	                            where superattr.colu_id = {})
                group by intf_id,intf_name
                """.format(pschaid, pschaid)
        retval = []
        data = dbDML.select(lsqle)
        """[(0,'logisches Modell', [Attribute]')]"""
        for d in data:
            if (d[2] is not None):
                retval.append([d[0], d[1], [Attribute().getbyid(e) for e in d[2].split(',')]])

        data = dbDML.select(lsqlt)
        """[ (schnid,schnname, [Column])]"""
        for d in data:
            if (d[2] is not None):
                retval.append([d[0], d[1], [Column().getbyid(e) for e in d[2].split(',')]])
        return retval

    # maopingto

    @staticmethod
    def fillextid():
        dbDML.exec("""update {}
                     set colu_ext_system_id = (select UDPV_VALUE
                    from UDP_VALUES 
                    join USER_DEFINED_PROPERTIES on udpr_id = udpv_udpr_id
                        and udpr_name = '{}'
                    where udpv_mode_id = colu_id)""".format(Column._tablename, Column.EXTIDUDP))


# Column

class ColAttrMap(Baseobject):
    INBOUND: str = 'INBOUND'
    OUTBOUND: str = 'OUTBOUND'
    MANUELL: str = 'MANUELL'
    PERIODE: str = 'PERIODE'
    ZPKT: str = 'ZPKT'

    _tablename: str = 'colu_attr_map'
    _prefix: str = 'coam'
    _columnlist: list = []

    def __init__(self):
        if (len(ColAttrMap._columnlist) == 0): ColAttrMap._columnlist = Baseobject.gettablecolumns(ColAttrMap._tablename)
        super().__init__(tablename=ColAttrMap._tablename, prefix=ColAttrMap._prefix)

    @staticmethod
    def getcolulist(pattrid=None,pintfid=None):
        return Column.select(pwhere=("""colu_id in (select coam_colu_id 
                                                    from colu_attr_map
                                                    join columns on colu_id = coam_colu_id
                                                    join tables on tabl_id = colu_tabl_id 
                                                    where coam_attr_id = ?
                                                    and tabl_intf_id = ?)""",
                                     pattrid if pattrid is not None else 'coam_attr_id',
                                     pintfid if pintfid is not None else 'tabl_intf_id'))
    @staticmethod
    def getattrlist(pcoluid=None):
        return Attribute.select(pwhere=("""attr_id in (select coam_attr_id 
                                                    from colu_attr_map
                                                    where coam_colu_id = ?
                                                    )""", pcoluid))


    @staticmethod
    def delete(pwhere=None):
        return Baseobject.delete(ColAttrMap._tablename,pwhere=pwhere)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=ColAttrMap
                                 , pwhere=pwhere, porderby=porderby)


    @staticmethod
    def columnlist(pattrid=None):
        data = dbDML.select("""select  intf_name,intf_id,group_concat(colu_id,',') schaids
                            from colu_attr_map
                            join columns on colu_id = coam_colu_id
                            join tables on tabl_id = colu_tabl_id
                            join interfaces on intf_id = tabl_intf_id 
                            where coam_ATTR_ID = {}
                            group by intf_name,intf_id
                            order by intf_name
                            """.format(pattrid))
        retval = []
        try:
            for d in data:
                intf_name, intf_id = d[0], d[1]
                collist = {}
                for coluid in d[2].split(','):
                    colu = Column().getbyid(coluid)
                    tabname = Table().getbyid(colu.colu_tabl_id).tabl_name
                    collist[tabname + '.' + colu.colu_column_name] = Modelelemtype.INTF
                # for
                retval.append([intf_name, collist])
            # for
        except  Exception as e:
            print(str(e))
            pass
        # try
        return retval
    # columnlist

    @staticmethod
    def colattrmap():
        data = dbDML.select("""select coam_colu_id,coam_attr_id
                                from colu_attr_map
                            """)
        retval = defaultdict(dict)
        for d in data:
            retval[d[0]][d[1]] = True
        # for
        return retval
    # colattrmap
# ColAttrMap
