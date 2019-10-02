from IM_ODM import odmParam,transferModel
from IM_DB import dbParam,dbConnect,dbDDL,dbDML,dbErstelleTables
from IM_DB import dbParam,dbConnect,dbDML
import sys

def main():
    odmParam.initODMParam(pimDirec=sys.argv[1])
    #    print (odmParam.imDirectory+odmParam.modelName)
    dbParam.initDBParam(odmParam.imDirectory
                        , odmParam.imModelName + '.db');
    dbConnect.openDB(dbParam.dbDirectory, dbParam.dbName);
    dbParam.liesDefaultLang()
    l_sql = """with arcs2 as (select name || '_subtype' arcs_name, id arcs_enti_id,uc arcs_uc,um arcs_um ,id arcs_id from 
                                  (select enti_name as name, enti_id as id,enti_uc as uc ,enti_dc as um
                                          ,(select count(*) from entitaeten as e1 where e2.enti_odm_guid = e1.enti_enti_guid) as subanz
                                   from entitaeten as e2
                                   ) where subanz > 0)     
                select 'ISA', slave_enti_id,''
                            , 'TRUE','FALSE'
                            ,master_enti_id,'','TRUE','FALSE'
                            ,arcs_id,arcs_uc, arcs_um,'' beziname
                            ,enti_master_name,enti_slave_name
                            from arcs
                            join (select enti_id as master_enti_id,enti_name as enti_master_name
                                       , enti_odm_guid as master_guid from entitaeten) on master_enti_id = arcs_enti_id
                            join  (select enti_id as slave_enti_id,enti_name as enti_slave_name
                                       , enti_enti_guid as slave_master_guid from entitaeten) on slave_master_guid = master_guid
                    """;
#, e1.enti_name , e2.enti_name
    l_sql = """select von.enti_id as von_enti_id,von.enti_name as von_name,von.enti_odm_guid as von_guid
                        		,bezi_assoc_von_zu
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
    						,bezi_assoc_zu_von
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
                        from entitaeten as von
    					join beziehungen on bezi_enti_id_von = von.enti_id
                        join entitaeten as zu on zu.enti_id = bezi_enti_id_zu
                        left join arcs on arcs_id = bezi_arcs_id
                                   and bezi_enti_id_von = von.enti_id
                                   where bezi_type = 'ISA'
                        order by von.enti_name
""";
#      join entitaeten as e1 on e1.enti_id = bezi_enti_id_von
#      join entitaeten as e2 on e2.enti_id = bezi_enti_id_zu

#    l_sql = """select * from arcs  join entitaeten as ae on ae.enti_id = arcs_enti_id
#      join beziehungen on bezi_arcs_id = arcs_id  where arcs_name = 'Arc_9'"""
#insert into sprachtext (sptx_attrname,  sptx_text,  sptx_spra_id,sptx_mode_id, sptx_uc,   sptx_dc    )

    l_sql = """select enti_name,enti_comment,enti_id 
                from entitaeten
                join modellelemente on mode_enti_id = enti_id
                left join sprachtexte dename on dename.sptx_mode_id = mode_id
                left join sprachtexte dename on dename.sptx_mode_id = mode_id
                left join sprachen desp on desp.spra_id = sptx_spra_id
                where spra_iso_code2 = lower('{}')
                and sptx_mode_id > {}
                and sptx_attrname = '{}'
                """.format('en',700,'ENT_NAME')
    l_sql = """select * from benudef_wert  order by 2"""
    result = dbDML.select(l_sql)
    for row in result:
        print (row)
#main
#.format(entiId,entiId)
#where von.enti_id = {} or zu.enti_id = {}

if __name__ == '__main__':
    main()
