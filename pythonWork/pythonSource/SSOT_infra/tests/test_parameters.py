import os
import tempfile
from SSOT_infra import parameters

TESTMODELNAME='TEST_DMD'


def makefile(pfilename, pcontent=["gugus"]):
    with open(pfilename, 'w+') as f:
        for l in pcontent: f.write(l)
        f.close()
    return


def test_lookfor1file():
    #init pparameter global variable
    parameters.parameterdefaults()

    with tempfile.TemporaryDirectory() as basedirec:
        assert parameters.lookfor1file(p_direc=basedirec) is None, f"nonexisting DMD found in {basedirec}"
        direc = basedirec +'/' + parameters.odmIMDefaultDirec()

        os.mkdir(direc)
        makefile(pfilename=direc +TESTMODELNAME + parameters.odmIMExtension())

        assert parameters.lookfor1file(p_direc=direc) == TESTMODELNAME,f"no {TESTMODELNAME}.dmd in {direc}"

        #erzeuge ein 2. DMD im selben Directory
        makefile(pfilename=direc + 'TEST_DMD2' + parameters.odmIMExtension())
        try:
            parameters.lookfor1file(p_direc=direc)
            assert False,f"more than one file in {direc}"
        except:
            pass
    #with
    return

def test_lookformodelname():
    #init pparameter global variable
    parameters.parameterdefaults()

    with tempfile.TemporaryDirectory() as basedirec:
        direc = basedirec
        try:
            lookformodelname(p_direc=direc)
            assert False,f"find nonexisting file in {direc}"
        except:
            pass
        direc = basedirec + '/' + parameters.odmIMDefaultDirec()
        os.mkdir(direc)
        firstfile=direc + TESTMODELNAME + parameters.odmIMExtension()
        makefile(pfilename = firstfile)
        (imdirectory, immodelname) = parameters.lookformodelname(p_direc=direc)
        assert immodelname == TESTMODELNAME,f"T{ESTMODELNAME}.dmd not found in {direc} with lookformodelname"
        assert imdirectory == direc,f"{direc} not found in lookformodelname"
        os.remove(firstfile)
        os.rmdir(direc)

        os.mkdir(basedirec + '/' + parameters.odmVCSDirec())
        direc = basedirec + '/' + parameters.odmVCSDirec() + parameters.odmIMDefaultDirec()
        os.mkdir(direc)
        firstfile=direc + TESTMODELNAME + parameters.odmIMExtension()
        makefile(pfilename=firstfile)
        (imdirectory, immodelname) = parameters.lookformodelname(p_direc=direc)
        assert immodelname == TESTMODELNAME,f"{TESTMODELNAME}.dmd not found in {direc} with lookformodelname"
        assert imdirectory == direc,f"{direc} not found in lookformodelname"

        secondfile=direc + 'TEST_DMD2' + parameters.odmIMExtension()
        makefile(pfilename=secondfile)
        try:
            (imdirectory, immodelname) = parameters.lookformodelname(p_direc=direc)
            assert False,f"2 dmd-files in {direc} not recognized with lookformodelname"
        except:
            pass
    #with
    return

def test_initparam():
    with tempfile.TemporaryDirectory() as basedirec:
        direc = basedirec + '/' + 'IM/'
        os.mkdir(direc)
        dmdfile = direc + TESTMODELNAME+ '.dmd'
        makefile(pfilename=dmdfile)
        #one Modell, nonexistent  param file, everything default
        parameters.initparam(p_callarg=basedirec + '/')
        assert parameters.modelName() == TESTMODELNAME, f"wrong modelname"
        assert parameters.odmIMDirec() == direc, f"wrong IMdirec"
        assert parameters.baseDirec() ==  basedirec + '/', f"wrong baseDirec"
        assert parameters.dbDirect() == basedirec + '/' + parameters.dbDefaultDirect(), f"wrong dbDirec"
        assert parameters.dbFilePath() == basedirec + '/' + parameters.dbDefaultDirect() + TESTMODELNAME + parameters.dbFileExtension(), f"wrong dbFilePath"
        assert parameters.webDirec() == basedirec + '/' + parameters.webDefaultDirec(), f"wrong webDirec"
        assert parameters.odmDefDomainsfilePath() == direc + parameters.odmKonfDirec()+'defaultdomains.xml', f"wrong odmDomainsFilePath"


        #Test mit Parameterfile implizit gerufen
        paramfile = basedirec +'/' + TESTMODELNAME + parameters.PARAMFILEEXTENSION
        makefile(pfilename=paramfile,pcontent=[
            '[ODM]]\n',
            '#base directory for all model data (with ending /)\n',
            f'odmIMDirec = "{direc}"\n',
            '#model name\n',
            '#default: single .dmd file in <odmIMDirec> or <odmIMDirec>/IM or <odmIMDirec>/github/IM\n',
            f'#modelName = "{TESTMODELNAME}"\n',
            '[DB]]\n',
            '#default language of model in DB\n',
            'dbDefaultLang =  "de"\n'
        ])
        parameters.initparam(p_callarg=basedirec + '/')
        assert parameters.baseDirec() == basedirec + '/',"falsches base Direc"
        assert parameters.odmIMDirec() == basedirec + '/' + parameters.odmIMDefaultDirec(), "falsches IM Direc"
        assert parameters.dbDefaultLang() == 'de', "falsche Language {} {}"
        os.remove(paramfile)

        paramfile = basedirec +'/' + TESTMODELNAME + parameters.PARAMFILEEXTENSION
        makefile(pfilename=paramfile,pcontent=[
            '[ODM]]\n',
            '#base directory for all model data (with ending /)\n',
            '#odmIMDirec = ""\n'  # freischalten für zu exception
            'baseDirec = "basedirec"\n'  # freischalten für zu exception
            '#model name\n',
            '#default: single .dmd file in <odmIMDirec> or <odmIMDirec>/IM or <odmIMDirec>/github/IM\n',
            'modelName = "TEST_DMDxx"\n'  # freischalten für zu exception
            '[DB]\n',
            '#default language of model in DB\n',
            'dbDefaultLang =  "de"\n',
        ])
        try:
            parameters.initparam(p_callarg=basedirec + '/')
            assert False,"exception expected"
        except:
            pass
        os.remove(paramfile)
    return


def setUp(self):
    pass

def tearDown(self):
    pass
    #print ("tearDown")
