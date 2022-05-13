import json
import logging
import os
import shutil
import unittest
from pathlib import Path

import pytest

from IM_WEB import listWebdoku
from IM_WEB.IM_HTML import HTMLExport
from SSOT_db.IM_JSON import JSModel
from SSOT_infra import parameters
import SSOT_infra.tests.integration as testsrc
from LOAD_MODELS.LOAD_ODM.tests.test_fillDB import create_testmodel


class GenerateHTML(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def init(self, tmp_path):
        self.temp_folder = Path(tmp_path)

    def setUp(self) -> None:
        self.testmodel1=testsrc.Testmodel(testsrc.TESTMODEL1)
        create_testmodel(self.testmodel1, new=True)
        self.testmodel1.initWeb()

        self.testmodelcrm=testsrc.Testmodel(testsrc.CRMTEST)
        self.testmodelcrm.initWeb()

        self.testmodelriddle=testsrc.Testmodel(testsrc.RIDDLE)
        self.testmodelriddle.initWeb()

    def test_html_proper(self):
        listWebdoku.webmain(pjsonfilepath=self.testmodelcrm.jsonfile, pwebdirec=self.testmodelcrm.webdir, pmodelname=self.testmodelcrm.modelname)
        with open(self.testmodelcrm.webdir / (self.testmodelcrm.modelname+'_de.html'),"r") as webfile:
            html=webfile.read()
            self.assertRegex(html,"Sachdienstmitarbeiter")
            self.assertRegex(html,"<br>\nde-at<br>")

        return

    def test_listwebdoku(self):
        #os.chdir(self.testmodelcrm.modeldir)
        listWebdoku.main(psysargs=[f'{testsrc.source_root()}/IM_WEB/listWebdoku.py',
                                   '-p',
                                   str(self.testmodelcrm.paramfile),
                                   '--diagrams=DUMMY,"Kunde mit Bilder"'])
        listWebdoku.main(psysargs=[f'{testsrc.source_root()}/IM_WEB/listWebdoku.py',
                                   '-p',
                                   str(self.testmodelcrm.paramfile),
                                   '--diagrams=DUMMY'])
        listWebdoku.main(psysargs=[f'{testsrc.source_root()}/IM_WEB/listWebdoku.py',
                                   '-p',
                                   str(self.testmodelcrm.paramfile),
                                   '-s',
                                   'PUBL'])

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
        parameters.initparam(str(project),pmodelname=js_model.modelname())
        html_export = HTMLExport()
        html_export.setmodel(js_model)
        html_export.setWebDirec(str(self.temp_folder))
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)
        listWebdoku.listwebmain(html_export)

    @pytest.mark.integration
    def test_integration_generate_html_riddle(self):
        self.generate_html(self.testmodelriddle.modeldir, self.testmodelriddle.jsonfile)

    @pytest.mark.integration
    def test_integration_generate_html_PIM(self):
        project = testsrc.resolve_project_root() / 'testdata' / 'fyyccim-refmodels' / 'PIM'
        ssot_file = project / 'DB' / 'IM_PIM_FYAYC.json'
        self.generate_html(project, ssot_file)
