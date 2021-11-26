import unittest
import os
import tempfile
from SSOT_infra import parameters


class ParameterTest(unittest.TestCase):

    def test_suche1file(self):
        with tempfile.TemporaryDirectory() as basedirec:
            #os.mkdir(basedirec )
            direc= basedirec
            self.assertIsNone (parameters.suche1file(p_direc=direc, p_pattern='.*')
                               , msg="doch ein DMD in "+direc)

        with tempfile.TemporaryDirectory() as basedirec:
            #os.mkdir(basedirec )
            direc = basedirec +'/' + parameters.odmIMDefaultDirec()
            os.mkdir(direc)
            with open(direc +'TEST_DMD' + parameters.odmIMExtension(), 'w+') as f:
                f.write("gugus")
            self.assertIsNone(parameters.suche1file(p_direc=direc, p_pattern='xyzGUgus')
                              , msg="es gibt ein xyzGUgus.dmd "+direc)
            self.assertEqual (parameters.suche1file(p_direc=direc
                                                    , p_pattern='TEST_DMD')
                              ,'TEST_DMD'
                              , msg="kein TEST_DMD.dmd in "+direc
                              )
            self.assertEqual (parameters.suche1file(p_direc=direc
                                                    , p_pattern='.*')
                              ,'TEST_DMD'
                              , msg="kein TEST_DMD.dmd in "+direc
                              )
            self.assertEqual (parameters.suche1file(p_direc=direc)
                              ,'TEST_DMD'
                              , msg="kein TEST_DMD.dmd in "+direc
                              )

            #erzeuge ein 2. DMD im selben Directory
            with open(direc + 'TEST_DMD2' + parameters.odmIMExtension(), 'w+') as f:
                f.write("gugus")
            with self.assertRaises(Exception
                                ,msg="Nur 1 DMD in "+direc):
                parameters.suche1file(p_direc=direc
                                      , p_pattern='.*')
            self.assertEqual(parameters.suche1file(p_direc=direc
                                                   , p_pattern='TEST_DMD2')
                             ,'TEST_DMD2'
                             , msg="explizites file nicht gefunden "+direc)
    #suche1file

    def test_suchemodelname(self):
        with tempfile.TemporaryDirectory() as basedirec:
            # os.mkdir(basedirec )
            direc = basedirec
            with self.assertRaises(Exception
                                ,msg="Doch ein Modell in"+ direc):
                suchemodelname(p_direc=direc)

            direc = basedirec + '/' + parameters.odmIMDefaultDirec()
            os.mkdir(direc)
            dmdfile = direc + 'TEST_DMD' + parameters.odmIMExtension()
            with open(dmdfile, 'w+') as f:
                f.write("gugus")
            self.assertEqual(parameters.suchemodelname(p_direc=direc)
                             , (direc,'TEST_DMD')
                             , msg="kein TEST_DMD.dmd in " + direc
                             )
            self.assertEqual(parameters.suchemodelname(p_direc=basedirec + '/')
                             , (direc,'TEST_DMD')
                             , msg="kein TEST_DMD.dmd in " + basedirec + " and below"
                             )
            os.remove(dmdfile)
            os.rmdir(direc)

            os.mkdir(basedirec + '/' + parameters.odmVCSDirec())
            direc = basedirec + '/' + parameters.odmVCSDirec() + parameters.odmIMDefaultDirec()
            os.mkdir(direc)

            with open(direc + 'TEST_DMD' + parameters.odmIMExtension(), 'w+') as f:
                f.write("gugus")

            self.assertEqual(parameters.suchemodelname(p_direc=basedirec + '/')
                             , (direc,'TEST_DMD')
                             , msg="kein TEST_DMD.dmd in " + direc
                             )

            with open(direc + 'TEST_DMD2' + parameters.odmIMExtension(), 'w+') as f:
                f.write("gugus")
            with self.assertRaises(Exception
                   , msg="Nur 1 DMD in " + direc):
                suchemodelname(p_direc=direc)

    #suchemodellname

    def test_initparam(self):
        with tempfile.TemporaryDirectory() as basedirec:
            direc = basedirec + '/' + parameters.odmIMDefaultDirec()
            os.mkdir(direc)
            dmdfile = direc + 'TEST_DMD' + parameters.odmIMExtension()
            with open(dmdfile, 'w+') as f:
                f.write("gugus")
            #one Modell, nonexistent  param file, everything default
            parameters.initparam(p_callarg=basedirec + '/')
            self.assertEqual(parameters.modelName(), 'TEST_DMD', msg="falscher modellname")
            self.assertEqual(parameters.odmIMDirec(), direc, msg="falsches IM-Verzeichnis")
            self.assertEqual(parameters.baseDirec(), basedirec + '/', msg="falsches base-Verzeichnis")
            self.assertEqual(parameters.dbDirect(), basedirec + '/' + parameters.dbDefaultDirect()
                             , msg="falsches DBverzeichnis")
            self.assertEqual(parameters.dbFilePath(), basedirec + '/' + parameters.dbDefaultDirect() + 'TEST_DMD' + parameters.dbFileExtension()
                             , msg="falsches DBverzeichnis")
            self.assertEqual(parameters.webDirec(), basedirec + '/' + parameters.webDefaultDirec()
                             , msg="falsches web verzeichnis")
            self.assertEqual(parameters.odmDomainsFilePath(), basedirec + '/' + parameters.odmKonfDirec() + parameters.odmDomainsFile()
                             , msg="falscher domainfilepath ")

            #Test mit Parameterfile implizit gerufen
            paramfile = basedirec +'/' + 'TEST_DMD' + parameters.PARAMFILEEXTENSION
            with open(paramfile, 'w+') as f:
                f.write('[ODM]]\n')
                f.write('#base directory for all model data (with ending /)\n')
                f.write('odmIMDirec = "{}"\n'.format(direc))
                f.write('#model name\n')
                f.write('#default: single .dmd file in <odmIMDirec> or <odmIMDirec>/IM or <odmIMDirec>/github/IM\n')
                f.write('#modelName = "{}"\n'.format('TEST_DMD'))
                f.write('[DB]]\n')
                f.write('#default language of model in DB\n')
                f.write('dbDefaultLang =  "de"\n')
            parameters.initparam(p_callarg=basedirec + '/')
            self.assertEqual(parameters.baseDirec(), basedirec + '/', msg="falsches base Direc")
            self.assertEqual(parameters.odmIMDirec(), basedirec + '/' + parameters.odmIMDefaultDirec()
                             , msg="falsches IM Direc")
            self.assertEqual(parameters.dbDefaultLang(), 'de', msg="falsche Language {} {}")
            os.remove(paramfile)

            paramfile = basedirec +'/' + 'TEST_DMD' + parameters.PARAMFILEEXTENSION
            with open(paramfile, 'w+') as f:
                f.write('[ODM]]\n')
                f.write('#base directory for all model data (with ending /)\n')
                f.write('#odmIMDirec = ""\n'.format('direc'))  #freischalten für zu exception
                f.write('#baseDirec = "{}"\n'.format('basedirec')) #freischalten für zu exception
                f.write('#model name\n')
                f.write('#default: single .dmd file in <odmIMDirec> or <odmIMDirec>/IM or <odmIMDirec>/github/IM\n')
                f.write('modelName = "{}"\n'.format('TEST_DMDxx'))  #freischalten für zu exception
                f.write('[DB]]\n')
                f.write('#default language of model in DB\n')
                f.write('dbDefaultLang =  "de"\n')
            try:
                parameters.initparam(p_callarg=basedirec + '/')
                self.assertTrue(False,msg="hier darf er nicht landen")
            except:
                self.assertTrue(True, msg="hier muss  er landen")
            os.remove(paramfile)


    def setUp(self):
        pass
        #print ("setUp")

    def tearDown(self):
        pass
        #print ("tearDown")
#ParameterTest

if __name__ == '__main__':
    unittest.main()
