from Graph import Graph
from HeapSort import HeapSort

INFINITE = 99999

class Dijkstra:

	"""
	This is the dijkstra method to find the shortest path
	@param graph: a graph of type Graph
	@param distancesFromS: all adjacencies of the starting node
	@param s: target node
	"""
	def dijkstra(self, graph, distancesFromS, s):
		heapsort = HeapSort()

		if s not in graph.graph:
			raise

		distances = {}
		distances[s] = 0

		for v in distancesFromS.adjacencies.keys:
			if (v != s):
				distances[v] = INFINITE

		orderedVertexes = []
		q = distancesFromS

		while len(q) != 0:
			u = min(q, key=q.get)
			del q[u]

			orderedVertexes.append(u)
			heapsort.heapsort(orderedVertexes, len(orderedVertexes))

			for v in graph.vertexAdjacencies(u).keys:
				if distances[v] > distances[u] + graph.vertexAdjacencies(u)[v]:
					distances[v] = distances[u] + graph.vertexAdjacencies(u)[v]
		return distances
