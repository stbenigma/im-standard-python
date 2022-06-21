import logging
from datetime import date

from SSOT_db import IM_OBJECTS
from SSOT_db.SQL_INFRA import dbDML
from .attribute import Attribute
from .baseobject import Baseobject, MultilangBaseobject
from .examples import Example
from .key import Key
from .language import Language
from .languagetext import Languagetext
from .modelelement import Modelelemtype, Modelelement
from .userdefprop import Userdefpropvalue, Userdefprop


class ElementUI(Baseobject):
    _tablename: str = 'element_ui'
    _prefix: str = 'elui'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []
    _defaultorderby = None

    def __init__(self):
        super().__init__()


class EntityCategory(Baseobject):
    _tablename: str = 'entity_categories'
    _prefix: str = 'enca'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []
    _defaultorderby = "enca_name"

    def __init__(self, pname=None):
        super().__init__()
        self.enca_name = pname

    def getname(self, plang=None):
        return self.enca_name

    def getchildren(self):
        children = Entity.select(pwhere=("enti_enca_id=?", self.enca_id))
        return [] if children is None else children
    # getchildren


class Entity(MultilangBaseobject):
    _tablename: str = 'entities'
    _prefix: str = 'enti'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.ENTI
    _columnlist: list = []
    _defaultorderby = "enti_name"

    def __init__(self, psrcname=None, psrcid=None):
        super().__init__(multilangcols=
                         {'enti_name': Languagetext.ENTI_NAME,
                          'enti_descr': Languagetext.ENTI_COMMENT,
                          'enti_tooltip': Languagetext.ENTI_TOOLTIP},
                         pscrid=psrcid,
                         psrcname=psrcname
                         )
        self._synonyms = None
        self._schluessel = None
        self._attributes = None

    def getmodellelement(self):
        return Modelelement.getbyelemid(pentiid=self.enti_id)

    def getmodeid(self):
        return self.enti_id

    def getname(self, plang=None):
        return self._getsprachval(colname='enti_name', plang=plang)

    def getdescr(self, plang=None):
        return self._getsprachval(colname='enti_descr', plang=plang)

    @staticmethod
    def getcategory(pid):
        return Entity().getbyid(pid).enti_category_guid

    def getparents(self):
        parents = Entity.select(pwhere=("enti_id in (select superenti_id from SUPERENTI where subenti_id = ?)",
                                        self.getid()))
        return [] if parents is None else parents

    def getchildren(self, ptype=None):
        """ptype None-> ALL, ISAS,'ISAR"""
        if ptype in (IM_OBJECTS.Relation.ISASUBTYPE, IM_OBJECTS.Relation.ISAROLE):
            relatype = ptype
        else:
            relatype = "%"
        children = Entity.select(pwhere=(
            """enti_id in 
                (select subenti_id 
                  from SUPERENTI 
                  where superenti_id = ? 
                  and rela_type like ?)""", self.getid(), relatype)
        )
        return [] if children is None else children

    def getsynonyms(self):
        if (self.getid() is not None) and (self._synonyms is None):
            self._synonyms = Synonym.select(pwhere=('syno_enti_id = ?', self.getid()),
                                            porderby='syno_name')
        # fi
        return self._synonyms

    def getkeys(self):
        return Key.select(pwhere=('keys_enti_id = ?', self.getid()),
                          porderby='keys_name')

    def getschluessel(self):
        if (self.getid() is not None) and (self._schluessel is None):
            self._schluessel = Key.select(pwhere=('keys_enti_id = ?', self.getid()),
                                          porderby='keys_laufnr')
        # fi
        return self._schluessel

    def getattributes(self):
        if (self.getid() is not None) and (self._attributes is None):
            self._attributes = Attribute.select(pwhere=('attr_enti_id = ?', self.getid()))
        # fi
        return self._attributes

    def getexamples(self):
        return Example.getexamples(pmodeid=self.getid())

    def getsubtypelevel(self):
        # restrict recursion to max 99 subentities for eternal loop
        subtypelevel = dbDML.select(
            """with recursive enti (entilev, entiid,parentid,name) as
            ( select 0 entilev, enti_id,enti_underlay_enti_id,enti_name
            from entities
            where enti_underlay_enti_id is NULL
            union all
            select enti.entilev + 1,enti_id,enti_underlay_enti_id,enti_name
            from entities
            join enti on enti.entiid = enti_underlay_enti_id
                      and enti.entilev < 100
            )
            select * from enti
            where entiid = {}
            """.format(self.enti_id))
        try:
            return subtypelevel[0][0]
        except:
            print(self.enti_id,subtypelevel)
            return 0

    @staticmethod
    def mappingto(ptablid):
        """ select list of entitiy id's for the logical model (dummy values) which ar linked
            to the given table id
        """
        lsqle = f"""select 0 intf_id, 'Logisches Modell' intf_name, group_concat(enti_id,',')
        	from  tabl_enti_maps as mastermap
	        left join entities on enti_id = mastermap.tema_enti_id
	        where  mastermap.tema_tabl_id = {ptablid}
	        GROUP BY mastermap.tema_tabl_id"""
        """ select list of table id's for each  model (except the model of the given table id) 
            which are linked to an entity, the given table id is mapped to
        """
        lsqlt = f"""select tabl_intf_id,intf_name,group_concat(tabl_id,',')
	        from tables subtab
	        join interfaces on intf_id = TABL_intf_ID
	        where tabl_id in
    	          (select tema1.tema_tabl_id
	               from tabl_enti_maps tema1
	                 join tabl_enti_maps tema2 on tema2.tema_enti_id = tema1.tema_enti_id
	                                and tema2.tema_tabl_id != tema1.tema_tabl_id
	                  where tema2.tema_tabl_id = {ptablid}
	            )
	            /* eigene Interface wird nicht angezeigt*/
	           and intf_id != (select tabl_intf_id 
	                            from tables where tabl_id = {ptablid})
            group by tabl_intf_id,intf_name
            """
        retval = []
        data = dbDML.select(lsqle)
        """[(0,'name', [Entity]'), (54,'name', [Entity])]"""
        for d in data:
            entis = []
            for e in d[2].split(','):
                ename = dbDML.select("select enti_name from entities where enti_id = {}".format(e))
                entis.append((ename[0][0], 'ENTI' + str(e)))
            retval.append([d[0], d[1], entis])
        data = dbDML.select(lsqlt)
        """[(0,'name', [Entity]'), (54,'name', [Entity])]"""
        for d in data:
            retval.append([d[0], d[1], [Entity().getbyid(e) for e in d[2].split(',')]])
        return retval

    # maopingto

    def getinheritedrelaids(self):
        """ get all own and inherited relations """
        lsql="""with recursive entitree(superenti_id, subenti_id,  relaids, level,super_enti_name,sub_enti_name)
                   as
                   (select superenti_id
                         , subenti_id
                         , ifnull(
                            (select relalist
                             from relas
                             where relaenti = superenti_id)
                             ,'') AS relaids
                         ,0 level
                        ,super_enti_name,sub_enti_name
                    from superenti
                    where superenti_id not in (select subenti_id from superenti)
                    union all
                    select sup2.superenti_id
                         , sup2.subenti_id
                         , ifnull(entitree.relaids,'')|| ','
                                  ||ifnull(
                                     (select relalist
                                      from relas
                                     where relaenti = sup2.superenti_id)
                                      ,'')  as relaids
                         , entitree.level+1
                    ,sup2.super_enti_name,sup2.sub_enti_name
                    from superenti sup2
                             join entitree on sup2.superenti_id = entitree.subenti_id
                     where entitree.level < 99
                    )
                ,relas as (select distinct relaenti
                                        ,group_concat(rela_id, ',')
                                             over (partition by relaenti
                                             rows between unbounded preceding
                                                 and unbounded following) as relalist
                            from (select rela_id,rela_enti_id_from relaenti
                                  from relations
                                  where rela_type not in ('ISAS','ISAR')
                                  union
                                  select rela_id,rela_enti_id_to relaenti
                                  from relations
                                  where rela_type not in ('ISAS','ISAR')
                                  )
                            )
            select rtrim(relaids ,',') as relaids,level
            from entitree
            where relaids != ''
                and subenti_id = ?"""

        retval = []
        relas = dbDML.select(lsql,self.getid())
        retval = []
        if len(relas)>0:
            assert relas[0][1] < 100, "recursive sql with loop"
            for a in relas[0][0].split(','):
                if a.isnumeric():
                    retval.append(int(a))
        return retval

    """ get all own and inherited attributes """
    def getinheritedattrids(self):
        """recursive SQL
           attrs: get comma separated listof attributes of an entity
           entitree: 1. select entities having subentities (=beeing super in view superenti)
                    union  2. select all entities which have as superentity the recursive predecessor entitiy
                           add list of attributes of this entity to the list of its predecessor
        """
        lsql = """with recursive entitree(superenti_id, subenti_id,  attrids, level)
                   as
                   (select superenti_id
                         , subenti_id
                         , ifnull(
                            (select attrlist
                             from attrs
                             where attr_enti_id = superenti_id)
                             ,'') AS attrids
                         ,0 level
                    from superenti
                    where superenti_id not in (select subenti_id from superenti)
                    union all
                    select sup2.superenti_id
                         , sup2.subenti_id
                         , ifnull(entitree.attrids,'')|| ',' 
                                  ||ifnull(
                                     (select attrlist
                                      from attrs
                                     where attr_enti_id = sup2.superenti_id)
                                      ,'')  as attrids
                         , entitree.level+1
                    from superenti sup2
                             join entitree on sup2.superenti_id = entitree.subenti_id
                     where entitree.level < 99
                    )
                ,attrs as (select distinct attr_enti_id
                                        ,group_concat(attr_id, ',')
                                             over (partition by attr_enti_id
                                            order by attr_displ_seq
                                             rows between unbounded preceding
                                                 and unbounded following) as attrlist
                            from attributes)
            select rtrim(attrids ,',') as attrids,level
            from entitree where subenti_id = ?
            """
        attrs = dbDML.select(lsql,self.getid())
        retval = []
        if len(attrs)>0:
            assert attrs[0][1] < 100, "recursive sql with loop"
            for a in attrs[0][0].split(','):
                if a.isnumeric():
                    retval.append(int(a))
        return retval
# Entity

class Synonym(MultilangBaseobject):
    _tablename: str = 'synonyms'
    _prefix: str = 'syno'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.SYNO
    _columnlist: list = []

    ##    _multilangcols: list = {'syno_name': 'ENTI_SYNONYM'}

    def __init__(self, pname=None, pentiid=None):
        super().__init__(multilangcols={'syno_name': Languagetext.ENTI_SYNONYM})
        self.syno_name = pname
        self.syno_enti_id = pentiid
        self.syno_uc = 'SYS'
        self.syno_dc = date.today()

    def getname(self, plang=None):
        retval = self._getsprachval(colname='syno_name', plang=plang)
        return '' if retval is None else retval

    def getparent(self):
        return Entity().getbyid(self.syno_enti_id)

    # getparent

    @staticmethod
    def transfersynotransl():
        """get all udpr translations for synonyms except for the default language
           if it is comma separated, dispatch an entry per synonym into language texts.
           If order or number is not the same, ignore it"""
        for udpr in Userdefprop.select(pwhere=("udpr_name like ?", '___ENTI_SYNONYM')):
            langiso2 = udpr.udpr_name[0:2].lower()
            l = Language().getbyuk(lang_iso_code2=langiso2)
            if l is None:
                logging.warning(f"Language {langiso2} from udpr ___ENTI_SYNONYM(id={udpr.getid()}) not present")
                continue
            langid = l.getid()
            if langid == Language.liesdeflangid(): continue
            for udpv in Userdefpropvalue.select(pwhere=("udpv_udpr_id = ?", udpr.udpr_id)):
                langsynos = udpv.udpv_value.split(',')
                for idx, syno in enumerate(Entity().getbyid(udpv.udpv_mode_id).getsynonyms()):
                    try:
                        synotransl = langsynos[idx]
                    except:
                        continue
                    lgtx = Languagetext()
                    lgtx.lgtx_attrname = Languagetext.ENTI_SYNONYM
                    lgtx.lgtx_text = synotransl
                    lgtx.lgtx_lang_id = langid
                    lgtx.lgtx_mode_id = syno.syno_id
                    lgtx.lgtx_uc = udpv.udpv_uc
                    lgtx.lgtx_dc = udpv.udpv_dc
                    lgtx.lgtx_um = udpv.udpv_um
                    lgtx.lgtx_dm = udpv.udpv_dm
                    lgtx.insert()
                # for
            # for
        return
