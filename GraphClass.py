# -*- coding: utf-8 -*-
import random

class Graph:
	"""docstring for Graph"""
	def __init__(self):
			self.nodes = {}

	def addNode(self, nodeName):
		self.nodes[nodeName] = []

	def removeNode(self, nodeName):
		del self.nodes[nodeName]

	def connect(self, node1,node2):
		if(node2 not in self.nodes[node1]):
			self.nodes[node1].append(node2)

	def disconnect(self, node1,node2): #Desconecta os vertices v1 e v2 em G"
		if(node2 in self.nodes[node1]):
			self.nodes[node1].remove(node2)
	
	def order(self): #Retorna o número de vertices de G"
		return len(self.nodes)

	def nodesList(self): #"Retorna um conjunto contendo os vertices de G"
		return self.nodes.keys()

	def oneNode(self): #"Retorna um vertice qualquer de G"
		return self.nodes.keys()[random.randint(0, self.order() - 1)]

	def adjacents(self, nodeName): #	"Retorna um conjunto contendo os vertices adjacentes a v em G"
		return self.nodes[nodeName]

	def degree(self, nodeName): #"Retorna o número de vertices adjacentes a v em G"
		return len(adjacents)

	def isRegular(self):
		d = self.degree(self.oneNode())
		for n in self.nodesList():
			if (self.degree(n) != d):
				return false
		return true

	def isComplete(self):
		o = (self.order() - 1)
   		for n in self.nodesList():
   			if (self.degree(n) != o):
   				return false
   		return true

   	def fechoTransitivo(self, nodeName):
   		return self.procuraFechoTransitivo(self, nodeName, [])

   	def procuraFechoTransitivo(self, nodeName, visitedNodes):
   		ft = visitedNodes
   		visitedNodes.append(nodeName)
   		for n in self.adjacents(n): 
   			if (n not in visitedNodes):
				ft = ft + self.procuraFechoTransitivo(n,visitedNodes)
		return visitedNodes

	def isConnected(self):
		ft = self.fechoTransitivo(self.oneNode())
		for n in self.nodesList():
			if (n not in ft):
				return false
		return true

	def isTree(self):
		n = self.oneNode()
		return (self.isConnected() and self.hasCycleWith(n, n, []))

	def hasCycleWith(self, node, nodeBefore, visitedNodes):
		if (node in visitedNodes):
			return true
		visitedNodes.append(node)
		for n in self.adjacents(node):
			if (n != nodeBefore):
				if (self.hasCycleWith(n, node, visitedNodes)):
					return true
		visitedNodes.remove(node)
		return false


