from .baseobject import  MultilangBaseobject
from .languagetext import Languagetext
from .domain import Domain
from .key import Key
from .modelelement import Modelelemtype,Modelelement
from .examples import Example
import SSOT_db.IM_OBJECTS


class Attribute(MultilangBaseobject):
    _tablename: str = 'attributes'
    _prefix: str = 'attr'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.ATTR
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []
    _defaultorderby : "attr_displ_seq"

    def __init__(self, pname=None, pentiid=None
                    ,psrcname=None, psrcid=None):


        super().__init__( multilangcols={'attr_displ_name': Languagetext.ATTR_NAME,
                                          'attr_descr': Languagetext.ATTR_COMMENT,
                                          'attr_tooltip': Languagetext.ATTR_TOOLTIP},
                         pscrid=psrcid,
                         psrcname=psrcname)
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
        return IM_db.IM_OBJECTS.Entity().getbyid(self.attr_enti_id)

    def isinkey(self):
        return Keyelement.isinkey(pattrid=self.attr_id)

    def getdomain(self):
        return Domain().getbyid(self.attr_doma_id)


    def getkeys(self):
        return Key.select(pwhere=("""keys_id in 
                                    (select kele_keys_id 
                                    from key_elements 
                                    where kele_attr_id = ?)""", self.attr_id))

    def getexamples(self):
        return Example.getexamples(pmodeid=self.getid())


# Attribute
from .key import Keyelement





