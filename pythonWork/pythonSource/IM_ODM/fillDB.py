# -*- coding: latin-1 -*-
from IM_ODM import transferModel,mergedbs
from IM_DB import logmessages,dbErstelleTables
import IM_db
from IM_JSON import *



# Main Programm

def filldbmain(pinmemory=False):
    if not pinmemory:
        dbConnect.openDB(parameters.dbFilePath(), fks='OFF')
        transferModel.loeschmodell()
        dbConnect.myDbConn.close()
        #print("filldbmain Constraints sollten auf ON stehen")
        dbConnect.openDB(parameters.dbFilePath(), fks='ON')
    #fi
    transferModel.insertBaseData()
    transferModel.transferODMModel();
    if not pinmemory: dbConnect.myDbConn.close()
# filldbmain


def filldbmain2(callarg,createnewdb=False):
    memoryfilepath = ":memory:"
    dbConnect.openDB(p_filepath=memoryfilepath,fks='ON');
    dbErstelleTables.erstelleInfra(parameters.sqlfilepath());
    transferModel.insertBaseData()
    transferModel.transferODMModel();
    odmjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
    dbConnect.closeDB()

    if createnewdb:
        IM_db.createDB(par1=callarg,pforcecreate=True)

    dbConnect.openDB(p_filepath=parameters.dbFilePath(),fks='ON');
    if createnewdb:
        transferModel.insertBaseData()
    mergedbs.mergeodm2db(podmjson=odmjson)
    dbConnect.closeDB()

def main(p_param1):
    """Main program for fillDB"""
    parameters.initparam(p_callarg=p_param1)
    logmessages.initlog('fillDB')

    try:
        filldbmain2(callarg=p_param1,createnewdb=not IM_db.existsDB(parameters.dbFilePath()))
    finally:
        logmessages.showmessages("database {} for model {} filled with modeldata"
                                 .format(parameters.dbFilePath(),
                               parameters.odmModelName()))
#  main

if __name__ == '__main__':
    import sys
    main(p_param1=sys.argv[1])
