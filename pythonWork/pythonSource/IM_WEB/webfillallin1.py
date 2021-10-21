import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../IM_db')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../tools')
from IM_DB import parameters, dbConnect, logmessages
from IM_HTML import printHTML
from IM_ODM import fillDB
import listWebdoku
from IM_JSON import sql2json,JSModel
from IM_OBJECTS import Languagetext
from createDB import existsDB
from tools import createMapExcel,createAllMapping


def main(pdirec, plang,pforceoverwrite = False):
    parameters.initparam(p_callarg=pdirec)
    if plang is None:
        Languagetext.reportLang(parameters.dbDefaultLang())
    else:
        Languagetext.reportLang(plang.lower())
    logmessages.initlog('AllIn1')



    os.makedirs(parameters.webDirec(),exist_ok=True)
    os.makedirs(parameters.dbDirect(),exist_ok=True)

    fillDB.filldbmain(callarg=pdirec, createnewdb=not existsDB(parameters.dbFilePath()))

    dbConnect.openDB(parameters.dbFilePath(), pfks='ON')
    #jsmodel = JSModel(pmodel=sql2json(pdbname=parameters.dbFilePath()))
    jsmodel = JSModel.readfromfile(parameters.dbDirect()+parameters.modelName()+".json")
    printHTML.setmodel(jsmodel)
    printHTML.setWebDirec(p_webdirec=None)

    listWebdoku.listwebmain(plang=Languagetext.reportLang())
    #jsmodel.printmodel(pfilepath=parameters.dbDirect(),pfilename=parameters.modelName())
    dbConnect.closeDB()

    createAllMapping(pjsonfile=parameters.dbDirect() + parameters.modelName() + '.json',plang=Languagetext.reportLang())
    createMapExcel(pjsonfile=parameters.dbDirect()+ parameters.modelName() + '.json')


    logmessages.showmessages("model {}: created and filled database ({})\n   created json, webdocu and mapping excel"
                             .format(parameters.modelName(), parameters.dbFilePath()))


if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv) > 2) else None
    force = (len(sys.argv) > 3) and (sys.argv[3] == 'FORCE')
    main(pdirec=direc, plang=lang)
