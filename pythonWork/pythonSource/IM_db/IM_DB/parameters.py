import os,re
from pathlib  import Path

""" Sammlung aller Parameter für die Verwaltung der Datenbank und aller Tools"""
MODELNAME:str = 'odmmodelname'
ODMIMDIREC:str = 'odmimdirec'
ODMBASEDIREC:str = 'odmbasedirec'

paramFileExension:str = ".params"
parameter = {
              'dbfilepath': None
            , 'dbdirec' : None
            , 'dbfileextension' : '.db'
            , 'dbdefaultdirec':'DB/'
            , 'dbdefaultlang': 'de'
            , 'dblanguages' : 'de,en'
            , 'dbdefaultlangid': None
            , ODMBASEDIREC: None
            ,'localbasedirec': None
            , ODMIMDIREC: None
            , 'odmimdefaultdirec': 'IM/'
            , 'odmimextension': '.dmd'
            , MODELNAME: None
            , 'odmkonfdirec': 'Konfiguration/'
            , 'odmdomainsfile': 'defaultdomains.xml'
            , 'odmsettingsfile': 'dl_settings.xml'
            , 'odmdomainsfilepath': None
            , 'odmtypesfile': 'types.xml'
            , 'odmstructypesdir':  "datatypes/structuredtype/"
            , 'odmfilesdirec': 'files/'
            , 'odmentitydirec': 'logical/entity/'
            , 'odmrelationdirec': 'logical/relation/'
            , 'odmentisubviewdirec': 'logical/subviews/'
            , 'odmarcdirec': 'logical/arc/'
            , 'odmdocumentdirec': 'businessinfo/document/'
            , 'odmudptranslfilename': 'translation'
            , 'odmudpmappingfilename': 'datamapping'
            , 'odmudpfileextension':'.udposdm'
            , 'odmvcsdirec' : 'gitHub/'
            , 'webdirec': None
            , 'webdefaultdirec': 'Web/'
            , 'logofilename': None
        }
def nvl(p_val1,p_val2):
    return p_val1 if p_val1 is not None else p_val2

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
        return parameter['dbdefaultlang']
    else:
        parameter['dbdefaultlang'] = newval
def dbLanguages(newval=None):
    if newval is None:
        return parameter['dblanguages']
    else:
        parameter['dblanguages'] = newval
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
def odmDomainsFile(newval=None):
    if newval is None:
        return parameter['odmdomainsfile']
    else:
        parameter['odmdomainsfile'] = newval
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
def odmDomainsFilePath(newval=None):
    if newval is None:
        return parameter['odmdomainsfilepath']
    else:
        parameter['odmdomainsfilepath'] = newval
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

def liesparamfile(p_filepath):
    import configparser
    global parameter

    paramfile = configparser.RawConfigParser()
    try:
        paramfile.read(p_filepath)
    except:
        print("parameterfile reading error")
        raise

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
    if odmDomainsFilePath() is None:
        odmDomainsFilePath(newval=odmIMDirec()+odmKonfDirec()+odmDomainsFile())
    if webDirec() is None:
        webDirec(newval=localbasedirec()+webDefaultDirec())
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
        raise Exception("parameter is neither file nor directory")
    if os.path.exists(paramfile):
        liesparamfile(p_filepath = paramfile)
    elif ((odmIMDirec() is None) or (odmModelName() is None)):
        #check for minimal information
        raise Exception('No parameter file and no model found in "{}"'.format(p_callarg))
    #fi
    filldefaultparams()
#end initparam