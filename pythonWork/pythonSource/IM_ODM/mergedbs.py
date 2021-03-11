from IM_JSON import *
from IM_OBJECTS import *
from datetime import datetime
from IM_DB import dbConnect
from dbDML import valuepairs2sqlexpr

nofunc = lambda p : None
#json-key: (processorder,baseobjectload, referencesload,js2obj,hasexternalref)
transferprocs = {
 'model': (1,proj2sql,nofunc,js2proj,False)
,'languages': (2,langs2sql,nofunc,js2lang,False)
,'physicalunits' : (3,physicalunits2sql,phyurefs2sql,js2phyu,False)
,'datatypes' : (4,datatypes2sql,dtayrefs2sql,js2daty,True)
,'storageformats' : (5,storageformats2sql,stforefs2sql,js2stfo,False)
,'documents': (6,documents2sql, docurefs2sql,js2docu,True)
,'orgunits': (7,orgunits2sql, orgurefs2sql,js2orgu,True)
,'userdefprops': (8,udps2sql, udprefs2sql,nofunc,True)
,'systems': (10,systems2sql, systrefs2sql,nofunc,True)
,'domains': (12,domains2sql, domarefs2sql,nofunc,True)
,'entities': (14,entities2sql,entirefs2sql,nofunc,True)
,'attributes': (16,attributes2sql, attrrefs2sql,nofunc,True)
,'arcs': (18,arcs2sql, arcsref2sql,nofunc,True)
,'relations': (20,relations2sql, relarefs2sql,nofunc,True)
,'keys': (22,keys2sql, keysrefs2sql,nofunc,True)
,'tables': (30,tables2sql, tablrefs2sql,nofunc,True)
,'columns': (32,columns2sql, colurefs2sql,nofunc,True)
,'diagrams': (34,diagrams2sql, diagrefs2sql,nofunc,True)
,'_imprint_':(99,nofunc,nofunc,nofunc,True)
}

def mergeodm2db(podmjson,pdbjson):
    assert dbConnect.isopenDB()
    result = Mergeresult()
    for masterobject in sorted(transferprocs.keys(),key=lambda val:transferprocs[val][0]):
        if masterobject not in ("languages","model","physicalunits","datatypes","storageformats","documents"): #or masterobject in ("_imprint_"):
            print (masterobject)
        else:
            objtype = JSModel.label2elemtype(masterobject)
            js2sql = transferprocs[masterobject][1]
            extref = transferprocs[masterobject][4]
            if js2sql != nofunc:
                js2sql(presult=result, podmjson=podmjson, pdbjson=pdbjson,pwithextsrcref=extref)
            #if masterobject not in ('model'):
            #    fromdb2odm(presult=presult, podmjson=podmjson, pdbjson=pdbjson, pelemtype=objtype, pjs2obj=js2obj,pwithextsrcref=extref)
        # fi
    #for
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
    print("elements changed in database {}".format(dbConnect.getDBname()))
    print ("          {} inserted, {} updated, {} deleted, {} references removed".format(result.insertcnt,result.updatecnt,result.deletecnt,result.deleterefcnt))
    for w in result.warnings:
        print (w)
    return
