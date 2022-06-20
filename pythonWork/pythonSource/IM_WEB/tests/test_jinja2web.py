import unittest
from pathlib import Path

from IM_WEB.IM_HTML import HTMLExport
from IM_WEB.jinja2web import formattext, model2html, Webmodel
from SSOT_db.IM_JSON import JSModel


class Jinja2WebTest(unittest.TestCase):
    MARKER = '<text/markdown>'

    def test_model2html(self):
        export = HTMLExport(modelname="anything")
        export.jinadirec = None
        wm = Webmodel(export=export, pcurlang='de', pintfid=0,
                      pjsmodel=JSModel(), phtmlfilelist=[])
        with self.assertRaises(Exception) :
            model2html(wm)

        template_path = Path(Path(__file__).parent, '..', 'html-lib', 'jinjatemplates')
        self.assertTrue(template_path.is_dir())
        export.jinadirec = str(template_path)

        with self.assertRaises(Exception):
            model2html(wm)

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
