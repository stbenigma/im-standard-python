import sys

from SSOT_db import createnewDB
from SSOT_db.IM_JSON import *
from SSOT_db.IM_OBJECTS import *
from SSOT_db.SQL_INFRA import dbConnect

logger = logging.getLogger('mergedbs')
summary = logging.getLogger('mergedbs:summary')

SOURCE_SPOD: str = 'SPOD'  # default source for SPOD-internal updates

nofunc = lambda p: None
# json-key: (processorder,baseobjectload, referencesload,hasexternalref,tablename)
# table name is only allowed for entries with typcial json-ids (xxxxNNNN)
transferprocs = {
    'model': (1, proj2sql, nofunc, False, None),
    'languages': (2, langs2sql, nofunc, False, None),
    'physicalunits': (3, physicalunits2sql, nofunc, False, PhysicalUnit._tablename),
    'datatypes': (4, datatypes2sql, nofunc, True, Datatype._tablename),
    'storageformats': (5, storageformats2sql, nofunc, False, Storageformat._tablename),
    'documents': (6, documents2sql, nofunc, True, Document._tablename),
    'orgunits': (7, orgunits2sql, nofunc, True, OragnisationalUnit._tablename),
    'actorroles': (7, actorroles2sql, actorconcerns2sql, True, Actorrole._tablename),
    'categories': (7, entitycategory2sql, nofunc, False, EntityCategory._tablename),
    'userdefprops': (8, udps2sql, nofunc, False, Userdefprop._tablename),
    'datamodels': (10, datamodels2sql, nofunc, True, Datamodel._tablename),
    'domains': (12, domains2sql, nofunc, True, Domain._tablename),
    'entities': (14, entities2sql, nofunc, True, Entity._tablename),
    'attributes': (16, attributes2sql, nofunc, True, Attribute._tablename),
    'arcs': (18, arcs2sql, nofunc, True, Arc._tablename),
    'relations': (20, relations2sql, nofunc, True, Relation._tablename),
    'keys': (22, keys2sql, nofunc, True, Key._tablename),
    'mappings': (29, nofunc, nofunc, True, Mapping._tablename), #self.mapstoid
    'tables': (30, tables2sql, nofunc, True, Table._tablename),
    'columns': (32, columns2sql, nofunc, True, Column._tablename),
    'businessrules': (33, businessrules2sql, nofunc, True, BusinessRule._tablename),
    'diagrams': (34, diagrams2sql, nofunc, True, Diagram._tablename),
    '_imprint_': (99, nofunc, nofunc, True, None)
}


def mergejson2sql(pmodel:JSModel, psrcname=SOURCE_SPOD, pverbose=False, pcheckonly=False, pkeepids=False) -> Mergeresult:
    """
    merge json into current connection
        DB-Version has already been checked
        returns the Mergeresult

    :param pmodel: JSModel with jsonfile to merge
    :param psrcname:  Name of the source providing model-info
    :param pverbose:  True -> do more logging
    :param pcheckonly: True -> I am beeing called by a check. do not check to avoid recursion
    :param pkeepids: use identities (number part of ENTI[nnnn]) from JSON as db id
    :return:
    """
    if not pcheckonly:
        # make sure, the model is consistent with database
        # but not if I am called by the check
        assert checkjsonmodel(pmodel=pmodel, pverbose=pverbose)

    # here we need an open database
    assert dbConnect.isopenDB()

    result = Mergeresult(verbose=pverbose, checkonly=pcheckonly, srcname=psrcname)
    result.use_json_id = pkeepids
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
        for masterobject in sorted(transferprocs.keys(), key=lambda val: transferprocs[val][0], reverse=True):
            extref = transferprocs[masterobject][3]
            if extref:
                try:
                    # it is an element with external reference
                    cnt = Modelelement.deletenonreferenced(JSModel.label2elemtype(masterobject))
                    if cnt > 0:
                        logger.warning(f"Deleted {cnt} dangling elements of type {masterobject}")
                    result.adddelcnt(cnt, masterobject)
                except Exception as e:
                    logger.warning(f"Cannot delete elements", exc_info=e)
            else:
                # no external reference. Delete entry, if its key does not exist in the json-file
                # the table is mapped to a db-objects
                tablename = transferprocs[masterobject][4]
                if tablename in table2class:
                    jsonids = tuple(jsguid2id(key) for key in pmodel.getelements(masterobject).keys())
                    # cnt = table2class[tablename].deletemissingids(jsonids)
                    # result.adddelcnt(cnt, masterobject)
            # fi
        # for

    rev = pmodel.jsmodel['_imprint_']['git-revision']
    logger.info(f"Writing git revision {rev} to DB")
    dbConnect.write_git_reversion(rev, dbConnect.getdbcon())

    if not pcheckonly and (len(result.errors) == 0):
        """clean up and set final project parameters"""
        proj: Project = Project.select()[0]
        proj.proj_um, proj.proj_dm = psrcname, datetime.now()
        proj.proj_languages = ','.join([langs.lang_iso_code2 for langs in Language.select()])
        proj.updatedb(pdoerrhdlng=True)
    # fi

    return result

def mergejs2db(pdbfile: str, pmodel: JSModel, psrcname=SOURCE_SPOD,
               pverbose=False, pdryrun=False, pkeepids=False):
    """
    merge jsonfile into existing database

    :param pdbfile: filepath of existing database to merge into
    :param pmodel:  JSModel read from file to merge
    :param psrcname: Name of the source merging data into an existing SPOD
    :param pverbose: log more information
    :param pdryrun: do a merging into a clone, not changing the real database
    :param pkeepids: use identities (number part of ENTI[nnnn]) from JSON as db id
    :return:  jsonstructure generated from the updated database
    """
    retval = None
    dbConnect.openDB(pfilepath=pdbfile)
    if pdryrun:
        # create a backup in memory and connect to it
        dbConnect.connecttodbcopy()

    mergeresult = None
    try:
        newversion = pmodel.jsmodel['_imprint_']["Modelversion"]
        dbversion = dbConnect.getversion()
        #do not check version of newly created memory database
        if newversion != dbversion and dbConnect.getDBname()!="":
            logmessages.showmessages(
                f"""existing database  {pdbfile}\nhas version {dbversion} but should have {newversion}""")
            raise Exception(f"DB-Version mismatch: found {dbversion} instead of {newversion}")

        mergeresult = mergejson2sql(pmodel=pmodel, psrcname=psrcname, pverbose=pverbose, pkeepids=pkeepids)

        message = f"Errors {len(mergeresult.errors)}, Warnings {len(mergeresult.warnings)}, Changes {len(mergeresult.changes)}"
        print("Merge result: " + message)
        if len(mergeresult.errors) > 0:
            summary.error(message)
        elif len(mergeresult.warnings) > 0:
            summary.warning(message)
        else:
            summary.info(message)

        if len(mergeresult.errors) > 0:
            summary.warning(f"--- Errors ---- ")
        for dbe in mergeresult.errors:
            summary.error(str(dbe))

        if len(mergeresult.warnings) > 0:
            summary.warning(f"--- Warnings ---- ")
        for w in mergeresult.warnings:
            summary.warning(w)

        if len(mergeresult.changes) > 0:
            summary.debug(f"--- Changes ---- ")
        for c in mergeresult.changes:
            summary.debug(str(c))

        print(f"Errors {len(mergeresult.errors)},  Warnings {len(mergeresult.warnings)}")
        print(f"elements changed in database {dbConnect.getDBname()}")
        print(
            f"    {mergeresult.insertcnt} inserted, {mergeresult.updatecnt} updated, {mergeresult.deletecnt} deleted, {mergeresult.deleterefcnt} references removed")
        if pdryrun:
            logging.info(f"***** Database was not modified ****")
        # return json from merge anyway
        retval = JSModel(pmodel=sql2json(pdbname=dbConnect.getDBname()))

    finally:
        if dbConnect.isopenDB():
            dbConnect.closeDB()

    if mergeresult is not None:
        js_change_file = Path('log') / 'merge.json'
        try:
            js_change_file.parent.mkdir(exist_ok=True)
            logger.debug("Writing change log to '%s'", str(js_change_file))
            mergeresult.write_json(js_change_file)
        except:
            pass  # logging darf nicht abstürzen

    return retval


def checkjsonfile(pjsonfilepath, pverbose=False) -> bool:
    logger.info(f"check jsonfile {pjsonfilepath}")
    return checkjsonmodel(pmodel=JSModel.readfromfile(pjsonfilepath), pverbose=pverbose)

def jsonviadbtojson(pmodel:JSModel,psrcname,pcheckonly=False,pverbose=False)->dict:
    """loads a jsonfile into an empty DB and creates a json file out of it.
        Thus filling all denormalized fields properly"""
    createnewDB(pdbfilepath=None)
    mergeresult = mergejson2sql(pmodel=pmodel, psrcname=psrcname, pverbose=pverbose,
                                pcheckonly=pcheckonly, pkeepids=False)
    mergeresult.consistencyerrors = checkdatabase()
    retval= sql2json(pdbname=dbConnect.getDBname())
    dbConnect.closeDB()
    return retval

def checkjsonmodel(pmodel:JSModel, pverbose=False) -> bool:
    """
    checks a json for consistency
        it is entered in an empty database and merged into it.
        This will show consistency and constraint errors
    :param pmodel: JSModel to be checked
    :param pverbose:  log more information
    :return:  True -> model could be inserted into database
            False-> errors detected
    """
    imprint = pmodel.jsmodel['_imprint_']
    modelname = pmodel.modelname()
    baselang = pmodel.modellanguage()
    languages = list(pmodel.jsmodel['languages'].keys())

    # create db in Memory with languages from the json file
    # save the old DB
    dbConnect.push()
    try:
        createnewDB(pdbfilepath=None)
        mergeresult = mergejson2sql(pmodel=pmodel, psrcname="CHECKJSON", pverbose=pverbose,
                                    pcheckonly=True, pkeepids=False)
        mergeresult.consistencyerrors = checkdatabase()

        logging.info(f"model {modelname}")
        logging.info(
            f"created: {imprint['created']}    Modelversion; {imprint['Modelversion']}       git-revision {imprint['git-revision']}")
        logging.info(f"Baselanguage: {baselang}  Languages: {languages}")
        logging.info(f"Errors {len(mergeresult.errors)+len(mergeresult.consistencyerrors)},  Warnings {len(mergeresult.warnings)}")
        logging.info(
            f"          {mergeresult.insertcnt} inserted, {mergeresult.updatecnt} updated, {mergeresult.deletecnt} deleted, {mergeresult.deleterefcnt} references removed")

        for dbe in mergeresult.errors:
            logger.error(dbe)
        for dbe in mergeresult.consistencyerrors:
            logger.error(dbe)
        for w in mergeresult.warnings:
            logger.warning(w)
    finally:
        dbConnect.pop()
    return (len(mergeresult.errors) + len(mergeresult.consistencyerrors)) == 0


if __name__ == '__main__':
    model = JSModel.readfromfile(pfilename=sys.argv[2])
    mergejs2db(pdbfile=sys.argv[1], pmodel=model,pverbose=True)
