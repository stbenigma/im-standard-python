import os
from pathlib import Path

from SSOT_infra import Parameter, nvl

"""  Collection of all parameters used for HTML generation
"""


class HTMLParameter(Parameter):
    # definitions by foryouandyourcustomers for ODM-defaults and enhancements

    WEBDEFAULTDIREC = 'Web'
    DATAMODELDIREC="datamodels"
    INFRADIREC="infra"
    IMAGEDEFAULTDIREC = 'images'
    JSSDEFAULTDIREC = 'js'
    JINJADEFAULTDIREC = 'jinjatemplates'
    CSDEFAULTDIREC = 'css'
    ICONEFAULTDIREC = 'icons'
    HTML = 'html'
    ASPX = 'aspx'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        this_direc = os.path.dirname(Path(__file__))
        self.libSourceDirec = os.path.join(this_direc, 'html-lib')
        assert os.path.exists(self.libSourceDirec), f"Unable to find {self.libSourceDirec}"

        self._webDirec = nvl(kwargs.get("webDirec")
                             ,os.path.join(super().baseDirec(),self.WEBDEFAULTDIREC))
        self._webFileName = nvl(kwargs.get("webFileName"),self.modelName())
        self._webFilePath = kwargs.get("webFilePath")
        self._webFileExtension = nvl(kwargs.get("webFileExtension"), self.HTML)
        self._imageDirec = nvl(kwargs.get("imageDirec"),
                               os.path.join(self.webDirec,self.INFRADIREC,self.IMAGEDEFAULTDIREC))
        self._cssDirec = nvl(kwargs.get("cssDirec"),
                             os.path.join(self.webDirec, self.INFRADIREC,self.CSDEFAULTDIREC))
        self._iconDirec = nvl(kwargs.get("iconDirec"),
                              os.path.join(self.webDirec, self.INFRADIREC,self.ICONEFAULTDIREC))
        self._jsDirec = nvl(kwargs.get("jsDirec"),
                            os.path.join(self.webDirec, self.INFRADIREC,self.JSSDEFAULTDIREC))
        self._jinjaDirec = nvl(kwargs.get("jinjaDirec"),
                               os.path.join(self.webDirec, self.INFRADIREC,self.JINJADEFAULTDIREC))
        self._singlefile = nvl(kwargs.get("singlefile"),True)
        self.webFileName = self.modelName()

        self.logofile = kwargs.get("logofile")
        return

    @property
    def webDirec(self):
        return self._webDirec

    @webDirec.setter
    def webDirec(self, newval):
        self._webDirec = Path(newval) if newval else None

    @property
    def imageDirec(self):
        return self._imageDirec
    @imageDirec.setter
    def imageDirec(self, newval):
        self._imageDirec = Path(newval) if newval else None

    @property
    def webFileName(self):
        return self._webFileName
    @webFileName.setter
    def webFileName(self, newval):
        self._webFileName = newval

    @property
    def webFilePath(self):
        return self._webFilePath
    @webFilePath.setter
    def webFilePath(self, newval):
        self._webFilePath = Path(newval)

    @property
    def webFileExtension(self):
        return self._webFileExtension

    @webFileExtension.setter
    def webFileExtension(self, newval):
        self._webFileExtension = newval

    @property
    def cssDirec(self):
        return self._cssDirec
    @cssDirec.setter
    def cssDirec(self, newval):
        self._cssDirec = Path(newval)

    @property
    def iconDirec(self):
        return self._iconDirec
    @iconDirec.setter
    def iconDirec(self, newval):
        self._iconDirec = Path(newval)

    @property
    def jsDirec(self):
        return self._jsDirec
    @jsDirec.setter
    def jsDirec(self, newval):
        self._jsDirec = Path(newval)

    @property
    def jinjaDirec(self):
        return self._jinjaDirec
    @jinjaDirec.setter
    def jinjaDirec(self, newval):
        self._jinjaDirec = Path(newval)

    @property
    def singlefile(self):
        return self._singlefile
    @singlefile.setter
    def singlefile(self, newval):
        self._singlefile = newval

    @property
    def logofile(self):
        return self._logofile

    @logofile.setter
    def logofile(self, newval):
        """ newval is None defaults to modelname
            return webDirec/imagedefaultdirec/newval. jpeg, jpg, png if it exists
            None otherwise
            """
        logofileextensions = ['jpeg', 'jpg', 'png', 'svg']
        logoname = newval if newval else self.modelName()
        retval = None
        for filetype in logofileextensions:
            logofile= os.path.join(self.IMAGEDEFAULTDIREC ,logoname , filetype)
            if os.path.isfile(logofile):
                retval = logofile
                break
        return retval
