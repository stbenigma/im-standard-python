from .baseobject import Baseobject

class Project(Baseobject):
    LOGICALTYPE = "logical"
    _tablename:str ='projects'
    _prefix:str ='proj'
    _columnlist:list = []

    def __init__(self):
        if (len(Project._columnlist) == 0): Project._columnlist = Baseobject.gettablecolumns(Project._tablename)
        super().__init__(tablename=Project._tablename, prefix=Project._prefix)


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
