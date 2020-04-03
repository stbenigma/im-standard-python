
from IM_OBJECTS import *
from IM_DB import parameters,dbConnect,dbDDL,dbDML,dbErstelleTables,dbInserts,dbLookup,dbParam
import sys

if (__name__ == '__main__'):
    parameters.initparam(p_callarg=sys.argv[1])
    dbConnect.openDB(p_filepath= parameters.dbFilePath());

#    ss = Sprache.select()
#    s = Sprache()
    ss = Tabelle.indexlist()
    t = Tabelle().getbyid(302)
    print(t.__dict__)
    print (Tabelle.mappingto(302))
#    for s in ss:
#        print (s)
#    print (baseobject.webanker(Tabelle,302).__dict__)
