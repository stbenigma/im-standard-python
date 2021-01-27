import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../IM_db')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from IM_DB import parameters, dbConnect, dbErstelleTables, logmessages
from IM_HTML import printHTML
from IM_ODM import fillDB,createJSON
import listWebdoku
import listmapping
from IM_JSON import sql2json,printJSON,JSModel
from IM_OBJECTS import Languagetext


def main(pdirec, plang,force = False):
    parameters.initparam(p_callarg=pdirec)
    if plang is None:
        Languagetext.reportLang(parameters.dbDefaultLang())
    else:
        Languagetext.reportLang(plang.lower())
    logmessages.initlog('AllIn1')


    dbConnect.openDB(p_filepath=":memory:",fks='ON');
    dbErstelleTables.erstelleInfra();
    fillDB.filldbmain(pinmemory=True)
    printHTML.setWebDirec(p_webdirec=None)
    jsmodel = JSModel(pmodel=sql2json(pmodelname=parameters.odmModelName(),pdbname=parameters.dbFilePath()))
    listWebdoku.listwebmain(plang=Languagetext.reportLang(),pmodel=jsmodel)
    createJSON.createJSON(pfilepath=parameters.dbDirect(),pfilename=parameters.odmModelName())
    jsmodel.printmodel(pfilepath=parameters.dbDirect(), pfilename=parameters.odmModelName())
    listmapping.writexls(pfilename=parameters.webDirec() + 'Mappingtables_' + parameters.odmModelName() + '.xlsx',pmodel=model,plang=Languagetext.reportLang())
    listmapping.writeintfxls(pfilepath=parameters.webDirec(),pmodel=model,plang=Languagetext.reportLang())


    logmessages.showmessages("model {}: created and filled database ({})\n   created json, webdocu and mapping excel"
                             .format(parameters.odmModelName(), parameters.dbFilePath()))


if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv) > 2) else None
    force = (len(sys.argv) > 3) and (sys.argv[3] == 'FORCE')
    main(pdirec=direc, plang=lang,pforceoverwrite=force)
