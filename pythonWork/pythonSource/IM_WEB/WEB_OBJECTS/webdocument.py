from .webbaseobject import BaseWebObj,Objlist
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
    #grouplist

    @staticmethod
    def docureflist(pdocuid, plang):
        modes = Document().getbyid(pdocuid).getrefmodes()
        reflist = [] if modes is None else [[mode.mode_type
                                            ,Modelelemtype.getbyshortname(pshortname=mode.mode_type).melt_name
                                            ,WebModelelement(pdbobj=mode.getmyelement()).webobject()]
                                            for mode in modes]
        refentries = [Referenceentry(pid=None if entry[2] is None else entry[2].getid()
                                     ,pname=None if entry[2] is None else entry[2].getname(plang=plang)
                                     ,ptype=entry[0],ptypename=entry[1]
                                     ,panker=None if entry[2] is None else entry[2].webanker().anker()
                                     )
                      for entry in reflist]
        return refentries
        # datalist = [Referenceentry(pid=e[1], pname=e[0], ptype=e[2], ptypename=e[3]
        #     , panker=Entity().getbyid(e[1]).webanker()
        #     if e[2] == Modelelemtype.ENTI
        #     else Attribute().getbyid(e[1]).webanker() if e[2] == Modelelemtype.ATTR
        #     else Tabelle().getbyid(e[1]).webanker() if e[2] == Modelelemtype.TABL
        #     else Schnittstelle().getbyid(e[1]).webanker() if e[2] == Modelelemtype.INTF
        #     else ''
        #                            ) for e in data]
        # return datalist
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

    @staticmethod
    def doculist(plang=None):
        webdocus = [WebDocument(pdbobj=docu) for docu in Document.doculist()]
        return webdocus

#WebDocument
from .webmodelelement import WebModelelement
