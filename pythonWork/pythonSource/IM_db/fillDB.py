# -*- coding: latin-1 -*-
from IM_ODM import odmParam,transferModel
from IM_DB import dbParam,dbConnect
from IM_DB import parameters



# Main Programm

def main(p_param1):
    parameters.initparam(p_callarg=p_param1)


    print ("fillDB",parameters.odmBaseDirec(),parameters.odmModelName())

    dbConnect.openDB(parameters.dbFilePath(),fks='OFF');
    transferModel.loeschmodell()
#    dbConnect.myDbConn.close()

#    dbConnect.openDB(parameters.dbFilePath(),fks='ON');
    transferModel.insertBaseData()
    dbParam.liesDefaultLang()
    transferModel.transferODMModel();

    dbConnect.myDbConn.close()
#end main

if __name__ == '__main__':
    import sys
    main(p_param1=sys.argv[1])
