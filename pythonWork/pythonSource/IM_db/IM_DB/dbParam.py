# -*- coding: latin-1 -*-

""" definiert alle systemparameter für die DB """


dbName:str = ''
dbDirectory:str = ''
dbDefaultLang:str = 'DE'

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