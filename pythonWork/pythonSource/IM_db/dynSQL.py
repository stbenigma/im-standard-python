
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
    l_sql ="""select diag_id,diag_name,diag_legendx,diag_legendy,breite,hoehe
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
            where diag_id = diag_id"""
    l_sql = """select * from elementdarst"""
    l_sql = """select 
                eled_position_x xpos,eled_breite breite
                ,eled_position_y ypos, eled_hoehe hoehe
                ,eled_deckkraft,eled_farbe
                ,eled_randbreite,eled_randdeckkraft,eled_randfarbe
                ,eled_schriftgroesse, eled_schriftfarbe
                ,case when ena.sptx_text is null then enti_name 
                                                else ena.sptx_text end  entiname
                ,enti_id 
                from elementdarst
                join modellelement on mode_id = eled_mode_id
                join entitaeten on enti_id = mode_enti_id
                join sprachen sp on sp.spra_iso_code2 = '{}'         
                left join spraattr ena on ena.sptx_attrname = 'ENT_NAME'
                                        and ena.sptx_mode_id = mode_id
                                        and ena.spra_id = sp.spra_id
                where eled_diag_id = {}
    """.format('de',5)
    """            where eled_diag_id = {}"""
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
