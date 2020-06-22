import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../IM_db')
from IM_DB import parameters,dbConnect, dbErstelleTables,logging
from IM_HTML import printHTML
import fillDB
import listWebdoku
import listmapping
from IM_OBJECTS import Sprachtext


def main(pdirec,plang):
    parameters.initparam(p_callarg=pdirec)
    if plang is None:
        Sprachtext.reportLang(parameters.dbDefaultLang())
    else:
        Sprachtext.reportLang(plang.lower())
    logging.initlog()

    dbConnect.openDB(p_filepath="file::memory:?cache=shared");
    dbErstelleTables.erstelleInfra();
    fillDB.filldbmain()
    printHTML.setWebDirec(p_webdirec=None)
    listWebdoku.listwebmain(plang=Sprachtext.reportLang())
    listmapping.filllists(plang=Sprachtext.reportLang())

    logging.logmessage("model {}: created and filled database ({})\n   created webdocu and mapping excel"
                   .format(parameters.odmModelName(),parameters.dbFilePath()))

#main

if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv)>2) else None
    main(pdirec=direc,plang=lang)