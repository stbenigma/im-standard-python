import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../IM_db')
from IM_DB import dbDML, parameters
from IM_OBJECTS import *
from WEB_OBJECTS import *




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
        datalist = Userdefprop.indexlist(pudptheme=parameters.odmUDPMappingFileName())
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