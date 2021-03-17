from IM_JSON import *
from IM_OBJECTS import *
from datetime import datetime
from IM_DB import dbConnect
from dbDML import valuepairs2sqlexpr

nofunc = lambda p : None
#json-key: (processorder,baseobjectload, referencesload,hasexternalref)
transferprocs = {
 'model': (1,proj2sql,nofunc,False)
,'languages': (2,langs2sql,nofunc,False)
,'physicalunits' : (3,physicalunits2sql,nofunc,False)
,'datatypes' : (4,datatypes2sql,nofunc,True)
,'storageformats' : (5,storageformats2sql,nofunc,False)
,'documents': (6,documents2sql, nofunc,True)
,'orgunits': (7,orgunits2sql, nofunc,True)
,'userdefprops': (8,udps2sql, nofunc,False)
,'systems': (10,systems2sql, nofunc,True)
,'domains': (12,domains2sql, nofunc,True)
,'entities': (14,entities2sql,nofunc,True)
,'attributes': (16,attributes2sql, nofunc,True)
,'arcs': (18,arcs2sql, nofunc,True)
,'relations': (20,relations2sql, nofunc,True)
,'keys': (22,keys2sql, nofunc,True)
,'tables': (30,tables2sql, nofunc,True)
,'columns': (32,columns2sql, nofunc,True)
,'diagrams': (34,diagrams2sql, nofunc,True)
,'_imprint_':(99,nofunc,nofunc,True)
}

def mergeodm2db(podmjson):
    assert dbConnect.isopenDB()
    result = Mergeresult()
    for masterobject in sorted(transferprocs.keys(),key=lambda val:transferprocs[val][0]):
        js2sql = transferprocs[masterobject][1]
        if js2sql != nofunc:
            extref = transferprocs[masterobject][3]
            js2sql(presult=result, podmjson=podmjson, pwithextsrcref=extref)
        # fi
    #for

    """Do dependency inserts where you need all Elements of a type (like superentities)"""
    for masterobject in sorted(transferprocs.keys(), key=lambda val: transferprocs[val][0]):
        js2refsql = transferprocs[masterobject][2]
        if js2refsql != nofunc:
            js2refsql(presult=result, podmjson=podmjson)
        # fi
    # for

    if (len(result.errors) == 0):
        """clean up and set final projecte parameters"""
        Language.deleteunused()
        proj:Project = Project.select()[0]
        proj.proj_um,proj.proj_dm = Baseobject.defaultCreator,datetime.today()
        Project.proj_languages = ','.join([langs.lang_iso_code2 for langs in Language.select()])
        proj.updatedb(pdoerrhdlng=True)
    else:
        for dbe in result.errors:
            print (dbe)
    # fi
    print("{}Errors {},  Warnings {}".format('' if (len(result.errors)+len(result.warnings)==0) else '******* '
                                             ,len(result.errors),len(result.warnings)))
    print("elements changed in database {}".format(dbConnect.getDBname()))
    print ("          {} inserted, {} updated, {} deleted, {} references removed".format(result.insertcnt,result.updatecnt,result.deletecnt,result.deleterefcnt))
    for w in result.warnings:
        print (w)
    return
