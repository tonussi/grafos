from Chronometer import timeit

class FloydWarshall:
    '''
    This class implements the function to extract the matrices
    of Routes and matrices of Adjacency from a given matrix that
    represents a Graph
    '''

    @timeit
    def floydWarshallWithPathReconstruction(self, dist, next, V):
        for (u,v) in V:
            dist[u][v] = self.weight(u,v)
            next[u][v] = v
        for k in range(1,len(V)):
            for i in range (1, len(V)):
                for j in range(1, len(V)):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next[i][j] = next[i][k]

    def weight(self, u, v):
        pass

    def path(self, next, u, v):
        if next[u][v] is None:
            return []
        path = [u]
        while u is not v:
            u = next[u][v]
            path.append(u)
            return path
