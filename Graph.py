from FloydWarshall import FloydWarshall
from time import sleep

class Graph:
	"""<h1>Simple Graph Class</h1>
	<p>This class implement a Graph
	structure with basic funcions.</p>"""

	def __init__(self, graphdict={}, name=''):
		self.graph = graphdict
		self.name = name

	def name(self, name):
		self.name = name

	def addEdge(self, v):
		self.graph[v] = []
	
	def addEdges(self, edges):
		for e in edges:
			self.graph[e]

	def removeEdge(self, v):
		if v in self.graph: 
			del self.graph[v]

	def addAdjacency(self, v, a):
		self.graph[v].append(a)

	def getEdge(self, v):
		return self.graph[v]

	def findBestWayToMedicalCenterRoute(self):
		# TODO: Usar funcionalidades do floyd warshall
		# para construir esse metodo de achar o melhor
		# caminho
		sleep(2)