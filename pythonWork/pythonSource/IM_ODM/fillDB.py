# -*- coding: latin-1 -*-
from IM_ODM import transferModel
from IM_DB import dbConnect, parameters, logmessages


# Main Programm

def filldbmain():
    dbConnect.openDB(parameters.dbFilePath(), fks='OFF')
    transferModel.loeschmodell()
    dbConnect.myDbConn.close()
    #print("filldbmain Constraints sollten auf ON stehen")
    dbConnect.openDB(parameters.dbFilePath(), fks='ON')
    transferModel.insertBaseData()
    transferModel.transferODMModel();
    dbConnect.myDbConn.close()
# filldbmain

def main(p_param1):
    """Main program for fillDB"""
    parameters.initparam(p_callarg=p_param1)
    logmessages.initlog('fillDB')

    try:
        filldbmain()
    finally:
        logmessages.showmessages("database {} for model {} filled with modeldata"
                                 .format(parameters.dbFilePath(),
                               parameters.odmModelName()))
#  main

if __name__ == '__main__':
    import sys
    main(p_param1=sys.argv[1])
