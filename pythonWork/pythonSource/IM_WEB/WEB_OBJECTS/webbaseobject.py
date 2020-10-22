from mystring import nvl

class Webanker:
    """enthält die Information um Web-Referenzen (Sprungziele / id) herzustellen.
         Webanker bestehen aus dem Kurznamen (prefix) des Elementes, seinem ID sowie ggf.
         dem Modelid (der dann in einen html-Dateinamen umgesetzt wird.
         Modelid =0 -> logisches Modell
    """
    def __init__(self,ptype,pid,pmodelid=0):
        self._id:int = pid
        self._type:str = ptype.upper()
        self._modelid:int = pmodelid
    def anker(self):
        return nvl(self._type) + str(nvl(self._id))
    def modelid(self):
        return self._modelid
#Webanker

class Objlist:
    def __init__(self,pmembers):
        #list of DB-elements making up the list
        self.__members = pmembers

    def getmembers(self):
        return self.__members

    def indexlist(self,plang=None):
        #I sort by the displayed, qualified name in the list, which is the first element in the sublists
        idxlist = [[member.getqualifiedname(plang), member.webanker(), member.getid()] for member in self.getmembers()]
        idxlist.sort()
        return idxlist
#Objlist

class BaseWebObj:
    __dbobject = None

    def __init__(self,pobjtype,pid=None,pdbobj=None):
        if (pid is not None or pdbobj is not None):
            self.setdbobject(pdbobj if pdbobj is not None else self.readbobject(pid))
        self.__objtype = pobjtype

    def dbobject(self):
        return self.__dbobject

    def setdbobject(self, pdbobj):
        self.__dbobject = pdbobj

    def readbobject(self,pid):
        self.setdbobject(self.__objtype.getbyid(pid))

    def getid(self):
        return self.dbobject().getid()

    def getname(self,plang=None):
        return self.dbobject().getname(plang=plang)

    """mit Präfix (Tabelle) oder in Klammern (Entität)
       falls Typ nicht überschreibt nimm einfach den Namen"""
    def getqualifiedname(self,plang=None):
        return self.getname(plang=plang)

    def webanker(self):
        if self.dbobject() is None: return None
        return Webanker(ptype=self.dbobject()._prefix, pid=self.getid())
#BaseWebObj