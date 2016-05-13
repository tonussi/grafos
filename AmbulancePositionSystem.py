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

        if type(emergency) is not int:
            emergency = int(emergency)

        if emergency in self.graph.graph:
            self.emergency = emergency
        else:
            raise AmbulancePositionSystemValidationError('This EMERGENCY NODE = {} is not present in the graph map = {}, GRAPH => {}\n'.format(emergency, name, self.graph.graph.keys()))

        # choose two random vertexes in the graph to be the Hospital
        # where the ambulances are located at
        self.localizations = []
        self.localizations.append(self.graph.getRandomVertexId())
        self.localizations.append(self.graph.getRandomVertexId())

        self.routes = {}
        self.distances = {}

        self.algorithm_type = algorithm_type

        # this is done to initialize the indexes of theses arrays
        # so we can store the results of the minimun costs paths

        # will store 2 costs and 2 paths for 2 localizations
        self.path = [[x] for x in self.localizations]
        self.costs = [[x] for x in self.localizations]

    def name(self, name):
        self.name = name

    def __str__(self):
        
        strgraph = str(self.graph)
        strdist = '\nShortest Distances One:\n'
        strroutes = '\nShortest Routes One:\n'
        strpath = '\nShortest way (more readable) for ambulance one:\n'
        strcost = '\nShortest cost (more readable) for ambulance one:\n'

        if (self.algorithm_type == AlgorithmTypeEnum.DIJKSTRA):

            for local in self.localizations:

                for d in self.distances[local]:
                    strdist += "\t(Node:{:4}, Cost:{:4})\n".format(d, self.distances[local][d])
                strdist += '\n\nShortest Distances Two: \n\n'

                for r in self.routes[local]:
                    strroutes += "\t(Node:{:4}, Next Node:{:4})\n".format(r, self.routes[local][r])
                strroutes += '\n\nShortest Routes Two: \n\n'

        elif (self.algorithm_type == AlgorithmTypeEnum.FLOYD):

            for i in range(len(self.distances)):
                for j in range(len(self.distances)):
                    strdist += " {:4} ".format(self.distances[i][j])
                    strroutes += " {:4} ".format(self.routes[i][j])
                strdist += '\n'
                strroutes += '\n'

        for p in self.path:
            strpath += '\nThe shortest path (easy readable) for {}\n\t to go to the emergency at vertex position {}, is the following:\n\n'.format(self.name, self.emergency)
            strpath += '\t'
            for s in range(len(p) - 1):
                strpath += '{:4} -> '.format(s)
            strpath += '{:4}\n'.format(p[len(p)-1])

        if (self.algorithm_type == AlgorithmTypeEnum.DIJKSTRA):

            strcost += "\tSee Matrix Routes to Find out the Costs.\n"

        elif (self.algorithm_type == AlgorithmTypeEnum.FLOYD):

            for i in self.costs:
                for j in i:
                    strcost += " {:2} ".format(j)
                strcost += 'Shortest path for ambulance two:\n'

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

            # in the case for dijkstra we have to run the procedure twice
            for index in range(len(self.localizations)):

                d = Dijkstra()
                D, P = d.dijkstra(self.graph, self.localizations[index], self.emergency)

                self.distances[self.localizations[index]] = D
                self.routes[self.localizations[index]]    = P

        elif (self.algorithm_type == AlgorithmTypeEnum.FLOYD):

            floyd_warshall = FloydWarshall()

            self.distances, self.routes = floyd_warshall.pathReconstruction(self.graph)

    @timeit
    def constructShortestPath(self):

        if (self.algorithm_type == AlgorithmTypeEnum.DIJKSTRA):

            self.shortestPathDijkstra()

        elif (self.algorithm_type == AlgorithmTypeEnum.FLOYD):

            self.shortestPathFloyd()

    def shortestPathDijkstra(self):
        # 1) this line is to pick get the adjacencies of a node in the graph

        # 2) when we have the adjacencies then we pick the next node AND this next node
        # must be in the adjacencies otherwise there will be some kind of error

        # 3) dijkstra find the path with less cost then other paths

        # 4) if dijkstra finds the PATH then when we pick a node in this path
        #    the next path have must be in the adjacencies of the predecessor

        S1, S2 = self.localizations[0], self.localizations[1]
        R1, R2 = self.routes[S1], self.routes[S2]

        self.__solvePathOne(S1, R1)
        self.__solvePathTwo(S2, R2)

    def __solvePathOne(self, S1, R1):

        end = self.emergency
        Path = []
        while True:
            Path.append(end)
            if end == S1:
                break
            end = R1[end]
        Path.reverse()
        self.path[0] = Path

    def __solvePathTwo(self, S2, R2):

        end = self.emergency
        Path = []
        while True:
            Path.append(end)
            if end == S2:
                break
            end = R2[end]
        Path.reverse()
        self.path[1] = Path

    def shortestPathFloyd(self):

        indexNodeDestination = int(self.emergency)

        for index in range(len(self.localizations)):
            indexNodeOrigin = self.localizations[index]

            for i in range(len(self.distances)):
                for j in range(len(self.distances)):
                    temp = self.routes[i][j]
                    if (temp == indexNodeDestination != indexNodeOrigin):
                        self.path[index].append(temp)
