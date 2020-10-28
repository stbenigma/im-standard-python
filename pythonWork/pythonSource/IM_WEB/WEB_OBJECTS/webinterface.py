from .webbaseobject import Webanker,BaseWebObj,Objlist
from IM_OBJECTS import  Schnittstelle


class WebInterface(BaseWebObj):
    def __init__(self, pid=None, pdbobj: Schnittstelle = None):
        super().__init__(pobjtype=Schnittstelle, pid=pid, pdbobj=pdbobj)

    def getname(self, plang=None):
        return self.dbobject().schn_name

    def webanker(self):
        if self.dbobject() is None: return None
        return Webanker(ptype=self.dbobject()._prefix, pid=self.getid(),pmodelid=self.dbobject().schn_id)

    @staticmethod
    def indexlist(plang=None):
        members = [WebInterface(pdbobj=obj) for obj in Schnittstelle.select()]
        idxlist = Objlist(pmembers=members).indexlist(plang=plang)
        return idxlist
    # indexlist
# WebInterface
