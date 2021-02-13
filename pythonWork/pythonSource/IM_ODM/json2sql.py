# -*- coding: latin-1 -*-
import sqlite3
import sys

from IM_DB import dbConnect, dbErstelleTables,parameters
from IM_JSON import *
from IM_ODM import transferModel

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
,'userdefprops': (8,udps2sql, udprefs2sql)
,'entities': (10,entities2sql,entirefs2sql)
,'systems': (11,systems2sql, systrefs2sql)
,'domains': (12,domains2sql, domarefs2sql)
,'attributes': (13,attributes2sql, attrrefs2sql)
,'arcs': (14,arcs2sql, arcsref2sql)
,'relations': (15,relations2sql, relarefs2sql)
,'keys': (16,keys2sql, keysrefs2sql)
,'tables': (21,tables2sql, tablrefs2sql)
,'columns': (22,columns2sql, colurefs2sql)
,'diagrams': (30,diagrams2sql, diagrefs2sql)
,'_imprint_':(99,nofunc,nofunc)
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

    dbErstelleTables.erstelleInfra(parameters.sqlfilepath());
    transferModel.insertBaseData(pwithlangs=False)

    try:
        fillsql(pmodel=jsmodel)
    finally:
        print("JSON file {} filled into db {}"
              .format(pjsonin, "in-memory" if pdbout is None else pdbout))

    #Test output
    if True:
        controljson = JSModel(pmodel=sql2json(pmodelname=jsmodel.jsmodel['model']['name'],pdbname=dbConnect.getDBname()))
        controljson.printmodel(pfilename='checkjson', pfilepath='/Users/stb/Downloads/')
        print ('/Users/stb/Downloads/checkjson.json created')

        del controljson.jsmodel['_imprint_']
        del jsmodel.jsmodel['_imprint_']
        del controljson.jsmodel['diagrams']
        del jsmodel.jsmodel['diagrams']
        for t in transferprocs.keys():
            if not t in jsmodel.jsmodel: continue
            for id,enti in jsmodel.jsmodel[t].items():
                c = controljson.jsmodel[t][id]
                if enti != c:
                    print (enti)
                    print (c)


        if controljson.jsmodel == jsmodel.jsmodel:
            print("==== input file {} identical to generated file {} ===="
                .format(pjsonin,'/Users/stb/Downloads/checkjson.json'))
        else:
            print("==== input file {} differs from generated file {} ===="
                .format(pjsonin,'/Users/stb/Downloads/checkjson.json'))

    dbConnect.closeDB()
# main


if __name__ == '__main__':
    main(pjsonin=sys.argv[1],
         pdbout=None if len(sys.argv) <= 2 else sys.argv[2])
