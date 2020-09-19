# -*- coding: latin-1 -*-
import sys,os
#sys.path.append(os.getcwd())
#sys.path.append(os.getcwd()+'/../IM_db')
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../IM_db')
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/..')
from datetime import date,datetime
from IM_DB import parameters,dbConnect,dbLookup,dbParam,logging
from IM_HTML import printHTML,web_sql,printdiagHTML,printRelHTML
from IM_OBJECTS import *


# Main Programm
def nvl(x,default=''):
    if x is None: return default
    else: return x
#nvl

#def makeAnker(ref,anz):
#    return """<a name = "{}" >{}</a>""".format(ref,anz)
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
       ,enti_id,attr_id,case when ana.sptx_text is null then attr_displ_name else ana.sptx_text end attr_displ_name
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
      join wertebereiche on wrtb_id = attr_doma_id
      ) order by enti_name,upper(attr_tech_name)"""
                           .format(Sprachtext.reportLang()))
    printHTML.starttable(ptitel='Attribute - User Defined Properties: ' + nvl(thema)
                         ,pueberschriften= udpListe
                         , anker=udpAnker(thema))
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
    printHTML.printlistofcontentelement(pname='Entitäten', plist=web_sql.namelist(ptype='ENTI', plang=Sprachtext.reportLang()))
    printHTML.printlistofcontentelement(pname='Attribute', plist=web_sql.namelist(ptype='ATTR', plang=Sprachtext.reportLang()))
    printHTML.printlistofcontentelement(pname='Wertebereiche', plist=web_sql.namelist(ptype='DOMA', plang=Sprachtext.reportLang()))
    printHTML.printlistofcontentelement(pname='Dokumente', plist=web_sql.namelist(ptype='DOKU', plang=Sprachtext.reportLang()))
    printHTML.printlistofcontentelement(pname='Attribut-Mapping', plist=web_sql.namelist(ptype='UDP', plang=Sprachtext.reportLang()))
    printHTML.printlistofcontentelement(pname='Diagramme', plist=web_sql.namelist(ptype='DIAG', plang=Sprachtext.reportLang()))
    printHTML.printlistofcontentelement(pname='Systeme', plist=web_sql.namelist(ptype='INTF', plang=Sprachtext.reportLang())
                                        ,pfileonly = True)
    printHTML.printlistofcontentfoot()
# printlistofcontent

def printcontent(pfirma,ptitel):
    printHTML.printcontenthead(pfirma=pfirma,ptitel=ptitel)
    printHTML.printcontententi()
    printHTML.printcontentattr()
    printHTML.printcontentwrtb(plist=web_sql.wrtblist())
    printHTML.printcontentdoku(plist=web_sql.dokulist())
    printHTML.printcontentmapping(plist=web_sql.namelist(ptype='UDP', plang=Sprachtext.reportLang()))
    printdiagHTML.printcontentdiag(plist=web_sql.diaglist(), plang=Sprachtext.reportLang(), ptitel=ptitel)
    printHTML.printcontentfoot()
#printcontent

def printhtmlfile(pfirma, ptitel, pinfo, plogofilename,pfilename):
    printHTML.createFile(pfilename=pfilename)
    printHTML.printhead(p_firma=pfirma
                        , p_titel=ptitel
                        , p_info=pinfo
                        , p_logofilename=plogofilename);
    printlistofcontent();
    printcontent(pfirma=pfirma, ptitel=ptitel);
    printHTML.printfoot();
    printHTML.closefile ();


#printhtmlfile

def printhtmlsysfile(pfirma, pfilename, ptitel, pinfo, plogofilename,pschnid):
    printHTML.createFile (pfilename=pfilename)
    printHTML.printhead(p_firma=pfirma
                        , p_titel=ptitel
                        , p_info=pinfo
                        , p_logofilename=plogofilename)
    printRelHTML.printlistofcontent(pschnid)
    printRelHTML.printcontent(pfirma=pfirma, ptitel=ptitel,pschnid=pschnid)
    printHTML.printfoot();
    printHTML.closefile ();
#printhtmlsysfile

def listwebmain(plang):
    dbParam.liesdefaultlang()
    printHTML.createlib()
    if (plang is None):
        langs = projekt.projektlangs().split(',')
        if (len(langs) == 0):
            Sprachtext.reportLang(parameters.dbDefaultLang())
            langs = [Sprachtext.reportLang()]
    else:
        Sprachtext.reportLang(plang.lower())
        langs = [Sprachtext.reportLang()]
    #fi

    #erstelle die Liste der HTML Files für HREF's
    schnlist = Schnittstelle.indexlist()
    for s in schnlist: printHTML.htmlfilelist[s[2]] = s[0]+ '.html'

    for lang in langs:
        Sprachtext.reportLang(lang.lower())
        langfilename = printHTML.webFileName + '_' + Sprachtext.reportLang() + '.html'
        print ("create web-files for language {} in file {}".format(Sprachtext.reportLang(),langfilename))
        printHTML.htmlfilelist[0] = langfilename
        printhtmlfile(pfirma="foryouandyourcustomers"
                      , ptitel=parameters.odmModelName() + ' ({})'.format(Sprachtext.reportLang())
                      , pinfo="{}".format(datetime.now().strftime("%Y-%m-%d, %H:%M"))
                      , plogofilename=parameters.logoFileName()
                      , pfilename=  langfilename
                      )
    # for
    Sprachtext.reportLang(parameters.dbDefaultLang())
    #backjumps from relational webpage goes to default-lang-model
    printHTML.htmlfilelist[0] = printHTML.webFileName + '_' + parameters.dbDefaultLang() + '.html'


    """Schnittstellen werden immer englisch gedruckt"""
    Sprachtext.reportLang(Sprachtext.EN)
    for s in schnlist:
        schn_name = s[0]
        schn_id = s[2]
        print ("create web-files for system {}".format(schn_name))
        printhtmlsysfile(pfirma="foryouandyourcustomers"
                      ,pfilename= printHTML.htmlfilelist[schn_id]
                      , ptitel= parameters.odmModelName() + ' - {}'.format(schn_name)
                      , pinfo="{}".format(datetime.now().strftime("%Y-%m-%d, %H:%M"))
                      , plogofilename=parameters.logoFileName()
                      ,pschnid=schn_id
                      )
    #

#listwebmain

def main(pdirec, plang):
    parameters.initparam(p_callarg=pdirec)
    logging.initlog('createHTML')

    printHTML.setWebDirec(p_webdirec=None)

    dbConnect.openDB(p_filepath= parameters.dbFilePath());
    deflang = Sprache.liesdeflangiso2()
    if deflang is not None : parameters.dbDefaultLang(deflang)
    listwebmain(plang=plang)

    dbConnect.myDbConn.close()

    logging.showmessages("web-files from database {} for model {} created"
                         .format(parameters.dbFilePath(),parameters.odmModelName()))
#main

if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv)>2) else None
    main(pdirec=direc, plang=lang)