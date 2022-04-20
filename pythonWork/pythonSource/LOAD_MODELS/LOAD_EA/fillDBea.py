# -*- coding: latin-1 -*-
from SSOT_infra import logmessages,parameters
from LOAD_MODELS.LOAD_EA import transferEAModel21, transferEAModelNative
from IM_ODM import createJSON
from LOAD_MODELS.LOAD_ODM import fillDB


def filldbmain(callarg, pintputfile, ptransffunc):
    fillDB.fillmergedb(pdestination=callarg
                       , transferfunction=ptransffunc
                       , pinput=pintputfile)


def main(p_param1, pxmlfile,ptransffuncversion):
    """Main program for fillDBea"""
    parameters.initparam(pparamfile=p_param1)
    logmessages.initlog('fillDBea')
    assert ptransffuncversion in ('2.1','native')\
        ,f"{ptransffuncversion} is unsupported version for load file from EA. ('2.1','native')"

    try:
        if ptransffuncversion == 'native':
            transffunc = transferEAModelNative.transferEAModel
        else:
            transffunc = transferEAModel21.transferEAModel
        #fi
        filldbmain(callarg=p_param1, pintputfile=pxmlfile,ptransffunc=transffunc, createnewdb=True)
        # not createDB.existsDB(parameters.dbFilePath()))
        filename = parameters.modelName()
        filepath = parameters.dbDirect()
        createJSON.createJSON(pdbfilepath=parameters.dbFilePath(),pmodelname=parameters.modelName(),
                              pjsfilepath=filepath, pjsfilename=filename)
    finally:
        logmessages.showmessages("database {} for model {} filled with modeldata {} and json file generated"
                                 .format(parameters.dbFilePath()
                                         , pxmlfile
                                         , parameters.modelName()))
    return


if __name__ == '__main__':
    import sys

    param1=sys.argv[1] if len(sys.argv)>1 else None
    xmlfile=sys.argv[2] if len(sys.argv)>2 else None
    transffuncversion=sys.argv[3] if len(sys.argv)>3 else "2.1"
    main(p_param1=param1, pxmlfile=xmlfile,ptransffuncversion=transffuncversion)
