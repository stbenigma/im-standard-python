# -*- coding: latin-1 -*-
import os
import sys

from IM_DB import parameters, dbConnect, dbErstelleTables, logmessages


def main(par1):
    """Main program for createDB"""
    parameters.initparam(p_callarg=par1)
    logmessages.initlog('CreateDB')

    dbtype = 'sqlite'
    if dbtype == parameters.SQLITE:
        if os.path.exists(parameters.dbFilePath()):
            print ("********* {}-DB-File {} alreday exists, cannot create it".format(parameters.SQLITE,parameters.dbFilePath()))
            return
        """# falls es das Verzeichnis für die DB nicht gibt erzeuge es"""
        if not os.path.isdir(parameters.dbDirect()):
            os.mkdir(parameters.dbDirect())
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
    main(par1)
