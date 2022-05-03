import unittest

from SSOT_db.IM_OBJECTS.baseobject import Baseobject


class TestFillDB(unittest.TestCase):

    def test_sql_logging_base(self):
        res = Baseobject.print_sql_placeholder_values(
            "insert into x (a,b,c) values (?,?,?)", ('1', '2', '3')
        )
        self.assertEqual('insert into x (a=1, b=2, c=3) values (...)', res)
