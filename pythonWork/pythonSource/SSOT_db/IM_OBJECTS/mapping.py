import logging
from collections import defaultdict

from SSOT_db.SQL_INFRA import dbDML
from .attribute import Attribute
from .baseobject import Baseobject, Boolean
from .column import Column
from .entity import Entity
from .modelelement import Modelelemtype
from .relationship import Relation
from .table import Table


class Mapping(Baseobject):
    MAPTYPE_DATM_IM = 'DATM-IM'
    MAPTYPE_DATM_DATM = 'DATM-DATM'
    MAPTYPE_DOMA_DOMA = 'DOMA-DOMA'
    MAPTYPE_DATM_SYST = 'DATM-SYST'

    _tablename: str = 'mappings'
    _prefix: str = 'maps'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.MAPS
    _columnlist = dict()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        return

    @classmethod
    def selectorcreate(cls, maptype, name,
                       modeid1, modeid2=None,
                       descr=None,
                       rulefw=None, rulebw=None):
        """ reads mapping with key (maptype,modeid1,modeid2)
            if not found, creates a mapping with this information

            returns the found or created mapping
        """
        mappings = Mapping.select(pwhere=
                                  ("""maps_type = ? and maps_mode_id1 = ?
                                      and coalesce(maps_mode_id2,-1)  = coalesce(?,-1)"""
                                   , maptype, modeid1, modeid2
                                   )
                                  )
        if len(mappings) == 0:
            mapping = Mapping(maps_name=name,
                              maps_type=maptype,
                              maps_mode_id1=modeid1,
                              maps_mode_id2=modeid2,  # Mapping to IM has no id2
                              maps_descr=descr,
                              maps_rule_frwd=rulefw,
                              maps_rule_bckw=rulebw
                              )
            mapping.insert()
        else:
            mapping = mappings[0]
        return mapping


class ModeMap(Baseobject):
    _tablename: str = 'mode_mode_maps'
    _prefix: str = 'momo'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def getentilist(tablid):
        """get list of entities, mapped to the given table"""
        return Entity.select(pwhere=("""enti_id in (select momo_mode_id2 
                                                    from mode_mode_maps
                                                    where momo_mode_id1 = ?
                                                    )""", tablid)
                             )

    @staticmethod
    def getrelaidlist(modeid):
        """get list of relations, mapped to the given table"""
        relaids=dbDML.select("""select momo_mode_id2 elemid
                               ,momo_sub_enti_id subentiid 
                              from mode_mode_maps
                              where momo_mode_id2 in (select rela_id from relations) 
                                and momo_mode_id1 = ?""",modeid)
        return relaids

    @staticmethod
    def gettabllist(tablid):
        """get list of tables, mapped to the given table"""
        return Table.select(pwhere=("""tabl_id in (select momo_mode_id2 
                                                    from mode_mode_maps
                                                    where momo_mode_id1 = ?
                                                    )""", tablid)
                            )

    @staticmethod
    def getattridlist(coluid):
        """get list of Attributes, mapped to the given column"""
        attrids=dbDML.select("""select momo_mode_id2 elemid
                               ,momo_sub_enti_id subentiid 
                              from mode_mode_maps
                             where momo_mode_id2 in (select attr_id from attributes) 
                             and momo_mode_id1 = ?""",coluid)
        return attrids

    @staticmethod
    def getcolulist(coluid):
        """get list of Columns, mapped to the given column"""
        return Column.select(pwhere=("""colu_id in (select momo_mode_id2 
                                                    from mode_mode_maps
                                                    where momo_mode_id1 = ?
                                                    )""", coluid)
                             )



class TablEntiMap(Baseobject):
    """ is now a view so do not apply Baseobject rules"""

    _tablename: str = 'tabl_enti_maps'
    _prefix: str = 'tema'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []

    def __init__(self):
        super().__init__()

    def insert(self, pdoerrhdlng=True):
        #logging.warning(f"TablEntiMap.insert should be replaced by ModeMap-method")
        # if mapping does not exists, create one
        tabl = Table().getbyid(self.tema_tabl_id)
        mapping = Mapping.selectorcreate(maptype=Mapping.MAPTYPE_DATM_IM,
                                         name=str(tabl.tabl_datm_id) + "-" + tabl.tabl_name,
                                         modeid1=tabl.tabl_id,
                                         modeid2=None)

        momo = ModeMap(momo_maps_id=mapping.maps_id,
                       momo_mode_id1=self.tema_tabl_id,
                       momo_mode_id2=self.tema_enti_id if self.tema_enti_id is not None \
                           else self.tema_rela_id,
                       momo_sub_enti_id=None,
                       momo_onedirection=Boolean.TRUE,
                       momo_uc=self.tema_uc, momo_dc=self.tema_dc,
                       momo_um=self.tema_um, momo_dm=self.tema_dm,
                       momo_descr=self.tema_descr,
                       momo_rule_frwd=self.tema_transf_rule_frwd,
                       momo_rule_bckw=self.tema_transf_rule_bckw
                       )
        momo.insert()
        return

    def update(self, pdoerrhdlng=True):
        assert False, "update has to be redirected to mode_mode_maps"

    @staticmethod
    def __combiwhere(pentiid=None, prelaid=None, pdatmid=None):
        return """ case when tema_enti_id is NULL 
                            then ' ' 
                            else tema_enti_id end  like '{}'
                      and case when tema_rela_id is NULL 
                            then ' ' 
                            else tema_rela_id end   like '{}'
                      and case when tabl_datm_id is NULL 
                            then ' ' 
                            else tabl_datm_id end like '{}'""".format(str(pentiid) if pentiid is not None else '%',
                                                                      str(prelaid) if prelaid is not None else '%',
                                                                      str(pdatmid) if pdatmid is not None else '%')

    @staticmethod
    def gettabllist(pentiid=None, prelaid=None, pdatmid=None):
        where = """tabl_id in (select tema_tabl_id 
                                from tabl_enti_maps
                                join tables on tabl_id = tema_tabl_id 
                                where {})""".format(
            TablEntiMap.__combiwhere(pentiid=pentiid, prelaid=prelaid, pdatmid=pdatmid))
        tabls = Table.select(pwhere=(where), porderby="tabl_id")
        return tabls

    @staticmethod
    def getentilist(ptablid):
        return Entity.select(pwhere=("""enti_id in (select tema_enti_id 
                                                    from tabl_enti_maps
                                                    where tema_tabl_id = ?
                                                    )""", ptablid)
                             )

    @staticmethod
    def getrelalist(ptablid):
        return Relation.select(pwhere=("""rela_id in (select tema_rela_id 
                                                    from tabl_enti_maps
                                                    where tema_tabl_id = ?
                                                    )""", ptablid)
                               )

    @staticmethod
    def gettablentimap(directonly, datmid=None):
        return


class ColAttrMap(Baseobject):
    """ is now a view so do not apply all Baseobject rules"""
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
        super().__init__(**kwargs)
        self.coam_read = Boolean.TRUE
        self.coam_update = Boolean.FALSE
        return

    def secondentiids(self):
        # get all entity-ids of all entites mapped to the table of the currently mapped column
        #  paired with the entity id of the currently mapped attribute
        lsql = """select attr_enti_id,tema_enti_id
            from colu_attr_map
            join attributes on attr_id = coam_attr_id
            join columns on colu_id = coam_colu_id
            join tabl_enti_maps
                on tema_tabl_id = colu_tabl_id and tema_enti_id != attr_enti_id
            where coam_id = ?        
        """
        entitypairs = dbDML.select(lsql, self.getid())
        return entitypairs

    def insert(self, pdoerrhdlng=True):
        #logging.warning(f"ColAttrMap.insert should be replaced by ModeMap-method")
        # if mapping does not exists, create one
        colu = Column().getbyid(self.coam_colu_id)
        tabl = Table().getbyid(colu.colu_tabl_id)
        mapping = Mapping.selectorcreate(maptype=Mapping.MAPTYPE_DATM_IM,
                                         name=str(tabl.tabl_datm_id) + "-" + tabl.tabl_name,
                                         modeid1=tabl.tabl_id,
                                         modeid2=None)  # IM has no ID

        momo = ModeMap(momo_maps_id=mapping.maps_id,
                       momo_mode_id1=self.coam_colu_id,
                       momo_mode_id2=self.coam_attr_id,
                       momo_sub_enti_id=self.coam_enti_id,
                       momo_onedirection=Boolean.TRUE,
                       momo_uc=self.coam_uc, momo_dc=self.coam_dc,
                       momo_um=self.coam_um, momo_dm=self.coam_dm,
                       momo_descr=self.coam_descr,
                       momo_rule_frwd=self.coam_transf_rule,
                       momo_rule_bckw=self.coam_transf_rule_bckw
                       )
        momo.insert()

    def update(self, pdoerrhdlng=True):
        assert False, "update has to be redirected to mode_mode_maps"

    def updatedb(self, pdoerrhdlng=True):
        assert False, "updatedb has to be redirected to mode_mode_maps"

    @classmethod
    def getcolulist(cls, pattrid=None, pdatmid=None):
        return Column.select(pwhere=("""colu_id in (select coam_colu_id 
                                                    from colu_attr_map
                                                    join columns on colu_id = coam_colu_id
                                                    join tables on tabl_id = colu_tabl_id 
                                                    where coam_attr_id = ?
                                                    and tabl_datm_id = ?)""",
                                     pattrid if pattrid is not None else 'coam_attr_id',
                                     pdatmid if pdatmid is not None else 'tabl_datm_id'))

    @staticmethod
    def getmappedattrlist(pcoluid):
        """ returns [attr_id,enti_id] for all mappings of this column
           Enti_id is null or the id of a subentity of the attributes-entity"""
        coams = ColAttrMap.select(pwhere=("""coam_colu_id = ?""", pcoluid))
        defenti = lambda a, e: [a,
                                e]  # if we always want the enti_id ... if e is not None else Attribute().getbyid(a).attr_enti_id]
        retval = [defenti(coam.coam_attr_id, coam.coam_enti_id) for coam in coams]
        return retval

    @staticmethod
    def columnlist(pattrid=None):
        data = dbDML.select("""select  datm_name,datm_id,group_concat(colu_id,',') schaids
                            from colu_attr_map
                            join columns on colu_id = coam_colu_id
                            join tables on tabl_id = colu_tabl_id
                            join datamodels on datm_id = tabl_datm_id 
                            where coam_ATTR_ID = {}
                            group by datm_name,datm_id
                            order by datm_name
                            """.format(pattrid))
        retval = []
        try:
            for d in data:
                datm_name, datm_id = d[0], d[1]
                collist = {}
                for coluid in d[2].split(','):
                    colu = Column().getbyid(coluid)
                    tabname = Table().getbyid(colu.colu_tabl_id).tabl_name
                    collist[tabname + '.' + colu.colu_column_name] = Modelelemtype.DATM
                # for
                retval.append([datm_name, collist])
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
        """ sets all sub_enti_id's to NULL if they are the same as the entity_id of the attribute
            this only applies if something is mapped to attributes. Attr_id is always momo_mode_id2
        """
        cnt = dbDML.exec("""
            update mode_mode_maps
            set momo_sub_enti_id = NULL
            where momo_sub_enti_id is not NULL
            and momo_sub_enti_id = (select attr_enti_id from attributes where attr_id = momo_mode_id2)        
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
            retval.append(
                f"column {r[0]}, attribute {r[1]},{r[4]}: subentity {r[2]},{r[7]} is not subtype of attribute-entity {r[4]},{r[3]}")
        return retval

    @staticmethod
    def createinheritedmaps():
        """ for all attributes which are inherited by other entities
            check wether in a mapping there exists an entitymapping of the columns table to
            a subentity of the attributes entitiy
            if yes: mark the subentity-mapping in momo_sub_enti_id
            examples
            tab1.col1 mapped to enti1.attr1
            tab1 is mapped to enti2
            enti2 is a subentity of enti1 (inherits all attributes)
            in the originial mapping enti2-id is entered in momo_sub_enti_id
            if several subentities are found take any of them and ignore the rest
        """
        for coam in ColAttrMap.select():
            attr = Attribute().getbyid(coam.coam_attr_id)
            secondentis = coam.secondentiids()
            if len(secondentis) > 0:
                # if the second entity is a subentity of the first (the acutal attributmappingentity),
                # enter it as secondary
                enti = Entity().getbyid(secondentis[0][0])  # the first entry is identical
                # why would I need it?? subenties=enti.getsubentities()
                subentiids = enti.getsubentityids()
                for secondenti in secondentis:
                    if secondenti[1] in subentiids:
                        momo = ModeMap().getbyid(coam.coam_id)
                        momo.momo_sub_enti_id = secondenti[1]
                        momo.updatedb()
                        break  # we take the first one
        return
