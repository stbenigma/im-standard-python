# -*- coding: latin-1 -*-
from IM_ODM import odmParam,transferModel
from IM_DB import dbParam,dbConnect



# Main Programm

def main(p_imdirec=None, p_modelname=None):

    odmParam.initODMParam(pimDirec=p_imdirec, pmodelName=p_modelname)

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
    import sys
    main(p_imdirec=sys.argv[1] if (len(sys.argv) > 1) else None
        ,p_modelname=sys.argv[2] if (len(sys.argv) > 2) else None)
