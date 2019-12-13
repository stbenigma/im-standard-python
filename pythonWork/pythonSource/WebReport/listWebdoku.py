# -*- coding: latin-1 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../IM_db')
from datetime import date,datetime
from IM_DB import parameters,dbConnect,dbDDL,dbDML,dbErstelleTables,dbInserts,dbLookup,dbParam
from IM_HTML import printHTML,web_sql,printdiagHTML

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
    printHTML.printlistofcontentelement(pname='Entitäten', plist=web_sql.namelist(ptype='ENTI', plang=printHTML.reportLang()))
    printHTML.printlistofcontentelement(pname='Attribute', plist=web_sql.namelist(ptype='ATTR', plang=printHTML.reportLang()))
    printHTML.printlistofcontentelement(pname='Domänen', plist=web_sql.namelist(ptype='WRTB', plang=printHTML.reportLang()))
    printHTML.printlistofcontentelement(pname='Attribut-Mapping', plist=web_sql.namelist(ptype='UDP', plang=printHTML.reportLang()))
    printHTML.printlistofcontentelement(pname='Diagramme', plist=web_sql.namelist(ptype='DIAG', plang=printHTML.reportLang()))
    printHTML.printlistofcontentfoot()
# printlistofcontent

def printcontent(pfirma,ptitel):
    printHTML.printcontenthead(pfirma=pfirma,ptitel=ptitel)
    printHTML.printcontententi(p_list=web_sql.entilist(p_lang=printHTML.reportLang()))
    printHTML.printcontentattr(plist=web_sql.attrlist(p_lang=printHTML.reportLang()))
    printHTML.printcontentwrtb(p_list=web_sql.wrtblist(p_lang=printHTML.reportLang()))
    printHTML.printcontentudp(plist=web_sql.namelist(ptype='UDP', plang=printHTML.reportLang()))
    printdiagHTML.printcontentdiag(plist=web_sql.diaglist(),plang=printHTML.reportLang())
#    printHTML.printattrmaps(p_list=web_sql.wrtblist(p_lang=printHTML.reportLang()))
#    printHTML.printdiagrams(p_list=web_sql.wrtblist(p_lang=printHTML.reportLang()))
    printHTML.printcontentfoot()
#printcontent

def printhtmlfile(p_firma,p_titel,p_info,p_logofilename):
    printHTML.createFile ();
    printHTML.printhead(p_firma=p_firma
                        ,p_titel=p_titel
                        ,  p_info=p_info
                        ,p_logofilename=p_logofilename);
    printlistofcontent();
    printcontent(pfirma=p_firma,ptitel=p_titel);
    printHTML.printfoot();
    printHTML.closefile ();


#printhtmlfile

def listwebmain(plang):
    dbParam.liesDefaultLang()
    printHTML.createlib()
    if (plang is None):
        langs = web_sql.projektlangs().split(',')
        if (len(langs) == 0):
            langs = [printHTML.reportLang()]
    else:
        printHTML.reportLang(plang.lower())
        langs = [printHTML.reportLang()]
    #fi

    for lang in langs:
        printHTML.reportLang(lang.lower())
        print ("create web-files for language {}".format(printHTML.reportLang()))
        printhtmlfile(p_firma="foryouandyourcustomers"
                          , p_titel=parameters.odmModelName()+' ({})'.format(printHTML.reportLang())
                          , p_info="{}".format(datetime.now().strftime("%Y-%m-%d, %H:%M"))
                          , p_logofilename=parameters.logoFileName()
                          )
    # for
#listwebmain

def main(pdirec, plang):
    parameters.initparam(p_callarg=pdirec)
    printHTML.setWebDirec(p_webdirec=None)

    dbConnect.openDB(p_filepath= parameters.dbFilePath());
    listwebmain(plang=plang)

    dbConnect.myDbConn.close()
#main

if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv)>2) else None
    main(pdirec=direc, plang=lang)