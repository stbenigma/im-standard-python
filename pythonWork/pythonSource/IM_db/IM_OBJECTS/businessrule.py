from .baseobject import Baseobject, MultilangBaseobject,Boolean
from .languagetext import Languagetext

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
    _columnlist: list = []

    def __init__(self, psrcname=None, psrcid=None):

        if (len(BusinessRule._columnlist) == 0): BusinessRule._columnlist = Baseobject.gettablecolumns(BusinessRule._tablename)
        super().__init__(tablename=BusinessRule._tablename, prefix=BusinessRule._prefix
                         , multilangcols={'buru_descr': Languagetext.ATTR_COMMENT,
                                          'buru_errormsg': Languagetext.ATTR_TOOLTIP}
                         , pmodelemtype=Modelelemtype.BURU
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
    def delete():
        Baseobject.delete(BusinessRule._tablename)

    @staticmethod
    def select(pwhere=None, porderby="buru_name"):
        attrs = Baseobject.select(pclass=BusinessRule
                                  , pwhere=pwhere, porderby=porderby)
        return attrs
    # select
# BusinessRule

class BusinessruleElement(Baseobject):
    _tablename: str = 'businessrule_elements'
    _prefix: str = 'bure'
    _columnlist: list = []

    def __init__(self, pburuid=None,pwriteable=False
                 ,pattrid=None,pentiid=None,prelaid=None,pdevaid=None,ptablid=None,pcoluid=None):

        if (len(BusinessruleElement._columnlist) == 0): BusinessruleElement._columnlist = Baseobject.gettablecolumns(BusinessruleElement._tablename)
        super().__init__(tablename=BusinessruleElement._tablename, prefix=BusinessruleElement._prefix)
        self.bure_buru_id = pburuid
        self.bure_attr_id = pattrid
        self.bure_enti_id = pentiid
        self.bure_rela_id = prelaid
        self.bure_deva_id = pdevaid
        self.bure_tabl_id = ptablid
        self.bure_colu_id = pcoluid
        self.bure_id = pburuid
        self.bure_writeable = Boolean.bool2str(pwriteable)

    def getelement(self):
        return Modelelement.getelement(pmodeid=self.bure_attr_id if self.bure_attr_id is not None else
                                               self .bure_enti_id if self.bure_enti_id is not None else
                                               self.bure_rela_id if self.bure_rela_id is not None else
                                               self.bure_deva_id if self.bure_deva_id is not None else
                                               self.bure_tabl_id if self.bure_tabl_id is not None else
                                               self.bure_colu_id if self.bure_colu_id is not None else
                                              None)

    @staticmethod
    def delete():
        Baseobject.delete(BusinessruleElement._tablename)

    @staticmethod
    def select(pwhere=None, porderby="attr_displ_seq"):
        attrs = Baseobject.select(pclass=BusinessruleElement
                                  , pwhere=pwhere, porderby=porderby)
        return attrs
    # select
# BusinessruleELement
from .modelelement import Modelelement,Modelelemtype






