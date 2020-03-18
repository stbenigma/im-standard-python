from IM_DB import dbDDL,dbDML,dbLookup
from datetime import date

class tabelle:
    def __init__(self):
        self.tabl_id = None
        self.tabl_name = None
        self.tabl_schn_id = None
        self.tabl_prefix = None
        self.tabl_beschr = None
        self.tabl_odm_guid = None
        self.tabl_uc = None
        self.tabl_dc = None
        self.tabl_um = None
        self.tabl_dm = None
    def toarray(self):
        return [	self.tabl_id, 	self.tabl_name, 	self.tabl_schn_id
                ,  self.tabl_prefix, 	self.tabl_beschr, 	self.tabl_odm_guid
                ,self.tabl_uc, 	self.tabl_dc, 	self.tabl_um, 	self.tabl_dm]
    #toarray

    def totuple(self):
        return tuple(self.toarray())

    def fromarray(self,parr):
        for key,val in enumerate(parr):
            if (key == 0):
                self.tabl_id = val
            elif (key == 1):
                self.tabl_name = val
            elif (key == 2):
                self.tabl_schn_id = val
            elif (key == 3):
                self.tabl_prefix = val
            elif (key == 4):
                self.tabl_beschr = val
            elif (key == 5):
                self.tabl_odm_guid = val
            elif (key == 6):
                self.tabl_dm = val
            elif (key == 7):
                self.tabl_dc = val
            elif (key == 8):
                self.tabl_um = val
            elif (key == 9):
                self.tabl_dm = val
            #fi
        #for
        return self
    #fromarray
    def anker(self):
        return anker(self.tabl_id)

#tabelle

tablename:str = 'tabelle'
prefix:str = 'tabl'

def createtable():
    dbDDL.dropTable(tablename);
    dbDDL.createTable("""
    CREATE TABLE {} 
        (
         TABL_ID integer primary key autoincrement , 
         TABL_NAME VARCHAR (60) NOT NULL , 
         TABL_SCHN_ID integer NOT NULL , 
         TABL_PREFIX VARCHAR (60) NULL , 
         TABL_BESCHR VARCHAR (4000) NULL , 
     	 TABL_odm_guid	varchar(36),
         TABL_UC VARCHAR (30) NOT NULL , 
         TABL_DC VARCHAR (30) NOT NULL , 
         TABL_UM VARCHAR (30) NULL , 
         TABL_DM VARCHAR (30) NULL ,
    	  CONSTRAINT TABL_UN UNIQUE (TABL_SCHN_ID , TABL_NAME)
     	   ,CONSTRAINT TABL_SCHN_FK FOREIGN KEY (TABL_SCHN_ID) 
     	      REFERENCES SCHNITTSTELLE (SCHN_ID ) 
        )
    """.format(tablename))

def insert(ptabl):
    lsql = """insert into {} 
                (	tabl_id, 	tabl_name, 	tabl_schn_id, 	tabl_prefix, 	tabl_beschr
                , 	tabl_odm_guid, 	tabl_uc, 	tabl_dc, 	tabl_um, 	tabl_dm)
                   values (?,?,?,?,?,?,?,?,?,?)
           """.format(tablename)
    return dbDML.insert(lsql, ptabl.totuple())
#insertschnittstelle

def select (pwhere=None,porderby=None):
    lsql = """select * from {} {} {} """\
        .format(tablename
                ,"" if pwhere is  None else
                    "where {}".format(pwhere)
                ,"" if porderby is None else
                  "order by {}".format(porderby))
    data = dbDML.select(psql=lsql)
    tabllist =[tabelle().fromarray(val) for key,val in enumerate(data)]
    return tabllist
#getbyid

def getbyid (pid):
    data=select ("tabl_id={}".format(pid))
    if (len(data)>1):
        raise Exception('{}: nonunique ID={}'.format(tablename,pid))
    elif (len(data)==0):
        raise Exception('{}: nonexistent ID={}'.format(tablename,pid))
    else:
        return data[0]
    #fi
#getbyid

def getbyguid (pguid):
    return select (pwhere="tabl_odm_guid = '{}'".format(pguid))
#getbyguid

def tablID (pguid):
    data = getbyguid(pguid)
    if (len(data) > 1):
        raise Exception('{}: nonunique GUID={}'.format(tablename, pguid))
    elif (len(data) == 0):
        return None #nichst gefunden ist NULL
    else:
        return data[0].tabl_id
    # fi
#tablId

def delete():
    dbDML.delete(tablename)

def anker(id):
    return prefix.upper()+str(id)

def indexlist(pschnid=None):
    data = select(pwhere= None if pschnid is None else "tabl_schn_id={}".format(pschnid)
                  ,porderby='tabl_name')
    indexlist = [[d.tabl_name,d.anker(),d.tabl_id] for d in data]
    return indexlist
#indexlist
