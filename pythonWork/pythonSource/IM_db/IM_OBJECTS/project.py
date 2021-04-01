from .baseobject import Baseobject
from IM_DB import dbDML

class Project(Baseobject):
    LOGICALTYPE = "logical"
    _tablename:str ='projects'
    _prefix:str ='proj'
    _columnlist:list = []

    def __init__(self):
        if (len(Project._columnlist) == 0): Project._columnlist = Baseobject.gettablecolumns(Project._tablename)
        super().__init__()


    @staticmethod
    def updlanguages(piso2list):
        langs = ','.join(iso2.upper() for iso2 in piso2list)
        """as we have only one project, do it for all"""
        lsql = """update projects set proj_languages = '{}'""".format(langs)
        dbDML.exec(lsql)

#Project

def projektlangs():
    """pwhere='select proj_languages from projects'"""
    data = Project.select()
    return data[0].proj_languages.lower()
#
