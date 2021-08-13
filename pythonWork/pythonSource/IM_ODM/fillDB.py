# -*- coding: latin-1 -*-
from IM_DB import logmessages,dbCreateStructure
from IM_ODM import transferModel,mergedbs,createJSON
from IM_JSON import *
import createDB

def filldbmain(callarg, createnewdb=False):
    fillmergedb(callarg=callarg,createnewdb=createnewdb,transferfunction=transferModel.transferODMModel)

def fillmergedb(callarg,transferfunction, createnewdb=False,**kwargs):
    if createnewdb:
        createDB.createDB(par1=callarg,pforcecreate=True)
        dbConnect.openDB(pfilepath=parameters.dbFilePath(), pfks='ON');
    else:
        memoryfilepath = ":memory:"
        dbConnect.openDB(pfilepath=memoryfilepath, pfks='ON')
        dbCreateStructure.applysqlscript(parameters.sqlfilepath());
        dbConnect.setversion() #newly created view in infra
        transferModel.insertBaseData()
    #fi
    transferfunction(**kwargs)
    loadedjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
    debugeloadntis=Entity.select(pwhere="enti_id in (464,383,381)")
    debugeloadrelas=Relation.select(pwhere="rela_id in (496,540,543,505,499)")
    dbConnect.closeDB()

    loadedjson.printmodel(pfilepath=parameters.dbDirect(), pfilename=parameters.modelName()+"_loaded")
    if createnewdb:
        loadedjson.printmodel(pfilepath=parameters.dbDirect(), pfilename=parameters.modelName())
    else:
        """merge created DB into existing one"""
        dbConnect.openDB(pfilepath=parameters.dbFilePath(), pfks='ON');
        debugenewtis = Entity.select(pwhere="enti_id in (464,383,381)")
        debugenewrelas = Relation.select(pwhere="rela_id in (496,540,543,505,499)")

        newversion =loadedjson.jsmodel['_imprint_']["Modelversion"]
        if newversion != dbConnect.getversion():
            logmessages.showmessages("""existing database  {}\nhas version {} but should have {}"""
                                     .format(parameters.dbFilePath(),dbConnect.getversion()
                                             ,newversion))
            raise Exception("DB-Version mismatch: found {} instead of {}".format(dbConnect.getversion()
                                             ,newversion))

        mergedbs.mergeodm2db(podmjson=loadedjson)
        """generate json from merged DB"""
        newjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
        dbConnect.closeDB()
        newjson.printmodel(pfilepath=parameters.dbDirect(), pfilename=parameters.modelName())
    #fi
    return

def main(p_param1):
    """Main program for fillDB"""
    parameters.initparam(p_callarg=p_param1)
    logmessages.initlog('fillDB')

    try:
        filldbmain(callarg=p_param1, createnewdb=not createDB.existsDB(parameters.dbFilePath()))
        filename = parameters.modelName()
        filepath = parameters.dbDirect()
        createJSON.createJSON(pfilepath=filepath, pfilename=filename)
    finally:
        logmessages.showmessages("database {} for model {} filled with modeldata and json file generated"
                                 .format(parameters.dbFilePath(),
                               parameters.modelName()))
#  main

if __name__ == '__main__':
    import sys
    main(p_param1=sys.argv[1])
