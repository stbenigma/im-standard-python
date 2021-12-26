# -*- coding: latin-1 -*-
import sys
import os
import logging

from IM_db.IM_DB import  dbConnect
from SSOT_infra import parameters, logmessages
from IM_db.IM_OBJECTS import  *
from IM_db.IM_JSON import  JSModel, sql2json
from IM_WEB import jinjawebmodel
from IM_WEB.IM_HTML import printRelHTML, printdiagHTML
from IM_WEB.IM_HTML.printHTML import HTMLExport


def printhtmlrender(export: HTMLExport, pfilename, planguage, pmodel, pintfid=None):
    with export.createFile(pfilename=pfilename) as f:
        if pintfid is None:
            diags = sorted([{"id": key
                                , "name": value["name"]
                                , "svg": printdiagHTML.getsvgtext(export=export, pdiagelem=value, pdiaganker=key,
                                                                  plang=planguage)
                                , "pdf": printdiagHTML.pdffilename(pname=value["name"], plang=planguage)
                             } for key, value in pmodel.jsmodel["diagrams"].items()
                            if (value["type"] == "Entity")]
                           , key=lambda x: x["name"].upper())
        else:
            diags = [{"id": pintfid
                         , "name": pmodel.getbyid(pintfid)["name"]
                         , "svg": printRelHTML.interfacediagram(export=export, pintf=pmodel.getbyid(pintfid))
                         , "pdf": printdiagHTML.pdffilename(pname=pmodel.getbyid(pintfid)["name"], plang=planguage)}
                     ]
        # fi
        html = jinjawebmodel.rendermodel(export=export, pcurlang=planguage, pmodel=pmodel, pintfid=pintfid,
                                         pdiagrams=diags,
                                         phtmlfilelist=export.htmlfilelist)
        export.fhtml.write(html)
        export.closefile()


# printhtmlrenderfile

def listwebmain(export: HTMLExport, plang, pfilter=(None, 'TEST', 'REL')):
    export.createlib()
    export.copyimages()
    model = export.getmodel()
    model.setstatusfilter(pfilter)
    defaultlang = model.jsmodel["model"]["language"]
    langs = model.jsmodel["languages"].keys()
    if (plang is None or (plang.lower() == 'all')):
        # all languages, with default from db
        parameters.dbDefaultLang(defaultlang)
    else:
        # only one language chosen
        if plang in langs:
            # chosen language is default language (for references from system-files)
            parameters.dbDefaultLang(plang.lower())
        else:
            raise Exception(
                f"""******* '{plang}' is invalid language for model '{model.jsmodel["model"]["name"]}'. Valid languages are '{",".join(langs)}'""")
    # fi

    # erstelle die Liste der HTML Files für HREF's
    schnlist = model.getelements(pelemtype=Modelelemtype.INTF)
    for key, value in schnlist.items():
        export.htmlfilelist[key] = value['name'] + '.html'

    langpart = lambda l: '_' + l
    for lang in langs:
        lang = lang.lower()
        Languagetext.reportLang(lang)
        # omit language in name for non translated models
        langfilename = export.webFileName + f"{'' if len(langs) == 1 else langpart(Languagetext.reportLang())}.html"
        logging.info("Generating web content for language {} in {}".format(lang, os.path.join(export.webDirectory,
                                                                                              langfilename)))
        export.htmlfilelist[0] = langfilename
        printhtmlrender(export=export, pfilename=langfilename, planguage=lang, pmodel=model)
    # for
    # prepare for relational models
    Languagetext.reportLang(parameters.dbDefaultLang())
    # backjumps from relational webpage goes to default-lang-model
    export.htmlfilelist[
        0] = export.webFileName + f"{'' if len(langs) == 1 else langpart(parameters.dbDefaultLang())}.html"

    """Schnittstellen werden immer englisch gedruckt"""
    lang = Languagetext.EN if (Languagetext.EN in langs) else parameters.dbDefaultLang()
    Languagetext.reportLang(lang)
    for anker, element in schnlist.items():
        langfilename = export.htmlfilelist[anker]
        logging.info("Generating web content fo system {} in {}".format(element['name'],
                                                                        os.path.join(export.webDirectory,
                                                                                     langfilename)))
        printhtmlrender(export=export, pfilename=langfilename, planguage=lang, pmodel=model, pintfid=anker)
    # for


# listwebmain

def main(pdirec, plang, pinputtype="JSON"):
    parameters.initparam(p_callarg=pdirec)
    logmessages.initlog('createHTML')
    exporter = HTMLExport()
    exporter.setWebDirec(p_webdirec=None)
    modelname = parameters.modelName()
    if pinputtype == "DB":
        dbConnect.openDB(pfilepath=parameters.dbFilePath())
        deflang = Language.liesdeflangiso2()
        if deflang is not None: parameters.dbDefaultLang(deflang)
        jsonmodel = JSModel(sql2json(pdbname=parameters.dbFilePath()))
        jsonfilepath = '<none>'
    elif pinputtype == "JSON":
        jsonfilepath = parameters.dbDirect() + modelname + ".json"
        jsonmodel = JSModel.readfromfile(pfilename=jsonfilepath)
        deflang = jsonmodel.modellanguage()
        modelname = jsonmodel.jsmodel["model"]["name"]
    else:
        raise Exception(f"illegal call parameter {pinputtype}")
    # fi

    if deflang is not None: parameters.dbDefaultLang(deflang)

    exporter.setmodel(jsonmodel)
    listwebmain(exporter, plang=plang)

    if pinputtype == "DB":
        dbConnect.myDbConn.close()
        logmessages.showmessages("web-files from database {} for model {} created"
                                 .format(parameters.dbFilePath(), parameters.modelName()))
    elif pinputtype == "JSON":
        logmessages.showmessages(f"web-files from jsonfile {jsonfilepath} for model {modelname} created")


# main

if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv) > 2) else None
    type = sys.argv[3] if (len(sys.argv) > 3) else "JSON"
    main(pdirec=direc, plang=lang, pinputtype=type)
