# -*- coding: latin-1 -*-
from IM_DB import dbConnect,parameters,logging
from IM_OBJECTS import baseobject
import transferModel
import __main__



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
    logging.initlog()

    dbConnect.openDB(parameters.dbFilePath(),fks='OFF')
    filldbmain()
    dbConnect.myDbConn.close()

    print("{}:\n  => database {} for model {} filled with modeldata".format(__main__.__file__, parameters.dbFilePath(), parameters.odmModelName()))
    logging.logmessage()

#end main

if __name__ == '__main__':
    import sys
    main(p_param1=sys.argv[1])

