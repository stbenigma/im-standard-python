import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../IM_db')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../tools')
from SSOT_db.SQL_INFRA import  dbConnect
from SSOT_infra import Parameter, logmessages
from IM_HTML import printHTML
from LOAD_MODELS.LOAD_ODM import fillDB
import listWebdoku
from SSOT_db.IM_JSON import  JSModel
from SSOT_db.IM_OBJECTS import  Languagetext
from SSOT_db.createDB import existsDB
from tools import createMapExcel,createAllMapping


def main(pdirec, plang,pforceoverwrite = False):
    parameters.initparam(basedirec=pdirec)
    if plang is None:
        Languagetext.reportLang(Parameter.DEFAULTLANG)
    else:
        Languagetext.reportLang(plang.lower())
    logmessages.initlog('AllIn1')

    os.makedirs(parameters.webDirec, exist_ok=True)
    os.makedirs(parameters.dbDirect(), exist_ok=True)

    fillDB.fillmergedb(pdbfilepath=parameters.dbFilePath(), pmodelname=parameters.modelName())

    dbConnect.openDB(parameters.dbFilePath())
    #mirojsmodel = JSModel(pmodel=sql2json(pdbname=parameters.dbFilePath()))
    jsmodel = JSModel.readfromfile(parameters.dbDirect() + parameters.modelName() + ".json")
    printHTMLmodel(jsmodel)
    printHTML.webDirec(p_webdirec=None)

    listWebdoku.listwebmain(plang=Languagetext.reportLang())
    #mirojsmodel.printmodel(pfilepath=parameters.dbDirect(),pfullfilename=parameters.modelName())
    dbConnect.closeDB()

    createAllMapping(pjsonfile=parameters.dbDirect() + parameters.modelName() + '.json', plang=Languagetext.reportLang())
    createMapExcel(pjsonfile=parameters.dbDirect() + parameters.modelName() + '.json')


    logmessages.showmessages("model {}: created and filled database ({})\n   created json, webdocu and mapping excel"
                             .format(parameters.modelName(), parameters.dbFilePath()))


if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv) > 2) else None
    force = (len(sys.argv) > 3) and (sys.argv[3] == 'FORCE')
    main(pdirec=direc, plang=lang)
