import json
import logging
import os
import shutil
import unittest
from pathlib import Path

import pytest

from IM_WEB import listWebdoku
from IM_WEB.IM_HTML import HTMLExport
from IM_WEB.listWebdoku import safe_filename
from SSOT_db.IM_JSON import JSModel
from SSOT_infra import parameters
import SSOT_infra.tests.integration as testsrc


class GenerateHTML(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def init(self, tmp_path):
        self.temp_folder = Path(tmp_path)

    def setUp(self) -> None:
        self.testmodel1=testsrc.Testmodel(testsrc.TESTMODEL1).initDB()
        self.testmodel1.initWeb()

        self.testmodelcrm=testsrc.Testmodel(testsrc.CRMTEST).initDB()
        self.testmodelcrm.initWeb()

        self.testmodelriddle=testsrc.Testmodel(testsrc.RIDDLE).initDB()
        self.testmodelriddle.initWeb()

    def test_html_proper(self):
        listWebdoku.webmain(pjsonfilepath=self.testmodelcrm.jsonfile, pwebdirec=self.testmodelcrm.webdir, pmodelname=self.testmodelcrm.modelname)
        self.assertTrue(os.path.isdir(self.testmodelcrm.webdir/'jinjatemplates'))
        self.assertTrue(os.path.isdir(self.testmodelcrm.webdir/'css'))
        self.assertTrue(os.path.isdir(self.testmodelcrm.webdir/'js'))
        self.assertTrue(os.path.isdir(self.testmodelcrm.webdir/'icons'))
        self.assertTrue(os.path.isdir(self.testmodelcrm.webdir/'images'))
        with open(self.testmodelcrm.webdir / (self.testmodelcrm.modelname+'_de.html'),"r") as webfile:
            html=webfile.read()
            self.assertRegex(html,"Sachdienstmitarbeiter")
            self.assertRegex(html,"<br>\nde-at<br>")

        return

    def test_listwebdoku(self):
        #os.chdir(self.testmodelcrm.modeldir)
        print ("\nDEBUG***************** sitch on ***********")
        return
        self.testmodelcrm.initWeb()
        listWebdoku.main(psysargs=[f'{testsrc.source_root()}/IM_WEB/listWebdoku.py',
                                    "-d",str(self.testmodelcrm.webdir),
                                   '--diagrams=DUMMY,"Kunde mit Bilder"',
                                   str(self.testmodelcrm.jsonfile)])
        listWebdoku.main(psysargs=[f'{testsrc.source_root()}/IM_WEB/listWebdoku.py',
                                   "-d", str(self.testmodelcrm.webdir),
                                   '--diagrams=DUMMY',
                                   str(self.testmodelcrm.jsonfile)])
        listWebdoku.main(psysargs=[f'{testsrc.source_root()}/IM_WEB/listWebdoku.py',
                                   "-d", str(self.testmodelcrm.webdir),
                                   '-s',
                                   'PUBL',
                                   str(self.testmodelcrm.jsonfile)])

    def test_generate_html_riddle(self):
        self.generate_html(self.testmodelriddle.modeldir, self.testmodelriddle.jsonfile)

    def generate_html(self, project, ssot_file):
        if not ssot_file.exists():
            logging.warning(f"Skipping integration test due to missing resource {ssot_file.resolve()}")
            return
        with open(ssot_file, 'r') as src:
            model = json.load(src)
        self.assertTrue(len(model['diagrams']) > 0)
        js_model = JSModel(pmodel=model)
        html_export = HTMLExport(basedirec=str(project),modelname=js_model.modelname(),webDirec=str(self.temp_folder))
        html_export.setmodel(js_model)
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)
        listWebdoku.listwebmain(html_export)

    def test_safe_filename(self):
        self.assertEqual('', safe_filename(''))
        self.assertEqual('-', safe_filename('-'))
        with self.assertRaises(ValueError):
            safe_filename('/').index('/')
        with self.assertRaises(ValueError):
            t = safe_filename('//')
            self.assertEqual(2, len(t))
            t.index('/')

    @pytest.mark.integration
    def test_integration_generate_html_riddle(self):
        self.generate_html(self.testmodelriddle.modeldir, self.testmodelriddle.jsonfile)

    @pytest.mark.integration
    def test_integration_generate_html_PIM(self):
        project = testsrc.resolve_project_root() / 'testdata' / 'fyyccim-refmodels' / 'PIM'
        ssot_file = project / 'DB' / 'IM_PIM_FYAYC.json'
        self.generate_html(project, ssot_file)
