from .baseobject import Baseobject, MultilangBaseobject, Boolean
from .languagetext import Languagetext
from .modelelement import Modelelement, Modelelemtype
from SSOT_infra import logmessages


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

    def __init__(self, **kwargs):
        srcid=kwargs['srcid'] if 'srcid' in kwargs else None
        srcname=kwargs['srcname'] if 'srcname' in kwargs else None
        super().__init__(multilangcols={'buru_name': Languagetext.BURU_NAME,
                                        'buru_descr': Languagetext.BURU_DESCR,
                                        'buru_errormsg': Languagetext.BURU_ERRORMSG}
                         , pscrid=srcid
                         , psrcname=srcname)
        for col,val in kwargs.items():
            if col in self._columnlist:
                self.setcolvalue(col,val)

    def getname(self, plang=None):
        return self._getsprachval(colname='buru_name', plang=plang)

    def getdescr(self, plang=None):
        return self._getsprachval(colname='buru_descr', plang=plang)

    def geterrormsg(self, plang=None):
        return self._getsprachval(colname='buru_errormsg', plang=plang)

    def getchildren(self):
        return BusinessruleElement.select(pwhere=("bure_buru_id=?",self.getid()))

    def getmodellelement(self):
        return Modelelement.getbyelemid(pattrid=self.buru_id)

    def searchorinsertburu(self):
        """searches for a buru with this name
            if it exists, return its id
            if not insert pburu and return this id
            if a found buru is not identical to pburu, write a log message, but return the found BR anyway
            """
        locburu = self.getbyuk(buru_name=self.buru_name)
        if locburu is None:
            #does not yet exist insert it
            buruid = self.insert()
        else:
            buruid = locburu.buru_id
            #check for identical definition and log error if not
            if not self.semanticequal(locburu):
                logmessages.writelog(f"""Business Rule "{self.buru_name}" already exists """+
                                     """ but with different definition. It is replaced by the exisiting one""")
        #fi
        return buruid

# BusinessRule

class BusinessruleElement(Baseobject):

    _tablename: str = 'businessrule_elements'
    _prefix: str = 'bure'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []

    def __init__(self, ** kwargs):
        super().__init__()
        for col, val in kwargs.items():
            if col in self._columnlist:
                self.setcolvalue(col, Boolean.bool2str(val) if type(val) is bool else val)
        if self.bure_writeable is None:
            self.bure_writeable = "FALSE"

    def getelement(self):
        return Modelelement.getelement(pmodeid=self.bure_mode_id)

    def getparent(self) -> BusinessRule:
        buru = BusinessRule().getbyid(pid=self.bure_buru_id)
        return buru

    @classmethod
    def getburuelements(cls, pmodeid):
        bures = cls.select(pwhere=("""(bure_mode_id = ?)""", pmodeid))
        return bures
# BusinessruleELement
