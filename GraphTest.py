import unittest
from Graph import Graph, Vertex, GraphValidationError


class GraphTest(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        self.graph.addVertex(vertexid='v1')
        self.graph.addVertex(vertexid='v2')
        self.graph.addVertex(vertexid='v3')
        self.graph.addVertex(vertexid='v4')
        self.graph.addVertex(vertexid='v5')
        self.graph.addVertex(vertexid='v6')
        self.graph.addVertex(vertexid='v7')
        self.graph.connect(vertexid1='v1', vertexid2='v2')
        self.graph.connect(vertexid1='v1', vertexid2='v3')
        self.graph.connect(vertexid1='v1', vertexid2='v4')
        self.graph.connect(vertexid1='v1', vertexid2='v5')
        self.graph.connect(vertexid1='v2', vertexid2='v2')
        self.graph.connect(vertexid1='v2', vertexid2='v3')
        self.graph.connect(vertexid1='v2', vertexid2='v4')
        # for node in self.graph.graph:
        #    print('sucessor: {}\n'.format(self.graph.graph.get(node).sucessor),
        #          'predecessor: {}\n'.format(self.graph.graph.get(node).predecessor))

    def tearDown(self):
        del self.graph

    def testWhenAddVertexShouldHaveId(self):
        self.assertEqual(self.graph.getVertex(vertexid='v1').vertexid,
                         'v1',
                         'should have the same id')

    def testDiferentVertexesShouldHaveDiferentIds(self):
        self.assertNotEqual(self.graph.getVertex(vertexid='v1').vertexid,
                            self.graph.getVertex(vertexid='v2').vertexid,
                            'should have diferent ids')

    def testAddSucessorPredecessorToVertex(self):
        self.graph.connect('v6', 'v7')
        self.assertEqual(self.graph.graph.get('v6').sucessor.vertexid, 'v7', 'v6 should have a sucessor pointing to v7')
        self.assertEqual(self.graph.graph.get('v7').predecessor.vertexid, 'v6', 'v7 should have a predecessor pointing to v6')
        self.assertEqual(self.graph.graph.get('v6').predecessor, None, 'v6 should have predecessor pointing to None')
        self.assertEqual(self.graph.graph.get('v7').sucessor, None, 'v7 should have sucessor pointing to None')

    def testSizeShouldBeEqualToGraphLength(self):
        self.assertEqual(self.graph.size, len(self.graph.graph),
                         'size must be equal to length(self.graph.graph)')

    def testShouldConnectUsingNumbers(self):
        self.graph.addVertex(1)
        self.graph.addVertex(2)
        self.graph.connect(vertexid1=1, vertexid2=2)
        self.assertEqual(self.graph.getVertex(vertexid=1).sucessor.vertexid, 2,
                         'after insertion and connection 2 must be sucessor of 1')

    def testAddVertexObjectInsteadOfId(self):
        with self.assertRaises(GraphValidationError):
            self.assertEqual(self.graph.addVertex(vertexid=Vertex('v1')),
                             self.graph.getVertex('v1'),
                             'should really get a raise for that')

    def testMakeDisconnectOfVertexes(self):
        self.graph.disconnect(vertexid1='v1', vertexid2='v5')
        self.assertEqual(self.graph.getVertex(vertexid='v1').sucessor, None, 'should not have a connection in between v1 and v5')
        self.assertEqual(self.graph.getVertex(vertexid='v5').predecessor, None, 'should not have a connection in between v1 and v5')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
