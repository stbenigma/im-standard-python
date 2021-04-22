from IM_DB import dbDML,dbDDL
from datetime import date
from .baseobject import Baseobject,MultilangBaseobject
from .languagetext import Languagetext
from .language import Language
from .modelelement import Modelelemtype,Modelelement
from .userdefprop import Userdefpropvalue,Userdefprop
import IM_OBJECTS


class EntityCategory(Baseobject):
    _tablename:str = 'entity_categories'
    _prefix:str = 'enca'
    _idcolname: str = _prefix + '_id'
    _columnlist:list = []
    _defaultorderby = None

    def __init__(self,pname):
        super().__init__()
        self.enca_name = pname

    def getname(self,plang=None):
        return self.enca_name

    def getchildren(self):
        children = Entity.select(pwhere=("enti_enca_id=?",self.enca_id))
        return [] if children is None else children
    # getchildren


class Entity(MultilangBaseobject):
    _tablename:str = 'entities'
    _prefix:str = 'enti'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.ENTI
    _columnlist:list = []
    _defaultorderby = "enti_name"

    def __init__(self, psrcname=None, psrcid=None):
        super().__init__(multilangcols = {'enti_name':Languagetext.ENTI_NAME
                                          ,'enti_descr':Languagetext.ENTI_COMMENT
                                          ,'enti_tooltip': Languagetext.ENTI_TOOLTIP}
                         , pscrid=psrcid
                         , psrcname=psrcname
                         )
        self._synonyms = None
        self._schluessel = None
        self._attributes = None

    def getmodellelement(self):
        return Modelelement.getbyelemid(pentiid=self.enti_id)

    def getmodeid(self):
        return self.enti_id

    def getname(self,plang=None):
        return self._getsprachval(colname='enti_name',plang=plang)

    def getdescr(self,plang=None):
        return self._getsprachval(colname='enti_descr',plang=plang)

    def getcategory(pid):
        return Entity().getbyid(pid).enti_category_guid

    def getparents(self):
        parents = Entity.select(pwhere=("enti_id in (select superenti_id from SUPERENTI where subenti_id = ?)",
                                        self.getid()))
        return [] if parents is None else parents


    def getchildren(self,ptype=None):
        """ptype None-> ALL, ISAS,'ISAR"""
        if ptype in (IM_OBJECTS.Relation.ISASUBTYPE,IM_OBJECTS.Relation.ISAROLE):
            relatype = ptype
        else:
            relatype = "%"
        children =  Entity.select(pwhere=(
                                """enti_id in 
                                    (select subenti_id 
                                      from SUPERENTI 
                                      where superenti_id = ? 
                                      and rela_type like ?)""", self.getid(),relatype)
                                )
        return [] if children is None else children


    def getsynonyms(self):
        if (self.getid() is not None) and (self._synonyms is None):
            self._synonyms = Synonym.select(pwhere=('syno_enti_id = ?', self.getid())
                                             , porderby='syno_name')
        # fi
        return self._synonyms



    def getkeys(self):
        return Key.select(pwhere=('keys_enti_id = ?', self.getid())
                                  , porderby='keys_name')


    def getschluessel(self):
        if (self.getid() is not None) and (self._schluessel is None):
            self._schluessel = Key.select(pwhere=('keys_enti_id = ?', self.getid())
                                          , porderby='keys_laufnr')
        # fi
        return self._schluessel


    def getattributes(self):
        if (self.getid() is not None) and (self._attributes is None):
            self._attributes = Attribute.select(pwhere=('attr_enti_id = ?', self.getid()))
        # fi
        return self._attributes
    #getschluessel

    def getsubtypelevel(self):
        subtypelevel = dbDML.select("""
            with recursive enti as
            ( select 0 entilev, enti_id
            from entities
            where not exists (select 1 from superenti where rela_type = 'ISAS' AND subenti_id = enti_id)
            union all
            select enti.entilev + 1, subenti_id
            from superenti
            join enti on enti_id = superenti_id
            )
            select entilev from enti
            where enti_id = {}
            """.format(self.enti_id))
        return subtypelevel[0][0]




    @staticmethod
    def mappingto(ptablid):
        lsqle = """select 0 intf_id, 'Logisches Modell' intf_name, group_concat(enti_id,',')
        	from  tabl_enti_maps as mastermap
	        left join entitaeten on enti_id = mastermap.tema_enti_id
	        where  mastermap.tema_tabl_id = {}
	        GROUP BY mastermap.tema_tabl_id""".format(ptablid)
        lsqlt = """select tabl_intf_id,intf_name,group_concat(tabl_id,',')
	        from tables subtab
	        join interfaces on intf_id = TABL_intf_ID
	        where tabl_id in
    	          (select tema1.tema_tabl_id
	               from tabl_enti_maps tema1
	                 join tabl_enti_maps tema2 on tema2.tema_enti_id = tema1.tema_enti_id
	                                and tema2.tema_tabl_id != tema1.tema_tabl_id
	                  where tema2.tema_tabl_id = {}
	            )
	            /* eigene Interface wird nicht angezeigt*/
	           and intf_id != (select tabl_intf_id 
	                            from tables where tabl_id = {})
            group by tabl_intf_id,intf_name
            """.format(ptablid,ptablid)
        retval = []
        data = dbDML.select(lsqle)
        """[(0,'name', [Entity]'), (54,'name', [Entity])]"""
        for d in data:
            entis = []
            for e in d[2].split(','):
                ename = dbDML.select("select enti_name from entitaeten where enti_id = {}".format(e))
                entis.append((ename[0][0],'ENTI'+str(e)))
            retval.append([d[0], d[1],entis])
        data = dbDML.select(lsqlt)
        """[(0,'name', [Entity]'), (54,'name', [Entity])]"""
        for d in data:
            retval.append([d[0], d[1], [Entity().getbyid(e) for e in d[2].split(',')]])
        return retval
    #maopingto
#Entity

class Synonym(MultilangBaseobject):
    _tablename: str = 'synonyms'
    _prefix: str = 'syno'
    _idcolname: str = _prefix + '_id'
    _modelemtype = Modelelemtype.SYNO
    _columnlist: list = []
##    _multilangcols: list = {'syno_name': 'ENTI_SYNONYM'}

    def __init__(self,pname=None,pentiid=None):
        super().__init__(multilangcols = {'syno_name': Languagetext.ENTI_SYNONYM})
        self.syno_name = pname
        self.syno_enti_id = pentiid
        self.syno_uc = 'SYS'
        self.syno_dc = date.today()


    def getname(self,plang=None):
        retval = self._getsprachval(colname='syno_name',plang=plang)
        return '' if retval is None else retval

    def getparent(self):
        return Entity.getbyid(self.syno_enti_id)
    # getparent


    @staticmethod
    def transfersynotransl():
        """get all udpr translations for synonyms except for the default language
           if it is comma separated, dispatch an entry per synonym into language texts.
           If order or number is not the same, ignore it"""
        for udpr in Userdefprop.select(pwhere=("udpr_name like ?", '___ENTI_SYNONYM')):
            langiso2 = udpr.udpr_name[0:2].lower()
            langid=Language().getbyuk(lang_iso_code2=langiso2).getid()
            if langid == Language.liesdeflangid(): continue
            for udpv in Userdefpropvalue.select(pwhere=("udpv_udpr_id = ?", udpr.udpr_id)):
                langsynos = udpv.udpv_value.split(',')
                for idx,syno in enumerate(Entity().getbyid(udpv.udpv_mode_id).getsynonyms()):
                    try:
                        synotransl = langsynos[idx]
                    except:
                        continue
                    lgtx=Languagetext()
                    lgtx.lgtx_attrname=Languagetext.ENTI_SYNONYM
                    lgtx.lgtx_text=synotransl
                    lgtx.lgtx_lang_id=langid
                    lgtx.lgtx_mode_id=syno.syno_id
                    lgtx.lgtx_uc=udpv.udpv_uc
                    lgtx.lgtx_dc=udpv.udpv_dc
                    lgtx.lgtx_um = udpv.udpv_um
                    lgtx.lgtx_dm = udpv.udpv_dm
                    lgtx.insert()
from .key import Key
from .attribute import Attribute



