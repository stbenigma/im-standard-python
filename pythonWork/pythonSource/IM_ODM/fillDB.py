# -*- coding: latin-1 -*-
import dbConnect
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
        dbConnect.setversion() #newly created view in infra
        transferModel.insertBaseData()
    #fi
    transferModel.transferODMModel();
    odmjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
    dbConnect.closeDB()

    odmjson.printmodel(pfilepath=parameters.dbDirect(), pfilename=parameters.odmModelName()+"_loadedfromodm")
    if createnewdb:
        pass # new db does not need merge print json
    else:
        """merge created DB into existing one"""
        dbConnect.openDB(p_filepath=parameters.dbFilePath(),fks='ON');
        newversion =odmjson.jsmodel['_imprint_']["Modelversion"]
        if newversion != dbConnect.getversion():
            logmessages.showmessages("""existing database  {}\nhas version {} but should have {}"""
                                     .format(parameters.dbFilePath(),dbConnect.getversion()
                                             ,newversion))
            raise Exception("DB-Version mismatch: found {} instead of {}".format(dbConnect.getversion()
                                             ,newversion))

        mergedbs.mergeodm2db(podmjson=odmjson)
        """generate json from merged DB"""
        odmjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
        dbConnect.closeDB()
    #fi
    #print current db as json file
    odmjson.printmodel(pfilepath=parameters.dbDirect(), pfilename=parameters.odmModelName())
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
