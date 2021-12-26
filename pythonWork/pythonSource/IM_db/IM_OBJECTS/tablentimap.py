from collections import defaultdict

from IM_db.IM_DB import  dbDML
from .baseobject import Baseobject, Boolean
from .entity import Entity
from .relationship import Relation
from .table import Table


class TablEntiMap(Baseobject):
    _tablename: str = 'tabl_enti_maps'
    _prefix: str = 'tema'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []

    def __init__(self):
        super().__init__()

    @staticmethod
    def __combiwhere(pentiid=None, prelaid=None, pintfid=None):
        return """ case when tema_enti_id is NULL 
                            then ' ' 
                            else tema_enti_id end  like '{}'
                      and case when tema_rela_id is NULL 
                            then ' ' 
                            else tema_rela_id end   like '{}'
                      and case when tabl_intf_id is NULL 
                            then ' ' 
                            else tabl_intf_id end like '{}'""".format(str(pentiid) if pentiid is not None else '%'
                                                                      , str(prelaid) if prelaid is not None else '%'
                                                                      , str(pintfid) if pintfid is not None else '%')

    @staticmethod
    def gettabllist(pentiid=None, prelaid=None, pintfid=None):
        where = """tabl_id in (select tema_tabl_id 
                                from tabl_enti_maps
                                join tables on tabl_id = tema_tabl_id 
                                where {})""".format(
                                    TablEntiMap.__combiwhere(pentiid=pentiid, prelaid=prelaid, pintfid=pintfid))
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
    def tablelist(pentiid=None):
        data = dbDML.select("""select  intf_name,group_concat(tabl_id,',') tabids
                            from tabl_enti_maps
                            join tables on tabl_id = tema_tabl_id
                            join interfaces on intf_id = tabl_intf_id 
                            where tema_enti_id = {}
                            group by intf_name
                            order by intf_name
                            """.format(pentiid if pentiid is not None else 'tema_enti_id'))
        retval = []
        try:
            for d in data:
                intf_name = d[0]
                tablist = {}
                for tabid in d[1].split(','):
                    tab = Table().getbyid(tabid)
                    tablist[tab.tabl_name] = tab.webanker()
                # for
                retval.append([intf_name, tablist])
            # for
        except:
            pass
        # try
        return retval

    # tablelist

    @staticmethod
    def extendedtabentimap():
        data = dbDML.select("""select  tema_tabl_id,tema_enti_id,tabl_name,enti_name,intf_name
                            from tabl_enti_maps
                            join tables on tabl_id = tema_tabl_id
                            join interfaces on intf_id = tabl_intf_id
                            join entitaeten on enti_id = tema_enti_id 
                            order by intf_name,tabl_name,enti_name
                            """)
        retval = defaultdict(dict)
        for d in data:
            retval[d[0]][d[1]] = [d[2], d[3], d[4]]
        # for
        return retval

    # extendedtabentimap

    @staticmethod
    def tabentimap():
        data = dbDML.select("""select  tema_tabl_id,tema_enti_id
                        from tabl_enti_maps
                        """)
        retval = defaultdict(dict)
        for d in data:
            retval[d[0]][d[1]] = True
        # for
        return retval

    # tabentimap

    @staticmethod
    def tabrelamap():
        data = dbDML.select("""select  tema_tabl_id,tema_rela_id
                        from tabl_enti_maps
                        """)
        retval = defaultdict(dict)
        for d in data:
            retval[d[0]][d[1]] = True
        # for
        return retval
    # tabrelamap
# TablEntiMap
