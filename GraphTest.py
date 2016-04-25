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
        self.graph.connect(vertexid1='v1', vertexid2='v2')
        self.graph.connect(vertexid1='v1', vertexid2='v3')
        self.graph.connect(vertexid1='v1', vertexid2='v4')
        self.graph.connect(vertexid1='v1', vertexid2='v5')
        self.graph.connect(vertexid1='v2', vertexid2='v1')
        self.graph.connect(vertexid1='v2', vertexid2='v3')
        self.graph.connect(vertexid1='v2', vertexid2='v4')
        self.graph.connect(vertexid1='v2', vertexid2='v5')
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
        self.graph.addVertex(vertexid='v6')
        self.graph.addVertex(vertexid='v7')
        self.graph.connect('v6', 'v7')
        self.assertEquals(self.graph.vertexAdjacencies('v6').get('v7'), 'v7',
                          'v6 should have a sucessor pointing to v7')
        self.assertEquals(self.graph.vertexAdjacencies('v7').get('v6'), 'v6',
                          'v7 should have a predecessor pointing to v6')

    def testSizeShouldBeEqualToGraphLength(self):
        self.assertEqual(self.graph.size, len(self.graph.graph),
                         'size must be equal to length(self.graph.graph)')

    def testShouldConnectUsingNumbers(self):
        self.graph.addVertex(1)
        self.graph.addVertex(2)
        self.graph.connect(vertexid1=1, vertexid2=2)
        self.assertTrue(2 in self.graph.vertexAdjacencies(1),
                         'after insertion and connection 2 must be \"sucessor\" of 1')

    def testAddVertexObjectInsteadOfId(self):
        with self.assertRaises(GraphValidationError):
            self.assertEqual(self.graph.addVertex(vertexid=Vertex('v1')),
                             self.graph.getVertex('v1'),
                             'should really get a raise for that')

    def testMakeDisconnectOfVertexes(self):
        self.graph.disconnect(vertexid1='v1', vertexid2='v5')
        self.assertTrue('v5' not in self.graph.vertexAdjacencies('v1'),
                        'should not have a connection in between v1 and v5')
        self.assertTrue('v1' not in self.graph.vertexAdjacencies('v5'),
                        'should not have a connection in between v1 and v5')
        self.assertTrue(self.graph.size == len(self.graph.graph) == self.graph.graphMagnitude(),
                        'should return true for all ways to get the graph size')

    def testVertexRemoval(self):
        self.graph.removeVertex(vertexid='v1')
        self.assertFalse('v1' in self.graph.vertexAdjacencies('v3'),
                         'should return nothing because v1 was removed before this')
        self.assertFalse('v1' in self.graph.vertexAdjacencies('v4'),
                         'should return nothing because v1 was removed before this')
        with self.assertRaises(GraphValidationError):
            self.assertEquals(self.graph.vertexAdjacencies(vertexid='v1'), None,
                              'should return nothign because it has been already deleted')
        self.assertTrue(self.graph.size == len(self.graph.graph) == self.graph.graphMagnitude(),
                        'should return true for all ways to get the graph size')

    def testGraphMagnitude(self):
        self.assertFalse(self.graph.graphMagnitude() == 7,
                          'should have take the number of nodes already inserted in')
        self.graph.disconnect(vertexid1='v1', vertexid2='v5')
        self.assertEquals(self.graph.graphMagnitude(), 5,
                          'should have take the number of nodes already inserted in')
        self.assertFalse(self.graph.size == 3,
                          'should return true by just getting size property')

    def testVertexMagnitude(self):
        self.assertEquals(self.graph.vertexMagnitude('v1'), 4,
                          'should have a vertex with a number of adjacencies')

    def testIfItIsRegularGraph(self):
        """
        The great thing about graphs is that you can save a lot of cpu power
        by just connecting nodes right, when we have a regular graph we dont
        need to waste cpu power to connect a lot of nodes in a case where the
        edges dont have direction of course, and we can come and go through
        the same edge, the connections do the heuristic job of anticipating
        useful connections.
        """
        self.assertEquals(self.graph.isRegular(), False, 'should return false a first attempt')
        self.graph.connect(vertexid1='v3', vertexid2='v4')
        self.graph.connect(vertexid1='v3', vertexid2='v5')
        self.graph.connect(vertexid1='v4', vertexid2='v5')
        self.assertEquals(self.graph.isRegular(), True, 'should return false a first attempt')

    def testFindTransitiveClosure(self):
        self.graph.connect(vertexid1='v3', vertexid2='v4')
        self.graph.connect(vertexid1='v3', vertexid2='v5')
        self.graph.connect(vertexid1='v4', vertexid2='v5')
        print(self.graph.transitiveClosure(vertexid='v3'))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
