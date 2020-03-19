
from IM_DB import dbDDL,dbDML,dbLookup

class Baseobject:

    def __init__(self):
        pass
    def toarray(self):
        return []

    def totuple(self):
        return tuple(self.toarray())

    @staticmethod
    def createtable(psql,ptablename):
        dbDDL.dropTable(ptablename);
        dbDDL.createTable(psql.format(ptablename))
    #createtable
    @staticmethod
    def select(ptablename,pwhere=None, porderby=None):
        lsql = """select * from {} {} {} """ \
            .format(ptablename
                , "" if pwhere is None else
                "where {}".format(pwhere)
                , "" if porderby is None else
                "order by {}".format(porderby))
        data = dbDML.select(psql=lsql)
        return data
    # select

    @staticmethod
    def getbyid(pid,pidcol,ptablename):
        data = select("{}={}".format(pidcol,pid))
        if (len(data) > 1):
            raise Exception('{}: nonunique ID={}'.format(ptablename, pid))
        elif (len(data) == 0):
            raise Exception('{}: nonexistent ID={}'.format(ptablename, pid))
        else:
            return data[0]
        # fi
    # getbyid

    @staticmethod
    def getbyguid(pguid,pguidcol,ptablename):
        return select(ptablename=ptablename
                    ,pwhere="{} = '{}'".format(pguidcol,pguid))
    # getbyguid

    @staticmethod
    def getID(pguid,pguidcol,ptablename):
        data = getbyguid(pguid,ptablename,pguidcol)
        if (len(data) > 1):
            raise Exception('{}: nonunique GUID={}'.format(ptablename, pguid))
        elif (len(data) == 0):
            return None  # nichst gefunden ist NULL
        else:
            return data[0][0] #make sure id is always the first element in object
        # fi
    #getID
    @staticmethod
    def delete(ptablename):
        dbDML.delete(ptablename)

    @staticmethod
    def anker(pid,pprefix):
        return pprefix.upper() + str(pid)
#Baseobject

