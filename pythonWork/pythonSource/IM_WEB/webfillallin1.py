import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../IM_db')
from IM_DB import parameters, dbConnect, dbErstelleTables, logmessages
from IM_HTML import printHTML
from IM_ODM import fillDB
import listWebdoku
import listmapping
from IM_OBJECTS import Languagetext


def main(pdirec, plang):
    parameters.initparam(p_callarg=pdirec)
    if plang is None:
        Languagetext.reportLang(parameters.dbDefaultLang())
    else:
        Languagetext.reportLang(plang.lower())
    logmessages.initlog('AllIn1')

    dbConnect.openDB(p_filepath="file::memory:?cache=shared");
    dbErstelleTables.erstelleInfra();
    fillDB.filldbmain()
    printHTML.setWebDirec(p_webdirec=None)
    listWebdoku.listwebmain(plang=Languagetext.reportLang())
    listmapping.filllists(plang=Languagetext.reportLang())

    logmessages.showmessages("model {}: created and filled database ({})\n   created webdocu and mapping excel"
                             .format(parameters.odmModelName(), parameters.dbFilePath()))



if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv) > 2) else None
    main(pdirec=direc, plang=lang)
