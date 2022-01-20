import os
import unittest
import tempfile
from SSOT_infra import parameters

TESTMODELNAME='TEST_DMD'

class test_parameters(unittest.TestCase):

    def makefile(self,pfilename, pcontent=["gugus"]):
        with open(pfilename, 'w+') as f:
            for l in pcontent: f.write(l)
            f.close()
        return

# def test_lookfor1file():
#     return
#     #init parameter global variable
#     parameters.parameterdefaults()
#
#     with tempfile.TemporaryDirectory() as basedirec:
#         assert parameters.lookfor1file(p_direc=basedirec) is None, f"nonexisting DMD found in {basedirec}"
#         direc = os.path.join(basedirec ,parameters.odmIMDefaultDirec())
#
#         os.mkdir(direc)
#         makefile(pfilename=os.path.join (direc ,TESTMODELNAME + parameters.odmIMExtension()))
#
#         assert parameters.lookfor1file(p_direc=direc) == TESTMODELNAME,f"no {TESTMODELNAME}.dmd in {direc}"
#
#         #erzeuge ein 2. DMD im selben Directory
#         makefile(pfilename=or.path.join(direc, 'TEST_DMD2' + parameters.odmIMExtension()))
#         try:
#             parameters.lookfor1file(p_direc=direc)
#             assert False,f"more than one file in {direc}"
#         except:
#             pass
#     #with
#     return

# def test_lookformodelname():
#     #init parameter global variable
#     parameters.parameterdefaults()
#
#     with tempfile.TemporaryDirectory() as basedirec:
#         direc = basedirec
#         try:
#             lookformodelname(p_direc=direc)
#             assert False,f"find nonexisting file in {direc}"
#         except:
#             pass
#         direc = basedirec + '/' + parameters.odmIMDefaultDirec()
#         os.mkdir(direc)
#         firstfile=direc + TESTMODELNAME + parameters.odmIMExtension()
#         makefile(pfilename = firstfile)
#         (imdirectory, immodelname) = parameters.lookformodelname(p_direc=direc)
#         assert immodelname == TESTMODELNAME,f"T{ESTMODELNAME}.dmd not found in {direc} with lookformodelname"
#         assert imdirectory == direc,f"{direc} not found in lookformodelname"
#         os.remove(firstfile)
#         os.rmdir(direc)
#
#         os.mkdir(basedirec + '/' + parameters.odmVCSDirec())
#         direc = basedirec + '/' + parameters.odmVCSDirec() + parameters.odmIMDefaultDirec()
#         os.mkdir(direc)
#         firstfile=direc + TESTMODELNAME + parameters.odmIMExtension()
#         makefile(pfilename=firstfile)
#         (imdirectory, immodelname) = parameters.lookformodelname(p_direc=direc)
#         assert immodelname == TESTMODELNAME,f"{TESTMODELNAME}.dmd not found in {direc} with lookformodelname"
#         assert imdirectory == direc,f"{direc} not found in lookformodelname"
#
#         secondfile=direc + 'TEST_DMD2' + parameters.odmIMExtension()
#         makefile(pfilename=secondfile)
#         try:
#             (imdirectory, immodelname) = parameters.lookformodelname(p_direc=direc)
#             assert False,f"2 dmd-files in {direc} not recognized with lookformodelname"
#         except:
#             pass
#     #with
#     return

    def test_initparam(self):
        with self.assertRaises(Exception):
            parameters.initparam()

        #modelname olny
        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            currentDirec = os.getcwd()
            parameters.initparam(pbasedirec=currentDirec, pmodelname=TESTMODELNAME)
            self.assertEqual(currentDirec,parameters.baseDirec())
            self.assertEqual(os.path.join(currentDirec,'IM'),parameters.odmIMDirec())
            self.assertEqual(os.path.join(currentDirec,'DB'),parameters.dbDirect())
            self.assertEqual(os.path.join(currentDirec,'DB',TESTMODELNAME+'.db'),parameters.dbFilePath())
            self.assertEqual(os.path.join(currentDirec,'Web'),parameters.webDirec())
            self.assertEqual(os.path.join(currentDirec),parameters.logfiledirec())
            self.assertEqual(os.path.join(currentDirec,TESTMODELNAME+'.log'),parameters.logfilepath())
            self.assertEqual('en',parameters.dbDefaultLang())
            self.assertEqual('en',parameters.dbLanguages())

            #some other parameters
            with self.assertRaises(Exception):
                parameters.initparam(pbasedirec=currentDirec,pmodelname=TESTMODELNAME,pmodellang='xx')
            with self.assertRaises(Exception) :
                parameters.initparam(pbasedirec=currentDirec,pmodelname=TESTMODELNAME,planguages='xx,es')

            parameters.initparam(pbasedirec=currentDirec,pmodelname=TESTMODELNAME,pmodellang='de',planguages='es')
            self.assertEqual('de',parameters.dbDefaultLang())
            self.assertEqual('es',parameters.dbLanguages())

            parameters.initparam(pbasedirec=currentDirec,pmodelname=TESTMODELNAME,pmodelfilepath='a.b')
            self.assertEqual(os.path.join(currentDirec),parameters.odmIMDirec())

            os.mkdir(os.path.join(tempdir,'IM'))
            parameters.initparam(pbasedirec=currentDirec,pmodelname=TESTMODELNAME,pmodelfilepath='IM/a.b')
            self.assertEqual(os.path.join(currentDirec,'IM'),parameters.odmIMDirec())

            parameters.initparam(pbasedirec=currentDirec,pmodelname=TESTMODELNAME,pmodelfilepath='IM/a.b')
            self.assertEqual(os.path.join(currentDirec,'IM'),parameters.odmIMDirec())

            parameters.initparam(pbasedirec=currentDirec,pmodelname=TESTMODELNAME,pmodellang='de',planguages='es,en,it,de')
            self.assertEqual('de',parameters.dbDefaultLang())
            self.assertEqual('es,en,it,de',parameters.dbLanguages())

            currentDirec = os.getcwd()
            parameters.initparam(pbasedirec=currentDirec,pmodelname=TESTMODELNAME,pdbfile=os.path.join(currentDirec,'foo.db'),plogfilepath=os.path.join(currentDirec,'foo.logg'))
            self.assertEqual(currentDirec,parameters.baseDirec())
            self.assertEqual(os.path.join(currentDirec,'IM'),parameters.odmIMDirec())
            self.assertEqual(os.path.join(currentDirec),parameters.dbDirect())
            self.assertEqual(os.path.join(currentDirec,'foo.db'),parameters.dbFilePath())
            self.assertEqual(os.path.join(currentDirec,'Web'),parameters.webDirec())
            self.assertEqual(os.path.join(currentDirec),parameters.logfiledirec())
            self.assertEqual(os.path.join(currentDirec,'foo.logg'),parameters.logfilepath())

        with tempfile.TemporaryDirectory() as tempdir:
            #Test mit Parameterfile implizit gerufen
            os.chdir(tempdir)
            currentDirec = os.getcwd()
            paramfile = os.path.join(currentDirec,TESTMODELNAME + parameters.PARAMFILEEXTENSION)
            self.makefile(pfilename=paramfile
                     ,pcontent=[
                '[ODM]\n',
                f'modelName = "{TESTMODELNAME}"\n',
                '#base directory for all model data\n',
                f'#odmIMDirec = "{None}"\n',
                '#model name\n',
                '[DB]\n',
                '#default language of model in DB\n',
                'dbDefaultLang =  "de"\n',
                'dblanguages =  "de,fr"\n'
                ])
            parameters.initparam(pbasedirec=currentDirec,pparamfile=paramfile)
            self.assertEqual(currentDirec, parameters.baseDirec())
            self.assertEqual(os.path.join(currentDirec, 'IM'), parameters.odmIMDirec())
            self.assertEqual(os.path.join(currentDirec, 'DB'), parameters.dbDirect())
            self.assertEqual(os.path.join(currentDirec, 'DB', TESTMODELNAME + '.db'), parameters.dbFilePath())
            self.assertEqual(os.path.join(currentDirec, 'Web'), parameters.webDirec())
            self.assertEqual(os.path.join(currentDirec), parameters.logfiledirec())
            self.assertEqual(os.path.join(currentDirec, TESTMODELNAME + '.log'), parameters.logfilepath())
            self.assertEqual('de', parameters.dbDefaultLang())
            self.assertEqual('de,fr', parameters.dbLanguages())
            #same paramfile called with both modelname in parameter
            parameters.initparam(pbasedirec=currentDirec,pmodelname=TESTMODELNAME,pparamfile=paramfile)
            self.assertEqual(currentDirec, parameters.baseDirec())
            self.assertEqual(os.path.join(currentDirec, 'IM'), parameters.odmIMDirec())
            self.assertEqual(os.path.join(currentDirec, 'DB'), parameters.dbDirect())
            self.assertEqual(os.path.join(currentDirec, 'DB', TESTMODELNAME + '.db'), parameters.dbFilePath())
            self.assertEqual(os.path.join(currentDirec, 'Web'), parameters.webDirec())
            self.assertEqual(os.path.join(currentDirec), parameters.logfiledirec())
            self.assertEqual(os.path.join(currentDirec, TESTMODELNAME + '.log'), parameters.logfilepath())
            self.assertEqual('de', parameters.dbDefaultLang())
            self.assertEqual('de,fr', parameters.dbLanguages())
            os.remove(paramfile)

            paramfile = os.path.join(currentDirec,TESTMODELNAME + parameters.PARAMFILEEXTENSION)
            self.makefile(pfilename=paramfile
                     ,pcontent=[
                '[ODM]\n',
                f'modelName = "{TESTMODELNAME}"\n',
                f"""odmIMDirec = "{os.path.join(currentDirec, 'gitHub','IM')}"\n""",
                f"""dbdirec = "{os.path.join(currentDirec, 'DB2')}"\n""",
                '[DB]\n',
                '#default language of model in DB\n',
                'logfilepath="./logfiles/speciallog.log"\n',
                ])
            parameters.initparam(pbasedirec=currentDirec,pparamfile=paramfile)
            self.assertEqual(currentDirec, parameters.baseDirec())
            self.assertEqual(os.path.join(currentDirec,'gitHub','IM'), parameters.odmIMDirec())
            self.assertEqual(os.path.join(currentDirec, 'DB2'), parameters.dbDirect())
            self.assertEqual(os.path.join(currentDirec, 'DB2', TESTMODELNAME + '.db'), parameters.dbFilePath())
            self.assertEqual(os.path.join(currentDirec, 'Web'), parameters.webDirec())
            self.assertEqual(os.path.join(currentDirec,'logfiles'), parameters.logfiledirec())
            self.assertEqual(os.path.join(currentDirec,'logfiles','speciallog.log'), parameters.logfilepath())
            os.remove(paramfile)


            paramfile = os.path.join(currentDirec, TESTMODELNAME + parameters.PARAMFILEEXTENSION)
            self.makefile(pfilename=paramfile
                          , pcontent=[
                    """[ODM]
                    #base directory for all modeler data (with ending /)
                    odmbasedirec = "gitHub"
                    
                    #base directory for odm-model-files (with ending /)
                    #odmimdirec = 
                    
                    #model name   
                    odmmodelname = "ModellModell_neu"
                    
                    #directory containing odm-configuration-files (below odmIMDirec)
                    #odmkonfdirec = "Konfiguration"
                    
                    [DB]
                    #default language of model in DB
                    dbdefaultlang = "en"
                    
                    #comma separated languages to be maintained, choose from de, en, fr, es
                    dblanguages = "de,en"
                    
                    #directory containing DB-file (with ending /)
                    dbdirec = "gitHub/DB"
                    
                    #directory for web-source output
                    #default <localbasedirec> <webDefaultDirec>
                    webdirec = "Web"
                    
                    #filename of logo in Webpage (path webdirec/image/)
                    logofilename = "logo.jpg"
                """
                ])
            with self.assertRaises(Exception):
                parameters.initparam(pbasedirec=currentDirec, pparamfile=paramfile)
            os.remove(paramfile)

            paramfile = os.path.join(currentDirec, TESTMODELNAME + parameters.PARAMFILEEXTENSION)
            self.makefile(pfilename=paramfile
                          , pcontent=[
                    """[ODM]
                    #base directory for all modeler data 
                    #basedirec = ""

                    #base directory for odm-model-files 
                    odmimdirec = "gitHub/IM"  

                    #model name   =========ERROR in ModelnameField "odm" is obsolete
                    modelname = "ModellModell_neu"

                    #directory containing odm-configuration-files (below odmIMDirec)
                    #odmkonfdirec = "Konfiguration"

                    [DB]
                    #default language of model in DB
                    dbdefaultlang = "en"

                    #comma separated languages to be maintained, choose from de, en, fr, es
                    dblanguages = "de,en"

                    #directory containing DB-file (with ending /)
                    dbdirec = "gitHub/DB"

                    #directory for web-source output
                    #default <localbasedirec> <webDefaultDirec>
                    webdirec = "Web"
                    
                    logfiledirec = ".."        
                                 
                    #filename of logo in Webpage (path webdirec/image/)
                    logofilename = "logo.jpg"
                """
                ])
            parameters.initparam(pbasedirec=currentDirec, pparamfile=paramfile)
            self.assertEqual(parameters.modelName(),"ModellModell_neu")
            self.assertEqual(parameters.baseDirec(),currentDirec)
            self.assertEqual(parameters.logfiledirec(),os.path.dirname(currentDirec))
            self.assertEqual(parameters.odmIMDirec(),currentDirec + "/gitHub/IM")
            os.remove(paramfile)
        return


    def setUp(self):
        pass

    def tearDown(self):
        pass
