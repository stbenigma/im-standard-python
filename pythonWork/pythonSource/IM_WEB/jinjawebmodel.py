from IM_JSON import JSModel,jsguid2type
from IM_WEB import jinja2web

def rendermodel(pmodel:JSModel,pcurlang,pintfid=None,phtmlfilelist={},pdiagrams=[]):
    webmodel = jinja2web.Webmodel(pcurlang=pcurlang,pjsmodel=pmodel,pintfid=pintfid,phtmlfilelist=phtmlfilelist)
    modelname = pmodel.getelements("model")["name"]
    if pintfid is None:
        title = modelname
        interfacename = None
    else:
        title = pmodel.getbyid(pintfid)["name"]
        interfacename = pmodel.getbyid(pintfid)["name"]
        webmodel.setelements(metainfo = {"title" : title
                                    ,"modelname" : modelname
                                    ,}
                       ,tables = sorted([[key, value["name"]] for key, value in pmodel.jsmodel["tables"].items()
                                      if value["interface-id"] == pintfid],key=lambda x:x[1].upper())
                       ,columns = sorted ([[key, value["name"]] for key, value in pmodel.jsmodel["columns"].items()
                                      if value["interface-id+"] == pintfid],key=lambda x:x[1].upper())
                        ,domains = sorted ([[key, value["name"][pcurlang]] for key, value in pmodel.jsmodel["domains"].items()
                                      if (value["interface-id"] == pintfid) and (value["origin"] == "DOM")],key=lambda x:x[1].upper())
                       ,diagrams =pdiagrams)
    #fi
    retval = jinja2web.model2html(pwebmodel=webmodel)
    return retval

