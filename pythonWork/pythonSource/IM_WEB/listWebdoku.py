# -*- coding: latin-1 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../IM_db')
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/..')
from IM_DB import dbConnect
from SSOT_infra import parameters, logmessages,nvl
from IM_HTML import printHTML, printRelHTML,printdiagHTML
from IM_OBJECTS import *
from IM_JSON import JSModel,sql2json
from IM_WEB import jinjawebmodel


def formatDatentyp(w):
    dt = anzDatentyp(w[0])
    return(
    "{}   ({}) {} {}" .format(dt, w[3], nvl(w[1]) + nvl2(w[1], '', ' - ')
                              , nvl(w[2]), nvl(w[11]), nvl(w[6])) if w[0] == 'ZPKT'\
        else '{}  ({}:{})   {}  {}'\
                .format(dt, nvl(w[8]), nvl(w[9]), nvl(w[7]).__str__() + nvl2(w[7], '', ' - ')
                        , nvl(w[10]))     if w[0] == 'NUM'\
        else '{}  ({}) {}'\
            .format(dt, nvl(w[4]), 'CHECK: ' + nvl(w[5], ''))   if w[0] == 'TEXT'\
        else '{}  ({})'\
                 .format(dt, nvl(w[4])) if w[0] == 'LOV'\
        else dt
    )
#formatDatentyp

def printhtmlrender(pfilename, planguage, pmodel, pintfid=None):
    printHTML.createFile (pfilename=pfilename)

    if pintfid is None:
        diags =sorted([{"id":key
                 ,"name": value["name"]
                ,"svg": printdiagHTML.getsvgtext(pdiagelem=value,pdiaganker=key,plang=planguage)
                , "pdf": printdiagHTML.pdffilename(pname=value["name"], plang=planguage)
                        } for key, value in pmodel.jsmodel["diagrams"].items()
                                                    if (value["type"] == "Entity")]
                , key=lambda x: x["name"].upper())
    else:
        diags = [{"id": pintfid
                , "name": pmodel.getbyid(pintfid)["name"]
                , "svg": printRelHTML.interfacediagram(pintf=pmodel.getbyid(pintfid))
               , "pdf": printdiagHTML.pdffilename(pname=pmodel.getbyid(pintfid)["name"], plang=planguage)}
        ]
    #fi
    html = jinjawebmodel.rendermodel(pcurlang=planguage,pmodel=pmodel,pintfid=pintfid,pdiagrams=diags,phtmlfilelist=printHTML.htmlfilelist)
    printHTML.fhtml.write(html)
    printHTML.closefile ();
#printhtmlrenderfile

def listwebmain(plang,pfilter=(None,'TEST','REL')):
    printHTML.createlib()
    printHTML.copyimages()
    model = printHTML.getmodel()
    model.setstatusfilter(pfilter)
    defaultlang = model.jsmodel["model"]["language"]
    langs = model.jsmodel["languages"].keys()
    if (plang is None or (plang.lower() == 'all')):
        #all languages, with default from db
        parameters.dbDefaultLang(defaultlang)
    else:
        #only one language chosen
        if plang in langs:
            #chosen language is default language (for references from system-files)
            parameters.dbDefaultLang(plang.lower())
        else:
            print ("******* '{}' is invalid language for model '{}'. Valid languages are '{}'".format(plang,model.jsmodel["model"]["name"],','.join(langs)))
            return
    #fi

    #erstelle die Liste der HTML Files für HREF's
    schnlist = model.getelements(pelemtype=Modelelemtype.INTF)
    for key,value in schnlist.items():
        printHTML.htmlfilelist[key] = value['name']+ '.html'

    langpart = lambda l : '_' + l
    for lang in langs:
        lang = lang.lower()
        Languagetext.reportLang(lang)
        #omit language in name for non translated models
        langfilename = printHTML.webFileName + f"{'' if len(langs) == 1 else langpart(Languagetext.reportLang())}.html"
        print ("create web-files for language {} in file {}".format(lang,printHTML.webDirectory + langfilename))
        printHTML.htmlfilelist[0] = langfilename
        printhtmlrender(pfilename=langfilename, planguage=lang, pmodel=model)
    # for
    #prepare for relational models
    Languagetext.reportLang(parameters.dbDefaultLang())
    #backjumps from relational webpage goes to default-lang-model
    printHTML.htmlfilelist[0] = printHTML.webFileName + f"{'' if len(langs) == 1 else langpart(parameters.dbDefaultLang())}.html"

    """Schnittstellen werden immer englisch gedruckt"""
    lang = Languagetext.EN if (Languagetext.EN in langs) else parameters.dbDefaultLang()
    Languagetext.reportLang(lang)
    for anker,element in schnlist.items():
        langfilename = printHTML.htmlfilelist[anker]
        print ("create web-files for system {} in file {}".format(element['name'],printHTML.webDirectory + langfilename))
        printhtmlrender(pfilename=langfilename, planguage=lang, pmodel=model, pintfid=anker)
    #for
#listwebmain

def main(pdirec, plang, pinputtype="JSON"):
    parameters.initparam(p_callarg=pdirec)
    logmessages.initlog('createHTML')
    printHTML.setWebDirec(p_webdirec=None)
    modelname = parameters.modelName()
    if pinputtype == "DB":
        dbConnect.openDB(pfilepath= parameters.dbFilePath());
        deflang = Language.liesdeflangiso2()
        if deflang is not None: parameters.dbDefaultLang(deflang)
        jsonmodel = JSModel(sql2json(pdbname=parameters.dbFilePath()))
    elif pinputtype == "JSON":
        jsonfilepath = parameters.dbDirect() + modelname + ".json"
        jsonmodel = JSModel.readfromfile(pfilename=jsonfilepath)
        deflang = jsonmodel.modellanguage()
        modelname = jsonmodel.jsmodel["model"]["name"]
    else:
        raise Exception(f"illegal call parameter {pinputtype}")
    #fi

    if deflang is not None: parameters.dbDefaultLang(deflang)

    printHTML.setmodel(jsonmodel)
    listwebmain(plang=plang)

    if pinputtype == "DB":
        dbConnect.myDbConn.close()
        logmessages.showmessages("web-files from database {} for model {} created"
                                 .format(parameters.dbFilePath(), parameters.modelName()))
    elif pinputtype == "JSON":
        logmessages.showmessages(f"web-files from jsonfile {jsonfilepath} for model {modelname} created")

#main

if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv)>2) else None
    type = sys.argv[3] if (len(sys.argv)>3) else "JSON"
    main(pdirec=direc, plang=lang, pinputtype=type)