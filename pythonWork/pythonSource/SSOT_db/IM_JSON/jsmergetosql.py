import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../IM_DB')
from SSOT_db.IM_JSON import *
from SSOT_db.IM_OBJECTS import *
from copy import copy
from SSOT_infra import parameters


class Mergeresult:
    def __init__(self, srcname, verbose=False,checkonly=False):
        self.verbose = verbose
        self.insertcnt = 0
        self.updatecnt = 0
        self.deletecnt = 0
        self.deleterefcnt = 0
        self.errors = []
        self.newerrors = []
        self.warnings = []
        self.changes = []
        self.srcname=srcname
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

class Extsourcerefs(list):
    def push(self, val):
        self.append(val)
        return

    def get(self, psrcname, psrcid):
        for e in self:
            if e.extr_source_name == psrcname and e.srextr_source_idcid == psrcid:
                return e
        return None

    def getall(self, pdbid):
        retval = Extsourcerefs()
        for e in self:
            if e.extr_mode_id == pdbid:
                retval.append(e)
        return retval

    def getmaxupd(self):
        retval = ''
        for e in self:
            retval = max(e.extr_last_update, retval)
        return retval

    def getwithmaxupd(self) -> Externalref:
        maxupd = self.getmaxupd()
        for e in self:
            if e.extr_last_update == maxupd:
                return e
        return None

    def exists(self, psrcname, psrcid=None, pdbid=None):
        for e in self:
            if (e.extr_source_name == psrcname) \
                    and ((psrcid is not None and e.extr_source_id == psrcid) \
                         or (pdbid is not None and e.extr_mode_id == pdbid)):
                return True
        return False
# Extrsourcerefs

def getallsrcrefs(pelemtype):
    retval = Extsourcerefs()
    for extr in Externalref.getallextrs(pelemtype=pelemtype):
        retval.push(extr)
    # for
    return retval


def translatefks(presult: Mergeresult, pdbobj):
    """fkvalues {colname:[fktable,fkcolname,fkprefix]} all names in lowercase"""
    fkvalues = pdbobj.getfkcolumns()
    for colname, fk in fkvalues.items():
        if not (colname == pdbobj.getidcolname() and fk[2] == 'mode'):
            """fk from ID to mode_id is not handled
               translate id, if it is translated, assume, untranslatd id's are in form xxxx0000"""
            if presult.istranslkey(pdbobj.colvalue(pcolname=colname)):
                pdbobj.setcolvalue(pcolname=colname, pvalue=presult.keytransl(pdbobj.colvalue(pcolname=colname)))
    # for
    return

def fromjson2db(presult: Mergeresult, pjson: JSModel, pelemtype, pjs2obj, pwithextsrcref=True, pequalexceptlist=[]):
    """from json-model to DB transfer"""
    try:
        modellang = Language.getdefaultlang().lang_iso_code2
    except:
        # e.g. if languages are not yet filled
        modellang = parameters.dbDefaultLang()

    olderrorlist, newerrorlist = None, []
    newelements = copy(pjson.getelements(pelemtype=pelemtype))
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

        """external source refs in the target Database for the acutal elementtype (pelemtype) in the form
            {OBJTkey: [srcname,srcid,srclastupd,modeid]}"""
        alldbsrcrefs:Extsourcerefs = getallsrcrefs(pelemtype=pelemtype)

        curjsonelements = copy(newelements)  # to allow deletion of done elements in loop
        for key, elem in curjsonelements.items():
            """some elements (ARCS,DOMAINS) can have ext-ref or not (depending wether they are generated or
               user maintained
               if pwithtextref is True, make sure the element really has a 'sourceref' entry for  external source """
            lwithextsrcref = pwithextsrcref and (
                        ('sourceref' in elem) and (presult.srcname in elem['sourceref']))
            if lwithextsrcref:
                extsrcref = Externalref(extr_source_name=presult.srcname,
                                         extr_source_id=elem['sourceref'][presult.srcname][0],
                                         extr_last_update=elem['sourceref'][presult.srcname][1],
                                         extr_mode_id=key)

                obj = pjs2obj(pkey=key, pelem=elem, pmodellang=modellang
                              , psrcname=extsrcref.srcname, psrcid=extsrcref.srcid)
                """get the db entry with the same external src GUID"""
                dbsrcref = alldbsrcrefs.get(psrcname=extsrcref.srcname, psrcid=extsrcref.srcid)
            else:
                obj = pjs2obj(pkey=key, pelem=elem, pmodellang=modellang)
                dbsrcref = None
            # fi
            """make sure we use new id's, wehreever we know it already"""
            translatefks(presult, obj)
            if dbsrcref is not None and not presult.ischeckonly():
                """entry via GUID found. this is my existing brother, try to update it"""

                """get all external sourcerefs from all sources for this db-ID"""
                dbsrcrefs: Extsourcerefs = alldbsrcrefs.getall(pdbid=dbsrcref.dbid)
                lastupdatesrcref = dbsrcrefs.getwithmaxupd()
                if (lastupdatesrcref.srcname != presult.srcname):
                    """other source updated DB after mine"""
                    presult.markerror(
                        f"""*** Double update merge problem for {pelemtype}:{dbsrcref.dbid}: source "{lastupdatesrcref.srcname}" updated after source {presult.srcname}""")
                    newerrorlist.append(key)
                else:
                    """update db-record if there is a difference"""
                    presult.addfkey(extjsid=key, dbid=dbsrcref.dbid)
                    dbelem = Modelelement.getelement(pmodeid=dbsrcref.dbid)
                    if not obj.semanticequal(dbelem, pequalexceptlist=pequalexceptlist):
                        try:
                            obj.setid(dbsrcref.dbid)  # preserve DB-id
                            obj.updatedb(pdoerrhdlng=False)
                            Externalref.setlastupdate(psrcname=presult.srcname, pmodeid=obj.getid())
                            presult.addupdcnt(1, f"Update of {str(obj)}")
                            del newelements[key]  # omit in next loop
                        except Exception as e:
                            newerrorlist.append(key)
                            err = f"""*** update-error : ID = "{pelemtype}:{obj.getid()}" """
                            err += f"""\n{elem}"""
                            presult.markerror(f"""{err} \n{e}""")
                    # fi
                # fi
            else:
                """Entry not found via dbsrcref. It could still have a different srcref-GUID"""
                ukref = obj.getbyanyuk()  # getbyuk(**{colname:obj.colvalue(colname) for colname in puknames})
                """ if an entry with the same UK exists (must have different srcid, otherwise it would not land here)
                    we habe a UK-problem. Otherwise insert the element """
                if ukref is None or presult.ischeckonly():
                    """Entry not found via SRCREF and not found via UK -> it is new"""
                    try:
                        obj.setid(None)  # provoke new ID in new db
                        objid = obj.insert(pdoerrhdlng=False)
                        presult.addfkey(extjsid=key, dbid=objid)
                        presult.addinscnt(1, f"Insert of  {str(obj)}")
                        del newelements[key]  # omit in next loop
                    except Exception as e:
                        if not (presult.ischeckonly() and pelemtype == "LANG"):
                            newerrorlist.append(key)
                            err = f"""*** insert-error: ID = "{key}" """
                            err += f"""\n{e}\n{elem}"""
                            presult.markerror(f"""{err} \n{e}""")
                else:
                    """Entry found via UK. update it.  update the external ref as well, as it could be"""
                    presult.addfkey(extjsid=key, dbid=ukref.getid())

                    if not ukref.semanticequal(obj, pequalexceptlist=pequalexceptlist):
                        try:
                            """update element found by it's uk"""
                            ukref.semanticcopy(obj)
                            translatefks(presult, ukref)
                            ukref.updatedb(pdoerrhdlng=False)
                            if lwithextsrcref:
                                """update lastupd and add extr scr id as it may have changed or is new"""
                                Externalref.setlastupdate(psrcname=presult.srcname, pmodeid=ukref.getid(),
                                                          psrcid=elem['sourceref'][presult.srcname][0])
                            presult.addupdcnt(1, f"Update of {str(ukref)}")
                            del newelements[key]  # omit in next loop
                        except Exception as e:
                            newerrorlist.append(key)
                            err = f"""*** update-error : ID = "{pelemtype}:{ukref.getid()}" """
                            err += f"""\n{elem}"""
                            presult.markerror(f"""{err} \n{e}""")
                    # fi
                # fi
            # fi
        # for
    # while
    presult.savenewerrors()
    return
