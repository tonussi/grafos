# encoding: utf-8

from Graph import Graph
from FileReader import FileReader
from AmbulancePositionSystem import AmbulancePositionSystem
from RandomGraphGenerator import RandomGraphGenerator

import sys
import getopt
import os
import threading

threads_list = []
list_of_ambulances = []
threadLock = threading.Lock()

class SamuOperatorSlave(threading.Thread):

    def __init__(self, ambulance, tid, name):
        threading.Thread.__init__(self)
        self.tid = tid
        self.name = name
        self.ambulance = ambulance

    def run(self):
        threadLock.acquire()
        self.ambulance.executeAlgorithm()
        self.ambulance.constructShortestPath()
        threadLock.release()

def exportNewRegularGraphsToDat(edgesArray=[10, 20, 50, 100, 500]):
    """
    This function exports to files 5 or more regular graph without crossing edges
    or also parallel edges.

    There will be files in dat directory with at least the number of nodes passed
    as parameter divided by 2 in edges.
    """
    graph_generator = RandomGraphGenerator()

    for i in edgesArray:
        set_of_edges = graph_generator.random_regular_graph(1, i)
        dict_of_edges = graph_generator.convertSetToOrderedDict(set_of_edges)
        FileReader.writef('dat' + os.path.sep + 'results_' + str(i) + '_nodes' + '.dat', 'edges=' + str(dict_of_edges))

def start_samu_threadings_floyd(edges_list, threads_number, accident_location):
    if len(accident_location) == 3:
        del accident_location[:1]
    else:
        raise

    index = 0
    for edges_map in edges_list:
        # Build the graph first them send the graph to the class ambulance
        graph_mapping=Graph.newGraphFromEdgesMap(edges_map, len(edges_map) - 1)
        list_of_ambulances.append(AmbulancePositionSystem(graph=graph_mapping,
            name="ambulance_ambulancia_" + str(index),
            emergency=accident_location[index],
            localizations=[edges_map[:1][0][0], edges_map[:1][0][1]],
            algorithm_type='FLOYD'))
        index = index + 1

    # Create new threads
    index = 0
    for ambulance in list_of_ambulances:
        threads_list.append(SamuOperatorSlave(ambulance, index, "operador_samu_" + str(index)))
        index = index + 1

    # Start new Threads
    for i in range(threads_number):
        print('Reconstruction path, threading number {} working....'.format(threads_list[i].tid))
        threads_list[i].start()

    # Wait for all threads to complete
    for t in threads_list:
        t.join()

    return list_of_ambulances

def start_samu_threadings_dijkstra(edges_list, threads_number, accident_location):
    if len(accident_location) == 7:
        del accident_location[:1]
    else:
        raise

    index = 0
    for edges_map in edges_list:
        # Build the graph first them send the graph to the class ambulance
        graph_mapping=Graph.newGraphFromEdgesMap(edges_map, len(edges_map))
        list_of_ambulances.append(AmbulancePositionSystem(graph=graph_mapping,
            name="ambulance_ambulancia_" + str(index),
            # for each file we send the emegency localization to the APS builder
            emergency=accident_location[index],
            # each file have we build the localizations extracting the last row
            localizations=[edges_map[:1][0][0], edges_map[:1][0][1]],
            # than we choose a strategy called DIJKSTRA to process the data
            algorithm_type='DIJKSTRA'))
        index = index + 1

    # Create new threads
    index = 0
    for ambulance in list_of_ambulances:
        threads_list.append(SamuOperatorSlave(ambulance, index, "operador_samu_" + str(index)))
        index = index + 1

    # Start new Threads
    for i in range(threads_number):
        print('Reconstruction path, threading number {} working....'.format(threads_list[i].tid))
        threads_list[i].start()

    # Wait for all threads to complete
    for t in threads_list:
        t.join()

    return list_of_ambulances


def command_help_text():
    print("(1) python app.py -d grafos v1 v2 v3 v4 v5 v6")
    print("(2) python app.py --edsger-dijkstra grafos v1 v2 v3 v4 v5 v6")
    print("(3) python app.py -f dat v1 v2")
    print("(4) python app.py ---floyd-warshall dat v1 v2")
    print("(5) python app.py -e (optional export)")
    print("(6) python app.py -h (help)")

def main(argv):

    try:
        opts, args = getopt.getopt(argv, "h|f|d|e", ['--floyd-warshall', '--edsger-dijkstra'])
    except getopt.GetoptError:
        command_help_text()
        raise Warning("warning: did you forget parameters?")
    for opt, arg in opts:
        if opt in ['-h', '--help']:
            command_help_text()
            sys.exit()
        elif opt in ("-f", "--floyd-warshall"):
            if os.path.exists(args[0]):
                number_of_files, data_files_list = FileReader.readFiles(args[0])
                start_samu_threadings_floyd(edges_list=data_files_list, threads_number=number_of_files, accident_location=args)
                print('visit results_floyd directory to see your results\n')
                if not os.path.exists('results_floyd'):
                    try:
                        os.makedirs('results_floyd')
                    except IOError:
                        raise Exception("it was impossible to create the given directory name\n")
                for ambulances in list_of_ambulances:
                    FileReader.writef('results_floyd' + os.path.sep + 'results_floyd_{}.txt'.format(ambulances.name), ambulances.__str__())
            else:
                raise Exception("such directory called {} doesnt exist!".format(args[0]))
        elif opt in ("-d", "--edsger-dijkstra"):
            if os.path.exists(args[0]):
                number_of_files, data_files_list = FileReader.readFiles(args[0])
                start_samu_threadings_dijkstra(edges_list=data_files_list, threads_number=number_of_files, accident_location=args)
                print('visit results_dijkstra directory to see your results\n')
                if not os.path.exists('results_dijkstra'):
                    try:
                        os.makedirs('results_dijkstra')
                    except IOError:
                        raise Exception("it was impossible to create the given directory name\n")
                for ambulances in list_of_ambulances:
                    FileReader.writef('results_dijkstra' + os.path.sep + 'results_dijkstra_{}.txt'.format(ambulances.name), ambulances.__str__())
            else:
                raise Exception("such directory called {} doesnt exist!".format(args[0]))
        elif opt in ("-e", "--export"):
            if not os.path.exists('dat'):
                try:
                    os.makedirs('dat')
                except IOError:
                    raise Exception("it was impossible to create the given directory name\n")
            exportNewRegularGraphsToDat()

if __name__ == '__main__':
    main(sys.argv[1:])
