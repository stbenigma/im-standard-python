from collections import defaultdict


class Graph:
    """
        graph=[
            ('A', 'B'),
            ('A', 'C'),
            ('B', 'D'),
            ('C', 'D'),
            ('E', 'D'),
        ]

    """
    def __init__(self, graph=None):
        self.graph = defaultdict(list)
        """
            self.graph{'A':['B','C'],
                       'B':['D']
                       'C':['D']
                       'E':['D']
                       }
            
        """
        if graph is not None:
            self.add_graph(graph)

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def add_graph(self, graph):
        for u, v in graph:
            self.add_edge(u,v)

    def get_predecessors(self,root):
        visited = set()
        predess = set()
        def pfs(node):
            visited.add(node)
            for parent in [p for p,s in self.graph.items() if node in s]:
                if parent not in visited:
                    predess.add(parent)
                    pfs(parent)
        pfs(root)
        return predess

    def get_descendants(self, root):
        visited = set()
        descendants = set()

        def dfs(node):
            visited.add(node)
            for neighbour in self.graph[node]:
                if neighbour not in visited:
                    descendants.add(neighbour)
                    dfs(neighbour)

        dfs(root)
        return descendants



