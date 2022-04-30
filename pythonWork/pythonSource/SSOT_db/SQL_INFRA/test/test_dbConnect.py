import unittest

from SSOT_db.SQL_INFRA import dbConnect


class MyTestCase(unittest.TestCase):
    TEST_VERSION = '1.2.3-unittest (dev)'

    def setUp(self) -> None:
        super().setUp()
        self.connection = dbConnect.openDBbasic('/tmp/test.db')

    def tearDown(self) -> None:
        dbConnect.closeDB()
        self.connection.close()
        self.connection = None
        super().tearDown()

    def test_write_git_revision(self):
        dbConnect.write_git_reversion(self.TEST_VERSION, self.connection)

    def test_read_git_revision(self):
        self.test_write_git_revision()

        self.tearDown()
        # reconnect
        self.setUp()

        value = dbConnect.read_git_revision()
        self.assertIsNotNone(value)
        self.assertEqual(self.TEST_VERSION, value)
