from .baseobject import Baseobject
from datetime import date

class Storageformat(Baseobject):
    _tablename:str = 'storage_formats'
    _prefix:str = 'stfo'
    _columnlist:list = []
    _defaultorderby = "stfo_id"

    def __init__(self,pname=None,pdescr=None):
        if (len(Storageformat._columnlist) == 0): Storageformat._columnlist = Baseobject.gettablecolumns(Storageformat._tablename)
        super().__init__()
        self.stfo_name = pname
        self.stfo_descr = pdescr
        self.stfo_uc = 'fillDB'
        self.stfo_dc = date.today()

    def getname(self,plang=None):
        return self.stfo_name

    def getdescr(self,plang=None):
        return self.getdescr()


    @classmethod
    def getbyname(cls,pname):
        return cls.getbyuk(stfo_name=pname)
    # getbyname

    @staticmethod
    def getorcreate(pname):
        stfo =  Storageformat().getbyuk(stfo_name=pname)
        if stfo is None:
            stfo = Storageformat(pname=pname)
            stfo.insert()
        return stfo
    # getbyorcreate

#Storageformat

class PhysicalUnit(Baseobject):
    _tablename:str = 'physical_unit'
    _prefix:str = 'phyu'
    _columnlist:list = []
    _defaultorderby = "phyu_name"


    def __init__(self,):
        if (len(PhysicalUnit._columnlist) == 0): PhysicalUnit._columnlist = Baseobject.gettablecolumns(PhysicalUnit._tablename)
        super().__init__()
        self.phyu_uc = 'fillDB'
        self.phyu_dc = date.today()



    @classmethod
    def getbyname(cls,pname):
        return cls.getbyuk(phyu_name=pname)
    # getbyname

    @staticmethod
    def getorcreate(pname):
        phyu =  PhysicalUnit().getbyuk(phyu_name=pname)
        if phyu is None:
            phyu = PhysicalUnit()
            phyu.phyu_name = pname
            phyu.insert()
        return phyu
    # getbyorcreate

#PhysicalUnit
