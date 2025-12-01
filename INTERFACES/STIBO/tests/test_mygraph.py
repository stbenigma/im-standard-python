import unittest
from INTERFACES.STIBO.mygraph import Graph

class MyTestCase(unittest.TestCase):
    def test_descendants(self):
        g = Graph(graph=[
            ('A', 'B'),
            ('A', 'C'),
            ('B', 'D'),
            ('C', 'D'),
            ('E', 'D'),
        ])
        self.assertSetEqual(set('D'),g.get_descendants('E'))
        self.assertSetEqual(set(),g.get_descendants('X'))
        self.assertSetEqual(set(['B','D','C']),g.get_descendants('A'))

    def test_predecessors(self):
        g = Graph(graph=[
            ('A', 'B'),
            ('A', 'C'),
            ('B', 'D'),
            ('C', 'D'),
            ('E', 'D'),
        ])
        self.assertSetEqual(set(),g.get_predecessors('A'))
        self.assertSetEqual(set(['A']),g.get_predecessors('B'))
        self.assertSetEqual(set(['A','E','C','B']),g.get_predecessors('D'))

if __name__ == '__main__':
    unittest.main()
