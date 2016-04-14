class Graph(object):
	"""<h1>Simple Graph Class</h1>
	<p>This class implement a Graph
	structure with basic funcions.</p>"""

	def __init__(self, arg):
		super(Graph, self).__init__()
		self.graph = arg

	def addEdge(self, v):
		self.graph[v] = []

	def removeEdge(self, v):
		if v in self.graph: 
			del self.graph[v]

	def addAdjacency(self, v, a):
		self.graph[v].append(a)

	def getEdge(self, v):
		return self.graph[v]
