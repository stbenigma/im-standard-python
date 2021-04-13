from .baseobject import Baseobject
from .modelelement import Modelelement,Modelelemtype
from IM_DB import dbDML

class Table(Baseobject):
    _tablename:str = 'tables'
    _prefix:str = 'tabl'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.TABL
    _columnlist = []
    _defaultorderby = "tabl_name"

    def __init__(self,psrcname=None, psrcid=None):
        if (len(Table._columnlist) == 0): Table._columnlist = Baseobject.gettablecolumns(Table._tablename)
        super().__init__(pscrid=psrcid
                         , psrcname=psrcname)


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
        return cls.select(pwhere=("tabl_intf_id = ?", pschnid))

    @staticmethod
    def indexlist(pschnid=None):
        data = Table.select(pwhere=("tabl_intf_id = ?", 'tabl_intf_id' if pschnid is None else pschnid))
        indexlist = [[d.tabl_name,"TAB",d.tabl_id] for d in data]
        return indexlist
    #grouplist

    @staticmethod
    def mappingto(ptablid):
        lsqle = """select 0 intf_id, 'Logisches Modell' intf_name, group_concat(enti_id,',')
        	from  tabl_enti_maps as mastermap
	        left join entites on enti_id = mastermap.tema_enti_id
	        where  mastermap.tema_tabl_id = {}
	        GROUP BY mastermap.tema_tabl_id""".format(ptablid)
        lsqlt = """select tabl_intf_id,intf_name,group_concat(tabl_id,',')
	        from tables subtab
	        join interfaces on intf_id = TABL_intf_ID
	        where tabl_id in
    	          (select tema1.tema_tabl_id
	               from tabl_enti_maps tema1
	                 join tabl_enti_maps tema2 on tema2.tema_enti_id = tema1.tema_enti_id
	                                and tema2.tema_tabl_id != tema1.tema_tabl_id
	                  where tema2.tema_tabl_id = {}
	            )
	            /* eigene Interface wird nicht angezeigt*/
	           and intf_id != (select tabl_intf_id 
	                            from tables where tabl_id = {})
            group by tabl_intf_id,intf_name
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




