from IM_DB import dbDDL,dbDML,dbLookup
from datetime import date

class schnittstelle:
    def __init__(self):
        self.schn_id = None
        self.schn_name = None
        self.schn_beschr = None
        self.schn_odm_guid = None
        self.schn_uc = None
        self.schn_dc = None
        self.schn_um = None
        self.schn_dm = None
    def toarray(self):
        return [self.schn_id,  self.schn_name,    self.schn_beschr
                ,self.schn_odm_guid,   self.schn_uc,  self.schn_dc
                ,self.schn_um, self.schn_dm]
    #toarray

    def totuple(self):
        return tuple(self.toarray())

    def fromarray(self,parr):
        for key,val in enumerate(parr):
            if (key == 0): self.schn_id = val
            elif (key == 1): self.schn_name = val
            elif (key == 2): self.schn_beschr = val
            elif (key == 3): self.schn_odm_guid = val
            elif (key == 4): self.schn_dm = val
            elif (key == 5): self.schn_dc = val
            elif (key == 6): self.schn_um = val
            elif (key == 7): self.schn_dm = val
            #fi
        #for
        return self
    #fromarray

    def webfilespec(self):
        return self.schn_name.upper() + '.html'

    def anker(self):
        return anker (self.schn_id)

#schnittstelle

tablename:str = 'schnittstelle'
prefix:str = 'schn'

def createtable():
    dbDDL.dropTable(tablename);
    dbDDL.createTable("""
CREATE TABLE {} 
    (
     SCHN_ID integer primary key autoincrement, 
     SCHN_NAME VARCHAR (60) NOT NULL , 
     SCHN_BESCHR VARCHAR (4000)  , 
 	 SCHN_odm_guid	varchar(36),
     SCHN_UC VARCHAR (30) NOT NULL , 
     SCHN_DC VARCHAR (30) NOT NULL , 
     SCHN_UM VARCHAR (30) NULL , 
     SCHN_DM VARCHAR (30) NULL ,
 CONSTRAINT SCHN_UN UNIQUE (SCHN_NAME)
    )
    """.format(tablename))

def insert(pschn):
    lsql = """insert into {} 
                (schn_id,schn_name, schn_beschr, schn_odm_guid,schn_uc, schn_dc,schn_um,schn_dm)
                   values (?,?,?,?,?,?,?,?)
           """.format(tablename)
    return dbDML.insert(lsql, pschn.totuple())
#insertschnittstelle

def select (pwhere=None,porderby=None):
    lsql = """select * from {} {} {} """\
        .format(tablename
                ,"" if pwhere is  None else
                    "where {}".format(pwhere)
                ,"" if porderby is None else
                  "order by {}".format(porderby))
    data = dbDML.select(psql=lsql)
    schnlist =[schnittstelle().fromarray(val) for key,val in enumerate(data)]
    return schnlist
#select

def getbyid (pid):
    data=select ("schn_id={}".format(pid))
    if (len(data)>1):
        raise Exception('{}: nonunique ID={}'.format(tablename,pid))
    elif (len(data)==0):
        raise Exception('{}: nonexistent ID={}'.format(tablename,pid))
    else:
        return data[0]
    #fi
#getbyid

def getbyguid (pguid):
    return select ("schn_odm_guid = '{}'".format(pguid))
#getbyguid

def schnID (pguid):
    data = getbyguid(pguid)
    if (len(data) > 1):
        raise Exception('{}: nonunique GUID={}'.format(tablename, pguid))
    elif (len(data) == 0):
        return None #nichst gefunden ist NULL
    else:
        return data[0].schn_id
    # fi
#schnId
def delete():
    dbDML.delete(tablename)

def anker(id):
    return prefix.upper()+str(id)

def webfilespec(pid):
    return getbyid(pid).webfilespec()

def indexlist():
    schn = select(porderby='schn_name')
    indexlist = [[s.schn_name, '',s.webfilespec(), s.schn_id] for s in schn]
    return indexlist
#indexlist
