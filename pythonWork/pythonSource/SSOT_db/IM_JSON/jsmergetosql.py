import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../IM_DB')
from SSOT_db.IM_JSON import  *
from SSOT_db.IM_OBJECTS import  *
from copy import copy
from SSOT_infra import parameters

"""{odmjsid: keytrans,}  jsid MMMMxxxx (RELA1442)"""
idTranslate= dict()
def addfk(odmjsid, dbid):
    global idTranslate
    idTranslate[odmjsid] = dbid

def keytransl(odmjsid):
    global idTranslate
    if odmjsid in idTranslate:
        return idTranslate[odmjsid]
    else:
        return None

class Mergeresult:
    def __init__(self,verbose=False):
        self.verbose = verbose
        self.insertcnt = 0
        self.updatecnt = 0
        self.deletecnt = 0
        self.deleterefcnt = 0
        self.errors = []
        self.warnings = []
        self.changes = []

    def markdberror(self,perr,pelem):
        self.errors.append(f"""*** DB-Error {perr}\{pelem}""")

    def markerror(self,pstr):
        self.errors.append(pstr)

    def markwarning(self,pstr):
        self.warnings.append(pstr)

    def addchange(self,pstr):
        if self.verbose:
            self.changes.append(pstr)

    def adddelcnt(self,cnt,pstr=None):
        self.deletecnt += cnt
        if cnt > 0 and pstr is not None:
            self.addchange(pstr+ f"  delete,cnt={str(cnt)}")

    def addinscnt(self,cnt,pstr=None):
        self.insertcnt += cnt
        if cnt > 0 and pstr is not None:
            self.addchange(pstr+ f"  insert,cnt={str(cnt)}")

    def addupdcnt(self,cnt,pstr=None):
        self.updatecnt += cnt
        if cnt > 0 and pstr is not None:
            self.addchange(pstr+ f"  update,cnt={str(cnt)}")

    def adddelrefcnt(self,cnt,pstr=None):
        self.deleterefcnt += cnt
        if cnt > 0 and pstr is not None:
            self.addchange(pstr+ f"  delete-refs,cnt={str(cnt)}")

class Extsourceref:
    def __init__(self,psrcname,psrcid,plastupd,pdbid):
        self.srcname=psrcname
        self.srcid=psrcid
        self.lastupd=plastupd
        self.dbid=pdbid

class Extsourcerefs(list):
    def push(self,val):
        self.append(val)

    def get(self,psrcname,psrcid):
        for e in self:
            if e.srcname == psrcname and e.srcid == psrcid:
                return e
        return None

    def getall(self,pdbid):
        retval = Extsourcerefs()
        for e in self:
            if e.dbid == pdbid:
                retval.append(e)
        return retval

    def getmaxupd(self):
        retval = ''
        for e in self:
            retval = max(e.lastupd,retval)
        return retval

    def getwithmaxupd(self) ->Extsourceref:
        maxupd=self.getmaxupd()
        for e in self:
            if e.lastupd == maxupd: return e
        return None

    def exists(self,psrcname,psrcid=None,pdbid=None):
        for e in self:
            if (e.srcname == psrcname)\
                and ((psrcid is not None and e.srcid == psrcid)\
                        or (pdbid is not None and e.keytrans == pdbid)):
                return True
        return False
#Extrsourceref

def getallsrcrefs(pelemtype):
    retval = Extsourcerefs()
    for extr in Externalref.getallextrs (pelemtype=pelemtype):
        retval.push(Extsourceref(psrcname=extr.extr_source_name, psrcid=extr.extr_source_id,
                                 plastupd=extr.extr_last_update, pdbid=extr.extr_mode_id))
    # for
    return retval


def translatefks(pdbobj):
    global idTranslate
    """fkvalues {colname:[fktable,fkcolname,fkprefix]} all names in lowercase"""
    fkvalues = pdbobj.getfkcolumns()
    if len(fkvalues) == 0: return
    for colname,fk in fkvalues.items():
        if not (colname == pdbobj.getidcolname() and fk[2] == 'mode'):
            """fk from ID to mode_id is not handled
               translate id, if it's jsid MMMMxxxx is already translated"""
            if jsguid(fk[2].upper(),pdbobj.colvalue(pcolname=colname)) in idTranslate:
                pdbobj.setcolvalue(pcolname=colname, pvalue=keytransl(jsguid(fk[2].upper(), pdbobj.colvalue(pcolname=colname))))
    #for
    return


def fromodm2db(presult,podmjson:JSModel, pelemtype, pjs2obj,pwithextsrcref=True,pequalexceptlist=[]):
    """from json-model to DB transfer"""
    try:
        modellang = Language.getdefaultlang().lang_iso_code2
    except:
        #e.g. if languages are not yet filled
        modellang = parameters.dbDefaultLang()


    newdberrors = []
    oldrepeaterrs,newrepeaterrs = None,[]
    newelements = copy(podmjson.getelements(pelemtype=pelemtype))
    """loop as long as the error list changes. This could be due to the order of constraints resolution (
        e.g. fk does not yet exists).
        Try several times, stop trying if errors stagnate"""
    loopcnt = 0 #safeguard
    while oldrepeaterrs != newrepeaterrs:
        loopcnt += 1
        if loopcnt > 50:
            print ("***** fromodm2db: too many tries for element {}".format(pelemtype))
            break

        oldrepeaterrs = newrepeaterrs
        newrepeaterrs = []

        """external source refs in the target Database for the acutal elementtype (pelemtype) in the form
            {OBJTkey: [srcname,srcid,srclastupd,keytrans]}"""
        if pwithextsrcref:
            alldbsrcrefs = getallsrcrefs(pelemtype=pelemtype)
        else:
            alldbsrcrefs = Extsourcerefs()

        curjsonelements = copy(newelements) #to allow deletion of done elements in loop
        for key,elem in curjsonelements.items():
            """some elements (ARCS,DOMAINS) can have ODM-ref or not (depending wether they are generated or
               user maintained
               if pwithtextref is True, make sure the element really has a 'sourceref' entry for  ODM """
            lwithextsrcref = pwithextsrcref and (('sourceref' in elem) and (Externalref.SOURCE_ODM in elem['sourceref']))
            if lwithextsrcref:
                odmsrcref = Extsourceref(psrcname = Externalref.SOURCE_ODM,
                                         psrcid = elem['sourceref'][Externalref.SOURCE_ODM][0]
                                        ,plastupd = elem['sourceref'][Externalref.SOURCE_ODM][1]
                                        ,pdbid = key)
                obj = pjs2obj(pkey=key,pelem=elem,pmodellang=modellang
                              ,psrcname=odmsrcref.srcname,psrcid=odmsrcref.srcid)
                """get the db entry with the same ODM src GUID"""
                dbsrcref = alldbsrcrefs.get(psrcname=odmsrcref.srcname, psrcid=odmsrcref.srcid)
            else:
                obj = pjs2obj(pkey=key, pelem=elem,pmodellang=modellang)
                dbsrcref = None
            #fi
            """make sure we use new id's, where ever we know it already"""
            translatefks(obj)
            if dbsrcref is not None:
                """entry via ODM-GUID found. this is my existing brother, try to update it"""

                """get all external sourcerefs from all sources for this db-ID"""
                dbsrcrefs:Extsourcerefs = alldbsrcrefs.getall(pdbid=dbsrcref.dbid)
                lastupdatesrcref = dbsrcrefs.getwithmaxupd()
                if (lastupdatesrcref.srcname !=  Externalref.SOURCE_ODM):
                    """other source updated DB after ODM"""
                    newdberrors.append(f"""*** Double update merge problem for {pelemtype}:{dbsrcref.dbid}: source "{lastupdatesrcref.srcname}" updated after source {Externalref.SOURCE_ODM}""")
                    newrepeaterrs.append(
                        f"""*** Double update merge problem for {pelemtype}:{dbsrcref.dbid}: source "{lastupdatesrcref.srcname}" updated after source {Externalref.SOURCE_ODM}"""
                        )
                else:
                    """update db-record if there is a difference"""
                    addfk(odmjsid=key, dbid=dbsrcref.dbid)
                    dbelem = Modelelement.getelement(pmodeid=dbsrcref.dbid)
                    if not obj.semanticequal(dbelem,pequalexceptlist=pequalexceptlist):
                        try:
                            obj.setid(dbsrcref.dbid) #preserve DB-id
                            obj.updatedb(pdoerrhdlng=False)
                            Externalref.setlastupdate(psrcname=Externalref.SOURCE_ODM,pmodeid=obj.getid())
                            presult.addupdcnt(1,f"Update of {str(obj)}")
                            del newelements[key] #omit in next loop
                        except Exception as e:
                            err = f"""*** update-error : ID = "{pelemtype}:{obj.getid()}" """
                            err += f"""\n{elem}"""
                            newdberrors.append(f"""{err} \n{e}""")
                            newrepeaterrs.append(err)
                    # fi
                #fi
            else:
                """Entry not found via dbsrcref. It could still have a different srcref-GUID"""
                ukref = obj.getbyanyuk() #getbyuk(**{colname:obj.colvalue(colname) for colname in puknames})
                """ if an entry with the same UK exists (must have different srcid, otherwise it would not land here)
                    we habe a UK-problem. Otherwise insert the element """
                if ukref is None:
                    """Entry not found via SRCREF and not found via UK -> it is new"""
                    try:
                        obj.setid(None) #provoke new ID in new db
                        objid = obj.insert(pdoerrhdlng=False)
                        logging.debug(f"Created new row with id {objid} for key {key}")
                        addfk(odmjsid=key, dbid=objid)
                        presult.addinscnt (1,f"Insert of  {str(obj)}")
                        del newelements[key]  # omit in next loop
                    except Exception as e:
                        err = f"""*** insert-error: ID = "{key}" exists with different GUID\n{e}"""
                        err += f"""\n{elem}"""
                        newdberrors.append(f"""{err} \n{e}""")
                        newrepeaterrs.append(err)
                else:
                    """Entry found via UK. update it.  update the external ref as well, as it could be"""
                    addfk(odmjsid=key, dbid=ukref.getid())

                    if not ukref.semanticequal(obj,pequalexceptlist=pequalexceptlist):
                        try:
                            """update element found by it's uk"""
                            ukref.semanticcopy(obj)
                            translatefks(ukref)
                            ukref.updatedb(pdoerrhdlng=False)
                            if lwithextsrcref:
                                """update lastupd and add extr scr id as it may have changed or is new"""
                                Externalref.setlastupdate(psrcname=Externalref.SOURCE_ODM,pmodeid=ukref.getid(),psrcid=elem['sourceref'][Externalref.SOURCE_ODM][0])
                            presult.addupdcnt(1,f"Update of {str(ukref)}")
                            del newelements[key]  # omit in next loop
                        except Exception as e:
                            err = f"""*** update-error : ID = "{pelemtype}:{ukref.getid()}" """
                            err += f"""\n{elem}"""
                            newdberrors.append(f"""{err} \n{e}""")
                            newrepeaterrs.append(err)
                    #fi
                # fi
            #fi
        #for
    #while
    presult.errors += newdberrors
    return