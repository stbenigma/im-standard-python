from SSOT_db.IM_JSON import *
from SSOT_db.IM_OBJECTS import *
from SSOT_db.SQL_INFRA import dbConnect

nofunc = lambda p: None
# json-key: (processorder,baseobjectload, referencesload,hasexternalref)
transferprocs = {
    'model': (1, proj2sql, nofunc, False)
    , 'languages': (2, langs2sql, nofunc, False)
    , 'physicalunits': (3, physicalunits2sql, nofunc, False)
    , 'datatypes': (4, datatypes2sql, nofunc, True)
    , 'storageformats': (5, storageformats2sql, nofunc, False)
    , 'documents': (6, documents2sql, nofunc, True)
    , 'orgunits': (7, orgunits2sql, nofunc, True)
    , 'actorroles': (7, actorroles2sql, actorconcerns2sql, True)
    , 'categories': (7, entitycategory2sql, nofunc, True)
    , 'userdefprops': (8, udps2sql, nofunc, False)
    , 'systems': (10, systems2sql, nofunc, True)
    , 'domains': (12, domains2sql, nofunc, True)
    , 'entities': (14, entities2sql, nofunc, True)
    , 'attributes': (16, attributes2sql, nofunc, True)
    , 'arcs': (18, arcs2sql, nofunc, True)
    , 'relations': (20, relations2sql, nofunc, True)
    , 'keys': (22, keys2sql, nofunc, True)
    , 'tables': (30, tables2sql, nofunc, True)
    , 'columns': (32, columns2sql, nofunc, True)
    , 'businessrules': (33, businessrules2sql, nofunc, True)
    , 'diagrams': (34, diagrams2sql, nofunc, True)
    , '_imprint_': (99, nofunc, nofunc, True)
}

""" merge json into current connection
    DB-Version has already been checked
    returns the Mergeresult
    """


def mergejson2sql(pmodeljson, psrcname=Externalref.SOURCE_SPOD, pverbose=False):
    assert dbConnect.isopenDB()
    result = Mergeresult(verbose=pverbose)
    for masterobject in sorted(transferprocs.keys(), key=lambda val: transferprocs[val][0]):
        js2sql = transferprocs[masterobject][1]
        if js2sql != nofunc:
            extref = transferprocs[masterobject][3]
            js2sql(presult=result, podmjson=pmodeljson, pwithextsrcref=extref)
        # fi
    # for

    """Do dependency inserts where you need all Elements of a type (like actor_roles)"""
    for masterobject in sorted(transferprocs.keys(), key=lambda val: transferprocs[val][0]):
        js2refsql = transferprocs[masterobject][2]
        if js2refsql != nofunc:
            js2refsql(presult=result, podmjson=pmodeljson)
        # fi
    # for

    if (len(result.errors) == 0):
        """clean up and set final project parameters"""
        Language.deleteunused()
        proj: Project = Project.select()[0]
        proj.proj_um, proj.proj_dm = Baseobject.defaultCreator, datetime.today()
        proj.proj_languages = ','.join([langs.lang_iso_code2 for langs in Language.select()])
        proj.updatedb(pdoerrhdlng=True)
    # fi
    return result


"""merge jsonfile into existing database
    and return the jsonfile generated from the updated database
"""


def connecttodbcopy():
    assert dbConnect.isopenDB()
    # get a copy of a db in Memory and open it
    memconn = dbConnect.connectmemorydb()
    dbConnect.getdbcon().backup(memconn)
    dbConnect.closeDB()
    dbConnect.setdbcon(memconn)
    assert dbConnect.isopenDB()
    return dbConnect.getdbcon()

def mergejs2db(pdbfile: str, pmodel: JSModel, psrcname=Externalref.SOURCE_SPOD,
               pverbose=False, pdryrun=False):
    dbConnect.openDB(pfilepath=pdbfile)
    if pdryrun:
        #create a backup in memory and connect to it
        connecttodbcopy()

    retval = None
    try:
        if pdryrun:
            print (f"***** dry merge-run on db {pdbfile}")
            print (f"***** Database will not be modified ****")
        newversion = pmodel.jsmodel['_imprint_']["Modelversion"]
        dbversion = dbConnect.getversion()
        if newversion != dbversion:
            logmessages.showmessages(
                f"""existing database  {pdbfile}\nhas version {dbversion} but should have {newversion}""")
            raise Exception(f"DB-Version mismatch: found {dbversion} instead of {newversion}")

        mergeresult = mergejson2sql(pmodeljson=pmodel, psrcname=psrcname, pverbose=pverbose)
        if pverbose and len(mergeresult.changes) > 0:
            for c in mergeresult.changes:
                print(c)
        if (len(mergeresult.errors) > 0):
            for dbe in mergeresult.errors:
                print(dbe)
        print("{} Errors {},  Warnings {}".format(
            '' if (len(mergeresult.errors) + len(mergeresult.warnings) == 0) else '*******'
            , len(mergeresult.errors), len(mergeresult.warnings)))
        print(f"elements changed in database {dbConnect.getDBname()}")
        print(
            f"          {mergeresult.insertcnt} inserted, {mergeresult.updatecnt} updated, {mergeresult.deletecnt} deleted, {mergeresult.deleterefcnt} references removed")
        for w in mergeresult.warnings:
            print(w)

        """generate json from merged DB"""
        retval = JSModel(pmodel=sql2json())
    finally:
        dbConnect.closeDB()
    return retval


if __name__ == '__main__':
    model = JSModel.readfromfile(pfilename=sys.argv[2])
    mergejs2db(pdbfile=sys.argv[1], pmodel=model)
