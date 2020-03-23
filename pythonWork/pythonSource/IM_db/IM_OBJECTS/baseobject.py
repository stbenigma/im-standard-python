
from IM_DB import dbDDL,dbDML,dbLookup
from mystring import nvl

class Baseobject:

    def __init__(self,tablename,prefix,columnlist,idcolname = None,guidcolname = None):
        self.tablename = tablename
        self.prefix = prefix
        self.idcolname = prefix + '_id' if idcolname is None else idcolname
        self.guidcolname = prefix + '_odm_guid' if guidcolname is None else guidcolname
        self.columnlist = columnlist
        for col in columnlist:
            self.__dict__[col] = None

    def toarray(self):
        return [self.__dict__[col] for col in self.columnlist]

    def totuple(self):
        return tuple(self.toarray())

    def _fromarray(self, parr):
        for key, val in enumerate(parr):
            self.__dict__[self.columnlist[key]] = val
        return self

    def placehoderstring(self):
        return ''.join('?,' for col in self.columnlist).rstrip(',')


    def insert(self):
        lsql = """insert into {} ({}) values ({})
           """.format(self.tablename, Baseobject.columnsliststring(self.columnlist), self.placehoderstring())
        id = dbDML.insert(lsql, self.totuple())
        self.__dict__[self.idcolname] = id #autocolumns zurücklesen
    #insert

    def getbyid(self,pid):
        data = self.select(pwhere="{}={}".format(self.idcolname,pid))
        if (len(data) > 1):
            raise Exception('{}: nonunique ID={}'.format(self.tablename, pid))
        elif (len(data) == 0):
            raise Exception('{}: nonexistent ID={}'.format(self.tablename, pid))
        else:
            return data[0]
    # getbyid

    def getbyguid(self,pguid):
        data = self.select(pwhere="{}='{}'".format(self.guidcolname,pguid))
        if (len(data) > 1):
            raise Exception('{}: nonunique GUID={}'.format(self.tablename, pid))
        elif (len(data) == 0):
            record [[None for col in self.columnlist]]
        else:
            record = data[0]
        # fi
        return record
    # getbyguid

    def getID(self,pguid):
        return self.getbyguid(pguid).__dict__[self.idcolname]

    def anker(self):
        return self.prefix.upper() + nvl(str(self.__dict__[self.idcolname] or ''))

    @staticmethod
    def createtable(ptablename,psql):
        dbDDL.dropTable(ptablename);
        dbDDL.createTable(psql)
    #createtable

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

