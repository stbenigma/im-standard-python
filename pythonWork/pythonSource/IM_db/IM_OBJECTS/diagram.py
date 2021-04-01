from .baseobject import Baseobject
from .modelelement import Modelelemtype
from datetime import date
from IM_DB import dbDML

class Diagram(Baseobject):
    _tablename:str = 'diagrams'
    _prefix:str = 'diag'
    _columnlist:list = []
    _defaultorderby = "upper(diag_name)"

    def __init__(self, psrcname=None, psrcid=None):
        if (len(Diagram._columnlist) == 0): Diagram._columnlist = Baseobject.gettablecolumns(Diagram._tablename)
        super().__init__( pmodelemtype=Modelelemtype.DIAG
                         , pscrid=psrcid
                         , psrcname=psrcname
                         )
        self._diagwidth = None
        self._diagheight = None

    def __diagsize(self):
        """(width,height)"""
        diagsize = dbDML.select("""
                select max(max_x) totwidth,max(max_y) totheight
                FROM (select diag_legendx + 400 max_x,diag_legendy + 140 max_y 
                        from diagrams
                        where diag_id = {}
                    union all
                    select max(eler_position_x + eler_width) max_x,max(eler_position_y + eler_height) max_y
                     from elementreps
                     where eler_diag_id = {}
                     union all 
                     select max(relr_endtext_x)  max_x,max(relr_endtext_y)  max_y
                     from relationreps
                     where relr_diag_id={}
                     union all 
                     select max(lise_x + 3) max_x,max(lise_y + 3) max_y
                     from relationreps
                     join linesegments on lise_relr_id = relr_id
                     where relr_diag_id = {}
                    )
            """.format(self.diag_id,self.diag_id,self.diag_id,self.diag_id))
        self._diagwidth = diagsize[0][0]
        self._diagheight = diagsize[0][1]
    #__diagsize

    def diagwidth(self):
        if self._diagwidth is None : self.__diagsize()
        return self._diagwidth
    def diagheight(self):
        if self._diagheight is None : self.__diagsize()
        return self._diagheight

    def getname(self, plang=None):
        return self.diag_name


    @classmethod
    def getdiagrams(cls,pmodeid):
        diags = cls.select(pwhere=("diag_id in (select eler_diag_id "
                                       "            from elementreps where eler_mode_id = ?)", pmodeid)
                               )
        return diags

    @classmethod
    def getbyname(cls,pname):
        return cls.getbyuk(diag_name=pname)
    # getbyname

#Diagram

class Diagramtype(Baseobject):
    ENTITY:str = 'Entity'
    RELATIONAL:str = 'Relational'

    _tablename:str = 'diagramtypes'
    _prefix:str = 'diat'
    _columnlist:list = []


    def __init__(self,pname=None):
        if (len(Diagramtype._columnlist) == 0): Diagramtype._columnlist = Baseobject.gettablecolumns(Diagramtype._tablename)
        super().__init__()
        self.diat_name = pname
        self.diat_uc = 'system'
        self.diat_dc = date.today()


    def getname(self,plang=None):
        return self.diat_name

    @classmethod
    def getbyname(cls,pname):
        return cls.getbyuk(diat_name=pname)
    # getbyname
#Diagramtype

class MeltDiat(Baseobject):
    _tablename:str = 'melt_diats'
    _prefix:str = 'medi'
    _columnlist:list = []

    def __init__(self,pmeltid=None,pdiatid=None):
        _columnlist = []
        if (len(MeltDiat._columnlist) == 0): MeltDiat._columnlist = Baseobject.gettablecolumns(MeltDiat._tablename)
        super().__init__()
        self.medi_melt_id = pmeltid
        self.medi_diat_id = pdiatid
        self.medi_uc = 'system'
        self.medi_dc = date.today()


#Diagramtype
