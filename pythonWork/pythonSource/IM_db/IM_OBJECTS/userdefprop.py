from .baseobject import Baseobject
from IM_DB import dbDML

class Userdefprop(Baseobject):
    _tablename: str = 'benudef_eigenschaft'
    _prefix: str = 'bdeg'
    _columnlist: list = []

    @staticmethod
    def setdomid(pdomid:int, pudpid:int):
        dbDML.exec("""update {}  set bdeg_wrtb_id = {}  where bdeg_Id = {} """
                        .format(Userdefprop._tablename,pdomid, pudpid))
    #setdomid

#Userdefprop

class Userdefpropvalue(Baseobject):
    _tablename:str = 'benudef_wert'
    _prefix:str = 'bdwe'
    _columnlist:list = []

    @staticmethod
    def removeemptyUDP(pempties):
        emptylist = ','.join("'{}'".format(e) for e in pempties)
        print (emptylist)
        dbDML.exec("""delete from {} 
                        where bdwe_wert is null
                            or bdwe_wert  in ({})""".format(Userdefpropvalue._tablename,emptylist))
    #removeemptydup
    @staticmethod
    def updvalues(prows):
        """[(value,modeid,udpid),...]"""
        dbDML.execmany(psql="""update benudef_wert
                            set bdwe_wert = ?
                            where bdwe_mode_id = ?
                            and bdwe_bdeg_id = ?
                        """, recs=prows)
    #updvalues

# Userdefpropvalue