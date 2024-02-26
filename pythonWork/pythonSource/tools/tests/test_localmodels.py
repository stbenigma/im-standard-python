import os
import shutil
import unittest

import pytest

from IM_WEB import listWebdoku
from tools.LANGTRANSL import exportdata
from LOAD_MODELS.LOAD_ODM import fillDB
from LOAD_MODELS.LOAD_INFRA.handleXML import stable_file_list
from SSOT_infra.tests.integration import testdata_root
from tools.excel.datamapping import listmapping

LOCALTESTMODELS: str = 'localtestmodels'
ODMIM: str = 'IM'
DBDIREC: str = 'DB'
WEBDIRC: str = 'Web'

""" testlocals
    tests all repositories in directory source-root/testdata/localmodels
    These models should never be pushed to github. This is used to test customer models
    
    The test looks for a file
      .../localmodels/<modeldir>/IM/<modelname>.dmd
       if found it uses all default parameters and 
      -- fills a db 
      -- generates the web-html-files
      -- generates a translation excel
        
    """


class MyTestCase(unittest.TestCase):

    @pytest.mark.integration
    def test_localODMs(self):

        localmodeldir = testdata_root() / LOCALTESTMODELS

        def check1ODMmodel(modelfilepath, basedirec):
            print(f"***** checking model {modelfilepath}")
            try:
                fillDB.fillmergedb(pmodelfilepath=str(modelfilepath),
                                  pdbfilepath=basedirec / DBDIREC / (modelfilepath.stem + '.db'),
                                  plogfilepath=basedirec / (modelfilepath.stem + '.log'))
            except Exception as e:
                self.assertTrue(False, f"\n******* model {modelfilepath}\n" +
                                f"could not be filled." +\
                                f"{e}")
            self.assertTrue(os.path.isfile(basedirec / DBDIREC / (modelfilepath.stem + '.json')))
            self.assertTrue(os.path.isfile(basedirec / DBDIREC / (modelfilepath.stem + '.db')))
            try:
                listWebdoku.webmain(pjsonfilepath=basedirec / DBDIREC / (modelfilepath.stem + '.json'),
                                    pwebdirec=basedirec / WEBDIRC,
                                    plogfilepath=basedirec / (modelfilepath.stem + '.log'))
            except Exception as e:
                self.assertTrue(False, f"******* model {modelfilepath}\n" +
                                f"could not generate HTML" \
                                f"{e}")
            self.assertTrue(os.path.isdir(basedirec / WEBDIRC / 'infra'  / 'jinjatemplates'))
            try:
                exportdata.createlangexcel(pjsonfile=basedirec / DBDIREC / (modelfilepath.stem + '.json'))
            except Exception as e:
                self.assertTrue(False, f"******* model {modelfilepath}\n" +
                                f"could not create translation excel" \
                                f"{e}")
            self.assertTrue(os.path.isfile(basedirec / DBDIREC / (modelfilepath.stem + '.xlsx')))

            try:
                listmapping.createAllMapping(pjsonfile=basedirec / DBDIREC / (modelfilepath.stem + '.json'),
                                             pdestination=basedirec / DBDIREC / (modelfilepath.stem + '_datamodels.xlsx'))
            except Exception as e:
                self.assertTrue(False, f"******* model {modelfilepath}\n" +
                                f"could not create listmapping excel" \
                                f"{e}")
            self.assertTrue(os.path.isfile(basedirec / DBDIREC / (modelfilepath.stem + '_datamodels.xlsx')))
            return

        print('')
        filelist = stable_file_list(folder=localmodeldir,removehidden=True)
        for file in filelist:
            basedirec = localmodeldir / file
            imdir = basedirec / ODMIM
            if os.path.exists(imdir):
                models = stable_file_list(folder=imdir,removehidden=True)
                for model in filter (lambda m : m.endswith('.dmd'), models):
                    if model != "IM_GEBERIT.dmd": continue
                    # if model != 'EZV_Stammdaten.dmd': continue
                    # if model != 'DC-IM.dmd': continue
                    # if model != 'ModellModell_neu.dmd': continue
                    shutil.rmtree(basedirec / DBDIREC, ignore_errors=True)
                    shutil.rmtree(basedirec / WEBDIRC, ignore_errors=True)
                    if os.path.exists(basedirec / (model[:-4]+ ".log")): os.remove(basedirec / (model[:-4]+ ".log"))
                    check1ODMmodel(modelfilepath=imdir / model, basedirec=basedirec)

        return


if __name__ == '__main__':
    unittest.main()
