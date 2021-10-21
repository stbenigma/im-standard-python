from .baseobject import Baseobject, MultilangBaseobject,Boolean
from .languagetext import Languagetext
from .modelelement import Modelelement,Modelelemtype

class BusinessRule(MultilangBaseobject):
    BURU_TYPE_TRIGGER = 'TRIGGER'
    BURU_TYPE_CHECK = 'CHECK'
    BURU_TYPE_CALC = 'CALC'
    BURU_LEVEL_TUPL = 'TUPL'
    BURU_LEVEL_ENTI = 'ENTI'
    BURU_LEVEL_DB = 'DB'
    BURU_LEVEL_ATTR = 'ATTR'

    _tablename: str = 'business_rules'
    _prefix: str = 'buru'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.BURU
    _columnlist: list = []
    _defaultorderby = "buru_name"

    def __init__(self, psrcname=None, psrcid=None):


        super().__init__( multilangcols={'buru_descr': Languagetext.ATTR_COMMENT,
                                          'buru_errormsg': Languagetext.ATTR_TOOLTIP}
                         , pscrid=psrcid
                         , psrcname=psrcname)

    def getname(self, plang=None):
        return self._getsprachval(colname='buru_name', plang=plang)

    def getdescr(self, plang=None):
        return self._getsprachval(colname='buru_descr', plang=plang)

    def geterrormsg(self, plang=None):
        return self._getsprachval(colname='buru_errormsg', plang=plang)

    def getmodellelement(self):
        return Modelelement.getbyelemid(pattrid=self.buru_id)



    @staticmethod
    def setburuelements():
        """
        analyse businesrules and link the buru too the elements mentionend in them.
        for domains copy buru to all attributes marked as "use domain constraint"
        """
        return

# BusinessRule

class BusinessruleElement(Baseobject):
    _tablename: str = 'businessrule_elements'
    _prefix: str = 'bure'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []

    def __init__(self, pburuid=None,pwriteable=False,pmodeid=None):
        super().__init__()
        self.bure_buru_id = pburuid
        self.bure_mode_id = pmodeid
        self.bure_writeable = Boolean.bool2str(pwriteable)

    def getelement(self):
        return Modelelement.getelement(pmodeid=self.bure_mode_id)

    def getparent(self) -> BusinessRule :
        buru = BusinessRule().getbyid(pid=self.bure_buru_id)
        return buru

    @classmethod
    def getburuelements(cls,pmodeid):
        bures = cls.select(pwhere=("""(bure_mode_id = ?)""", pmodeid))
        return bures
# BusinessruleELement






