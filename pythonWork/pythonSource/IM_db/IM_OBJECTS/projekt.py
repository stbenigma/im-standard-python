from .baseobject import Baseobject

class Projekt(Baseobject):
    _tablename:str ='projekte'
    _prefix:str ='proj'
    _columnlist:list = ['proj_id', 'proj_name', 'proj_uc', 'proj_dc', 'proj_sprachen', 'proj_akt_sprache' ]

    def __init__(self):
        super().__init__(tablename=Projekt._tablename,prefix=Projekt._prefix
                        ,columnlist = Projekt._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Projekt._tablename
                               , psql="""
CREATE TABLE projekte(
    proj_id            integer primary key autoincrement,
    proj_name          VARCHAR(60) NOT NULL,
    proj_uc            VARCHAR(30) NOT NULL,
    proj_dc            VARCHAR(30) NOT NULL,
    proj_sprachen      VARCHAR(60),
    proj_akt_sprache   VARCHAR2(2),
	CONSTRAINT proj__un UNIQUE(proj_name)
    )"""
                            )
    @staticmethod
    def delete():
        Baseobject.delete(Projekt._tablename)

    @staticmethod
    def select(pwhere=None,porderby=None):
        return Baseobject.select(pclass=Projekt
                                 ,pwhere=pwhere,porderby=porderby)
#Projekt

def projektlangs():
    """pwhere='select proj_sprachen from projekt'"""
    data = Projekt().select()
    return data[0].proj_sprachen
#
