# -*- coding: latin-1 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../IM_db')
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/..')
from IM_DB import dbConnect, logmessages,parameters
from IM_HTML import printHTML, printRelHTML,printdiagHTML
from IM_OBJECTS import *
from IM_JSON import JSModel,sql2json
from IM_WEB import jinjawebmodel


def formatDatentyp(w):
    dt = anzDatentyp(w[0])
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
                     for key,value in printHTML.getmodel().getelements(pelemtype='entities').items()]
                     ,key=lambda val:val['name'])
    except:
        idxlist=[]
        mod = printHTML.getmodel().jsmodel['entities'].values()

    printHTML.printlistofcontentelement(pname='Entitäten'
                                            , plist= idxlist)

    idxlist = sorted([{'anker':key
                  ,'name': "{} ({})".format(value['name'][plang]
                                    ,printHTML.getmodel().getbyid(value['entity'])['name'][plang]
                                            if value['entity'] is not None
                                    else printHTML.getmodel().getbyid(value['relation'])['name'])
                   }
                 for key,value in printHTML.getmodel().getelements(pelemtype='attributes').items()]
                 ,key=lambda val:val['name'])
    printHTML.printlistofcontentelement(pname='Attribute', plist=idxlist)

#    origindomains = {key:value for key,value in printHTML.getmodel().jsmodel['domains'].items() if value['origin'] == Domain.DOMAIN}
    idxlist=sorted([{'anker':key
                    ,'name': "{} ({})".format(value['name'][plang]
                                    ,str(len(value['usedinattrs+'])
                                         +len(value['usedincols+'])))}
                    for key,value in printHTML.origindomains(pintfid=None).items()]
                ,key=lambda val:val['name'])
    printHTML.printlistofcontentelement(pname='Wertebereiche', plist=idxlist)

    idxlist=sorted([{'anker':key
                    ,'name': "{} ({})".format(value['name']
                                             ,str(value['referencecnt+']))
                     }
                    for key,value in printHTML.getmodel().jsmodel['documents'].items()
                    ]
                ,key=lambda val:val['name'])
    printHTML.printlistofcontentelement(pname='Dokumente', plist=idxlist)

    idxlist=sorted([{'anker':key
                    ,'name': "{}".format(value['name']
                                             ,str(value['referencecnt+']))
                     }
                    for key,value in printHTML.getmodel().jsmodel['orgunits'].items()
                    ]
                ,key=lambda val:val['name'])
    printHTML.printlistofcontentelement(pname='Org. Einheiten', plist=idxlist)

    # idxlist=sorted([{'anker':key
    #                 ,'name': "{} ({})".format(value['name']
    #                                          ,str(len(value['referencedfrom']))
    #                                         )
    #                  }
    #                 for key,value in printHTML.getmodel().jsmodel['documents'].items()
    #                 ]
    #             ,key=lambda val:val['name'])
    # printHTML.printlistofcontentelement(pname='Attribut-Mapping', plist=idxlist)

    idxlist=sorted([{'anker':key
                    ,'name': "{}".format(value['name'])
                    }
                    for key,value in printHTML.getmodel().jsmodel['diagrams'].items()
                    ]
                ,key=lambda val:val['name'])

    printHTML.printlistofcontentelement(pname='Diagramme', plist=idxlist)

    idxlist=sorted([{'anker':key
                    ,'name': "{}".format(value['name'])
                     }
                    for key,value in printHTML.getmodel().jsmodel['systems'].items()
                    ]
                ,key=lambda val:val['name'])
    printHTML.printlistofcontentelement(pname='Systeme', plist=idxlist,pfileonly = True)
    printHTML.printlistofcontentfoot()
# printlistofcontent

def printcontent(pfirma,ptitel):
    printHTML.printcontenthead(pfirma=pfirma,ptitel=ptitel)
    printHTML.printcontententi()
    printHTML.printcontentattr()
    printHTML.printcontentdoma(pdomains=printHTML.origindomains(pintfid=None))
    printHTML.printcontentdoku()
    printHTML.printcontentorgu()
    #printHTML.printcontentmapping(ptheme=parameters.odmUDPMappingFileName())
    printdiagHTML.printcontentdiag(plist=printHTML.getmodel().jsmodel['diagrams'], plang=Languagetext.reportLang(), ptitel=ptitel)
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

def printhtmlrender(pfilename, planguage, pmodel, pintfid=None):
    printHTML.createFile (pfilename=pfilename)

    if pintfid is None:
        diags =sorted([{"id":key
                 ,"name": value["name"]
                ,"svg": printdiagHTML.getsvgtext(pdiagelem=value,pdiaganker=key,plang=planguage)
                        } for key, value in pmodel.jsmodel["diagrams"].items()
                                                    if (value["type"] == "Entity")]
                , key=lambda x: x["name"].upper())
    else:
        diags = [{"id": pintfid
                , "name": pmodel.getbyid(pintfid)["name"]
                , "svg": printRelHTML.interfacediagram(pintf=pmodel.getbyid(pintfid))}
                 ]
    #fi
    html = jinjawebmodel.rendermodel(pcurlang=planguage,pmodel=pmodel,pintfid=pintfid,pdiagrams=diags,phtmlfilelist=printHTML.htmlfilelist)
    printHTML.fhtml.write(html)
    printHTML.closefile ();
#printhtmlrenderfile

def listwebmain(plang,pfilter=(None,'TEST','REL')):
    printHTML.createlib()
    printHTML.copyimages()
    printHTML.getmodel().setstatusfilter(pfilter)
    defaultlang = printHTML.getmodel().jsmodel["model"]["language"]
    langs = printHTML.getmodel().jsmodel["languages"].keys()
    if (plang is None or (plang.lower() == 'all')):
        #all languages, with default from db
        parameters.dbDefaultLang(defaultlang)
    else:
        #only one language chosen
        if plang in langs:
            #chosen language is default language (for references from system-files)
            parameters.dbDefaultLang(plang.lower())
        else:
            print ("******* '{}' is invalid language for model '{}'. Valid languages are '{}'".format(plang,pmodel.jsmodel["model"]["name"],','.join(langs)))
            return
    #fi

    #erstelle die Liste der HTML Files für HREF's
    schnlist = printHTML.getmodel().getelements(pelemtype=Modelelemtype.INTF)
    for key,value in schnlist.items():
        printHTML.htmlfilelist[key] = value['name']+ '.html'

    for lang in langs:
        lang = lang.lower()
        Languagetext.reportLang(lang)
        langfilename = printHTML.webFileName + '_' + Languagetext.reportLang() + '.html'
        print ("create web-files for language {} in file {}".format(lang,printHTML.webDirectory + langfilename))
        printHTML.htmlfilelist[0] = langfilename
        printhtmlrender(pfilename=langfilename, planguage=lang, pmodel=printHTML.getmodel())
        # printhtmlfile(pfirma="foryouandyourcustomers"
        #               , ptitel=parameters.odmModelName() + ' ({})'.format(lang)
        #               , pinfo="{}".format(datetime.now().strftime("%Y-%m-%d, %H:%M"))
        #               , plogofilename=parameters.logoFileName()
        #               , pfilename=  langfilename
        #               )
    # for
    Languagetext.reportLang(parameters.dbDefaultLang())
    #backjumps from relational webpage goes to default-lang-model
    printHTML.htmlfilelist[0] = printHTML.webFileName + '_' + parameters.dbDefaultLang() + '.html'

    """Schnittstellen werden immer englisch gedruckt"""
    Languagetext.reportLang(Languagetext.EN)
    lang = Languagetext.EN
    for anker,element in schnlist.items():
        langfilename = printHTML.htmlfilelist[anker]
        print ("create web-files for system {} in file {}".format(element['name'],printHTML.webDirectory + langfilename))
        printhtmlrender(pfilename=langfilename, planguage=lang, pmodel=printHTML.getmodel(), pintfid=anker)
    #for
#listwebmain

def main(pdirec, plang):
    parameters.initparam(p_callarg=pdirec)
    logmessages.initlog('createHTML')

    printHTML.setWebDirec(p_webdirec=None)

    dbConnect.openDB(p_filepath= parameters.dbFilePath());
    deflang = Language.liesdeflangiso2()
    if deflang is not None : parameters.dbDefaultLang(deflang)
    printHTML.setmodel(JSModel(sql2json(pdbname=parameters.dbFilePath())))
    listwebmain(plang=plang)

    dbConnect.myDbConn.close()

    logmessages.showmessages("web-files from database {} for model {} created"
                             .format(parameters.dbFilePath(),parameters.odmModelName()))
#main

if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv)>2) else None
    main(pdirec=direc, plang=lang)