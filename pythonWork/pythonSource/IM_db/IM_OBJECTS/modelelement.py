from datetime import date
from .baseobject import Baseobject, Boolean
from IM_DB import dbDML

class Modelelemtype(Baseobject):
    ENTI: str = 'ENTI'
    BURU: str = 'BURU'
    SYNO: str = 'SYNO'
    RELA: str = 'RELA'
    ATTR: str = 'ATTR'
    DOMA: str = 'DOMA'
    ORGU: str = 'ORGU'
    TABL: str = 'TABL'
    INTF: str = 'INTF'
    COLU: str = 'COLU'
    ARCS: str = 'ARCS'
    DOCU: str = 'DOCU'
    KEYS: str = 'KEYS'
    DATY: str = 'DATY'
    DGRM: str = 'DGRM'
    DIAG: str = 'DIAG'
    PHYU: str = 'PHYU'
    STFO: str = 'STFO'
    UDPR: str = 'UDPR'

    _tablename: str = 'modelelem_type'
    _prefix: str = 'melt'
    _columnlist = []

    def __init__(self, pshortname=None, pname=None):
        if (len(Modelelemtype._columnlist) == 0): Modelelemtype._columnlist = Baseobject.gettablecolumns(Modelelemtype._tablename)
        super().__init__(tablename=Modelelemtype._tablename, prefix=Modelelemtype._prefix)
        self.melt_shortname = pshortname
        self.melt_name = pname
        self.melt_uc = 'SYS'
        self.melt_dc = date.today()
        return

    @staticmethod
    def delete(pwhere=None):
        return Baseobject.delete(Modelelemtype._tablename)
        return

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Modelelemtype, pwhere=pwhere, porderby=porderby)

    def getname(self,plang=None):
        return self.melt_name

    @staticmethod
    def fillmelt():
        # melt_shortname,  melt_name    ,melt_uc,  melt_dc
        Modelelemtype(pshortname=Modelelemtype.ARCS, pname='Arc').insert()
        Modelelemtype(pshortname=Modelelemtype.ATTR, pname='Attribute').insert()
        Modelelemtype(pshortname=Modelelemtype.BURU, pname='Business Rule').insert()
        Modelelemtype(pshortname=Modelelemtype.COLU, pname='Column').insert()
        Modelelemtype(pshortname=Modelelemtype.DOMA, pname='Domain').insert()
        Modelelemtype(pshortname=Modelelemtype.ENTI, pname='Entity').insert()
        Modelelemtype(pshortname=Modelelemtype.INTF, pname='Interface').insert()
        Modelelemtype(pshortname=Modelelemtype.ORGU, pname='Organizational Unit').insert()
        Modelelemtype(pshortname=Modelelemtype.RELA, pname='Relation').insert()
        Modelelemtype(pshortname=Modelelemtype.SYNO, pname='Synonym').insert()
        Modelelemtype(pshortname=Modelelemtype.TABL, pname='Table').insert()
        Modelelemtype(pshortname=Modelelemtype.DATY, pname='Datatyope').insert()
        Modelelemtype(pshortname=Modelelemtype.KEYS, pname='Key').insert()
        Modelelemtype(pshortname=Modelelemtype.DOCU, pname='Document').insert()
        Modelelemtype(pshortname=Modelelemtype.DGRM, pname='Domaingroupmember').insert()
        Modelelemtype(pshortname=Modelelemtype.DIAG, pname='Diagram').insert()

    @staticmethod
    def getidbyshortname(pshortname):
        melt = Modelelemtype.select(pwhere=("melt_shortname = ?", pshortname))
        if melt is None or (len(melt)==0): return None
        return melt[0].melt_id

    @staticmethod
    def getshortname(pmeltid):
        return Modelelemtype().getbyid(pmeltid).melt_shortname

    @staticmethod
    def getbyshortname(pshortname):
        return Modelelemtype().getbyid(Modelelemtype.getidbyshortname(pshortname))

    @staticmethod
    def type2melt(type):
        trans = {"Entity": Modelelemtype.ENTI
            , "Attribute": Modelelemtype.ATTR
            , "Relation": Modelelemtype.RELA
            , "Table": Modelelemtype.TABL
            , "Column": Modelelemtype.INTF
            , "Arcs": Modelelemtype.ARCS
            , "FKIndexAssociation": ""
                 }
        if type in trans: return trans[type]
        else: return ""

# Modelelemtype

class Modelelement(Baseobject):
    """Modelelement is a supertype of a lot of entities. It shares common attributes and relationships
        It's ID is identical to id's in subtype tables.
        So Modelelement is created first (with a system generated ID, unique over all subtables). It's ID is then
        used as ID' of the subtables
    """
    _tablename: str = 'modelelement'
    _prefix: str = 'mode'
    _columnlist: list = []

    def __init__(self, pid=None,pmeltshortname=None):
        if (len(Modelelement._columnlist) == 0): Modelelement._columnlist = Baseobject.gettablecolumns(Modelelement._tablename)
        super().__init__(tablename=Modelelement._tablename, prefix=Modelelement._prefix)
        self.mode_type = pmeltshortname
        self.mode_id = pid
        if pmeltshortname is not None: self.mode_melt_id = Modelelemtype.getidbyshortname(pshortname=pmeltshortname)
    # __init__

    """Mapping of mode attributes to udp-names  in ODM"""
    ODMattrmapping = {'mode_min_zoom_level': 'minzoomlevel'
                    ,'mode_max_zoom_level': 'maxzoomlevel'
                    ,'mode_dev_status': 'dev_status'
                    ,'attr_is_descriptive': 'isdescriptive'}



    @staticmethod
    def longdevstatus(pdbvalue):
        longstati = {'DEV':'Development'
                     ,'TEST': 'Test'
                     ,'REL': 'Released'}
        if pdbvalue in longstati: return longstati[pdbvalue]
        return None


    @staticmethod
    def delete(pwhere=None):
        return Baseobject.delete(Modelelement._tablename,pwhere=pwhere)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Modelelement
                                 , pwhere=pwhere, porderby=porderby)

    @staticmethod
    def getmodebyextref(psrcname, psrcid):
        modeid = Externalref.getmodeid(psrcname=psrcname, psrcid=psrcid)
        return None if modeid is None else Modelelement().getbyid(pid=modeid)

    @staticmethod
    def getmodebyodmguid(psrcid):
        return Modelelement.getmodebyextref(psrcname=Externalref.SOURCE_ODM,psrcid=psrcid)

    def getmyelement(self):
        if self.mode_type == Modelelemtype.SYNO:
            element = Synonym().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.DOMA:
            element = Domain().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.ATTR:
            element = Attribute().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.BURU:
            element = Buseinssrule().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.RELA:
            element = Relation().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.ENTI:
            element = Entity().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.ORGU:
            element = OragnisationalUnit().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.TABL:
            element = Table().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.COLU:
            element = Column().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.INTF:
            element = Interface().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.ARCS:
            element = Arc().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.DGRM:
            element = DefaultGroupMember().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.DATY:
            element = Datatype().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.KEYS:
            element = Key().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.DIAG:
            element = Diagram().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.DOCU:
            element = Document().getbyid(self.mode_id)
        else:
            element = None
        return element

    @staticmethod
    def getelement(pmodeid):
        mode = Modelelement().getbyid(pid=pmodeid)
        return None if mode is None else mode.getmyelement()


    @staticmethod
    def getelementbyextref(psrcname, psrcid):
        return Modelelement.getelement(pmodeid=Externalref.getmodeid(psrcname=psrcname, psrcid=psrcid))

    @staticmethod
    def getelementbyodmguid(psrcid):
        return Modelelement.getelementbyextref(psrcname=Externalref.SOURCE_ODM, psrcid=psrcid)

    @staticmethod
    def select(pwhere=None, porderby=None):
        return Baseobject.select(pclass=Modelelement, pwhere=pwhere, porderby=porderby)

    @staticmethod
    def insertudpelems(pudpthema):
        """übertrage alle Felder (mode_min_zoom_level, mode_max_zoom_level, mode_dev_status) aus Elementdisplay
            in die Modelelement Felder
        """
        print('Processing {}'.format(pudpthema))
        subselect = lambda pcolname : """(select UDPV_VALUE
                         from UDP_VALUES
                         join USER_DEFINED_PROPERTIES on udpr_id = udpv_udpr_id
                    where lower(udpr_theme) = lower('{}')
                    and  lower(udpr_name) = lower('{}')
                     and udpv_mode_id = mode_id
                        )""".format(pudpthema,pcolname)

        lsql = """update MODELELEMENT set MODE_MIN_ZOOM_LEVEL = {},
                MODE_MAX_ZOOM_LEVEL = {},
                MODE_DEV_STATUS = {}
                where mode_melt_id in (select metp_melt_id
                                        from MODELEMTYPE_PROPERTIES
                                        join user_defined_properties on udpr_id = metp_udpr_id
                                        where lower(udpr_theme) = lower('{}')
                                        )
                """.format(subselect(Modelelement.ODMattrmapping['mode_min_zoom_level'])
                          ,subselect(Modelelement.ODMattrmapping['mode_max_zoom_level'])
                          ,subselect(Modelelement.ODMattrmapping['mode_dev_status'])
                          ,pudpthema)
        print(dbDML.exec("select * from UDP_VALUES join USER_DEFINED_PROPERTIES on udpr_id = udpv_udpr_id where udpr_name in ('maxzoomlevel', 'minzoomlevel') and UDPV_VALUE not in (0,1,2,3,4)"))
        dbDML.exec(lsql)
        #update the attributes "descriptive" UDP
        lsql = """with udpval as (select UDPV_VALUE,udpv_mode_id
                         from UDP_VALUES
                         join USER_DEFINED_PROPERTIES on udpr_id = udpv_udpr_id,
                    where lower(udpr_name) = lower('isdescriptive')
                        )
                update ATTRIBUTES set ATTR_IS_DESCRIPTIVE
                    = case when (select udpv_value from udpval where udpv_mode_id =attr_id) is Null then 'FALSE'
                    else  (select udpv_value from udpval where udpv_mode_id =attr_id) end
                """.format(pudpthema, Modelelement.ODMattrmapping['attr_is_descriptive'])
        dbDML.exec(lsql)
        return

    @staticmethod
    def upddisplelements(pmodeid,pminzl,pmaxzl,pdevstat):
        #******* to be replaced by update() in baseobject ******
        #currently used in js2sql
        lsql = """update modelelement
                    set mode_min_zoom_level = {}
                    ,mode_max_zoom_level = {}
                    ,mode_dev_status = {} 
                    where mode_id = {}""".format(dbDML.dbval(pminzl),dbDML.dbval(pmaxzl)
                                                 ,dbDML.dbval(pdevstat),pmodeid)
        dbDML.exec(lsql)

# modelelement

class ModelelementProperty(Baseobject):
    _tablename: str = 'modelemtype_properties'
    _prefix: str = 'metp'
    _columnlist: list = []

    def __init__(self, pmeltid=None,pudprid=None):
        if (len(ModelelementProperty._columnlist) == 0): ModelelementProperty._columnlist = Baseobject.gettablecolumns(ModelelementProperty._tablename)
        super().__init__(tablename=ModelelementProperty._tablename, prefix=ModelelementProperty._prefix)
        self.metp_melt_id = pmeltid
        self.metp_udpr_id = pudprid
        self.metp_optional = Boolean.FALSE

    @staticmethod
    def delete(pwhere=None):
        return Baseobject.delete(ModelelementProperty._tablename,pwhere=pwhere)

    @staticmethod
    def select(pwhere=None, porderby="metp_id"):
        return Baseobject.select(pclass=ModelelementProperty, pwhere=pwhere, porderby=porderby)

#ModelelementProperty
from .externalref import Externalref
from .datatype import Datatype
from .domain import Domain
from .entity import Entity
from .table import Table
from .attribute import Attribute
from .column import Column
from .interface import Interface
from .document import Document
from .diagram import Diagram
from .orgunit import OragnisationalUnit
from .key import Key
from .relationship import Relation,Arc
