from Chronometer import timeit
from PriorityQueue import PriorityQueue

from heapq import heappop, heappush

INFINITE = 99999

class Dijkstra:

    """
    @summary: Find shortest paths from the  start vertex to all
              vertices nearer than or equal to the end.
    @see: https://www.youtube.com/watch?v=CHvQ3q_gJ7E

    @param graph: a graph of type Graph
    @param distancesFromS: all adjacencies of the starting node
    @param s: target node
    """
    @timeit
    def dijkstra(self, G, start, end=None):

        D = {} # dictionary of final distances
        P = {} # dictionary of predecessors
        Q = PriorityQueue() # estimated distances of non-final vertices
        Q[start] = 0 # add zero cost

        for v in Q:
            D[v] = Q[v]

            if v == end:
                break

            for w in G.getVertex(v).adjacencies:
                vwLength = D.get(v) + G.vertexAdjacencies(v).get(w).getcost()

                if w in D:
                    if vwLength < D.get(w):
                        raise ValueError("Dijkstra: found better path to already-final vertex")
                elif w not in Q or vwLength < Q.get(w):
                    Q[w] = vwLength
                    P[w] = v

        return D, P

    """
    Find shortest paths from the  start vertex to all vertices nearer than or equal to the end.

    @param graph: a graph of type Graph
    @param distancesFromS: all adjacencies of the starting node
    @param s: target node
    """
    @timeit
    def dijkstraWithBuiltinHeap(self, G, start, end=None):
        D = {} # dictionary of final distances
        P = {} # dictionary of predecessors
        Q = [(0, None, start)] # heap of (est.dist., pred., vert.)
        while Q:
            dist, pred, v = heappop(Q)
            if v in D:
                continue # tuple outdated by decrease-key, ignore
            D[v] = dist
            P[v] = pred
            for w in G.getVertex(v).adjacencies:
                heappush(Q, (D[v] + G.vertexAdjacencies(v).get(w).getcost(), v, w))
        return (D,P)