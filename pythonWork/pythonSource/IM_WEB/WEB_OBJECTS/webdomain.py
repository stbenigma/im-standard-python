from .webbaseobject import Webanker,BaseWebObj,Objlist
from IM_OBJECTS import  Domain

class WebDomain(BaseWebObj):
    def __init__(self, pid=None, pdbobj:Domain=None):
        super().__init__(pobjtype=WebDomain, pid=pid, pdbobj=pdbobj)

    """Domainname (Anzahl Refs) """
    def getqualifiedname(self, plang=None):
            return '{} ({})'.format(self.getname(plang=plang), self.dbobject().refattranz())

    @staticmethod
    def indexlist(porigin,plang=None):
        members = [WebDomain(pdbobj=obj) for obj in Domain.select(pwhere="doma_origin = '{}'".format(porigin))]
        return Objlist(pmembers=members).indexlist(plang=plang)
    # indexlist
#WebDomain
