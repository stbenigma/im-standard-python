from .baseobject import Baseobject
from .modelelement import Modelelemtype

class Key(Baseobject):
    _tablename: str = 'keys'
    _prefix: str = 'keys'
    _columnlist: list = []

    def __init__(self, psrcname=None, psrcid=None):
        if (len(Key._columnlist) == 0): Key._columnlist = Baseobject.gettablecolumns(Key._tablename)
        super().__init__(tablename=Key._tablename, prefix=Key._prefix
                         , pmodelemtype=Modelelemtype.KEYS
                         , psrcname=psrcname
                         , pscrid=psrcid)


    def getkeyelements(self,ptype=None):
        if ptype == Modelelemtype.RELA:
            which = ' and kele_rela_id is not null'
        elif ptype == Modelelemtype.ATTR:
            which = ' and kele_attr_id is not null'
        else:
            which = ''
        #fi
        return  Keyelement.select(pwhere=('kele_keys_id = ?', str(self.getid()) + which))

    @staticmethod
    def delete(pwhere=None):
        return Baseobject.delete(Key._tablename)

    @staticmethod
    def select(pwhere=None, porderby="keys_id"):
        return Baseobject.select(pclass=Key, pwhere=pwhere, porderby=porderby)
# Key

class Keyelement(Baseobject):
    _tablename: str = 'key_elements'
    _prefix: str = 'kele'
    _columnlist: list = []

    def __init__(self):
        if (len(Keyelement._columnlist) == 0): Keyelement._columnlist = Baseobject.gettablecolumns(Keyelement._tablename)
        super().__init__(tablename=Keyelement._tablename, prefix=Keyelement._prefix)


    @staticmethod
    def isinkey(pattrid=None, prelaid=None) -> bool:
        if pattrid is not None:
            return len(Keyelement.select(pwhere=("kele_attr_id = ?", pattrid))) > 0
        if prelaid is not None:
            return len(Keyelement.select(pwhere=("kele_rela_id = ?", prelaid))) > 0
        return False

    # isinkey

    def getkeyelement(self):
        if self.kele_attr_id is not None:
            return Attribute().getbyid(self.kele_attr_id)
        if self.kele_rela_id is not None:
            return Relation().getbyid(self.kele_rela_id)

    # getkeyelement

    @staticmethod
    def delete(pwhere=None):
        return Baseobject.delete(Keyelement._tablename,pwhere=pwhere)

    @staticmethod
    def select(pwhere=None, porderby="kele_id"):
        return Baseobject.select(pclass=Keyelement, pwhere=pwhere, porderby=porderby)
    # Keyelement
from .attribute import Attribute
from .relationship import Relation
