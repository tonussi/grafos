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

        self.graph          = graph
        self.name           = name
        self.emergency      = emergency

        # ambulance medical center localization fixed nodes
        self.localizations  = localizations

        self.routes         = {}
        self.distances      = {}

        self.algorithm_type = algorithm_type

        # this is done to initialize the indexes of theses arrays
        # so we can store the results of the minimun costs paths

        # will store 2 costs and 2 paths for 2 localizations
        self.path  = [[x] for x in self.localizations]
        self.costs = [[x] for x in self.localizations]

    def name(self, name):
        self.name = name

    def __str__(self):
        strgraph  = str(self.graph)
        strdist   = '\n'
        strroutes = '\n'
        strpath   = '\n'
        strcost   = '\n'

        for i in range(len(self.distances)):
            for j in range(len(self.distances)):
                strdist   += " {:4} ".format(self.distances[i][j])
                strroutes += " {:4} ".format(self.routes[i][j])
            strdist   += '\n'
            strroutes += '\n'

        for i in self.path:
            for j in i:
                strpath += " {:2} ".format(j)
            strpath += '\n'

        for i in self.costs:
            for j in i:
                strcost += " {:2} ".format(j)
            strcost += '\n'


        res  = 'Proximity Map:                    {}\n'.format(strgraph)
        res += 'Distances Matrix:                 {}\n'.format(strdist)
        res += 'Routes Matrix:                    {}\n'.format(strroutes)
        res += 'Path to Emergency:                {}\n'.format(strpath)
        res += 'Costs to Emergency:               {}\n'.format(strcost)
        res += 'Hospital Name:                    {}\n'.format(self.name)
        res += 'Where is the emergency at?        {}\n'.format(self.emergency)
        res += 'Where the Hospital is located at? {}\n'.format(self.localizations)
        return res

    @timeit
    def executeAlgorithm(self):
        if (self.algorithm_type == AlgorithmTypeEnum.DIJKSTRA):
            dijkstra = Dijkstra()

            # in the case for dijkstra we have to run the procedure twice
            for index in range(len(self.localizations)):
                self.path[index] = dijkstra.dijkstra(self.graph, self.localizations[index], self.emergency)
            del dijkstra

        elif (self.algorithm_type == AlgorithmTypeEnum.FLOYD):

            floyd_warshall = FloydWarshall()
            self.distances, self.routes = floyd_warshall.pathReconstruction(self.graph)
            del floyd_warshall

    @timeit
    def constructShortestPath(self):
        if (self.algorithm_type == AlgorithmTypeEnum.DIJKSTRA):
            for index in len(self.path - 1):

                # 1) this line is to pick get the adjacencies of a node in the graph

                # 2) when we have the adjacencies then we pick the next node AND this next node
                #    must be in the adjacencies otherwise there will be some kind of error

                # 3) dijkstra find the path with less cost then other paths

                # 4) if dijkstra finds the PATH then when we pick a node in this path
                #    the next path have must be in the adjacencies of the predecessor
                self.path[index] = self.graph.vertexAdjacencies(self.path[index]).get(self.path[index + 1]).getcost()

        elif (self.algorithm_type == AlgorithmTypeEnum.FLOYD):
            indexNodeDestination = int(self.emergency)

            for index in range(len(self.localizations)):
                indexNodeOrigin = int(self.localizations[index])

                for i in range(len(self.distances)):
                    for j in range(len(self.distances)):
                        temp = self.routes[i][j]
                        if (temp == indexNodeDestination != indexNodeOrigin):
                            self.costs[index].append(self.distances[i][j])
                            self.path[index].append(temp)
