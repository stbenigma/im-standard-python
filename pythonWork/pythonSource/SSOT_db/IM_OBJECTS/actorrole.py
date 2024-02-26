from SSOT_infra import logmessages
from .baseobject import Baseobject, Boolean
from .languagetext import Languagetext
from .modelelement import Modelelement, Modelelemtype


class Actorrole(Baseobject):

    _tablename: str = 'actor_roles'
    _prefix: str = 'actr'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.ACTR
    _columnlist = dict()
    _defaultorderby = "actr_name"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setdefaultval("self.actc_responsible",'FALSE')
        self.setdefaultval("self.actc_accountable",'FALSE')
        self.setdefaultval("self.actc_consulted",'FALSE')
        self.setdefaultval("self.actc_informed",'FALSE')
        return

    def getname(self, plang=None):
        return self._getsprachval(colname='actr_name', plang=plang)

    def getdescr(self, plang=None):
        return self._getsprachval(colname='actr_descr', plang=plang)

    def getchildren(self):
        return Actorconcern.select(pwhere=("actc_actr_id=?", self.getid()))

    def getmodellelement(self):
        return Modelelement.getbyelemid(pattrid=self.getid())

    @staticmethod
    def getracis(pmodeid):
        actcs = Actorconcern.select(pwhere=("actc_mode_id = ?",pmodeid))
        retval ={ac.actc_actr_id : ac.getraci() for ac in actcs}
        return retval


# Actorrole

class Actorconcern(Baseobject):

    _tablename: str = 'actor_concerns'
    _prefix: str = 'actc'
    _idcolname: str = _prefix + '_id'
    _columnlist = dict()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def getelement(self):
        return Modelelement.getelement(pmodeid=self.actc_mode_id)

    def getparent(self) -> Actorrole:
        actr = Actorrole().getbyid(pid=self.actc_actr_id)
        return actr

    def getraci(self) -> str:
        retval = 'R' if Boolean.str2bool(self.actc_responsible) else ''
        retval += 'A' if Boolean.str2bool(self.actc_accountable) else ''
        retval += 'C' if Boolean.str2bool(self.actc_consulted) else ''
        retval += 'I' if Boolean.str2bool(self.actc_informed) else ''
        return retval

    @classmethod
    def getmodeconcerns(cls, pmodeid):
        actcs = cls.select(pwhere=("""(actc_mode_id = ?)""", pmodeid))
        return acts
# BusinessruleELement
