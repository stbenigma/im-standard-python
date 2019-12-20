import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../IM_db')
from IM_DB import dbDML,dbLookup,parameters


def langText(p_attrname, p_lang, p_modeid):
   lsql= """select sptx_text
    from spraattr
    where spra_iso_code2 = lower('{}')
     and sptx_mode_id = {}
     and sptx_attrname = '{}'
    """.format(p_lang, p_modeid, p_attrname)
   ltext = dbDML.select(lsql)[0][0]
   return ltext
#langText
def enti_name(p_lang, p_modeid):
    return langText('ENTI_NAME', p_lang, p_modeid)
def enti_comment(lang,modeId):
    return langName('ENTI_COMMENT',lang,modeId)
def attr_name(lang,modeId):
    return langName('ATTR_NAME',lang,modeId)
def attr_comment(lang,modeId):
    return langName('ATTR_COMMENT',lang,modeId)
def bezi_from(lang,modeId):
    return langName('TEXT_FROM',lang,modeId)
def bezi_to(lang,modeId):
    return langName('TEXT_TO',lang,modeId)
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
def elementid(pmodeid,ptyp):
    data = dbDML.select("""select mode_{}_id id
                            from modellelement 
                            where mode_id = {}""".format(ptyp.lower(),pmodeid))
    return data[0][0]
#entiid

def namelist(ptype, plang, pwrtbid=None):
    if ptype == 'ENTI':
        data = dbDML.select("""select name,enti_id from 
        (select e1.enti_id
                ,case when ena.sptx_text is null then e1.enti_name 
                                                else ena.sptx_text end  name 
              from entitaeten e1
              join modellelement on mode_enti_id = enti_id
              join sprachen sp on sp.spra_iso_code2 = '{}'         
              left join spraattr ena on ena.sptx_attrname = 'ENTI_NAME'
                                    and ena.sptx_mode_id = mode_id
                                    and ena.spra_id = sp.spra_id
              ) order by upper(name)
                  """.format(plang))
        datalist = [(e[0],entiAnker(e[1])) for e in data]
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
          ) order by upper(name)
              """.format(plang, pwrtbid if (pwrtbid is not None) else 'wrtb_id'))
        datalist = [(e[0], attrAnker(e[1])) for e in data]
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
                  """.format(plang, pwrtbid if (pwrtbid is not None) else 'wrtb_id' ))
        datalist = [(e[0], wrtbAnker(e[3])) for e in data]
    elif (ptype == 'WRTB'):
        data = dbDML.select("""select wrtbname ||' ('|| anz ||')' name, wrtb_id 
        from 
         (select case when wna.sptx_text is null then wrtb_name 
                                            else wna.sptx_text end  wrtbname
            ,wrtb_id
            ,(select count(*) from attributes where attr_wrtb_id = wrtb_id) anz 
          from wertebereiche 
          join sprachen sp on sp.spra_iso_code2 = '{}'         
          left join modellelement wmo on wmo.mode_wrtb_id = wrtb_id
          left join spraattr wna on wna.sptx_attrname = 'WRTB_NAME'
                                and wna.sptx_mode_id = wmo.mode_id
                                and wna.spra_id = sp.spra_id
          ) order by upper(name)
              """.format(plang))
        datalist = [(e[0], wrtbAnker(e[1])) for e in data]
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
        datalist = [(e[0], udpAnker(e[1]),e[2]) for e in data]
    elif (ptype == 'DIAG'):
        data = dbDML.select("""select diag_name ||' ('|| diat_bez ||')' name, diag_id 
        from 
         (select  diag_name
            ,diag_id
            ,diat_bez
          from diagramme 
          join diagrammtypen on diat_id = diag_diat_id
          ) order by upper(diat_bez),upper(diag_name)
              """.format(plang))
        datalist = [(e[0], diagAnker(e[1])) for e in data]
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
def entilist(p_lang):
    #id, name, descr
    #group_concat('<a href="#ENTI'||sub_enti_id||'" target="details">'
    #                            ||sub_enti_name||'</a>'
    #                    ,', ') subent
    data = dbDML.select("""select * from 
    (select e1.enti_id
            ,case when ena.sptx_text is null then e1.enti_name 
                                            else ena.sptx_text end  name
            ,case when eco.sptx_text is null then e1.enti_beschr 
                                            else eco.sptx_text end  descr 
          ,e1.enti_uc
          ,e1.enti_dc
          ,super_enti_name
          ,super_enti_id
         ,(select group_concat(sub_enti_id||':'||sub_enti_name,',') subent
          from superenti where super_enti_id = e1.enti_id
          ) as subentities
        ,(select group_concat(syno_name,', ') synos
            from (select case when sna.sptx_text is null then syno_name 
                                            else sna.sptx_text end syno_name
              from synonyme
              left join modellelement on mode_syno_id = syno_id
              left join spraattr sna on sna.sptx_attrname = 'SYNO_NAME'
                                and sna.sptx_mode_id = mode_id
                                and sna.spra_id = sp.spra_id
             where syno_enti_id = e1.enti_id
             )
          ) as synos
          from entitaeten e1
          join modellelement on mode_enti_id = enti_id
          join sprachen sp on sp.spra_iso_code2 = '{}'         
          left join spraattr ena on ena.sptx_attrname = 'ENTI_NAME'
                                and ena.sptx_mode_id = mode_id
                                and ena.spra_id = sp.spra_id
          left join spraattr eco on eco.sptx_attrname = 'ENTI_COMMENT'
                                and eco.sptx_mode_id = mode_id
                                and eco.spra_id = sp.spra_id
          left join (select case when ena.sptx_text is null then super_enti_name 
                                            else ena.sptx_text end  super_enti_name
                            ,super_enti_id
                            ,sub_enti_id
                            ,ena.spra_id super_spra_id
                       from superenti
                       left join modellelement on mode_enti_id = super_enti_id
                       left join spraattr ena on ena.sptx_attrname = 'ENTI_NAME'
                                and ena.sptx_mode_id = mode_id
                    ) on  sub_enti_id = e1.enti_id
                      and (super_spra_id = sp.spra_id 
                            or super_spra_id is null)
          ) order by upper(name)
              """.format(p_lang))
    data = [(e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8]) for e in data]
    return data
#entilist

def pointlist(pliseid):
    data = dbDML.select("""
            select lise_x,lise_y,lise_konnektor,lise_linientyp
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
join beziehungen b on m.mode_bezi_id = b.bezi_id
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

def attrlist(p_lang,p_entiid=None):
    data = dbDML.select("""select 
        attr_id
       ,case when ana.sptx_text is null then attr_anzname else ana.sptx_text end attr_anzname
       ,case when wna.sptx_text is null then wrtb_name else wna.sptx_text end wrtb_name
       ,wrtb_id
       ,wrtb_typ
       ,attr_pflichtattr
       ,attr_deskriptor
       ,attr_sprachabhaengig
       ,attr_historisiert
       ,attr_wiederholt
       ,attr_verschluesselt
       ,case when (select 'TRUE' from schluesselelement where scel_attr_id = attr_id) IS NULL THEN 'FALSE' ELSE 'TRUE' end schluessel
       ,attr_tech_name
       ,attr_tooltip
       ,attr_uc,attr_dc
       ,attr_um,attr_dm
       ,case when aco.sptx_text is null then attr_beschr else aco.sptx_text end attr_beschr
       ,attr_bezi_id
       ,attr_odm_guid
       ,amo.mode_id
       ,attr_enti_id
       ,wrtb_name
      from attributes 
        join wertebereiche on wrtb_id = attr_wrtb_id
        join sprachen sp on sp.spra_iso_code2 = '{}'
        join modellelement amo on amo.mode_attr_id = attr_id
        left join spraattr  ana on ana.sptx_attrname = 'ATTR_NAME'
                                and ana.sptx_mode_id = amo.mode_id
                                and ana.spra_id = sp.spra_id            
        left join spraattr  aco on aco.sptx_attrname = 'ATTR_COMMENT'
                                and aco.sptx_mode_id = amo.mode_id
                                and aco.spra_id = sp.spra_id            
        left join modellelement wmo on wmo.mode_wrtb_id = wrtb_id
        left join spraattr  wna on wna.sptx_attrname = 'WRTB_NAME'
                                and wna.sptx_mode_id = wmo.mode_id
                                and wna.spra_id = sp.spra_id            
      where attr_enti_id = {}
      order by {}"""
                        .format(p_lang, p_entiid if (p_entiid is not None) else 'attr_enti_id'
                                ,'attr_anz_rhflg' if (p_entiid is not None) else 'attr_tech_name'))
    return data
#attrlist

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
                ,spra_id
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
    						,arcs_name,arcs_odm_guid,bezi_name
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
    									 and bezi_type != 'ISA'
    					join modellelement on mode_bezi_id = bezi_id
                        left join spraattr bvon on bvon.sptx_attrname = 'TEXT_FROM'
                                and bvon.sptx_mode_id = mode_id
                                and bvon.spra_id = sp.spra_id 
                        left join spraattr bzu on bzu.sptx_attrname = 'TEXT_TO'
                                and bzu.sptx_mode_id = mode_id
                                and bzu.spra_id = sp.spra_id 
                        join sprenti as zu on zu.enti_id = bezi_enti_id_zu
                                        and zu.spra_id = sp.spra_id
                        left join arcs on arcs_id = bezi_arcs_id
                                   and bezi_enti_id_von = von.enti_id
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
    data = dbDML.select("""select  bdwe_wert
            from benudef_wert
            join modellelement on mode_id = bdwe_mode_id
                                    and ({} = {}) 
            join benudef_eigenschaft on bdeg_id = bdwe_bdeg_id
                    and bdeg_thema = '{}' and bdeg_gruppe = {}
            order by bdeg_thema,bdeg_gruppe,bdeg_name
            """.format("mode_" +
                       ("enti" if pmeltname == 'ENTI'
                        else "attr" if pmeltname == 'ATTR'
                       else "")
                       + "_id" ,pid
                       , pthema, 'bdeg_gruppe' if pgruppe =='*'  else  "'{}'".format (pgruppe)
                       ))
    return data
#udpwerte

def wrtblist(p_lang):
    data = dbDML.select("""select * from 
    (select wrtb_id, case when wna.sptx_text is null then wrtb_name 
                                    else wna.sptx_text end  wrtbname
            ,wrtb_business_rule, wrtb_name
            ,wrtb_beschr, wrtb_typ
            ,wrtb_zpkt_minwert, wrtb_zpkt_maxwert
            ,wrtb_zpkt_granularitaet, wrtb_text_maxlng
            ,wrtb_text_syntaxregel, wrtb_num_maxwert
            ,wrtb_num_minwert, wrtb_num_vorkstellen
            ,wrtb_num_nachkstellen, wrtb_num_rundng_einh
            ,wrtb_num_pheh_id, wrtb_bin_inhalttyp
            ,wrtb_bin_spfo_id, wrtb_odm_guid
            ,wrtb_uc, wrtb_dc
            ,wrtb_um, wrtb_dm
            ,wrtb_datatype_ref
        from wertebereiche 
        join sprachen sp on sp.spra_iso_code2 = '{}'         
        left join modellelement wmo on wmo.mode_wrtb_id = wrtb_id
        left join spraattr wna on wna.sptx_attrname = 'WRTB_NAME'
                                and wna.sptx_mode_id = wmo.mode_id
                                and wna.spra_id = sp.spra_id
        ) order by upper(wrtbname)
      """.format(p_lang))
    return data
#wrtblist

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
def projektlangs():
    data = dbDML.select("select proj_sprachen from projekt")
    return data[0][0]
#
def wrtbwerte(p_wrtbid):
    data = dbDML.select("""
             select vgwt_sortrhfg,vgwt_wert,vgwt_anzeige,vgwt_beschr 
               from vorgabewerte
               where vgwt_wrtb_id = {}
               order by vgwt_sortrhfg
    """.format(p_wrtbid))
    return data
#wrtbwerte

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