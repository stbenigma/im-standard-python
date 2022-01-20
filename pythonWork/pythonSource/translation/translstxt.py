# -*- coding: latin-1 -*-
from IM_ODM import odmParam
from SSOT_db.SQL_INFRA import  dbConnect
from SSOT_db.SQL_INFRA import dbDML
from SSOT_infra import parameters
from mydeepl import translate
from datetime import date

# Main Programm

def translateNewText():
    l_sql ="""select sptx_text,sptx_mode_id,sptx_spra_id,sptx_attrname
        from sprachtexte
        join sprachen
        where spra_ist_modellsprache = 'FALSE'
        and  sptx_text like '*'||'{}'||'*%' 
        """.format(str.upper(parameters.dbDefaultLang()))
    result = dbDML.select(l_sql)
    for row in result:
        print (row)
    return
    rows = dbDML.select(l_sql)
    rowslist = [list(l) for l in rows ]
    for i,row in enumerate(rowslist,start=1):
        if i> 10: break
        #print (row,row[0][5:])
        newval = '**'+translate.translate(p_text=row[0][5:], p_fromlang=parameters.dbDefaultlang(), p_tolang=)
        #print (row[0][5:],newval,row[1])
        row[0] = newval
    print (rowslist)
    l_sql = """select count(*) from sprachtexte where sptx_text like '*'||'{}'||'*%'""".format(str.upper(
        parameters.dbDefaultlang()))
    result = dbDML.select(l_sql)
    print (result)

    l_sql = """update sprachtexte
                set sptx_um = '{}'  
                , sptx_dm = '{}'
                , sptx_text = ?
             where sptx_mode_id = ?
               and sptx_spra_id = ?
               and sptx_attrname = ?
               """ . format('--',date.today().__str__())
    dbDML.execmany(l_sql, rowslist)
    l_sql = """select count(*) from sprachtexte where sptx_text like '*'||'{}'||'*%'""".format(str.upper(
        parameters.dbDefaultlang()))
    result = dbDML.select(l_sql)
    print (result)
#translateNewText

def main(p_imdirec=None, p_modelname=None):
    odmParam.initODMParam(pimDirec=p_imdirec, pmodelName=p_modelname)

    print ("translate language texts", odmParam.imDirectory, odmParam.imModelName)
    dbConnect.openDB(parameters.dbDirect(), odmParam.imModelName + '.db');

    translateNewText()

    dbConnect.myDbConn.close()
#end main

if __name__ == '__main__':
    import sys
    main(p_imdirec=sys.argv[1] if (len(sys.argv) > 1) else None
        ,p_modelname=sys.argv[2] if (len(sys.argv) > 2) else None)
