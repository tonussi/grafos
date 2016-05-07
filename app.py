#!/usr/bin/env python
# encoding: utf-8

from Graph import Graph
from FileReader import FileReader
from AmbulancePositionSystem import AmbulancePositionSystem
from RandomGraphGenerator import RandomGraphGenerator

import sys
import getopt
import os
import threading

"""
You can choose -e or --export to build the dat directory this will populate the
dat directory with graphs You also can start the calculation of a graph at time
just input in your terminal the following line: python app.py -a
"dat/<name_of_file>" <emergency_node1> ... <emergency_nodeN> and them fo to the
\"results\" directory at the root of. In this case we have only to nodes emergency!
this software package to pick up your results. note: this program already build
regular graphs with random costs, and this program also makes use of an good
algorithm to to build random regular graphs, see RandomGraphGenerator.py for
more information. Another thing to account is that the program divide the
efforts to find the best path into to running threads. each thread called Samu
Slave will calculate the best path for the ambulance to arrive at his Medical
Center. What I mean is that a ambulance A is related to medical center A and not
to medical center B wich is related to ambulance B.
"""

threads_list = []
list_of_ambulances = []
threadLock = threading.Lock()

class SamuOperatorSlave(threading.Thread):

    def __init__(self, ambulance, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.ambulance = ambulance

    def run(self):
        threadLock.acquire()
        print('Reconstruction path, threading number {} working....'.format(self.threadID))
        self.ambulance.buildMatrixDistancesAndMAtrixRoutes()
        self.ambulance.shortestPath()
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
    # this is just to remove 'dat' directory from the list
    # that must contains only the localtion of the accident
    if len(accident_location) == 3:
        # here we have the two locations because we have two files
        # ambulan1.dat and ambulan2.dat. its one location for each
        del accident_location[:1]

    index = 0
    for edges_map in edges_list:
        # Build the graph first them send the graph to the class ambulance
        graph_mapping=Graph.newGraphFromEdgesMap(edges_map)
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
        threads_list[i].start()

    # Wait for all threads to complete
    for t in threads_list:
        t.join()

    return list_of_ambulances

def start_samu_threadings_dijkstra(edges_list, threads_number, accident_location):
    # this is just to remove 'dat' directory from the list
    # that must contains only the localtion of the accident
    if len(accident_location) == 3:
        # here we have the two locations because we have two files
        # ambulan1.dat and ambulan2.dat. its one location for each
        del accident_location[:1]

    index = 0
    for edges_map in edges_list:
        # Build the graph first them send the graph to the class ambulance
        graph_mapping=Graph.newGraphFromEdgesMap(edges_map)
        list_of_ambulances.append(AmbulancePositionSystem(graph=graph_mapping,
                                                          name="ambulance_ambulancia_" + str(index),
                                                          emergency=accident_location[index],
                                                          localizations=[edges_map[:1][0][0], edges_map[:1][0][1]],
                                                          algorithm_type='DIJKSTRA'))
        index = index + 1

    # Create new threads
    index = 0
    for ambulance in list_of_ambulances:
        threads_list.append(SamuOperatorSlave(ambulance, index, "operador_samu_" + str(index)))
        index = index + 1

    # Start new Threads
    for i in range(threads_number):
        threads_list[i].start()

    # Wait for all threads to complete
    for t in threads_list:
        t.join()

    return list_of_ambulances


def command_help_text():
    print("(1) python app.py -i <DAT_FILE_INPUT> (find best path)")
    print("(2) python app.py -e (export)")
    print("(3) python app.py -h (help)")

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

            if len(args) != 3 or args[0] is not 'dat':
                raise Exception("must be python app.py -f dat <v1> <v2>\n")
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
                os.makedirs('dat')
                try:
                    os.makedirs('dat')
                except IOError:
                    raise Exception("it was impossible to create the given directory name\n")
                raise Exception("dat does not exists in the root directory of this project\n")
        elif opt in ("-d", "--edsger-dijkstra"):

            if len(args) != 6 or args[0] is not 'grafos':
                raise Exception("must be python app.py -d grafos <v1> <v2> <v3> <v4> <v5>\n")
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
                os.makedirs('dat')
                try:
                    os.makedirs('dat')
                except IOError:
                    raise Exception("it was impossible to create the given directory name\n")
                raise Exception("dat does not exists in the root directory of this project\n")

        elif opt in ("-e", "--export"):
            if not os.path.exists('dat'):
                try:
                    os.makedirs('dat')
                except IOError:
                    raise Exception("it was impossible to create the given directory name\n")

            exportNewRegularGraphsToDat()

if __name__ == '__main__':
    main(sys.argv[1:])
