import os
from pathlib import Path

from SSOT_infra import Parameter

"""  Collection of all parameters used for ODM-transfer to SPOD
"""

class ODMParameter(Parameter):

    # definitions from foryouandyourcustomers for ODM-defaults and enhancements

    #analyzed User defined property files
    ELEMDISPLAYFILENAME:str = 'elementdisplay' #UDP filename for elementdisplay information
    RACIFILENAME: str = 'RACI'  # UDP filename vor RACI-information
    TRANSLATIONFILENAME:str ='translation'
    GUIDPATTERN: str = '[A-Z0-9-]{20,45}'

    def __init__(self,imdirec=None,configdirec=None,**kwargs):
        super().__init__(**kwargs)
        self._imdirec = imdirec
        self._configdirec = configdirec
        self._dbDefaultLangID = None
        return

    @staticmethod
    def imdefaultdirec():
        return 'IM'

    @staticmethod
    def imextension():
        return '.dmd'

    @staticmethod
    def udpfileextension():
        return '.udposdm'

    @staticmethod
    def guidpattern():
        return ODMParameter.GUIDPATTERN

    def udpelemdisplfilepath(self):
        return self.odmfilesdirec() / (self.ELEMDISPLAYFILENAME + ODMParameter.udpfileextension())

    @staticmethod
    def udpelemdisplfilename():
        return ODMParameter.ELEMDISPLAYFILENAME

    def udpracifilepath(self):
        return self.odmfilesdirec() / (self.RACIFILENAME + ODMParameter.udpfileextension())

    @staticmethod
    def udpracifilename():
        return ODMParameter.RACIFILENAME

    def udptranslfilepath(self):
        return self.odmfilesdirec() / (self.TRANSLATIONFILENAME + ODMParameter.udpfileextension())

    @staticmethod
    def udptranslfilename():
        return ODMParameter.TRANSLATIONFILENAME

    def dbDefaultLangID(self,newval=None):
        if newval is None:
            retval = self._dbDefaultLangID
        else:
            self._dbDefaultLangId = newval
            retval = None
        return retval

    def imdirec(self, newval=None):
        """ set imdirec if newval is not None
            return imdirec
            return basedirec/imdefaultdirec if None
            """
        if newval is None:
            retval = self._imdirec if self._imdirec is not None else os.path.join(self.baseDirec(), ODMParameter.imdefaultdirec())
        else:
            self._imdirec = Path(newval)
            retval = None
        return retval

    """ return all path specific in ODM an relative to ODM-directory """

    def modelfilepath(self):
        return os.path.join(self.imdirec() , self.modelName() + ODMParameter.imextension())


    def odmspecificpath(self, *paths):
        retval = Path(os.path.join(self._imdirec, self.modelName(), *paths))
        return retval

    # the following are all relative to the imdirec
    def datatypesdirec(self):
        return self.odmspecificpath("datatypes")

    def structypesdirec(self):
        return self.datatypesdirec() / "structuredtype"

    def filesdirec(self):
        return self.odmspecificpath('files')

    def mappingdirec(self):
        return self.odmspecificpath('mapping')

    def domainsdirec(self):
        return self.odmspecificpath('domains')

    #logical subdirectory
    def entitydirec(self):
        return self.odmspecificpath('logical', 'entity')

    def relationdirec(self):
        return self.odmspecificpath('logical', 'relation')

    def logicalsubviewdirec(self):
        return self.odmspecificpath('logical', 'subviews')

    def arcdirec(self):
        return self.odmspecificpath('logical', 'arc')

    #business data subdirectory
    def businessinfodirec(self):
        return self.odmspecificpath('businessinfo')

    def documentdirec(self):
        return self.businessinfodirec() / 'document'

    def orgunitdirec(self):
        return self.businessinfodirec() /'party'

    def emaildirec(self):
        return self.businessinfodirec() /'email'

    def phonedirec(self):
        return self.businessinfodirec() /'phone'

    def contactdirec(self):
        return self.businessinfodirec() /'contact'

    #relational subdirectories
    def reldirec(self):
        return self.odmspecificpath('rel')

    def intfdirec(self,pintfdirec):
        return self.reldirec() / pintfdirec

    def tabledirec(self,pintfdirec):
        return self.intfdirec(pintfdirec) / 'table'

    def relsubviewsdirec(self,pintfdirec):
        return self.intfdirec(pintfdirec) / 'subviews'

    def fkdirec(self,pintfdirec):
        return self.intfdirec(pintfdirec) / 'foreignkey'

    """ special directories """
    def configpath(self,newval=None):
        if newval is not None:
            self._configdirec = Path(newval)
            retval = None
        elif self._configdirec is not None:
            retval = self._configdirec
        else:
            retval = self.imdirec() / 'Configuration'
            if not os.path.isdir(retval):
                retval = self.imdirec() / 'Konfiguration'
            assert os.path.isdir(retval), f"no configuration directory found in {self.imdirec()}"
        return retval

    def defdomainsfilpath(self):
        return self.configpath() / ODMParameter.defdomainsfilname()

    @staticmethod
    def defdomainsfilname():
        return 'defaultdomains.xml'

    def typesfile(self):
        return self.configpath() /'types.xml'

    def settingsfile(self):
        """settings can be in config or in ODM-directory"""
        dlsettingfilename = 'dl_settings.xml'
        filepath = self.odmspecificpath(dlsettingfilename)
        if not os.path.exists(filepath):
            filepath = os.path.join(self.configdirec(), dlsettingfilename)
        return filepath

#global getodmparams for ODM-fill
curodmparams:ODMParameter = None

def setodmparams(odmparam):
    global curodmparams
    curodmparams = odmparam
    return

def getodmparams():
    global curodmparams
    return curodmparams
