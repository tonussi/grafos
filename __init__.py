# encoding:utf-8

from Graph import Graph
from FileReader import FileReader
from Hospital import Hospital
from RandomGraphGenerator import RandomGraphGenerator
from FloydWarshall import FloydWarshall

import sys
import getopt
import os
import threading
import random

"""
You can choose -e or --export to build the dat directory this will populate the
dat directory with graphs You also can start the calculation of a graph at time
just input in your terminal the following line: python __init__.py -i
"dat/<name_of_file>" and them fo to the \"results\" directory at the root of
this software package to pick up your results. note: this program already build
regular graphs with random costs, and this program also makes use of an good
algorithm to to build random regular graphs, see RandomGraphGenerator.py for
more information. Another thing to account is that the program divide the
efforts to find the best path into to running threads. each thread called Samu
Slave will calculate the best path for the ambulance to arrive at his Medical
Center. What I mean is that a ambulance A is related to medical center A and not
to medical center B wich is related to ambulance B.
"""

threadLock = threading.Lock()
threads_list = []
list_of_ambulances = []

class SamuSlave(threading.Thread):

    def __init__(self, hospital, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.hospital = hospital

    def run(self):
        threadLock.acquire()
        print('reconstruction path, threading number {} working....'.format(self.threadID))
        self.hospital.buildMatrixDistancesAndMAtrixRoutes()
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

def start_samu_threadings(edges_list, threads_number, accident_location):
    # this is just to remove 'dat' directory from the list
    # that must contains only the localtion of the accident
    if len(accident_location) == 3:
        del accident_location[:1]

    index = 0
    for edges_map in edges_list:
        list_of_ambulances.append(Hospital(graph=edges_map, name="hospital_ambulancia_" + str(index),
                                           emergency=accident_location, localization=edges_map[-1]))
        print(list_of_ambulances[index])
        index = index + 1

    # Create new threads
    index = 0
    for hospital in list_of_ambulances:
        threads_list.append(SamuSlave(hospital, index, "operador_samu_" + str(index)))
        index = index + 1

    # Start new Threads
    for i in range(threads_number):
        threads_list[i].start()

    # Wait for all threads to complete
    for t in threads_list:
        t.join()

    return list_of_ambulances

def command_help_text():
    print("(1) python __init__.py -i <DAT_FILE_INPUT> (find best path)")
    print("(2) python __init__.py -e (export)")
    print("(3) python __init__.py -h (help)") 

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h|a|e", ['--rota-acidente'])
    except getopt.GetoptError:
        command_help_text()
        raise Warning("warning: did you forget parameters?")
    for opt, arg in opts:
        if opt in ['-h', '--help']:
            command_help_text()
            sys.exit()
        elif opt in ("-a", "--rota-acidente"):
            # must be 'args' just for this case
            # so we can get the values ao a edges
            # that its marked with an accident
            # them the threads will start to calculate
            # the routes and display the list of routes
            # in sorted form
            print (opt, args)
            if len(args) != 3 and args[0] is not 'dat':
                raise Exception("must be 2 values to find a specific edge you need to type\n\
python __init__.py -a (or --route-accident) <dir> <number> <number> where\n\
<dir> is the name of the directory where there are files with the graphs\n\
data <number> are valid vertex that exist in the files all files must be\n\
of equal node numbers but can have distinct costs for each edge\n")
            if os.path.exists(args[0]):
                number_of_files, data_files_list = FileReader.readFiles(args[0])
                start_samu_threadings(edges_list=data_files_list, threads_number=number_of_files, accident_location=args)
            else:
                os.makedirs('dat')
                try:
                    os.makedirs('dat')
                except IOError:
                    raise Exception("it was impossible to create the given directory name\n")
                raise Exception("dat does not exists in the root directory of this project\n\
we created one for you, now all you have to do is put files with graph data\n\
into the dat directory\n")

        elif opt in ("-e", "--export"):
            if not os.path.exists('dat'):
                try:
                    os.makedirs('dat')
                except IOError:
                    raise Exception("it was impossible to create the given directory name\n")

            exportNewRegularGraphsToDat()

    print('visit results directory to see your results\n')

    if not os.path.exists('results'):
        try:
            os.makedirs('results')
        except IOError:
            raise Exception("it was impossible to create the given directory name\n")

    for ambulances in list_of_ambulances:
        FileReader.writef('results' + os.path.sep + 'results_{}.txt'.format(ambulances.name), ambulances.__str__())

if __name__ == '__main__':
    main(sys.argv[1:])
