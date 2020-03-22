
from IM_DB import dbDDL,dbDML,dbLookup
from mystring import nvl

class Baseobject:

    def __init__(self,tablename,prefix,columnlist,idcolname = None,guidcolname = None):
        self.tablename = tablename
        self.prefix = prefix
        self.idcolname = prefix + '_id'  if idcolname is None else idcolname
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

    def createtable(self,psql):
        dbDDL.dropTable(self.tablename);
        dbDDL.createTable(psql)
    #createtable

    def columnsliststring(self):
        return ''.join(col + ',' for col in self.columnlist).rstrip(',')
    def placehoderstring(self):
        return ''.join('?,' for col in self.columnlist).rstrip(',')

    def select(self,pwhere=None, porderby=None):
        lsql = """select {} from {} {} {} """ \
            .format(self.columnsliststring()
                , self.tablename
                , "" if pwhere is None else
                "where {}".format(pwhere)
                , "" if porderby is None else
                "order by {}".format(porderby))
        data = dbDML.select(psql=lsql)
        return data
    # select

    def insert(self):
        lsql = """insert into {} ({}) values ({})
           """.format(self.tablename, self.columnsliststring(), self.placehoderstring())
        id = dbDML.insert(lsql, self.totuple())
        self.getbyid(id) #autocolumns zurücklesen
    #insert

    def getbyid(self,pid):
        data = self.select(pwhere="{}={}".format(self.idcolname,pid))
        if (len(data) > 1):
            raise Exception('{}: nonunique ID={}'.format(self.tablename, pid))
        elif (len(data) == 0):
            raise Exception('{}: nonexistent ID={}'.format(self.tablename, pid))
        else:
            self._fromarray(data[0])
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
        self._fromarray(record)
        return self
    # getbyguid

    def getID(self,pguid):
        return self.getbyguid(pguid).__dict__[self.idcolname]

    def delete(self):
        dbDML.delete(self.tablename)

    def anker(self):
        return self.prefix.upper() + nvl(str(self.__dict__[self.idcolname] or ''))
#Baseobject

