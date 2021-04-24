from datetime import date
from .relationship import Relation
from .baseobject import Baseobject
from .modelelement import Modelelement,Modelelemtype
from .entity import Entity
from .attribute import Attribute


class Elementrep(Baseobject):
    _tablename: str = 'elementreps'
    _prefix: str = 'eler'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []

    def __init__(self):
        if (len(Elementrep._columnlist) == 0): Elementrep._columnlist = Baseobject.gettablecolumns(Elementrep._tablename)
        super().__init__()
        eler_index = 0
        eler_uc = 'system'
        eler_dc = date.today()



    """what is displayed on bottom (0) and what in higer positions"""
    def displorder(self):
        elem = Modelelement.getelement(self.eler_mode_id)
        if isinstance(elem,Entity):
            return elem.getsubtypelevel()
        elif isinstance(elem,Attribute):
            return elem.attr_displ_seq
        else: return 0
    #displorder




    @classmethod
    def getbydiagmode(pdiagid, pmodeid,pidx=None):
        elers = cls.select(pwhere=("""eler_diag_id = ? 
                                              and eler_mode_id = ?
                                              and eler_index = ?""",
                                    pdiagid, pmodeid, pidx if pidx is not None else 'eler_index'))
        if elers is None:
            return []
        elif (pidx is None):
            #may be several
            return elers
        else:
            #can only be one
            return elers[0]
    #getbydiagmode
# elementrep

class Relationrep(Baseobject):
    NORTH = 'N'
    EAST = 'O'
    SOUTH = 'S'
    WEST = 'W'
    ONE = Relation.ONE
    MANY = Relation.MANY

    _tablename: str = 'relationreps'
    _prefix: str = 'relr'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []

    def __init__(self):
        if (len(Relationrep._columnlist) == 0): Relationrep._columnlist = Baseobject.gettablecolumns(Relationrep._tablename)
        super().__init__()
        relr_uc = 'system'
        relr_dc = date.today()


    def getlinesegments(self):
        return Linesegment.select(pwhere=("lise_relr_id = ?", self.relr_id))


# relationrep

class Linesegment(Baseobject):
    DADO = "DADO"
    DASHED = "DASHED"
    DOTTED= "DOTTED"
    SOLID = "SOLID"

    _tablename: str = 'linesegments'
    _prefix: str = 'lise'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []
    _defaultorderby = "lise_seq"

    def __init__(self):
        if (len(Linesegment._columnlist) == 0): Linesegment._columnlist = Baseobject.gettablecolumns(Linesegment._tablename)
        super().__init__()
        lise_uc = 'system'
        lise_dc = date.today()


# linesegment
