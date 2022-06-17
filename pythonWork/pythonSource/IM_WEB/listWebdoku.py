# -*- coding: latin-1 -*-
import argparse
import logging
import os
import sys
from pathlib import Path

from IM_WEB import jinjawebmodel,htmlparameters
from IM_WEB.IM_HTML import printRelHTML, printdiagHTML
from IM_WEB.IM_HTML.printHTML import HTMLExport
from SSOT_db.IM_JSON import JSModel,FILTEREDJSModel
from SSOT_db.IM_OBJECTS import *
from SSOT_infra import parameters,Parameter, logmessages, argparseparent,settransldomain


def printhtmlrender(export: HTMLExport, pfilename, planguage, pmodel, pintfid=None):
    settransldomain(plang=planguage)
    with export.createFile(pfilename=pfilename):
        if pintfid is None:
            diags = sorted([{"id": dkey,
                             "name": dvalue["name"],
                             "svg": printdiagHTML.getsvgtext(export=export, pdiagelem=dvalue, pdiaganker=dkey,
                                                             plang=planguage),
                             "pdf": printdiagHTML.pdffilename(export=export,pname=dvalue["name"], plang=planguage)
                             } for dkey, dvalue in pmodel.jsmodel["diagrams"].items()
                            if (dvalue["type"] == "Entity")],
                           key=lambda x: x["name"].upper())
        else:
            diags = [{"id": pintfid,
                      "name": pmodel.getbyid(pintfid)["name"],
                      "svg": printRelHTML.interfacediagram(export=export, pintf=pmodel.getbyid(pintfid)),
                      "pdf": printdiagHTML.pdffilename(export=export,pname=pmodel.getbyid(pintfid)["name"], plang=planguage)}
                     ]
        # fi
        html = jinjawebmodel.rendermodel(export=export, pcurlang=planguage, pmodel=pmodel, pintfid=pintfid,
                                         pdiagrams=diags,
                                         phtmlfilelist=export.htmlfilelist)
        export.fhtml.write(html)
        export.closefile()
    return


def safe_filename(path: str) -> str:
    return path.replace('/', '-').replace(' - ', '-')


def listwebmain(export: HTMLExport):
    def langpart(plang):
        return '_' + plang

    export.createlib()
    export.copyimages()
    model = export.getmodel()
    export.modelLang(model.modellanguage())
    langs = model.jsmodel["languages"].keys()
    # erstelle die Liste der HTML Files für HREF's
    schnlist = model.getelements(pelemtype=Modelelemtype.INTF)
    for skey, svalue in schnlist.items():
        export.htmlfilelist[skey] = safe_filename(svalue['name'] + '.html')

    for lang in langs:
        lang = lang.lower()
        Languagetext.reportLang(lang)
        # omit language in name for non translated models
        langfilename = export.webFileName + f"{'' if len(langs) == 1 else langpart(Languagetext.reportLang())}.html"
        logging.info(f"Generating web content for language {lang} in {os.path.join(export.webDirec(),langfilename)}")
        export.htmlfilelist[0] = langfilename
        printhtmlrender(export=export, pfilename=langfilename, planguage=lang, pmodel=model)
    # for
    # prepare for relational models
    Languagetext.reportLang(export.modelLang())
    # backjumps from relational webpage goes to default-lang-model
    export.htmlfilelist[0] \
        = export.webFileName + f"{'' if len(langs) == 1 else langpart(export.modelLang())}.html"

    """Schnittstellen werden immer englisch gedruckt"""
    lang = Languagetext.EN if (Languagetext.EN in langs) else export.modelLang()
    Languagetext.reportLang(lang)
    for anker, element in schnlist.items():
        langfilename = export.htmlfilelist[anker]
        logging.info("Generating web content fo system {} in {}".format(element['name'],
                                                                        os.path.join(export.webDirec(),
                                                                                     langfilename)))
        printhtmlrender(export=export, pfilename=langfilename, planguage=lang, pmodel=model, pintfid=anker)
    # for
    return


def webmain(pjsonfilepath=None, pwebdirec=None, pmodelname=None, plogfilepath=None, **kwargs ):
    assert (pjsonfilepath is not None and pwebdirec is not None),\
        f"jsonsource and destination directory must be given"

    status = None
    diagrams = None
    for key,val in kwargs.items():
        if key == "status" :
            status = val
            stati= [Modelelement.GTOP,Modelelement.DRAFT,Modelelement.PUBL]
            assert status is None or status.upper()  in stati, f"Publication status must be in {stati}"
        elif key == "diagrams" and val is not None:
            diagrams = [dia.strip(" '\"") for dia in val.split(',')]
        #fi
    #for

    if pjsonfilepath is not None:
        jsonfilepath=Path(pjsonfilepath).resolve()
        basedirec = os.path.abspath(os.path.dirname(os.path.dirname(jsonfilepath)))
        jsonmodel = JSModel.readfromfile(pfilename=jsonfilepath)
        modelname = jsonmodel.modelname()
    else:
        basedirec = os.getcwd()
        jsonmodel = None
        modelname = pmodelname

    exporter = HTMLExport(baseDirec=basedirec, modelname=modelname,
                          webDirec=pwebdirec, logofile=plogfilepath)
    try:
        logmessages.initlog('createHTML',
                            plogfilepath=exporter.logfilepath())
        if jsonfilepath is None:
            jsonfilepath = os.path.join(exporter.dbDirec(), exporter.modelName() + ".json")
            jsonmodel = JSModel.readfromfile(pfilename=jsonfilepath)
        elif exporter.modelName() != jsonmodel.modelname():
            raise Exception(f"Modelnames parameter:{exporter.modelName()}" +
                            f" and jsonfile:{jsonmodel.modelname()} do not match")
        deflang = jsonmodel.modellanguage()

        if deflang is not None:
            exporter.modelLang(deflang)

        jsonmodel = FILTEREDJSModel(pmodel = jsonmodel.jsmodel,ppublstatus=status,pimdiagrams=diagrams)
        #jsonmodel.printmodel("/Users/stb/Downloads","DEBUG") #DEBUG
        exporter.setmodel(jsonmodel)
        listwebmain(exporter)
    finally:
        logmessages.showmessages(f"web-files from jsonfile {jsonfilepath} for model {exporter.modelName()} created into {exporter.webDirec()}")


def main(psysargs):
    parser = argparse.ArgumentParser(description='Generate html-pages for model')
    parser.add_argument('--modelname', '-m', dest="modelname")
    parser.add_argument('jsonfile', nargs='?',
                        help=f"Path of the jsonfile to be converted. Default ./{Parameter.SPODDBDIREC}" +
                             f"/<modelname>{Parameter.JSONEXTENSION})")
    parser.add_argument('--destination', '-d', dest="destination",
                        help=f"Directory to write the generated files to . Default ./{htmlparameters.HTMLParameter.WEBDEFAULTDIREC}")
    parser.add_argument('--logfile', '-log', dest='logfile',
                        help=f"Path for logfile. Default: ./<modelname>{Parameter.LOGFILEEXTENSION}")
    parser.add_argument('--status', '-s', dest='status',
                        help=f"Publication status (DRAFT, GTOP, PUBL). Default: None")
    parser.add_argument('--diagrams', '-diag', dest='diagrams',
                        help=f"List of comma seperated diagram names to be published. Default: None")
    parser.add_argument('--version', '-v', action='store_true')
    parser.add_argument('--unittest', action='store_true', dest='unittest',
                        help=argparse.SUPPRESS)  # for testing purposes only

    argparse.Namespace()

    if (len(psysargs) > 0) and ('.py' in psysargs[0]) and ('ipykernel' not in psysargs[0]):
        arguments: argparse.Namespace = parser.parse_args(psysargs[1:])
        myargs = arguments.__dict__
    else:
        # in jupyter environment
        """set myargs with arguments """
        myargs = {}
    # fi
    if myargs['version']:
        argparseparent.showversion()
        exit(0)

    currentdir = os.getcwd()
    argparseparent.fillssotdefaults(pcurrentdir=currentdir, parguments=myargs)
    if myargs['modelname'] is not None:
        if myargs['jsonfile'] is None:
            myargs['jsonfile'] = os.path.join(currentdir, Parameter.SPODDBDIREC,
                                              myargs['modelname'] + Parameter.JSONEXTENSION)
    # fi

    if myargs['jsonfile'] is None and myargs['modelname'] is None:
        print(f"Either modelname or jsonfile must be given.")
        exit(1)

    # do only testing of parameterpassing while in unittest
    if not myargs["unittest"]:
        webmain(pjsonfilepath=myargs['jsonfile'], pwebdirec=myargs['destination'],
                plogfilepath=myargs['logfile'], pmodelname=myargs['modelname']
                ,status=myargs["status"],diagrams=myargs["diagrams"])
    return


if __name__ == '__main__':
    main(sys.argv)
