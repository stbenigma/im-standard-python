# -*- coding: latin-1 -*-
from SSOT_infra import logmessages
from IM_EA import transferEAModel
from IM_ODM import fillDB, createJSON


def filldbmain(callarg, pintputfile, createnewdb=False):
    fillDB.fillmergedb(callarg=callarg, createnewdb=createnewdb
                       , transferfunction=transferEAModel.transferEAModel
                       , pinput=pintputfile)


def main(p_param1, pxmlfile):
    """Main program for fillDBea"""
    parameters.initparam(p_callarg=p_param1)
    logmessages.initlog('fillDBea')

    try:
        filldbmain(callarg=p_param1, pintputfile=pxmlfile, createnewdb=True)
        # not createDB.existsDB(parameters.dbFilePath()))
        filename = parameters.modelName()
        filepath = parameters.dbDirect()
        createJSON.createJSON(pfilepath=filepath, pfilename=filename)
    finally:
        logmessages.showmessages("database {} for model {} filled with modeldata {} and json file generated"
                                 .format(parameters.dbFilePath()
                                         , pxmlfile
                                         , parameters.modelName()))
    #  main


if __name__ == '__main__':
    import sys

    main(p_param1=sys.argv[1], pxmlfile=sys.argv[2])
