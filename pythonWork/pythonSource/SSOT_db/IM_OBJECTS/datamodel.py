from .baseobject import Baseobject
from .modelelement import Modelelemtype

class Datamodel(Baseobject):
    _tablename:str = 'datamodels'
    _prefix:str = 'datm'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.DATM
    _columnlist = dict()
    _defaultorderby = 'datm_name'

    def __init__(self, psrcname=None, psrcid=None):

        super().__init__(pscrid=psrcid,
                         psrcname=psrcname)

    def getname(self,plang=None):
        return self.datm_name

    def getqualifiedname(self,plang=None):
        return self.datm_name

    def getdescr(self, plang=None):
        return self.datm_descr



    @staticmethod
    def getmapped(pentiid=None,pattrid=None,prelaid=None):
        retval = []
        if pentiid is not None:
            retval = Datamodel.select(pwhere=("""datm_id in (select tabl_datm_id 
                                                    from tables
                                                    join tabl_enti_maps on tema_tabl_id = tabl_id
                                                    where tema_enti_id = ?
                                                    )""", pentiid))
        if prelaid is not None:
            retval = Datamodel.select(pwhere=("""datm_id in (select tabl_datm_id 
                                                        from tables
                                                        join tabl_enti_maps on tema_tabl_id = tabl_id
                                                        where tema_rela_id = ?
                                                        )""", prelaid))
        if pattrid is not None:
            retval = Datamodel.select(pwhere=("""datm_id in (select tabl_datm_id 
                                                        from tables
                                                        join columns on colu_tabl_id = tabl_id
                                                        join colu_attr_map on coam_colu_id = colu_id
                                                        where coam_attr_id = ?
                                                        )""", pattrid))
        return retval



