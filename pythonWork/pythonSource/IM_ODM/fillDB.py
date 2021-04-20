# -*- coding: latin-1 -*-
from IM_ODM import transferModel,mergedbs
from IM_DB import logmessages,dbErstelleTables
import IM_db
from IM_JSON import *

# Main Programm


def filldbmain(callarg, createnewdb=False):
    if createnewdb:
        IM_db.createDB(par1=callarg,pforcecreate=True)
        dbConnect.openDB(p_filepath=parameters.dbFilePath(), fks='ON');
    else:
        memoryfilepath = ":memory:"
        dbConnect.openDB(p_filepath=memoryfilepath,fks='ON')
        dbErstelleTables.erstelleInfra(parameters.sqlfilepath());
        transferModel.insertBaseData()
    #fi
    transferModel.transferODMModel();
    odmjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
    dbConnect.closeDB()

    odmjson.printmodel(pfilepath=parameters.dbDirect(), pfilename=parameters.odmModelName())
    if createnewdb:
        pass # new db does not need merge
    else:
        """merge created DB into existing one"""
        dbConnect.openDB(p_filepath=parameters.dbFilePath(),fks='ON');
        mergedbs.mergeodm2db(podmjson=odmjson)
        dbConnect.closeDB()
    #fi
    return

def main(p_param1):
    """Main program for fillDB"""
    parameters.initparam(p_callarg=p_param1)
    logmessages.initlog('fillDB')

    try:
        filldbmain(callarg=p_param1, createnewdb=not IM_db.existsDB(parameters.dbFilePath()))
    finally:
        logmessages.showmessages("database {} for model {} filled with modeldata and json file generated"
                                 .format(parameters.dbFilePath(),
                               parameters.odmModelName()))
#  main

if __name__ == '__main__':
    import sys
    main(p_param1=sys.argv[1])
