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

        for k in range(1, edges_size):
            for i in range(1, edges_size):
                if i is not k:
                    for j in range(1, edges_size):
                        if j is not k:
                            # d(i,j) = min{d(i, k), d(i,j) + d(j,k)}
                            distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])
                            if distances[i][j] > distances[i][k] + distances[k][j]:
                                routes[i][j] = k

        return distances, routes
