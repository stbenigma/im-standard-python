# -*- coding: latin-1 -*-
import os
import sys

from IM_DB import parameters, dbConnect, dbErstelleTables, logmessages


def main(par1):
    """Main program for createDB"""
    parameters.initparam(p_callarg=par1)
    logmessages.initlog('CreateDB')

    # falls es das Verzeichnis für die DB nicht gibt erzeuge es
    if not os.path.isdir(parameters.dbDirect()):
        os.mkdir(parameters.dbDirect())
    dbConnect.openDB(parameters.dbFilePath(), 'OFF');
    dbErstelleTables.erstelleInfra();
    dbConnect.myDbConn.close()
    logmessages.showmessages("database {} for model {} created"
                             .format(parameters.dbFilePath()
                               , parameters.odmModelName())
                             )
# end main

if __name__ == '__main__':
    par1 = sys.argv[1]
    main(par1)
