from .webbaseobject import Webanker,BaseWebObj,Objlist
from IM_OBJECTS import  Diagram,Diagramtype


class WebDiagram(BaseWebObj):
    LEGENDWIDTH:int = 363
    LEGENDHEIGHT:int = 128
    DEFAULT_LINEWIDTH:int = 1
    ICONSIZE:int=40

    def __init__(self, pid=None, pdbobj: Diagram = None):
        super().__init__(pobjtype=Diagram, pid=pid, pdbobj=pdbobj)

    def getname(self, plang=None):
        return self.dbobject().diag_name

    def haslegend(self):
        return self.dbobject().diag_legendx is not None

    """Diagramname (entry type) """
    def getqualifiedname(self, plang=None):
            return '{} ({})'.format(self.dbobject().diag_name, Diagramtype().getbyid(pid=self.dbobject().diag_diat_id).diat_name)

    @staticmethod
    def contentlist(pentiid=None,plang=None):
        if pentiid is None:
            diags = Diagram.select(porderby="upper(diag_name)")
        else:
            diags = Diagram.getdiagrams(pmodeid=pentiid)
        # fi
        return [WebDiagram(pdbobj=diag) for diag in diags]
    # diaglist

    @staticmethod
    def indexlist(pentiid=None,plang=None):
        #order by in grouplist not yet resolved (diagramtype -> diagramnbame)
        #    porderby='(select diat_name from diagramtypes where diat_id = diag_diat_id),diag_name'
        members = WebDiagram.contentlist(pentiid=pentiid,plang=plang)
        return Objlist(pmembers=members).indexlist()
    # grouplist
#WebDiagram
