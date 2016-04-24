from Graph import Graph
from FloydWarshall import FloydWarshall


class Hospital(Graph):
    """<h1>Simple Graph Class Impl of the Medical Center's problem</h1>
    <p>This class implement a Graph for the Medical Center's problem
    Its structured with basic functions and extends FloydWarshall actions.</p>"""

    def __init__(self, graph, name, emergency, localization):
        self.graph = graph
        self.name = name
        self.emergency = emergency
        self.localization = localization
        self.routes = {}
        self.distances = {}

    def name(self, name):
        self.name = name

    def __str__(self):
        strgraph = '\n'
        for i in range(len(self.graph) - 1):
            strgraph += 'edge {:2}: {:2} -> {:2}: {:2} (miles)\n'.format(
                i,
                self.graph[i][0],
                self.graph[i][1],
                self.graph[i][2])
        strgraph += 'edge {:2}: {:2} -> {:2}: {:2} (hospital location)\n'.format(
            len(self.graph), self.graph[-1][0], self.graph[-1][1], self.graph[-1][2])
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
Hospital Name: {}\n\
Where is the emergency at? {}\n\
Where the Hospital is located at? {}\n'.format(strgraph, strdist, strroutes, self.name, self.emergency, self.localization) + '\n'

    def getRoute(self):
        return 'Best route I could find is: {}'.format(self.routes)

    def buildMatrixDistancesAndMAtrixRoutes(self):
        floyd_warshall = FloydWarshall()
        self.distances, self.routes = floyd_warshall.pathReconstruction(self.graph)
        del floyd_warshall

    def pathInBetween(self, u, v):
        if self.routes[u][v] is None:
            return []
        path = [u]
        while u is not v:
            u = self.routes[u][v]
            path.append(u)
        return path
