from .webbaseobject import Webanker,BaseWebObj,Objlist
from IM_OBJECTS import  Interface


class WebInterface(BaseWebObj):
    def __init__(self, pid=None, pdbobj: Interface = None):
        super().__init__(pobjtype=Interface, pid=pid, pdbobj=pdbobj)

    def getname(self, plang=None):
        return self.dbobject().getname(plang=plang)

    def webanker(self):
        if self.dbobject() is None: return None
        return Webanker(ptype=self.dbobject()._prefix, pid=self.getid(),pmodelid=self.dbobject().intf_id)

    @staticmethod
    def indexlist(plang=None):
        members = [WebInterface(pdbobj=obj) for obj in Interface.select()]
        idxlist = Objlist(pmembers=members).indexlist(plang=plang)
        return idxlist
    # grouplist
# WebInterface
