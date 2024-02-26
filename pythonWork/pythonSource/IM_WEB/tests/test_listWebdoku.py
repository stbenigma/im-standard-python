import json
import logging
import os
import shutil
import unittest
from pathlib import Path
from distutils.dir_util import copy_tree

import pytest

import SSOT_infra.tests.integration as testsrc
from IM_WEB import listWebdoku
from IM_WEB.IM_HTML import HTMLExport
from SSOT_db.IM_JSON import JSModel


class GenerateHTML(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def init(self, tmp_path):
        self.temp_folder = Path(tmp_path)

    def setUp(self) -> None:
        self.testmodel1 = testsrc.ModelHelper(testsrc.TESTMODEL1).initDB(palways=False)
        self.testmodel1.remove_web_infrastructure()

        self.testmodel2 = testsrc.ModelHelper(testsrc.TESTMODEL2).initDB(palways=False)
        self.testmodel2.remove_web_infrastructure()

        self.testmodelcrm = testsrc.ModelHelper(testsrc.CRMTEST).initDB(palways=False)

        self.testmodelriddle = testsrc.ModelHelper(testsrc.RIDDLE).initDB(palways=False)
        self.testmodelriddle.remove_web_infrastructure()

    def test_html_proper(self):

        self.testmodelcrm.remove_web_infrastructure(self.testmodel2.webdir)
        listWebdoku.webmain(pjsonfilepath=self.testmodel2.jsonfile, pwebdirec=self.testmodel2.webdir,
                            pmodelname=self.testmodel2.modelname)


        self.testmodelcrm.remove_web_infrastructure(self.testmodelcrm.webdir)
        listWebdoku.webmain(pjsonfilepath=self.testmodelcrm.jsonfile, pwebdirec=self.testmodelcrm.webdir,
                            pmodelname=self.testmodelcrm.modelname)
        self.assertTrue(os.path.isdir(self.testmodelcrm.webdir / "infra" / 'jinjatemplates'))
        self.assertTrue(os.path.isdir(self.testmodelcrm.webdir / "infra" / 'css'))
        self.assertTrue(os.path.isdir(self.testmodelcrm.webdir / "infra" / 'js'))
        self.assertTrue(os.path.isdir(self.testmodelcrm.webdir / "infra" / 'images'))
        self.assertTrue(os.path.isdir(self.testmodelcrm.webdir / "infra" / 'images' / 'icons'))
        with open(self.testmodelcrm.webdir / "de" / "index.html", "r") as webfile:
            html = webfile.read()
            self.assertRegex(html, "Sachdienstmitarbeiter")
            self.assertRegex(html, "<br>\nde-at<br>")

        return

    def test_listwebmain_tm2_nonsingle(self):
        self.testmodelcrm.remove_web_infrastructure(self.testmodel2.modeldir / 'WebMulti')

        #create webpages as multiple pages
        html_export = HTMLExport(basedirec=str(self.testmodel2.modeldir),
                                 modelname=self.testmodel2.modelname,
                                 webDirec=self.testmodel2.modeldir / 'WebMulti',
                                 singlefile=False
                                 )
        copy_tree(os.path.join(html_export.libSourceDirec, 'image'), html_export.imageDirec)
        copy_tree(os.path.join(html_export.libSourceDirec, 'jinjatemplates'), html_export.jinjaDirec)

        js_model = JSModel.readfromfile(self.testmodel2.jsonfile)
        html_export.model=js_model
        listWebdoku.listwebmain(export=html_export)
        return

    def test_listwebmain_crm_nonsingle(self):
        self.testmodelcrm.remove_web_infrastructure(self.testmodelcrm.modeldir / 'WebMulti')

        #create webpages as multiple pages
        html_export = HTMLExport(basedirec=str(self.testmodelcrm.modeldir),
                                 modelname=self.testmodelcrm.modelname,
                                 webDirec=self.testmodelcrm.modeldir / 'WebMulti',
                                 singlefile=False
                                 )
        copy_tree(os.path.join(html_export.libSourceDirec, 'image'), html_export.imageDirec)
        copy_tree(os.path.join(html_export.libSourceDirec, 'jinjatemplates'), html_export.jinjaDirec)

        js_model = JSModel.readfromfile(self.testmodelcrm.jsonfile)
        html_export.model=js_model
        listWebdoku.listwebmain(export=html_export)
        return

    def test_listwebmain_tm2_single(self):
        self.testmodelcrm.remove_web_infrastructure(self.testmodel2.modeldir / 'WebSingle')

        html_export = HTMLExport(basedirec=str(self.testmodel2.modeldir),
                                 modelname=self.testmodel2.modelname,
                                 webDirec=self.testmodel2.modeldir / 'Web2',
                                 singlefile=True
                                 )
        copy_tree(os.path.join(html_export.libSourceDirec, 'jinjatemplates'), html_export.jinjaDirec)

        js_model = JSModel.readfromfile(self.testmodel2.jsonfile)
        html_export.model = js_model

        listWebdoku.listwebmain(html_export)

        return

    def test_listwebdoku(self):
        # os.chdir(self.testmodelcrm.modeldir)
        self.testmodelcrm.remove_web_infrastructure(self.testmodelcrm.webdir)
        self.testmodelcrm.remove_web_infrastructure(self.testmodel2.webdir)
        listWebdoku.main(psysargs=[f'{testsrc.source_root()}/IM_WEB/listWebdoku.py',
                                   "-d", str(self.testmodelcrm.webdir),
                                   '--diagrams=DUMMY,"Kunde mit Bilder"',
                                   '-sf',
                                   str(self.testmodelcrm.jsonfile)])
        listWebdoku.main(psysargs=[f'{testsrc.source_root()}/IM_WEB/listWebdoku.py',
                                   "-d", str(self.testmodelcrm.webdir),
                                   '--diagrams=DUMMY',
                                    '-sf',
                                   str(self.testmodelcrm.jsonfile)])
        listWebdoku.main(psysargs=[f'{testsrc.source_root()}/IM_WEB/listWebdoku.py',
                                   "-d", str(self.testmodel2.webdir),
                                   "--filetype", "html",
                                   "--status", 'PUBL',
                                   str(self.testmodel2.jsonfile)])
        listWebdoku.main(psysargs=[f'{testsrc.source_root()}/IM_WEB/listWebdoku.py',
                                   "-d", str(self.testmodel2.webdir),
                                   "-f", 'aspx',
                                   "--status", 'PUBL',
                                   str(self.testmodel2.jsonfile)])
        listWebdoku.main(psysargs=[f'{testsrc.source_root()}/IM_WEB/listWebdoku.py',
                                   "-d", str(self.testmodel2.webdir)+"/WebODM",
                                   "--filetype", "html",
                                   "-sf",
                                   "--diagtype","ODM",
                                   str(self.testmodel2.jsonfile)])
        listWebdoku.main(psysargs=[f'{testsrc.source_root()}/IM_WEB/listWebdoku.py',
                                   "-d", str(self.testmodel2.webdir)+"/WebFYAYC",
                                   "--filetype", "html",
                                   "-sf",
                                   "--diagtype","FYAYC",
                                   str(self.testmodel2.jsonfile)])

    def test_generate_html_riddle(self):
        self.generate_html(self.testmodelriddle.modeldir, self.testmodelriddle.jsonfile)

    def generate_html(self, project, ssot_file, filetype='html'):
        if not ssot_file.exists():
            logging.warning(f"Skipping integration test due to missing resource {ssot_file.resolve()}")
            return
        with open(ssot_file, 'r') as src:
            model = json.load(src)
        self.assertTrue(len(model['diagrams']) > 0)
        js_model = JSModel(pmodel=model)
        html_export = HTMLExport(basedirec=str(project), modelname=js_model.modelname(),
                                 webDirec=str(self.temp_folder), webFileExtension=filetype
                                 )
        html_export.model=js_model
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)
        listWebdoku.listwebmain(html_export)
        self.assertTrue(os.path.exists(html_export.webDirec + '/en/' + "index" + "." + filetype))

    def test_safe_filename(self):
        self.assertEqual('', HTMLExport.safe_filename(''))
        self.assertEqual('-', HTMLExport.safe_filename('-'))
        with self.assertRaises(ValueError):
            HTMLExport.safe_filename('/').index('/')
        with self.assertRaises(ValueError):
            t = HTMLExport.safe_filename('//')
            self.assertEqual(2, len(t))
            t.index('/')

    def test_aspx(self):
        self.generate_html(self.testmodel1.modeldir, self.testmodel1.jsonfile)
        self.generate_html(self.testmodel1.modeldir, self.testmodel1.jsonfile, 'html')
        self.generate_html(self.testmodel1.modeldir, self.testmodel1.jsonfile, 'aspx')
        self.generate_html(self.testmodel1.modeldir, self.testmodel1.jsonfile, 'xxx')

    @pytest.mark.integration
    def test_integration_generate_html_riddle(self):
        self.generate_html(self.testmodelriddle.modeldir, self.testmodelriddle.jsonfile)

    @pytest.mark.integration
    def test_integration_generate_html_PIM(self):
        tm = testsrc.ModelHelper('PIM',
                                 testsrc.resolve_project_root() / 'testdata' / 'fyyccim-refmodels' / 'IM_PIM_FYAYC')
        tm.remove_web_infrastructure()
        self.generate_html(tm.modeldir, tm.jsonfile)
