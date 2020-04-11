
from IM_DB import dbDDL,dbDML
from mystring import nvl

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

class   Baseobject:

    def __init__(self,tablename,prefix,columnlist,idcolname = None,guidcolname = None):
        self._tablename:str = tablename
        self._prefix:str = prefix
        self._idcolname:str = prefix + '_id' if idcolname is None else idcolname
        self._guidcolname:str = prefix + '_odm_guid' if guidcolname is None else guidcolname
        self._columnlist = columnlist
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

    def placehoderstring(self):
        return ''.join('?,' for col in self._columnlist).rstrip(',')

    def insert(self):
        lsql = """insert into {} ({}) values ({})
           """.format(self._tablename, Baseobject.columnsliststring(self._columnlist), self.placehoderstring())
        id = dbDML.insert(lsql, self.totuple())
        self.__dict__[self._idcolname] = id #autocolumns zurücklesen
    #insert

    def getbyid(self,pid):
        data = self.select(pwhere="{}={}".format(self._idcolname, pid))
        if (len(data) > 1):
            raise Exception('{}: nonunique ID={}'.format(self._tablename, pid))
        elif (len(data) == 0):
            raise Exception('{}: nonexistent ID={}'.format(self._tablename, pid))
        else:
            self._fromarray(data[0].toarray())
        return self
    # getbyid

    def getbyguid(self,pguid):
        data = self.select(pwhere="{}='{}'".format(self._guidcolname, pguid))
        if (len(data) > 1):
            raise Exception('{}: nonunique GUID={}'.format(self._tablename, pid))
        elif (len(data) == 0):
            self.__emptyclass()
        else:
            self._fromarray(data[0].toarray())
        # fi
        return self
    # getbyguid

    def prefix(self):
        return self._prefix

    def getID(self,pguid):
        self.getbyguid(pguid)
        return self.__dict__[self._idcolname]

    def webanker(self,pmodelid=0):
        return Webanker(pname=self._prefix, pid= self.__dict__[self._idcolname],pmodelid=pmodelid)

    @staticmethod
    def createtable(ptablename,psql):
        dbDDL.dropTable(ptablename);
        dbDDL.createTable(psql)
    #createtable

    @staticmethod
    def select(pwhere=None, porderby=None):
        pass # Method filled by sub-class

    @staticmethod
    def select(pclass, pwhere=None, porderby=None):
        lsql = """select {} from {} {} {} """ \
            .format(Baseobject.columnsliststring(pclass._columnlist)
                    , pclass._tablename
                    , "" if pwhere is None else
                "where {}".format(pwhere)
                    , "" if porderby is None else
                "order by {}".format(porderby))
        data = dbDML.select(psql=lsql)
        return [pclass()._fromarray(d) for d in data]
    #select

    @staticmethod
    def delete(ptablename):
        dbDML.delete(ptablename)

    @staticmethod
    def columnsliststring(pcollist):
        return ''.join(col + ',' for col in pcollist).rstrip(',')

#Baseobject

def webanker(pclass,pid):
    o = pclass()
    o.getbyid(pid)
    return o.webanker()

