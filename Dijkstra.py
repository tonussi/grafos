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
	def dijkstra(self, graph, start, end):
		if end not in graph.graph:
			raise

		distances = {}
		distances[end] = 0

		for vertexid in graph.vertexAdjacencies(start):
			if (vertexid != end):
				distances[vertexid] = INFINITE

		orderedVertexes = []
		q = start

		while len(q.adjacencies) != 0:
			u = min(q, key=q.get)
			del q[u]

			orderedVertexes.append(u)
			HeapSort.heapsort(orderedVertexes, len(orderedVertexes))

			for vertexid in graph.vertexAdjacencies(u).keys:
				if distances[vertexid] > distances[u] + graph.vertexAdjacencies(u)[vertexid]:
					distances[vertexid] = distances[u] + graph.vertexAdjacencies(u)[vertexid]
		return distances
