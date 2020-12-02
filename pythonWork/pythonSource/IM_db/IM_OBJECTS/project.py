from .baseobject import Baseobject

class Project(Baseobject):
    LOGICALTYPE = "logical"
    _tablename:str ='projects'
    _prefix:str ='proj'
    _columnlist:list = ['proj_id', 'proj_name', 'proj_languages', 'proj_curr_lang'
                        , 'proj_uc', 'proj_dc', 'proj_um', 'proj_dm']

    def __init__(self):
        super().__init__(tablename=Project._tablename, prefix=Project._prefix
                         , columnlist = Project._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Project._tablename
                               , psql="""
CREATE TABLE projects(
    proj_id            integer primary key autoincrement,
    proj_name          VARCHAR(60) NOT NULL,
    proj_languages      VARCHAR(60),
    proj_curr_lang   VARCHAR2(2),
    proj_uc            VARCHAR(30) NOT NULL,
    proj_dc            VARCHAR(30) NOT NULL,
    proj_um            VARCHAR(30) ,
    proj_dm            VARCHAR(30) ,
	CONSTRAINT proj__un UNIQUE(proj_name)
    )"""
                            )
    @staticmethod
    def delete():
        Baseobject.delete(Project._tablename)

    @staticmethod
    def select(pwhere=None,porderby=None):
        return Baseobject.select(pclass=Project
                                 ,pwhere=pwhere,porderby=porderby)
#Project

def projektlangs():
    """pwhere='select proj_languages from projects'"""
    data = Project().select()
    return data[0].proj_languages.lower()
#
