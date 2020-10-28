from .webbaseobject import Webanker,BaseWebObj,Objlist
from IM_OBJECTS import  Domain

class WebDomain(BaseWebObj):
    def __init__(self, pid=None, pdbobj:Domain=None):
        super().__init__(pobjtype=Domain, pid=pid, pdbobj=pdbobj)
        self.doma_id = self.dbobject().doma_id

    """Domainname (Anzahl Refs) """
    def getqualifiedname(self, plang=None):
            return '{} ({})'.format(
                self.getname(plang=plang), self.dbobject().refattranz())
    def getname(self,plang=None):
        self.dbobject().getname(plang=plang)

    @staticmethod
    def indexlist(porigin,pdomaid=None,plang=None):
        if pdomaid is None:
            where = "doma_origin = '{}'".format(porigin)
        else:
            where = """doma_origin = '{}' and doma_id in (select dgrm_doma_id_member 
                                                        from domaingroup_members 
                                                        where dgrm_doma_id_group = {})"""\
                .format(porigin,pdomaid)
        members = [WebDomain(pdbobj=obj) for obj in Domain.select(pwhere=where)]
        return Objlist(pmembers=members).indexlist(plang=plang)
    # indexlist
#WebDomain
