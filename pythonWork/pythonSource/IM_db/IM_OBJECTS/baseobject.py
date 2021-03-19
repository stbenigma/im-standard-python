import sqlite3

from IM_DB import dbDML, dbDDL,logmessages
from datetime import datetime



class Boolean:
    TRUE: str = 'TRUE'
    FALSE: str = 'FALSE'

    @staticmethod
    def str2bool(pstr):
        if (pstr is None):
            return None
        elif (pstr.upper() in (Boolean.TRUE, 'T')):
            return True
        elif (pstr.upper() in (Boolean.FALSE, 'F')):
            return False
        else:
            raise Exception('Ungültiger Wert für Boolean "{}"'.format(pstr))

    # str2bool
    @staticmethod
    def bool2str(bool):
        return Boolean.TRUE if bool else Boolean.FALSE

    @staticmethod
    def strnegbool(pstr):
        return Boolean.bool2str(not Boolean.str2bool(pstr))
    # strNegBool


# Boolean

class Baseobject:
    defaultCreator:str= "sys"
    def fullcolname(self, col):
        return self._prefix+'_'+col

    def colvalue(self,pcolname):
        return self.__dict__[pcolname.lower()] if pcolname.lower() in self.__dict__ else None
    def setcolvalue(self, pcolname, pvalue):
        self.__dict__[pcolname.lower()] = pvalue

    def setdefaultval(self, pcolname, pvalue):
        col = self.fullcolname(pcolname.lower())
        if col in self._columnlist:
            if self.colvalue(col) is None: self.setcolvalue(col, pvalue)



    def __init__(self, tablename, prefix, idcolname=None
                 , psrcname=None, pscrid=None, pmodelemtype=None):
        self._tablename: str = tablename
        self._prefix: str = prefix
        self._idcolname: str = self.fullcolname('id') if idcolname is None else idcolname
        self.__srcname = psrcname
        self.__srcid = pscrid
        self.__modelemtype = pmodelemtype
        self.__emptyclass()
    def __emptyclass(self):
        for col in self._columnlist:
            self.setcolvalue(pcolname=col,pvalue=None)
    # emptyclass

    def _semanticcols(self):
        """Return list of columns without standard management columns"""
        return list(set(self._columnlist).difference((self.fullcolname(n) for n in ['id', 'uc', 'um', 'dc', 'dm'])))

    def semanticequal(self,pbrother):
        """ true, if all semantic elements are equal. Managing attributes (id, uc,dc etc.) are excluded"""
        for sc in self._semanticcols():
            if self.colvalue(sc) != pbrother.colvalue(sc):
                return False
        return True

    def semanticcopy(self,pbrother):
        """ copies  all semantic elements. Managing attributes (id, uc,dc etc.) are excluded"""
        for sc in self._semanticcols():
            self.setcolvalue(pcolname=sc,pvalue=pbrother.colvalue(sc))

    def getname(self,plang=None):
        """if object has name, it must be overwritten"""
        return "{} ({}) has no name".format(self._prefix,self.getid())

    def toarray(self):
        return [self.__dict__[col] for col in self._columnlist]

    def totuple(self):
        return tuple(self.toarray())

    def _fromarray(self, parr):
        for key, val in enumerate(parr):
            self.__dict__[self._columnlist[key]] =val
        return self

    def getid(self):
        return self.colvalue(self._idcolname)

    def getidcolname(self):
        return self._idcolname

    def setid(self, pid):
        self.setcolvalue(pcolname=self._idcolname,pvalue=pid)

    def insert(self, pdoerrhdlng=True):
        self.setdefaultval(pcolname='dc', pvalue=datetime.today())
        self.setdefaultval(pcolname='uc', pvalue=Baseobject.defaultCreator)
        """wird erst bei  update gemacht        
        if self.colvalue(self.fullcolname('dm')) is None: self.setcolvalue(self.colvalue(self.fullcolname('dm')), datetime.today())
        if self.colvalue(self.fullcolname('um')) is None: self.setcolvalue(self.colvalue(self.fullcolname('um')), Baseobject.defaultCreator)
        """
        if self.__modelemtype is not None:
            locid = Modelelement(pid=self.getid(),pmeltshortname=self.__modelemtype).insert()
            self.setid(locid)

        lsql = """insert into {} ({}) values ({})
           """.format(self._tablename, Baseobject.columnsliststring(self._columnlist)
                      , Baseobject.columnsliststring(pcollist=self._columnlist, pplaceholder=True))
        try:
            id = dbDML.insert(lsql, self.totuple())
            if self.getid() is None: self.setid(id)  # autocolumns zurücklesen
        except sqlite3.Error as e:
            if pdoerrhdlng:
                try:
                    logmessages.writelog(str(e))
                    logmessages.writelog(self.tostring())
                    if self.__modelemtype is not None:
                        Modelelement.delete(pwhere="mode_id = {}".format(locid))
                except:
                    print ("Loggin-Error in Baseobject.insert():")
                    print(str(e))
                    print (lsql)
                    print (self.totuple())
            # if
            raise e
        # try
        if self.__srcname is not None:
            Externalref(psrcname=self.__srcname, psrcid=self.__srcid, pmodeid=self.getid()).insert(
                pdoerrhdlng=pdoerrhdlng)
        return self.getid()

    def updatedb(self, pdoerrhdlng=True):
        now = datetime.today()
        self.setcolvalue(pcolname='dm',pvalue=now)
        self.setdefaultval(pcolname='um', pvalue=Baseobject.defaultCreator)

        updcollist = self._columnlist.copy()
        updcollist.remove(self._idcolname) #ID will never be changed, it is the where-condition
        lsql = """update {} """.format(self._tablename, Baseobject.columnsliststring(updcollist))
        lsql += """\nset {}""".format('\n,'.join("""{} = {}""".format(col,dbDML.dbval(self.colvalue(pcolname=col))) for col in updcollist))
        lsql += """\nwhere {} = {}""".format(self._idcolname,dbDML.dbval(self.getid()))
        #print (lsql)
        try:
            id = dbDML.exec(lsql)
        except sqlite3.Error as e:
            if pdoerrhdlng:
                try:
                    logmessages.writelog(str(e))
                    logmessages.writelog(self.tostring())
                except:
                    print ("Loggin-Error in Baseobject.insert():")
                    print(str(e))
                    print (lsql)
                    print (self.totuple())
            # if
            raise e
        # try
        return


    def gettablecolumns(ptablename):
        sql = "PRAGMA table_info({})".format(ptablename)
        try:
            cols = dbDML.select(sql)
            retval = [c[1].lower() for c in cols]
        except:
            retval = []
        return retval

    def tostring(self):
        lretval = "Table: {}\n".format(self._tablename)
        lretval += "\n".join("{} = '{}'".format(col, self.colvalue(col)) for col in self._columnlist)
        return lretval

    def getbyid(self, pid):
        if pid is None: return None
        data = self.select(pwhere="{}={}".format(self._idcolname, pid))
        if (len(data) > 1):
            logmessages.writelog("{}: nonunique ID={}'".format(self._tablename, pid))
            raise Exception('{}: nonunique ID={}'.format(self._tablename, pid))
        elif (len(data) == 0):
            logmessages.writelog("{}: nonexistent ID={} '".format(self._tablename, pid))
            raise Exception('{}: nonexistent ID={}'.format(self._tablename, pid))
        else:
            self = data[0]
        return self

    # getbyid

    def getbyuk(self, **colvalpairs):
        """{colname:colvalue,}"""
        wherecond = dbDML.valuepairs2sqlexpr(**colvalpairs)
        data = self.select(pwhere=wherecond)
        if (len(data) > 1):
            raise Exception('{}: nonunique {}'.format(self._tablename, wherecond))
        elif (len(data) == 0):
            # self.__emptyclass()
            return None
        else:
            self = data[0]
        # fi
        return self
    # getbyuk

    def getbyanyuk(self):
        """return a new object selected with the uk-values of self.
            if there is no uk return None
            if there are several uk's
                try each one
                if a uk-select returns more than 1 row
                    error too many rows
                if the number of different rows returned from all uk's lookup
                    = 0 return None
                    = 1 return this row
                    > raise error (different rows found)
                    """
        uklist = dbDDL.getuklist(ptablename=self._tablename)
        if len(uklist) == 0: return None
        foundrows = []
        """uklist = [[colname,],]"""
        for uk in uklist:
            row = self.getbyuk(**{colname:self.colvalue(colname) for colname in uk})
            if row is not None: foundrows.append(row)
        #for
        #make a list of  all id's of the found elements
        idset = set([r.getid() for r in foundrows])
        if len(idset)== 0: return None
        if len(idset) == 1: return foundrows[0]
        raise Exception("different rows found for different uk's of table {}, id={}".format(self._tablename,self.getid()))
        return

    def prefix(self):
        return self._prefix

    def _getmode(self):
        if self.__modelemtype is None: return None
        mode = Modelelement().getbyid(self.getid())
        return mode

    def getminzoomlevel(self):
        mode = self._getmode()
        return None if mode is None else mode.mode_min_zoom_level

    def getmaxzoomlevel(self):
        mode = self._getmode()
        return None if mode is None else mode.mode_max_zoom_level

    def getdevstatus(self):
        mode = self._getmode()
        return None if mode is None else mode.mode_dev_status

    @staticmethod
    def createtable(ptablename, psql):
        dbDDL.createTable(psql)
    # createtable

    def getbyextref(self, psrcid, psrcname):
        if self.__modelemtype is None: return None
        mode = Modelelement.getmodebyextref(psrcname=psrcname, psrcid=psrcid)
        if mode is None or mode.mode_type != self.__modelemtype: return None
        return self.getbyid(mode.mode_id)

    def getIDbyextref(self, psrcid, psrcname):
        ref = self.getbyextref(psrcid=psrcid, psrcname=psrcname)
        return None if ref is None else ref.getid()

    def getbyODMref(self, psrcid):
        return self.getbyextref(psrcid=psrcid, psrcname=Externalref.SOURCE_ODM)

    def getIDbyODMref(self, psrcid):
        return self.getIDbyextref(psrcid=psrcid, psrcname=Externalref.SOURCE_ODM)

    def getsprachvals(self):
        raise NotImplementedError("Must override getsprachvals")

    def getukvaluepairs(self):
        uklist = dbDDL.getuklist(ptablename=self._tablename)
        return [dbDML.valuepairs2sqlexpr(**{colname:self.colvalue(colname) for colname in uk}) for uk in uklist]

    def getfkcolumns(self):
        """{colname: (fktable, fkcolname,fkprefix)} all names in lowercase"""
        fkcols = dbDDL.getfklist(ptablename=self._tablename)
        retval = {}
        for col, fk in fkcols.items():
            fk.append(fk[1][0:4])
            retval[col] = fk
        return retval

    @staticmethod
    def select(pclass, pwhere=None, porderby=None):
        if (len(pclass._columnlist) == 0): pclass._columnlist = Baseobject.gettablecolumns(pclass._tablename)
        lsql = """select {} from {} as {} {} {} """ \
            .format(Baseobject.columnsliststring(pclass._columnlist)
                    , pclass._tablename
                    , pclass._prefix
                    , "" if pwhere is None else
                    "where {}".format(pwhere)
                    , "" if porderby is None else
                    "order by {}".format(porderby))
        data = dbDML.select(psql=lsql)
        retval = []
        for d in data:
            obj = pclass()._fromarray(d)
            try:
                """obj ist vom Typ des Subtypes"""
                """ist in MultilangBaseobject definiert"""
                obj.getsprachvals()
            except Exception as err:
                pass
            retval.append(obj)
        return retval
    # select

    @staticmethod
    def delete(ptablename,pwhere=None):
        retval = None
        try:
            retval = dbDML.delete(ptablename,pwhere=pwhere)
        except Exception as err:
            if (not err.__str__().startswith("no such table")):
                raise err
        return retval

    @staticmethod
    def columnsliststring(pcollist, pplaceholder=False):
        return ','.join('?' if pplaceholder else col for col in pcollist)


# Baseobject

class MultilangBaseobject(Baseobject):
    def __init__(self, tablename, prefix, multilangcols
                 , idcolname=None, psrcname=None, pscrid=None, pmodelemtype=None):
        super().__init__(tablename=tablename, prefix=prefix
                         , idcolname=idcolname
                         , pmodelemtype=pmodelemtype, psrcname=psrcname, pscrid=pscrid
                         )
        self._multilangcols = multilangcols

    # __init__

    def getmodeid(self):
        raise NotImplementedError("'getmodeid' muss implementiert werden")

    def getsprachvals(self):
        for col in self._multilangcols:
            spt = Languagetext.getlang_texts(pattrname=self._multilangcols[col], pmodeid=self.getid())
            self.setcolvalue(pcolname=col + '_l', pvalue=spt)
        # for

    # getsprachvals

    def _getsprachval(self, colname, plang = None):
        try:
            retval = self.colvalue(colname + '_l')[plang]
        except:
            # keine sprache oder keinen Namen für Language
            retval = self.colvalue(colname)
        # try

        return retval
    #_getsprachval


from .languagetext import Languagetext
from .modelelement import Modelelement
from .externalref import Externalref
