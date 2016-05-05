from Graph import Graph
import sys

def Dijkstra(graph, distancesFromS, s):
	distances = {}
	distances[s] = 0
	for v in distancesFromS.keys:
		if (v != s):
			distances[v] = sys.maxint
	orderedVertexes = []
	q = distancesFromS
	while len(q) != 0:
		u = min(q, key=q.get)
		del q[u]
		orderedVertexes.append(u)
		for v in graph.vertexAdjacencies(u).keys:
			if distances[v] > distances[u] + graph.vertexAdjacencies(u)[v]:
				distances[v] = distances[u] + graph.vertexAdjacencies(u)[v]
	return distances
		
		
