from SSOT_db.IM_JSON import *
from SSOT_db.IM_OBJECTS import *

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


def mergejson2db(pmodeljson: JSModel):
    assert dbConnect.isopenDB()
    result = Mergeresult()
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

    rev = pmodeljson.jsmodel['_imprint_']['git-revision']
    logging.info(f"Writing git revision {rev} to DB")
    dbConnect.write_git_reversion(rev, dbConnect.getdbcon())
    dbConnect.getdbcon().commit()

    if (len(result.errors) == 0):
        """clean up and set final project parameters"""
        Language.deleteunused()
        proj: Project = Project.select()[0]
        proj.proj_um, proj.proj_dm = Baseobject.defaultCreator, datetime.today()
        proj.proj_languages = ','.join([langs.lang_iso_code2 for langs in Language.select()])
        proj.updatedb(pdoerrhdlng=True)
    else:
        logging.warning("There where errors updating the database")
        for dbe in result.errors:
            print(dbe)
    # fi
    print("{}Errors {},  Warnings {}".format('' if (len(result.errors) + len(result.warnings) == 0) else '******* '
                                             , len(result.errors), len(result.warnings)))
    print(f"elements changed in database {dbConnect.getDBname()}")
    print(
        f"          {result.insertcnt} inserted, {result.updatecnt} updated, {result.deletecnt} deleted, {result.deleterefcnt} references removed")
    for w in result.warnings:
        print(w)
    return
