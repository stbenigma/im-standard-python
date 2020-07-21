import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../IM_db')
from IM_DB import dbDML, parameters
from IM_OBJECTS import *


# def langText(p_attrname, p_lang, p_modeid):
#    lsql= """select sptx_text
#     from spraattr
#     where spra_iso_code2 = lower('{}')
#      and sptx_mode_id = {}
#      and sptx_attrname = '{}'
#     """.format(p_lang, p_modeid, p_attrname)
#    data = dbDML.select(lsql)
#    try:
#        ltext = data[0][0]
#    except:
#        print (p_attrname,p_lang,p_modeid,data,sep=' | ')
#        return ""
#    return ltext
# #langText
#def enti_name(p_lang, p_modeid):
#    return langText('ENTI_NAME', p_lang, p_modeid)
def entiAnker(id):
    return 'ENTI'+str(id)
def attrAnker(id):
    return 'ATTR'+str(id)
def attgAnker(id):
    return 'ATTG'+str(id)
def beziAnker(id):
    return 'BEZI'+str(id)
def schlAnker(id):
    return 'SCHL'+str(id)
def wrtbAnker(id):
    return 'WRTB'+str(id)
def udpAnker(id):
    return 'UDP'+str(id)
def diagAnker(id):
    return 'DIAG'+str(id)
def dokuAnker(id):
    return 'DOKU'+str(id)
def elementid(pmodeid,ptyp):
    data = dbDML.select("""select mode_{}_id id
                            from modellelement 
                            where mode_id = {}""".format(ptyp.lower(),pmodeid))
    return data[0][0]
#entiid

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
        select case when spa.sptx_text is null then name 
                                                else spa.sptx_text end  name
                ,id,melt_kurzname type,melt_name anztype 
        from modelelem_doku
        join  modellelement on mode_id = modo_mode_id
        join modellelem_Typ on melt_id = mode_melt_id
        left join (select enti_id id ,enti_name name 
                   from entitaeten
                   union all
                   select attr_id id ,attr_anzname name 
                   from attributes 
                   union all
                   select tabl_id id ,TABL_NAME name 
                   from tabellen
                   union all
                   select SCHN_ID id ,SCHN_NAME name 
                   from schnittstellen
           ) on id = mode_enti_id or id = mode_attr_id or id = mode_tabl_id or id = mode_schn_id
         join sprachen sp on sp.spra_iso_code2 = '{}'
         left join spraattr spa on spa.sptx_attrname = case melt_kurzname when 'ENTI' then 'ENTI_NAME'
                                                            when 'ATTR' then 'ATTR_NAME'
                                                            else ''
                                                        end
                                    and spa.sptx_mode_id = mode_id
                                    and spa.spra_id = sp.spra_id
        where  MODO_DOKU_ID = {}
    )
    order by type,upper(name)
                  """.format(plang,pid))
    datalist = [Referenceentry(pid=e[1], pname=e[0], ptype=e[2], ptypename=e[3]
                        , panker=Entitaet().getbyid(e[1]).webanker() if e[2] == Entitaet._prefix.upper()
                            else Attribut().getbyid(e[1]).webanker() if e[2] == Attribut._prefix.upper()
                            else Tabelle().getbyid(e[1]).webanker() if e[2] == Tabelle._prefix.upper()
                            else Schnittstelle().getbyid(e[1]).webanker() if e[2] == Schnittstelle._prefix.upper()
                            else ''
                               ) for e in data]
    return datalist
#dokureflist

def refdokulist (pid, pelemtype):
    data = dbDML.select("""
        select name,id, 'DOKU' type, 'Dokumente'  anztype ,direct
        from (
            select doku_name name,doku_id id
                , case  melt_kurzname 
                   when 'ENTI' then mode_enti_id 
                   when 'ATTR' then mode_attr_id
                   when 'SCHN' then mode_schn_id
                   when 'TABL' then mode_tabl_id
                   else null
                   end ref_id 
                ,'TRUE' direct
                ,melt_kurzname ref_type
            from DOKUMENTE
            join MODELELEM_DOKU on MODO_DOKU_ID = DOKU_ID
            join modellelement on mode_id = MODO_MODE_ID
            join modellelem_typ on melt_id = mode_melt_id
            union all 
            select doku_name name,doku_id id,tabl_id ref_id,'FALSE' direct,'TABL' ref_type
            from DOKUMENTE
            join MODELELEM_DOKU on MODO_DOKU_ID = DOKU_ID
            join modellelement on mode_id = MODO_MODE_ID
            join (select schn_id, TABL_ID
                  from tabellen
                  join schnittstellen on SCHN_ID = TABL_SCHN_ID
                 ) on mode_schn_id = SCHN_ID        
            ) 
        where ref_type = '{}' and ref_id = {}  
    order by type,upper(name)
    """.format(pelemtype,pid))
    datalist = [Referenceentry(pid=e[1], pname=e[0], ptype=e[2], ptypename=e[3]
                               , pdirect = e[4]
                                ,panker=dokuAnker(e[1]) if e[2] == 'DOKU'
                                        else ''
                               )
                for e in data]
    return datalist
#refdokulist

def namelist(ptype, plang=None, pid=None):
    datalist = []
    if ptype == 'ENTI':
        datalist = Entitaet.indexlist(plang=plang)
    elif (ptype == 'ATTR'):
        data = dbDML.select("""select attrname || ' ('||entname||')' name, attr_id 
        from 
         (select case when ana.sptx_text is null then attr_anzname 
                                            else ana.sptx_text end  attrname
            ,attr_id
            ,case when ena.sptx_text is null then enti_name 
                                            else ena.sptx_text end  entname
          from attributes 
          join entitaeten on enti_id = attr_enti_id
          join sprachen sp on sp.spra_iso_code2 = '{}'         
          join modellelement amo on amo.mode_attr_id = attr_id
          left join spraattr ana on ana.sptx_attrname = 'ATTR_NAME'
                                and ana.sptx_mode_id = amo.mode_id
                                and ana.spra_id = sp.spra_id
          join modellelement ame on ame.mode_enti_id = enti_id
          left join spraattr ena on ena.sptx_attrname = 'ENTI_NAME'
                                and ena.sptx_mode_id = ame.mode_id
                                and ena.spra_id = sp.spra_id
          join wertebereiche on wrtb_id = attr_wrtb_id
                            and wrtb_id = {}
          union all
          select case when ana.sptx_text is null then attr_anzname
                                            else ana.sptx_text end  attrname
            ,attr_id
            ,bezi_name  beziname
          from attributes
          join beziehungen on attributes.attr_bezi_id = beziehungen.bezi_id
          join sprachen sp on sp.spra_iso_code2 = 'de'
          join modellelement amo on amo.mode_attr_id = attr_id
          left join spraattr ana on ana.sptx_attrname = 'ATTR_NAME'
                                and ana.sptx_mode_id = amo.mode_id
                                and ana.spra_id = sp.spra_id
          join wertebereiche on wrtb_id = attr_wrtb_id                          
                            and wrtb_id = {}
          ) order by upper(name)
              """.format(plang, pid if (pid is not None) else 'wrtb_id', pid if (pid is not None) else 'wrtb_id'))
        datalist = [(e[0], attrAnker(e[1]),'') for e in data]
    elif (ptype == 'ATTG'):
        data = dbDML.select("""select wbgrname || ' ('||wrtbname||')' name, wbgr_id,wrtbname,wrtb_id 
            from 
             (select  wbgr_name wbgrname
                ,wbgr_id,w2.wrtb_id
                ,case when ana.sptx_text is null then w2.wrtb_name 
                                                else ana.sptx_text end  wrtbname
              from wertebereichgruppen 
              join wertebereiche w2 on w2.wrtb_id = wbgr_wrtb_id_gruppe
              join sprachen sp on sp.spra_iso_code2 = '{}'         
              left join modellelement amo on amo.mode_attr_id = w2.wrtb_id
              left join spraattr ana on ana.sptx_attrname = 'WRTB_NAME'
                                    and ana.sptx_mode_id = amo.mode_id
                                    and ana.spra_id = sp.spra_id
              where wbgr_wrtb_id_member = {}
              ) order by wrtbname,upper(name)
                  """.format(plang, pid if (pid is not None) else 'wrtb_id'))
        datalist = [(e[0], wrtbAnker(e[3]),'') for e in data]
    elif (ptype == 'WRTB'):
        datalist = Wertebereich.indexlist(pherkunft = 'DOM',plang=plang)
    elif (ptype == 'UDP'):
        data = dbDML.select("""select  distinct bdeg_gruppe,bdeg_thema||'-'||bdeg_gruppe id
                             ,bdeg_thema
                            from benudef_eigenschaft 
                           where bdeg_thema = '{}'
                           union 
                           select '*' grp,'datamapping-alle','{}'
                           where exists (select  1 from
                                    benudef_eigenschaft 
                                    where bdeg_thema = '{}')
                        order by bdeg_gruppe""".format(parameters.odmUDPMappingFileName()
                                                       ,parameters.odmUDPMappingFileName()
                                                       ,parameters.odmUDPMappingFileName()))
        datalist = [(e[0], udpAnker(e[1]),'',e[2]) for e in data]
    elif (ptype == 'DIAG'):
        data = dbDML.select("""select diag_name ||' ('|| diat_bez ||')' name, diag_id 
        from 
         (select  diag_name
            ,diag_id
            ,diat_bez
          from diagramme 
          join diagrammtypen on diat_id = diag_diat_id
          ) order by upper(diat_bez),upper(diag_name)
              """)
        datalist = [(e[0], diagAnker(e[1]),'') for e in data]
    elif (ptype == 'DOKU') :
        datalist = Dokument.indexlist()
    elif (ptype == 'SCHN') :
        datalist = Schnittstelle.indexlist()
    elif (ptype == 'SCHA'):
        datalist = Schnittstelleattr.indexlist(pschnid=pid)
    elif (ptype == 'TABL') :
        datalist = Tabelle.indexlist(pschnid=pid)
    #fi
    return datalist
#namelist

def udpattrlist(plang,pthema,pgruppe):
    data = dbDML.select("""select attrname || ' ('||entname||')' name, attr_id 
        from 
 (select case when ana.sptx_text is null then attr_anzname 
                                    else ana.sptx_text end  attrname
    ,attr_id
    ,case when ena.sptx_text is null then enti_name 
                                    else ena.sptx_text end  entname
  from attributes 
  join entitaeten on enti_id = attr_enti_id
  join sprachen sp on sp.spra_iso_code2 = '{}'         
  join modellelement amo on amo.mode_attr_id = attr_id
  left join spraattr ana on ana.sptx_attrname = 'ATTR_NAME'
                        and ana.sptx_mode_id = amo.mode_id
                        and ana.spra_id = sp.spra_id
  join modellelement ame on ame.mode_enti_id = enti_id
  left join spraattr ena on ena.sptx_attrname = 'ENTI_NAME'
                        and ena.sptx_mode_id = ame.mode_id
                        and ena.spra_id = sp.spra_id
 where exists (select 1 from benudef_wert
                    join benudef_eigenschaft on bdeg_id = bdwe_bdeg_id
                    where bdwe_mode_id = amo.mode_id
                      and bdeg_thema = '{}' and bdeg_gruppe = {}
                      and bdwe_wert != '.')
  ) order by upper(name)
      """.format(plang,pthema,'bdeg_gruppe' if pgruppe == '*' else "'{}'".format(pgruppe)))
    datalist = [(e[0], attrAnker(e[1]),e[1]) for e in data]
    return datalist
#udpattrlist


def pointlist(pliseid):
    data = dbDML.select("""
            select lise_x,lise_y,lise_konnektor,lise_linientyp,lise_winkel
            from linie_segment
            where lise_beda_id = {}
            order by lise_rhfg
            """.format(pliseid))
    return data
#pointlist

def diagrelalist(pdiagid, plang):
    data = dbDML.select("""select beda_starttext_x,beda_starttext_y
       ,beda_starttext_breite,beda_starttext_hoehe
        ,beda_endtext_x,beda_endtext_y
        ,beda_endtext_breite,beda_endtext_hoehe
       ,beda_schriftfarbe,beda_schriftgroesse
       ,sfrom.sptx_text fromname
       ,sto.sptx_text toname
        ,beda_id
       ,beda_liniefarbe,beda_linienbreite,beda_liniedeckkraft
from beziehung_darst
join modellelement m on beziehung_darst.beda_mode_id = m.mode_id
join beziehungen b on m.mode_rela_id = b.bezi_id
cross join sprachen spra
join sprachtexte sfrom on  spra.spra_id = sfrom.sptx_spra_id
            and sfrom.sptx_attrname='RELA_TEXT_FROM'
            and sfrom.sptx_mode_id = m.mode_id
join sprachtexte sto on  spra.spra_id = sto.sptx_spra_id
            and sto.sptx_attrname='RELA_TEXT_TO'
            and sto.sptx_mode_id = m.mode_id
where beda_diag_id = {}
and lower(spra.spra_iso_code2) = lower('{}')
""".format(pdiagid,plang))
    return data
#diagrelalist


def diagattrlist(plang,pdiagid):
    data = dbDML.select("""select 
        attr_id
       ,case when ana.sptx_text is null then attr_anzname else ana.sptx_text end attr_anzname
       ,attr_pflichtattr
       ,attr_deskriptor
       ,case when (select 'TRUE' from schluesselelement 
                    where scel_attr_id = attr_id) IS NULL THEN 'FALSE' ELSE 'TRUE' end schluessel
       ,amo.mode_id
       ,eled_position_x,eled_position_y
      from elementdarst
       join modellelement amo on eled_mode_id = mode_id 
       join attributes on attr_id = mode_attr_id 
        join sprachen sp on sp.spra_iso_code2 = '{}'
        left join spraattr  ana on ana.sptx_attrname = 'ATTR_NAME'
                                and ana.sptx_mode_id = amo.mode_id
                                and ana.spra_id = sp.spra_id            
      where eled_diag_id = {}
      order by attr_anz_rhflg"""
                        .format(plang, pdiagid))
    return data
#diagattrlist

def keylist(p_entiid,p_lang):
    schl = dbDML.select("""select schl_laufnr,schl_name,attrs,bezis from
    (select  schl_id,schl_laufnr,schl_name
                  ,group_concat(case when ana.sptx_text is null then attr_anzname else ana.sptx_text end 
                                    ,', ') attrs
                  ,group_concat(bezi_name, ', ') bezis
         from schluessel
         join schluesselelement on scel_schl_id = schl_id
            join sprachen sp on sp.spra_iso_code2 = '{}'
         left join attributes on attr_id = scel_attr_id
         left join modellelement ma on ma.mode_attr_id = attr_id
         left join spraattr  ana on ana.sptx_attrname = 'ATTR_NAME'
                                    and ana.sptx_mode_id = ma.mode_id
                                    and ana.spra_id = sp.spra_id            
         left join beziehungen on bezi_id = scel_bezi_id
         where schl_enti_id = {}
           group by schl_id,schl_laufnr,schl_name)
                    """.format(p_lang,p_entiid))
    return schl
#keylist

def relalist (p_entiid,p_lang):
    bezi = dbDML.select("""
          with sprenti as 
          (select enti_id, enti_odm_guid
                ,case when ena.sptx_text is null then enti_name else ena.sptx_text end enti_name
                ,spra_id,enti_enti_id
             from entitaeten
             join modellelement on mode_enti_id = enti_id
              left join spraattr ena on ena.sptx_attrname = 'ENTI_NAME'
                                and ena.sptx_mode_id = mode_id
           )
            select von.enti_id as von_enti_id,von.enti_name as von_name,von.enti_odm_guid as von_guid
                        		,case when bvon.sptx_text is null then  bezi_assoc_von_zu else bvon.sptx_text end  bezi_assoc_von_zu
    							,case bezi_type
                           when '1:1' then 
                            case bezi_pflicht_assoc_von_zu
                                 when 'TRUE' THEN '1'
                                 else '0..1'
                               end
                           when 'M:N' then 
                            case bezi_pflicht_assoc_von_zu
                                 when 'TRUE' THEN '1..N'
                                 else '0..N'
                               end
                           when 'M:1' then 
                                case bezi_pflicht_assoc_von_zu
                                 when 'TRUE' THEN '1'
                                 else '0..1'
                               end         
                            end card1
    						,zu.enti_id as zu_enti_id,zu.enti_name as zu_name,zu.enti_odm_guid as zu_guid
    						,case when bzu.sptx_text is null then  bezi_assoc_zu_von else bzu.sptx_text end bezi_assoc_zu_von
    	                    ,case bezi_type
    	                       when '1:1' then 
    	                          case bezi_pflicht_assoc_zu_von
    	                             when 'TRUE' THEN '1'
    	                             else '0..1'
    	                           end
    	                       when 'M:N' then 
    	                        case bezi_pflicht_assoc_zu_von
    	                             when 'TRUE' THEN '1..N'
    	                             else '0..N'
    	                           end
    	                       when 'M:1' then 
    	                            case bezi_pflicht_assoc_zu_von
    	                             when 'TRUE' THEN '1..N'
    	                             else '0..N'
    	                           end         
    	                        end card2
    						,bezi_id,bezi_type,bezi_pflicht_assoc_von_zu,bezi_pflicht_assoc_zu_von
    						,arcs_name,extr_source_id,bezi_name
                            ,case when (select 1 from schluesselelement 
                                         join schluessel on schl_id = scel_schl_id
                                         where scel_bezi_id = bezi_id
                                         and schl_enti_id = von.enti_id
                                         ) IS NULL 
                            THEN 'FALSE' ELSE 'TRUE' end schluessel
                        from   sprachen sp          
                        join sprenti as von on von.enti_id = bezi_enti_id_von
                                        and von.spra_id = sp.spra_id
    					join beziehungen on bezi_enti_id_von = von.enti_id
    									 and not (bezi_type = 'ISA' and von.enti_enti_id is not NULL)
    					join modellelement on mode_rela_id = bezi_id
                        left join spraattr bvon on bvon.sptx_attrname = 'RELA_TEXT_FROM'
                                and bvon.sptx_mode_id = mode_id
                                and bvon.spra_id = sp.spra_id 
                        left join spraattr bzu on bzu.sptx_attrname = 'RELA_TEXT_TO'
                                and bzu.sptx_mode_id = mode_id
                                and bzu.spra_id = sp.spra_id 
                        join sprenti as zu on zu.enti_id = bezi_enti_id_zu
                                        and zu.spra_id = sp.spra_id
                        left join arcs on arcs_enti_id = von.enti_id
                        left join externalrefs on extr_mode_id = arcs_id
                        where  sp.spra_iso_code2 = '{}'
                           and (von.enti_id = {} or zu.enti_id = {})     
                        order by arcs_name 
                        """.format(p_lang,p_entiid, p_entiid))
    return bezi
#relalist

def udpnamen(pmeltname, pthema=None, pgruppe=None):
    if pgruppe is None:
        lsql = """select  bdeg_thema,bdeg_gruppe,group_concat(bdeg_name,',') attrs
                           from modellelem_typ
                           join modelltyp_eigensch on mote_melt_id = melt_id  
                           join benudef_eigenschaft on bdeg_id = mote_bdeg_id
                           where melt_kurzname = '{}'
                        group by bdeg_thema,bdeg_gruppe
                        order by bdeg_thema,bdeg_gruppe""".format(pmeltname)
    elif pgruppe == '*':
        lsql="""select  bdeg_thema,'*'gr,group_concat(bdeg_name,',') attrs
                           from modellelem_typ
                           join modelltyp_eigensch on mote_melt_id = melt_id  
                           join benudef_eigenschaft on bdeg_id = mote_bdeg_id
                           where melt_kurzname = '{}'
                           and bdeg_thema = {} 
                        group by bdeg_thema
                        order by bdeg_thema""".format(pmeltname
                         ,'bdeg_thema' if pthema is None else "'{}'".format(pthema))
    else:
        lsql = """select  bdeg_thema,bdeg_gruppe,group_concat(bdeg_name,',') attrs
                   from modellelem_typ
                   join modelltyp_eigensch on mote_melt_id = melt_id  
                   join benudef_eigenschaft on bdeg_id = mote_bdeg_id
                   where melt_kurzname = '{}'
                   and bdeg_thema = {} 
                   and bdeg_gruppe = '{}' 
                group by bdeg_thema,bdeg_gruppe
                order by bdeg_thema,bdeg_gruppe""".format(pmeltname
        , 'bdeg_thema' if pthema is None else "'{}'".format(pthema)
            ,pgruppe)
    data = dbDML.select(lsql)
    return data
#udpnamen
def udpwerte(pmeltname, pthema, pgruppe, pid):
    data = dbDML.select("""select bdeg_name,bdwe_wert
            from benudef_wert
            join modellelement on mode_id = bdwe_mode_id
                                    and ({} = {}) 
            join benudef_eigenschaft on bdeg_id = bdwe_bdeg_id
                    and bdeg_thema = '{}' and bdeg_gruppe = {}
            order by bdeg_thema,bdeg_gruppe,bdeg_name
            """.format("mode_{}_id".format(pmeltname.lower() )
                        ,pid
                       , pthema, 'bdeg_gruppe' if pgruppe =='*'  else  "'{}'".format (pgruppe)
                       ))
    return data
#udpwerte

def wrtblist():
    return Wertebereich.select(pwhere="wrtb_herkunft = 'DOM'", porderby='wrtb_name')
#wrtblist

def dokulist():
    return Dokument.dokulist()
#dokulist

def diaglist(pentiid=None):
    if pentiid is None:
        lsql = """  
        select diag_name,diag_id,diag_legendx,diag_legendy,breite,hoehe,diag_uc,diag_dc,diag_um
           from diagramme
           left join  (select diag_id size_diag_id,max(xpos + breite) breite,max(ypos + hoehe) hoehe
                FROM (select eled_diag_id diag_id,eled_position_x xpos,eled_breite breite
                     ,eled_position_y ypos, eled_hoehe hoehe
                     from elementdarst
                     union all 
                     select beda_diag_id, beda_endtext_x xpos, beda_endtext_breite breite
                     ,beda_endtext_y ypos, beda_endtext_hoehe hoehe
                     from beziehung_darst
                     union all 
                     select beda_diag_id, lise_x xpos, 3 breite
                     ,lise_y ypos, 3 hoehe
                     from beziehung_darst
                     join linie_segment on lise_beda_id = beda_id
                    )
                    group by size_diag_id
                ) on size_diag_id = diag_id
            order by upper(diag_name)"""
    else:
        lsql = """
        select diag_name,diag_id
        from diagramme
        join  elementdarst on eled_diag_id = diag_id
        join modellelement on mode_id = eled_mode_id
        where mode_enti_id = {}
     order by upper(diag_name)""".format(pentiid)
    #fi
    data = dbDML.select(lsql)
    return data
#diaglist

def diagenti(pdiagid,plang):
    data = dbDML.select("""
            with recursive enti as
                ( select  0 entilev, enti_id, enti_odm_guid,enti_name from entitaeten
                where enti_enti_guid is null
                union all
                select enti.entilev + 1,entitaeten.enti_id,entitaeten.enti_odm_guid
                ,entitaeten.enti_name
                from entitaeten
                    join enti on entitaeten.enti_enti_guid = enti.enti_odm_guid
                )
            select 
                eled_position_x xpos,eled_breite breite
                ,eled_position_y ypos, eled_hoehe hoehe
                ,eled_deckkraft,eled_farbe
                ,eled_randbreite,eled_randdeckkraft,eled_randfarbe
                ,eled_schriftgroesse, eled_schriftfarbe
                ,case when ena.sptx_text is null then enti_name 
                                                else ena.sptx_text end  entiname
                ,enti_id ,eled_index
                from elementdarst
                join modellelement on mode_id = eled_mode_id
                join enti on enti_id = mode_enti_id
                join sprachen sp on sp.spra_iso_code2 = '{}'         
                left join spraattr ena on ena.sptx_attrname = 'ENTI_NAME'
                                        and ena.sptx_mode_id = mode_id
                                        and ena.spra_id = sp.spra_id
                where eled_diag_id = {}
                order by entilev
    """.format(plang,pdiagid))
    return data
#diagenti

def wbgrelements(wrtbid):
    data = dbDML.select("""select wbgr_name, wbgr_beschr ,  wrtb_name
            ,wrtb_typ, wrtb_bin_inhalttyp, wbgr_uc
            ,wbgr_dc, wbgr_um, wbgr_dm
            , wbgr_wrtb_id_member, wbgr_id
            from wertebereichgruppen
            join wertebereiche on wrtb_id = wbgr_wrtb_id_member
            where wbgr_wrtb_id_gruppe = {}
    """.format(wrtbid))
    return data
#wbgrelements

def udplist(ptyp):
    data = dbDML.select("""select distinct bdeg_thema,bdet_gruppe
                    from benudef_eigenschaft
                    where bdeg_thema = '{}'
                    order by bdeg_thema,gruppe"""
            .format(ptyp))
    return data
#udplist
def transltext(pattr, pmodeid, plang):
    data = dbDML.select("""
    select sptx_text
    from sprachtexte
    join sprachen on spra_id = sptx_spra_id
    join modellelement on mode_id = sptx_mode_id
    where mode_id ={}
    and sptx_attrname = '{}'
    and lower(spra_iso_code2) = lower('{}') 
    """.format(pmodeid, pattr, plang))
    return data[0][0] if (len(data)> 0) else ''
#translist

def liesarcs(pdiagid):
    data = dbDML.select("""
        select arcs_id,beda_id,enti_id,enti_name,eled_position_x,eled_position_y,eled_hoehe,eled_breite
        from arcs
        join beziehungen  on arcs_id = bezi_von_arcs_id or arcs_id = bezi_zu_arcs_id
        join modellelement  m on bezi_id = m.mode_rela_id
        join beziehung_darst on beda_mode_id = m.mode_id
        join entitaeten on arcs_enti_id = enti_id
        join modellelement m2 on m2.mode_enti_id = enti_id
        join elementdarst e on m2.mode_id = eled_mode_id
        where beda_diag_id = {}
    """.format(pdiagid))
    return data
#liesarcs
def liesarcselem(pdiagid,parcsid):
    data = dbDML.select("""with lseg as (select linie_segment.*
               ,row_number() over (PARTITION BY lise_beda_id ORDER BY lise_rhfg ASC) up
               ,row_number() over (PARTITION BY lise_beda_id ORDER BY lise_rhfg desc) down
           from linie_segment)
        select beda_id,lsegstart.lise_x startx,lsegstart.lise_y starty
             ,lsegend.lise_x endx,lsegend.lise_y endy
             ,evon.enti_id,evon.enti_name,ezu.enti_id,ezu.enti_name
             ,case when lsegstart.up = 1 then lsegstart.lise_winkel else lsegend.lise_winkel  end winkel
        from arcs 
        join entitaeten earc on earc.enti_id =arcs_enti_id
        join beziehungen on bezi_von_arcs_id = arcs_id or bezi_zu_arcs_id = arcs_id
        join modellelement on bezi_id = mode_rela_id
        join entitaeten evon on evon.enti_odm_guid = bezi_source_enti_guid
        join entitaeten ezu on ezu.enti_odm_guid = bezi_target_enti_guid
        join beziehung_darst on beda_mode_id = mode_id
        join lseg lsegstart        on beda_id = lsegstart.lise_beda_id
             and ((lsegstart.up = 1 and bezi_source_enti_guid = earc.enti_odm_guid
                ) or (lsegstart.down = 1 and bezi_target_enti_guid = earc.enti_odm_guid
                ))
        join lseg lsegend on beda_id = lsegend.lise_beda_id
             and ((lsegend.up = 2 and bezi_source_enti_guid = earc.enti_odm_guid
                ) or (lsegend.down = 2 and bezi_target_enti_guid = earc.enti_odm_guid
                ))                
    where beda_diag_id = {}
    and arcs_id = {}
    """.format(pdiagid,parcsid))
    return data
#liesarcselem