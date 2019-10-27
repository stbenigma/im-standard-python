# -*- coding: latin-1 -*-
from IM_DB import parameters,dbConnect,dbErstelleTables
import pathlib
import sys,os

# Main Programm

def main(par1):
    parameters.initparam(p_callarg=par1)

    print("createDB",  parameters.dbDirect(), parameters.odmModelName())
    #falls es das Verzeichnis für die DB nicht gibt erzeuge es
    if not os.path.isdir(parameters.dbDirect()):
        os.mkdir(parameters.dbDirect())
    dbConnect.openDB(parameters.dbFilePath(),'OFF');
    dbErstelleTables.erstelleInfra();

    dbConnect.myDbConn.close()
#end main

if __name__ == '__main__':
    par1 = sys.argv[1]
    main(par1)
