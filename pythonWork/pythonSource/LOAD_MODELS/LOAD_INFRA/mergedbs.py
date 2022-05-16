import logging

from SSOT_db.IM_JSON import *
from SSOT_db.IM_OBJECTS import *
from SSOT_db.SQL_INFRA import dbConnect
from SSOT_db import createnewDB
import sys

SOURCE_SPOD:str='SPOD' #default source for SPOD-internal updates

nofunc = lambda p: None
# json-key: (processorder,baseobjectload, referencesload,hasexternalref,tablename)
# table name is only allowed for entries with typcial json-ids (xxxxNNNN)
transferprocs = {
    'model': (1, proj2sql, nofunc, False,None)
    , 'languages': (2, langs2sql, nofunc, False,None)
    , 'physicalunits': (3, physicalunits2sql, nofunc, False,PhysicalUnit._tablename)
    , 'datatypes': (4, datatypes2sql, nofunc, True,Datatype._tablename)
    , 'storageformats': (5, storageformats2sql, nofunc, False,Storageformat._tablename)
    , 'documents': (6, documents2sql, nofunc, True,Document._tablename)
    , 'orgunits': (7, orgunits2sql, nofunc, True,OragnisationalUnit._tablename)
    , 'actorroles': (7, actorroles2sql, actorconcerns2sql, True,Actorrole._tablename)
    , 'categories': (7, entitycategory2sql, nofunc, False,EntityCategory._tablename)
    , 'userdefprops': (8, udps2sql, nofunc, False,Userdefprop._tablename)
    , 'systems': (10, systems2sql, nofunc, True,Interface._tablename)
    , 'domains': (12, domains2sql, nofunc, True,Domain._tablename)
    , 'entities': (14, entities2sql, nofunc, True,Entity._tablename)
    , 'attributes': (16, attributes2sql, nofunc, True,Attribute._tablename)
    , 'arcs': (18, arcs2sql, nofunc, True,Arc._tablename)
    , 'relations': (20, relations2sql, nofunc, True,Relation._tablename)
    , 'keys': (22, keys2sql, nofunc, True,Key._tablename)
    , 'tables': (30, tables2sql, nofunc, True,Table._tablename)
    , 'columns': (32, columns2sql, nofunc, True,Column._tablename)
    , 'businessrules': (33, businessrules2sql, nofunc, True,BusinessRule._tablename)
    , 'diagrams': (34, diagrams2sql, nofunc, True,Diagram._tablename)
    , '_imprint_': (99, nofunc, nofunc, True,None)
}

def mergejson2sql(pmodel, psrcname=SOURCE_SPOD, pverbose=False,pcheckonly=False) -> Mergeresult:
    """ merge json into current connection
        DB-Version has already been checked
        returns the Mergeresult
    """
    if not pcheckonly:
        #make sure, the model is consistent with database
        #but not if I am called by the check
        assert checkjsonmodel(pmodel=pmodel,pverbose=pverbose)

    #here we need an open database
    assert dbConnect.isopenDB()
    
    result = Mergeresult(verbose=pverbose,checkonly=pcheckonly,srcname=psrcname)
    for masterobject in sorted(transferprocs.keys(), key=lambda val: transferprocs[val][0]):
        js2sql = transferprocs[masterobject][1]
        if js2sql != nofunc:
            extref = transferprocs[masterobject][3]
            js2sql(presult=result, pjson=pmodel, pwithextsrcref=extref)
        # fi
    # for

    """Do dependency inserts where you need all Elements of a type (like actor_roles)"""
    for masterobject in sorted(transferprocs.keys(), key=lambda val: transferprocs[val][0]):
        js2refsql = transferprocs[masterobject][2]
        if js2refsql != nofunc:
            js2refsql(presult=result, pjson=pmodel)
        # fi
    # for

    # while checking, there is no delete
    if not pcheckonly:
        # delete in reversed order (because of possible references) all elements which are no longer relevant
        # cannot be done in fromjson2db because dependencies might exists
        for masterobject in sorted(transferprocs.keys(), key=lambda val: transferprocs[val][0],reverse=True):
            extref = transferprocs[masterobject][3]
            if extref:
                #it is an element with external reference
                cnt = Modelelement.deletenonreferenced(JSModel.label2elemtype(masterobject))
                result.adddelcnt(cnt,masterobject)
            else:
                #no external reference. Delete entry, if its key does not exist in the json-file
                #the table is mapped to a db-objects
                tablename = transferprocs[masterobject][4]
                if tablename in table2class:
                    jsonids = tuple(jsguid2id(key) for key in pmodel.getelements(masterobject).keys())
                    #cnt = table2class[tablename].deletemissingids(jsonids)
                    #result.adddelcnt(cnt, masterobject)
            #fi
        # for

    rev = pmodel.jsmodel['_imprint_']['git-revision']
    logging.info(f"Writing git revision {rev} to DB")
    dbConnect.write_git_reversion(rev, dbConnect.getdbcon())
    dbConnect.getdbcon().commit()

    if not pcheckonly and (len(result.errors) == 0):
        """clean up and set final project parameters"""
        Language.deleteunused()
        proj: Project = Project.select()[0]
        proj.proj_um, proj.proj_dm = psrcname, datetime.now()
        proj.proj_languages = ','.join([langs.lang_iso_code2 for langs in Language.select()])
        proj.updatedb(pdoerrhdlng=True)
    # fi
    return result

def connecttodbcopy():
    assert dbConnect.isopenDB()
    # get a copy of a db in Memory and open it
    memconn = dbConnect.connectmemorydb()
    dbConnect.getdbcon().backup(memconn)
    dbConnect.closeDB()
    dbConnect.makedbsafe(memconn)
    dbConnect.setdbcon(memconn)
    assert dbConnect.isopenDB()
    return dbConnect.getdbcon()


def mergejs2db(pdbfile: str, pmodel: JSModel, psrcname=SOURCE_SPOD,
               pverbose=False, pdryrun=False):
    """merge jsonfile into existing database
        and return the jsonfile generated from the updated database
    """

    dbConnect.openDB(pfilepath=pdbfile)
    if pdryrun:
        # create a backup in memory and connect to it
        connecttodbcopy()
        print(f"***** dry merge-run on db {pdbfile}")

    try:
        newversion = pmodel.jsmodel['_imprint_']["Modelversion"]
        dbversion = dbConnect.getversion()
        if newversion != dbversion:
            logmessages.showmessages(
                f"""existing database  {pdbfile}\nhas version {dbversion} but should have {newversion}""")
            raise Exception(f"DB-Version mismatch: found {dbversion} instead of {newversion}")

        mergeresult = mergejson2sql(pmodel=pmodel, psrcname=psrcname, pverbose=pverbose)
        if pverbose and len(mergeresult.changes) > 0:
            for c in mergeresult.changes:
                print(c)
        if (len(mergeresult.errors) > 0):
            for dbe in mergeresult.errors:
                print(dbe)
        for w in mergeresult.warnings:
            print(w)
        print(f"Errors {len(mergeresult.errors)},  Warnings {len(mergeresult.warnings)}")
        print(f"elements changed in database {dbConnect.getDBname()}")
        print(
            f"    {mergeresult.insertcnt} inserted, {mergeresult.updatecnt} updated, {mergeresult.deletecnt} deleted, {mergeresult.deleterefcnt} references removed")
        if pdryrun:
            print(f"***** Database was not modified ****")

    finally:
        if dbConnect.isopenDB():
            dbConnect.closeDB()
    return


def checkjsonfile(pjsonfilepath, pverbose=False)-> bool:
    logging.info(f"check jsonfile {pjsonfilepath}")
    return checkjsonmodel(pmodel=JSModel.readfromfile(pjsonfilepath),pverbose=pverbose)


def checkjsonmodel(pmodel, pverbose=False) -> bool:
    """ checks a json for consistency

        it is entered in a empty database and merged into it.
        This will show consistency and constraint errors
    """
    imprint = pmodel.jsmodel['_imprint_']
    modelname = pmodel.jsmodel['model']["name"]
    baselang = pmodel.jsmodel['model']["language"]
    languages = list(pmodel.jsmodel['languages'].keys())

    # create db in Memory with languages from the json file
    # save the old DB
    dbConnect.push()
    try:
        createnewDB(pdbfilepath=None, pbaselang=baselang, planguages=languages)
        mergeresult = mergejson2sql(pmodel=pmodel, psrcname="CHECKJSON", pverbose=pverbose,pcheckonly=True)
        logging.info(f"model {modelname}")
        logging.info(f"created: {imprint['created']}    Modelversion; {imprint['Modelversion']}       git-revision {imprint['git-revision']}")
        logging.info(f"Baselanguage: {baselang}  Languages: {languages}")
        logging.info(f"Errors {len(mergeresult.errors)},  Warnings {len(mergeresult.warnings)}")
        logging.info(
            f"          {mergeresult.insertcnt} inserted, {mergeresult.updatecnt} updated, {mergeresult.deletecnt} deleted, {mergeresult.deleterefcnt} references removed")

        for dbe in mergeresult.errors:
            logging.error(dbe)
        for w in mergeresult.warnings:
            logging.warning(w)
    finally:
        dbConnect.pop()
    return len(mergeresult.errors) == 0


if __name__ == '__main__':
    model = JSModel.readfromfile(pfilename=sys.argv[2])
    mergejs2db(pdbfile=sys.argv[1], pmodel=model)
