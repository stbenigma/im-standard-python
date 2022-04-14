import html
import json
import logging
import re
from pathlib import Path

import pytest

from IM_WEB.IM_HTML import HTMLExport
from IM_WEB.IM_HTML.svgpublisher import publish_svg_diagrams
from SSOT_db.IM_JSON import JSModel
from SSOT_infra import parameters
from SSOT_infra.parameters import parameterdefaults
from SSOT_infra.tests.integration import IntegrationTest, riddle_json


def udpr_to_link(element: dict) -> (str or None):
    udpr = element.get('userdefprops')
    if udpr is not None:
        assert isinstance(udpr, dict)
        for m_key, m_value in udpr.items():
            for g_key, g_value in m_value.items():
                for key, value in g_value.items():
                    if 'TOOL' in value['name']:
                        return value['value']
    return None


class EnvironDiagramGeneration(IntegrationTest):

    RIDDLE_PATH = riddle_json()

    @pytest.fixture(autouse=True)
    def init(self, tmp_path):
        self.temp_folder = Path(tmp_path)

    def test_render(self, ssot_file=RIDDLE_PATH):
        if not ssot_file.exists():
            logging.warning(f"Skipping integration test due to missing resource {ssot_file.resolve()}")
        with open(ssot_file, 'r') as src:
            model = json.load(src)
        self.assertTrue(len(model['diagrams']) > 0)
        html_export = HTMLExport()
        html_export.model = JSModel(pmodel=model)
        content = self.temp_folder / 'content'
        content.mkdir(parents=True, exist_ok=True)

        # TODO get rid of this
        parameterdefaults()
        parameters.parameter['webdirec'] = str(content)

        html_export.setWebDirec(str(content.resolve()))

        html_export.custom_hyperlink = udpr_to_link

        for lang in model['languages'].keys():
            generated = publish_svg_diagrams(html_export, lang)
            self.assertTrue(len(generated) > 1)
            print(generated)
            riddle_file = list(filter(lambda d: 'riddle-' in str(d), generated.values()))
            self.assertEqual(1, len(riddle_file))
            with open(riddle_file[0], 'r') as src:
                lines = src.readlines()
                match = list(filter(lambda l: 'https://res.cloudinary.com/' in l.lower(), lines))
                self.assertTrue(len(match) > 0)
                m = re.findall(r'"https://res\.cloudinary\.com.+&amp;"', match[0])
                self.assertEqual(len(m), 1)
                content = m[0][1:-1]
                verify = html.escape(html.unescape(content))
                self.assertEqual(content, verify)
