# -*- coding: latin-1 -*-
import os
import re

imDirectory:str = ''
imModelName:str = ''
imKonfDirectory:str = 'Konfiguration/'
imDomainsFile:str = 'defaultdomains.xml'
imTypesFile:str = 'types.xml'
imFilesDirec:str = imDirectory+imModelName+'/files/'
imEntityDirec:str = imDirectory+imModelName+'/logical/entity/'
imRelationDirec:str = imDirectory+imModelName+'/logical/relation/'
imArcDirec:str = imDirectory+imModelName+'/logical/arc/'
imTranslationFileName:str = 'translation'

def suche1File(direc,pattern):
    lretval = None
    dmdfiles = []
    try:
        dmdfiles = [f for f in os.listdir(direc) if re.match(pattern + '\.dmd', f)]
    except:
        pass
    #fi
    if (len(dmdfiles) == 1):
        lretval =  re.sub('.dmd', '', dmdfiles[0])
    elif (len(dmdfiles) == 0):
        pass
    else:
        print("Mehrere Modelle gefunden in {}".format(direc))
    # fi
    return lretval
#sucheFile

def initODMParam(pimDirec = None , pmodelName  = None, pDomainsFile = None):
    global imDirectory
    global imModelName
    global imKonfDirectory
    global imDomainsFile
    global imEntityDirec
    global imFilesDirec
    global imRelationDirec
    global imArcDirec

    imDirectory = pimDirec if (pimDirec  is not None) else imDirectory

    # nimm den Namen des einzigen .dmd-Files im aktuellen, im IM/, im gitHub/IM-Directory
    imModelName = suche1File(direc=imDirectory,pattern= '.*' if (pmodelName is None) else pmodelName)
    if imModelName is None:
        imModelName = suche1File(direc=imDirectory.__str__()+'IM/', pattern='.*')
        if imModelName is None:
            imModelName = suche1File(direc=imDirectory.__str__()+'gitHub/IM/', pattern='.*')
            if (imModelName is None):
                print("Kein Modell gefunden in {}".format(imDirectory.__str__()+'...'))
            else:
                imDirectory += 'gitHub/IM/'
            #fi
        else:
            imDirectory += 'IM/'
        #fi
    #fi
    imFilesDirec = imDirectory + imModelName + '/files/'
    imEntityDirec = imDirectory + imModelName + '/logical/entity/'
    imRelationDirec = imDirectory + imModelName + '/logical/relation/'
    imArcDirec = imDirectory + imModelName + '/logical/arc/'

    imDomainsFile  = pDomainsFile if (pDomainsFile  is not None) else imDomainsFile

#end initODMParam

# with open(filename) as fh:
# ...     commands = dict(re.findall(r'(\S+)\s+(.+)', fh.read()))
# ...
# >>> print(json.dumps(commands, indent=2, sort_keys=True))
