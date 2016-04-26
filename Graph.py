from Chronometer import timeit
import time

class GraphValidationError(Exception):
    pass


class Vertex(object):

    def __init__(self, vertexid):
        self.vertexid = vertexid
        self.name = 'vertex_object_' + str(time.clock())
        # this gives better control of the graph
        self.adjacencies = {}

    """
    This method above is useful to convert a list of lists
    graph-like structure to fit inside this Graph klazz data
    structure
    
    @param edges_map: List of lists graph like structure
    with the elements being a list like this [v1, v2, cost]
    """
    def newGraphFromEdgesMap(self, edges_map):
        graph = Graph()
        for edge in edges_map:
            graph.addVertex(vertexid=edge[0])
            graph.addVertex(vertexid=edge[1])
            graph.connect(vertexid1=edge[0], vertexid2=edge[1])
        return graph

    # add a name to the vertex (the name is like a property)
    def nameit(self, name):
        self.name = name

    # add a property to the vertex and give it a value
    def addAdjacency(self, vertexid):
        if vertexid in self.adjacencies:
            self.adjacencies[vertexid] = vertexid

    # remove an adjacency of this vertex but do not raise KeyError
    # is the element does not exists in the adjacencies set
    def removeAdjacency(self, vertexid):
        if vertexid in self.adjacencies:
            del self.adjacencies[vertexid]

class Graph(object):
    """
    <h1>Simple Graph Class</h1>
    <p>This class implement a Graph
    structure with basic funcions.</p>

    v1 -> v3
    v2 -> v4
    v3 -> v5 (impossible since v5 doesnt exist)
    v4 -> v2

    once Graph insert vertex we have to just get the
    size of the dictionary to count how much vertexes
    """

    def __init__(self):
        self.size = 0
        self.graph = {}
        self.name = 'graph_object_' + str(time.clock())

    def nameit(self, name):
        self.name = name

    """
    Basic actions
    """

    # adds a new vertex (which is a node) to the graph dictionary
    @timeit
    def addVertex(self, vertexid):
        if not vertexid in self.graph:
            if isinstance(vertexid, Vertex):
                if not vertexid.vertexid in self.graph:
                    self.graph[vertexid] = vertexid
                    self.size = self.size + 1
                else:
                    raise GraphValidationError('This vertex already exists in the graph')
            else:
                self.graph[vertexid] = Vertex(vertexid)
                self.size = self.size + 1
        else:
            raise GraphValidationError('This vertex already exists in the graph')

    # removes a specific vertex (which is a node)  to the graph dictionary
    # it also removes all its conections
    @timeit
    def removeVertex(self, vertexid):
        # Python dict doesnt not consider None as being of type EmptySet element
        if vertexid in self.graph:
            for adjacency in self.getVertex(vertexid).adjacencies:
                self.getVertex(adjacency).removeAdjacency(vertexid)
            del self.graph[vertexid]
            self.size = self.size - 1
        else:
            raise GraphValidationError('Vertex could not be of NoneType')

    # connect node v1 to node v2
    # v1 and v2 must exist in order to connect
    # the order matter here, what i mean is that
    # v1 will be predecessor of v2 and
    # v2 will be sucessor of v1
    @timeit
    def connect(self, vertexid1, vertexid2):
        if vertexid1 in self.graph and vertexid2 in self.graph:
            self.graph.get(vertexid1).adjacencies[vertexid2] = vertexid2
            self.graph.get(vertexid2).adjacencies[vertexid1] = vertexid1
            return True
        else:
            return False

    @timeit
    def disconnect(self, vertexid1, vertexid2):
        if vertexid1 in self.graph and vertexid2 in self.graph:
            # when removing adjacency of v2 onto v1, its also
            # needed to be removed a existing adjancency of v1
            # onto v2 the same logic apply to the connection
            self.graph[vertexid1].removeAdjacency(vertexid2)
            self.graph[vertexid2].removeAdjacency(vertexid1)
            return True
        else:
            return False

    # return the number of nodes that are present in the graph
    def graphMagnitude(self):
        return len(self.graph)

    @timeit
    def graphVertexes(self):
        return self.graph.keys()

    @timeit
    def getVertex(self, vertexid):
        if vertexid in self.graph:
            return self.graph.get(vertexid)
        else:
            return None

    @timeit
    def vertexAdjacencies(self, vertexid):
        """
        This method is really useful on this point of view
        the Graph klazz has control of his vertexes's adjacencies
        Of couse this method could be in the Vertex klazz, it doesnt
        really matters. This method returns the adjacency set of a
        vertex. The method get the vertex in O(1) time, because Graph
        use self.graph = {} (a dictionary). In other words this klazz
        make use of the properties of dictionary hashing mechanisms.
        """
        if vertexid in self.graph:
            return self.getVertex(vertexid).adjacencies
        else:
            raise GraphValidationError('Verify if vertexid={} exists before to get its adjacencies'.format(vertexid))

    @timeit
    def vertexMagnitude(self, vertexid):
        if vertexid in self.graph:
            return len(self.getVertex(vertexid).adjacencies)
        else:
            raise GraphValidationError('Verify if vertexid={} exists before to get its adjacencies'.format(vertexid))

    """
    Derivated actions
    """

    def isRegular(self):
        node = list(self.graph.values())[0]
        test = len(node.adjacencies)
        for vertexid in self.graph:
            if (test != self.vertexMagnitude(vertexid)):
                return False
        return True

    def isComplete(self):
        n = self.size - 1
        for vertexid in self.graph:
            if (n != self.vertexMagnitude(vertexid)):
                return False
        return True

    def transitiveClosure(self, vertexid):
        visited = set()
        self.__findTransitiveClosure(vertexid, visited)
        return visited

    def __findTransitiveClosure(self, vertexid, visited):
        visited.add(vertexid)

        for adjacency in self.vertexAdjacencies(vertexid):
            if adjacency not in visited:
                self.__findTransitiveClosure(adjacency, visited)

    """
    [relational] means in portuguese: relacionado, relativo,
    conexo, aparentado, ligado. Verify if exists at least one
    way between every pair of nodes in the graph
    """
    def isRelational(self):
        node = list(self.graph.values())[0]
        for vertexid in self.graphVertexes():
            if vertexid not in self.transitiveClosure(node.vertexid):
                return False
        return True

    """
    Please have a look at https://en.wikipedia.org/wiki/Tree_(graph_theory)
    """
    def isTree(self):
        visited = set()
        node = list(self.graph.values())[0]
        return self.isRelational() and not self.__haveCycleWith(node.vertexid, node.vertexid, visited)

    def __haveCycleWith(self, sucessor, predecessor, visited):
        # base case scenario
        if sucessor in visited:
            return True

        visited.add(sucessor)

        for adjacency in self.vertexAdjacencies(sucessor):
            if adjacency is not predecessor:
                if self.__haveCycleWith(adjacency, sucessor, visited):
                    return True

        visited.remove(sucessor)

        return False

    def __removeCycle(self, sucessor, predecessor, visited):
        if sucessor in visited:
            self.disconnect(vertexid1=sucessor.vertexid, vertexid2=predecessor.vertexid)
            return True

        visited.add(sucessor)

        for adjacency in self.vertexAdjacencies(sucessor):
            if adjacency is not predecessor:
                if self._removeCiclo(adjacency, sucessor, visited):
                    return True
        return False
