from .baseobject import Baseobject
from .modelelement import Modelelemtype

class Interface(Baseobject):
    _tablename:str = 'interfaces'
    _prefix:str = 'intf'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.INTF
    _columnlist =  []
    _defaultorderby = 'intf_name'

    def __init__(self, psrcname=None, psrcid=None):
        if (len(Interface._columnlist) == 0): Interface._columnlist = Baseobject.gettablecolumns(Interface._tablename)
        super().__init__(pscrid=psrcid
                         , psrcname=psrcname)

    def getname(self,plang=None):
        return self.intf_name

    def getqualifiedname(self,plang=None):
        return self.intf_name

    def getdescr(self, plang=None):
        return self.intf_descr



    @staticmethod
    def getmapped(pentiid=None,pattrid=None):
        if pentiid is not None:
            return Interface.select(pwhere=("""intf_id in (select tabl_intf_id 
                                                        from tables
                                                        join tabl_enti_maps on tema_tabl_id = tabl_id
                                                        where tema_enti_id = ?
                                                        )""", pentiid))
        if pattrid is not None:
            return Interface.select(pwhere=("""intf_id in (select tabl_intf_id 
                                                        from tables
                                                        join columns on colu_tabl_id = tabl_id
                                                        join colu_attr_map on coam_colu_id = colu_id
                                                        where coam_attr_id = ?
                                                        )""", pattrid))
        return []

#Interface



