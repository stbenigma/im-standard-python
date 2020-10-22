from .webbaseobject import Webanker,BaseWebObj,Objlist
from IM_OBJECTS import  Document


class WebDocument(BaseWebObj):
    def __init__(self, pid=None, pdbobj:Document=None):
        super().__init__(pobjtype=WebDocument, pid=pid, pdbobj=pdbobj)

    def getname(self,plang=None):
        return self.dbobject().docu_name

    @staticmethod
    def indexlist(plang=None):
        members = [WebDocument(pdbobj=obj) for obj in Document.select()]
        return Objlist(pmembers=members).indexlist()
    #indexlist
#WebDocument