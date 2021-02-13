from .baseobject import Baseobject
from .table import Table
from IM_DB import dbDML
from collections import defaultdict
from .entity import Entity

class TablEntiMap(Baseobject):
    _tablename:str = 'tabl_enti_maps'
    _prefix:str = 'tema'
    _columnlist:list = []

    def __init__(self):
        if (len(TablEntiMap._columnlist) == 0): TablEntiMap._columnlist = Baseobject.gettablecolumns(TablEntiMap._tablename)
        super().__init__(tablename=TablEntiMap._tablename, prefix=TablEntiMap._prefix)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=TablEntiMap._tablename
                               , psql="""
 create table tabl_enti_maps 
 (
  tema_id integer primary key autoincrement , 
  tema_tabl_id integer not null , 
  tema_enti_id integer null , 
  tema_rela_id integer null , 
  constraint tema_ck check ((tema_enti_id is not null and tema_rela_id is null )
      	        		  or (tema_enti_id is null and tema_rela_id is not null)),
		   constraint tema_un unique (tema_tabl_id , tema_enti_id ,tema_rela_id)
	   ,constraint tema_rela_fk foreign key (tema_rela_id) 
	      references relations (rela_id ) 
	   ,constraint tema_enti_fk foreign key (tema_enti_id) 
	      references entities (enti_id ) 
	   ,constraint tema_tabl_fk foreign key (tema_tabl_id) 
	      references tables (tabl_id ) 
 )    """
                            )
    @staticmethod
    def delete():
        Baseobject.delete(TablEntiMap._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=TablEntiMap
                                 , pwhere=pwhere, porderby="tabl_name")
    @staticmethod
    def anker(pid):
        return Baseobject.anker(TablEntiMap._prefix,pid)

    @staticmethod
    def gettabllist(pentiid=None,pintfid=None):
        return Table.select(pwhere="""tabl_id in (select tema_tabl_id 
                                                    from tabl_enti_maps
                                                    join tables on tabl_id = tema_tabl_id 
                                                    where tema_enti_id = {}
                                                    and tabl_intf_id = {})""".format(pentiid if pentiid is not None else 'tema_enti_id',pintfid if pintfid is not None else 'tabl_intf_id')
                            ,porderby="tabl_id")
    @staticmethod
    def getentilist(ptablid):
        return Entity.select(pwhere="""enti_id in (select tema_enti_id 
                                                    from tabl_enti_maps
                                                    where tema_tabl_id = {}
                                                    )""".format(ptablid)
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
            retval[d[0]][d[1]] = [d[2],d[3],d[4]]
        # for
        return retval
    #extendedtabentimap


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
    #tabentimap
#TablEntiMap


