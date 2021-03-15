from IM_JSON import *
from IM_OBJECTS import *
from dbDML import valuepairs2sqlexpr
from copy import copy

"""{odmjsid: dbid,}  jsid MMMMxxxx (RELA1442)"""
idTranslate= dict()
def addfk(odmjsid, dbid):
    global idTranslate
    idTranslate[odmjsid] = dbid
def dbid(odmjsid):
    global idTranslate
    return idTranslate[odmjsid]

class Mergeresult:
    def __init__(self):
        self.insertcnt = 0
        self.updatecnt = 0
        self.deletecnt = 0
        self.deleterefcnt = 0
        self.errors = []
        self.warnings = []

    def update(self,pmerge):
        self.insertcnt += pmerge.insertcnt
        self.updatecnt += pmerge.updatecnt
        self.deleterefcnt += pmerge.deleterefcnt
        self.deletecnt += pmerge.deletecnt
        self.errors += pmerge.errors
        self.warnings += pmerge.warnings

    def markdberror(self,perr,pelem):
        self.errors.append("""*** DB-Error {}\{}""".format(perr, pelem))

    def markerror(self,pstr):
        self.errors.append(str)

    def markwarning(self,pstr):
        self.warnings.append(str)



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
                        or (pdbid is not None and e.dbid == pdbid)):
                return True
        return False
#Extrsourceref

def getallsrcrefs(pelemtype):
    retval = Extsourcerefs()
    for extr in Externalref.getallextrs (pelemtype=pelemtype):
        retval.push(Extsourceref(psrcname=extr.extr_source_name, psrcid=extr.extr_source_id, plastupd=extr.extr_last_update, pdbid=extr.extr_mode_id))
    # for
    return retval

def fromdb2odm(presult,podmjson,pdbjson,pelemtype,puknames,pjs2obj,pwithextsrcref=True):
    """from DB to ODM transfer"""
    removedrefs = []
    """get all srcrefs existing in ODM
         in the form
        {OBJTkey: [srcname,srcid,srclastupd,dbid]}"""
    if pwithextsrcref:
        allodmsrcrefs = getallsrcrefs(pelemtype=pelemtype,pjson=podmjson)
    else:
        allodmsrcrefs = Extsourcerefs()

    """is there a db-element without ODM-GUID"""
    for key, elem in pdbjson.getelements(pelemtype=pelemtype).items():
        if pwithextsrcref:
            if len(elem["sourceref"])== 0:
                """no external source references this entry, mark to be removed"""
                removedrefs.append(key)
            else:
                dbsrcid = None
                for srcname, srcelem in elem["sourceref"].items():
                    if srcname == Externalref.SOURCE_ODM:
                        dbsrcid = srcelem[0]
                        break
                    #fi
                if dbsrcid is None:
                    presult.warnings.append("+++ Element {} in db not yet in ODM".format(key))
                else:
                    """does db-odmguid exist in ODM """
                    odmsrcref = allodmsrcrefs.get(psrcname=Externalref.SOURCE_ODM,psrcid=dbsrcid)
                    if odmsrcref is None:
                        """odm-source id does no longer exist in ODM
                            remove it from DB"""
                        Externalref.delete(pwhere="extr_source_name = '{}' and extr_source_id = '{}'"
                                                    .format(Externalref.SOURCE_ODM,dbsrcid))
                        removedrefs.append(key)
                        presult.deleterefcnt += 1
                    else:
                        """odm found. already treated in fromo dm2db"""
                        pass
                    #fi
                #fi
            #fi
        #fi
    #for
    if pwithextsrcref:
        """delete all elements which no longer exist"""
        Modelelement.deletemodes(pmodeids=[jsguid2id(key) for key in removedrefs])
        presult.deletecnt += len (removedrefs)
    else:
        """delete all DB elements with UK not in the ODM-DB"""
        jsukname = 'name' #currently we have only names as UK in non-odm-guid-elements
        for dbkey,dbval in pdbjson.getelements(pelemtype=pelemtype).items():
            uklist = [dbkey for odmval in podmjson.getelements(pelemtype=pelemtype).values() if dbval[jsukname] == odmval[jsukname]]
            if len(uklist) == 0:
                """no uk found in ODM, delete it from DB"""
                dbobj = pjs2obj(pkey=dbkey,pelem=dbval) #memory only object
                dbobj.delete(pwhere=valuepairs2sqlexpr(**{colname:dbobj.colvalue(colname) for colname in puknames}))
                presult.deletecnt += 1
            #fi
        #for
    return


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
                pdbobj.setcolvalue(pcolname=colname, pvalue=idTranslate[jsguid(fk[2].upper(), pdbobj.colvalue(pcolname=colname))])
    #for
    return


def fromodm2db(presult,podmjson:JSModel, pelemtype, pjs2obj,pwithextsrcref=True):
    """from ODM to DB transfer"""
    modellang = Language.getdefaultlang().lang_iso_code2
    newdberrors = []
    olddberrors = None
    odmelements = copy(podmjson.getelements(pelemtype=pelemtype))
    """loop as long as the error list changes. This could be due to the order of constraints resolution (
        e.g. fk does not yet exists).
        Try several times, stop trying if errors stagnate"""
    loopcnt = 0 #safeguard
    while olddberrors != newdberrors:
        loopcnt += 1
        if loopcnt > 50:
            print ("***** fromodm2db: too many trys for element {}".format(pelemtype))
            break

        olddberrors = newdberrors
        newdberrors = []

        """external source refs in the target Database for the acutal elementtype (pelemtype) in the form
            {OBJTkey: [srcname,srcid,srclastupd,dbid]}"""
        if pwithextsrcref:
            alldbsrcrefs = getallsrcrefs(pelemtype=pelemtype)
        else:
            alldbsrcrefs = Extsourcerefs()

        curodmelements = copy(odmelements) #to allow deletion of done elements in loop
        for key,elem in curodmelements.items():
            if pwithextsrcref:
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

            if dbsrcref is not None:
                """entry via ODM-GUID found. this is my existing brother, try to update it"""

                """get all external sourcerefs from all sources for this db-ID"""
                dbsrcrefs:Extsourcerefs = alldbsrcrefs.getall(pdbid=dbsrcref.dbid)
                lastupdatesrcref = dbsrcrefs.getwithmaxupd()
                if (lastupdatesrcref.srcname !=  Externalref.SOURCE_ODM):
                    """other source updated DB after ODM"""
                    newdberrors.append("""*** Double update merge problem for {}:{}: source "{}" updated after source {}"""
                                       .format(pelemtype,dbsrcref.dbid,lastupdatesrcref.srcname,Externalref.SOURCE_ODM))
                else:
                    """update db-record if there is a difference"""
                    if not obj.semanticequal(Modelelement.getelement(pmodeid=dbsrcref.dbid)):
                        try:
                            addfk(odmjsid=key, dbid=jsdbsrcref.dbid)
                            obj.setid(jsguid2id(dbsrcref.dbid)) #preserve DB-id
                            translatefks(obj)
                            obj.updatedb(pdoerrhdlng=False)
                            Externalref.setlastupdate(psrcname=Externalref.SOURCE_ODM,pmodeid=obj.getid())
                            presult.updatecnt += 1
                            del odmelements[key] #omit in next loop
                        except Exception as e:
                            newdberrors.append("""*** update-error : ID = "{}:{}" \n{}""".format(pelemtype,obj.getid(),e))
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
                        translatefks(obj)
                        objid = obj.insert(pdoerrhdlng=False)
                        addfk(odmjsid=key, dbid=objid)
                        presult.insertcnt += 1
                        del odmelements[key]  # omit in next loop
                    except Exception as e:
                        newdberrors.append("""*** insert-error: ID = "{}:{}" exists with different GUID\n{}""".format(pelemtype,obj.getid(),e))
                else:
                    """Entry found via UK. update it.  update the external ref as well, as it could be"""
                    if not ukref.semanticequal(obj):
                        try:
                            """update element found by it's uk"""
                            addfk(odmjsid=key, dbid=ukref.getid())
                            ukref.semanticcopy(obj)
                            translatefks(ukref)
                            ukref.updatedb(pdoerrhdlng=False)
                            if pwithextsrcref:
                                """update lastupd and add extr scr id as it may have changed or is new"""
                                Externalref.setlastupdate(psrcname=Externalref.SOURCE_ODM,pmodeid=obj.getid(),psrcid=elem['sourceref'][Externalref.SOURCE_ODM][0])
                            presult.updatecnt += 1
                            del odmelements[key]  # omit in next loop
                        except Exception as e:
                            newdberrors.append("""*** update-error : ID = "{}:{}" \n{}""".format(pelemtype,ukref.getid(),e))

                    #fi
                # fi
            #fi
        #for
    #while
    presult.errors += newdberrors
    return