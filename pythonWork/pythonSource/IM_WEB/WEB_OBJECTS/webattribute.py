from .webbaseobject import Webanker,BaseWebObj,Objlist
from IM_OBJECTS import  Attribute,Entity
import WEB_OBJECTS

class WebAttribute(BaseWebObj):

    def __init__(self, pid=None, pdbobj:Attribute=None):
        super().__init__(pobjtype=Attribute, pid=pid, pdbobj=pdbobj)
        self.attr_id = self.dbobject().attr_id

    """Attrname (Entityname) """
    def getqualifiedname(self,plang=None):
        return "{} ({})".format(self.getname(plang=plang) ,self.dbobject().getentiname(plang=plang))

    def getname(self,plang=None):
        return self.dbobject().getname(plang=plang)

    def getwebentity(self):
        parent = self.dbobject().getparent()
        return WEB_OBJECTS.WebEntity(pdbobj=parent) if isinstance(parent,Entity) else WEB_OBJECTS.WebRelation(pdbobj=parent)

    def getwebdomain(self):
        return WEB_OBJECTS.WebDomain(pdbobj=self.dbobject().getdomain())

    @staticmethod
    def indexlist(pdomaid=None,plang=None):
        """ ALTE Lösung, mit Sortieren der Sprach-namen und den Relationsattributen
                data = dbDML.select"select attrname || ' ('||entname||')' name, attr_id
        from
         (select case when ana.lgtx_text is null then attr_displ_name
                                            else ana.lgtx_text end  attrname
            ,attr_id
            ,case when ena.lgtx_text is null then enti_name
                                            else ena.lgtx_text end  entname
          from attributes
          join entities on enti_id = attr_enti_id
          join languages sp on sp.lang_iso_code2 = '{}'
          left join langattr ana on ana.lgtx_attrname = 'ATTR_NAME'
                                and ana.lgtx_mode_id = attr_id
                                and ana.lang_id = sp.lang_id
          left join langattr ena on ena.lgtx_attrname = 'ENTI_NAME'
                                and ena.lgtx_mode_id = enti_id
                                and ena.lang_id = sp.lang_id
          join domains on doma_id = attr_doma_id
                            and doma_id = {}
          union all
          select case when ana.lgtx_text is null then attr_displ_name
                                            else ana.lgtx_text end  attrname
            ,attr_id
            ,rela_name  beziname
          from attributes
          join relations on attributes.attr_rela_id = relations.rela_id
          join languages sp on sp.lang_iso_code2 = 'de'
          left join langattr ana on ana.lgtx_attrname = 'ATTR_NAME'
                                and ana.lgtx_mode_id = attr_id
                                and ana.lang_id = sp.lang_id
          join domains on doma_id = attr_doma_id
                            and doma_id = {}
          ) order by upper(name)
              ".format(plang, pid if (pid is not None) else 'doma_id', pid if (pid is not None) else 'doma_id'))
        datalist = [(e[0], attrAnker(e[1]),'') for e in data]
        """
        members = [WebAttribute(pdbobj=obj) for obj in Attribute.select(pwhere="attr_doma_id = {}".format('attr_doma_id' if pdomaid is None else pdomaid))]
        return Objlist(pmembers=members).indexlist(plang=plang)
    # grouplist
#WebAttribute

