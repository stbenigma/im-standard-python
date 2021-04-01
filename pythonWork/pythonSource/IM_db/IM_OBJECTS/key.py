from .baseobject import Baseobject
from .modelelement import Modelelemtype

class Key(Baseobject):
    _tablename: str = 'keys'
    _prefix: str = 'keys'
    _columnlist: list = []
    _defaultorderby = "keys_id"

    def __init__(self, psrcname=None, psrcid=None):
        if (len(Key._columnlist) == 0): Key._columnlist = Baseobject.gettablecolumns(Key._tablename)
        super().__init__( pmodelemtype=Modelelemtype.KEYS
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


# Key

class Keyelement(Baseobject):
    _tablename: str = 'key_elements'
    _prefix: str = 'kele'
    _columnlist: list = []
    _defaultorderby = "kele_id"

    def __init__(self):
        if (len(Keyelement._columnlist) == 0): Keyelement._columnlist = Baseobject.gettablecolumns(Keyelement._tablename)
        super().__init__()


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


# Keyelement
from .attribute import Attribute
from .relationship import Relation
