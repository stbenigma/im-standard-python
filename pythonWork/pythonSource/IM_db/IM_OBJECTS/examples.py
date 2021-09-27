from .baseobject import Baseobject
import IM_OBJECTS


class Example(Baseobject):
    _tablename:str = 'examples'
    _prefix:str = 'expl'
    _idcolname: str = _prefix + '_id'
    _columnlist:list = []
    _defaultorderby = None

    def __init__(self,pvalue=None,pentiid=None,pattrid=None):
        super().__init__()
        self.expl_value = pvalue
        self.expl_enti_id = pentiid
        self.expl_attr_id = pattrid

    @staticmethod
    def getexamples(pattrid=None,pentiid=None):
        if pattrid is not None:
            src=IM_OBJECTS.Attribute._prefix
            id = pattrid
        elif pentiid is not None:
            src=IM_OBJECTS.Entity._prefix
            id = pentiid
        #fi
        return Baseobject.select(pwhere=(f"expl_{src}_id = ?",id))


