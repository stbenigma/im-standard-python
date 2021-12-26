# -*- coding: latin-1 -*-
import os

from SSOT_infra import logmessages,parameters
from IM_ODM import transferModel, mergedbs
from IM_db.IM_JSON import  *
from SSOT_db import existsDB,createnewDB


def filldbmain(callarg, createnewdb=False):
    fillmergedb(callarg=callarg,createnewdb=createnewdb,transferfunction=transferModel.transferODMModel)

def fillmergedb(callarg,transferfunction, createnewdb=False,**kwargs):

    if createnewdb:
        createnewDB(pdbfilepath=callarg)
    else:
        createnewDB(pdbfilepath=None) #create in Memory
    #fi
    transferfunction(**kwargs)
    loadedjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
    dbConnect.closeDB()

    loadedjson.printmodel(pfilepath=parameters.dbDirect(), pfilename=parameters.modelName() + "_loaded")
    if createnewdb:
        loadedjson.printmodel(pfilepath=parameters.dbDirect(), pfilename=parameters.modelName())
    else:
        """merge created DB into existing one"""
        dbConnect.openDB(pfilepath=parameters.dbFilePath(), pfks='ON')

        newversion =loadedjson.jsmodel['_imprint_']["Modelversion"]
        if newversion != dbConnect.getversion():
            logmessages.showmessages("""existing database  {}\nhas version {} but should have {}"""
                                     .format(parameters.dbFilePath(), dbConnect.getversion()
                                             , newversion))
            raise Exception("DB-Version mismatch: found {} instead of {}".format(dbConnect.getversion()
                                             ,newversion))

        mergedbs.mergeodm2db(podmjson=loadedjson)
        """generate json from merged DB"""
        newjson = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))
        dbConnect.closeDB()
        newjson.printmodel(pfilepath=parameters.dbDirect(), pfilename=parameters.modelName())
    #fi
    return

def main(p_param1, create_base_folder=False):
    """Main program for fillDB"""
    parameters.initparam(p_callarg=p_param1)
    logmessages.initlog('fillDB')

    try:
        if create_base_folder:
            os.makedirs(os.path.split(parameters.dbFilePath())[0], exist_ok=True)
        filldbmain(callarg=parameters.dbFilePath(), createnewdb=not existsDB(parameters.dbFilePath()))
    except Exception as e:
        raise e # for debugging purposes (breaktpoint on exception)
    finally:
        logmessages.showmessages("database {} for model {} filled with modeldata and json file generated"
                                 .format(parameters.dbFilePath(),
                                         parameters.modelName()))
#  main

if __name__ == '__main__':
    import sys
    main(p_param1=sys.argv[1])
