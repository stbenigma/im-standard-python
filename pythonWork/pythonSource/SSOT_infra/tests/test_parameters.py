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


    def test_initparam(self):
        with self.assertRaises(Exception):
            parameters.initparam()

        #modelname olny
        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            currentDirec = os.getcwd()
            parameters.initparam(basedirec=currentDirec, modelname=TESTMODELNAME)
            self.assertEqual(currentDirec,str(parameters.parameter.baseDirec()))
            self.assertEqual(os.path.join(currentDirec,'DB'),str(parameters.parameter.dbDirect()))
            self.assertEqual(os.path.join(currentDirec,'DB',TESTMODELNAME+'.db'),str(parameters.parameter.dbFilePath()))
            self.assertEqual(os.path.join(currentDirec),str(parameters.parameter.logfiledirec()))
            self.assertEqual(os.path.join(currentDirec,TESTMODELNAME+'.log'),str(parameters.parameter.logfilepath()))
            self.assertEqual('en', parameters.parameter.modelLang())
            self.assertEqual('en', parameters.parameter.languages())

            #some other parameters
            with self.assertRaises(Exception):
                parameters.initparam(basedirec=currentDirec,odelname=TESTMODELNAME,modellang='xx')
            with self.assertRaises(Exception) :
                parameters.initparam(basedirec=currentDirec,modelname=TESTMODELNAME,languages='xx,es')

            parameters.initparam(basedirec=currentDirec,modelname=TESTMODELNAME,modellang='de',languages='es')
            self.assertEqual('de', parameters.parameter.modelLang())
            self.assertEqual('es', parameters.parameter.languages())

            parameters.initparam(basedirec=currentDirec,modelname=TESTMODELNAME,modellang='de',languages='es,en,it,de')
            self.assertEqual('de', parameters.parameter.modelLang())
            self.assertEqual('es,en,it,de', parameters.parameter.languages())

            currentDirec = os.getcwd()
            parameters.initparam(basedirec=currentDirec,modelname=TESTMODELNAME,dbfilepath=os.path.join(currentDirec,'foo.db'),logfilepath=os.path.join(currentDirec,'foo.logg'))
            self.assertEqual(currentDirec,str(parameters.parameter.baseDirec()))
            self.assertEqual(os.path.join(currentDirec),str(parameters.parameter.dbDirect()))
            self.assertEqual(os.path.join(currentDirec,'foo.db'),str(parameters.parameter.dbFilePath()))
            self.assertEqual(os.path.join(currentDirec),str(parameters.parameter.logfiledirec()))
            self.assertEqual(os.path.join(currentDirec,'foo.logg'),str(parameters.parameter.logfilepath()))

        return


    def setUp(self):
        pass

    def tearDown(self):
        pass
