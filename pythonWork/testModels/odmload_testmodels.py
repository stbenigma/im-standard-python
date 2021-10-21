import json
import os,shutil,re

import logmessages
from IM_ODM import fillDB
from IM_DB import parameters
from difflib import unified_diff

TESTMODEL1 = "/testmodel-1"
TESTMODEL2 = "/testmodel-2"
CRMTEST = "/crmTest"
MODELMODEL = "/ModellModell"


def emptyloadingfiles(pmodelpath):
    try: os.remove(parameters.logfilepath())
    except Exception as e: pass
    try: shutil.rmtree(parameters.dbDirect())
    except Exception as e: pass
    try: shutil.rmtree(parameters.webDirec())
    except Exception as e: pass

def loadjsonfile(pfilepath,ptext=False):
    with open(pfilepath) as f:
        if ptext:
            retval = f.readlines()
        else:
            retval =json.load(f)
    return retval

def cleaneddiffs(pfile1,pfile2,ptype):
    noproblemdiffjson = lambda l: not (re.match('^\s.*$',l)
                                   or re.match('^[-+]{3}.*$',l)
                                   or re.match('^[@]{2}.*$',l)
                                   or re.match('^[-+]\s+\"created\"\:.*$',l)
                                   or re.match('^[-+]\s+\"(hashvalue|database)\"\:.*$',l)
                                   or re.match('^[-+]\s+\"(dc|dm|um|uc)\"\: .*$',l)
                                   or re.match('^[-+]\s+\"[\d\-]{10} [\d:.]{15}\".*$',l)
                                    )
    #logfiles have lines starting with date-time
    noproblemdifflog = lambda l: not (re.match('^[^-+].*$',l)
                                   or re.match('^[-+]{3}.*$',l)
                                   or re.match('^[@]{2}.*$',l)
                                   or re.match('^[-+]\s*[\d\-]{10} [\d:]{8}.*$',l)
                                      )

    # print ("".join(context_diff(loadedjsontxt,mergedjsontxt)))
    ufd = unified_diff(pfile1, pfile2)
    diff = "".join(ufd).splitlines()
    if ptype == 'json':
        retval = list(filter(noproblemdiffjson,diff))
    elif ptype == 'logfile':
        retval = list(filter(noproblemdifflog, diff))
    return retval

def testloading1model(pcallarg):
    parameters.initparam(p_callarg=pcallarg)
    modelname=parameters.modelName()
    parameters.dbFilePath()

    #load reference files to compare to as json and as text
    #loadedjsonref = loadjsonfile(pcallarg+f"/ref_{modelname}_loaded.json")
    loadedjsonreftxt = loadjsonfile(pcallarg+f"/ref_{modelname}_loaded.json",ptext=True)
    #mergedjsonref = loadjsonfile(pcallarg+f"/ref_{modelname}.json")
    mergedjsonreftxt = loadjsonfile(pfilepath=pcallarg+f"/ref_{modelname}.json",ptext=True)
    logreftext = loadjsonfile(pfilepath=pcallarg+f"/ref_{modelname}.log",ptext=True)

    #Clear environment for test
    emptyloadingfiles(pmodelpath=pcallarg)

    #fill database from ODM for the first time
    fillDB.main(pcallarg)
    loadedjson = loadjsonfile(parameters.dbDirect()+f"{modelname}_loaded.json")
    mergedjson = loadjsonfile(parameters.dbDirect()+f"{modelname}.json")
    loadedjsontxt = loadjsonfile(pfilepath=parameters.dbDirect() + f"{modelname}_loaded.json", ptext=True)
    mergedjsontxt = loadjsonfile(pfilepath=parameters.dbDirect() + f"{modelname}.json", ptext=True)
    logtext = loadjsonfile(pfilepath=pcallarg+f"/{modelname}.log",ptext=True)
    mergeddiff = cleaneddiffs(mergedjsontxt, mergedjsonreftxt,'json')
    loadeddiff = cleaneddiffs(loadedjsontxt, loadedjsonreftxt,'json')
    logdiff = cleaneddiffs(logtext, logreftext,'logfile')

    try:
        #compare loaded json file with merged jsonfile
        #first time load the must be identical in hashvalue
        assert loadedjson["_imprint_"]["hashvalue"] == mergedjson["_imprint_"]["hashvalue"],"new generated jsonfiles: hashvalue mismatch"
        print("          ============ First load json equals first merged json ============")

        #compare loaded json file with refrence loaded json
        #some UC may be different
        assert len(loadeddiff)==0,"new and ref loaded jsonfile : differences"
        print("          ============ First load json matches load json reference ============")

        #compare merged json file with refrence merged json
        #some UC may be different
        assert len(mergeddiff)==0,"new and ref merged jsonfile : differences"
        print("          ============ First merged json matches merged json reference ============")

        #compare written logfile
        assert len(logdiff)==0,"logfile and logfile-reference : differences"
        print("          ============ logfile matches logfile reference ============")


    except Exception as e:
        print (loadeddiff)
        print (mergeddiff)
        print (logdiff)
        raise e

    #fill database from same ODM for the second time (nonempty DB->test merge as well)
    fillDB.main(pcallarg)
    #loadedjson = loadjsonfile(parameters.dbDirect()+f"{modelname}_loaded.json")
    #mergedjson = loadjsonfile(parameters.dbDirect()+f"{modelname}.json")
    loadedjsontxt = loadjsonfile(pfilepath=parameters.dbDirect() + f"{modelname}_loaded.json", ptext=True)
    mergedjsontxt = loadjsonfile(pfilepath=parameters.dbDirect() + f"{modelname}.json", ptext=True)
    newdiff = cleaneddiffs(loadedjsontxt, mergedjsontxt,'json')
    mergeddiff = cleaneddiffs(mergedjsontxt, mergedjsonreftxt,'json')
    loadeddiff = cleaneddiffs(loadedjsontxt, loadedjsonreftxt,'json')
    try:
        #compare loaded json file with merged jsonfile
        #first time load the must be identical in hashvalue
        assert len(newdiff)==0,"new generated jsonfiles: content mismatch"
        print("          ============ Second load json equals first merged json ============")

        #compare loaded json file with refrence loaded json
        #some UC may be different
        assert len(loadeddiff)==0,"new and ref loaded jsonfile : differences"
        print("          ============ Second load json matches load json reference ============")

        #compare merged json file with refrence merged json
        #some UC may be different
        assert len(mergeddiff)==0,"new and ref merged jsonfile : differences"
        print("          ============ Second merged json matches merged json reference ============")
    except Exception as e:
        print (loadeddiff)
        print (mergeddiff)
        raise e
    return

def main():
    curpath=os.getcwd()
    print ("============ Test Loading ODM->SSOT  ============")
    testloading1model(curpath + TESTMODEL1)
    print ("============ Loading ODM->SSOT run without differences ============")
    return

if __name__ == '__main__':
    main()

