from Chronometer import timeit
import time

class GraphValidationError(Exception):
    pass


class Vertex(object):

    def __init__(self, vertexid):
        self.vertexid = vertexid
        self.sucessor = None
        self.predecessor = None
        self.name = 'vertex_object_' + str(time.clock())

        # this gives better control of the graph
        self.adjacencies = set()

    # add a name to the vertex (the name is like a property)
    def nameit(self, name):
        self.name = name

    # add a property to the vertex and give it a value
    def addAdjacency(self, vertexid):
        self.adjacencies.add(vertexid)

    # remove an adjacency of this vertex but do not raise KeyError
    # is the element does not exists in the adjacencies set
    def removeAdjacency(self, vertexid):
        self.adjacencies.discard(vertexid)

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
    def removeVertex(self, v):
        if v is not None:
            del self.graph[v]
        else:
            raise GraphValidationError('Vertex could not be of NoneType')

    # remove a edge by id including all its conections
    @timeit
    def removeEdge(self, v):
        if v in self.graph:
            del self.graph[v]

    # connect node v1 to node v2
    # v1 and v2 must exist in order to connect
    # the order matter here, what i mean is that
    # v1 will be predecessor of v2 and
    # v2 will be sucessor of v1
    @timeit
    def connect(self, vertexid1, vertexid2):
        if vertexid1 in self.graph and vertexid2 in self.graph:
            self.graph.get(vertexid1).sucessor = Vertex(vertexid2)
            self.graph.get(vertexid1).addAdjacency(vertexid2)
            self.graph.get(vertexid2).predecessor = Vertex(vertexid1)
            self.graph.get(vertexid1).addAdjacency(vertexid1)
        else:
            raise GraphValidationError('Verify if vertexid1 and vertexid2 exists before try to made a connection')

    @timeit
    def disconnect(self, vertexid1, vertexid2):
        if vertexid1 in self.graph and vertexid2 in self.graph:
            del self.graph[vertexid1].sucessor
            del self.graph[vertexid2].predecessor
        else:
            raise GraphValidationError('Verify if vertexid1 and vertexid2 exists before try to made a connection')

    # return the number of nodes that are present in the graph
    def magnitude(self):
        return len(self.graph)

    @timeit
    def vertexes(self):
        res = set()
        for node in self.graph:
            res.add(node)
        return res

    @timeit
    def getVertex(self, vertexid):
        return self.graph.get(vertexid)

    # timeit
    def getAdjacencies(self, vertexid):
        if vertexid in self.graph:
            return self.getVertex(vertexid).adjacencies
        else:
            raise GraphValidationError('Verify if vertexid1 exists before to get its adjacencies')

