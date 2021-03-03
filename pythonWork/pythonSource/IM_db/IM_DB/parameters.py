import os
import re
from pathlib import Path
import json

""" Sammlung aller Parameter für die Verwaltung der Datenbank und aller Tools"""
MODELNAME:str = 'odmmodelname'
ODMIMDIREC:str = 'odmimdirec'
ODMBASEDIREC:str = 'odmbasedirec'
DBDEFAULTLANG:str = 'dbdefaultlang'
DBLANGUAGES:str = 'dblanguages'
LOGFILEDIREC:str = 'logfiledirec'
LOGFILEPATH:str = 'logfilepath'
VERSIONFILEPATH:str=os.path.dirname(os.path.abspath(__file__))+"/../../versions.json"
with open(VERSIONFILEPATH, 'r') as handle:
    versions = json.load(handle)
def toolversion():
    return versions['TOOLVERSION']

SQLITE:str = 'sqlite'
SQLSERVER:str = 'sql-server'
POSTGRES:str = 'postgres'

paramFileExension:str = ".params"
parameter = {'dbtype': SQLITE
             ,'sqlpath': os.path.dirname(os.path.abspath(__file__))+"/../sqlfiles/"
            , 'sqlfilename': 'modelmodel_'+SQLITE
            ,'dbfilepath': None
            , 'dbdirec' : None
            , 'dbfileextension' : '.db'
            , 'dbdefaultdirec':'DB/'
            , DBDEFAULTLANG: 'de'
            , DBLANGUAGES : 'de,en'
            , 'dbdefaultlangid': None
            , ODMBASEDIREC: None
            ,'localbasedirec': None
            , ODMIMDIREC: None
            , 'odmimdefaultdirec': 'IM/'
            , 'odmimextension': '.dmd'
            , MODELNAME: None
            , 'odmkonfdirec': 'Konfiguration/'
            , 'odmdefdomainsfile': 'defaultdomains.xml'
            , 'odmsettingsfile': 'dl_settings.xml'
            , 'odmdefdomainsfilepath': None
            , 'odmtypesfile': 'types.xml'
            , 'odmstructypesdir':  "datatypes/structuredtype/"
            , 'odmfilesdirec': 'files/'
            , 'odmentitydirec': 'logical/entity/'
            , 'odmrelationdirec': 'logical/relation/'
            , 'odmentisubviewdirec': 'logical/subviews/'
            , 'odmarcdirec': 'logical/arc/'
            , 'odmdocumentdirec': 'businessinfo/document/'
            , 'odmorgunitdirec': 'businessinfo/party/'
            , 'odmudptranslfilename': 'translation'
            , 'odmudpmappingfilename': 'datamapping'
            , 'odmudpelemdisplfilename': 'elementdisplay'
            , 'odmmappingdirec': 'mapping/'
            , 'odmudpfileextension':'.udposdm'
            , 'odmvcsdirec' : 'gitHub/'
            , 'webdirec': None
            , 'webdefaultdirec': 'Web/'
            , 'logofilename': None
            , 'odmreldirec': 'rel/'
            , 'odmtabledirec': 'table/'
            , 'odmdomainsdirec': 'domains/'
            , 'odmsubviewsdirec': 'subviews/'
            , 'odmfkdirec': 'foreignkey/'
            , LOGFILEDIREC: None
            , LOGFILEPATH: None
}
def nvl(p_val1,p_val2=''):
    return p_val1 if p_val1 is not None else p_val2

def nvl2(pval,pvalnull,pvalnnull):
    return pvalnull if pval is None else pvalnnull

def logfilepath(newval:str=None):
    if newval is None:
        return parameter[LOGFILEPATH]
    else:
        parameter[LOGFILEPATH] = newval
def logfiledirec(newval:str=None):
    if newval is None:
        return parameter[LOGFILEDIREC]
    else:
        parameter[LOGFILEDIREC] = newval
def dbFilePath(newval=None):
    if newval is None:
        return parameter['dbfilepath']
    else:
        parameter['dbfilepath'] = newval
def dbDirect(newval=None):
    if newval is None:
        return parameter['dbdirec']
    else:
        parameter['dbdirec'] = newval
def dbFileExtension(newval=None):
    if newval is None:
        return parameter['dbfileextension']
    else:
        parameter['dbfileextension'] = newval
def dbDefaultDirect(newval=None):
    if newval is None:
        return parameter['dbdefaultdirec']
    else:
        parameter['dbdefaultdirec'] = newval
def dbDefaultLang(newval=None):
    if newval is None:
        return parameter[DBDEFAULTLANG]
    else:
        parameter[DBDEFAULTLANG] = newval
def dbLanguages(newval=None):
    if newval is None:
        return parameter[DBLANGUAGES]
    else:
        parameter[DBLANGUAGES] = newval
def dbDefaultLangID(newval=None):
    if newval is None:
        return parameter['dbdefaultlangid']
    else:
        parameter['dbdefaultlangid'] = newval
def odmBaseDirec(newval=None):
    if newval is None:
        return parameter[ODMBASEDIREC]
    else:
        parameter[ODMBASEDIREC] = newval
def odmIMDirec(newval=None):
    if newval is None:
        return parameter[ODMIMDIREC]
    else:
        parameter[ODMIMDIREC] = newval
def odmIMDefaultDirec(newval=None):
    if newval is None:
        return parameter['odmimdefaultdirec']
    else:
        parameter['odmimdefaultdirec'] = newval
def odmIMExtension(newval=None):
    if newval is None:
        return parameter['odmimextension']
    else:
        parameter['odmimextension'] = newval
def odmModelName(newval=None):
    if newval is None:
        return parameter[MODELNAME]
    else:
        parameter[MODELNAME] = newval

def odmsettingsfile(newval=None):
    if newval is None:
        filepath=odmIMDirec()+odmModelName()+'/'+parameter['odmsettingsfile']
        if not os.path.exists(filepath):
            filepath = odmIMDirec() + odmKonfDirec() + parameter['odmsettingsfile']
        return filepath
    else:
        parameter['odmsettingsfile'] = newval
def odmentisubviewdirec(newval=None):
    if newval is None:
        return odmIMDirec()+odmModelName()+'/'+parameter['odmentisubviewdirec']
    else:
        parameter['odmentisubviewdirec'] = newval
def odmKonfDirec(newval=None):
    if newval is None:
        return parameter['odmkonfdirec']
    else:
        parameter['odmkonfdirec'] = newval
def odmVCSDirec(newval=None):
    if newval is None:
        return parameter['odmvcsdirec']
    else:
        parameter['odmvcsdirec'] = newval
def odmdefdomainsfile(newval=None):
    if newval is None:
        return parameter['odmdefdomainsfile']
    else:
        parameter['odmdefdomainsfile'] = newval
def localbasedirec(newval=None):
    if newval is None:
        return parameter['localbasedirec']
    else:
        parameter['localbasedirec'] = newval
def odmdocumentdirec(newval=None):
    if newval is None:
        return odmIMDirec()+odmModelName()+'/'+parameter['odmdocumentdirec']
    else:
        parameter['odmdocumentdirec'] = newval
def odmorgunitdirec(newval=None):
    if newval is None:
        return odmIMDirec()+odmModelName()+'/'+parameter['odmorgunitdirec']
    else:
        parameter['odmorgunitdirec'] = newval
def odmDefDomainsfilePath(newval=None):
    if newval is None:
        return parameter['odmdefdomainsfilepath']
    else:
        parameter['odmdefdomainsfilepath'] = newval
def odmTypesFile(newval=None):
    if newval is None:
        return parameter['odmtypesfile']
    else:
        parameter['odmtypesfile'] = newval
def odmFilesDirec(newval=None):
    if newval is None:
        return odmIMDirec()+odmModelName()+'/'+parameter['odmfilesdirec']
    else:
        parameter['odmfilesdirec'] = newval
def odmstructypesdir(newval=None):
    if newval is None:
        return odmIMDirec()+odmModelName()+'/'+parameter['odmstructypesdir']
    else:
        parameter['odmstructypesdir'] = newval

def odmEntityDirec(newval=None):
    if newval is None:
        return odmIMDirec()+odmModelName()+'/'+parameter['odmentitydirec']
    else:
        parameter['odmentitydirec'] = newval
def odmRelationDirec(newval=None):
    if newval is None:
        return odmIMDirec()+odmModelName()+'/'+parameter['odmrelationdirec']
    else:
        parameter['odmrelationdirec'] = newval
def odmArcDirec(newval=None):
    if newval is None:
        return odmIMDirec()+odmModelName()+'/'+parameter['odmarcdirec']
    else:
        parameter['odmarcdirec'] = newval
def odmUDPTranslFileName(newval=None):
    if newval is None:
        return parameter['odmudptranslfilename']
    else:
        parameter['odmudptranslfilename'] = newval

def odmUDPElemdisplFileName(newval=None):
    if newval is None:
        return parameter['odmudpelemdisplfilename']
    else:
        parameter['odmudpelemdisplfilename'] = newval

def odmmappingdirec(newval=None):
    if newval is None:
        return odmIMDirec()+odmModelName()+'/'+parameter['odmmappingdirec']
    else:
        parameter['odmmappingdirec'] = newval
def odmUDPMappingFileName(newval=None):
    if newval is None:
        return parameter['odmudpmappingfilename']
    else:
        parameter['odmudpmappingfilename'] = newval
def odmUDPFileExtension(newval=None):
    if newval is None:
        return parameter['odmudpfileextension']
    else:
        parameter['odmudpfileextension'] = newval
def webDirec(newval=None):
    if newval is None:
        return parameter['webdirec']
    else:
        parameter['webdirec'] = newval
def webDefaultDirec(newval=None):
    if newval is None:
        return parameter['webdefaultdirec']
    else:
        parameter['webdefaultdirec'] = newval
def logoFileName(newval=None):
    if newval is None:
        return parameter['logofilename']
    else:
        parameter['logofilename'] = newval

def odmtabledirec(newval=None):
    if newval is None:
        return parameter['odmtabledirec']
    else:
        parameter['odmtabledirec'] = newval
def odmdomainsdirec(newval=None):
    if newval is None:
        return odmIMDirec()+odmModelName()+'/'+parameter['odmdomainsdirec']
    else:
        parameter['odmdomainsdirec'] = newval
def odmsubviewsdirec(newval=None):
    if newval is None:
        return parameter['odmsubviewsdirec']
    else:
        parameter['odmsubviewsdirec'] = newval
def odmfkdirec(newval=None):
    if newval is None:
        return parameter['odmfkdirec']
    else:
        parameter['odmfkdirec'] = newval
def odmreldirec(newval=None):
    if newval is None:
        return odmIMDirec()+odmModelName()+'/'+parameter['odmreldirec']
    else:
        parameter['odmreldirec'] = newval

def dbtype(newval=None):
    if newval is None:
        return parameter['dbtype']
    else:
        parameter['dbtype'] = newval
    return
def sqlpath(newval=None):
    if newval is None:
        return parameter['sqlpath']
    else:
        parameter['sqlpath'] = newval
    return
def sqlfilename(newval=None):
    if newval is None:
        return parameter['sqlfilename']
    else:
        parameter['sqlfilename'] = newval
    return
def sqlfilepath():
    return sqlpath()+sqlfilename()+".sql"

def liesparamfile(p_filepath):
    import configparser
    global parameter

    paramfile = configparser.RawConfigParser()
    try:
        paramfile.read(p_filepath)
    except:
        print("parameterfile reading error")
        raise
    # try

    for sect in paramfile.sections():
        #print (sect,paramfile[sect])
        for param in paramfile[sect]:
            val = paramfile[sect][param].strip('"'+"'")
            #print (param,paramfile[sect][param],val)
            #Grundparameter sind speziell
            if param ==ODMBASEDIREC:
                if odmBaseDirec() is None:
                    odmBaseDirec(newval=val)
                else:
                    #wurde schon gesetzt, muss gleich sein
                    if (val is not None)\
                        and (val != odmBaseDirec()):
                        raise Exception("Base-direc mismatch '{}' and '{}'".format (val, odmBaseDirec()))
                    #fi
                #fi
            elif param == DBDEFAULTLANG:
                dbDefaultLang(val)
            elif param == DBLANGUAGES:
                dbLanguages(val)
            elif param ==ODMIMDIREC:
                if odmIMDirec() is None:
                    odmIMDirec(newval=val)
                else:
                    # wurde schon gesetzt, muss gleich sein
                    if (val is not None) \
                            and (val != odmIMDirec()):
                        raise Exception(
                            "IM-Direc mismatch '{}' and '{}'".format(val, odmIMDirec()))
                    #fi
                #fi
            elif param ==MODELNAME:
                if odmModelName() is None:
                    odmModelName(newval=val)
                else:
                    # wurde schon gesetzt, muss gleich sein
                    if (val is not None) \
                            and (val != odmModelName()):
                        raise Exception(
                            "Model name mismatch '{}' and '{}'".format(val, odmModelName()))
                    #fi
                #fi
            else:
                parameter[param] = val
            #fi
        #for
    #for
    """
    basedirec is special, default  is the directory of the loaded parameter file 
    """
    if odmBaseDirec() is None:
        odmBaseDirec(newval=os.path.dirname(os.path.realpath(p_filepath))+'/')


#liesparamfile

def filldefaultparams():
    if localbasedirec() is None:
        localbasedirec(newval=odmBaseDirec())
    if odmIMDirec() is None:
        odmIMDirec(newval=odmBaseDirec() + odmIMDefaultDirec())
    if dbDirect() is None:
        dbDirect(newval=localbasedirec()+dbDefaultDirect())
    if dbFilePath() is None:
        dbFilePath(newval=dbDirect()+odmModelName()+dbFileExtension())
    if odmDefDomainsfilePath() is None:
        odmDefDomainsfilePath(newval=odmIMDirec() + odmKonfDirec() + odmdefdomainsfile())
    if webDirec() is None:
        webDirec(newval=localbasedirec()+webDefaultDirec())
    if logfiledirec() is None:
        logfiledirec(localbasedirec())
    if logfilepath() is None:
        logfilepath(logfiledirec()+odmModelName()+'.log')


#filldefaultparams

def suche1file(p_direc,p_pattern='.*'):
    lretval = None
    dmdfiles = []
    try:
        dmdfiles = [f for f in os.listdir(p_direc) if re.match(p_pattern + re.escape(odmIMExtension()), f)]
    except:
        pass
    #fi
    if (len(dmdfiles) == 1):
        lretval =  re.sub(odmIMExtension(), '', dmdfiles[0])
    elif (len(dmdfiles) == 0):
        pass # to be handled by caller
    else:
        raise Exception("more than 1 model found in {}".format(p_direc))
    # fi
    return lretval
#suche1file

def suchemodelname(p_direc):
    # nimm den Namen des einzigen .dmd-Files im aktuellen, im IM/, im gitHub/IM-Directory
    immodelname = suche1file(p_direc=p_direc)
    if immodelname is not None:
        imdirectory = p_direc
    else:
        testdirec = p_direc+odmIMDefaultDirec()
        immodelname = suche1file(p_direc=testdirec)
        if immodelname is not None:
            imdirectory = testdirec
        else:
            """search in the vcs directory"""
            testdirec = p_direc+odmVCSDirec()+odmIMDefaultDirec()
            immodelname = suche1file(p_direc=testdirec)
            if (immodelname is not None):
                imdirectory = testdirec
            else:
                raise Exception ("No model found in {}...".format(p_direc))
            #fi
        #fi
    #fi
    return (imdirectory,immodelname)
#suchemodelname

def initparam(p_callarg):
    global parameter

    my_file = Path(p_callarg)
    if my_file.is_file():
        #file gegeben, lies dieses
        paramfile = p_callarg
    elif my_file.is_dir():
        if (p_callarg[-1] != '/'):
            p_callarg = p_callarg + '/'
        #Verzeichnis gegeben, suche ein Modell und dann ein Parameterfile
        (imdirec,modelname) = suchemodelname(p_direc=p_callarg)
        odmIMDirec(newval=imdirec)
        odmBaseDirec(newval=imdirec[0:len(imdirec)-len(odmIMDefaultDirec())] if (imdirec.split('/')[-2]+'/' == odmIMDefaultDirec()) else imdirec)
        odmModelName(newval=modelname)
        paramfile = p_callarg + modelname + paramFileExension
    else:
        print (my_file)
        raise Exception("parameter is neither file nor directory")
    if os.path.exists(paramfile):
        liesparamfile(p_filepath = paramfile)
    elif ((odmIMDirec() is None) or (odmModelName() is None)):
        #check for minimal information
        raise Exception('No parameter file and no model found in "{}"'.format(p_callarg))
    #fi
    filldefaultparams()
#end initparam