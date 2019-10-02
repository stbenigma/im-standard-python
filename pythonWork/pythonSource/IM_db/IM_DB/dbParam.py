# -*- coding: latin-1 -*-
from IM_DB import dbLookup
""" definiert alle systemparameter für die DB """


dbName:str = ''
dbDirectory:str = ''
dbDefaultLang:str = 'de'
dbDefaultLangID:int = None

def initDBParam(pdbDirec, pdbName):
    global dbDirectory
    global dbName
    global dbDefaultLang

    dbDirectory = pdbDirec

    if pdbName == '':
        #nimm den Namen des einzigen .dmd-Files im IM-Directory
        pass
    else:
        dbName = pdbName
#end initDBParam

def liesDefaultLang():
    global dbDefaultLang
    global dbDefaultLangID
    dbDefaultLang = dbLookup.liesDefaultLang()
    dbDefaultLangID = dbLookup.spraLookup(dbDefaultLang)
    #print("defaultLang=" + dbDefaultLang + " " + str(dbDefaultLangID))
#liesDefaultLang