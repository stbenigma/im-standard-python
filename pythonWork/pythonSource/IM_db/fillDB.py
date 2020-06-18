# -*- coding: latin-1 -*-
import transferModel
from IM_DB import dbConnect, parameters, logging


# Main Programm

def filldbmain():
    transferModel.loeschmodell()
    transferModel.insertBaseData()
    transferModel.transferODMModel();
# filldbmain

def main(p_param1):
    """Main program for fillDB"""
    parameters.initparam(p_callarg=p_param1)
    logging.initlog()

    dbConnect.openDB(parameters.dbFilePath(), fks='OFF')
    filldbmain()
    dbConnect.myDbConn.close()

    logging.logmessage("database {} for model {} filled with modeldata"
                       .format(parameters.dbFilePath(),
                               parameters.odmModelName()))
#  main

if __name__ == '__main__':
    import sys
    main(p_param1=sys.argv[1])
