import argparse
import logging
import os
import sys
from pathlib import Path

from IM_WEB import jinjawebmodel, htmlparameters
from IM_WEB.IM_HTML import printRelHTML, printdiagHTML
from IM_WEB.IM_HTML.printHTML import HTMLExport
from SSOT_db.IM_JSON import JSModel, FILTEREDJSModel
from SSOT_db.IM_OBJECTS import *
from SSOT_infra import Parameter, logmessages, argparseparent, settransldomain, nvl


def getimdiags(export, curlang, diagtype):
    return sorted([{"id": dkey,
                    "name": dvalue["name"],
                    "svg": printdiagHTML.getsvgtext(export=export, pdiagelem=dvalue, pdiaganker=dkey,
                                                    plang=curlang, pdiagtype=diagtype),
                    "pdf": printdiagHTML.pdffilename(export=export, pname=dvalue["name"], plang=curlang)
                    } for dkey, dvalue in export.model.jsmodel["diagrams"].items()
                   if (dvalue["type"] == "Entity")],
                  key=lambda x: x["name"].upper())


def getdatmdiags(export, datmid, curlang):
    return [{"id": datmid,
             "name": export.model.getbyid(datmid)["name"],
             "svg": printRelHTML.datamodeldiagram(export=export, pdatm=export.model.getbyid(datmid)),
             "pdf": printdiagHTML.pdffilename(export=export, pname=export.model.getbyid(datmid)["name"],
                                              plang=curlang)}
            ]


def printhtmlrender(export: HTMLExport, pfullfilename, pjinjawebmodel=None,
                    pelemtype=None, pelemid=None):

    html = jinjawebmodel.rendermodel(pjinjawebmodel=pjinjawebmodel,
                                     pelemtype=pelemtype, pelemid=pelemid)

    with export.createFile(pfilename=pfullfilename) as fhtmlfile:
        fhtmlfile.write(html)
        fhtmlfile.close()
    return

def listwebmain(export: HTMLExport, diagtype="FYAYC"):
    export.createlib()
    export.copyimages()
    model = export.getmodel()
    export.modelLang(model.modellanguage())
    langs = model.jsmodel["languages"].keys()
    # erstelle die Liste der HTML Files für HREF's
    datmlist = model.getelements(pelemtype=Modelelemtype.DATM)
    for skey, svalue in datmlist.items():
        export.htmlfilelist[skey] = HTMLExport.safe_filename(svalue['name'] + f'.{export.webFileExtension}')

    export.modelLang(export.model.modellanguage())
    langs = export.modellangs()

    export.htmlfilelist[0] = "index"
    # erstelle die Liste der HTML Files für HREF's
    datmlist = export.model.getelements(pelemtype=Modelelemtype.DATM)
    for skey, svalue in datmlist.items():
        export.htmlfilelist[skey] = export.DATAMODELDIREC + "/" + HTMLExport.safe_filename(svalue['name']) + "/index"

    elementtypes = ["entities", "orgunits", "attributes", "domains",
                    "businessrules", "documents", "actorroles", "diagrams"]
    for lang in langs:
        lang = lang.lower()
        Languagetext.reportLang(lang)
        settransldomain(plang=lang)

        # create language path
        fullpath = os.path.join(export.webDirec, lang)
        os.makedirs(name=fullpath, exist_ok=True)

        # create datamodels html directory
        for datmid, element in datmlist.items():
            fullpath = os.path.join(export.webDirec, export.DATAMODELDIREC,
                                    HTMLExport.safe_filename(element['name']))
            os.makedirs(name=fullpath, exist_ok=True)
            for f in os.listdir(fullpath):
                os.remove(os.path.join(fullpath, f))

        langfilename = f"{lang}/{export.fullwebfilename(export.htmlfilelist[0])}"
        logging.info(f"Generating web content for language {lang} in {os.path.join(export.webDirec, langfilename)}")

        # calcualte all diagrams for IM
        imdiags = getimdiags(export=export, curlang=lang, diagtype=diagtype)

        # clean or make language-element-paths
        if not export.singlefile:
            for elemtype in elementtypes:
                elempath = f"{lang}/elements/{elemtype}"
                fullpath = os.path.join(export.webDirec, elempath)
                os.makedirs(name=fullpath, exist_ok=True)
                for f in os.listdir(fullpath):
                    os.remove(os.path.join(fullpath, f))

        # create index-file for language
        langfilename = f"{lang}/{export.fullwebfilename(export.htmlfilelist[0])}"
        jinjamodel = jinjawebmodel.jinjawebmodelim(export=export, curlang=lang,
                                                   diagrams=imdiags)
        printhtmlrender(export=export, pfullfilename=langfilename,
                        pjinjawebmodel=jinjamodel)

        if not export.singlefile:
            jinjamodel = jinjawebmodel.jinjawebmodelim(export=export, curlang=lang, diagrams=imdiags)
            # generate element pages
            for elemtype in elementtypes:
                elempath = f"{lang}/elements/{elemtype}"
                elems = export.model.getelements(pelemtype=elemtype)
                for elemid in elems.keys():
                    langfilename = f"{elempath}/{export.fullwebfilename(elemid)}"
                    logging.info(
                        f"Generating web content for language {lang} in {os.path.join(export.webDirec, langfilename)}")
                    printhtmlrender(export=export, pfullfilename=langfilename,
                                    pjinjawebmodel=jinjamodel,
                                    pelemtype=elemtype, pelemid=elemid)
                    if elemtype=="diagrams":
                        #print svg file for this diagram
                        svgfilename = f"{elempath}/{elemid}.svg"
                        with export.createFile(pfilename=svgfilename) as svgfile:
                            svgfile.write(jinjamodel.getelem(elemid)["svg"])

            # for
            elemtype="mainview"
            langfilename = f"{elempath}/{elemtype}.{export.webFileExtension}"
            printhtmlrender(export=export, pfullfilename=langfilename,
                            pjinjawebmodel=jinjamodel, pelemtype=elemtype)

        # fi
        # break #DEBUG
    # for
    # backjumps from relational webpage goes to default-lang-model
    """Schnittstellen werden immer englisch gedruckt"""
    lang = Languagetext.EN if (Languagetext.EN in langs) else export.modelLang()
    Languagetext.reportLang(lang)
    settransldomain(plang=lang)

    for datmid, datamodel in datmlist.items():
        langfilename = export.fullwebfilename(pfilename=export.htmlfilelist[datmid])
        logging.info(
            f"Generating web content fo datamodel {datamodel['name']} in {os.path.join(export.webDirec, langfilename)}")
        datmdiags = getdatmdiags(export=export, datmid=datmid, curlang=lang)
        jinjamodel = jinjawebmodel.jinjawebmodeldatm(export=export, datmid=datmid, curlang=lang,
                                                     diagrams=datmdiags)
        printhtmlrender(export=export, pfullfilename=langfilename,
                        pjinjawebmodel=jinjamodel)
    # for
    return


def webmain(pjsonfilepath=None, pwebdirec=None, pmodelname=None, plogfilepath=None,
            pfiletype=None, **kwargs):
    assert (pjsonfilepath is not None and pwebdirec is not None), \
        f"jsonsource and destination directory must be given"

    singlefile = kwargs.get("singlefile",False)
    diagtype = kwargs.get("diagtype", "FYAYC")

    if pjsonfilepath is not None:
        jsonfilepath = Path(pjsonfilepath).resolve()
        basedirec = os.path.abspath(os.path.dirname(os.path.dirname(jsonfilepath)))
        jsonmodel = JSModel.readfromfile(pfilename=jsonfilepath)
        modelname = jsonmodel.modelname()
    else:
        basedirec = os.getcwd()
        jsonmodel = None
        modelname = pmodelname

    exporter = HTMLExport(baseDirec=basedirec, modelname=modelname,
                          webDirec=pwebdirec, logofile=plogfilepath,
                          webFileExtension=pfiletype,
                          singlefile=singlefile)
    if pjsonfilepath is None:
        # resolve json path from standards
        jsonfilepath = os.path.join(exporter.dbDirect(), exporter.modelName() + ".json")
        jsonmodel = JSModel.readfromfile(pfilename=jsonfilepath)

    if exporter.modelName() != jsonmodel.modelname():
        raise Exception(f"Modelnames parameter:{exporter.modelName()}" +
                        f" and jsonfile:{jsonmodel.modelname()} do not match")

    try:
        logmessages.initlog('createHTML', plogfilepath=exporter.logfilepath())
        deflang = jsonmodel.modellanguage()

        if deflang is not None:
            exporter.modelLang(deflang)

        status = kwargs.get("status")
        stati = [Modelelement.GTOP, Modelelement.DRAFT, Modelelement.PUBL]
        assert status is None or status.upper() in stati, f"Publication status must be in {stati}"
        diags = kwargs.get("diagrams")
        diagrams = None if diags is None else [dia.strip(" '\"") for dia in diags.split(',')]
        jsonmodel = FILTEREDJSModel(pmodel=jsonmodel.jsmodel, ppublstatus=status, pimdiagrams=diagrams)
        # jsonmodel.printmodel("/Users/stb/Downloads","DEBUG") #DEBUG
        exporter.model = jsonmodel
        listwebmain(exporter, diagtype=diagtype)
    finally:
        logmessages.showmessages(
            f"web-files from jsonfile {jsonfilepath} for model {exporter.modelName()} created into {exporter.webDirec}")


def main(psysargs):
    parser = argparse.ArgumentParser(description='Generate html-pages for model')
    parser.add_argument('--modelname', '-m', dest="modelname")
    parser.add_argument('jsonfile', nargs='?',
                        help=f"Path of the jsonfile to be converted. Default ./{Parameter.SPODDBDIREC}" +
                             f"/<modelname>{Parameter.JSONEXTENSION})")
    parser.add_argument('--destination', '-d', dest="destination",
                        help=f"Directory to write the generated files to . Default ./{htmlparameters.HTMLParameter.WEBDEFAULTDIREC}")
    parser.add_argument('--filetype', '-f', dest="filetype", help=f"html or aspx. Default html",
                        default="html")
    parser.add_argument('--diagtype', '-dt', dest="diagtype", default="FYAYC",
                        help=f"Type of diagramrendering: ODM or FYAYC. Default FYAYC")
    parser.add_argument('--singlefile', '-sf', action='store_true',
                        help=f"Print model in single html-file. Otherwise generate a file per element. Default: False")
    parser.add_argument('--logfile', '-log', dest='logfile',
                        help=f"Path for logfile. Default: ./<modelname>{Parameter.LOGFILEEXTENSION}")
    parser.add_argument('--status', '-s', dest='status',
                        help=f"Filter: publication status (DRAFT, GTOP, PUBL). Default: None")
    parser.add_argument('--diagrams', '-diag', dest='diagrams',
                        help=f"Filter: list of comma seperated diagram names to be published. Default: None")
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
                plogfilepath=myargs['logfile'], pmodelname=myargs['modelname'],
                pfiletype=myargs['filetype'],
                status=myargs["status"], diagrams=myargs["diagrams"],
                singlefile=myargs["singlefile"], diagtype=myargs["diagtype"])
    return


if __name__ == '__main__':
    main(sys.argv)
