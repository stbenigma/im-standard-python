import logging
from datetime import date

from SSOT_db.SQL_INFRA import dbDML
from .baseobject import Baseobject, Boolean
from SSOT_infra import logmessages

""" Modelelemtype
    master data object filled at start never changed thereafter
"""
class Modelelemtype(Baseobject):
    ACTR: str = 'ACTR'
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
    EXPL: str = 'EXPL'

    _tablename: str = 'modelelem_type'
    _prefix: str = 'melt'
    _idcolname: str = _prefix + '_id'
    _columnlist = dict()

    def __init__(self, pshortname=None, pname=None):

        super().__init__()
        self.melt_shortname = pshortname
        self.melt_name = pname
        self.melt_uc = 'SYS'
        self.melt_dc = date.today()
        return

    def getname(self, plang=None):
        return self.melt_name

    @staticmethod
    def fillmelt():
        #insert as special function, table should remain immutable
        # melt_shortname,  melt_name    ,melt_uc,  melt_dc
        Modelelemtype(pshortname=Modelelemtype.ARCS, pname='Arc')._insert()
        Modelelemtype(pshortname=Modelelemtype.ATTR, pname='Attribute')._insert()
        Modelelemtype(pshortname=Modelelemtype.BURU, pname='Business Rule')._insert()
        Modelelemtype(pshortname=Modelelemtype.COLU, pname='Column')._insert()
        Modelelemtype(pshortname=Modelelemtype.DOMA, pname='Domain')._insert()
        Modelelemtype(pshortname=Modelelemtype.ENTI, pname='Entity')._insert()
        Modelelemtype(pshortname=Modelelemtype.INTF, pname='Interface')._insert()
        Modelelemtype(pshortname=Modelelemtype.ORGU, pname='Organizational Unit')._insert()
        Modelelemtype(pshortname=Modelelemtype.RELA, pname='Relation')._insert()
        Modelelemtype(pshortname=Modelelemtype.SYNO, pname='Synonym')._insert()
        Modelelemtype(pshortname=Modelelemtype.TABL, pname='Table')._insert()
        Modelelemtype(pshortname=Modelelemtype.DATY, pname='Datatyope')._insert()
        Modelelemtype(pshortname=Modelelemtype.KEYS, pname='Key')._insert()
        Modelelemtype(pshortname=Modelelemtype.DOCU, pname='Document')._insert()
        Modelelemtype(pshortname=Modelelemtype.DGRM, pname='Domaingroupmember')._insert()
        Modelelemtype(pshortname=Modelelemtype.DIAG, pname='Diagram')._insert()
        Modelelemtype(pshortname=Modelelemtype.EXPL, pname='Example')._insert()
        Modelelemtype(pshortname=Modelelemtype.ACTR, pname='Actor Role')._insert()

    @staticmethod
    def getidbyshortname(pshortname):
        melt = Modelelemtype.select(pwhere=("melt_shortname = ?", pshortname))
        if melt is None or (len(melt) == 0):
            return None
        return melt[0].melt_id

    @staticmethod
    def getshortname(pmeltid):
        return Modelelemtype().getbyid(pmeltid).melt_shortname

    @staticmethod
    def getbyshortname(pshortname):
        return Modelelemtype().getbyid(Modelelemtype.getidbyshortname(pshortname))

    @staticmethod
    def type2melt(ptype):
        trans = {"Entity": Modelelemtype.ENTI,
                 "Attribute": Modelelemtype.ATTR,
                 "Relation": Modelelemtype.RELA,
                 "Table": Modelelemtype.TABL,
                 "Column": Modelelemtype.COLU,
                 "Arcs": Modelelemtype.ARCS,
                 "FKIndexAssociation": ""
                 }
        if ptype in trans:
            return trans[ptype]
        else:
            return ""

    """override insert, delete and update to make sure it is never changed after init
    """
    def insert(self,pdoerrhdlng=True):
        raise Exception(f"no chnages in table {self._tablename} allowed")
    def updatedb(self, pdoerrhdlng=True):
        raise Exception(f"no chnages in table {self._tablename} allowed")
    def delete(cls,pwhere=None):
        raise Exception(f"no chnages in table {self._tablename} allowed")
    def _insert(self):
        super().insert()

# Modelelemtype

class Modelelement(Baseobject):
    """Modelelement is a supertype of a lot of entities. It shares common attributes and relationships
        It's ID is identical to id's in subtype tables.
        So Modelelement is created first (with a system generated ID, unique over all subtables). It's ID is then
        used as ID' of the subtables
    """
    #publication status
    DRAFT: str = 'DRAFT'
    GTOP: str = 'GTOP'
    PUBL: str = 'PUBL'

    _tablename: str = 'modelelement'
    _prefix: str = 'mode'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []

    def __init__(self, pid=None, pmeltshortname=None):

        super().__init__()
        self.mode_type = pmeltshortname
        self.mode_id = pid
        if pmeltshortname is not None:
            self.mode_melt_id = Modelelemtype.getidbyshortname(pshortname=pmeltshortname)

    # __init__

    def __repr__(self):
        return f"Modelelement({self.getid()}, {self.mode_type})"

    """Mapping of mode attributes to udp-names  in ODM"""
    ODMattrmapping = {'mode_min_zoom_level': 'minzoomlevel',
                      'mode_max_zoom_level': 'maxzoomlevel',
                      'mode_publ_status': 'publ_status',
                      'attr_is_descriptive': 'isdescriptive'}

    @staticmethod
    def longpublstatus(pdbvalue):
        longstati = {Modelelement.DRAFT : 'draft',
                     Modelelement.GTOP: 'good to print',
                     Modelelement.PUBL: 'published'}
        if pdbvalue in longstati:
            return longstati[pdbvalue]
        return None

    @staticmethod
    def getmodebyextref(psrcname, psrcid):
        modeid = Externalref.getmodeid(psrcname=psrcname, psrcid=psrcid)
        return None if modeid is None else Modelelement().getbyid(pid=modeid)

    def getmyelement(self):
        if self.mode_type == Modelelemtype.SYNO:
            element = Synonym().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.DOMA:
            element = Domain().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.ATTR:
            element = Attribute().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.BURU:
            element = BusinessRule().getbyid(self.mode_id)
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
            element = DomaingroupMember().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.DATY:
            element = Datatype().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.KEYS:
            element = Key().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.DIAG:
            element = Diagram().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.DOCU:
            element = Document().getbyid(self.mode_id)
        elif self.mode_type == Modelelemtype.ACTR:
            element = Actorrole().getbyid(self.mode_id)
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
    def insertudpelems(pudpthema):
        """übertrage alle Felder (mode_min_zoom_level, mode_max_zoom_level, mode_publ_status) aus Elementdisplay
            in die Modelelement Felder
        """
        subselect = lambda pcolname: """(select UDPV_VALUE
                         from UDP_VALUES
                         join USER_DEFINED_PROPERTIES on udpr_id = udpv_udpr_id
                    where lower(udpr_theme) = lower('{}')
                    and  lower(udpr_name) = lower('{}')
                     and udpv_mode_id = mode_id
                        )""".format(pudpthema, pcolname)

        lsql = """update MODELELEMENT set MODE_MIN_ZOOM_LEVEL = {},
                MODE_MAX_ZOOM_LEVEL = {},
                MODE_PUBL_STATUS = {}
                where mode_melt_id in (select metp_melt_id
                                        from MODELEMTYPE_PROPERTIES
                                        join user_defined_properties on udpr_id = metp_udpr_id
                                        where lower(udpr_theme) = lower('{}')
                                        )
                """.format(subselect(Modelelement.ODMattrmapping['mode_min_zoom_level']),
                           subselect(Modelelement.ODMattrmapping['mode_max_zoom_level']),
                           subselect(Modelelement.ODMattrmapping['mode_publ_status']),
                           pudpthema)
        try:
            dbDML.exec(lsql)
        except Exception as e:
            msg = """Invalid values in user defined properties """ \
                 + """'mode_min_zoom_level','mode_max_zoom_level' or 'mode_publ_status'"""
            print(msg)
            logmessages.writelog(msg)
            raise e
        # update the attributes "descriptive" UDP
        lsql = """with udpval as (select UDPV_VALUE,udpv_mode_id
                         from UDP_VALUES
                         join USER_DEFINED_PROPERTIES on udpr_id = udpv_udpr_id
                    where lower(udpr_name) = lower('isdescriptive')
                        )
                update ATTRIBUTES set ATTR_IS_DESCRIPTIVE
                    = case when (select udpv_value from udpval where udpv_mode_id =attr_id) is Null then 'FALSE'
                    else  (select udpv_value from udpval where udpv_mode_id =attr_id) end
                """
        try:
            dbDML.exec(lsql)
        except Exception as e:
            msg = """Invalid values in user defined propertiy 'isdescriptive'"""
            print(msg)
            logmessages.writelog(msg)
            raise e
        return

    @staticmethod
    def upddisplelements(pmodeid, pminzl, pmaxzl, ppublstat):
        # ******* to be replaced by update() in baseobject ******
        # currently used in js2sql
        lsql = """update modelelement
                    set mode_min_zoom_level = {}
                    ,mode_max_zoom_level = {}
                    ,mode_publ_status = {} 
                    where mode_id = {}""".format(dbDML.dbval(pminzl), dbDML.dbval(pmaxzl),
                                                 dbDML.dbval(ppublstat), pmodeid)
        dbDML.exec(lsql)
        return

    @staticmethod
    def deletenonreferenced(pmodetype):
        """ delete all modelelements which do not longer have an external reference
        """
        try:
            where = ("""mode_type = ? 
                                and not exists 
                                (select 1 from external_refs 
                                    where extr_mode_id = mode_id)""", pmodetype)
            cnt = Modelelement.delete(pwhere=where)
        except BaseException as e:
            candidates = Modelelement.select(pwhere=where)
            logging.error(f"Failed to delete one of {list(candidates)} where mode_type={pmodetype}. " + str(e))
            raise
        return cnt

    @staticmethod
    def selecttanglingmode():
        """ check, wether there are modelelements not linked to any object.
        """
        retval = []
        relations = dbDML.select(
                    """with tabls as (SELECT name tabname
                                    FROM sqlite_schema
                                    WHERE
                                    type ='table' AND
                                    name NOT LIKE 'sqlite_%')
                        select tabname,"from" pkcol, "table" reftable,"to" fkcol,on_delete
                            from tabls
                            cross join pragma_foreign_key_list(tabname)
                        where lower(reftable) = 'modelelement'
                        and upper(on_delete) = 'CASCADE'
                        and pkcol like '_____id';
                    """
                    )
        #[tabname,pkcol,reftable,fkcol,on_delete]
        allidssql = "\nunion ".join([f"select {t[1]} from {t[0]}" for t in relations])

        sql = f"""
        select mode_id,mode_type
            from main.modelelement
            where mode_id not in ({allidssql})
        """
        result = dbDML.select(sql)
        """(mode_id,mode_type)"""
        for r in result:
            retval.append(f"Modelelement  {r[0]} for element-type {r[1]} is tangling. (Element no longer exists)")
        return retval



class ModelelementProperty(Baseobject):
    _tablename: str = 'modelemtype_properties'
    _prefix: str = 'metp'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []
    _defaultorderby = "metp_id"

    def __init__(self, pmeltid=None, pudprid=None):
        super().__init__()
        self.metp_melt_id = pmeltid
        self.metp_udpr_id = pudprid
        self.metp_optional = Boolean.FALSE


# ModelelementProperty
from .actorrole import Actorrole
from .externalref import Externalref
from .datatype import Datatype
from .domain import Domain, DomaingroupMember
from .entity import Entity, Synonym
from .businessrule import BusinessRule
from .table import Table
from .attribute import Attribute
from .column import Column
from .interface import Interface
from .document import Document
from .diagram import Diagram
from .orgunit import OragnisationalUnit
from .key import Key
from .relationship import Relation, Arc
