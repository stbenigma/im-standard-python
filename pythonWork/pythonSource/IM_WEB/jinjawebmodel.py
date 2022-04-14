from IM_WEB.IM_HTML import HTMLExport
from SSOT_db.IM_JSON import  JSModel
from IM_WEB import jinja2web


def rendermodel(export: HTMLExport, pmodel: JSModel, pcurlang, pintfid=None, phtmlfilelist=None, pdiagrams=None):
    if phtmlfilelist is None:
        phtmlfilelist = {}
    if pdiagrams is None:
        pdiagrams = []
    webmodel = jinja2web.Webmodel(export=export, pcurlang=pcurlang, pjsmodel=pmodel, pintfid=pintfid,
                                  phtmlfilelist=phtmlfilelist)
    modelname = pmodel.getelements("model")["name"]
    if pintfid is None:
        webmodel.setelements(metainfo = {"title" : modelname,
                                     "modelname" : modelname
                                     },
                        entities = sorted([[key, value["name"][pcurlang]] for key, value in pmodel.jsmodel["entities"].items()],
                                           key=lambda x:x[1].upper()),
                        attributes = sorted ([[key, value["name"][pcurlang]] for key, value in pmodel.jsmodel["attributes"].items()],
                                              key=lambda x:x[1].upper()),
                        domains=sorted([[key, value["name"][pcurlang]] for key, value in pmodel.jsmodel["domains"].items()
                                                    if (value["interface-id"] is None and value["origin"] == "DOM")],
                                               key=lambda x: x[1].upper() if x[1] is not None else ''),
                        businessrules=sorted([[key, value["name"][pcurlang]] for key, value in pmodel.jsmodel["businessrules"].items()],
                                               key=lambda x: x[1].upper() if x[1] is not None else ''),
                        documents=sorted([[key, "{} ({})".format(value["name"],str(len(value['references+'])))] for key, value in pmodel.jsmodel["documents"].items()],
                                         key=lambda x: x[1].upper()),
                         orgunits=sorted([[key, "{} ({})".format(value["name"], str(len(value['references+'])))] for key, value in
                                                    pmodel.jsmodel["orgunits"].items()],
                                                 key=lambda x: x[1].upper()),
                         systems=sorted([[key, value["name"]] for key, value in pmodel.jsmodel["systems"].items()],
                                                 key=lambda x: x[1].upper()),
                              diagrams =pdiagrams)

    else:
        title = pmodel.getbyid(pintfid)["name"]
        webmodel.setelements(metainfo = {"title" : title,
                                     "modelname" : modelname,
                                     },
                        tables = sorted([[key, value["name"]] for key, value in pmodel.jsmodel["tables"].items()
                                      if value["interface-id"] == pintfid],key=lambda x:x[1].upper()),
                        columns = sorted ([[key, value["name"]] for key, value in pmodel.jsmodel["columns"].items()
                                      if value["interface-id+"] == pintfid],key=lambda x:x[1].upper()),
                         domains = sorted ([[key, value["name"][pcurlang]] for key, value in pmodel.jsmodel["domains"].items()
                                      if (value["interface-id"] == pintfid) and (value["origin"] == "DOM")],key=lambda x:x[1].upper()),
                        diagrams =pdiagrams)
    #fi
    retval = jinja2web.model2html(pwebmodel=webmodel)
    return retval

