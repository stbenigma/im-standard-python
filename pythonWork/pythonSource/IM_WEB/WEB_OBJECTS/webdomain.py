from .webbaseobject import Webanker,BaseWebObj,Objlist
from IM_OBJECTS import  Domain,DomaingroupMember

class WebDomain(BaseWebObj):
    def __init__(self, pid=None, pdbobj:Domain=None):
        super().__init__(pobjtype=Domain, pid=pid, pdbobj=pdbobj)
        self.doma_id = self.dbobject().doma_id

    """Domainname (Anzahl Refs) """
    def getqualifiedname(self, plang=None):
            return '{} ({})'.format(
                self.getname(plang=plang), self.dbobject().refattrcnt()+self.dbobject().refcolucnt())
    def getname(self,plang=None):
        return self.dbobject().getname(plang=plang)

    @staticmethod
    def indexlist(porigin,pdomaid=None,plang=None):
        if pdomaid is None:
            where = "doma_origin = '{}'".format(porigin)
        else:
            where = """doma_origin = '{}' and doma_id in (select dgrm_doma_id_group 
                                                        from domaingroup_members 
                                                        where dgrm_doma_id_member = {})"""\
                .format(porigin,pdomaid)
        members = [WebDomain(pdbobj=obj) for obj in Domain.select(pwhere=where)]
        return Objlist(pmembers=members).indexlist(plang=plang)
    # grouplist

    def dgrmelements(self):
        dgrmelements = [WebDomainMember(pdbobj=dgrm) for dgrm in DomaingroupMember.select(pwhere="dgrm_doma_id_group = {}".format(self.doma_id))]
        return dgrmelements
    # wbgrelements
#WebDomain

class WebDomainMember(BaseWebObj):
    def __init__(self, pid=None, pdbobj:DomaingroupMember=None):
        super().__init__(pobjtype=DomaingroupMember, pid=pid, pdbobj=pdbobj)
        self.webdomain = WebDomain(pid=self.dbobject().dgrm_doma_id_member)

    """Domainname (Anzahl Refs) """
    def getqualifiedname(self, plang=None):
            return '{}.{})'.format(self.webdomain.getname(plang=plang),self.getname(plang=plang))

    def getname(self,plang=None):
        return self.dbobject().getname(plang=plang)
#WebDomainMember


