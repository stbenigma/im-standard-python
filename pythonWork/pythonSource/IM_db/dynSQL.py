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
    l_sql = """select ae.enti_id super_enti_id,ae.enti_name super_enti_name
               ,e1.enti_id sub_enti_id,e1.enti_name sub_enti_name
      from arcs
      join entitaeten as ae on ae.enti_id = arcs_enti_id 
      join (select bezi_arcs_id,count(*) alleanz
           , SUM(case when bezi_type in ('ISA','1:1') then 1 else 0 end) isaanz
           , SUM(case bezi_pflicht_assoc_von_zu when 'TRUE' then 1 else 0 end) nnvonanz
           , SUM(case bezi_pflicht_assoc_zu_von when 'TRUE' then 1 else 0 end) nnzuanz
            from  beziehungen
            where bezi_type in ('ISA','1:1') 
            group by bezi_arcs_id) as st
            on st.bezi_arcs_id = arcs_id AND alleanz = isaanz and alleanz = nnvonanz and alleanz = nnzuanz
      join beziehungen b1 on b1.bezi_arcs_id = arcs_id
      join entitaeten e1 on e1.enti_id = b1.bezi_enti_id_von  
    order by ae.enti_name""";
#      join entitaeten as e1 on e1.enti_id = bezi_enti_id_von
#      join entitaeten as e2 on e2.enti_id = bezi_enti_id_zu

#    l_sql = """select * from arcs  join entitaeten as ae on ae.enti_id = arcs_enti_id
#      join beziehungen on bezi_arcs_id = arcs_id  where arcs_name = 'Arc_9'"""
    l_sql = """select * from superenti"""
    result = dbDML.select(l_sql)
    for row in result:
        print (row)
#main
#.format(entiId,entiId)
#where von.enti_id = {} or zu.enti_id = {}

if __name__ == '__main__':
    main()
