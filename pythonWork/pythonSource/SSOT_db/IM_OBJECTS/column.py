from collections import defaultdict
from SSOT_db.SQL_INFRA import dbDML
from .modelelement import Modelelemtype,Modelelement
from .entity import Entity
from .attribute import Attribute
from .baseobject import Baseobject,Boolean
from .interface import Interface
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

    def __init__(self, psrcname=None, psrcid=None):

        super().__init__( pscrid=psrcid,
                         psrcname=psrcname)


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



    @classmethod
    def indexlist(cls,pschnid):
        schas = cls.select(
            pwhere=("""colu_tabl_id in (select tabl_id from tables where tabl_intf_id = ?)""", pschnid),
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

    @classmethod
    def fillextid(cls):
        dbDML.exec("""update {}
                     set colu_ext_system_id = (select UDPV_VALUE
                    from UDP_VALUES 
                    join USER_DEFINED_PROPERTIES on udpr_id = udpv_udpr_id
                        and udpr_name = '{}'
                    where udpv_mode_id = colu_id)""".format(cls._tablename, cls.EXTIDUDP))


class ColAttrMap(Baseobject):
    INBOUND: str = 'INBOUND'
    OUTBOUND: str = 'OUTBOUND'
    MANUELL: str = 'MANUELL'
    PERIODE: str = 'PERIODE'
    ZPKT: str = 'ZPKT'

    _tablename: str = 'colu_attr_map'
    _prefix: str = 'coam'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []

    def __init__(self, **kwargs):
        super().__init__( **kwargs)
        self.coam_read = Boolean.TRUE
        self.coam_update = Boolean.FALSE

    def secondentiids(self):
        #get all entity-ids of all entites mapped to the table of the currently mapped column
        #  paired with the entity id of the currently mapped attribute
        lsql="""select attr_enti_id,tema_enti_id
            from colu_attr_map
            join columns on colu_id = coam_colu_id
            join attributes on attr_id = coam_attr_id
            join tabl_enti_maps
                on tema_tabl_id = colu_tabl_id and tema_enti_id != attr_enti_id
            where coam_id = ?        
        """
        entitypairs=dbDML.select(lsql,self.getid())
        return entitypairs

    @classmethod
    def getcolulist(cls,pattrid=None,pintfid=None):
        return Column.select(pwhere=("""colu_id in (select coam_colu_id 
                                                    from colu_attr_map
                                                    join columns on colu_id = coam_colu_id
                                                    join tables on tabl_id = colu_tabl_id 
                                                    where coam_attr_id = ?
                                                    and tabl_intf_id = ?)""",
                                     pattrid if pattrid is not None else 'coam_attr_id',
                                     pintfid if pintfid is not None else 'tabl_intf_id'))
    @staticmethod
    def getmappedattrlist(pcoluid):
        """ returns [attr_id,enti_id] for all mappings of this column
           Enti_id is null or the id of a subentity of the attributes-entity"""
        coams =  ColAttrMap.select(pwhere=("""coam_colu_id = ?""",pcoluid))
        defenti = lambda a,e: [a,e] # if we always want the enti_id ... if e is not None else Attribute().getbyid(a).attr_enti_id]
        retval = [defenti(coam.coam_attr_id,coam.coam_enti_id) for coam in coams]
        return retval

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

    @staticmethod
    def setdefaultentity():
        """ sets all coam_enti_id to NULL if they are the same as the entity_id of the coam_attr_id """
        cnt= dbDML.exec("""
        update colu_attr_map
        set coam_enti_id = NULL
        where coam_enti_id is not NULL
        and coam_enti_id = (select attr_enti_id from attributes where attr_id = coam_attr_id)
        """)
        return

    @staticmethod
    def checksuperentitymap():
        """ return list of mappings where  coam_enti_id reference an entity that is a NOT subentity of the
            entity referenced via coam_attr_id
            meaning also that the referenced attribute is NOT inherited by by coam_enti_id which it should be
        """
        retval = []

        sql = """
        with recursive subentitree(superenti_id, subenti_id, level,rootenti_id)
           as
           (select superenti_id
                 , subenti_id
                 ,0 level
                 ,superenti_id rootenti_id
            from superenti
            union all
            select sup2.superenti_id
                 , sup2.subenti_id
                 , subentitree.level+1
                 , subentitree.rootenti_id
            from superenti sup2
                     join subentitree on sup2.superenti_id = subentitree.subenti_id
             where subentitree.level < 99
            ) 
        select coam_colu_id,coam_attr_id,coam_enti_id,
               attrenti.enti_id, attrenti.enti_name attrenti_name,attr_tech_name
               ,subenti.enti_id subenti_id, subenti.enti_name subenti_name
                from colu_attr_map
            join attributes on coam_attr_id = attr_id
            join entities attrenti on attrenti.enti_id = attr_enti_id
              join entities subenti on subenti.enti_id = coam_enti_id
            where coam_enti_id not in (select subenti_id from subentitree
                                    where rootenti_id = attr_enti_id)
    """
        result = dbDML.select(sql)
        """(coam_colu_id,coam_attr_id,coam_enti_id,
               attrenti.enti_id, attrenti_name,attr_tech_name
               ,subenti_id, subenti_name)"""
        for r in result:
            retval.append(f"column {r[0]}, attribute {r[1]},{r[4]}: subentity {r[2]},{r[7]} is not subtype of attribute-entity {r[4]},{r[3]}")
        return retval

    @staticmethod
    def createinheritedmaps():
        """ for all attributes which are inherited by other entities
            check wether in a mapping there exists a entitymapping of the columns table with
            a subentity of the attributes entitiy
            if yes: mark the subentity-mapping in coam_enti_id
            examples
            tab1.col1 mapped to enti1.attr1
            tab1 is mapped to enti2
            enti2 is a subentity of enti1 (inherits all attributes)
            in the originial mapping enti2-id is entered in coam_enti_id
            if several subentities are found take any of them and ignore the rest
        """
        for coam in ColAttrMap.select():
            attr=Attribute().getbyid(coam.coam_attr_id)
            secondentis = coam.secondentiids()
            if len(secondentis) >0:
                # if the second entity is a subentity of the first (the acutal attributmappingentity), enter it as secondary
                enti= Entity().getbyid(secondentis[0][0]) #the first entry is identical
                subenties=enti.getsubentities()
                subentiids=enti.getsubentityids()
                for secondenti in secondentis:
                    if secondenti[1] in subentiids:
                        coam.coam_enti_id = secondenti[1]
                        coam.updatedb()
                        break # we take the first one
        return
