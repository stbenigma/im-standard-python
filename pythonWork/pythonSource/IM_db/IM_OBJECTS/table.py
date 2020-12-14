from .baseobject import Baseobject
from .modelelement import Modelelement,Modelelemtype
from IM_DB import dbDML

class Table(Baseobject):
    _tablename:str = 'tables'
    _prefix:str = 'tabl'
    _columnlist =  []

    def __init__(self,psrcname=None, psrcid=None):
        if (len(Table._columnlist) == 0): Table._columnlist = Baseobject.gettablecolumns(Table._tablename)
        super().__init__(tablename=Table._tablename, prefix=Table._prefix
                         , pmodelemtype=Modelelemtype.TABL
                         , pscrid=psrcid
                         , psrcname=psrcname)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Table._tablename
                               , psql="""
    CREATE TABLE tables
        (
         tabl_id integer primary key autoincrement , 
         tabl_name varchar (60) not null , 
         tabl_intf_id integer not null , 
         tabl_prefix varchar (60) null , 
         tabl_descr varchar (4000) null , 
         tabl_uc varchar (30) not null , 
         tabl_dc varchar (30) not null , 
         tabl_um varchar (30) null , 
         tabl_dm varchar (30) null ,
    	  CONSTRAINT TABL_UN UNIQUE (TABL_intf_ID , TABL_NAME)
     	   ,CONSTRAINT TABL_intf_FK FOREIGN KEY (TABL_intf_ID) 
     	      REFERENCES interfaces (intf_ID ) 
     	   ,CONSTRAINT TABL_MODE_FK FOREIGN KEY (TABL_ID) 
     	      REFERENCES modelelement (mode_ID ) 
        )"""
                            )
    def getmodellelement(self):
        return Modellelement.getbyelemid(ptablid=self.tabl_id)

    def getcolumns(self):
        return Column.select("colu_tabl_id = {}".format(self.tabl_id))

    def getname(self,plang=None):
        return self.tabl_name

    def getdescr(self,plang=None):
        return self.tabl_descr

    def insert(self):
        self.tabl_id = Modelelement(Modelelemtype.TABL).insert()
        super().insert()

    @staticmethod
    def delete():
        Baseobject.delete(Table._tablename)

    @staticmethod
    def select(pwhere=None, porderby="tabl_name"):
        return Baseobject.select(pclass=Table
                                 , pwhere=pwhere, porderby=porderby)
    @staticmethod
    def selectbyschnid(pschnid):
        return Table.select(pwhere="tabl_intf_id = {}".format(pschnid))

    @staticmethod
    def indexlist(pschnid=None):
        data = Table.select(pwhere="tabl_intf_id={}".format('tabl_intf_id' if pschnid is None else pschnid))
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




