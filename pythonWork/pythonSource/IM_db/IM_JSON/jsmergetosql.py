from IM_JSON import *
from IM_OBJECTS import *
from datetime import datetime
from IM_DB import dbConnect
from dbDML import valuepairs2sqlexpr


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

def getallsrcrefs(pelemtype,pjson):
    retval = Extsourcerefs()
    for key, elem in pjson.getelements(pelemtype=pelemtype).items():
        for srcname, srcelem in elem["sourceref"].items():
            retval.push(Extsourceref(psrcname=srcname, psrcid=srcelem[0], plastupd=srcelem[1], pdbid=key))
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

def fromodm2db(presult,podmjson, pdbjson, pelemtype, pjs2obj,pwithextsrcref=True):
    """from ODM to DB transfer"""
    newdberrors = [0]
    olddberrors = []

    """loop as long as the error list changes. This could be due to the order of constraints resolution (
        e.g. fk does not yet exists).
        Try several times, stop trying if errors stagnate"""
    while olddberrors != newdberrors:
        olddberrors = newdberrors
        newdberrors = []

        """external source refs in the form
            {OBJTkey: [srcname,srcid,srclastupd,dbid]}"""
        if pwithextsrcref:
            alldbsrcrefs = getallsrcrefs(pelemtype=pelemtype,pjson=pdbjson)
        else:
            alldbsrcrefs = Extsourcerefs()

        for key,elem in podmjson.getelements(pelemtype=pelemtype).items():
            if pwithextsrcref:
                odmsrcref = Extsourceref(psrcname = Externalref.SOURCE_ODM,
                                         psrcid = elem['sourceref'][Externalref.SOURCE_ODM][0]
                                        ,plastupd = elem['sourceref'][Externalref.SOURCE_ODM][1]
                                        ,pdbid = key)
                obj = pjs2obj(pkey=key,pelem=elem,psrcname=odmsrcref.srcname,psrcid=odmsrcref.srcid)
                """get the db entry with the same ODM src GUID"""
                dbsrcref = alldbsrcrefs.get(psrcname=odmsrcref.srcname, psrcid=odmsrcref.srcid)
            else:
                obj = pjs2obj(pkey=key, pelem=elem)
                dbsrcref = None
            #fi

            if dbsrcref is not None:
                """entry via ODM-GUID found. this is my existing brother, try to update it"""
                """get all sourcerefs from all sources for this db-ID"""
                dbsrcrefs:Extsourcerefs = alldbsrcrefs.getall(pdbid=dbsrcref.dbid)
                lastupdatesrcref = dbsrcrefs.getwithmaxupd()
                if (lastupdatesrcref.srcname !=  Externalref.SOURCE_ODM):
                    """other source updated DB after ODM"""
                    newdberrors.append("""*** Double update merge problem for {}:{}: source "{}" updated after source {}"""
                                       .format(pelemtype,dbsrcref.dbid,lastupdatesrcref.srcname,Externalref.SOURCE_ODM))
                else:
                    """update db-record if there is a difference"""
                    if not obj.semanticequal(pjs2obj(pkey=dbsrcref.dbid,pelem=pdbjson.getbyid(dbsrcref.dbid))):
                        try:
                            obj.setid(jsguid2id(dbsrcref.dbid)) #preserve DB-id
                            obj.updatedb(pdoerrhdlng=False)
                            Externalref.setlastupdate(psrcname=Externalref.SOURCE_ODM,pmodeid=obj.getid())
                            presult.updatecnt += 1
                        except Exception as e:
                            newdberrors.append("""*** update-error : ID = "{}:{}" \n{}""".format(pelemtype,obj.getid(),e))
                    # fi
                #fi
            else:
                ukref = obj.getbyanyuk() #getbyuk(**{colname:obj.colvalue(colname) for colname in puknames})
                """ if an entry with the same UK exists (must have different srcid, otherwise it would not land here)
                    we habe a UK-problem. Otherwise insert the element """
                if ukref is None:
                    try:
                        obj.setid(None) #provoke new ID in new db
                        obj.translatefks()
                        objid = obj.insert(pdoerrhdlng=False)
                        presult.insertcnt += 1
                    except Exception as e:
                        newdberrors.append("""*** insert-error: ID = "{}:{}" exists with different GUID\n{}""".format(pelemtype,obj.getid(),e))
                else:
                    if pwithextsrcref:
                        ukvalues = '\n'.join(val for val in obj.getukvaluepairs())
                        newdberrors.append("""*** Merge-error: Element "{}:{}" with UK "{}" exists with different GUID"""
                                         .format(pelemtype,obj.getid(),ukvalues))
                    else:
                        if not ukref.semanticequal(obj):
                            """update element found by it's uk"""
                            ukref.semanticcopy(obj)
                            ukref.updatedb(pdoerrhdlng=False)
                            presult.updatecnt += 1
                        #fi
                    #fi
                # fi
            #fi
        #for
    #while
    presult.errors += newdberrors
    return