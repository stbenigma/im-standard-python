
from IM_DB import dbDDL,dbDML
from mystring import nvl

class Boolean:
    TRUE:str='TRUE'
    FALSE:str='FALSE'
    @staticmethod
    def str2bool(pstr):
        if (pstr is None): return None
        elif (pstr.upper() in (TRUE,'T')): return True
        elif (pstr.upper() in (FALSE,'F')): return False
        else: raise Exception('Ungültiger Wert für Boolean "{}"'.format (pstr))
    #str2bool
    @staticmethod
    def bool2str(bool):
        return TRUE if bool else False
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

    def getid(self):
        return self.__dict__[self._idcolname]

    def insert(self):
        lsql = """insert into {} ({}) values ({})
           """.format(self._tablename, Baseobject.columnsliststring(self._columnlist), self.placehoderstring())
        id = dbDML.insert(lsql, self.totuple())
        self.__dict__[self._idcolname] = id #autocolumns zurücklesen
        return id
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

    def getbyuk(self,pcolname,pukvalue):
        data = self.select(pwhere="{}='{}'".format(pcolname, pukvalue))
        if (len(data) > 1):
            raise Exception('{}: nonunique {}={}'.format(self._tablename, pcolname,pukvalue))
        elif (len(data) == 0):
            self.__emptyclass()
        else:
            self._fromarray(data[0].toarray())
        # fi
        return self
    # getbyuk

    def getbyguid(self,pguid):
        return self.getbyuk(pcolname=self._guidcolname, pukvalue=pguid)
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

#    @staticmethod
#    def select(pwhere=None, porderby=None):
#        raise NotImplementedError("Must override select")

    def getsprachvals(self):
        raise NotImplementedError("Must override getsprachvals")

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
        retval =[]
        for d in data:
            obj = pclass()._fromarray(d)
            """obj ist vom Typ des Subtypes"""
            try:
                """ist in MultilangBaseobject definiert"""
                obj.getsprachvals()
            except:
                pass
            retval.append(obj)
        return retval
    #select

    @staticmethod
    def delete(ptablename):
        dbDML.delete(ptablename)

    @staticmethod
    def columnsliststring(pcollist):
        return ''.join(col + ',' for col in pcollist).rstrip(',')

#Baseobject

class MultilangBaseobject(Baseobject):
    def __init__(self, tablename, prefix, columnlist, multilangcols
                 ,idcolname=None, guidcolname=None):
        super().__init__(tablename=tablename, prefix=prefix, columnlist=columnlist
                        ,idcolname=idcolname, guidcolname=guidcolname
                        )
        self._multilangcols = multilangcols
    #__init__

    def getmodeid(self):
        raise NotImplementedError("'getmodeid' muss implementiert werden")

    def getsprachvals(self):
        modeid = self.getmodeid()
        for col in self._multilangcols.keys():
            self.__dict__[col + '_L'] = Sprachtext.getsprachtexte(pattrname=self._multilangcols[col],pmodeid=modeid)
        # for
    # getsprachvals

    def _getsprachval(self,colname,plang=None):
        try:
            retval = self.__dict__[colname+'_L'][plang]
        except:
            #keine sprache oder keinen Namen für Sprache
            retval = self.retval = self.__dict__[colname]
        #try
        return retval
    #getbeschr


#MultilangBaseobject
#def webanker(pclass,pid):
#    o = pclass()
#    o.getbyid(pid)
#    return o.webanker()

