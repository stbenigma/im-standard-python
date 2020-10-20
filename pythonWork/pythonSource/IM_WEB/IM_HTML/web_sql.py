import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../IM_db')
from IM_DB import dbDML, parameters
from IM_OBJECTS import *
from mystring import nvl

class Webanker:
    """enthält die Information um Web-Referenzen (Sprungziele / id) herzustellen.
         Webanker bestehen aus dem Kurznamen (prefix) des Elementes, seinem ID sowie ggf.
         dem Modelid (der dann in einen html-Dateinamen umgesetzt wird.
         Modelid =0 -> logisches Modell
    """
    def __init__(self,ptype,pid,pmodelid=0):
        self._id:int = pid
        self._type:str = ptype.upper()
        self._modelid:int = pmodelid
    def anker(self):
        return nvl(self._type) + str(nvl(self._id))
    def modelid(self):
        return self._modelid
#Webanker

class Objlist:
    def __init__(self,pmembers):
        #list of DB-elements making up the list
        self.__members = pmembers

    def getmembers(self):
        return self.__members

    def indexlist(self,plang=None):
        #I sort by the displayed, qualified name in the list, which is the first element in the sublists
        idxlist = [[member.getqualifiedname(plang), member.webanker(), member.getid()] for member in self.getmembers()]
        idxlist.sort()
        return idxlist
#Objlist

class BaseWebObj:
    __dbobject = None

    def __init__(self,pobjtype,pid=None,pdbobj=None):
        if (pid is not None or pdbobj is not None):
            self.setdbobject(pdbobj if pdbobj is not None else self.readbobject(pid))
        self.__objtype = pobjtype

    def dbobject(self):
        return self.__dbobject

    def setdbobject(self, pdbobj):
        self.__dbobject = pdbobj

    def readbobject(self,pid):
        self.setdbobject(self.__objtype.getbyid(pid))

    def getid(self):
        return self.dbobject().getid()

    def getname(self,plang=None):
        return self.dbobject().getname(plang=plang)

    """mit Präfix (Tabelle) oder in Klammern (Entität)
       falls Typ nicht überschreibt nimm einfach den Namen"""
    def getqualifiedname(self,plang=None):
        return self.getname(plang=plang)

    def webanker(self):
        if self.dbobject() is None: return None
        return Webanker(ptype=self.dbobject()._prefix, pid=self.getid())
#BaseWebObj

class WebEntity(BaseWebObj):

    def __init__(self,pid=None,pdbobj:Entity=None):
        super().__init__(pobjtype=WebEntity,pid=pid,pdbobj=pdbobj)

    @staticmethod
    def indexlist(plang=None):
        members = [WebEntity(pdbobj=obj) for obj in Entity.select()]
        return Objlist(pmembers=members).indexlist(plang=plang)
    # indexlist
#WebEntity

class WebAttribute(BaseWebObj):

    def __init__(self, pid=None, pdbobj:Attribute=None):
        super().__init__(pobjtype=WebAttribute, pid=pid, pdbobj=pdbobj)

    """Attrname (Entityname) """
    def getqualifiedname(self,plang=None):
        return self.getname(plang=plang) + ' (' +self.dbobject().getentiname(plang=plang) +')'

    @staticmethod
    def indexlist(plang=None):
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
        members = [WebAttribute(pdbobj=obj) for obj in Attribute.select()]
        return Objlist(pmembers=members).indexlist(plang=plang)
    # indexlist
#WebAttribute

class WebDomain(BaseWebObj):

    def __init__(self, pid=None, pdbobj:Domain=None):
        super().__init__(pobjtype=WebDomain, pid=pid, pdbobj=pdbobj)

    """Domainname (Anzahl Refs) """
    def getqualifiedname(self, plang=None):
            return '{} ({})'.format(self.getname(plang=plang), self.dbobject().refattranz())

    @staticmethod
    def indexlist(porigin,plang=None):
        members = [WebDomain(pdbobj=obj) for obj in Domain.select(pwhere="doma_origin = '{}'".format(porigin))]
        return Objlist(pmembers=members).indexlist(plang=plang)
    # indexlist
#WebDomain

class WebDocument(BaseWebObj):
    def __init__(self, pid=None, pdbobj:Document=None):
        super().__init__(pobjtype=WebDocument, pid=pid, pdbobj=pdbobj)

    def getname(self,plang=None):
        return self.dbobject().docu_name

    @staticmethod
    def indexlist(plang=None):
        members = [WebDocument(pdbobj=obj) for obj in Document.select()]
        return Objlist(pmembers=members).indexlist()
    #indexlist
#WebDocument

class WebDiagram(BaseWebObj):
    def __init__(self, pid=None, pdbobj: Diagram = None):
        super().__init__(pobjtype=WebDiagram, pid=pid, pdbobj=pdbobj)

    def getname(self, plang=None):
        return self.dbobject().diag_name

    """Diagramname (entry type) """
    def getqualifiedname(self, plang=None):
            return '{} ({})'.format(self.dbobject().diag_name, Diagramtype().getbyid(pid=self.dbobject().diag_diat_id).diat_name)

    @staticmethod
    def indexlist(plang=None):
        #order by in indexlist not yet resolved (diagramtype -> diagramnbame)
        #    porderby='(select diat_name from diagramtypes where diat_id = diag_diat_id),diag_name'
        members = [WebDiagram(pdbobj=obj) for obj in Diagram.select()]
        return Objlist(pmembers=members).indexlist()
    # indexlist
#WebDiagram

class WebInterface(BaseWebObj):
    def __init__(self, pid=None, pdbobj: Schnittstelle = None):
        super().__init__(pobjtype=WebInterface, pid=pid, pdbobj=pdbobj)

    def getname(self, plang=None):
        return self.dbobject().schn_name

    def webanker(self):
        if self.dbobject() is None: return None
        return Webanker(ptype=self.dbobject()._prefix, pid=self.getid(),pmodelid=self.dbobject().schn_id)

    @staticmethod
    def indexlist(plang=None):
        members = [WebInterface(pdbobj=obj) for obj in Schnittstelle.select()]
        idxlist = Objlist(pmembers=members).indexlist(plang=plang)
        return idxlist
    # indexlist
# WebInterface



def entiAnker(id):
    return 'ENTI'+str(id)
def attrAnker(id):
    return 'ATTR'+str(id)
def wrtbAnker(id):
    return 'DOMA'+str(id)
def diagAnker(id):
    return 'DIAG'+str(id)
def dokuAnker(id):
    return 'DOKU'+str(id)

class Referenceentry:
    def __init__(self,pid,pname,ptype,ptypename,pdirect='TRUE',panker=None):
        self.name = pname
        self.anker = panker
        self.elemtype = ptype
        self.typename = ptypename
        self.elemid = pid
        self.direct = pdirect == 'TRUE'
#Rererenceentry

def dokureflist (pid, plang):
    data = dbDML.select("""
    select name,id,type,anztype from (
        select case when spa.lgtx_text is null then name 
                                                else spa.lgtx_text end  name
                ,id,melt_shortname type,melt_name anztype 
        from mode_docu
        join modellelement on mode_id = MODO_MODE_ID
        join modelelem_type on melt_id = mode_melt_id
        left join (select enti_id id ,enti_name name 
                   from entities
                   union all
                   select attr_id id ,attr_displ_name name 
                   from attributes 
                   union all
                   select tabl_id id ,TABL_NAME name 
                   from tabellen
                   union all
                   select SCHN_ID id ,SCHN_NAME name 
                   from schnittstellen
           ) on id = modo_mode_id 
         join languages sp on sp.lang_iso_code2 = '{}'
         left join langattr spa on spa.lgtx_attrname = case melt_shortname when 'ENTI' then 'ENTI_NAME'
                                                            when 'ATTR' then 'ATTR_NAME'
                                                            else ''
                                                        end
                                    and spa.lgtx_mode_id = modo_mode_id
                                    and spa.lang_id = sp.lang_id
        where  MODO_docu_ID = {}
    )
    order by type,upper(name)
                  """.format(plang,pid))
    datalist = [Referenceentry(pid=e[1], pname=e[0], ptype=e[2], ptypename=e[3]
                        , panker=Entity().getbyid(e[1]).webanker() if e[2] == Modelelemtype.ENTI
                            else Attribute().getbyid(e[1]).webanker() if e[2] == Modelelemtype.ATTR
                            else Tabelle().getbyid(e[1]).webanker() if e[2] == Modelelemtype.TABL
                            else Schnittstelle().getbyid(e[1]).webanker() if e[2] == Modelelemtype.INTF
                            else ''
                               ) for e in data]
    return datalist
#dokureflist

def refdokulist (pid, pelemtype):
    data = dbDML.select("""
        select name,id, 'DOKU' type, 'documents'  anztype ,direct
        from (
            select docu_name name,docu_id id
                , MODO_MODE_ID as ref_id 
                ,'TRUE' direct
                ,melt_shortname ref_type
            from documents
            join mode_docu on MODO_docu_ID = docu_ID
            join modelelement on mode_id = MODO_MODE_ID
            join modelelem_type on melt_id = mode_melt_id
            union all 
            select docu_name name,docu_id id,tabl_id ref_id,'FALSE' direct,'TABL' ref_type
            from documents
            join mode_docu on MODO_docu_ID = docu_ID
            join (select schn_id, TABL_ID
                  from tabellen
                  join schnittstellen on SCHN_ID = TABL_SCHN_ID
                 ) on MODO_MODE_ID = SCHN_ID      
            ) 
        where ref_type = '{}' and ref_id = {}  
    order by type,upper(name)
    """.format(pelemtype,pid))
    datalist = [Referenceentry(pid=e[1], pname=e[0], ptype=e[2], ptypename=e[3]
                               , pdirect = e[4]
                                ,panker=dokuAnker(e[1]) if e[2] == Modelelemtype.DOCU
                                        else ''
                               )
                for e in data]
    return datalist
#refdokulist

def namelist(ptype, plang=None, pid=None):
    datalist = []
    if ptype == Modelelemtype.ENTI:
        datalist = WebEntity.indexlist(plang=plang)
    elif (ptype ==  Modelelemtype.ATTR):
        datalist = WebAttribute.indexlist(plang=plang)
    elif (ptype == Modelelemtype.DGRM):
        data = dbDML.select("""select wbgrname || ' ('||wrtbname||')' name, dgrm_id,wrtbname,doma_id 
            from 
             (select  dgrm_name wbgrname
                ,dgrm_id,w2.doma_id
                ,case when ana.lgtx_text is null then w2.doma_name 
                                                else ana.lgtx_text end  wrtbname
              from domaingroup_members 
              join domains w2 on w2.doma_id = dgrm_doma_id_group
              join languages sp on sp.lang_iso_code2 = '{}'         
              left join langattr ana on ana.lgtx_attrname = 'DOMA_NAME'
                                    and ana.lgtx_mode_id = w2.doma_id
                                    and ana.lang_id = sp.lang_id
              where dgrm_doma_id_member = {}
              ) order by wrtbname,upper(name)
                  """.format(plang, pid if (pid is not None) else 'doma_id'))
        datalist = [(e[0], wrtbAnker(e[3]),'') for e in data]
    elif (ptype == Modelelemtype.DOMA):
        datalist = WebDomain.indexlist(porigin =Domain.DOMAIN, plang=plang)
    elif (ptype == 'UDP'):
        datalist = Userdefprop.indexlist(pmapfilename=parameters.odmUDPMappingFileName())
    elif (ptype == Modelelemtype.DIAG):
        datalist = WebDiagram.indexlist()
    elif (ptype == Modelelemtype.DOCU) :
        datalist = WebDocument.indexlist()
    elif (ptype == Modelelemtype.INTF) :
        datalist = WebInterface.indexlist()
    elif (ptype == Modelelemtype.COLU):
        datalist = Schnittstelleattr.indexlist(pschnid=pid)
    elif (ptype == Modelelemtype.TABL) :
        datalist = Tabelle.indexlist(pschnid=pid)
    #fi
    return datalist
#namelist

def udpattrlist(plang,pthema,pgruppe):
    data = dbDML.select("""select attrname || ' ('||entname||')' name, attr_id 
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
 where exists (select 1 from udp_values
                    join user_defined_properties on udpr_id = udpv_udpr_id
                    where udpv_mode_id = amo.mode_id
                      and udpr_theme = '{}' and udpr_group = {}
                      and udpv_value != '.')
  ) order by upper(name)
      """.format(plang,pthema,'udpr_group' if pgruppe == '*' else "'{}'".format(pgruppe)))
    datalist = [(e[0], attrAnker(e[1]),e[1]) for e in data]
    return datalist
#udpattrlist


def pointlist(pliseid):
    data = dbDML.select("""
            select lise_x,lise_y,'Konnektor' as connector ,lise_linetype,lise_angle
            from linesegments
            where lise_relr_id = {}
            order by lise_seq
            """.format(pliseid))
    return data
#pointlist

def diagrelalist(pdiagid, plang):
    data = dbDML.select("""select relr_starttext_x,relr_starttext_y
       ,relr_starttext_breite,relr_starttext_hoehe
        ,relr_endtext_x,relr_endtext_y
        ,relr_endtext_breite,relr_endtext_hoehe
       ,relr_schriftfarbe,relr_schriftgroesse
       ,sfrom.lgtx_text fromname
       ,sto.lgtx_text toname
        ,relr_id
        
       ,relr_liniefarbe,relr_linienbreite,relr_liniedeckkraft
from relationreps
join relations b on b.rela_id = relr_mode_id
cross join languages spra
join lang_texts sfrom on  spra.lang_id = sfrom.lgtx_lang_id
            and sfrom.lgtx_attrname='RELA_TEXT_FROM'
            and sfrom.lgtx_mode_id = rela_id
join lang_texts sto on  spra.lang_id = sto.lgtx_lang_id
            and sto.lgtx_attrname='RELA_TEXT_TO'
            and sto.lgtx_mode_id = rela_id
where relr_diag_id = {}
and lower(spra.lang_iso_code2) = lower('{}')
""".format(pdiagid,plang))
    return data
#diagrelalist


def diagattrlist(plang,pdiagid):
    data = dbDML.select("""select 
        attr_id
       ,case when ana.lgtx_text is null then attr_displ_name else ana.lgtx_text end attr_displ_name
       ,attr_is_mandatory
       ,attr_is_descriptive
       ,case when (select 'TRUE' from key_elements 
                    where kele_attr_id = attr_id) IS NULL THEN 'FALSE' ELSE 'TRUE' end keys
       ,amo.mode_id
       ,eler_position_x,eler_position_y
      from elementreps
       join attributes on eler_mode_id = attr_id  
        join languages sp on sp.lang_iso_code2 = '{}'
        left join langattr  ana on ana.lgtx_attrname = 'ATTR_NAME'
                                and ana.lgtx_mode_id = attr_id
                                and ana.lang_id = sp.lang_id            
      where eler_diag_id = {}
      order by attr_displ_seq"""
                        .format(plang, pdiagid))
    return data
#diagattrlist

def keylist(p_entiid,p_lang):
    keys = dbDML.select("""select 0 as keyseq,keys_name,attrs,bezis from
    (select  keys_id,keys_name
                  ,group_concat(case when ana.lgtx_text is null then attr_displ_name else ana.lgtx_text end 
                                    ,', ') attrs
                  ,group_concat(rela_name, ', ') bezis
         from keys
         join key_elements on kele_keys_id = keys_id
            join languages sp on sp.lang_iso_code2 = '{}'
         left join attributes on attr_id = kele_attr_id
         left join langattr  ana on ana.lgtx_attrname = 'ATTR_NAME'
                                    and ana.lgtx_mode_id = attr_id
                                    and ana.lang_id = sp.lang_id            
         left join relations on rela_id = kele_rela_id
         where keys_enti_id = {}
           group by keys_id,keys_name)
                    """.format(p_lang,p_entiid))
    return keys
#keylist

def relalist (p_entiid,p_lang):
    bezi = dbDML.select("""
          with sprenti as 
          (select enti_id
                ,case when ena.lgtx_text is null then enti_name else ena.lgtx_text end enti_name
                ,lang_id,enti_enti_id
             from entities
              left join langattr ena on ena.lgtx_attrname = 'ENTI_NAME'
                                and ena.lgtx_mode_id = enti_id
           )
            select von.enti_id as von_enti_id,von.enti_name as von_name
                        		,case when bvon.lgtx_text is null then  rela_assoc_from_to else bvon.lgtx_text end  rela_assoc_from_to
    							,case rela_type
                           when '1:1' then 
                            case rela_mandatory_from_to
                                 when 'TRUE' THEN '1'
                                 else '0..1'
                               end
                           when 'M:N' then 
                            case rela_mandatory_from_to
                                 when 'TRUE' THEN '1..N'
                                 else '0..N'
                               end
                           when 'M:1' then 
                                case rela_mandatory_from_to
                                 when 'TRUE' THEN '1'
                                 else '0..1'
                               end         
                            end card1
    						,zu.enti_id as zu_enti_id,zu.enti_name as zu_name
    						,case when bzu.lgtx_text is null then  rela_assoc_to_from else bzu.lgtx_text end rela_assoc_to_from
    	                    ,case rela_type
    	                       when '1:1' then 
    	                          case rela_mandatory_to_from
    	                             when 'TRUE' THEN '1'
    	                             else '0..1'
    	                           end
    	                       when 'M:N' then 
    	                        case rela_mandatory_to_from
    	                             when 'TRUE' THEN '1..N'
    	                             else '0..N'
    	                           end
    	                       when 'M:1' then 
    	                            case rela_mandatory_to_from
    	                             when 'TRUE' THEN '1..N'
    	                             else '0..N'
    	                           end         
    	                        end card2
    						,rela_id,rela_type,rela_mandatory_from_to,rela_mandatory_to_from
    						,arcs_name,extr_source_id,rela_name
                            ,case when (select 1 from key_elements 
                                         join keys on keys_id = kele_keys_id
                                         where kele_rela_id = rela_id
                                         and keys_enti_id = von.enti_id
                                         ) IS NULL 
                            THEN 'FALSE' ELSE 'TRUE' end keys
                        from  sprenti as von
    					join relations on rela_enti_id_from = von.enti_id
    								        and not (rela_type = 'ISAS') 
    				    join languages sp on sp.lang_id = von.lang_id
                        left join langattr bvon on bvon.lgtx_attrname = 'RELA_TEXT_FROM'
                                and bvon.lgtx_mode_id = rela_id
                                and bvon.lang_id = sp.lang_id 
                        left join langattr bzu on bzu.lgtx_attrname = 'RELA_TEXT_TO'
                                and bzu.lgtx_mode_id = rela_id
                                and bzu.lang_id = sp.lang_id 
                        join sprenti as zu on zu.enti_id = rela_enti_id_to
                                        and zu.lang_id = sp.lang_id
                        left join arcs on arcs_enti_id = von.enti_id
                        left join external_refs on extr_mode_id = arcs_id
                        where  sp.lang_iso_code2 = '{}'
                           and (von.enti_id = {} or zu.enti_id = {})     
                        order by arcs_name 
                        """.format(p_lang,p_entiid, p_entiid))
    return bezi
#relalist

def udpnamen(pmeltname, pthema=None, pgruppe=None):
    if pgruppe is None:
        lsql = """select  udpr_theme,udpr_group,group_concat(udpr_name,',') attrs
                           from modelelem_type
                           join modelemtype_properties on metp_melt_id = melt_id  
                           join user_defined_properties on udpr_id = metp_udpr_id
                           where melt_shortname = '{}'
                        group by udpr_theme,udpr_group
                        order by udpr_theme,udpr_group""".format(pmeltname)
    elif pgruppe == '*':
        lsql="""select  udpr_theme,'*'gr,group_concat(udpr_name,',') attrs
                           from modelelem_type
                           join modelemtype_properties on metp_melt_id = melt_id  
                           join user_defined_properties on udpr_id = metp_udpr_id
                           where melt_shortname = '{}'
                           and udpr_theme = {} 
                        group by udpr_theme
                        order by udpr_theme""".format(pmeltname
                         ,'udpr_theme' if pthema is None else "'{}'".format(pthema))
    else:
        lsql = """select  udpr_theme,udpr_group,group_concat(udpr_name,',') attrs
                   from modelelem_type
                   join modelemtype_properties on metp_melt_id = melt_id  
                   join user_defined_properties on udpr_id = metp_udpr_id
                   where melt_shortname = '{}'
                   and udpr_theme = {} 
                   and udpr_group = '{}' 
                group by udpr_theme,udpr_group
                order by udpr_theme,udpr_group""".format(pmeltname
        , 'udpr_theme' if pthema is None else "'{}'".format(pthema)
            ,pgruppe)
    data = dbDML.select(lsql)
    return data
#udpnamen
def udpwerte(pmeltname, pthema, pgruppe, pid):
    data = dbDML.select("""select udpr_name,udpv_value
            from udp_values
            join user_defined_properties on udpr_id = udpv_udpr_id
                    and udpr_theme = '{}' and udpr_group = {}
            where udpv_mode_id = {}
            order by udpr_theme,udpr_group,udpr_name
            """.format(pthema, 'udpr_group' if pgruppe =='*'  else  "'{}'".format (pgruppe)
                       ,pid
            ))
    return data
#udpwerte

def wrtblist():
    return Domain.select(pwhere="doma_herkunft = 'DOM'", porderby='doma_name')
#wrtblist

def dokulist():
    return Document.dokulist()
#dokulist

def diaglist(pentiid=None):
    if pentiid is None:
        lsql = """  
        select diag_name,diag_id,diag_legendx,diag_legendy,breite,hoehe,diag_uc,diag_dc,diag_um
           from diagrams
           left join  (select diag_id size_diag_id,max(xpos + breite) breite,max(ypos + hoehe) hoehe
                FROM (select eler_diag_id diag_id,eler_position_x xpos,eler_width breite
                     ,eler_position_y ypos, eler_height hoehe
                     from elementreps
                     union all 
                     select relr_diag_id, relr_endtext_x xpos, relr_endtext_breite breite
                     ,relr_endtext_y ypos, relr_endtext_hoehe hoehe
                     from relationreps
                     union all 
                     select relr_diag_id, lise_x xpos, 3 breite
                     ,lise_y ypos, 3 hoehe
                     from relationreps
                     join linesegments on lise_relr_id = relr_id
                    )
                    group by size_diag_id
                ) on size_diag_id = diag_id
            order by upper(diag_name)"""
    else:
        lsql = """
        select diag_name,diag_id
        from diagrams
        join  elementreps on eler_diag_id = diag_id
        where eler_mode_id = {}
     order by upper(diag_name)""".format(pentiid)
    #fi
    data = dbDML.select(lsql)
    return data
#diaglist

def diagenti(pdiagid,plang):
    data = dbDML.select("""
            with recursive enti as
                ( select  0 entilev, enti_id, enti_odm_guid,enti_name from entities
                where enti_enti_guid is null
                union all
                select enti.entilev + 1,entities.enti_id,entities.enti_odm_guid
                ,entities.enti_name
                from entities
                    join enti on entities.enti_enti_guid = enti.enti_odm_guid
                )
            select 
                eler_position_x xpos,eler_width breite
                ,eler_position_y ypos, eler_height hoehe
                ,eler_opacity,eler_color
                ,eler_marginwidth,eler_marginopacity,eler_margincolor
                ,eler_fontsize, eler_fontcolor
                ,case when ena.lgtx_text is null then enti_name 
                                                else ena.lgtx_text end  entiname
                ,enti_id ,eler_index
                from elementreps
                join enti on enti_id = eler_mode_id
                join languages sp on sp.lang_iso_code2 = '{}'         
                left join langattr ena on ena.lgtx_attrname = 'ENTI_NAME'
                                        and ena.lgtx_mode_id = enti_id
                                        and ena.lang_id = sp.lang_id
                where eler_diag_id = {}
                order by entilev
    """.format(plang,pdiagid))
    return data
#diagenti

def wbgrelements(wrtbid):
    data = dbDML.select("""select dgrm_name, dgrm_beschr ,  doma_name
            ,doma_typ, doma_bin_inhalttyp, dgrm_uc
            ,dgrm_dc, dgrm_um, dgrm_dm
            , dgrm_doma_id_member, dgrm_id
            from domaingroup_members
            join domains on doma_id = dgrm_doma_id_member
            where dgrm_doma_id_group = {}
    """.format(wrtbid))
    return data
#wbgrelements

def udplist(ptyp):
    data = dbDML.select("""select distinct udpr_theme,bdet_group
                    from user_defined_properties
                    where udpr_theme = '{}'
                    order by udpr_theme,gruppe"""
            .format(ptyp))
    return data
#udplist
def transltext(pattr, pmodeid, plang):
    data = dbDML.select("""
    select lgtx_text
    from lang_texts
    join languages on lang_id = lgtx_lang_id
    join modelelement on mode_id = lgtx_mode_id
    where mode_id ={}
    and lgtx_attrname = '{}'
    and lower(lang_iso_code2) = lower('{}') 
    """.format(pmodeid, pattr, plang))
    return data[0][0] if (len(data)> 0) else ''
#translist

def liesarcs(pdiagid):
    data = dbDML.select("""
        select arcs_id,relr_id,enti_id,enti_name,eler_position_x,eler_position_y,eler_height,eler_width
        from arcs
        join relations  on arcs_id = rela_arcs_id_from or arcs_id = rela_arcs_id_to
        join relationreps on relr_mode_id = rela_id
        join entities on arcs_enti_id = enti_id
        join elementreps e on eler_mode_id = enti_id
        where relr_diag_id = {}
    """.format(pdiagid))
    return data
#liesarcs
def liesarcselem(pdiagid,parcsid):
    data = dbDML.select("""with lseg as (select linesegments.*
               ,row_number() over (PARTITION BY lise_relr_id ORDER BY lise_seq ASC) up
               ,row_number() over (PARTITION BY lise_relr_id ORDER BY lise_seq desc) down
           from linesegments)
        select relr_id,lsegstart.lise_x startx,lsegstart.lise_y starty
             ,lsegend.lise_x endx,lsegend.lise_y endy
             ,evon.enti_id,evon.enti_name,ezu.enti_id,ezu.enti_name
             ,case when lsegstart.up = 1 then lsegstart.lise_angel else lsegend.lise_angel  end winkel
        from arcs 
        join entities earc on earc.enti_id =arcs_enti_id
        join relations on rela_arcs_id_from = arcs_id or rela_arcs_id_to = arcs_id
        join relationreps on relr_mode_id = rela_id
        join lseg lsegstart        on relr_id = lsegstart.lise_relr_id
                            and lsegstart.up = 1 
        join lseg lsegend on relr_id = lsegend.lise_relr_id
                            and lsegend.up = 2   
    where relr_diag_id = {}
    and arcs_id = {}
    """.format(pdiagid,parcsid))
    return data
#liesarcselem