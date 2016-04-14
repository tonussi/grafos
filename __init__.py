from Graph import Graph

# v1 -> v2 custo
#  1 ->  2  1000     
#  2 ->  4  1000
#  3 ->  1  1000
#  4 ->  2  1000

def main():
	graph = Graph({'hospitalA': [1, 1, 3]})
	graph.addEdge('hospitalB')
	graph.addAdjacency('hospitalB', 2)
	graph.addAdjacency('hospitalB', 2)
	graph.addAdjacency('hospitalB', 4)
	print ('hospitalB: ', graph.getEdge('hospitalB'))
	print ('hospitalA: ', graph.getEdge('hospitalA'))

if __name__ == '__main__':
	main()
