import unittest
from unittest import SkipTest

import pytest

try:
    import office365
except ModuleNotFoundError:
    raise SkipTest("Missing module office356. Install using `pip install Office365-REST-Python-Client`")

from PUBLISH_MODEL.sharepoint.list_publisher import *

CONFIGURATION = Path(__file__).parent / 'test.yaml'


class TestSharepointListPublisher(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def init(self, tmp_path, caplog):
        self.temp_folder = tmp_path
        caplog.set_level(logging.DEBUG)
        self.caplog = caplog

    def setUp(self):
        if not CONFIGURATION.is_file():
            self.skipTest(f"Missing configuratoin in '{CONFIGURATION.resolve()}.")
        with open(CONFIGURATION, 'r') as src:
            self.config = yaml.safe_load(src)
        logging.info("**** start of test ****")

    def tearDown(self) -> None:
        logging.info("**** end of test ****")
        print(os.linesep.join(map(lambda x: x.getMessage(), self.caplog.records)))

    @pytest.mark.integration
    def test_login_test(self):
        ctx = login(self.config['sharepoint'])
        result = ctx.lists.get().execute_query()
        self.assertTrue(len(result) > 0, f"Expecting more than 0 lists")

    @pytest.mark.integration
    def test_update_structure(self):
        sp_conf = self.config['sharepoint']
        ctx = login(sp_conf)

        for sp_list_config in sp_conf['lists']:
            kind = sp_list_config.get('type')
            if kind == 'entities':
                spl = ctx.web.lists.get_by_title(sp_list_config['title']).execute_query()
                fields = spl.fields.get().execute_query()
                self.assertTrue(len(fields) > 0)
                msg = update_structure(spl, entity_mapping)
                print(f"Update result:\n{os.linesep.join(msg)}")
                ctx.execute_query()
            elif kind == 'attributes':
                spl = ctx.lists.get_by_title(sp_list_config['title']).execute_query()
                fields = spl.fields.get().execute_query()
                self.assertTrue(len(fields) > 0)
                msg = update_structure(spl, attribute_mapping)
                print(f"Update result:\n{os.linesep.join(msg)}")
                ctx.execute_query()
            else:
                print(f"Unknown list kind {kind}")

        print(os.linesep.join(map(lambda x: x.getMessage(), self.caplog.records)))
        # perform update

    def disabled_test_collect_content(self):
        sp_conf = self.config['sharepoint']
        ctx = login(sp_conf)
        for sp_list_config in sp_conf['lists']:
            kind = sp_list_config.get('type')
            if kind == 'entities':
                spl = ctx.web.lists.get_by_title(sp_list_config['title'])
                content = spl.items.get().execute_query()
                cd = collect_content(content, Path(self.temp_folder) / 'entities-0.csv')
                content_map = dict(map(lambda e: (e[0], e[1]), []))
                i, u, d = update_content(spl, entity_mapping, {}, content_map)
                logging.info(f"Row summary 1: {len(i)} inserted, {len(u)} updated, {len(d)} deleted. "
                             f"Count before {len(cd)}")
                # ctx.clear_queries()
                ctx.execute_query()

                # Why do we have to reload to update?
                content1 = spl.items.get().execute_query()
                self.assertEqual(0, len(content1))
                cd = collect_content(content1, Path(self.temp_folder) / 'entities-1.csv')
                content_map = dict(map(lambda e: (e[0], e[1]), cd))
                i, u, d = update_content(spl, entity_mapping, one_entry, content_map)
                logging.info(f"Row summary 2: {len(i)} inserted, {len(u)} updated, {len(d)} deleted")
                ctx.execute_query()

                # Why do we have to reload to update?
                content2 = spl.items.get().execute_query()
                cd = collect_content(content2, Path(self.temp_folder) / 'entities-2.csv')
                content_map = dict(map(lambda e: (e[0], e[1]), cd))
                i, u, d = update_content(spl, entity_mapping, {}, content_map)
                logging.info(f"Row summary 3: {len(i)} inserted, {len(u)} updated, {len(d)} deleted")
                ctx.execute_query()
                self.assertEqual(1, len(cd))


one_entry = {
    "ENTI0000": {
        "name": {"en": "Enti101"},
        "descr": {"en": "Zero Entity"},
        "synonyms": {"en": "Bla"},
        "diagrams+": ['DIAG000', 'DIAG001'],
    }
}
