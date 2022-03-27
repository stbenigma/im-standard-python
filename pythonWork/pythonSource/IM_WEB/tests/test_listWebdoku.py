import json
import logging
import os
import unittest
from pathlib import Path

import pytest

from IM_WEB import listWebdoku
from IM_WEB.IM_HTML import HTMLExport
from SSOT_db.IM_JSON import JSModel
from SSOT_infra import parameters
from LOAD_MODELS.LOAD_ODM import fillDB
import SSOT_infra.tests.integration as testsrc


class GenerateHTML(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def init(self, tmp_path):
        self.temp_folder = Path(tmp_path)

    def setUp(self) -> None:
        from LOAD_MODELS.LOAD_ODM.tests.test_fillDB import create_testmodel
        testmodelname, testdir, dbfilepath = testsrc.testmodel1()
        create_testmodel(testmodelname=testmodelname, testdir=testdir, dbfilepath=dbfilepath, new=True)

        testmodelname, testdir, dbfilepath = testsrc.testmodelcrm()
        fillDB.filldbmain(pparamfile = testdir / (testmodelname + '.params'))

    def test_listwebdoku(self):
        testmodelname, testdir, dbfilepath = testsrc.testmodelcrm()
        os.chdir(testdir)
        listWebdoku.main(psysargs=['/Users/stb/Documents/Projekte/FYAYC_intern/fyyccim-tools/pythonWork/pythonSource/IM_WEB/listWebdoku.py',
                                   '-p',
                                   'crmTest.params',
                                   '--diagrams=DUMMY,"Kunde mit Bilder"'])
        listWebdoku.main(psysargs=['/Users/stb/Documents/Projekte/FYAYC_intern/fyyccim-tools/pythonWork/pythonSource/IM_WEB/listWebdoku.py',
                                   '-p',
                                   'crmTest.params',
                                   '--diagrams=DUMMY'])
        listWebdoku.main(psysargs=['/Users/stb/Documents/Projekte/FYAYC_intern/fyyccim-tools/pythonWork/pythonSource/IM_WEB/listWebdoku.py',
                                   '-p',
                                   'crmTest.params',
                                   '-s',
                                   'PUBL'])

    def test_generate_html_riddle(self):
        project = testsrc.testmodels_dir() / testsrc.RIDDLE

        ssot_file = project / 'DB' / (testsrc.RIDDLE+'.json')
        self.generate_html(project, ssot_file)

    def generate_html(self, project, ssot_file):
        if not ssot_file.exists():
            logging.warning(f"Skipping integration test due to missing resource {ssot_file.resolve()}")
        with open(ssot_file, 'r') as src:
            model = json.load(src)
        self.assertTrue(len(model['diagrams']) > 0)
        js_model = JSModel(pmodel=model)

        # HACK fake model
        model_file = project / 'IM' / 'riddle.dmd'
        if not model_file.exists():
            model_file.parent.mkdir(exist_ok=True)
            model_file.touch(exist_ok=True)

        parameters.initparam(str(project),pmodelname=js_model.modelname())
        html_export = HTMLExport()
        html_export.setmodel(js_model)
        html_export.setWebDirec(str(self.temp_folder))
        listWebdoku.listwebmain(html_export)

    def test_integration_generate_html_riddle(self):
        project = testsrc.testmodels_dir() / 'riddle'
        ssot_file = project / 'DB' / 'riddle.json'
        self.generate_html(project, ssot_file)

    @pytest.mark.integration
    def test_integration_generate_html_PIM(self):
        project = testsrc.resolve_project_root() / 'testdata' / 'fyyccim-refmodels' / 'PIM'
        ssot_file = project / 'DB' / 'IM_PIM_FYAYC.json'
        self.generate_html(project, ssot_file)
