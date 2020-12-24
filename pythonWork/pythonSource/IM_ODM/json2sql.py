# -*- coding: latin-1 -*-
import json
import sqlite3
import sys
from datetime import date

from IM_DB import dbConnect, dbErstelleTables
from IM_OBJECTS import *
from IM_ODM import transferModel
from IM_JSON import *

errcnt: int = 0
warncnt: int = 0
modellang: str = None

anker = lambda n, i: None if i is None else n + str(i)
ankerid = lambda a: None if a is None else a[4:]




def error(pmsg, pelem=None):
    global errcnt
    if type(pmsg) in (sqlite3.IntegrityError, sqlite3.DatabaseError, sqlite3.DataError, sqlite3.Error):
        errtype = 'DB-'
    else:
        errtype = ''

    print("***{}ERROR: {}".format(errtype, pmsg))
    if pelem is not None: print("     ", pelem)
    errcnt += 1
    raise Exception("error")


# error

def warning(pmsg):
    global warncnt
    print("WARNING: {}".format(pmsg))
    warncnt += 1

def insudp(pmodeid,pudps):
    if pudps is None: return
    """ "userdefprop": {
            "-file-": {
                "-group-": {
                    "PENTA TabName": null
                },
            },
        },
    """
    for file,jtheme in pudps.items():
        for group,judps in jtheme.items():
            for udpname,udpval in judps.items():
                udpv = Userdefpropvalue(pmodeid=pmodeid,pudprid=Userdefprop.getbyname(udpname),pvalue=udpval)
                try:
                    udpv.insert()
                except Exception as err:
                    error(pmsg=err, pelem=udpv.tostring())
            #for
        #for
    #for

nofunc = lambda p : None
#json-key: (baseobjectload, referencesload)
transferprocs = {
 'model': (1,proj2sql,nofunc)
,'languages': (2,langs2sql,nofunc)
,'physicalunits' : (3,physicalunits2sql,phyurefs2sql)
,'datatypes' : (4,datatypes2sql,dtayrefs2sql)
,'storageformats' : (5,storageformats2sql,stforefs2sql)
,'documents': (6,documents2sql, docurefs2sql)
,'orgunits': (7,orgunits2sql, orgurefs2sql)
,'userdefprop': (8,udps2sql, udprefs2sql)
,'entities': (10,entities2sql,entirefs2sql)
,'domains': (11,domains2sql, domarefs2sql)
,'attributes': (12,attributes2sql, attrrefs2sql)
,'arcs': (13,arcs2sql, arcsref2sql)
,'relations': (14,relations2sql, relarefs2sql)
,'keys': (15,keys2sql, keysrefs2sql)
,'systems': (20,systems2sql, systrefs2sql)
,'tables': (21,tables2sql, tablrefs2sql)
,'columns': (22,columns2sql, colurefs2sql)
,'diagrams': (30,diagrams2sql, diagrefs2sql)
}

def fillsql(pmodel):
    for eletyp in pmodel.jsmodel.keys():
        if not (eletyp in transferprocs.keys()):
            warning('Unknown elementtype "{}" ignored'.format(eletyp))

    for eletyp in sorted(transferprocs.keys(),key=lambda val:transferprocs[val][0]):
        transferprocs[eletyp][1](pmodel)

    """now that all base objects are installed, transfer relationships"""
    for eletyp in sorted(transferprocs.keys(),key=lambda val:transferprocs[val][0]):
        transferprocs[eletyp][2](pmodel)

    for err in pmodel.errors(): print (err)
    print("==== {} error(s) found ====".format(str(pmodel.errcnt())))
    for warn in pmodel.warnings(): print (warn)
    print("==== {} warning(s) found ====".format(str(pmodel.wrncnt())))
# fillsql


# Main Programm
def main(pjsonin, pdbout):
    jsmodel = JSModel.readfromfile(pfilename=pjsonin)

    if pdbout is None:
        dbConnect.openDB(p_filepath=":memory:",fks='ON');
    else:
        dbConnect.openDB(pdbout, 'ON');

    dbErstelleTables.erstelleInfra();
    transferModel.insertBaseData(pwithlangs=False)

    try:
        fillsql(pmodel=jsmodel)
    finally:
        print("JSON file {} filled into db {}"
              .format(pjsonin, "in-memory" if pdbout is None else pdbout))

    #Test output
    if True:
        controljson = sql2json(pmodelname=jsmodel.jsmodel['model']['name'])
        printJSON(pmodel=controljson, pfilename='checkjson', pfilepath='/Users/stb/Downloads/')

    dbConnect.closeDB()
# main


if __name__ == '__main__':
    main(pjsonin=sys.argv[1],
         pdbout=None if len(sys.argv) <= 2 else sys.argv[2])
