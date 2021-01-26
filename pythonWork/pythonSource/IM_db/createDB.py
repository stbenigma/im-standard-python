# -*- coding: latin-1 -*-
import os
import sys

from IM_DB import parameters, dbConnect, dbErstelleTables, logmessages


def createDB(par1,pforcecreate=False):
    """Main program for createDB"""
    parameters.initparam(p_callarg=par1)
    logmessages.initlog('CreateDB')

    dbtype = 'sqlite'
    if dbtype == parameters.SQLITE:
        if os.path.exists(parameters.dbFilePath()):
            if pforcecreate:
                os.remove(parameters.dbFilePath())
            else:
                print ("********* {}-DB-File {} alreday exists, cannot create it".format(parameters.SQLITE,parameters.dbFilePath()))
                return
            #fi
        elif not os.path.isdir(parameters.dbDirect()):
            """falls es das Verzeichnis für die DB nicht gibt erzeuge es"""
            os.mkdir(parameters.dbDirect())
        #fi
        dbConnect.openDB(parameters.dbFilePath(), 'OFF');
        sqlfile = parameters.sqlfilepath()
    #fi
    dbErstelleTables.erstelleInfra(psqlfilename=sqlfile);
    dbConnect.myDbConn.close()
    logmessages.showmessages("database {} for model {} created"
                             .format(parameters.dbFilePath()
                               , parameters.odmModelName())
                             )
# end main

if __name__ == '__main__':
    par1 = sys.argv[1]
    force = (len(sys.argv) > 2) and (sys.argv[2]== 'FORCE')
    createDB(par1,pforcecreate=force)
