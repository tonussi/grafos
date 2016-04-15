# encoding:utf-8
from Graph import Graph
from FileReader import FileReader
from Hospital import Hospital
from RandomGraphGenerator import RandomGraphGenerator
import sys, getopt, os
from FloydWarshall import FloydWarshall
import threading, random

# v1 -> v2 custo
#  1 ->  2  1000
#  2 ->  4  1000
#  3 ->  1  1000
#  4 ->  2  1000

class SamuThread(threading.Thread):
    def __init__(self, hospital, threadID, name, routes):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.routes = routes
        self.hospital = hospital
    def run(self):
        threadLock.acquire()
        self.hospital.findBestWayToMedicalCenterRoute()
        threadLock.release()

threadLock = threading.Lock()
threads = []

def main(argv):
	graphs_directory = 'dat'
	graphs_list = []

	arestas = FileReader.listGraphsInDirectory(graphs_directory)

	for p in arestas:
		graphs_list.append(FileReader.readFile(p))
	
	for g in graphs_list:
		print g

	graph_generator = RandomGraphGenerator()

	for i in [10, 20, 25, 50, 100, 500]:
		set_of_edges = graph_generator.random_regular_graph(2, i)
		dict_of_edges = graph_generator.convertSetToDict(set_of_edges)
		FileReader.writef('results' + os.path.sep + 'results_' + str(i) + '_nodes' + '.dat', str(dict_of_edges))

	hospitalA = Hospital()
	hospitalB = Hospital()

	# Create new threads
	thread1 = SamuThread(hospitalA, 0x1, "Operador Samu 1", [1, 2, 3])
	thread2 = SamuThread(hospitalB, 0x2, "Operador Samu 2", [3, 2, 1])

	# Start new Threads
	thread1.start()
	thread2.start()

	# Add threads to thread list
	threads.append(thread1)
	threads.append(thread2)

	# Wait for all threads to complete
	for t in threads:
		t.join()

	# graph = Graph({'hospitalA': [1, 1, 3]})
	# graph.addEdge('hospitalB')
	# graph.addAdjacency('hospitalB', 2)
	# graph.addAdjacency('hospitalB', 2)
	# graph.addAdjacency('hospitalB', 4)
	# print ('hospitalB: ', graph.getEdge('hospitalB'))
	# print ('hospitalA: ', graph.getEdge('hospitalA'))

if __name__ == '__main__':
   main(sys.argv[1:])
