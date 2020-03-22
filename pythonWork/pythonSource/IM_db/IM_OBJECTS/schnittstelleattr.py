from IM_DB import dbDDL,dbDML,dbLookup
from baseoject import Baseobject

class Schnittstelleattr(Baseobject):

    def __init__(self):
        baseobject.__init__(self,tablename = 'schnittstelle_attr'
                                ,prefix = 'scha'
                                ,idcolname = 'scha_id'
                                ,guidcolname= = 'scha_odm_guid')
        self.scha_id = None
        self.scha_column_name = None
        self.scha_format = None
        self.scha_fremdsystem_id = None
        self.scha_beschr = None
        self.scha_tabl_id = None
        self.scha_daty_id  None
        self.scha_odm_guid = None
        self.scha_uc = None
        self.scha_dc = None
        self.scha_um = None
        self.scha_dm = None
    def toarray(self):
        return [self.scha_id, self.scha_column_name, self.scha_format, self.scha_fremdsystem_id
                , self.scha_beschr, self.scha_tabl_id, self.scha_daty_id, self.scha_odm_guid
                , self.scha_uc, self.scha_dc, self.scha_um, self.scha_dm]
    # toarray

    def totuple(self):
        return tuple(self.toarray())

    @staticmethod
    def fromarray(self, parr):
        for key, val in enumerate(parr):
            if (key == 0):
                self.scha_id = val
            elif (key == 1):
                self.scha_column_name = val
            elif (key == 2):
                self.scha_format = val
            elif (key == 3):
                self.scha_fremdsystem_id = val
            elif (key == 4):
                self.scha_beschr = val
            elif (key == 5):
                self.scha_tabl_id = val
            elif (key == 6):
                self.scha_daty_id = val
            elif (key == 7):
                self.scha_odm_guid = val
            elif (key == 8):
                self.scha_uc = val
            elif (key == 9):
                self.scha_dc = val
            elif (key == 10):
                self.scha_um = val
            elif (key == 11):
                self.scha_dm = val
            # fi
        # for
        return self
    # fromarray

    def anker(self):
        return super.anker(pid=self.scha_id)

    def createtable():
        super.createtable("""
    create table schnittstelle_attr
    (
        scha_id             integer
            primary key autoincrement,
        scha_column_name    varchar(60) not null
            constraint scha_un
                unique,
        scha_format         varchar(200),
        scha_fremdsystem_id varchar(100),
        scha_beschr         varchar(4000),
        scha_tabl_id        integer     not null
            constraint scha_tabl_fk
                references tabelle,
        scha_daty_id        integer     not null
            constraint scha_daty_fk
                references datatypes (daty_id),
        scha_odm_guid       varchar(36),
        scha_uc             varchar(30) not null,
        scha_dc             varchar(30) not null,
        scha_um             varchar(30),
        scha_dm             varchar(30)
        )
        """)

    @staticmethod
    def insert(self):
        lsql = """insert into schnittstelle_attr
                (scha_id, scha_column_name, scha_format, scha_fremdsystem_id
                ,scha_beschr, scha_tabl_id, scha_daty_id, scha_odm_guid  
                ,scha_uc, scha_dc, scha_um, scha_dm)
                   values (?,?,?,?,?,?,?,?,?,?,?,?)
           """
        return dbDML.insert(lsql, self.totuple())
    # insertschnittstelle

    def select(pwhere=None, porderby=None):
        data = super.select(pwhere=pwhere,porderby=porderby)
        schalist = [Schnittstelleattr().fromarray(val) for key, val in enumerate(data)]
        return schalist
    # select

    def getbyid(self,pid):
        return Schnittstelleattr.fromarray(super.getbyid(pid))

    def getbyguid(pguid):
        return Schnittstelleattr.fromarray(super.getbyguid(pguid))

    def getID(pguid):
        return super.getbyguid(pguid).scha_id

    def indexlist():
        scha = self.select(porderby='scha_name')
        indexlist = [[s.scha_name, '', s.anker(), s.scha_id] for s in scha]
        return indexlist
    # indexlist
# schnittstelleattr


