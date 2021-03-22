from .baseobject import Baseobject, MultilangBaseobject
from .languagetext import Languagetext
from .domain import Domain
from .key import Key
import IM_OBJECTS

class Attribute(MultilangBaseobject):
    _tablename: str = 'attributes'
    _prefix: str = 'attr'
    _columnlist: list = []

    def __init__(self, pname=None, pentiid=None
                    ,psrcname=None, psrcid=None):

        if (len(Attribute._columnlist) == 0): Attribute._columnlist = Baseobject.gettablecolumns(Attribute._tablename)
        super().__init__(tablename=Attribute._tablename, prefix=Attribute._prefix
                         , multilangcols={'attr_displ_name': Languagetext.ATTR_NAME,
                                          'attr_descr': Languagetext.ATTR_COMMENT,
                                          'attr_tooltip': Languagetext.ATTR_TOOLTIP}
                         , pmodelemtype=Modelelemtype.ATTR
                         , pscrid=psrcid
                         , psrcname=psrcname)
        self.attr_displ_name = pname
        self.attr_enti_id = pentiid

    def getname(self, plang=None):
        return self._getsprachval(colname='attr_displ_name', plang=plang)

    def getdescr(self, plang=None):
        return self._getsprachval(colname='attr_descr', plang=plang)

    def gettooltip(self, plang=None):
        return self._getsprachval(colname='attr_tooltip', plang=plang)

    def getentiname(self, plang=None):
        return self.getparent().getname(plang)

    def getmodellelement(self):
        return Modelelement.getbyelemid(pattrid=self.attr_id)

    def getmodeid(self):
        return self.getmodellelement().mode_id

    def getparent(self):
        return IM_OBJECTS.Entity().getbyid(self.attr_enti_id)

    def isinkey(self):
        return Keyelement.isinkey(pattrid=self.attr_id)

    def getdomain(self):
        return Domain().getbyid(self.attr_doma_id)


    def getkeys(self):
        return Key.select(pwhere=("""keys_id in 
                                    (select kele_keys_id 
                                    from key_elements 
                                    where kele_attr_id = ?)""", self.attr_id))
    @staticmethod
    def delete(pwhere=None):
        return Baseobject.delete(Attribute._tablename,pwhere=pwhere)

    @staticmethod
    def select(pwhere=None, porderby="attr_displ_seq"):
        attrs = Baseobject.select(pclass=Attribute
                                  , pwhere=pwhere, porderby=porderby)
        return attrs
    # select
# Attribute
from .modelelement import Modelelement,Modelelemtype
from .key import Keyelement





