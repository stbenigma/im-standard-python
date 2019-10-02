# -*- coding: latin-1 -*-
from IM_ODM import odmParam,transferModel
from IM_DB import dbParam,dbConnect,dbDDL,dbDML,dbErstelleTables
import sys


# Main Programm

def main():

    limDirec = sys.argv[1] if (len(sys.argv)>1) else None
    lModelName = sys.argv[2] if (len(sys.argv)>2) else None

    odmParam.initODMParam(pimDirec=limDirec,pmodelName=lModelName)

    dbParam.initDBParam(odmParam.imDirectory
                ,odmParam.imModelName+'.db');
#    print (dbParam.dbDirectory+dbParam.dbName)

    print ("fillDB",odmParam.imDirectory,odmParam.imModelName)
    dbConnect.openDB(dbParam.dbDirectory,dbParam.dbName);

    transferModel.insertBaseData()
    dbParam.liesDefaultLang()
    transferModel.transferODMModel();

    dbConnect.myDbConn.close()
#end main

if __name__ == '__main__':
    main()
