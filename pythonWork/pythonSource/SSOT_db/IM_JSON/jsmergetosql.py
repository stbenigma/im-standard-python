import logging
from copy import copy

from tqdm.autonotebook import tqdm

from SSOT_db.IM_JSON import *
from SSOT_db.IM_OBJECTS import *
from SSOT_infra import parameters
from SSOT_infra import todatetime

logger = logging.getLogger("jsmergetosql")

class Mergeresult:
    def __init__(self, srcname, verbose=False, checkonly=False):
        self.verbose = verbose
        self.insertcnt = 0
        self.insertstats = {}
        self.updatecnt = 0
        self.updatestats = {}
        self.deletecnt = 0
        self.deletestats = {}
        self.deleterefcnt = 0
        self.errors = []
        self.newerrors = []
        self.warnings = []
        self.changes = []
        self.srcname = srcname
        self.idTranslate = dict()
        self.use_json_id = False
        """{extjsid: keytrans,}  jsid MMMMxxxx (RELA1442)"""
        self.checkonly = checkonly
        self.failures = {}  # key: json element key, value: tuple(exception, message, json)

    def ischeckonly(self):
        return self.checkonly

    def istranslkey(self, extjsid):
        return (extjsid in self.idTranslate)

    def addfkey(self, extjsid, dbid):
        self.idTranslate[extjsid] = dbid

    def keytransl(self, extjsid):
        if extjsid in self.idTranslate:
            return self.idTranslate[extjsid]
        else:
            return 0

    def markdberror(self, perr, pelem):
        self.newerrors.append(f"""*** DB-Error {perr}\{pelem}""")
        return

    def markerror(self, pstr):
        self.newerrors.append(pstr)
        return

    def resetnewerrors(self):
        self.newerrors = []
        return

    def savenewerrors(self):
        self.errors += self.newerrors
        self.resetnewerrors()
        return

    def markwarning(self, pstr):
        self.warnings.append(pstr)
        return

    def addchange(self, pstr):
        if self.verbose:
            self.changes.append(pstr)
        return

    def adddelcnt(self, cnt, pstr=None):
        self.deletecnt += cnt
        if cnt > 0 and pstr is not None:
            self.addchange(pstr + f"  delete,cnt={str(cnt)}")
        return

    def addinscnt(self, cnt, pstr=None):
        self.insertcnt += cnt
        if cnt > 0 and pstr is not None:
            self.addchange(pstr + f"  insert,cnt={str(cnt)}")
        return

    def addupdcnt(self, cnt, pstr=None):
        self.updatecnt += cnt
        if cnt > 0 and pstr is not None:
            self.addchange(pstr + f"  update,cnt={str(cnt)}")
        return

    def adddelrefcnt(self, cnt, pstr=None):
        self.deleterefcnt += cnt
        if cnt > 0 and pstr is not None:
            self.addchange(pstr + f"  delete-refs,cnt={str(cnt)}")
        return

    def write_json(self, file):
        """Write the merge result to a json file"""
        with open(file, 'w') as out:
            json.dump(self._repr_json_(), out)

    def _repr_json_(self):
        return {
            'summary': {
                'inserted': self.insertcnt,
                'updated': self.updatecnt,
                'deleted': self.deletecnt,
                'errors': len(self.newerrors),
                'warnings': len(self.warnings),
            },
            'changeset': self.changes,
            'errors': self.newerrors,
            'warnings': self.warnings,
        }

    def __repr__(self):
        return f"c:{self.insertcnt}, u:{self.updatecnt}, d:{self.deletecnt}." \
               f" errors:{len(self.newerrors)}, warnings:{len(self.warnings)}"


def getallsrcrefs(pelemtype, psrcname):
    """ get all sourcerefs for an elementtype and a source"""
    retval = {extr.extr_source_id: extr.extr_id \
              for extr in Externalref.getallextrs(pelemtype=pelemtype, psrcname=psrcname)}
    return retval


def translatefks(presult: Mergeresult, pobj):
    """fkvalues {colname:[fktable,fkcolname,fkprefix]} all names in lowercase"""
    fkvalues = pobj.getfkcolumns()
    for colname, fk in fkvalues.items():
        if not (colname == pobj.getidcolname() and fk[2] == 'mode'):
            """fk from ID to mode_id is not handled
               translate id, if it is translated, assume, untranslatd id's are in form xxxx0000"""
            try:
                if presult.istranslkey(pobj.colvalue(pcolname=colname)):
                    pobj.setcolvalue(pcolname=colname, pvalue=presult.keytransl(pobj.colvalue(pcolname=colname)))
            except Exception as e:
                raise Exception(f"Failed to process foreign key '{fk} of column '{colname} on object {pobj}. Value: {pobj.colvalue(pcolname=colname)}") from e
    # for
    return


def getelemsrcrefs(psrcname, pkey, pelem):
    """ get all source refs of the element, if current sourcename is missing it is a insert, create it
        we assume, the elemnent requires a srcref
    """
    if 'sourceref' in pelem:
        srcrefs = pelem['sourceref']
    else:
        srcrefs = dict()
    if psrcname not in srcrefs:
        from datetime import datetime as dt
        srcrefs[psrcname] = [pkey, str(dt.now())]
    return srcrefs


def getelemsrcid(psrcrefs, psrcname):
    if psrcname in psrcrefs:
        retval = psrcrefs[psrcname][0]
    else:
        retval = None
    return retval


"""get the db entry with any of the external src refs
    if there is more than one id found raise an error, mixed srcrefs in the element
"""


def getbyanysrcref(presult, pelemsrcrefs):
    retval = None
    for name, ref in pelemsrcrefs.items():
        dbobj = Modelelement.getelementbyextref(psrcname=name, psrcid=ref[0])
        if dbobj is not None:
            return dbobj  ###TODO HOTFIX return first found Check problem of SPOD creating new id for same json entry
            if False and (retval is not None) and (dbobj.getid() != retval.getid()):
                raise Exception(
                    f"too many extrefs for source_id {ref[0]} and dbids {dbobj.getid()} and {retval.getid()}'")
            else:
                retval = dbobj
    return retval


def whoupdatedmeanwhile(psrcname, pjsonsrcrefs, pdbsrcrefs):
    retval = None
    for key, ref in pjsonsrcrefs.items():
        # don't check current source
        if key == psrcname:
            pass
        elif key in pdbsrcrefs:
            if todatetime(ref[1]) < todatetime(pdbsrcrefs[key][1]):
                # db younger than (means >) json => db updated after my checkout
                retval = key
                break
        else:
            # json has srcref (not current src), db doesn't -> db deleted record after I did my checkout, don't care
            pass
    return retval


def fromjson2db(presult: Mergeresult, pjson: JSModel, pelemtype, pjs2obj, pwithextsrcref=True, pequalexceptlist=[]):
    """from json-model to DB transfer
        mergecases for source A
        case    jsonob srcref   dbobj srcref
        json exported and changed by external source
        1       A,B,C           A,B,C         => find by A, update, update extref A
                                                  or merge error if updatetimestamp of B/C in db > B/C in json
        2       A,B,C           B,C           => find by B or C, update, insert extref A
                                                  or merge error if updatetimestamp of B/C in db > B/C in json
        3       A,B,C           A,B           => find A, update, update extref A
        5       A               missing entry => insert, insert extref A
        6       missing entry   B,C           => not handled
        7       missing entry   A,B,C         => delete extref A, delete element if it is last extref
        completely generated json out of modeler (ODM) last update in db for A is checkout-timestamp for ODM
        ODM overwrites all data which is not detectable as merge conflict.
        10       A               A,B,C         => find by A, update, update extref A
                                                   possible merge problem
        11       A               A             => find by A, update, update extref A
        12       A               B,C           => found by ukref
                                                    update, insert extref A
        13       A               A',B,C        => found by ukref,
                                                   update, replace extref A
        13       A                             => not found by ukref
                                                   inset, insert extref A
        14      swap UK-column in external system / json -> not updateable, each fails because of other.
        ===> how to detect???
     (9) element in ODM copied. Changes GUID but perserves UK-fields

    """
    cursrcrefname = presult.srcname
    try:
        modellang = Language.getdefaultlang().lang_iso_code2
    except:
        # e.g. if languages are not yet filled
        modellang = parameters.dbDefaultLang()

    olderrorlist, newerrorlist = None, []
    newelements = copy(pjson.getelements(pelemtype=pelemtype))
    dbelemtypesrcrefs = getallsrcrefs(pelemtype=pelemtype, psrcname=cursrcrefname)

    """loop as long as the error list changes. This could be due to the order of constraints resolution (
        e.g. fk does not yet exists).
        Try several times, stop trying if errors stagnate"""
    loopcnt = 0  # safeguard

    failures = dict()
    while olderrorlist != newerrorlist:
        loopcnt += 1
        if loopcnt > 50:
            print(f"***** fromjson2db: too many tries for element {pelemtype}")
            break

        olderrorlist = newerrorlist
        newerrorlist = []
        presult.resetnewerrors()
        curjsonelements = copy(newelements)  # to allow deletion of done elements in loop

        action = f"{'Verification' if presult.checkonly else 'Processing'} {pelemtype}. Pass {loopcnt}"
        if len(curjsonelements.items()) > 0:
            for key, elem in tqdm(curjsonelements.items(), desc=action, dynamic_ncols=True):
                if pwithextsrcref and not presult.ischeckonly():
                    """ get all srcrefs of the element 
                    make sure it has an entry for the current srcname 
                    if not: create one
                    """
                    elemsrcrefs = getelemsrcrefs(psrcname=cursrcrefname, pkey=key, pelem=elem)
                    # remove sourceref which has been handled
                    cursrcrefid = elemsrcrefs[cursrcrefname][0]
                    if cursrcrefid in dbelemtypesrcrefs:
                        del dbelemtypesrcrefs[cursrcrefid]

                    # local obj of element information
                    jsonobj = pjs2obj(pkey=key, pelem=elem, pmodellang=modellang
                                      , psrcname=cursrcrefname,
                                      psrcid=getelemsrcid(psrcrefs=elemsrcrefs, psrcname=cursrcrefname))

                    dbobj = getbyanysrcref(presult=presult, pelemsrcrefs=elemsrcrefs)

                else:
                    jsonobj = pjs2obj(pkey=key, pelem=elem, pmodellang=modellang)
                    cursrcrefid, elemsrcrefs = None, dict()
                    dbobj = None

                # fi
                """here we have an object from the json-element (jsonobj) and 
                    and a dbobj  (if I found one with any external ref)
                    or no dbobj, if there are no external refs or none was found
                """
                """make sure we use new id's, wehreever we know it already"""
                translatefks(presult, jsonobj)

                """ if there is checkonly modus my db was empty and dbobj is None (see above) . I do only inserts to check the consistency. """
                if dbobj is None and not presult.ischeckonly():
                    """Entry not found via sourceref. It could have a changed different srcrefs     """
                    dbobj = jsonobj.getbyanyuk()  # getbyuk(**{colname:obj.colvalue(colname) for colname in puknames})
                # fi
                if dbobj is None:
                    """Entry not found via SRCREF and not found via UK -> it is new"""
                    identity = insert_identity(context=presult, elementtype=pelemtype, key=key, jsonobj=jsonobj)
                    jsonobj.setid(identity)
                    try:
                        dbobjid = jsonobj.insert(pdoerrhdlng=False)
                        logging.debug(f"Inserted {key} with identity {identity} -> {dbobjid}")
                        if identity is not None:
                            assert dbobjid == identity, f"ID to be inserted {identity} got {dbobjid}"
                        else:
                            assert int(dbobjid) > 0, f"ID to be inserted {identity} got {dbobjid} for {key}"
                        presult.addfkey(extjsid=key, dbid=dbobjid)
                        presult.addinscnt(1, f"Insert of {str(jsonobj)}")
                        del newelements[key]  # omit in next loop
                        del failures[key]
                    except Exception as e:
                        #logging.debug(f"Insert attempt of element {key} with id {identity} failed", exc_info=e)
                        if not (presult.ischeckonly() and pelemtype == "LANG"):
                            newerrorlist.append(key)
                            err = f"""*** insert-error: ID = "{key}" """
                            err += f"""\n{e}\n{elem}"""
                            presult.markerror(f"""{err} \n{e}""")
                        failures[key] = ('insert', e, jsonobj)
                else:
                    """entry via external ref  or uk found. this is my existing brother, try to update it"""

                    """get from db all external sourcerefs for this db-ID"""
                    dbsrcrefs = Externalref.getsrcinfo(dbobj.getid())
                    """ check if any db-external refs was updated later than the corresponding json ref """
                    lastupdatedsrcname = whoupdatedmeanwhile(psrcname=cursrcrefname, pjsonsrcrefs=elemsrcrefs,
                                                             pdbsrcrefs=dbsrcrefs)
                    if lastupdatedsrcname is not None:
                        # case 1,2,3
                        presult.markerror(
                            f"""*** Double update merge problem for {pelemtype}: DB-id = {dbobj.getid()} Json-Key = {key}: source "{lastupdatedsrcname}" updated record in DB""")
                        """ the element is in error, don't try again"""
                        del newelements[key]  # omit in next loop
                    else:
                        """ my version seems to be the youngest. 
                            update db-record if there is a difference
                            case 1,2,3
                            """
                        presult.addfkey(extjsid=key, dbid=dbobj.getid())
                        try:
                            jsonobj.setid(dbobj.getid())  # preserve DB-id
                            if pwithextsrcref and cursrcrefid != getelemsrcid(psrcrefs=dbsrcrefs,
                                                                              psrcname=cursrcrefname):
                                Externalref.setlastupdate(psrcname=cursrcrefname, pmodeid=dbobj.getid(),
                                                          psrcid=cursrcrefid)

                            if not jsonobj.semanticequal(dbobj, pequalexceptlist=pequalexceptlist):
                                jsonobj.updatedb(pdoerrhdlng=False)
                                presult.addupdcnt(1, f"Update of {str(jsonobj)}")
                            del newelements[key]  # omit in next loop
                            del failures[key]
                        except Exception as e:
                            newerrorlist.append(key)
                            err = f"""*** update-error : "{pelemtype}: DB-id = {dbobj.getid()} Json-Key = {key} """
                            err += f"""\n{elem}"""
                            presult.markerror(f"""{err} \n{e}""")
                            failures[key] = ('update', e, jsonobj)
                        # fi
                    # fi
                # fi
            # for
        # if
    # while

    # check list of sourcerefs, that are in the db but not in the json
    for dbid in dbelemtypesrcrefs.values():
        extrfs = Externalref.getsrcinfo(dbid)
        if cursrcrefname in extrfs:
            # remove srcrefentry which was not in jsonfile from db
            Externalref.delete(pwhere=("extr_source_name = ? and extr_mode_id = ?", cursrcrefname, dbid))

    if len(newerrorlist) > 0:
        logger.warning(f"Remaining {len(newerrorlist)}"
                       f" i:{len(list(filter(lambda t: 'insert' == t[0], failures.values())))}"
                       f" u: {len(list(filter(lambda t: 'update' == t[0], failures.values())))}"
                       f" errors for {pelemtype}: {newerrorlist}")

        if logger.isEnabledFor(logging.DEBUG):
            for js_key, error in failures.items():
                logger.warning(f"Failed to {error[0]} element {js_key}: {str(error[1])}: {error[1].args} {error[2]}")

    presult.failures.update(failures)
    presult.savenewerrors()
    return


def insert_identity(context: Mergeresult, elementtype: str, key: str, jsonobj) -> int:
    """
    Identity management for new elements.
    Keep identities from JSON for specific element types
    :param jsonobj:
    :param key:
    :param presult:
    :return:
    """
    if context.use_json_id:
        if elementtype in [Modelelemtype.ATTR,
                           Modelelemtype.ENTI,
                           Modelelemtype.INTF,
                           Modelelemtype.TABL,
                           Modelelemtype.COLU,
                           ]:
            try:
                assert context.idTranslate.get(key) is None, f"Id for {key} already set: {context.idTranslate.get(key)}"
                identity = int(key[4:])
                if identity > 0:
                    return identity
            except ValueError:
                logging.warning(f"Unable to use key {key} for identity")
                pass

    # in any other case
    return None
