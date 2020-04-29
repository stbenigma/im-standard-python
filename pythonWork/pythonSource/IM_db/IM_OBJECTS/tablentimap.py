from .baseobject import Baseobject
from .tabelle import Tabelle
from  IM_DB import dbDML

class TablEntiMap(Baseobject):
    _tablename:str = 'tabl_enti_maps'
    _prefix:str = 'tema'
    _columnlist:list = ['tema_id', 'tema_tabl_id', 'tema_enti_id', 'tema_bezi_id']

    def __init__(self):
        super().__init__(tablename=TablEntiMap._tablename, prefix=TablEntiMap._prefix
                        ,columnlist = TablEntiMap._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=TablEntiMap._tablename
                               , psql="""
          create table tabl_enti_maps 
          (
           tema_id integer primary key autoincrement , 
           tema_tabl_id integer not null , 
           tema_enti_id integer null , 
           tema_bezi_id integer null , 
           constraint tema_ck check ((tema_enti_id is not null and tema_bezi_id is null )
               	        		  or (tema_enti_id is null and tema_bezi_id is not null)),
       		   constraint tema_un unique (tema_tabl_id , tema_enti_id ,tema_bezi_id)
    		   ,constraint tema_bezi_fk foreign key (tema_bezi_id) 
    		      references beziehung (bezi_id ) 
    		   ,constraint tema_enti_fk foreign key (tema_enti_id) 
    		      references entitaet (enti_id ) 
    		   ,constraint tema_tabl_fk foreign key (tema_tabl_id) 
    		      references tabellen (tabl_id ) 
          )    """
                            )
    @staticmethod
    def delete():
        Baseobject.delete(TablEntiMap._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=TablEntiMap
                                 , pwhere=pwhere, porderby=porderby)
    @staticmethod
    def anker(pid):
        return Baseobject.anker(TablEntiMap._prefix,pid)

    @staticmethod
    def tablelist(pentiid=None):
        data = dbDML.select("""select  schn_name,group_concat(tabl_id,',') tabids
                            from tabl_enti_maps
                            join tabellen on tabl_id = tema_tabl_id
                            join schnittstellen on schn_id = tabl_schn_id 
                            where tema_enti_id = {}
                            group by schn_name
                            order by schn_name
                            """.format(pentiid))
        retval = []
        try:
            for d in data:
                schn_name = d[0]
                tablist = {}
                for tabid in d[1].split(','):
                    tab = Tabelle().getbyid(tabid)
                    tablist[tab.tabl_name] = tab.webanker()
                # for
                retval.append([schn_name, tablist])
            # for
        except:
            pass
        # try
        return retval
# tablelist
#TablEntiMap


