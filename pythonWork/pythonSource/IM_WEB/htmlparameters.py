import os

import path

from SSOT_infra import parameters

"""  Collection of all parameters used for HTML generation
"""


class HTMLParameter():

    # definitions from foryouandyourcustomers for ODM-defaults and enhancements

    def __init__(self, webdirec=None, imagedirec=None, logofile=None):
        self._webdirec = webdirec
        self._imagedirec = imagedirec
        self._logofile = logofile
        return

    def modelName(self):
        return parameters.modelName()

    def baseDirec(self):
        return parameters.baseDirec()

    def dbLanguages(self):
        return parameters.dbLanguages()

    def dbDefaultLang(self):
        return parameters.dbDefaultLang()

    @classmethod
    def webdefaultdirec(cls):
        return 'Web'

    @classmethod
    def imagedefaultdirec(cls):
        return 'images'

    def webdirec(self, newval=None):
        """ set webdirec if newval is not None
            return webdirec
            return basedirec/webdefaultdirec if None
            """
        if newval is None:
            retval = self._webdirec if self._webdirec is not None else os.path.join(self.baseDirec(),
                                                                                    self.webdefaultdirec())
        else:
            self._webdirec = path.Path(newval)
            retval = None
        return retval

    def imagedirec(self, newval=None):
        """ set imagedirec if newval is not None
            return imagedirec
            return webdirec/imagedefaultdirec if None
            """
        if newval is None:
            retval = self._imagedirec if self._imagedirec is not None else os.path.join(self.webdirec(),
                                                                                        self.imagedefaultdirec())
        else:
            self._imagedirec = path.Path(newval)
            retval = None
        return retval

    def logofile(self, newval=None):

        """ set logofile if newval is not None
            return logofile
            return webdirec/imagedefaultdirec/logo. jpeg, jpg, png is exists
            return webdirec/imagedefaultdirec/modelname. jpeg, jpg, png if exists
            """
        logofileextensions = ['jpeg', 'jpg', 'png', 'svg']
        if newval is None:
            if self._logofile is not None:
                retval = self._logofile
            else:
                for filetype in logofileextensions:
                    retval = os.path.join(self.imagedefaultdirec() / 'logo' / filetype)
                    if os.path.isfile(retval):
                        retval = None
                        break
                if retval is None:
                    for filetype in logofileextensions:
                        retval = os.path.join(self.imagedefaultdirec() / self.modelName() / filetype)
                        if os.path.isfile(retval):
                            retval = None
                            break
        else:
            self._logofile = path.Path(newval)
            retval = None
        return retval


# global getodmparams for ODM-fill
curhtmlparams: HTMLParameter = None


def sethtmlparams(htmlparam):
    global curhtmlparams
    curhtmlparams = htmlparam
    return


def gethtmlparams():
    global curhtmlparams
    return curhtmlparams
