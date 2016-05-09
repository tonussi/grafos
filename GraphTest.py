import unittest
from Graph import Graph, Vertex

class GraphTest(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        self.graph.addVertex(vertexid='v1')
        self.graph.addVertex(vertexid='v2')
        self.graph.addVertex(vertexid='v3')
        self.graph.addVertex(vertexid='v4')
        self.graph.addVertex(vertexid='v5')
        self.graph.connect(vertexid1='v1', vertexid2='v2', cost=None)
        self.graph.connect(vertexid1='v1', vertexid2='v3', cost=None)
        self.graph.connect(vertexid1='v1', vertexid2='v4', cost=None)
        self.graph.connect(vertexid1='v1', vertexid2='v5', cost=None)
        self.graph.connect(vertexid1='v2', vertexid2='v1', cost=None)
        self.graph.connect(vertexid1='v2', vertexid2='v3', cost=None)
        self.graph.connect(vertexid1='v2', vertexid2='v4', cost=None)
        self.graph.connect(vertexid1='v2', vertexid2='v5', cost=None)
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

    def testWeigth(self):
        self.graph.addVertex(vertexid='v6')
        self.graph.addVertex(vertexid='v7')
        self.graph.connect('v6', 'v7', cost=1290)
        self.assertEquals(self.graph.vertexAdjacencies('v6').get('v7').getcost(), 1290,
                          'v6 should have weigth equal to 1290 linked to v7')
        self.assertEquals(self.graph.vertexAdjacencies('v7').get('v6').getcost(), 1290,
                          'v7 should have weigth equal to 1290 linked to v6')

    def testSizeShouldBeEqualToGraphLength(self):
        self.assertEqual(self.graph.size, len(self.graph.graph),
                         'size must be equal to length(self.graph.graph)')

    def testShouldConnectUsingNumbers(self):
        self.graph.addVertex(vertexid=1)
        self.graph.addVertex(vertexid=2)
        self.graph.connect(vertexid1=1, vertexid2=2, cost=None)
        self.assertTrue(2 in self.graph.vertexAdjacencies(vertexid=1),
                         'after insertion and connection 2 must be \"sucessor\" of 1')

    def testAddVertexObjectInsteadOfId(self):
        #with self.assertRaises(GraphValidationError):
        self.assertEqual(self.graph.addVertex(vertexid=Vertex('v1')),
                         None, 'should get None after trying to input another \"v1\" in the graph')

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
        #with self.assertRaises(GraphValidationError):
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
        self.graph.connect(vertexid1='v3', vertexid2='v4', cost=None)
        self.graph.connect(vertexid1='v3', vertexid2='v5', cost=None)
        self.graph.connect(vertexid1='v4', vertexid2='v5', cost=None)
        self.assertEquals(self.graph.isRegular(), True, 'should return false a first attempt')

    def testIfItIsCompleteGraph(self):
        self.graph.connect(vertexid1='v3', vertexid2='v4', cost=None)
        self.graph.connect(vertexid1='v3', vertexid2='v5', cost=None)
        self.graph.connect(vertexid1='v4', vertexid2='v5', cost=None)
        self.assertEquals(self.graph.isComplete(), True, 'should return false a first attempt')

    def testIfItIsCompleteGraphAfterAnotherConnection(self):
        self.graph.connect(vertexid1='v3', vertexid2='v4', cost=None)
        self.graph.connect(vertexid1='v3', vertexid2='v5', cost=None)
        self.graph.connect(vertexid1='v4', vertexid2='v5', cost=None)
        self.graph.connect(vertexid1='v4', vertexid2='v4', cost=None)
        self.assertEquals(self.graph.isComplete(), False,
                          'this really should fail because we just added an adjacency to v4 itself')

    def testFindTransitiveClosure(self):
        newGraph = Graph()
        newGraph.addVertex(1)
        newGraph.addVertex(2)
        newGraph.connect(vertexid1=1, vertexid2=2, cost=None)
        testTransitiveClosureSet = newGraph.transitiveClosure(vertexid=1)
        self.assertTrue(1 in testTransitiveClosureSet and
                        2 in testTransitiveClosureSet,
                        'should be inside the transitive closure')
        del newGraph

    def testIfItIsRelational(self):
        self.assertTrue(self.graph.isRelational(), 'this graph in this state should not be relational because\
v4 and v5 dont have connection in between')

        # diconnect some vertexes and try the test again
        self.graph.disconnect(vertexid1='v1', vertexid2='v2')
        self.graph.disconnect(vertexid1='v1', vertexid2='v3')
        self.graph.disconnect(vertexid1='v2', vertexid2='v2')
        self.graph.disconnect(vertexid1='v2', vertexid2='v3')
        self.assertFalse(self.graph.isRelational(), 'should not be relational')

    def testIfItIsTree(self):
        self.assertFalse(self.graph.isTree(), 'should not be a tree')

        # (1)  (2)  (3)
        #    \  |  /
        #     \ | /
        #      (4)
        #       |
        #      (5)
        newGraph = Graph()
        newGraph.addVertex(1)
        newGraph.addVertex(2)
        newGraph.addVertex(3)
        newGraph.addVertex(4)
        newGraph.addVertex(5)
        newGraph.connect(vertexid1=1, vertexid2=4, cost=None)
        newGraph.connect(vertexid1=2, vertexid2=4, cost=None)
        newGraph.connect(vertexid1=3, vertexid2=4, cost=None)
        newGraph.connect(vertexid1=5, vertexid2=4, cost=None)
        self.assertTrue(newGraph.isTree(), 'should be a tulip right, its a flower sort of...')
        del newGraph

    def testConvertEdgesListToGraph(self):
        edges_map = [[ 2 , 0 , 44 ],
                     [ 2 , 1 , 57 ],
                     [ 3 , 1 , 73 ],
                     [ 3 , 2 , 56 ],
                     [ 4 , 0 , 74 ],
                     [ 4 , 1 , 51 ],
                     [ 4 , 2 , 66 ],
                     [ 4 , 3 , 71 ],
                     [ 5 , 2 , 70 ],
                     [ 5 , 4 , 62 ],
                     [ 6 , 0 , 34 ],
                     [ 6 , 1 , 74 ],
                     [ 6 , 2 , 58 ],
                     [ 6 , 3 , 80 ],
                     [ 6 , 4 , 87 ],
                     [ 6 , 5 , 76 ],
                     [ 2,  4 , 0  ]]
        newGraph = Graph.newGraphFromEdgesMap(edges_map)

        # this test the graph constrution from a mapping of edges with its costs
        for index in range(len(edges_map) - 1):
            v1, v2, cost = edges_map[index]
            self.assertTrue(cost == newGraph.vertexAdjacencies(v1).get(v2).getcost(),
                            'test graph\'s consistence in costs and coesion in connections')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
