
import sys
from  IM_DB  import parameters,dbConnect,dbParam,dbDML

def main(p_imdirec=None, p_modelname=None):

    parameters.initparam(p_imdirec)
    print ("dynsql",parameters.dbFilePath())
    dbConnect.openDB(parameters.dbFilePath());

    dbParam.liesDefaultLang()

#, e1.enti_name , e2.enti_name
    l_sql ="""select  schl_id,schl_laufnr,schl_name
                  ,group_concat('<a href="#ATTR'||attr_id||'" target="details">'
                                    ||
                                    case when ana.sptx_text is null then attr_anzname else ana.sptx_text end 
                                    ||'</a>', ', ') attrs
                  ,group_concat('<a href="#BEZI'||bezi_id||'" target="details">'
                                    ||bezi_name||'</a>', ', ') bezis
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
           group by schl_id,schl_laufnr,schl_name
                    """.format('de',835)
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
