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
import SSOT_infra.tests.integration as testsrc


class GenerateHTML(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def init(self, tmp_path):
        self.temp_folder = Path(tmp_path)

    def setUp(self) -> None:
        self.testmodel1=testsrc.ModelHelper(testsrc.TESTMODEL1).initDB()
        self.testmodel1.remove_web_infrastructure()

        self.testmodel2=testsrc.ModelHelper(testsrc.TESTMODEL2).initDB()
        self.testmodel2.remove_web_infrastructure()

        self.testmodelcrm=testsrc.ModelHelper(testsrc.CRMTEST).initDB()
        self.testmodelcrm.remove_web_infrastructure()

        self.testmodelriddle=testsrc.ModelHelper(testsrc.RIDDLE).initDB()
        self.testmodelriddle.remove_web_infrastructure()

    def test_html_proper(self):
        listWebdoku.webmain(pjsonfilepath=self.testmodelcrm.jsonfile, pwebdirec=self.testmodelcrm.webdir, pmodelname=self.testmodelcrm.modelname)
        self.assertTrue(os.path.isdir(self.testmodelcrm.webdir/'jinjatemplates'))
        self.assertTrue(os.path.isdir(self.testmodelcrm.webdir/'css'))
        self.assertTrue(os.path.isdir(self.testmodelcrm.webdir/'js'))
        self.assertTrue(os.path.isdir(self.testmodelcrm.webdir/'images'))
        self.assertTrue(os.path.isdir(self.testmodelcrm.webdir/'images'/'icons'))
        with open(self.testmodelcrm.webdir / (self.testmodelcrm.modelname+'_de.html'),"r") as webfile:
            html=webfile.read()
            self.assertRegex(html,"Sachdienstmitarbeiter")
            self.assertRegex(html,"<br>\nde-at<br>")

        return

    def test_listwebmain_crm(self):
        html_export = HTMLExport(basedirec=str(self.testmodelcrm.modeldir),
                                 modelname=self.testmodelcrm.modelname,
                                 webDirec=self.testmodelcrm.webdir
                                 )
        js_model = JSModel.readfromfile(self.testmodelcrm.jsonfile)
        html_export.setmodel(js_model)
        listWebdoku.listwebmain(html_export)


    def test_listwebdoku(self):
        #os.chdir(self.testmodelcrm.modeldir)
        self.testmodelcrm.remove_web_infrastructure()
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
                                   "--filetype","html",
                                   '-s',
                                   'PUBL',
                                   str(self.testmodelcrm.jsonfile)])
        listWebdoku.main(psysargs=[f'{testsrc.source_root()}/IM_WEB/listWebdoku.py',
                                   "-d", str(self.testmodelcrm.webdir),
                                   "-f",'aspx',
                                   '-s',
                                   'PUBL',
                                   str(self.testmodelcrm.jsonfile)])

    def test_generate_html_riddle(self):
        self.generate_html(self.testmodelriddle.modeldir, self.testmodelriddle.jsonfile)

    def generate_html(self, project, ssot_file,filetype='html'):
        if not ssot_file.exists():
            logging.warning(f"Skipping integration test due to missing resource {ssot_file.resolve()}")
            return
        with open(ssot_file, 'r') as src:
            model = json.load(src)
        self.assertTrue(len(model['diagrams']) > 0)
        js_model = JSModel(pmodel=model)
        html_export = HTMLExport(basedirec=str(project),modelname=js_model.modelname(),
                                 webDirec=str(self.temp_folder),webFileExtension=filetype
                                 )
        html_export.setmodel(js_model)
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)
        listWebdoku.listwebmain(html_export)
        self.assertTrue(os.path.exists(html_export.webDirec()+'/'+js_model.modelname()+"."+filetype))

    def test_safe_filename(self):
        self.assertEqual('', safe_filename(''))
        self.assertEqual('-', safe_filename('-'))
        with self.assertRaises(ValueError):
            safe_filename('/').index('/')
        with self.assertRaises(ValueError):
            t = safe_filename('//')
            self.assertEqual(2, len(t))
            t.index('/')

    def test_aspx(self):
        self.generate_html(self.testmodel1.modeldir, self.testmodel1.jsonfile)
        self.generate_html(self.testmodel1.modeldir, self.testmodel1.jsonfile,'html')
        self.generate_html(self.testmodel1.modeldir, self.testmodel1.jsonfile,'aspx')
        self.generate_html(self.testmodel1.modeldir, self.testmodel1.jsonfile,'xxx')

    @pytest.mark.integration
    def test_integration_generate_html_riddle(self):
        self.generate_html(self.testmodelriddle.modeldir, self.testmodelriddle.jsonfile)

    @pytest.mark.integration
    def test_integration_generate_html_PIM(self):
        tm = testsrc.ModelHelper('PIM', testsrc.resolve_project_root() / 'testdata' / 'fyyccim-refmodels' / 'IM_PIM_FYAYC')
        tm.remove_web_infrastructure()
        self.generate_html(tm.modeldir, tm.jsonfile)
