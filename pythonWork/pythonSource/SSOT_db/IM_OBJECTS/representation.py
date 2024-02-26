from math import pi
from .attribute import Attribute
from .baseobject import Baseobject
from .entity import Entity
from .modelelement import Modelelement
from .relationship import Relation


class Elementrep(Baseobject):
    _tablename: str = 'elementreps'
    _prefix: str = 'eler'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setdefaultval("eler_index", 0)
        return

    """what is displayed on bottom (0) and what in higer positions"""
    def insert(self,pdoerrhdlng=True):
        super().insert(pdoerrhdlng=pdoerrhdlng)

    def displorder(self):
        elem = Modelelement.getelement(self.eler_mode_id)
        if isinstance(elem, Entity):
            return elem.getsubtypelevel()
        elif isinstance(elem, Attribute):
            return elem.attr_displ_seq
        else:
            return 0

    @classmethod
    def getbydiagmode(cls,pdiagid, pmodeid, pidx=None):
        if pidx is None:
            where =("""eler_diag_id = ? 
                        and eler_mode_id = ?""",
                                   pdiagid, pmodeid)
        else:
            where = ("""eler_diag_id = ? 
                        and eler_mode_id = ?
                       and (eler_index = ?)"""
                     ,pdiagid, pmodeid, pidx)
        #fi
        elers = cls.select(pwhere=where)
        if elers is None or len(elers)==0:
            return []
        elif (pidx is None):
            # may be several
            return elers
        else:
            # can only be one
            return elers[0]


class Relationrep(Baseobject):
    ONE = Relation.ONE
    MANY = Relation.MANY

    _tablename: str = 'relationreps'
    _prefix: str = 'relr'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setdefaultval("relr_linewidth",1)
        self.setdefaultval("relr_linecolor",'000000')
        self.setdefaultval("relr_lineopacity",100)
        self.setdefaultval("relr_fontcolor",'000000')
        return

    def getlinesegments(self):
        return Linesegment.select(pwhere=("lise_relr_id = ?", self.relr_id), porderby="lise_seq")

    # direction (NEWS) in with the relationship starts from the from element
    def startingdirection(self):
        linesegs = self.getlinesegments()
        return linesegs[0].direction()

    # direction (NEWS) in with the relationship ends on the toelement
    def endingdirection(self):
        linesegs = self.getlinesegments()
        return linesegs[len(linesegs) - 2].reversedirection()

    def getrela(self):
        return Relation().getbyid(pid=self.relr_mode_id)

class Linesegment(Baseobject):
    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'
    DADO = "DADO"
    DASHED = "DASHED"
    DOTTED = "DOTTED"
    SOLID = "SOLID"

    _tablename: str = 'linesegments'
    _prefix: str = 'lise'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []
    _defaultorderby = "lise_seq"

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.setdefaultval("lise_linetype",'SOLID')
        return

    def direction(self):
        if pi / 4 <= self.lise_angle < 3 * pi / 4:
            return Linesegment.NORTH
        elif -pi / 4 <= self.lise_angle < pi / 4:
            return Linesegment.EAST
        elif -3 * pi / 4 <= self.lise_angle < -pi / 4:
            return Linesegment.SOUTH
        elif (3 * pi / 4 <= self.lise_angle <= pi) \
                or (-pi < self.lise_angle < -3 * pi / 4):
            return Linesegment.WEST
        assert False, f"winkel {self.lise_angle} nicht im Bereich"

    def reversedirection(self):
        direc = self.direction()
        return Linesegment.NORTH if direc == Linesegment.SOUTH else \
            Linesegment.SOUTH if direc == Linesegment.NORTH else \
                Linesegment.WEST if direc == Linesegment.EAST else \
                    Linesegment.EAST
# linesegment
