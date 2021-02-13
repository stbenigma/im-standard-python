from .baseobject import Baseobject
from datetime import date

class Storageformat(Baseobject):
    _tablename:str = 'storage_formats'
    _prefix:str = 'stfo'
    _columnlist:list = []

    def __init__(self,pname=None,pdescr=None):
        if (len(Storageformat._columnlist) == 0): Storageformat._columnlist = Baseobject.gettablecolumns(Storageformat._tablename)
        super().__init__(tablename= Storageformat._tablename, prefix= Storageformat._prefix)
        self.stfo_name = pname
        self.stfo_descr = pdescr
        self.stfo_uc = 'fillDB'
        self.stfo_dc = date.today()

    def getname(self,plang=None):
        return self.stfo_name

    def getdescr(self,plang=None):
        return self.getdescr()

    @staticmethod
    def delete():
        Baseobject.delete(Storageformat._tablename)

    @staticmethod
    def select(pwhere=None, porderby="stfo_id"):
        return Baseobject.select(pclass=Storageformat
                                 , pwhere=pwhere, porderby=porderby)
    @staticmethod
    def getbyname(pname):
        return Storageformat().getbyuk(pcolname='stfo_name', pukvalue=pname)
    # getbyname

    @staticmethod
    def getorcreate(pname):
        stfo =  Storageformat().getbyuk(pcolname='stfo_name', pukvalue=pname)
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


    def __init__(self,):
        if (len(PhysicalUnit._columnlist) == 0): PhysicalUnit._columnlist = Baseobject.gettablecolumns(PhysicalUnit._tablename)
        super().__init__(tablename= PhysicalUnit._tablename, prefix= PhysicalUnit._prefix)
        self.phyu_uc = 'fillDB'
        self.phyu_dc = date.today()


    @staticmethod
    def delete():
        Baseobject.delete(PhysicalUnit._tablename)

    @staticmethod
    def select(pwhere=None, porderby="phyu_name"):
        return Baseobject.select(pclass=PhysicalUnit
                                 , pwhere=pwhere, porderby=porderby)
    @staticmethod
    def getbyname(pname):
        return PhysicalUnit().getbyuk(pcolname='phyu_name', pukvalue=pname)
    # getbyname

    @staticmethod
    def getorcreate(pname):
        phyu =  PhysicalUnit().getbyuk(pcolname='phyu_name', pukvalue=pname)
        if phyu is None:
            phyu = PhysicalUnit()
            phyu.phyu_name = pname
            phyu.insert()
        return phyu
    # getbyorcreate

#PhysicalUnit
