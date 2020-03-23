# -*- coding: latin-1 -*-
from IM_DB import dbLookup
from  IM_OBJECTS import *
""" definiert alle systemparameter für die DB """


dbName:str = ''
dbDirectory:str = ''
dbDefaultLang:str = 'de'
dbDefaultLangID:int = None


def liesDefaultLang():
    global dbDefaultLang
    global dbDefaultLangID
    dbDefaultLang = sprache.liesDefaultLang()
    dbDefaultLangID = sprache.spraLookup(dbDefaultLang)
    #print("defaultLang=" + dbDefaultLang + " " + str(dbDefaultLangID))
#liesDefaultLang