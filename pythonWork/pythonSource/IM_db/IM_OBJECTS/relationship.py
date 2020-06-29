from .baseobject import Baseobject
from datetime import datetime

class Arc(Baseobject):
    _tablename:str ='arcs'
    _prefix:str ='arcs'
    _columnlist:list = ['arcs_id', 'arcs_name', 'arcs_enti_id','arcs_odm_guid'
                        ,'arcs_uc', 'arcs_dc','arcs_um','arcs_dm' ]

    def __init__(self,pname,pentiid,podmguid,puc,pdc=None):
        super().__init__(tablename=Arc._tablename,prefix=Arc._prefix
                        ,columnlist = Arc._columnlist)
        self.arcs_name = pname
        self.arcs_enti_id = pentiid
        self.arcs_odm_guid = podmguid
        self.arcs_uc = puc
        self.arcs_dc = pdc if (pdc is not None) else str(datetime)
    #__init__

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Arc._tablename
                               , psql="""
CREATE TABLE arcs(
    arcs_id        integer  not null primary key autoincrement,
    arcs_name      VARCHAR2(60) NOT NULL,
    arcs_enti_id   integer NOT NULL,
	arcs_odm_guid		varchar(36),
    arcs_uc        VARCHAR2(30) NOT NULL,
    arcs_dc        varchar(30) NOT NULL,
    arcs_um        VARCHAR2(30) NULL,
    arcs_dm        varchar(30) NULL,
	UNIQUE(arcs_enti_id,arcs_name),
	CONSTRAINT arcs_enti_fk FOREIGN KEY(arcs_enti_id)
	        REFERENCES entitaeten(enti_id) ON DELETE CASCADE
)
    """
                            )
    def relalist(self):
        """List of relations in this arc"""
        return Relation().select(pwhere="arcs_id = {}".format(self.arcs_id))

    @staticmethod
    def delete():
        Baseobject.delete(Arc._tablename)

    @staticmethod
    def select(pwhere=None,porderby=None):
        return Baseobject.select(pclass=Arc
                                 ,pwhere=pwhere,porderby=porderby)
#Arc

