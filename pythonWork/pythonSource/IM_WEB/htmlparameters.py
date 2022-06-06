import os

import path
from pathlib import Path

from SSOT_infra import parameters

"""  Collection of all parameters used for HTML generation
"""


class HTMLParameter():

    # definitions by foryouandyourcustomers for ODM-defaults and enhancements

    WEBDEFAULTDIREC = 'Web'
    IMAGEDEFAULTDIREC= 'images'
    JSSDEFAULTDIREC= 'js'
    JINJADEFAULTDIREC= 'jinjatemplates'
    CSDEFAULTDIREC= 'css'
    ICONEFAULTDIREC= 'icons'

    def __init__(self, **kwargs):
        #should be in call to super once parameter is also a class
        self.modelName(kwargs.get("modelName"))
        self.baseDirec(kwargs.get("baseDirec"))
        self.dbLanguages(kwargs.get("dbLanguages"))
        self.dbDefaultLang(kwargs.get("dbDefaultLang"))

        this_direc = os.path.dirname(path.Path(__file__))
        self.libSourceDirec = os.path.join(this_direc, 'html-lib')
        assert os.path.exists(self.libSourceDirec), f"Unable to find {self.libSourceDirec}"

        self._webDirec = kwargs.get("webDirec")
        self._webFileName = kwargs.get("webFileName")
        self._webFileNamePath =kwargs.get("webFileNamePath")
        self._imageDirec = kwargs.get("imageDirec")
        self._cssDirec = kwargs.get("cssDirec")
        self._iconDirec = kwargs.get("iconDirec")
        self._jsDirec= kwargs.get("jsDirec")
        self._jinjaDirec= kwargs.get("jinjaDirec")
        self.webFileName = parameters.modelName()


        self._logofile = kwargs.get("logofile")


        return

    def modelName(self,newval=None):
        return parameters.modelName(newval)

    def baseDirec(self,newval=None):
        return parameters.baseDirec(newval)

    def dbDirec(self,newval=None):
        return parameters.dbDirect(newval)

    def dbLanguages(self,newval=None):
        return parameters.dbLanguages(newval)

    def dbDefaultLang(self,newval=None):
        return parameters.dbDefaultLang(newval)

    def webDirec(self, newval=None):
        """ set webDirec if newval is not None
            return webDirec
            return basedirec/webdefaultdirec if None
            """
        if newval is None:
            retval = self._webDirec if self._webDirec is not None else os.path.join(self.baseDirec(),
                                                                                    HTMLParameter.WEBDEFAULTDIREC)
        else:
            self._webDirec = path.Path(newval)
            retval = None
        return retval

    def imageDirec(self, newval=None):
        """ set imagedirec if newval is not None
            return imagedirec
            return webDirec/imagedefaultdirec if None
            """
        if newval is None:
            retval = self._imageDirec if self._imageDirec is not None else os.path.join(self.webDirec(),
                                                                                        HTMLParameter.IMAGEDEFAULTDIREC)
        else:
            self._imageDirec = path.Path(newval)
            retval = None
        return retval

    def webFileName(self, newval=None):
        if newval is None:
            retval = self._webFileName
        else:
            self._webFileName = path.Path(newval)
            retval = None
        return retval

    def webFileNamePath(self, newval=None):
        if newval is None:
            retval = self._webFileNamePath
        else:
            self._webFileNamePath = path.Path(newval)
            retval = None
        return retval

    def cssDirec(self, newval=None):
        if newval is None:
            retval = self._cssDirec if self._cssDirec is not None else os.path.join(self.webDirec(),
                                                                                        HTMLParameter.CSDEFAULTDIREC)
        else:
            self._cssDirec = path.Path(newval)
            retval = None
        return retval

    def iconDirec(self, newval=None):
        if newval is None:
            retval = self._iconDirec if self._iconDirec is not None else os.path.join(self.imageDirec(),
                                                                                        HTMLParameter.ICONEFAULTDIREC)
        else:
            self._iconDirec = path.Path(newval)
            retval = None
        return retval


    def jsDirec(self, newval=None):
        if newval is None:
            retval = self._jsDirec if self._jsDirec is not None else os.path.join(self.webDirec(),
                                                                                        HTMLParameter.JSSDEFAULTDIREC)
        else:
            self._jsDirec = path.Path(newval)
            retval = None
        return retval

    def jinjaDirec(self, newval=None):
        if newval is None:
            retval = self._jinjaDirec if self._jinjaDirec is not None else os.path.join(self.webDirec(),
                                                                                        HTMLParameter.JINJADEFAULTDIREC)
        else:
            self._jinjaDirec = path.Path(newval)
            retval = None
        return retval

    def logofile(self, newval=None):

        """ set logofile if newval is not None
            return logofile
            return webDirec/imagedefaultdirec/logo. jpeg, jpg, png is exists
            return webDirec/imagedefaultdirec/modelname. jpeg, jpg, png if exists
            """
        logofileextensions = ['jpeg', 'jpg', 'png', 'svg']
        if newval is None:
            if self._logofile is not None:
                retval = self._logofile
            else:
                for filetype in logofileextensions:
                    retval = os.path.join(self.imagedefaultdirec() / 'logo' / filetype)
                    if not os.path.isfile(retval):
                        retval = None
                        break
        else:
            self._logofile = path.Path(newval)
            retval = None
        return retval



