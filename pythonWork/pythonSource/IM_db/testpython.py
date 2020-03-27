
from IM_OBJECTS import *
from IM_DB import parameters,dbConnect,dbDDL,dbDML,dbErstelleTables,dbInserts,dbLookup,dbParam
import sys

if (__name__ == '__main__'):
    parameters.initparam(p_callarg=sys.argv[1])
    dbConnect.openDB(p_filepath= parameters.dbFilePath());

#    ss = Sprache.select()
#    s = Sprache()
    ss = tabelle.indexlist()
    print (baseobject.webanker(Tabelle,235).__dict__)
    for s in ss:
        print (s)
