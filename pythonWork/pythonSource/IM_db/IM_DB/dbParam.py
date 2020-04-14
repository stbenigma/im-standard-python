# -*- coding: latin-1 -*-
from  IM_OBJECTS import *
""" definiert alle systemparameter für die DB """


dbName:str = ''
dbDirectory:str = ''
dbDefaultLang:str = 'de'
dbDefaultLangID:int = None


def liesdefaultlang():
    global dbDefaultLang
    global dbDefaultLangID
    dbDefaultLang = Sprache.liesdeflangiso2()
    dbDefaultLangID = Sprache.liesdeflangid()
    #print("defaultLang=" + dbDefaultLang + " " + str(dbDefaultLangID))
#liesdefaultlang