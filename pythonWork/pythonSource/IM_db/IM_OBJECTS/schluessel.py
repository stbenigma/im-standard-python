from .baseobject import Baseobject

class Schluessel(Baseobject):
    _tablename:str = 'schluessel'
    _prefix:str = 'schl'
    _columnlist:list = ['schl_id', 'schl_laufnr', 'schl_name'
                    ,'schl_odm_guid', 'schl_uc', 'schl_dc'
                    ,'schl_enti_id']

    def __init__(self):
        super().__init__(tablename= Schluessel._tablename, prefix= Schluessel._prefix
                        ,columnlist = Schluessel._columnlist)
        self._schluesselelement = None

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Schluessel._tablename
                                ,psql="""
CREATE TABLE schluessel(
    schl_id        integer NOT NULL primary key autoincrement,
    schl_laufnr    integer NOT NULL,
	schl_name	varchar(60),
	schl_odm_guid		varchar(36),
    schl_uc varchar(30),
    schl_dc varchar(30),
    schl_enti_id   integer NOT NULL,
	unique (schl_enti_id,schl_laufnr),
	foreign key (schl_enti_id) references entitaeten(enti_id) ON DELETE CASCADE
)
""")

    def getschluesselelement(self):
        if (self.getid() is not None) and (self._schluesselelement is None):
            self._schluesselelement = Schluesselelement.select(pwhere='scel_schl_id = {}'.format(self.getid()))
        # fi
        return self._schluesselelement
    #getschluesselelement

    @staticmethod
    def delete():
        Baseobject.delete(Schluessel._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Schluessel, pwhere=pwhere, porderby=porderby) 
#Schluessel
    
class Schluesselelement(Baseobject):
    _tablename:str = 'schluesselelement'
    _prefix:str = 'scel'
    _columnlist:list = ['scel_id','scel_schl_id','scel_attr_id','scel_bezi_id'
                        , 'scel_uc', 'scel_dc','scel_um','scel_dm']


    def __init__(self):
        super().__init__(tablename= Schluesselelement._tablename, prefix= Schluesselelement._prefix
                        ,columnlist = Schluesselelement._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Schluesselelement._tablename
                                ,psql="""
CREATE TABLE schluesselelement(
    scel_id        integer NOT NULL primary key autoincrement,
    scel_schl_id   integer NOT NULL,
    scel_attr_id   integer ,
    scel_bezi_id   integer ,
    scel_uc         varchar(30) NOT NULL,
    scel_dc        varchar(30) NOT NULL,
    scel_um        varchar(30),
    scel_dm        varchar(30),
	UNIQUE(scel_schl_id,scel_attr_id,scel_bezi_id),
	CONSTRAINT scel_element_ck CHECK((scel_attr_id IS NOT NULL
                                   AND scel_bezi_id IS NULL)
                                  OR(scel_attr_id IS NULL
                                     AND scel_bezi_id IS NOT NULL)),
	FOREIGN KEY(scel_attr_id)
        REFERENCES attributes(attr_id)
            ON DELETE CASCADE,
	FOREIGN KEY(scel_bezi_id)
        REFERENCES beziehungen(bezi_id)
            ON DELETE CASCADE,
	FOREIGN KEY(scel_schl_id)
        REFERENCES schluessel(schl_id)
            ON DELETE CASCADE
		)
""")

    @staticmethod
    def delete():
        Baseobject.delete(Schluesselelement._tablename)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Schluesselelement, pwhere=pwhere, porderby=porderby) 
#Schluesselelement


