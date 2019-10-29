# -*- coding: latin-1 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../IM_db')
from datetime import date,datetime
from IM_DB import parameters,dbConnect,dbDDL,dbDML,dbErstelleTables,dbInserts,dbLookup,dbParam
from IM_HTML import printHTML,web_sql



# Main Programm
def nvl(x,default=''):
    if x is None: return default
    else: return x
#nvl

def makeAnker(ref,anz):
    return """<a name = "{}" >{}</a>""".format(ref,anz)
#href

def formatDatentyp(w):
    dt = anzDatentyp(w[0])
    #print (w)
    return(
    "{}   ({}) {} {}" .format(dt, w[3], nvl(w[1])\
        + ' - ' if w[1] is not None else ''
            , nvl(w[2]), nvl(w[11]), nvl(w[6])) if w[0] == 'ZPKT'\
        else '{}  ({}:{})   {}  {}'\
                .format(dt, nvl(w[8]), nvl(w[9]), nvl(w[7]).__str__() \
            + ' - ' if w[7] is not None else ''
            , nvl(w[10]))     if w[0] == 'NUM'\
        else '{}  ({}) {}'\
            .format(dt, nvl(w[4]), 'CHECK: ' + w[5] if (not (w[5] is None))
                                            else '')   if w[0] == 'TEXT'\
        else '{}  ({})'\
                 .format(dt, nvl(w[4])) if w[0] == 'LOV'\
        else dt
    )
#formatDatentyp

def bool2JN(b):
    return 'Ja' if (b == 'TRUE') else 'Nein'
#bool2JN


def printAttrUDPMatrix(thema=None):
    udpListe = [transl('Entität'),transl('Attribut'),transl('Technischer Name'),transl('Datentyp')]
    lsql = """select  bdeg_name,bdeg_thema,bdeg_gruppe
                    from benudef_eigenschaft
                    join modelltyp_eigensch on mote_bdeg_id = bdeg_id
                    join modellelem_typ on melt_id = mote_melt_id
                                    and melt_kurzname = 'ATTR'
                    where bdeg_thema like '{}'
                    order by bdeg_thema,bdeg_gruppe,bdeg_name
                        """ .format(nvl(thema,'%'))
    udpWerte = dbDML.select(lsql)
    for udpWert in udpWerte:
        udpListe.append(udpWert[0])
    #print ('udpListe=',udpListe)
    allattr = dbDML.select("""select * from 
        (select 
       case when ena.sptx_text is null then enti_name else ena.sptx_text end enti_name
       ,enti_id,attr_id,case when ana.sptx_text is null then attr_anzname else ana.sptx_text end attr_anzname
       ,attr_tech_name,wrtb_name,wrtb_typ
      from attributes 
        join sprachen sp on sp.spra_iso_code2 = '{}'
        join modellelement ma on ma.mode_attr_id = attr_id
        left join spraattr  ana on ana.sptx_attrname = 'ATTR_NAME'
                                    and ana.sptx_mode_id = ma.mode_id
                                    and ana.spra_id = sp.spra_id            
      join entitaeten on enti_id = attr_enti_id
        join modellelement me on me.mode_enti_id = enti_id
        left join spraattr  ena on ena.sptx_attrname = 'ENTI_NAME'
                                    and ena.sptx_mode_id = me.mode_id
                                    and ena.spra_id = sp.spra_id            
      join wertebereiche on wrtb_id = attr_wrtb_id
      ) order by enti_name,upper(attr_tech_name)"""
                           .format(printHTML.greportLang))
    printHTML.starttable('Attribute - User Defined Properties: ' + nvl(thema), udpListe, anker=udpAnker(thema))
    for at in allattr:
        values = [href(ref=entiAnker(at[1]), anz=at[0]), href(ref=attrAnker(at[2]), anz=at[3])
                              ,nvl(at[4]),nvl(at[6])]
        lsql = """select  bdwe_wert
                    from benudef_wert
                    join modellelement on mode_id = bdwe_mode_id
                                        and (mode_attr_id = {}) 
                    join benudef_eigenschaft on bdeg_id = bdwe_bdeg_id
                    where bdeg_thema like '{}'
                    order by bdeg_thema,bdeg_gruppe,bdeg_name
                    """.format(at[2],nvl(thema,'%'))
        udpWerte = dbDML.select(lsql)
        for udpWert in udpWerte:
            values.append(nvl(udpWert[0]))
        printHTML.writeTable(values)
    # endFor
    printHTML.endTable('')

#printAttrUDPMatrix


def printlistofcontent():
    printHTML.printlistofcontenthead()
    printHTML.printlistofcontentelement(p_name='Entitäten', p_list=web_sql.namelist(p_type='ENTI',p_lang=printHTML.reportLang()))
    printHTML.printlistofcontentelement(p_name='Attribute', p_list=web_sql.namelist(p_type='ATTR',p_lang=printHTML.reportLang()))
    printHTML.printlistofcontentelement(p_name='Domänen', p_list=web_sql.namelist(p_type='WRTB',p_lang=printHTML.reportLang()))
    printHTML.printlistofcontentfoot()
# printlistofcontent

def printcontent():
    printHTML.printcontenthead()
    printHTML.printcontententi(p_list=web_sql.datalist(p_type='ENTI',p_lang=printHTML.reportLang()))
#    printHTML.printcontentattr(p_list=web_sql.attrdatalist(p_lang=printHTML.reportLang()))
    #printHTML.printcontentwrtb(p_list=datalist('WRTB'))
    printHTML.printcontentfoot()
    return



    printHTML.writeToc("""<div><ol class ="tree"><li><label for="attributes">Attribute</label>
                <input type="checkbox" id="attributes" /><ol>
    """)
    for a in attr:
        printHTML.writeToc("""<li class="obj"><a href="{}#{}" \
                target="details">{}</a></li>
                """.format(printHTML.contFileName + ".html", attrAnker(a[12]), a[3]))
    #endfor
    printHTML.writeToc("</ol></ol></div>")
    wrtb = dbDML.select("""select * from wertebereiche order by upper(wrtb_name)""")
    printHTML.writeToc("""<div><ol class ="tree"><li><label for="objects">Domains</label>
            <input type="checkbox" id="objects" /><ol>
            """)
    for w in wrtb:
        printHTML.writeToc("""<li class="obj"><a href="{}#{}" target="details">{}</a></li>\
           """ .format(printHTML.contFileName + ".html", wrtbAnker(w[0]), w[2]))
    #endfor
    printHTML.writeToc("</ol></ol></div>")

    printHTML.writeToc("""<div><ol class ="tree"><li><label for="matrix">UDP-Matrix</label>
            <input type="checkbox" id="matrix" /><ol>
            """)
    udpAttrThema = dbDML.select(udpThemenSql)
    for u in udpAttrThema:
        printHTML.writeToc("""<li class="obj"><a href="{}#{}" target="details">{}</a></li>\
           """.format(printHTML.contFileName + ".html", udpAnker(u[0]), u[0]))
    printHTML.writeToc("</ol></ol></div>")

    printHTML.closeToc("""</div></div>""")
#printcontent

def printhtmlfile(p_firma,p_titel,p_info,p_logofilename):

    printHTML.createFile ();
    printHTML.printhead(p_firma=p_firma
                        ,p_titel=p_titel
                        ,  p_info=p_info
                        ,p_logofilename=p_logofilename);
    printlistofcontent();
    printcontent();
    printHTML.printfoot();
    return

    for e in enti:
        printHTML.printTable({transl('Entität'): e[0], "Beschreibung":nvl(e[2])
                              ,"Synonyme":nvl(e[10])
        , "Autor":e[3], "Erstellt":e[4], "Superentität":href(entiAnker(e[7]), anz=nvl(e[6]))
                , "Subentitäten":nvl(e[9])}, anker=entiAnker(e[5]))

        eattr = dbDML.select("""select 
           attr_odm_guid,attr_tech_name
           ,case when ana.sptx_text is null then attr_anzname else ana.sptx_text end attr_anzname
           ,wrtb_odm_guid,wrtb_name,attr_pflichtattr
           ,attr_historisiert,attr_wiederholt,attr_sprachabhaengig
           ,attr_verschluesselt,wrtb_typ,attr_deskriptor
           ,attr_id,wrtb_id             
           ,(select group_concat('<a href="#SCHL'||schl_id||'" target="details">'
                                    ||schl_laufnr||'</a>',',')
               from schluesselelement 
                join schluessel on schl_id = scel_schl_id
                where scel_attr_id = attr_id
            ) as schluessel
          from attributes 
                 join modellelement on mode_attr_id = attr_id
                 join sprachen sp on sp.spra_iso_code2 = '{}'
                 left join spraattr  ana on ana.sptx_attrname = 'ATTR_NAME'
                                    and ana.sptx_mode_id = mode_id
                                    and ana.spra_id = sp.spra_id            
                join wertebereiche on wrtb_id = attr_wrtb_id
          where attr_enti_id = {}
          order by upper(attr_tech_name)""" .format(printHTML.greportLang,e[5]))
        entiId = e[5]
        printUDP(meltName='ENTI', Id=entiId)
        printBezi(entiId=entiId)
        printSchluessel(entiId=entiId)
    #endfor


    for a in attr:
            #        select
            #        attr_tech_name || ' ('||enti_name||')' as vollname,attr_odm_guid,attr_tech_name
            #        ,attr_anzname,enti_odm_guid,attr_uc
            #           ,attr_dc,attr_beschr,enti_name
            #           ,wrtb_id,wrtb_name,wrtb_typ
            #           ,attr_id,enti_id,schluessel
        printHTML.printTable({"Attribut": a[3], transl('Entität'): href(ref=entiAnker(a[13]), anz=a[8])
                                     , "Wertebereich": href(ref=wrtbAnker(a[9]), anz=a[10])
                                     , "Datentyp": anzDatentyp(a[11])
                                     , "Beschreibung": nvl(a[7])
                                     , "in Schlüssel": nvl(a[14])
                                     , "Autor": a[5], "Erstellt": a[6]}, anker=attrAnker(a[12]))

        # print (a)
        attrId = a[12]
        printUDP(meltName='ATTR', Id=attrId)
    # rof

    for w in wrtb:
        #print (w)
        printHTML.printTable({"Wertebereich": w[2], "Beschreibung":nvl(w[3])\
                                    ,"Datentyp":formatDatentyp((w[4],w[5],w[6],w[7],w[8],w[9],w[10],w[11],w[12],w[13],w[6],w[10]))
        , "Autor":w[18], "Erstellt":w[19]} \
                             , anker=wrtbAnker(w[0]))
        #print (w)
        doms = dbDML.select("select * from vorgabewerte where vgwt_wrtb_id ={} order by vgwt_sortrhfg" .format(w[0]))
        if doms != []:
            printHTML.starttable('Werteliste', ('Sort', 'Wert', 'Anzeige', 'Beschreibung'))
            #print ("Vorgabewerte",doms)
            for d in doms:
                #print (d)
                printHTML.writeTable((d[2], d[1], d[4], d[5]))
            #endfor
            printHTML.endTable('')
        #endif
        printHTML.starttable('Verwendet von', ('Typ', 'Entität/Tabelle', 'Name'))
        attcols = dbDML.select("""select 'Attribut' as attr ,enti_name,attr_tech_name
                        , attr_id,enti_id
                        from attributes 
                     join sprachen sp on sp.spra_iso_code2 = '{}'         
                      join (select case when ena.sptx_text is null then enti_name else ena.sptx_text end enti_name
                                ,enti_id,spra_id ,enti_odm_guid
                        from entitaeten 
                        join modellelement on mode_enti_id = enti_id
                       left join spraattr ena on ena.sptx_attrname = 'ENT_NAME'
                                and ena.sptx_mode_id = mode_id 
                ) ent on enti_id = attr_enti_id
                     and ent.spra_id = sp.spra_id
                        where attr_wrtb_id = {}""" .format(printHTML.greportLang,w[0]))
        for c in attcols:
            printHTML.writeTable((c[0], href(ref=entiAnker(c[4]), anz=c[1]), href(ref=attrAnker(c[3]), anz=c[2])))
        printHTML.endTable('')
    #endfor

    for u in udpAttrThema:
        printAttrUDPMatrix(thema=u[0])
    # printAttrUDPMatrix()


#printhtmlfile

def main(p_direc,p_lang,p_webdirec):
    parameters.initparam(p_callarg=p_direc)
    printHTML.setWebDirec(p_webdirec=p_webdirec)

    dbConnect.openDB(p_filepath= parameters.dbFilePath());
    dbParam.liesDefaultLang()
    if (p_lang is None):
        printHTML.reportLang(dbParam.dbDefaultLang)
    else:
        printHTML.reportLang(p_lang.lower())


    printhtmlfile(    p_firma="foryouandyourcustomers"
                        ,p_titel="Testwebreport"
                        ,p_info="stb, {}".format(datetime.now().strftime("%Y-%m-%d, %H:%M"))
                        ,p_logofilename=parameters.logoFileName());

    dbConnect.myDbConn.close()
#main

if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv)>2) else None
    webdirec = sys.argv[3] if (len(sys.argv)>3) else None
    main(p_direc=direc,p_lang=lang,p_webdirec=webdirec)