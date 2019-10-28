
import sys
from  IM_DB  import parameters,dbConnect,dbParam,dbDML

def main(p_imdirec=None, p_modelname=None):

    parameters.initparam(p_imdirec)
    print ("dynsql",parameters.dbFilePath())
    dbConnect.openDB(parameters.dbFilePath());

    dbParam.liesDefaultLang()

#, e1.enti_name , e2.enti_name
    l_sql ="""select attr_id,attr_anzname,attr_pflichtattr from attributes where attr_pflichtattr = 'FALSE'
                  """
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
