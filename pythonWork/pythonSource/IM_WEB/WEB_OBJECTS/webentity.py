from .webbaseobject import Webanker,BaseWebObj,Objlist
from IM_OBJECTS import  Entity,Attribute,Relation

class WebEntity(BaseWebObj):
    __members = None

    def __init__(self,pid=None,pdbobj:Entity=None):
        super().__init__(pobjtype=WebEntity,pid=pid,pdbobj=pdbobj)
        self.enti_id = self.dbobject().enti_id

    def getname(self,plang):
        return self.dbobject().getname(plang=plang)
    def getdescr(self,plang):
        return self.dbobject().getdescr(plang=plang)

    def getnames(self):
        return self.dbobject().enti_name_L

    def getparents(self):
        return [WebEntity(pdbobj=e) for e in self.dbobject().getparents()]

    def getchildren(self):
        return [WebEntity(pdbobj=e) for e in self.dbobject().getchildren()]

    @staticmethod
    def contentlist(plang):
        if WebEntity.__members is None: WebEntity.__members = [WebEntity(pdbobj=obj) for obj in Entity.select()]
        return WebEntity.__members

    @staticmethod
    def indexlist(plang=None):
        return Objlist(pmembers=WebEntity.contentlist(plang)).indexlist(plang=plang)
    # indexlist
#WebEntity

