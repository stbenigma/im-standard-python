from .webbaseobject import Webanker,BaseWebObj,Objlist
from IM_OBJECTS import  Table


class WebTable(BaseWebObj):
    def __init__(self, pid=None, pdbobj: Table = None):
        super().__init__(pobjtype=Table, pid=pid, pdbobj=pdbobj)

    def getname(self, plang=None):
        return self.dbobject().getname(plang=plang)

    def webanker(self):
        if self.dbobject() is None: return None
        return Webanker(ptype=self.dbobject()._prefix, pid=self.getid(),pmodelid=self.dbobject().tabl_id)

    @staticmethod
    def indexlist(plang=None):
        members = [WebTable(pdbobj=obj) for obj in Table.select()]
        idxlist = Objlist(pmembers=members).indexlist(plang=plang)
        return idxlist
    # grouplist
# WebInterface
