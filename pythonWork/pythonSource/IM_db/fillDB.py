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
    logging.initlog('fillDB')

    print("filldbmain Domains sollten auf ON stehen")
    dbConnect.openDB(parameters.dbFilePath(), fks='OFF')
    try:
        filldbmain()
        dbConnect.myDbConn.close()
    finally:
        logging.showmessages("database {} for model {} filled with modeldata"
                             .format(parameters.dbFilePath(),
                               parameters.odmModelName()))
#  main

if __name__ == '__main__':
    import sys
    main(p_param1=sys.argv[1])
