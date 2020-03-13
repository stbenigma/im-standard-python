# -*- coding: latin-1 -*-
from IM_DB import dbConnect,parameters
import transferModel


# Main Programm

def filldbmain():
    transferModel.loeschmodell()
    #    dbConnect.myDbConn.close()

    #    dbConnect.openDB(parameters.dbFilePath(),fks='ON');
    transferModel.insertBaseData()
    transferModel.transferODMModel();
#filldbmain

def main(p_param1):
    parameters.initparam(p_callarg=p_param1)


    print ("fillDB",parameters.odmBaseDirec(),parameters.odmModelName())

    dbConnect.openDB(parameters.dbFilePath(),fks='OFF')
    filldbmain()
    dbConnect.myDbConn.close()
#end main

if __name__ == '__main__':
    import sys
    main(p_param1=sys.argv[1])
