from IM_WEB.IM_HTML import HTMLExport
from IM_WEB import jinja2web

def jinjawebmodeldatm(export, datmid, curlang, diagrams):
    webmodel = jinja2web.Webmodel(export=export, pcurlang=curlang, pdatmid=datmid)
    webmodel.setelements(metainfo={"title": export.model.getbyid(datmid)["name"],
                                   "modelname": export.model.getelements("model")["name"],
                                   "company": "foryouandyourcustomers" ,
                                   },
                         tables=sorted([[key, value["name"]] for key, value in export.model.jsmodel["tables"].items()
                                        if value["datamodel-id"] == datmid], key=lambda x: x[1].upper()),
                         columns=sorted([[key, value["name"]] for key, value in export.model.jsmodel["columns"].items()
                                         if value["datamodel-id+"] == datmid], key=lambda x: x[1].upper()),
                         domains=sorted(
                             [[key, value["name"][curlang]] for key, value in export.model.jsmodel["domains"].items()
                              if (value["datamodel-id"] == datmid) and (value["origin"] == "DOM")],
                             key=lambda x: x[1].upper()),
                         diagrams=diagrams)
    return webmodel

def jinjawebmodelim(export, curlang, diagrams):
    webmodel = jinja2web.Webmodel(export=export, pcurlang=curlang, pdatmid=None)
    webmodel.setelements(metainfo={"title": export.model.getelements("model")["name"],
                                   "modelname": export.model.getelements("model")["name"],
                                   "company": "foryouandyourcustomers" ,
                                   },
                         entities=sorted([[key, value["name"][curlang]] for key, value in
                                          export.model.jsmodel["entities"].items()],
                                         key=lambda x: x[1].upper()),
                         attributes=sorted([[key, value["name"][curlang]] for key, value in
                                            export.model.jsmodel["attributes"].items()],
                                           key=lambda x: x[1].upper()),
                         domains=sorted(
                             [[key, value["name"][curlang]] for key, value in export.model.jsmodel["domains"].items()
                              if (value["datamodel-id"] is None and value["origin"] == "DOM")],
                             key=lambda x: x[1].upper() if x[1] is not None else ''),
                         businessrules=sorted([[key, value["name"][curlang]] for key, value in
                                               export.model.jsmodel["businessrules"].items()],
                                              key=lambda x: x[1].upper() if x[1] is not None else ''),
                         documents=sorted(
                             [[key, "{} ({})".format(value["name"], str(len(value['references+'])))] for key, value in
                              export.model.jsmodel["documents"].items()],
                             key=lambda x: x[1].upper()),
                         orgunits=sorted(
                             [[key, "{} ({})".format(value["name"], str(len(value['references+'])))] for key, value in
                              export.model.jsmodel["orgunits"].items()],
                             key=lambda x: x[1].upper()),
                         actorroles=sorted([[key, f"{value['name']} ({str(len(value['concerns']))})"] for key, value in
                                            export.model.jsmodel["actorroles"].items()],
                                           key=lambda x: x[1].upper()),
                         datamodels=sorted(
                             [[key, value["name"]] for key, value in export.model.jsmodel["datamodels"].items()],
                             key=lambda x: x[1].upper()),
                         diagrams=diagrams)
    imdiagids = [d["id"] for d in diagrams]
    # STARTDIAGRAM is mainview with Kacheln or single diagram
    export.startdiagram = imdiagids[0] if len(imdiagids) == 1 else "mainview"

    return webmodel

def rendermodel(pjinjawebmodel,pelemtype=None,pelemid=None):
    if pelemtype is None:
        #main file rendering
        retval = jinja2web.model2html(pwebmodel=pjinjawebmodel)
    else:
        #objectfile rendering
        retval= jinja2web.element2html(pwebmodel=pjinjawebmodel, pelemtype=pelemtype, pelemid=pelemid)

    return retval
