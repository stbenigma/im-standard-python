# -*- coding: latin-1 -*-
from IM_ODM import odmParam
from IM_DB import dbParam,dbConnect,dbErstelleTables
import pathlib
import sys

# Main Programm

def main(argv):
    limDirec = argv[1] if (len(sys.argv) > 1) else None
    lModelName = argv[2] if (len(sys.argv) > 2) else None

    if limDirec is None:
        limDirec = pathlib.Path(__file__).parent.__str__()+'/'
        lModelName = 'emptyODM.db'
    #fi
    odmParam.initODMParam(pimDirec=limDirec, pmodelName=lModelName)

    dbParam.initDBParam(odmParam.imDirectory
                        , odmParam.imModelName + '.db');

    print("createDB",  dbParam.dbDirectory, dbParam.dbName)
    dbConnect.openDB(dbParam.dbDirectory, dbParam.dbName);
    dbErstelleTables.erstelleInfra();

    dbConnect.myDbConn.close()
#end main

if __name__ == '__main__':
    main(sys.argv)
