from .webbaseobject import Webanker,BaseWebObj,Objlist
from IM_OBJECTS import  *


class Referenceentry:
    def __init__(self,pid,pname,ptype,ptypename,pdirect=True,panker=None):
        self.name = pname
        self.anker = panker
        self.elemtype = ptype
        self.typename = ptypename
        self.elemid = pid
        self.direct = pdirect
#Rererenceentry

class WebDocument(BaseWebObj):
    def __init__(self, pid=None, pdbobj:Document=None):
        super().__init__(pobjtype=Document, pid=pid, pdbobj=pdbobj)

    def getname(self,plang=None):
        return self.dbobject().docu_name

    @staticmethod
    def indexlist(plang=None):
        members = [WebDocument(pdbobj=obj) for obj in Document.select()]
        return Objlist(pmembers=members).indexlist()
    #indexlist

    @staticmethod
    def docureflist(pdocuid, plang):
        modes = Modelelement.select(pwhere="mode_id in (select modo_mode_id from mode_docu where modo_docu_id = {})".format(pdocuid))
        reflist = [] if modes is None else [mode.getmyelement() for mode in modes]
        refentries = [Referenceentry(pid=entry.getid(),pname=entry.getname(plang=plang)
                                     ,ptype=entry._prefix,ptypename=Modelelemtype.getbyshortname(pshortname=entry._prefix)
                                     )
                      for entry in reflist]
        print (refentries)
        return
        datalist = [Referenceentry(pid=e[1], pname=e[0], ptype=e[2], ptypename=e[3]
            , panker=Entity().getbyid(e[1]).webanker()
            if e[2] == Modelelemtype.ENTI
            else Attribute().getbyid(e[1]).webanker() if e[2] == Modelelemtype.ATTR
            else Tabelle().getbyid(e[1]).webanker() if e[2] == Modelelemtype.TABL
            else Schnittstelle().getbyid(e[1]).webanker() if e[2] == Modelelemtype.INTF
            else ''
                                   ) for e in data]
        return datalist
    # docureflist

    @staticmethod
    def refdokulist(pid):
        docus = Document.getrefdoculist(pid=pid)
        typename = Modelelemtype.getbyshortname(Modelelemtype.DOCU).getname()
        datalist = []
        for doc in docus:
            webdocu = WebDocument(pid=doc[0])
            datalist.append(Referenceentry(pid=doc[0], pname=webdocu.getname(), ptype=Modelelemtype.DOCU, ptypename=typename
                                   , pdirect=Boolean.str2bool(doc[1])
                                   , panker=webdocu.webanker().anker()))

        return datalist
    # refdokulist
#WebDocument