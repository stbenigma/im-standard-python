from IM_DB import dbDML,dbLookup
from IM_HTML import web_sql

udpThemenSql:str = """select distinct bdeg_thema
                    from benudef_eigenschaft
                    join modelltyp_eigensch on mote_bdeg_id = bdeg_id
                    join modellelem_typ on melt_id = mote_melt_id
                                    and melt_kurzname = 'ATTR'
                                    and bdeg_thema != 'translation'
                    order by bdeg_thema"""

def langText(attrName, sprache, modeId):
   lsql= """select sptx_text
    from spraattr
    where spra_iso_code2 = lower('{}')
     and sptx_mode_id = {}
     and sptx_attrname = '{}'
    """.format(sprache,modeId,attrName)
   ltext = dbDML.select(lsql)[0][0]
   return ltext
#langText
def enti_name(lang,modeId):
    return langText('ENT_NAME', lang, modeId)
def enti_comment(lang,modeId):
    return langName('ENT_COMMENT',lang,modeId)
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
def beziAnker(id):
    return 'BEZI'+str(id)
def schlAnker(id):
    return 'SCHL'+str(id)
def wrtbAnker(id):
    return 'WRTB'+str(id)
def udpAnker(id):
    return 'UDP'+str(id)


def namelist(p_type,p_lang):
    if p_type == 'ENTI':
        data = dbDML.select("""select name,enti_id from 
        (select e1.enti_id
                ,case when ena.sptx_text is null then e1.enti_name 
                                                else ena.sptx_text end  name 
              from entitaeten e1
              join modellelement on mode_enti_id = enti_id
              join sprachen sp on sp.spra_iso_code2 = '{}'         
              left join spraattr ena on ena.sptx_attrname = 'ENT_NAME'
                                    and ena.sptx_mode_id = mode_id
                                    and ena.spra_id = sp.spra_id
              ) order by upper(name)
                  """.format(p_lang))
        datalist = [(e[0],entiAnker(e[1])) for e in data]
    elif (p_type == 'ATTR'):
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
          left join spraattr ena on ena.sptx_attrname = 'ENT_NAME'
                                and ena.sptx_mode_id = ame.mode_id
                                and ena.spra_id = sp.spra_id
          ) order by upper(name)
              """.format(p_lang))
        datalist = [(e[0], attrAnker(e[1])) for e in data]
    elif (p_type == 'WRTB'):
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
              """.format(p_lang))
        datalist = [(e[0], wrtbAnker(e[1])) for e in data]
    #fi
    return datalist
#namelist

def datalist(p_type,p_lang):
    if p_type == 'ENTI':
        #id, name, descr
        data = dbDML.select("""select * from 
        (select e1.enti_id
                ,case when ena.sptx_text is null then e1.enti_name 
                                                else ena.sptx_text end  name
                ,case when eco.sptx_text is null then e1.enti_beschr 
                                                else eco.sptx_text end  descr 
              from entitaeten e1
              join modellelement on mode_enti_id = enti_id
              join sprachen sp on sp.spra_iso_code2 = '{}'         
              left join spraattr ena on ena.sptx_attrname = 'ENT_NAME'
                                    and ena.sptx_mode_id = mode_id
                                    and ena.spra_id = sp.spra_id
              left join spraattr eco on eco.sptx_attrname = 'ENT_COMMENT'
                                    and eco.sptx_mode_id = mode_id
                                    and eco.spra_id = sp.spra_id
              ) order by upper(name)
                  """.format(p_lang))
        data = [(e[0],e[1],e[2]) for e in data]
    #fi
    return data
#datalist

def attrlist(p_entiid,p_lang):
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
      from attributes 
        join wertebereiche on wrtb_id = attr_wrtb_id
        join sprachen sp on sp.spra_iso_code2 = '{}'
        join modellelement amo on amo.mode_attr_id = attr_id
        left join spraattr  ana on ana.sptx_attrname = 'ATTR_NAME'
                                and ana.sptx_mode_id = amo.mode_id
                                and ana.spra_id = sp.spra_id            
        left join modellelement wmo on wmo.mode_attr_id = attr_id
        left join spraattr  wna on wna.sptx_attrname = 'WRTB_NAME'
                                and wna.sptx_mode_id = wmo.mode_id
                                and wna.spra_id = sp.spra_id            
      where attr_enti_id = {}
      order by upper(attr_tech_name)""".format(p_lang, p_entiid))
    return data
#attrlist