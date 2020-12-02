import WEB_OBJECTS
from IM_OBJECTS import *

class WebModelelement(WEB_OBJECTS.BaseWebObj):
    __webobject = None

    def __init__(self,pdbobj):
        if isinstance(pdbobj,Entity):
            self.__webobject = WEB_OBJECTS.WebEntity(pdbobj=pdbobj)
        elif isinstance(pdbobj,Document):
            self.__webobject = WEB_OBJECTS.WebDocument(pdbobj=pdbobj)
        elif isinstance(pdbobj,Attribute):
            self.__webobject = WEB_OBJECTS.WebAttribute(pdbobj=pdbobj)
        elif isinstance(pdbobj, Table):
            self.__webobject = WEB_OBJECTS.WebTable(pdbobj=pdbobj)
        elif isinstance(pdbobj,Domain):
            self.__webobject = WEB_OBJECTS.WebDomain(pdbobj=pdbobj)
        elif isinstance(pdbobj, Interface):
            self.__webobject = WEB_OBJECTS.WebInterface(pdbobj=pdbobj)
        elif isinstance(pdbobj, Column):
            self.__webobject = None
        else:
            self.__webobject = None

    def webobject(self):
        return self.__webobject

    def getid(self):
        if self.webobject() is None: return None
        return self.webobject().getid()

    def getname(self,plang=None):
        if self.webobject() is None: return None
        return self.webobject().getname(plang=plang)

    def getqualifiedname(self,plang=None):
        if self.webobject() is None: return None
        return self.webobject().getqualifiedname(plang=plang)

    def webanker(self):
        if self.webobject() is None: return None
        return self.webobject().webanker()
#WebModelelement