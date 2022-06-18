import json
import os
import re
import shutil
from difflib import unified_diff

from SSOT_infra import parameters
from LOAD_MODELS.LOAD_ODM import fillDB


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
    parameters.initparam()
    modelname= parameters.modelName()

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
    loadedjson = loadjsonfile(parameters.dbDirect() + f"{modelname}_loaded.json")
    mergedjson = loadjsonfile(parameters.dbDirect() + f"{modelname}.json")
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
        def lineprint(plist):
            for l in plist:
                print(l)
            #for
            return
        lineprint (loadeddiff)
        lineprint (mergeddiff)
        lineprint (logdiff)
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

def quicktest(pmodel):
    """just run a filldb to check wether it runs through without errors.
        remove all generated files to make sure, it is created with the correct db-version
    """

    #Clear environment for test
    emptyloadingfiles(pmodelpath=pmodel)

    #fill database from ODM for the first time
    try:
        fillDB.main(pmodel)
        modelname = parameters.modelName()
        print(f"============ Test {pmodel} for model {modelname} OK ============\n")
    except Exception as e:
        modelname = parameters.modelName()
        print(pmodel)
        print(e)
        print(f"=*=*=*=*=*=*=*=*=*=*=*= Test {pmodel} for model {modelname} FAILED =*=*=*=*=*=*=*=*=*=*=*=\n")
        raise e
    return

def main(plocaltestdirec,pmodelnames):
    curpath=os.getcwd() + '/testmodels/'
    localtestdirec = '' if plocaltestdirec is None else plocaltestdirec
    modeldirecs ={
        #'official' online testmodels
        'testmodel-1': curpath + 'testmodel-1'
        ,'testmodel-2   ': curpath + 'testmodel-2'
        , 'crmTest': curpath + 'crmTest'
    }
    # additional/private testmodels, locally stored
    privatemodeldirecs = [plocaltestdirec + m for m in pmodelnames]
    print ("============ Test Loading ODM->SSOT  ============")
    testloading1model(modeldirecs['testmodel-1'])
    print ("============ Loading ODM->SSOT run without differences ============")

    if len(privatemodeldirecs) > 0:
        print ("============================================================================================================================")
        print("============ Test load ODM quickrun local models  ============")
    failedcnt =0
    for pm in privatemodeldirecs:
        print(f"============ ODM-Load Test {pm}  ============")
        try:
            quicktest (pm)
        except Exception as e:
            failedcnt += 1
    print("============ Test load ODM quickrun local models ended ============")

    # for pm in privatemodeldirecs:
    #     print(f"============ HTML-Test {pm}  ============")
    #     try:
    #         listWebdoku.main(pdirec=pm,pinputtype='JSON',plang=None)
    #     except:
    #         failedcnt += 1
    # print("============ Test HTML generation quickrun local models ended ============")

    assert (failedcnt == 0),"error in local testmodels"
    return

if __name__ == '__main__':
    import sys
    main(plocaltestdirec=None if len(sys.argv) <= 1 else sys.argv[1]
         ,pmodelnames =sys.argv[2:])

