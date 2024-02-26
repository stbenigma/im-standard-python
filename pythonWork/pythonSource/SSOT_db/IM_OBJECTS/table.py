from .baseobject import Baseobject
from .modelelement import Modelelemtype
from SSOT_db.SQL_INFRA import dbDML


class Table(Baseobject):
    _tablename:str = 'tables'
    _prefix:str = 'tabl'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.TABL
    _columnlist = dict()
    _defaultorderby = "tabl_name"

    def __init__(self,psrcname=None, psrcid=None,**kwargs):
        super().__init__(pscrid=psrcid,
                         psrcname=psrcname,**kwargs)
        self.setdefaultval("tabl_create",'FALSE')
        self.setdefaultval("tabl_read",'TRUE')
        self.setdefaultval("tabl_update",'FALSE')
        self.setdefaultval("tabl_delete",'FALSE')
        return


    def getmodellelement(self):
        return Modellelement.getbyelemid(ptablid=self.tabl_id)

    def getcolumns(self):
        return Column.select(pwhere=("colu_tabl_id = ?", self.tabl_id), porderby="colu_id")

    def getname(self,plang=None):
        return self.tabl_name

    def getdescr(self,plang=None):
        return self.tabl_descr


    @classmethod
    def selectbyschnid(cls,pschnid):
        return cls.select(pwhere=("tabl_datm_id = ?", pschnid))

    @staticmethod
    def indexlist(pschnid=None):
        data = Table.select(pwhere=("tabl_datm_id = ?", 'tabl_datm_id' if pschnid is None else pschnid))
        indexlist = [[d.tabl_name,"TAB",d.tabl_id] for d in data]
        return indexlist
    #grouplist

    @staticmethod
    def mappingto(ptablid):
        lsqle = """select 0 datm_id, 'Logisches Modell' datm_name, group_concat(enti_id,',')
        	from  tabl_enti_maps as mastermap
	        left join entites on enti_id = mastermap.tema_enti_id
	        where  mastermap.tema_tabl_id = {}
	        GROUP BY mastermap.tema_tabl_id""".format(ptablid)
        lsqlt = """select tabl_datm_id,datm_name,group_concat(tabl_id,',')
	        from tables subtab
	        join datamodels on datm_id = TABL_datm_ID
	        where tabl_id in
    	          (select tema1.tema_tabl_id
	               from tabl_enti_maps tema1
	                 join tabl_enti_maps tema2 on tema2.tema_enti_id = tema1.tema_enti_id
	                                and tema2.tema_tabl_id != tema1.tema_tabl_id
	                  where tema2.tema_tabl_id = {}
	            )
	            /* eigene Datamodel wird nicht angezeigt*/
	           and datm_id != (select tabl_datm_id 
	                            from tables where tabl_id = {})
            group by tabl_datm_id,datm_name
            """.format(ptablid,ptablid)
        retval = []
        data = dbDML.select(lsqle)
        """[(0,'name', [Entity]'), ]"""
        for d in data:
            retval.append([d[0], d[1], [Entity().getbyid(e) for e in d[2].split(',')]])
        data = dbDML.select(lsqlt)
        """[(54,'name', [Table])]"""
        for d in data:
            retval.append([d[0], d[1], [Table().getbyid(e) for e in d[2].split(',')]])
        return retval
    #maopingto
#Table
from .column import Column
from .entity import Entity




