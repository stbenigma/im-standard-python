from .baseobject import Baseobject
from .modelelement import Modelelemtype

class Interface(Baseobject):
    _tablename:str = 'interfaces'
    _prefix:str = 'intf'
    _columnlist:list = ['intf_id',  'intf_name',    'intf_descr'
                ,   'intf_uc',  'intf_dc' ,'intf_um', 'intf_dm']

    def __init__(self, psrcname=None, psrcid=None):
        super().__init__(tablename=Interface._tablename, prefix=Interface._prefix
                         , columnlist= Interface._columnlist
                         , pmodelemtype=Modelelemtype.INTF
                         , pscrid=psrcid
                         , psrcname=psrcname)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Interface._tablename
                               , psql="""
    CREATE TABLE interfaces
        (
         intf_ID integer primary key autoincrement, 
         intf_NAME VARCHAR (60) NOT NULL , 
         intf_DESCR VARCHAR (4000)  , 
         intf_UC VARCHAR (30) NOT NULL , 
         intf_DC VARCHAR (30) NOT NULL , 
         intf_UM VARCHAR (30) NULL , 
         intf_DM VARCHAR (30) NULL ,
     CONSTRAINT intf_UN UNIQUE (intf_NAME)
      ,CONSTRAINT INFT_MODE_FK FOREIGN KEY (INTF_ID) 
        REFERENCES MODELELEMENT (MODE_ID) 
        )
        """)

    def getname(self,plang=None):
        return self.intf_name
    def getqualifiedname(self,plang=None):
        return self.intf_name

    def getdescr(self, plang=None):
        return self.intf_descr

    @staticmethod
    def delete():
        Baseobject.delete(Interface._tablename)

    @staticmethod
    def select(pwhere=None, porderby='intf_name'):
        return Baseobject.select(pclass=Interface
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def getmapped(pentiid=None,pattrid=None):
        if pentiid is not None:
            return Interface.select(pwhere="""intf_id in (select tabl_intf_id 
                                                        from tables
                                                        join tabl_enti_maps on tema_tabl_id = tabl_id
                                                        where tema_enti_id = {}
                                                        )""".format(pentiid))
        if pattrid is not None:
            return Interface.select(pwhere="""intf_id in (select tabl_intf_id 
                                                        from tables
                                                        join columns on colu_tabl_id = tabl_id
                                                        join colu_attr_map on coam_colu_id = colu_id
                                                        where coam_attr_id = {}
                                                        )""".format(pattrid))
        return []

#Interface



