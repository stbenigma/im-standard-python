from .baseobject import Baseobject
from SSOT_db.SQL_INFRA import dbDML


class Project(Baseobject):
    LOGICALTYPE = "logical"
    _tablename:str ='projects'
    _prefix:str ='proj'
    _idcolname: str = _prefix + '_id'
    _columnlist = dict()

    def __init__(self):
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
