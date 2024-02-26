from SSOT_db.SQL_INFRA import dbDML
from .modelelement import Modelelemtype,Modelelement
from .attribute import Attribute
from .baseobject import Baseobject
from .datamodel import Datamodel
from .table import Table
from .domain import  Domain


class Column(Baseobject):
    EXTIDUDP: str = 'EXT_ATTR_ID'
    _tablename: str = 'columns'
    _prefix: str = 'colu'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.COLU
    _columnlist = dict()
    _defaultorderby = "colu_column_name"

    def __init__(self, psrcname=None, psrcid=None,**kwargs):
        super().__init__( pscrid=psrcid,
                         psrcname=psrcname,**kwargs)
        self.setdefaultval("colu_read",'TRUE')
        self.setdefaultval("colu_update",'FALSE')
        return


    def getname(self, plang=None):
        return self.colu_column_name

    def getdescr(self, plang=None):
        return self.colu_descr

    def getmodellelement(self):
        return Modelelement.getbyelemid(pschaid=self.colu_id)

    def gettable(self):
        return Table().getbyid(self.colu_tabl_id)

    def gettablname(self):
        return self.gettable().tabl_name

    def getdatm(self):
        return Datamodel().getbyid(self.gettable().tabl_datm_id)

    def getdatmname(self):
        return self.getdatm().datm_name


    def getdatmid(self):
        return self.getdatm().datm_id

    def getwrtb(self):
        return Domain().getbyid(self.colu_doma_id)


    def getdatmid(self):
        tab = Table().getbyid(self.colu_tabl_id)
        return tab.tabl_datm_id



    @classmethod
    def indexlist(cls,pschnid):
        schas = cls.select(
            pwhere=("""colu_tabl_id in (select tabl_id from tables where tabl_datm_id = ?)""", pschnid),
            porderby='colu_column_name')
        indexlist = []
        for s in schas:
            t = Table().getbyid(s.colu_tabl_id)
            indexlist.append(["{} ({})".format(s.colu_column_name, t.tabl_name), 'COL', s.colu_id])
        return indexlist

    # grouplist

    @classmethod
    def selectbyschnid(cls,pschnid):
        return cls.select(pwhere=("""exists (select 1 from tables where
                                     tabl_datm_id = ? 
                                     and tabl_id = colu_tabl_id)""", pschnid))

    @staticmethod
    def mappingto(pschaid):
        lsqle = """select 0 datm_id, 'Logisches Modell' datm_name, group_concat(attr_id,',')
            	from  colu_attr_map as mastermap
    	        left join attributes on attr_id = mastermap.coam_attr_id
    	        where  mastermap.coam_colu_id = {}
    	        GROUP BY mastermap.coam_colu_id""".format(pschaid)
        lsqlt = """select datm_id,datm_name,group_concat(colu_id,',')
    	        from columns subscha
    	        join tables subtab on subtab.tabl_id = subscha.colu_tabl_id
    	        join datamodels on datm_id = subtab.TABL_datm_ID
    	        where subscha.colu_id in
        	          (select attf1.coam_colu_ID
    	               from colu_attr_map attf1
    	                 join colu_attr_map attf2  on attf2.coam_attr_id = attf1.coam_attr_id
    	                                 and attf2.coam_colu_id != attf1.coam_colu_id
    	                  where attf2.coam_colu_id = {}
    	            )
    	            /* eigene Datamodel wird nicht angezeigt*/
    	           and datm_id != (select supertab.tabl_datm_id 
    	                            from columns superattr
    	                            join tables supertab on supertab.tabl_id = superattr.colu_tabl_id 
    	                            where superattr.colu_id = {})
                group by datm_id,datm_name
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

    @classmethod
    def fillextid(cls):
        dbDML.exec("""update {}
                     set colu_ext_system_id = (select UDPV_VALUE
                    from UDP_VALUES 
                    join USER_DEFINED_PROPERTIES on udpr_id = udpv_udpr_id
                        and udpr_name = '{}'
                    where udpv_mode_id = colu_id)""".format(cls._tablename, cls.EXTIDUDP))

