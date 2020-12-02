# -*- coding: latin-1 -*-
from IM_OBJECTS import Language
""" definiert alle systemparameter für die DB """


dbName:str = ''
dbDirectory:str = ''
dbDefaultLang:str = 'de'
dbDefaultLangID:int = None


def liesdefaultlang():
    global dbDefaultLang
    global dbDefaultLangID
    dbDefaultLang = Language.liesdeflangiso2()
    dbDefaultLangID = Language.liesdeflangid()
    #print("defaultLang=" + dbDefaultLang + " " + str(dbDefaultLangID))
#getdefaultlang