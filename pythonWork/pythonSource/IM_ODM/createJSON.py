# -*- coding: latin-1 -*-
import json
import math

from IM_DB import dbConnect, parameters, logmessages
from IM_OBJECTS import *
from mystring import nvl
from IM_JSON import sql2json

EMPTYJSONFILE = 'emptyjsonmodel'

def getJSONfile(pfilename):
    with open(pfilename, 'r') as handle:
        model = json.load(handle)
    return model




anker = lambda n, i: None if i is None else n + str(i)

def jsonfilename(pfilename):
    return pfilename + '.json'

emptystruct = lambda x: x == EMPTYJSONFILE

def printJSON(pmodel, pfilepath, pfilename):
    jsonfile = open(pfilepath + jsonfilename(pfilename), 'w')
    jsonfile.write(json.dumps(pmodel, indent=3, sort_keys=False))
    jsonfile.close()

def createJSON(pfilepath, pfilename):
    if pfilename is not None:
        dbConnect.openDB(parameters.dbFilePath(), fks='ON')

    jsmodel = sql2json(pmodelname=parameters.odmModelName(),pwithdata=not emptystruct(EMPTYJSONFILE))
    printJSON(pmodel=jsmodel, pfilename=pfilename, pfilepath=pfilepath)
    if (not emptystruct(EMPTYJSONFILE)):
        dbConnect.myDbConn.close()

# createJSON
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
    if emptystruct(param1):
        filename = param1
        filepath = '~/Downloads/'
    else:
        parameters.initparam(p_callarg=param1)
        logmessages.initlog('createJSON')
        filename = parameters.odmModelName()
        filepath = parameters.dbDirect()
    # fi
    try:
        createJSON(pfilepath=filepath, pfilename=filename)
    finally:
        if emptystruct:
            print("JSON file {} for model {} created"
                  .format(filepath + jsonfilename(filename), EMPTYJSONFILE))
        else:
            logmessages.showmessages("JSON file {} for model {} created"
                                     .format(filepath + jsonfilename(filename), parameters.odmModelName()))

    #model = getJSONfile(filepath + jsonfilename(filename))
    #print (json2xml(model))
#  main

if __name__ == '__main__':
    import sys
    main(param1=EMPTYJSONFILE if len(sys.argv) <= 1 else sys.argv[1])
