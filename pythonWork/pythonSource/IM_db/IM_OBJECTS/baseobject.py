
from IM_DB import dbDML,dbDDL
from mystring import nvl
from logging import writelog
import sqlite3

class Boolean:
    TRUE:str='TRUE'
    FALSE:str='FALSE'
    @staticmethod
    def str2bool(pstr):
        if (pstr is None): return None
        elif (pstr.upper() in (Boolean.TRUE,'T')): return True
        elif (pstr.upper() in (Boolean.FALSE,'F')): return False
        else: raise Exception('Ungültiger Wert für Boolean "{}"'.format (pstr))
    #str2bool
    @staticmethod
    def bool2str(bool):
        return Boolean.TRUE if bool else Boolean.FALSE
    @staticmethod
    def strnegbool(pstr):
        return Boolean.bool2str( not Boolean.str2bool(pstr))
    # strNegBool
#Boolean

class Webanker:
    """enthält die Information um Web-Referenzen (Sprungziele / id) herzustellen.
         Webanker bestehen aus dem Kurznamen (prefix) des Elementes, seinem ID sowie ggf.
         dem Modelid (der dann in einen html-Dateinamen umgesetzt wird.
         Modelid =0 -> logisches Modell
    """
    def __init__(self,pname,pid,pmodelid=0):
        self._id:int = pid
        self._name:str = pname.upper()
        self._modelid:int = pmodelid
    def anker(self):
        return nvl(self._name) + str(nvl(self._id))
    def modelid(self):
        return self._modelid
#Webanker

class Baseobject:
    def __init__(self,tablename,prefix,columnlist,idcolname = None
                 ,psrcname=None,pscrid = None,pmodelemtype=None):
        self._tablename:str = tablename
        self._prefix:str = prefix
        self._idcolname:str = prefix + '_id' if idcolname is None else idcolname
        self._columnlist = columnlist
        self.__srcname=psrcname
        self.__srcid=pscrid
        self.__modelemtype=pmodelemtype
        self.__emptyclass()

    def __emptyclass(self):
        for col in self._columnlist:
            self.__dict__[col] = None
    #emptyclass

    def toarray(self):
        return [self.__dict__[col] for col in self._columnlist]

    def totuple(self):
        return tuple(self.toarray())

    def _fromarray(self, parr):
        for key, val in enumerate(parr):
            self.__dict__[self._columnlist[key]] = val
        return self

    def getid(self):
        return self.__dict__[self._idcolname]

    def setid(self,pid):
         self.__dict__[self._idcolname] = pid

    def getscrname(self):
        return self.__srcname
    def getscrid(self):
        return self.__srcid

    def insert(self,pdoerrhdlng=True):
        if self.__modelemtype is not None:
            self.setid(Modelelement(self.__modelemtype).insert())

        lsql = """insert into {} ({}) values ({})
           """.format(self._tablename, Baseobject.columnsliststring(self._columnlist)
                      , Baseobject.columnsliststring(pcollist=self._columnlist,pplaceholder=True))
        try:
            id = dbDML.insert(lsql, self.totuple())
            if self.getid() is None: self.setid(id)  # autocolumns zurücklesen
        except sqlite3.Error as e:
            if pdoerrhdlng:
                print(str(e))
                print(self.tostring())
            #if
            raise e
        #try
        if self.getscrname() is not None:
            Externalref(psrcname=self.getscrname(),psrcid = self.getscrid(),pmodeid=self.getid()).insert(pdoerrhdlng=pdoerrhdlng)
        return self.getid()

    def tostring(self):
        lretval = "Table: {}\n".format(self._tablename)
        lretval += "\n".join("{} = '{}'".format(col,self.__dict__[col]) for col in self._columnlist)
        return lretval

    def getbyid(self,pid):
        if pid is None: return None
        data = self.select(pwhere="{}={}".format(self._idcolname, pid))
        if (len(data) > 1):
            writelog("{}: nonunique ID={}'".format(self._tablename, pid))
            raise Exception('{}: nonunique ID={}'.format(self._tablename, pid))
        elif (len(data) == 0):
            writelog("{}: nonexistent ID={} '".format(self._tablename, pid))
            raise Exception('{}: nonexistent ID={}'.format(self._tablename, pid))
        else:
            self._fromarray(data[0].toarray())
        return self
    # getbyid

    def getbyuk(self,pcolname,pukvalue):
        data = self.select(pwhere="{}='{}'".format(pcolname, pukvalue))
        if (len(data) > 1):
            raise Exception('{}: nonunique {}={}'.format(self._tablename, pcolname,pukvalue))
        elif (len(data) == 0):
            #self.__emptyclass()
            return None
        else:
            self._fromarray(data[0].toarray())
        # fi
        return self
    # getbyuk

    def prefix(self):
        return self._prefix

    def webanker(self,pmodelid=0):
        return Webanker(pname=self._prefix, pid= self.getid(),pmodelid=pmodelid)

    @staticmethod
    def createtable(ptablename,psql):
        dbDDL.dropTable(ptablename);
        dbDDL.createTable(psql)
    #createtable

    def getbyextref(self,psrcid,psrcname):
        if self.__modelemtype is None : return None
        mode = Modelelement.getmodebyextref(psrcname=psrcname,psrcid=psrcid)
        if mode is None or mode.mode_type != self.__modelemtype: return None
        return self.getbyid(mode.mode_id)

    def getIDbyextref(self,psrcid,psrcname):
        ref = self.getbyextref(psrcid=psrcid,psrcname=psrcname)
        return None if ref is None else ref.getid()

    def getbyODMref(self,psrcid):
        return self.getbyextref(psrcid=psrcid,psrcname=Externalref.SOURCE_ODM)

    def getIDbyODMref(self,psrcid):
        return self.getIDbyextref(psrcid=psrcid,psrcname=Externalref.SOURCE_ODM)

    def getsprachvals(self):
        raise NotImplementedError("Must override getsprachvals")

    @staticmethod
    def select(pclass, pwhere=None, porderby=None):
        lsql = """select {} from {} as {} {} {} """ \
            .format(Baseobject.columnsliststring(pclass._columnlist)
                    , pclass._tablename
                    , pclass._prefix
                    , "" if pwhere is None else
                "where {}".format(pwhere)
                    , "" if porderby is None else
                "order by {}".format(porderby))
        data = dbDML.select(psql=lsql)
        retval =[]
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
    #select

    @staticmethod
    def delete(ptablename):
        dbDML.delete(ptablename)

    @staticmethod
    def columnsliststring(pcollist,pplaceholder=False):
        return ','.join('?' if pplaceholder else col for col in pcollist)
#Baseobject

class MultilangBaseobject(Baseobject):
    def __init__(self, tablename, prefix, columnlist, multilangcols
                 ,idcolname=None,psrcname=None,psrcid = None,pmodelemtype=None):
        super().__init__(tablename=tablename, prefix=prefix, columnlist=columnlist
                        ,idcolname=idcolname
                        ,pmodelemtype=pmodelemtype,psrcname=psrcname,pscrid=psrcid
                        )
        self._multilangcols = multilangcols
    #__init__

    def getmodeid(self):
        raise NotImplementedError("'getmodeid' muss implementiert werden")

    def getsprachvals(self):
        modeid = self.getmodeid()
        for col in self._multilangcols.keys():
            spt = Sprachtext.getsprachtexte(pattrname=self._multilangcols[col], pmodeid=modeid)
            self.__dict__[col + '_L'] = spt
        # for
    # getsprachvals

    def _getsprachval(self,colname:str,plang:str =None):
        try:
            retval = self.__dict__[colname+'_L'][plang]
        except:
            #keine sprache oder keinen Namen für Sprache
            retval = self.retval = self.__dict__[colname]
        #try
        return retval
    #getbeschr

from .sprachtext import Sprachtext
from .modelelement import Modelelement
from .externalref import Externalref

