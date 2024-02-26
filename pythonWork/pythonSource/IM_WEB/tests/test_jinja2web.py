import unittest
from pathlib import Path

import pytest

from IM_WEB.IM_HTML import HTMLExport
from IM_WEB.jinja2web import formattext, model2html, Webmodel
from SSOT_db.IM_JSON import JSModel
import SSOT_infra.tests.integration as testbase


class Jinja2WebTest(unittest.TestCase):
    MARKER = '<text/markdown>'

    def test_model2html(self):
        export = HTMLExport(modelname="anything")
        export.jinjaDirec=''
        export.model = JSModel()
        wm = Webmodel(export=export, pcurlang='de', pdatmid=0)
        with self.assertRaises(Exception) :
            model2html(wm)

        template_path = Path(Path(__file__).parent, '..', 'html-lib', 'jinjatemplates')
        self.assertTrue(template_path.is_dir())
        export.jinjaDirec=str(template_path)

        with self.assertRaises(Exception):
            model2html(wm)

        crm = testbase.ModelHelper(testbase.CRMTEST)
        export = HTMLExport(modelname=crm.modelname)
        export.jinjaDirec=''
        export.model = JSModel.readfromfile(crm.jsonfile)
        wm = Webmodel(export = export,pcurlang='de',pdatmid=None)
        enti=export.model.getbyfield(pvalue="Geografische Einheit",ptype="entities",plang="de")
        subenties = wm.getsubentyids(attrid=enti[0][1]["attributes+"][0])
        self.assertTrue(len(subenties)>0)

    def test_format_text_pass(self):
        r = formattext(None)
        self.assertIsNone(r)

        r = formattext("bla")
        self.assertEqual("bla", r)

    def test_format_text_linefeed(self):
        r = formattext("\n")
        self.assertEqual("<br>\n", r)

        r = formattext('this\nis\n<br/>\na multiline text\n\n')
        self.assertEqual('this<br>\nis<br>\n<br/><br>\na multiline text<br>\n<br>\n', r)

    def test_format_text_rewrite_markdown(self):
        r = formattext(self.MARKER + '<h1>Title</h1>')
        self.assertEqual('<h1 class="md">Title</h1>', r)

        r = formattext(self.MARKER + '<h1>Title</h1>\n<h3>H3</h3><li>\n<ul></ul></li>')
        self.assertEqual('<h1 class="md">Title</h1>\n'
                         '<h3 class="md">H3</h3>\n'
                         '<li class="md">\n'
                         '<ul class="md"></ul></li>', r)
