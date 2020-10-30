from .webbaseobject import Webanker,BaseWebObj,Objlist
from IM_OBJECTS import  Userdefprop,Attribute,Userdefpropvalue


class WebUdp(BaseWebObj):
    def __init__(self, pid=None, pdbobj: Userdefprop = None):
        super().__init__(pobjtype=Userdefprop, pid=pid, pdbobj=pdbobj)

    def getname(self, plang=None):
        return self.dbobject().getname(plang=plang)

    def webanker(self):
        if self.dbobject() is None: return None
        return Webanker(ptype=self.dbobject()._prefix, pid=self.getid())

    @staticmethod
    def groupwebanker(ptheme, pgroup):
        return Webanker(ptype=ptheme, pid='ALL' if pgroup=='*' else pgroup)

    @staticmethod
    def contentlist(ptheme,pgroup,pmeltname):
        udplist = Userdefprop.getudps(pmeltname=pmeltname,ptheme=ptheme,pgroup=None if pgroup=='*' else pgroup)

        return [WebUdp(pdbobj=udp) for udp in udplist]
    # contentlist

    @staticmethod
    def indexlist(ptheme=None,plang=None):
        groups = Userdefprop.grouplist(pudptheme=ptheme)
        """[(theme,group)]"""
        if (groups is None or len(groups)== 0): return None
        groups.insert(0, (ptheme,'*'))
        idxlist = [(group[1],WebUdp.groupwebanker(ptheme=ptheme,pgroup=group[1])
                    ,group[1]) for group in groups]
        return idxlist
    # indexlist

    @staticmethod
    def getattributes(ptheme,pgroup):
        attrs = Attribute.select(pwhere="""attr_id in (select udpv_mode_id
                                                        from udp_values
                                                        join user_defined_properties on udpr_id = udpv_udpr_id
                                                        where udpr_theme = '{}' and udpr_group like '{}')""".format(ptheme,'%' if pgroup=='*' else pgroup))
        webattrs = [WebAttribute(pdbobj=attr) for attr in attrs]
        return webattrs
    #getattriburtes

    @staticmethod
    def getvalues(ptheme,pgroup,pmodeid,pmeltype):
        return Userdefpropvalue.udpvalues(ptheme=ptheme,pgroup=pgroup,pmodeid=pmodeid,pmeltype=pmeltype)
#Webudp
from .webattribute import WebAttribute

