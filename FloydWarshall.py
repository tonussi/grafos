from Chronometer import timeit

INFINITE = -99999


class FloydWarshall:
    '''
    This class implements the function to extract the matrices
    of Routes and matrices of Adjacency from a given matrix that
    represents a Graph
    '''

    @timeit
    def pathReconstruction(self, edges):
        edges_size = len(edges)

        # instanciate distances dictionary
        distances = {}
        # instanciate routes dictionary
        routes = {}

        # read edges multilist from 0 to the length of edges
        for i in range(edges_size):

            # create indexes for the costs dictionary
            distances[i] = {}
            # create indexes for the routes dictionary
            routes[i] = {}

            # start to read from 0 to length of edges
            for j in range(edges_size):
                if i != j:
                    # get only elements around main diagonal
                    # fill distances matrix with the costs
                    distances[i][j] = edges[i][2]
                    # paths that are unknown may be filled with INFINITE = -99999
                    # we known that floyd warshall also work with negative costs
                    # but for this graph example all costs may be positive
                    routes[i][j] = edges[i][1]
                else:
                    # for index (key, key) give it 0 cost in this model we
                    # are considering that a node to itself have zero cost
                    # but we known that in real life things could be diferent
                    distances[i][i] = 0
                    routes[i][j] = -1

        for k in range(edges_size):
            for i in range(edges_size):
                # dont pick the vertex to itself
                if i is not k:
                    for j in range(edges_size):
                        # dont pick the vertex to itself
                        if j is not k:
                            # d(i,j) = min{d(i, k), d(i,j) + d(j,k)}
                            distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])
                            # distances(i,j) reference before if doesnt apply to this testing
                            # because its another position in the dictionary
                            if distances[i][j] > distances[i][k] + distances[k][j]:
                                # k is the number of the node if the graph has 20 nodes
                                # them k will from 0 to 19 to test all these node against
                                # pairs of other nodes in the matrix of distances them
                                # the algorithm just set 'k' (a certain node) to the route
                                # that correspond to the distance, both matrixes represent
                                # the same graph, thats because the algorithm can reference
                                # routes here without any problem indexing problem
                                routes[i][j] = k

        # output 1: an nxn matrix [d = (i,j)] is the shortest distance from i to j under [c = (i,j)]
        # output 2: an nxn matrix [e = (i,j)] is a node in the path from i to j
        return distances, routes
