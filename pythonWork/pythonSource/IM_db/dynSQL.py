
import sys
from  IM_DB  import parameters,dbConnect,dbParam,dbDML

def main(p_imdirec=None, p_modelname=None):

    parameters.initparam(p_imdirec)
    print ("dynsql",parameters.dbFilePath())
    dbConnect.openDB(parameters.dbFilePath());

    dbParam.liesDefaultLang()

#, e1.enti_name , e2.enti_name
    l_sql ="""select attr_tech_name || ' ('||enti_name||')' as vollname ,attr_odm_guid,attr_tech_name
            ,attr_anzname,enti_odm_guid,attr_uc
           ,attr_dc,attr_beschr,enti_name
           ,wrtb_id,wrtb_name,wrtb_typ
           ,attr_id,enti_id
           ,(select group_concat('<a href="#SCHL'||schl_id||'" target="details">'
                                    ||schl_laufnr||'</a>',',')
               from schluesselelement 
                join schluessel on schl_id = scel_schl_id
                where scel_attr_id = attr_id
            ) as schluessel
          from (select  attr_tech_name, attr_odm_guid, 
                case when ana.sptx_text is null then attr_anzname else ana.sptx_text end attr_anzname
                , case when abe.sptx_text is null then attr_beschr else abe.sptx_text end  attr_beschr
                ,attr_id,sp.spra_id,
                attr_uc,attr_dc,attr_enti_id,attr_wrtb_id
                 from attributes
                 join modellelement on mode_attr_id = attr_id
                 join sprachen sp on sp.spra_iso_code2 = '{}'
                 left join spraattr  ana on ana.sptx_attrname = 'ATTR_NAME'
                                    and ana.sptx_mode_id = mode_id
                                    and ana.spra_id = sp.spra_id 
                 left join spraattr  abe on abe.sptx_attrname = 'ATTR_COMMENT'
                                    and abe.sptx_mode_id = mode_id 
                                    and abe.spra_id = sp.spra_id
                ) attr         
          join (select case when ena.sptx_text is null then enti_name else ena.sptx_text end enti_name
                    ,enti_id,spra_id spra_id,enti_odm_guid
                 from entitaeten 
                 join modellelement on mode_enti_id = enti_id
                left join spraattr ena on ena.sptx_attrname = 'ENTI_NAME'
                                and ena.sptx_mode_id = mode_id 
                ) ent on enti_id = attr_enti_id
                     and ent.spra_id = attr.spra_id
          join wertebereiche on wrtb_id = attr_wrtb_id
          order by upper(attr_tech_name)
          """.format('de')

    #l_sql = """select * from entitaeten where enti_id = 835"""
    result = dbDML.select(l_sql)
    for row in result:
        print (row)
#main
#.format(entiId,entiId)
#where von.enti_id = {} or zu.enti_id = {}

if __name__ == '__main__':
    import sys
    main(p_imdirec=sys.argv[1] if (len(sys.argv) > 1) else None
        ,p_modelname=sys.argv[2] if (len(sys.argv) > 2) else None)
