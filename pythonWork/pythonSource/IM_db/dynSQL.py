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
    l_sql = """select arcs.*, e1.enti_name , e2.enti_name from arcs
      join beziehungen on bezi_arcs_id = arcs_id 
      join entitaeten as e1 on e1.enti_id = bezi_enti_id_von 
      join entitaeten as e2 on e2.enti_id = bezi_enti_id_zu
    where arcs_name = 'Arc_9' 
    order by e2.enti_name""";
    result = dbDML.select(l_sql)
    for row in result:
        print (row)
#main
#.format(entiId,entiId)
#where von.enti_id = {} or zu.enti_id = {}

if __name__ == '__main__':
    main()
