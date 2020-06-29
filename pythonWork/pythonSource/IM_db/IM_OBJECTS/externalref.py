from .baseobject import Baseobject

class ExternalRef(Baseobject):
    ODM:str = 'ODM'
    _tablename:str ='externalrefs'
    _prefix:str ='extr'
    _columnlist:list = ['extr_id','extr_source','extr_obj','extr_obj_id','extr_ref']

    def __init__(self):
        super().__init__(tablename=ExternalRef._tablename,prefix=ExternalRef._prefix
                        ,columnlist = ExternalRef._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=ExternalRef._tablename
                               , psql="""
CREATE TABLE externalrefs(
    extr_id            integer primary key autoincrement,
    extr_source        VARCHAR(20) NOT NULL,
    extr_source_id     VARCHAR(250) NOT NULL,
    extr_obj           VARCHAR(50) NOT NULL,
    extr_obj_id        integer NOT NULL,
	CONSTRAINT extr_un UNIQUE(extr_source,extr_obj,extr_obj_id)
    )"""
                            )
    @staticmethod
    def delete():
        Baseobject.delete(ExternalRef._tablename)

    @staticmethod
    def select(pwhere=None,porderby=None):
        return Baseobject.select(pclass=ExternalRef
                                 ,pwhere=pwhere,porderby=porderby)
#ExternalRef

def projektlangs():
    """pwhere='select extr_sprachen from projekt'"""
    data = ExternalRef().select()
    return data[0].extr_sprachen
#
