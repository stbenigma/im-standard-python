from .webbaseobject import Webanker,BaseWebObj,Objlist
from IM_OBJECTS import  Entity
from .webattribute import WebAttribute



class WebEntity(BaseWebObj):
    __members = None

    def __init__(self,pid=None,pdbobj:Entity=None):
        super().__init__(pobjtype=Entity,pid=pid,pdbobj=pdbobj)
        self.enti_id = self.dbobject().enti_id
        self.enti_uc = self.dbobject().enti_uc
        self.enti_dc = self.dbobject().enti_dc

    def getname(self,plang):
        return self.dbobject().getname(plang=plang)
    def getdescr(self,plang):
        return self.dbobject().getdescr(plang=plang)

    def getnames(self):
        return self.dbobject().enti_name_L

    def getparents(self):
        entis = self.dbobject().getparents()
        return [] if (entis is None or len(entis) == 0) else [WebEntity(pdbobj=e) for e in entis]

    def getchildren(self,ptype=None):
        entis = self.dbobject().getchildren(ptype=ptype)
        return [] if (entis is None or len(entis) == 0) else [WebEntity(pdbobj=e) for e in entis]

    def getwebattributes(self):
        attrs = self.dbobject().getattributes()
        return [] if attrs is None else [WebAttribute(pdbobj=attr) for attr in attrs]

    def getkeylist(self,plang):
        keys = self.dbobject().getkeys()
        webkeys = []
        for k in keys:
            kelems = k.getkeyelements()
            attrs = []
            relas = []
            for kelem in kelems:
                if kelem.kele_attr_id is not None:
                    attrs.append(WebAttribute(pid=kelem.kele_attr_id).getname(plang=plang))
                if kelem.kele_rela_id is not None:
                    relas.append(WebRelation(pid=kelem.kele_rela_id).getname(plang=plang))
            webkeys.append((k.keys_name,', '.join(a for a in attrs),', '.join(r for r in relas)))
        return webkeys

    @staticmethod
    def contentlist(plang):
        if WebEntity.__members is None: WebEntity.__members = [WebEntity(pdbobj=obj) for obj in Entity.select()]
        return WebEntity.__members


    @staticmethod
    def indexlist(plang=None):
        return Objlist(pmembers=WebEntity.contentlist(plang)).indexlist(plang=plang)
    # grouplist
#WebEntity
from .webrelation import WebRelation


