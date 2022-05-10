from SSOT_infra import todatetime
from datetime import datetime
import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../IM_DB')
from SSOT_db.IM_JSON import *
from SSOT_db.IM_OBJECTS import *
from copy import copy
from SSOT_infra import parameters


class Mergeresult:
    def __init__(self, srcname, verbose=False, checkonly=False):
        self.verbose = verbose
        self.insertcnt = 0
        self.updatecnt = 0
        self.deletecnt = 0
        self.deleterefcnt = 0
        self.errors = []
        self.newerrors = []
        self.warnings = []
        self.changes = []
        self.srcname = srcname
        self.idTranslate = dict()
        """{extjsid: keytrans,}  jsid MMMMxxxx (RELA1442)"""
        self.checkonly = checkonly

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


def getallsrcrefs(pelemtype,psrcname):
    """ get all sourcerefs for an elementtype and a source"""
    retval = {extr.extr_source_id:extr.extr_id \
              for extr in Externalref.getallextrs(pelemtype=pelemtype, psrcname=psrcname)}
    return retval


def translatefks(presult: Mergeresult, pobj):
    """fkvalues {colname:[fktable,fkcolname,fkprefix]} all names in lowercase"""
    fkvalues = pobj.getfkcolumns()
    for colname, fk in fkvalues.items():
        if not (colname == pobj.getidcolname() and fk[2] == 'mode'):
            """fk from ID to mode_id is not handled
               translate id, if it is translated, assume, untranslatd id's are in form xxxx0000"""
            if presult.istranslkey(pobj.colvalue(pcolname=colname)):
                pobj.setcolvalue(pcolname=colname, pvalue=presult.keytransl(pobj.colvalue(pcolname=colname)))
    # for
    return


def getelemsrcref(psrcname, pkey, pelem):
    """ get all source refs of the element, if current sourcename is missing it is a insert, create it
        we assume, the elemnent requires a srcref
    """
    if 'sourceref' in pelem:
        srcrefs = pelem['sourceref']
    else:
        srcrefs = dict()
    if psrcname not in srcrefs:
        srcrefs[psrcname] = [pkey, datetime.now()]
    return srcrefs


"""get the db entry with any of the external src refs
    if there is more than one id found raise an error, mixed srcrefs in the element
"""


def getbyanysrcref(presult, pelemsrcrefs):
    retval = None
    for name, ref in pelemsrcrefs.items():
        dbobj = Modelelement.getelementbyextref(psrcname=name, psrcid=ref[0])
        if dbobj is not None:
            if (retval is not None) and (dbobj.getid() != retval.getid()):
                raise Exception("too many extrefs")
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
    try:
        modellang = Language.getdefaultlang().lang_iso_code2
    except:
        # e.g. if languages are not yet filled
        modellang = parameters.dbDefaultLang()

    olderrorlist, newerrorlist = None, []
    newelements = copy(pjson.getelements(pelemtype=pelemtype))
    dbelemtypesrcrefs = getallsrcrefs(pelemtype=pelemtype,psrcname=presult.srcname)

    """loop as long as the error list changes. This could be due to the order of constraints resolution (
        e.g. fk does not yet exists).
        Try several times, stop trying if errors stagnate"""
    loopcnt = 0  # safeguard
    while olderrorlist != newerrorlist:
        loopcnt += 1
        if loopcnt > 50:
            print(f"***** fromjson2db: too many tries for element {pelemtype}")
            break

        olderrorlist = newerrorlist
        newerrorlist = []
        presult.resetnewerrors()

        curjsonelements = copy(newelements)  # to allow deletion of done elements in loop
        for key, elem in curjsonelements.items():
            if pwithextsrcref:
                """ get all srcrefs of the element 
                make sure it has an entry for the current srcname 
                if not: create one
                """
                elemsrcrefs = getelemsrcref(psrcname=presult.srcname, pkey=key, pelem=elem)
                #remove sourceref which has been handled
                cursrcrefid = elemsrcrefs[presult.srcname][0]
                if cursrcrefid in dbelemtypesrcrefs:
                    del dbelemtypesrcrefs[cursrcrefid]

                # local obj of element information
                jsonobj = pjs2obj(pkey=key, pelem=elem, pmodellang=modellang
                                  , psrcname=presult.srcname, psrcid=elemsrcrefs[presult.srcname][0])

                dbobj = getbyanysrcref(presult=presult, pelemsrcrefs=elemsrcrefs)

            else:
                jsonobj = pjs2obj(pkey=key, pelem=elem, pmodellang=modellang)
                elemsrcrefs = []
                dbobj = None
            # fi
            """here we have a object from the json-element (jsonobj) and 
                and a dbobj  (if I found one with any external ref)
                or no dbobj, if there are no external refs or none was found
            """

            """make sure we use new id's, wehreever we know it already"""
            translatefks(presult, jsonobj)
            """ if there is checkonly modus, my db was empty. I do only inserts to check the consistency. """
            if dbobj is not None and not presult.ischeckonly():
                """entry via external ref  found. this is my existing brother, try to update it"""

                """get from db all external sourcerefs for this db-ID"""
                dbsrcrefs = Externalref.getsrcinfo(dbobj.getid())
                """ check if any db-external refs was updated later than the corresponding json ref """
                lastupdatedsrcname = whoupdatedmeanwhile(psrcname=presult.srcname, pjsonsrcrefs=elemsrcrefs,
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
                    if not jsonobj.semanticequal(dbobj, pequalexceptlist=pequalexceptlist):
                        try:
                            jsonobj.setid(dbobj.getid())  # preserve DB-id
                            jsonobj.updatedb(pdoerrhdlng=False)
                            presult.addupdcnt(1, f"Update of {str(jsonobj)}")
                            del newelements[key]  # omit in next loop
                        except Exception as e:
                            newerrorlist.append(key)
                            err = f"""*** update-error : "{pelemtype}: DB-id = {dbobj.getid()} Json-Key = {key} """
                            err += f"""\n{elem}"""
                            presult.markerror(f"""{err} \n{e}""")
                    # fi
                # fi
            else:
                """Entry not found via sourceref. It could have a changed different srcref"""
                dbukobj = jsonobj.getbyanyuk()  # getbyuk(**{colname:obj.colvalue(colname) for colname in puknames})
                """ if an entry with the same UK exists (must have different srcid, otherwise it would not land here)
                    we habe a UK-problem. Otherwise insert the element """
                if dbukobj is None or presult.ischeckonly():
                    """Entry not found via SRCREF and not found via UK -> it is new"""
                    try:
                        jsonobj.setid(None)  # provoke new ID in new db
                        dbobjid = jsonobj.insert(pdoerrhdlng=False)
                        presult.addfkey(extjsid=key, dbid=dbobjid)
                        presult.addinscnt(1, f"Insert of  {str(jsonobj)}")
                        del newelements[key]  # omit in next loop
                    except Exception as e:
                        if not (presult.ischeckonly() and pelemtype == "LANG"):
                            newerrorlist.append(key)
                            err = f"""*** insert-error: ID = "{key}" """
                            err += f"""\n{e}\n{elem}"""
                            presult.markerror(f"""{err} \n{e}""")
                else:
                    """Entry found via UK. update it.  update the external ref as well"""
                    presult.addfkey(extjsid=key, dbid=dbukobj.getid())

                    if not dbukobj.semanticequal(jsonobj, pequalexceptlist=pequalexceptlist):
                        try:
                            """update element found by it's uk"""
                            dbukobj.semanticcopy(jsonobj)
                            dbukobj.updatedb(pdoerrhdlng=False)
                            presult.addupdcnt(1, f"Update of {str(dbukobj)}")
                            del newelements[key]  # omit in next loop
                        except Exception as e:
                            newerrorlist.append(key)
                            err = f"""*** update-error : {pelemtype} DB-id = {dbobj.getid()} Json-Key = {key}: """
                            err += f"""\n{elem}"""
                            presult.markerror(f"""{err} \n{e}""")
                    # fi
                # fi
            # fi
        # for
    # while

    #check list of sourcerefs, that are in the db but not in the json
    for dbid in dbelemtypesrcrefs.values():
        extrfs = Externalref.getsrcinfo(dbid)
        if presult.srcname in extrfs:
            #remove srcrefentry which was not in jsonfile from db
            Externalref.delete(pwhere=("extr_source_name = ? and extr_mode_id = ?",presult.srcname,dbid))

    presult.savenewerrors()
    return
