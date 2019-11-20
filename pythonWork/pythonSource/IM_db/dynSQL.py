
import sys
from  IM_DB  import parameters,dbConnect,dbParam,dbDML

def main(p_imdirec=None, p_modelname=None):

    parameters.initparam(p_imdirec)
    print ("dynsql",parameters.dbFilePath())
    dbConnect.openDB(parameters.dbFilePath());
#    dbParam.liesDefaultLang()

#, e1.enti_name , e2.enti_name
    l_sql ="""select * FROM DIAGRAMME join diagrammtypen on diat_id = diag_diat_id """
    l_sql ="""select * FROM melt_diat    join modellelem_typ on melt_id = medi_melt_id"""
    l_sql ="""select * FROM elementdarst"""
    l_sql ="""select * from diagrammtypen"""
    result = dbDML.select(l_sql)
    for row in result:
        print (row)
#    dbDML.exec("""delete from benudef_wert where bdwe_wert = '.'""")

#main
#.format(entiId,entiId)
#where von.enti_id = {} or zu.enti_id = {}

if __name__ == '__main__':
    import sys
    main(p_imdirec=sys.argv[1] if (len(sys.argv) > 1) else None
        ,p_modelname=sys.argv[2] if (len(sys.argv) > 2) else None)
