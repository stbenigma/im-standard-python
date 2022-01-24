# -*- coding: latin-1 -*-
import argparse
import logging
import os
import sys

from IM_WEB import jinjawebmodel
from IM_WEB.IM_HTML import printRelHTML, printdiagHTML
from IM_WEB.IM_HTML.printHTML import HTMLExport
from SSOT_db.IM_JSON import JSModel
from SSOT_db.IM_OBJECTS import *
from SSOT_infra import parameters, logmessages, argparseparent,settransldomain


def printhtmlrender(export: HTMLExport, pfilename, planguage, pmodel, pintfid=None):
    settransldomain(plang=planguage)
    with export.createFile(pfilename=pfilename):
        if pintfid is None:
            diags = sorted([{"id": dkey,
                             "name": dvalue["name"],
                             "svg": printdiagHTML.getsvgtext(export=export, pdiagelem=dvalue, pdiaganker=dkey,
                                                             plang=planguage),
                             "pdf": printdiagHTML.pdffilename(pname=dvalue["name"], plang=planguage)
                             } for dkey, dvalue in pmodel.jsmodel["diagrams"].items()
                            if (dvalue["type"] == "Entity")],
                           key=lambda x: x["name"].upper())
        else:
            diags = [{"id": pintfid,
                      "name": pmodel.getbyid(pintfid)["name"],
                      "svg": printRelHTML.interfacediagram(export=export, pintf=pmodel.getbyid(pintfid)),
                      "pdf": printdiagHTML.pdffilename(pname=pmodel.getbyid(pintfid)["name"], plang=planguage)}
                     ]
        # fi
        html = jinjawebmodel.rendermodel(export=export, pcurlang=planguage, pmodel=pmodel, pintfid=pintfid,
                                         pdiagrams=diags,
                                         phtmlfilelist=export.htmlfilelist)
        export.fhtml.write(html)
        export.closefile()
    return


def listwebmain(export: HTMLExport, pfilter=(None, 'TEST', 'REL')):
    def langpart(plang):
        return '_' + plang

    export.createlib()
    export.copyimages()
    model = export.getmodel()
    model.setstatusfilter(pfilter)
    parameters.dbDefaultLang(model.modellanguage())
    langs = model.jsmodel["languages"].keys()
    # erstelle die Liste der HTML Files für HREF's
    schnlist = model.getelements(pelemtype=Modelelemtype.INTF)
    for skey, svalue in schnlist.items():
        export.htmlfilelist[skey] = svalue['name'] + '.html'

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
    return


def webmain(pparamfile=None, pjsonfilepath=None, pwebdirec=None, pmodelname=None, plogfilepath=None, ):
    assert (pparamfile is not None or (
                pjsonfilepath is not None and pwebdirec is not None)), f"paramfile or source and dest must begiven"

    if pparamfile is not None:
        basedirec = os.path.abspath(os.path.dirname(pparamfile))
    else:
        # modelname given, take current directory as basedirec
        basedirec = os.getcwd()
    # fi

    if pjsonfilepath is not None:
        jsonmodel = JSModel.readfromfile(pfilename=pjsonfilepath)
        modelname = jsonmodel.modelname()
    else:
        jsonmodel = None
        modelname = pmodelname

    parameters.initparam(pbasedirec=basedirec, pparamfile=pparamfile, pmodelname=modelname, plogfilepath=plogfilepath,
                         pwebdirec=pwebdirec)

    logmessages.initlog('createHTML')
    try:
        exporter = HTMLExport()
        exporter.setWebDirec(p_webdirec=None)
        jsonfilepath = pjsonfilepath
        if jsonfilepath is None:
            jsonfilepath = os.path.join(parameters.dbDirect(), parameters.modelName() + ".json")
            jsonmodel = JSModel.readfromfile(pfilename=jsonfilepath)
        elif parameters.modelName() != jsonmodel.modelname():
            raise Exception(f"Modelnames parameter:{parameters.modelName()}" +
                            f" and jsonfile:{jsonmodel.modelname()} do not match")
        deflang = jsonmodel.modellanguage()

        if deflang is not None:
            parameters.dbDefaultLang(deflang)

        exporter.setmodel(jsonmodel)
        listwebmain(exporter)

    finally:
        logmessages.showmessages(f"web-files from jsonfile {jsonfilepath} for model {parameters.modelName()} created into {parameters.webDirec()}")


def main(psysargs):
    parser = argparse.ArgumentParser(description='Generate html-pages for model')
    parser.add_argument('--paramfile', '-p', dest='paramfile',
                        help=f"Parameterfile for modelenvironent. Default: " +
                             f"./<modelname>{parameters.PARAMFILEEXTENSION}")
    parser.add_argument('--modelname', '-m', dest="modelname")
    parser.add_argument('jsonfile', nargs='?',
                        help=f"Path of the jsonfile to be converted. Default ./{parameters.SSOTDBDIREC}" +
                             f"/<modelname>{parameters.JSONEXTENSION})")
    parser.add_argument('--destination', '-d', dest="destination",
                        help=f"Directory to write the generated files to . Default ./{parameters.WEBDEFAULTDIREC}")
    parser.add_argument('--logfile', '-log', dest='logfile',
                        help=f"Path for logfile. Default: ./<modelname>{parameters.LOGFILEEXTENSION}")
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
            myargs['jsonfile'] = os.path.join(currentdir, parameters.SSOTDBDIREC,
                                              myargs['modelname'] + parameters.JSONEXTENSION)
    # fi

    if myargs['jsonfile'] is None and myargs['modelname'] is None and myargs['paramfile'] is None:
        print(f"Either modelname or jsonfile must be given.")
        exit(1)

    # do only testing of parameterpassing while in unittest
    if not myargs["unittest"]:
        webmain(pparamfile=myargs['paramfile'], pjsonfilepath=myargs['jsonfile'], pwebdirec=myargs['destination'],
                plogfilepath=myargs['logfile'], pmodelname=myargs['modelname'])
    return


if __name__ == '__main__':
    main(sys.argv)
