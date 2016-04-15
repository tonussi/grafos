# encoding:utf-8
from Graph import Graph
from FileReader import FileReader
from RandomGraphGenerator import RandomGraphGenerator
import sys, getopt, os

# v1 -> v2 custo
#  1 ->  2  1000     
#  2 ->  4  1000
#  3 ->  1  1000
#  4 ->  2  1000

def main(argv):
	graphs_directory = 'dat'
	graphs_list = []

	arestas = FileReader.listGraphsInDirectory(graphs_directory)

	for p in arestas:
		graphs_list = FileReader.readFile(p)

	print (graphs_list)

	set_of_edges = RandomGraphGenerator.random_regular_graph(4, 10)
	print RandomGraphGenerator.convertSetToDict(set_of_edges)

	graph = Graph({'hospitalA': [1, 1, 3]})
	graph.addEdge('hospitalB')
	graph.addAdjacency('hospitalB', 2)
	graph.addAdjacency('hospitalB', 2)
	graph.addAdjacency('hospitalB', 4)
	print ('hospitalB: ', graph.getEdge('hospitalB'))
	print ('hospitalA: ', graph.getEdge('hospitalA'))

if __name__ == '__main__':
   main(sys.argv[1:])
