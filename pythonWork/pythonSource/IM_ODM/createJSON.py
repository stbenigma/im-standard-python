# -*- coding: latin-1 -*-
import json
from IM_DB import dbConnect, parameters, logmessages
from IM_JSON import sql2json,jsonfilename,JSModel

def getJSONfile(pfilename):
    with open(pfilename, 'r') as handle:
        model = json.load(handle)
    return model


def createJSON(pfilepath, pfilename):
    dbConnect.openDB(parameters.dbFilePath(), fks='ON')

    jsmodel = JSModel(pmodel=sql2json(pmodelname=parameters.odmModelName(),pdbname=dbConnect.getDBname()))

    jsmodel.printmodel(pfilepath=pfilepath,pfilename=pfilename)
    dbConnect.myDbConn.close()
    return

def json2xml(json_obj, line_padding=""):
    result_list = list()

    json_obj_type = type(json_obj)

    if json_obj_type is list:
        for sub_elem in json_obj:
            result_list.append(json2xml(sub_elem, line_padding))

        return "\n".join(result_list)

    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            if sub_obj is None: continue
            result_list.append("%s<%s>" % (line_padding, tag_name))
            result_list.append(json2xml(sub_obj, "\t" + line_padding))
            result_list.append("%s</%s>" % (line_padding, tag_name))

        return "\n".join(result_list)

    return "%s%s" % (line_padding, json_obj)
#json2xml

def main(param1):
    parameters.initparam(p_callarg=param1)
    logmessages.initlog('createJSON')
    filename = parameters.odmModelName()
    filepath = parameters.dbDirect()
    try:
        createJSON(pfilepath=filepath, pfilename=filename)
    finally:
        logmessages.showmessages("JSON file {} for model {} created"
                                    .format(filepath + jsonfilename(filename), parameters.odmModelName()))
#  main

if __name__ == '__main__':
    import sys
    main(param1=sys.argv[1])
