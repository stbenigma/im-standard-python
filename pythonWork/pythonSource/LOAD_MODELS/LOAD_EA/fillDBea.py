# -*- coding: latin-1 -*-
from SSOT_infra import logmessages,parameter
from LOAD_MODELS.LOAD_EA import transferEAModel21, transferEAModelNative
from SSOT_db import createJSON
from LOAD_MODELS.LOAD_ODM import fillDB


def filldbmain(callarg, pinputfile, ptransffunc):
    fillDB.fillmergedb (pdbfilepath=callarg
                       , transferfunction=ptransffunc
                       , pinputfile=pinputfile)


def main(p_param1, pxmlfile,ptransffuncversion):
    """Main program for fillDBea"""
    parameters.initparam(modelname = '???')
    logmessages.initlog('fillDBea',plogfilepath='?')
    assert ptransffuncversion in ('2.1','native')\
        ,f"{ptransffuncversion} is unsupported version for load file from EA. ('2.1','native')"

    try:
        if ptransffuncversion == 'native':
            transffunc = transferEAModelNative.transferEAModel
        else:
            transffunc = transferEAModel21.transferEAModel
        #fi
        filldbmain(callarg=p_param1, pinputfile=pxmlfile,ptransffunc=transffunc, createnewdb=True)
        # not createDB.existsDB(parameters.dbFilePath()))
        filename = parameter.modelName()
        filepath = parameter.dbDirect()
        createJSON.createJSON(pdbfilepath=parameter.dbFilePath(), pmodelname=parameter.modelName(),
                              pjsfilepath=filepath, pjsfilename=filename)
    finally:
        logmessages.showmessages("database {} for model {} filled with modeldata {} and json file generated"
                                 .format(parameter.dbFilePath()
                                         , pxmlfile
                                         , parameter.modelName()))
    return


if __name__ == '__main__':
    import sys

    param1=sys.argv[1] if len(sys.argv)>1 else None
    xmlfile=sys.argv[2] if len(sys.argv)>2 else None
    transffuncversion=sys.argv[3] if len(sys.argv)>3 else "2.1"
    main(p_param1=param1, pxmlfile=xmlfile,ptransffuncversion=transffuncversion)
