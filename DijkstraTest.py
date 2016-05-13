import unittest
from Graph import Graph, Vertex
from Dijkstra import Dijkstra
from AmbulancePositionSystem import AmbulancePositionSystem

class GraphTest(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        self.graph.addVertex(vertexid='v1')
        self.graph.addVertex(vertexid='v2')
        self.graph.addVertex(vertexid='v3')
        self.graph.addVertex(vertexid='v4')
        self.graph.addVertex(vertexid='v5')
        self.graph.connect(vertexid1='v1', vertexid2='v2', cost=1)
        self.graph.connect(vertexid1='v2', vertexid2='v3', cost=23)
        self.graph.connect(vertexid1='v3', vertexid2='v4', cost=2)
        self.graph.connect(vertexid1='v4', vertexid2='v5', cost=93)
        # for node in self.graph.graph:
        #    print('sucessor: {}\n'.format(self.graph.graph.get(node).sucessor),
        #          'predecessor: {}\n'.format(self.graph.graph.get(node).predecessor))

    def tearDown(self):
        del self.graph

    def testShortestPathDijkstra(self):
        dijkstra = Dijkstra()
        S1 = 'v1'
        end = 'v4'
        D, R1 = dijkstra.dijkstra(self.graph, S1, end)
        print(D, R1)

        Path = []
        while True:
            Path.append(end)
            if end == S1:
                break
            end = R1[end]
        Path.reverse()
        print(Path)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
