from Chronometer import timeit
from FloydWarshall import FloydWarshall
from Graph import Graph
from Dijkstra import Dijkstra
from enum import Enum

class AlgorithmType(Enum):
    DIJKSTRA = 'DIJKSTRA'
    FLOYD = 'FLOYD'

class AmbulancePositionSystemValidationError(Exception):
    pass

class AmbulancePositionSystem(object):
    """<h1>Simple Graph Class Impl of the Medical Center's problem</h1>
    <p>This class implement a Graph for the Medical Center's problem
    Its structured with basic functions and extends FloydWarshall actions.</p>"""

    def __init__(self, graph, name, emergency, localizations, algorithm_type):
        if not isinstance(graph, Graph):
            raise AmbulancePositionSystemValidationError('TypeGraph error, it must be a map of TypeGraph')
        self.graph = graph
        self.name = name
        self.emergency = emergency
        self.localizations = localizations
        self.routes = {}
        self.distances = {}
        self.algorithm_type = algorithm_type

        # this is done to initialize the indexes of theses arrays
        # so we can store the results of the minimun costs paths
        self.path = [[x] for x in self.localizations]
        self.costs = [[x] for x in self.localizations]

    def name(self, name):
        self.name = name

    def __str__(self):
        strgraph = str(self.graph)
        strdist = '\n'
        strroutes = '\n'
        for i in range(len(self.distances)):
            for j in range(len(self.distances)):
                strdist += " {:4} ".format(self.distances[i][j])
                strroutes += " {:4} ".format(self.routes[i][j])
            strdist += '\n'
            strroutes += '\n'
        return 'Proximity Map: {:4}\n\
Distances Matrix: {}\n\
Routes Matrix: {}\n\
Path to Emergency: {}\n\
Costs to Emergency: {}\n\
Hospital Name: {}\n\
Where is the emergency at? {}\n\
Where the Hospital is located at? {}\n'.format(strgraph, strdist, strroutes, self.path, self.costs,
                                               self.name, self.emergency, self.localizations) + '\n'

    @timeit
    def buildMatrixDistancesAndMAtrixRoutes(self):
        if (self.algorithm_type == AlgorithmType.DIJKSTRA):
            dijkstra = Dijkstra()
            self.distances, self.routes = dijkstra.dijkstra(self.graph, self.localizations, self.emergency)
            del dijkstra
        elif (self.algorithm_type == AlgorithmType.FLOYD):
            floyd_warshall = FloydWarshall()
            self.distances, self.routes = floyd_warshall.pathReconstruction(self.graph)
            del floyd_warshall

    """
    The usage is basically when invoking this
    function the caller wants to find the path
    with the costs related between A and B.

    If B is direct related to A them the Algorithm should run O(1)
    If the path between B and A is n arcs (or edges) them the algorithm runs O(n^2)
    where n is the number of arcs, because the worst case scenario the function will
    run through all the distances matrix and routes matrix to gather all the path and costs.

    <code>
    Algorithm PathInBetween(nodeA, nodeB):
        if self.routes[nodeA][nodeB] is None:
            return []
        self.path = [u]
        while u is not v
            u = self.routes[u][v]
            self.path.append(u)
        return path
    </code>
    """
    @timeit
    def shortestPath(self):
        #indexNodeDestination = self.emergency
        #for index in range(len(self.localizations)):
        #    indexNodeOrigin = self.localizations[index]
        #    while ((indexNodeOrigin != indexNodeDestination) or (indexNodeOrigin == -1 or indexNodeDestination == -1)):
        #        indexNodeOrigin = self.routes[indexNodeOrigin][indexNodeDestination]
        #        print(indexNodeOrigin)
        #        print(indexNodeOrigin, indexNodeDestination)
        #        self.path[index].append(indexNodeOrigin)
        #        self.costs[index].append(self.distances[indexNodeOrigin][indexNodeDestination])
        #return self.routes
        pass
