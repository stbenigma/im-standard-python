# -*- coding: latin-1 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../IM_db')
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/..')
from datetime import datetime
from IM_DB import parameters,dbConnect, dbParam,logmessages,parameters
from IM_HTML import printHTML, printRelHTML,printdiagHTML
from IM_OBJECTS import *
from IM_JSON import JSModel,sql2json


def formatDatentyp(w):
    dt = anzDatentyp(w[0])
    #print (w)
    return(
    "{}   ({}) {} {}" .format(dt, w[3], parameters.nvl(w[1])+ parameters.nvl2(w[1],'',' - ')
                    , parameters.nvl(w[2]), parameters.nvl(w[11]), parameters.nvl(w[6])) if w[0] == 'ZPKT'\
        else '{}  ({}:{})   {}  {}'\
                .format(dt, parameters.nvl(w[8]), parameters.nvl(w[9]), parameters.nvl(w[7]).__str__() + parameters.nvl2(w[7],'',' - ')
            , parameters.nvl(w[10]))     if w[0] == 'NUM'\
        else '{}  ({}) {}'\
            .format(dt, parameters.nvl(w[4]), 'CHECK: ' + parameters.nvl(w[5], ''))   if w[0] == 'TEXT'\
        else '{}  ({})'\
                 .format(dt, parameters.nvl(w[4])) if w[0] == 'LOV'\
        else dt
    )
#formatDatentyp

def bool2JN(b):
    return 'Ja' if (b == 'TRUE') else 'Nein'
#bool2JN


def printAttrUDPMatrix(thema=None):
    udpListe = [transl('Entität'),transl('Attribute'),transl('Technischer Name'),transl('Datentyp')]
    lsql = """select  bdeg_name,bdeg_thema,bdeg_gruppe
                    from benudef_eigenschaft
                    join modelltyp_eigensch on mote_bdeg_id = bdeg_id
                    join modellelem_typ on melt_id = mote_melt_id
                                    and melt_kurzname = 'ATTR'
                    where bdeg_thema like '{}'
                    order by bdeg_thema,bdeg_gruppe,bdeg_name
                        """ .format(parameters.nvl(thema,'%'))
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
                           .format(Languagetext.reportLang()))
    printHTML.starttable(ptitle='Attribute - User Defined Properties: ' + parameters.nvl(thema)
                         , pheaders= udpListe
                         , anker=udpAnker(thema))
    for at in allattr:
        values = [href(ref=entiAnker(at[1]), anz=at[0]), href(ref=attrAnker(at[2]), anz=at[3])
                              ,parameters.nvl(at[4]),parameters.nvl(at[6])]
        lsql = """select  bdwe_wert
                    from benudef_wert
                    join modellelement on mode_id = bdwe_mode_id
                                        and (mode_attr_id = {}) 
                    join benudef_eigenschaft on bdeg_id = bdwe_bdeg_id
                    where bdeg_thema like '{}'
                    order by bdeg_thema,bdeg_gruppe,bdeg_name
                    """.format(at[2],parameters.nvl(thema,'%'))
        udpWerte = dbDML.select(lsql)
        for udpWert in udpWerte:
            values.append(parameters.nvl(udpWert[0]))
        printHTML.writeTable(values)
    # endFor
    printHTML.endTable('')
#printAttrUDPMatrix


def printlistofcontent(plang):
    printHTML.printlistofcontenthead()
    try:
        idxlist = sorted([{'anker':key,'name': value['name'][plang]}
                     for key,value in printHTML.model.jsmodel['entities'].items()]
                     ,key=lambda val:val['name'])
    except:
        mod = printHTML.model.jsmodel['entities'].values()

    printHTML.printlistofcontentelement(pname='Entitäten'
                                            , plist= idxlist)

    idxlist = sorted([{'anker':key
                      ,'name': "{} ({})".format(value['name'][plang]
                                        ,printHTML.model.getbyid(value['entity'])['name'][plang]
                                                if value['entity'] is not None
                                        else printHTML.model.getbyid(value['relation'])['name'])
                       }
                     for key,value in printHTML.model.jsmodel['attributes'].items()]
                     ,key=lambda val:val['name'])
    printHTML.printlistofcontentelement(pname='Attribute', plist=idxlist)

#    origindomains = {key:value for key,value in printHTML.model.jsmodel['domains'].items() if value['origin'] == Domain.DOMAIN}
    idxlist=sorted([{'anker':key
                    ,'name': "{} ({})".format(value['name'][plang]
                                    ,str(len(value['usedinattrs+'])
                                         +len(value['usedincols+'])))}
                    for key,value in printHTML.origindomains().items()]
                ,key=lambda val:val['name'])
    printHTML.printlistofcontentelement(pname='Wertebereiche', plist=idxlist)

    idxlist=sorted([{'anker':key
                    ,'name': "{} ({})".format(value['name']
                                             ,str(value['referencecnt+']))
                     }
                    for key,value in printHTML.model.jsmodel['documents'].items()
                    ]
                ,key=lambda val:val['name'])
    printHTML.printlistofcontentelement(pname='Dokumente', plist=idxlist)

    idxlist=sorted([{'anker':key
                    ,'name': "{}".format(value['name']
                                             ,str(value['referencecnt+']))
                     }
                    for key,value in printHTML.model.jsmodel['orgunits'].items()
                    ]
                ,key=lambda val:val['name'])
    printHTML.printlistofcontentelement(pname='Org. Einheiten', plist=idxlist)

    # idxlist=sorted([{'anker':key
    #                 ,'name': "{} ({})".format(value['name']
    #                                          ,str(len(value['referencedfrom']))
    #                                         )
    #                  }
    #                 for key,value in printHTML.model.jsmodel['documents'].items()
    #                 ]
    #             ,key=lambda val:val['name'])
    # printHTML.printlistofcontentelement(pname='Attribut-Mapping', plist=idxlist)

    idxlist=sorted([{'anker':key
                    ,'name': "{}".format(value['name'])
                    }
                    for key,value in printHTML.model.jsmodel['diagrams'].items()
                    ]
                ,key=lambda val:val['name'])

    printHTML.printlistofcontentelement(pname='Diagramme', plist=idxlist)

    idxlist=sorted([{'anker':key
                    ,'name': "{}".format(value['name'])
                     }
                    for key,value in printHTML.model.jsmodel['systems'].items()
                    ]
                ,key=lambda val:val['name'])
    printHTML.printlistofcontentelement(pname='Systeme', plist=idxlist,pfileonly = True)
    printHTML.printlistofcontentfoot()
# printlistofcontent

def printcontent(pfirma,ptitel):
    printHTML.printcontenthead(pfirma=pfirma,ptitel=ptitel)
    printHTML.printcontententi()
    printHTML.printcontentattr()
    printHTML.printcontentdoma()
    printHTML.printcontentdoku()
    printHTML.printcontentorgu()
    #printHTML.printcontentmapping(ptheme=parameters.odmUDPMappingFileName())
    printdiagHTML.printcontentdiag(plist=printHTML.model.jsmodel['diagrams'], plang=Languagetext.reportLang(), ptitel=ptitel)
    printHTML.printcontentfoot()
#printcontent

def printhtmlfile(pfirma, ptitel, pinfo, plogofilename,pfilename):
    printHTML.createFile(pfilename=pfilename)
    printHTML.printhead(p_firma=pfirma
                        ,piconfilename="image/imicon.png"
                        , p_titel=ptitel
                        , p_info=pinfo
                        , p_logofilename=plogofilename);
    printlistofcontent(plang=Languagetext.reportLang());
    printcontent(pfirma=pfirma, ptitel=ptitel);
    printHTML.printfoot();
    printHTML.closefile ();
#printhtmlfile

def printhtmlsysfile(pfirma, pfilename, ptitel, pinfo, plogofilename,pelement):
    printHTML.createFile (pfilename=pfilename)
    printHTML.printhead(p_firma=pfirma
                        ,piconfilename="image/imicon.png"
                        , p_titel=ptitel
                        , p_info=pinfo
                        , p_logofilename=plogofilename)
    printRelHTML.printlistofcontent(pintf=pelement)
    printRelHTML.printcontent(pfirma=pfirma, ptitel=ptitel,pintf=pelement)
    printHTML.printfoot();
    printHTML.closefile ();
#printhtmlsysfile

def listwebmain(pmodel:JSModel,plang):
    dbParam.liesdefaultlang()
    printHTML.createlib()
    printHTML.copyimages()
    if (plang is None):
        langs = project.projektlangs().split(',')
        if (len(langs) == 0):
            Languagetext.reportLang(parameters.dbDefaultLang())
            langs = [Languagetext.reportLang()]
    else:
        Languagetext.reportLang(plang.lower())
        langs = [Languagetext.reportLang()]
    #fi

    #erstelle die Liste der HTML Files für HREF's
    schnlist = pmodel.jsmodel['systems']
    for key,value in schnlist.items():
        printHTML.htmlfilelist[key] = value['name']+ '.html'
    printHTML.model = pmodel

    for lang in langs:
        lang = lang.lower()
        Languagetext.reportLang(lang)
        langfilename = printHTML.webFileName + '_' + Languagetext.reportLang() + '.html'
        print ("create web-files for language {} in file {}".format(lang,printHTML.webDirectory + langfilename))
        printHTML.htmlfilelist[0] = langfilename
        printhtmlfile(pfirma="foryouandyourcustomers"
                      , ptitel=parameters.odmModelName() + ' ({})'.format(lang)
                      , pinfo="{}".format(datetime.now().strftime("%Y-%m-%d, %H:%M"))
                      , plogofilename=parameters.logoFileName()
                      , pfilename=  langfilename
                      )
    # for
    Languagetext.reportLang(parameters.dbDefaultLang())
    #backjumps from relational webpage goes to default-lang-model
    printHTML.htmlfilelist[0] = printHTML.webFileName + '_' + parameters.dbDefaultLang() + '.html'

    """Schnittstellen werden immer englisch gedruckt"""
    Languagetext.reportLang(Languagetext.EN)
    lang = Languagetext.EN
    for anker,element in schnlist.items():
        print ("create web-files for system {} in file {}".format(element['name'],printHTML.webDirectory + langfilename))
        printhtmlsysfile(pfirma="foryouandyourcustomers"
                      ,pfilename= printHTML.htmlfilelist[anker]
                      , ptitel= parameters.odmModelName() + ' - {}'.format(element['name'])
                      , pinfo="{}".format(datetime.now().strftime("%Y-%m-%d, %H:%M"))
                      , plogofilename=parameters.logoFileName()
                      ,pelement=element
                      )
    #
#listwebmain

def main(pdirec, plang):
    parameters.initparam(p_callarg=pdirec)
    logmessages.initlog('createHTML')

    printHTML.setWebDirec(p_webdirec=None)

    dbConnect.openDB(p_filepath= parameters.dbFilePath());
    deflang = Language.liesdeflangiso2()
    if deflang is not None : parameters.dbDefaultLang(deflang)
    listwebmain(pmodel=JSModel(sql2json(pmodelname=parameters.odmModelName(),pdbname=parameters.dbFilePath())), plang=plang)

    dbConnect.myDbConn.close()

    logmessages.showmessages("web-files from database {} for model {} created"
                             .format(parameters.dbFilePath(),parameters.odmModelName()))
#main

if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv)>2) else None
    main(pdirec=direc, plang=lang)