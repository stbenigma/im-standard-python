# -*- coding: latin-1 -*-
from IM_DB import parameters,dbConnect,dbErstelleTables,logging
import sys,os
import __main__

# Main Programm

def main(par1):
    parameters.initparam(p_callarg=par1)
    logging.initlog()

    #falls es das Verzeichnis für die DB nicht gibt erzeuge es
    if not os.path.isdir(parameters.dbDirect()):
        os.mkdir(parameters.dbDirect())
    dbConnect.openDB(parameters.dbFilePath(),'OFF');
    dbErstelleTables.erstelleInfra();
    dbConnect.myDbConn.close()
    print("{}:\n  => database {} for model {} created".format(__main__.__file__, parameters.dbFilePath(), parameters.odmModelName()))
    logging.logmessage()
#end main

if __name__ == '__main__':
    par1 = sys.argv[1]
    main(par1)
