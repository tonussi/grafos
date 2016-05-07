from Chronometer import timeit
from FloydWarshall import FloydWarshall
from Graph import Graph
from Dijkstra import Dijkstra

class AlgorithmTypeEnum:
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
        res  = 'Proximity Map: {:4}\n'.format(strgraph)
        res += 'Distances Matrix: {}\n'.format(strdist)
        res += 'Routes Matrix: {}\n'.format(strroutes)
        res += 'Path to Emergency: {}\n'.format(self.path)
        res += 'Costs to Emergency: {}\n'.format(self.costs)
        res += 'Hospital Name: {}\n'.format(self.name)
        res += 'Where is the emergency at? {}\n'.format(self.emergency)
        res += 'Where the Hospital is located at? {}\n'.format(self.localizations)
        return res

    @timeit
    def buildMatrixDistancesAndMAtrixRoutes(self):
        if (self.algorithm_type == AlgorithmTypeEnum.DIJKSTRA):
            dijkstra = Dijkstra()
            for l in self.localizations:
                self.dijkstra = dijkstra.dijkstra(self.graph, l, self.emergency)
            del dijkstra
        elif (self.algorithm_type == AlgorithmTypeEnum.FLOYD):
            floyd_warshall = FloydWarshall()
            self.distances, self.routes = floyd_warshall.pathReconstruction(self.graph)
            del floyd_warshall

    @timeit
    def shortestPath(self):
        if (self.algorithm_type == AlgorithmTypeEnum.DIJKSTRA):
            pass
        elif (self.algorithm_type == AlgorithmTypeEnum.FLOYD):
            indexNodeDestination = self.emergency
            for index in range(len(self.localizations)):
                indexNodeOrigin = self.localizations[index]
                while ((indexNodeOrigin is not indexNodeDestination) or (indexNodeOrigin == -1 or indexNodeDestination == -1)):
                    indexNodeOrigin = self.routes[indexNodeOrigin][indexNodeDestination]
                    self.path[index].append(indexNodeOrigin)
                    self.costs[index].append(self.distances[indexNodeOrigin][indexNodeDestination])
            return self.routes
