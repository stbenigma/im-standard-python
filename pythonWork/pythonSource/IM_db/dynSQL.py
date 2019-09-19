from IM_ODM import odmParam,transferModel
from IM_DB import dbParam,dbConnect,dbDDL,dbDML,dbErstelleTables
from IM_DB import dbParam,dbConnect,dbDML

def main():
    odmParam.initODMParam()
    #    print (odmParam.imDirectory+odmParam.modelName)
    dbParam.initDBParam(odmParam.imDirectory
                        , odmParam.imModelName + '.db');
    dbConnect.openDB(dbParam.dbDirectory, dbParam.dbName);

    result = dbDML.select(
         """select * from entitaeten where enti_id = 9
                    """ )
    for row in result:
        print (row)
#main
#.format(entiId,entiId)
#where von.enti_id = {} or zu.enti_id = {}

if __name__ == '__main__':
    main()
