import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../IM_db')
from IM_DB import dbDML, parameters
from IM_OBJECTS import *
from WEB_OBJECTS import *


# def  namelist(ptype, plang=None, pid=None):
#     datalist = []
#     if ptype == Modelelemtype.ENTI:
#         datalist = WebEntity.indexlist(plang=plang)
#     elif (ptype ==  Modelelemtype.ATTR):
#         datalist = WebAttribute.indexlist(plang=plang)
#     elif (ptype == Modelelemtype.DGRM):
#         data = dbDML.select("""select wbgrname || ' ('||wrtbname||')' name, dgrm_id,wrtbname,doma_id
#             from
#              (select  dgrm_name wbgrname
#                 ,dgrm_id,w2.doma_id
#                 ,case when ana.lgtx_text is null then w2.doma_name
#                                                 else ana.lgtx_text end  wrtbname
#               from domaingroup_members
#               join domains w2 on w2.doma_id = dgrm_doma_id_group
#               join languages sp on sp.lang_iso_code2 = '{}'
#               left join langattr ana on ana.lgtx_attrname = 'DOMA_NAME'
#                                     and ana.lgtx_mode_id = w2.doma_id
#                                     and ana.lang_id = sp.lang_id
#               where dgrm_doma_id_member = {}
#               ) order by wrtbname,upper(name)
#                   """.format(plang, pid if (pid is not None) else 'doma_id'))
#         datalist = [(e[0], wrtbAnker(e[3]),'') for e in data]
#     elif (ptype == Modelelemtype.DOMA):
#         datalist = WebDomain.indexlist(porigin =Domain.DOMAIN, plang=plang)
#     elif (ptype == Modelelemtype.DIAG):
#         datalist = WebDiagram.indexlist()
#     elif (ptype == Modelelemtype.DOCU) :
#         datalist = WebDocument.indexlist()
#     elif (ptype == Modelelemtype.INTF) :
#         datalist = WebInterface.indexlist()
#     elif (ptype == Modelelemtype.COLU):
#         datalist = Schnittstelleattr.indexlist(pschnid=pid)
#     elif (ptype == Modelelemtype.TABL) :
#         datalist = Tabelle.indexlist(pschnid=pid)
#     #fi
#     return datalist
# #namelist

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


# def diagenti(pdiagid,plang):
#     data = dbDML.select("""
#             with recursive enti as
#                 ( select  0 entilev, enti_id, enti_odm_guid,enti_name from entities
#                 where enti_enti_guid is null
#                 union all
#                 select enti.entilev + 1,entities.enti_id,entities.enti_odm_guid
#                 ,entities.enti_name
#                 from entities
#                     join enti on entities.enti_enti_guid = enti.enti_odm_guid
#                 )
#             select
#                 eler_position_x xpos,eler_width breite
#                 ,eler_position_y ypos, eler_height hoehe
#                 ,eler_opacity,eler_color
#                 ,eler_marginwidth,eler_marginopacity,eler_margincolor
#                 ,eler_fontsize, eler_fontcolor
#                 ,case when ena.lgtx_text is null then enti_name
#                                                 else ena.lgtx_text end  entiname
#                 ,enti_id ,eler_index
#                 from elementreps
#                 join enti on enti_id = eler_mode_id
#                 join languages sp on sp.lang_iso_code2 = '{}'
#                 left join langattr ena on ena.lgtx_attrname = 'ENTI_NAME'
#                                         and ena.lgtx_mode_id = enti_id
#                                         and ena.lang_id = sp.lang_id
#                 where eler_diag_id = {}
#                 order by entilev
#     """.format(plang,pdiagid))
#     return data
# #diagenti

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
